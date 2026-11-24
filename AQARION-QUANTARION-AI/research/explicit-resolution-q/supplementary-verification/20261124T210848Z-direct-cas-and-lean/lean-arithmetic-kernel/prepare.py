import hashlib
import json
import pathlib
import re
import subprocess
import urllib.request

OUT = pathlib.Path(__file__).resolve().parent
PIN = "leanprover/lean4:v4.35.0-rc4"
BASE = "66efa358583f3331afbd9ee4c898a26c8e089fb3"

SOURCE = (
    pathlib.Path.home()
    / "aq_p2_lean_preflight_WdNg9mBM"
    / "AQARION-LEAN"
)

def generate():
    fields = [
        ("n"+str(i), "0 ≤ a"+str(i), "0 < a"+str(i))
        for i in range(4)
    ]

    fields += [
        (
            "p"+str(i)+str(j),
            "k ≤ a%d + a%d" % (i,j),
            "k < a%d + a%d" % (i,j),
        )
        for i in range(4)
        for j in range(i+1,4)
    ]

    lines = [
        "import Lean.Elab.Tactic.Omega",
        "set_option autoImplicit false",
        "namespace Aqarion.P2Arithmetic",
        "",
    ]

    names = []

    for title,index in (
        ("Feasible",1),
        ("StrictFeasible",2),
    ):
        lines.append(
            "structure "+title
            +" (a0 a1 a2 a3 k : Int) : Prop where"
        )
        lines += [
            "  "+field[0]+" : "+field[index]
            for field in fields
        ]
        lines.append("")

    def theorem(name, statement, proof):
        names.append("Aqarion.P2Arithmetic."+name)
        lines.extend(
            ["theorem "+name+" "+statement+" := by"]
            + ["  "+line for line in proof.splitlines()]
            + [""]
        )

    generators = [("A",[0,0,0,0,-1])]

    generators += [
        ("E"+str(i),[int(j == i) for j in range(4)]+[0])
        for i in range(4)
    ]

    generators += [
        ("B"+str(i),[int(j != i) for j in range(4)]+[1])
        for i in range(4)
    ]

    generators += [("C",[1,1,1,1,2])]

    for name,coordinates in generators:
        arguments = " ".join(
            "("+str(value)+")" if value < 0 else str(value)
            for value in coordinates
        )
        theorem(
            "generator_"+name,
            ": Feasible "+arguments,
            "constructor <;> omega",
        )

    lines.append("variable {a0 a1 a2 a3 k : Int}\n")

    for i in range(4):
        target = " ".join(
            "a"+str(j) if j == i
            else "(a%d - 1)" % j
            for j in range(4)
        )

        theorem(
            "subtract_B%d_zero" % i,
            "(h : Feasible a0 a1 a2 a3 k) "
            "(hk : 1 ≤ k) "
            "(hz : a%d = 0) : Feasible %s (k - 1)"
            % (i,target),
            "cases h\nconstructor <;> omega",
        )

    theorem(
        "subtract_C",
        "(h : Feasible a0 a1 a2 a3 k) "
        "(h0 : 1 ≤ a0) (h1 : 1 ≤ a1) "
        "(h2 : 1 ≤ a2) (h3 : 1 ≤ a3) : "
        "Feasible (a0 - 1) (a1 - 1) (a2 - 1) "
        "(a3 - 1) (k - 2)",
        "cases h\nconstructor <;> omega",
    )

    theorem(
        "subtract_B0_at_one",
        "(h : Feasible a0 a1 a2 a3 1) "
        "(h1 : 1 ≤ a1) (h2 : 1 ≤ a2) (h3 : 1 ≤ a3) : "
        "Feasible a0 (a1 - 1) (a2 - 1) (a3 - 1) 0",
        "cases h\nconstructor <;> omega",
    )

    theorem(
        "strict_iff_shifted",
        ": StrictFeasible a0 a1 a2 a3 k ↔ "
        "Feasible (a0 - 1) (a1 - 1) (a2 - 1) "
        "(a3 - 1) (k - 1)",
        "constructor\n"
        "· intro h\n"
        "  cases h\n"
        "  constructor <;> omega\n"
        "· intro h\n"
        "  cases h\n"
        "  constructor <;> omega",
    )

    theorem(
        "bound_after_B",
        "(n : Nat) (k : Int) "
        "(h : k ≤ ((n + 1 : Nat) : Int)) : "
        "k - 1 ≤ (n : Int)",
        "omega",
    )

    theorem(
        "bound_after_C",
        "(n : Nat) (k : Int) "
        "(h : k ≤ ((n + 1 : Nat) : Int)) : "
        "k - 2 ≤ (n : Int)",
        "omega",
    )

    theorem(
        "bound_by_toNat",
        "(k : Int) : k ≤ (Int.toNat k : Int)",
        "omega",
    )

    lines += [
        "end Aqarion.P2Arithmetic",
        "",
    ]
    lines += [
        "#print axioms "+name
        for name in names
    ]

    return "\n".join(lines)+"\n",names

def main():
    def git(*args):
        return subprocess.run(
            ["git","-C",str(SOURCE),*args],
            check=True,
            stdout=subprocess.PIPE,
        ).stdout.decode().strip()

    if git("rev-parse","HEAD") != BASE:
        raise SystemExit(
            "Lean source checkout differs from the inspected commit."
        )

    actual = git(
        "show",
        BASE+":PROJECTS/PBCore006/lean-toolchain",
    )

    if actual != PIN:
        raise SystemExit("Pinned compiler mismatch.")

    lean,names = generate()

    if re.search(
        r"\b(sorry|admit|axiom|native_decide)\b",
        lean,
    ):
        raise SystemExit("Unexpected proof escape token.")

    (OUT/"ArithmeticKernel.lean").write_text(lean)

    (OUT/"NegativeControl.lean").write_text(
        "import Lean.Elab.Tactic.Omega\n"
        "theorem rejects_false : (0 : Int) = 1 := by\n"
        "  omega\n"
    )

    (OUT/"lean-toolchain").write_text(PIN+"\n")

    (OUT/"THEOREMS.json").write_text(
        json.dumps(names,indent=2)+"\n"
    )

    refs = subprocess.run(
        [
            "git","ls-remote",
            "https://github.com/leanprover/elan.git",
            "refs/heads/master",
        ],
        check=True,
        stdout=subprocess.PIPE,
    ).stdout.decode().split()

    if not refs or not re.fullmatch("[0-9a-f]{40}",refs[0]):
        raise SystemExit("Cannot pin official bootstrap source.")

    commit = refs[0]
    url = (
        "https://raw.githubusercontent.com/leanprover/elan/"
        +commit+"/elan-init.sh"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent":"AQARION-Lean-preparation"},
    )

    with urllib.request.urlopen(request,timeout=60) as response:
        data = response.read()

    (OUT/"elan-init.sh").write_bytes(data)

    (OUT/"PINNING.json").write_text(json.dumps({
        "toolchain": PIN,
        "lean_source_commit": BASE,
        "toolchain_source":
            "PROJECTS/PBCore006/lean-toolchain",
        "bootstrap_commit": commit,
        "bootstrap_url": url,
        "bootstrap_sha256":
            hashlib.sha256(data).hexdigest(),
        "mathlib_required": False,
        "candidate_status": "UNCOMPILED",
        "ubuntu_private_elan_home":
            "/root/.elan-aqarion-p2",
        "scope": (
            "Arithmetic helpers only; not full semigroup "
            "generation or the resolution proof."
        ),
    },indent=2)+"\n")

    source_names = [
        "prepare.py",
        "finish.py",
        "run_ubuntu.sh",
        "ArithmeticKernel.lean",
        "NegativeControl.lean",
        "lean-toolchain",
        "THEOREMS.json",
        "elan-init.sh",
        "PINNING.json",
    ]

    (OUT/"SOURCE_SHA256SUMS").write_text(
        "\n".join(
            hashlib.sha256(
                (OUT/name).read_bytes()
            ).hexdigest()+"  "+name
            for name in source_names
        )+"\n"
    )

    print("CANDIDATE_STATUS=UNCOMPILED")
    print("TOOLCHAIN="+PIN)
    print("NAMED_ARITHMETIC_THEOREMS="+str(len(names)))
    print("BOOTSTRAP_SOURCE_COMMIT="+commit)
    print("\n===== LEAN CANDIDATE SOURCE =====\n"+lean)

if __name__ == "__main__":
    main()
