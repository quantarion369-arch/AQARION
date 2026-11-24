from fractions import Fraction as F
import datetime
import hashlib
import json
import pathlib
import time

START = time.time()
OUT = pathlib.Path(__file__).resolve().parent

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def mul(A, B):
    return [
        [
            sum((x*y for x, y in zip(row, col)), F(0))
            for col in zip(*B)
        ]
        for row in A
    ]

def ident(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]

def minus(A, B):
    return [
        [x-y for x, y in zip(a, b)]
        for a, b in zip(A, B)
    ]

def infnorm(A):
    return max(sum(abs(x) for x in row) for row in A)

def dobrushin(A):
    return max(
        sum(abs(x-y) for x, y in zip(a, b))/2
        for a in A for b in A
    )

def aggregation(P, labels):
    order = list(dict.fromkeys(labels))
    ids = {label: i for i, label in enumerate(order)}
    lab = [ids[label] for label in labels]
    n, k = len(lab), len(order)

    S = [
        [F(lab[i] == j) for j in range(k)]
        for i in range(n)
    ]
    L = [
        [F(lab[i] == j, lab.count(j)) for i in range(n)]
        for j in range(k)
    ]

    R = mul(S, L)
    Q = mul(mul(L, P), S)
    E = minus(mul(P, S), mul(S, Q))
    D = mul(mul(minus(ident(n), R), P), R)

    return S, L, R, Q, E, D

P = [
    [F(3,5), 0, F(2,5), 0],
    [F(2,5), 0, F(3,5), 0],
    [0, 0, 0, 1],
    [0, 0, 0, 1],
]

need(
    all(min(row) >= 0 and sum(row) == 1 for row in P),
    "P must be stochastic",
)

system = aggregation(P, (0,0,1,2))

need(
    system == aggregation(P, (10,10,20,30)),
    "Partition relabeling invariance",
)

S, L, R, Q, E, D = system

need(mul(L, S) == ident(3), "LS = I")
need(mul(R, R) == R, "R is idempotent")
need(mul(E, L) == D, "EL = D")
need(mul(D, S) == E, "DS = E")
need(
    infnorm(D) == infnorm(E) == F(1,5),
    "Defect norm equality",
)
need(
    all(min(row) >= 0 and sum(row) == 1 for row in Q),
    "Q must be stochastic",
)

pt = [ident(4)]
qt = [ident(3)]

for _ in range(40):
    pt.append(mul(pt[-1], P))
    qt.append(mul(qt[-1], Q))

eta = [infnorm(mul(A, E)) for A in pt]
tau = [dobrushin(A) for A in qt]

need(
    eta == [F(1,5)*F(3,5)**t for t in range(41)],
    "Fine defect profile through power 40",
)
need(
    tau == [F(1)] + [
        F(1,2)**(t-1) for t in range(1,41)
    ],
    "Coarse contraction profile through power 40",
)

errors = []
bounds = []

for t in range(41):
    difference = minus(
        mul(pt[t], S),
        mul(S, qt[t]),
    )

    actual = infnorm(difference)/2
    bound = sum(
        (
            eta[r]*tau[t-1-r]/2
            for r in range(t)
        ),
        F(0),
    )

    need(
        actual <= min(F(1), bound),
        "Dual-profile inequality",
    )

    errors.append(actual)
    bounds.append(bound)

    if t:
        closed = (
            F(1,10)
            if t == 1
            else (
                F(33,50)*F(3,5)**(t-2)
                - F(1,2)*F(1,2)**(t-2)
            )
        )
        need(bound == closed, "Dual closed form")

    if t <= 12:
        telescoped = [[F(0)]*3 for _ in range(4)]

        for r in range(t):
            term = mul(mul(pt[r], E), qt[t-1-r])
            telescoped = [
                [x+y for x, y in zip(a, b)]
                for a, b in zip(telescoped, term)
            ]

        need(
            telescoped == difference,
            "Exact telescoping identity",
        )

need(
    P[-1] == [0,0,0,1] and Q[-1] == [0,0,1],
    "Common absorbing target",
)

fine_tail = max(sum(row[:-1]) for row in pt[6])
coarse_tail = max(sum(row[:-1]) for row in qt[6])
tail = max(fine_tail, coarse_tail)

need(
    tail == F(243,3125) and tail < F(11,100),
    "All-time absorbing-tail certificate",
)
need(
    max(errors[:6]) == F(11,100),
    "Exact finite-prefix maximum",
)
need(
    [
        t for t in range(6)
        if errors[t] == F(11,100)
    ] == [2,3],
    "Actual maximizing times",
)

need(
    F(33,125) > F(1,4),
    "Dual decreasing-tail inequality",
)
need(
    bounds[1] == F(1,10)
    and bounds[2] == F(4,25),
    "Dual-profile maximum prefix",
)

def write(name, data):
    (OUT/name).write_text(
        json.dumps(data, indent=2, default=str) + "\n"
    )

home = pathlib.Path.home()

candidates = [
    home / (
        "AQARION-tablet/AQARION-QUANTARION-AI/"
        "evidence/AQ/detection_signatures_n4.json"
    )
]

candidates += sorted(home.glob(
    "AQARION-release-control-*/checkout/"
    "AQARION-QUANTARION-AI/evidence/AQ/"
    "detection_signatures_n4.json"
))

diagnosis = []

for path in dict.fromkeys(candidates):
    item = {"path": str(path), "status": "NOT_FOUND"}

    if path.is_file():
        data = path.read_bytes()
        item.update(
            bytes=len(data),
            sha256=hashlib.sha256(data).hexdigest(),
        )

        try:
            text = data.decode("utf-8")
            item["characters"] = len(text)
            json.loads(text)
            item["status"] = "VALID_JSON"

        except json.JSONDecodeError as error:
            item.update(
                status="MALFORMED_STORED_JSON",
                message=error.msg,
                line=error.lineno,
                column=error.colno,
                position=error.pos,
                at_end=error.pos == len(text),
            )

        except UnicodeDecodeError as error:
            item.update(
                status="UTF8_ERROR",
                message=str(error),
            )

    diagnosis.append(item)

write("SOURCE_JSON_DIAGNOSIS.json", diagnosis)

receipt = {
    "status": "WITNESS_ARITHMETIC_PASS",
    "scope": (
        "Explicit four-state witness only; "
        "not imported verifier replay or Lean verification"
    ),
    "utc": datetime.datetime.now(
        datetime.timezone.utc
    ).isoformat(),
    "source_sha256": hashlib.sha256(
        pathlib.Path(__file__).read_bytes()
    ).hexdigest(),
    "Q": Q,
    "epsilon": F(1,5),
    "profiles_checked_through": 40,
    "telescoping_checked_through": 12,
    "dual_all_time_max": F(4,25),
    "actual_all_time_max": F(11,100),
    "actual_maximizing_times": [2,3],
    "tail_start": 6,
    "all_later_times_error_bound": tail,
    "finite_error_values_t0_to6": errors[:7],
    "justification": (
        "Finite prefix plus absorbing-state tail monotonicity; "
        "dual closed form plus monotone ratio "
        "of its difference terms."
    ),
    "source_json_diagnostics_are_separate_from_math_status": True,
    "elapsed_seconds": time.time()-START,
}

write("WITNESS_RECEIPT.json", receipt)

(OUT/"PROOF_NOTES.txt").write_text(
    "Actual error is maximum row TV by convexity. "
    "At t=6, fine mass outside the absorbing state is at most "
    "243/3125; coarse mass is at most 1/32. "
    "Both are nonincreasing thereafter. "
    "TV between distributions sharing an absorbing target "
    "is at most the larger mass outside that target. "
    "The t=0..5 maximum is 11/100, attained at t=2,3. "
    "Thus the all-time maximum is exactly 11/100.\n"
    "Dual bound: B1=1/10; for t>=2, "
    "Bt=(33/50)(3/5)^(t-2)-(1/2)(1/2)^(t-2). "
    "Its difference is negative because 33/125>1/4 "
    "and the negative term's relative dominance grows by 6/5. "
    "Hence the dual maximum is B2=4/25.\n"
    "No truncation mechanism is inferred "
    "from parser offsets alone.\n"
)

checks = []

for path in sorted(OUT.iterdir()):
    if (
        path.is_file()
        and path.name not in ("SHA256SUMS", "console.log")
    ):
        checks.append(
            hashlib.sha256(path.read_bytes()).hexdigest()
            + "  " + path.name
        )

(OUT/"SHA256SUMS").write_text(
    "\n".join(checks) + "\n"
)

print("RELABELING=PASS")
print("DEFECT_IDENTITIES=PASS")
print("PROFILE_CHECKS_THROUGH_40=PASS")
print("EXACT_TELESCOPING_THROUGH_12=PASS")
print("DUAL_ALL_TIME_MAX=4/25 at t=2")
print("ACTUAL_ALL_TIME_MAX=11/100 at t=2,3")
print("ALL_T_GE_6_ERROR_BOUND=243/3125 < 11/100")
print("WITNESS_ARITHMETIC_STATUS=PASS")

print("\nSOURCE FILE DIAGNOSTICS:")
print(json.dumps(diagnosis, indent=2))

print("\nRESULTS:", OUT)
