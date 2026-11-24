import collections
import csv
import datetime
import hashlib
import io
import json
import pathlib
import platform
import sys

OUT = pathlib.Path(__file__).resolve().parent
HOME = pathlib.Path.home()

FROZEN = (
    "1a9f22866a38f135859a41616f18a5756e7fdecc921a2f36b078c20db334a8a0"
)
EXPORT = "AQARION-complete-complex-20261114T163933580791Z.json"

SPECS = [
    (
        "qq",
        HOME/"aq_p2_json_native_CGdjVwxB",
        "PASS_ARITHMETIC_WITH_EXPLICIT_THEOREM_DEPENDENCIES",
        7,
    ),
    (
        "divisor",
        HOME/"aq_p2_divisor_b3X2omUU",
        "PASS_COMPLETE_DIVISOR_HOMOLOGY_WITH_EXPLICIT_DEPENDENCIES",
        11,
    ),
    (
        "integral",
        HOME/"aq_p2_integral_components_X9sQlk2K",
        "PASS_UNIMODULAR_COMPONENT_CERTIFICATES",
        13,
    ),
]

CASES = [
    ("D2",4,3),
    ("D2",5,39),
    ("D2",6,180),
    ("D3",6,8),
    ("D3",7,64),
    ("D3",8,277),
    ("D3",9,937),
    ("D4",8,6),
    ("D4",9,38),
]

def need(ok, message):
    if not ok:
        raise AssertionError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def save(name, value):
    (OUT/name).write_text(
        json.dumps(value, indent=2) + "\n"
    )

def read_bundle(root, status, count):
    manifest = (root/"SHA256SUMS").read_bytes()
    files = {}

    for line in manifest.decode().splitlines():
        if not line.strip():
            continue

        digest,name = line.split("  ",1)
        relative = pathlib.PurePosixPath(name)

        need(
            relative.parts
            and not relative.is_absolute()
            and ".." not in relative.parts
            and name not in files,
            "Unsafe manifest name",
        )

        path = root.joinpath(*relative.parts)

        need(
            path.is_file() and not path.is_symlink(),
            "Missing or symlinked artifact: " + name,
        )

        path.resolve().relative_to(root.resolve())
        data = path.read_bytes()

        need(
            sha(data) == digest,
            "Checksum mismatch: " + name,
        )
        files[name] = data

    need(
        len(files) == count,
        "Unexpected artifact count in " + str(root),
    )

    receipt = json.loads(files["RECEIPT.json"])

    need(
        receipt["status"] == status,
        "Prior status mismatch",
    )
    need(
        sha(files["verify.py"]) == receipt["source_sha256"],
        "Prior verifier/receipt mismatch",
    )
    need(
        sha(files["inputs/"+EXPORT]) == FROZEN,
        "Export identity mismatch",
    )

    files["SHA256SUMS"] = manifest
    return files,receipt,sha(manifest)

def upper_bounds(shifts):
    polynomial_dimensions = [1]+[0]*9

    for weight in [1]*5+[2]*5:
        for degree in range(weight,10):
            polynomial_dimensions[degree] += (
                polynomial_dimensions[degree-weight]
            )

    numerator = {
        0:1, 3:-8, 4:-3, 5:24,
        7:-24, 8:3, 9:8, 12:-1,
    }

    free_numerators = [
        collections.Counter(source)
        for source in shifts
    ]

    def subtract(a,b):
        result = collections.Counter(a)
        for degree,value in b.items():
            result[degree] -= value
        return {
            degree:value
            for degree,value in result.items()
            if value
        }

    k1 = dict(numerator)

    for degree,value in free_numerators[1].items():
        k1[degree] = k1.get(degree,0)+value

    k1[0] -= 1
    k1 = {
        degree:value
        for degree,value in k1.items()
        if value
    }

    k2 = subtract(free_numerators[2],k1)
    k3 = subtract(free_numerators[3],k2)

    numerators = {"D2":k1,"D3":k2,"D4":k3}
    rows = []

    for name,degree,expected in CASES:
        dimension = sum(
            coefficient*polynomial_dimensions[degree-j]
            for j,coefficient in numerators[name].items()
            if 0 <= j <= degree
        )

        need(
            dimension == expected,
            "Upper-bound coefficient mismatch",
        )

        dependency = {
            "D2": "Endpoint presentation and Hilbert series",
            "D3": "After D2 generation and minimal-cover proof",
            "D4": "After D3 generation and minimal-cover proof",
        }[name]

        rows.append([
            name,degree,dimension,dependency
        ])

    return polynomial_dimensions,numerators,rows

THEOREM = r'''# Project 2: proof draft for the frozen ten-variable export

Status: THEOREM_DRAFT_SUPPORTED_BY_REPLAYED_CERTIFICATES.

This document assembles an ordinary mathematical argument and computational
evidence. It is not Lean verification, peer review, or a novelty assertion.
Earlier receipts are historical records and are copied without editing.

## Object and proposed theorem

Let P_K=K[A,E0,E1,E2,E3,B0,B1,B2,B3,C], with positive weights
(1,1,1,1,1,2,2,2,2,2).

Let the five differential matrices be exactly those in the frozen export
identified by PROVENANCE.json and the evidence inputs.

The proposed theorem is that they form a minimal graded free resolution
of K[S] over P_K for every field K, where S is generated by

A=(0,0,0,0,-1),
E_i=(e_i,0),
B_i=(sum_{j!=i}e_j,1),
C=(1,1,1,1,2).

This statement concerns this export, not all parameter values of Project 2.
P(-d) denotes a free summand whose generator has degree d.

## Lemma 1: semigroup, lattice, facets and positive grading

S is exactly the integral points satisfying a_i>=0 and a_i+a_j>=k.

One inclusion follows by checking the ten generators.
For the converse:

* k<=0: use sum a_i E_i + (-k) A.

* k=1: at most one a_i is zero. Choose that i, if present, otherwise
  any i. Subtract B_i; other coordinates stay nonnegative and k becomes 0.

* k>=2 and all a_i>=1: subtract C.
  Every pair form a_i+a_j-k is unchanged.

* k>=2 and a_i=0: other a_j>=k. Subtract B_i.
  For pairs containing i, the new form is a_j-k>=0.
  For the other pairs it is a_j+a_l-k-1>=k-1>=1.
  All coordinates remain nonnegative.

Positive k strictly decreases, so the procedure terminates.

The determinant of A,E0,E1,E2,E3 is -1, giving group lattice Z^5.

The forms a_i and a_i+a_j-k are primitive.

Each coordinate facet has an interior point in its hyperplane:
a_i=0, other a_j=2, k=1.

Each pair facet has a_i=a_j=1, other coordinates 2, k=2.

All other inequalities are strict at these points, proving irredundancy.
The point kappa=(1,1,1,1,1) is strictly interior, so the cone is
full-dimensional.

The functional w=sum a_i-k is positive away from zero:
k<=sum a_i/2; if all a_i=0, then k<=0 and w=-k.
Hence the cone is pointed.

## Lemma 2: endpoint presentation over every field

Let J_Z be generated by the fourteen entries of D1.
Each is a pure monomial difference with coefficients +1,-1.

Let ~ be the congruence on N^10 generated by those monomial relations.
For any coefficient ring B,

B[x]/J_B = B[N^10/~].

Monomials in the same congruence class are identified, and the quotient
is free as a B-module on the congruence classes.

The rational saturation and localized graph calculation identifies
Q[x]/J_Q with Q[S].

The induced surjective monoid map N^10/~ -> S must therefore be
injective: two distinct classes with the same image would give a
nonzero difference of basis vectors in the rational algebra kernel.

Thus N^10/~ is S.
In particular J_K is the semigroup kernel over every field, and the
integral endpoint is Z[S].

For the rational identification, localizing at A gives

B_i=(product_{j!=i} E_j)/A,
C=E0 E1 E2 E3/A^2.

The quotient after localization is Q[A,A^-1,E0,E1,E2,E3].
The replayed identity J_Q:A^infinity=J_Q gives the unlocalized kernel.

## Lemma 3: canonical shift and finite Betti-degree interval

All ten primitive facet forms take value one on kappa.

Consequently interior lattice points equal kappa+S:
subtracting kappa from an interior lattice point leaves all integral
facet values >=0, and adding kappa makes every value positive.

Standard normal-semigroup Cohen-Macaulay and canonical-module theorems
therefore give a Gorenstein endpoint over every field.

The semigroup rank is 5, and the polynomial ring has 10 variables.
Auslander-Buchsbaum gives projective dimension 5.

The scalar canonical generator degree is w(kappa)=3.
The ambient variable-weight sum is 15, so the last scalar shift is 12.

Multigraded:

sum g_j=(5,5,5,5,5),
c=sum g_j-kappa=(4,4,4,4,4).

Abstract minimal-resolution duality gives

beta(i,b)=beta(5-i,c-b).

Every nonzero Betti degree b belongs to S; its dual degree does too.
Thus all Betti degrees lie in S intersect (c-S), exactly

0<=a_i<=4,
max_pair(a_i+a_j)-4 <= k <= min_pair(a_i+a_j).

There are 835 such degrees.
This cutoff does not assume exactness of the displayed matrices.

## Lemma 4: independent Betti data

For each degree b, the divisor complex has a face F when

b-sum(g_j:j in F) belongs to S.

The divisor/Koszul formula is

beta(i,b)=dim reduced_H_(i-1)(Delta_b;K).

The positive monoid embeds into N^10 by its rank-five facet map, so
its negative last-coordinate generator is no obstruction to the formula.

The preserved complete divisor audit examines all 835 degrees, checks
boundary compositions, computes 2956 integer Smith forms and also
constructs and replays 2956 integral unit-reduction traces.

Every boundary is equivalent over Z to a unit diagonal plus zero.
The reduced homology is torsion-free, and its dimensions are unchanged
over every field.

The 54 nonzero multigraded positions match the export.

The scalar Betti shifts are:

F0: 0^1
F1: 3^8,4^6
F2: 4^3,5^24,6^8
F3: 6^8,7^24,8^3
F4: 8^6,9^8
F5: 12^1.

These are endpoint invariants computed without using the displayed matrices.

## Lemma 5: exact ranks and full kernel-component dimensions

The integer component audit reconstructs each component from the frozen
matrices and reaches a unit diagonal plus a zero residual in all nine cases.

A unit pivot allows integral row and column elimination.
The saved and replayed traces therefore certify exact ranks over every field.
This is distinct from the older modular lower-bound audit.

Let

Delta=(1-t)^5(1-t^2)^5,
N=1-8t^3-3t^4+24t^5-24t^7+3t^8+8t^9-t^12.

Then H_P=1/Delta and H_R=N/Delta.

Write Z_i=ker(D_i:F_i -> F_(i-1)).

Once D1 presents the endpoint,

H_Z1=(3t^4+24t^5-24t^7+3t^8+8t^9-t^12)/Delta.

Its degree 4,5,6 dimensions are 3,39,180.

ONLY AFTER D2 is shown to generate Z1, subtract to obtain

H_Z2=(8t^6+24t^7-3t^8-8t^9+t^12)/Delta.

Its degree 6,7,8,9 dimensions are 8,64,277,937.

ONLY AFTER D3 is shown to generate Z2, subtract to obtain

H_Z3=(6t^8+8t^9-t^12)/Delta.

Its degree 8,9 dimensions are 6,38.

UPPER_BOUND_TABLE.csv and UPPER_BOUND_RECONSTRUCTION.json record
these coefficient calculations.

Betti multiplicities are not being substituted for full kernel dimensions.

## Theorem proof: induction through the displayed maps

D1 is a minimal presentation: its fourteen generators have the same
numbers and degrees as the endpoint's first Betti data.

Z1 therefore has minimal generator degrees 4,5,6.

Composition zero gives im D2 subset Z1.
The certified component ranks match the full dimensions in Lemma 5
in each generator degree. Thus D2 generates all of Z1.

Its source has exactly the endpoint's second Betti counts in each degree,
so it is a minimal free cover.

Now the computed H_Z2 is justified.
The endpoint's third Betti data put generator degrees at 6,7,8.

Certified D3 ranks match those full components, so im D3=Z2.
The degree-nine check is supplementary.
Its source counts match the minimal cover, so D3 is minimal.

Now H_Z3 is justified.
Its generator degrees are 8,9, from the fourth Betti data.
The D4 ranks 6,38 imply im D4=Z3, and the source is minimal.

The abstract fifth Betti data and length-five resolution imply

ker D4 is P_K(-12).

D5 maps P_K(-12) into it homogeneously.
An entry B0 E0-A C is nonzero over every field, so D5 is nonzero.

After a graded identification of the kernel with P_K(-12), this map
is multiplication by a nonzero element of (P_K)_0=K.

It is an isomorphism onto the kernel and is injective.

All differential entries have zero constant term; the resolution is minimal.

No rational gcd certificate was transferred to positive characteristic.

## Integral corollary, after acceptance of the fieldwise proof

Every scalar-degree piece is a finite complex of finite free abelian groups.

The universal coefficient injection

H_i(C)_d tensor F_p -> H_i(C tensor F_p)_d

and the fieldwise theorem make the left side zero for every prime, i>0.

A nonzero finitely generated abelian group cannot have this property.

Thus positive integral homology vanishes in every degree.
The integral endpoint is Z[S], from Lemma 2.

This proves integral exactness.
Minimality is asserted here only over fields.

## Limits

This is a reviewed-in-conversation proof draft, not independent peer review.

The assembly script checks file identity, receipt consistency,
Betti comparisons and coefficient arithmetic.
It does NOT rerun the three mathematical audits.

The theorem relies on the finite certificates and the named standard
theorems. It is not a proof-assistant certificate.

No general-parameter theorem, novelty, recovered constructor,
basis-bridge verification, or Macaulay2 execution is claimed.
'''

SOURCES = '''# External theorem inputs and citation boundaries

1. Winfried Bruns, Normal Semigroup Rings.
https://www.math.ucdavis.edu/~deloera/MISC/LA-BIBLIO/trunk/Bruns/brunsnormalsemigrouprings.pdf

Use: positive weighted grading, minimal covers, Cohen-Macaulayness,
canonical module and normal-semigroup interior description.

2. Ornella Greco and Ivan Martino, Cohen-Macaulay Property and linearity
of pinched Veronese Rings, arXiv:1709.10461, Theorem 1.4.
https://ar5iv.labs.arxiv.org/html/1709.10461

Use the general divisor-complex formula in the preliminaries.
This does not identify our algebra with a pinched Veronese ring.

3. Laura Felicia Matusevich and Ignacio Ojeda,
Binomial ideals and congruences on N^n, arXiv:2003.03861.
https://arxiv.org/abs/2003.03861

Background for monoid congruences. The specialized pure-difference
presentation argument is written in THEOREM_DRAFT.md.
Do not claim an arbitrary binomial ideal is determined by its congruence.

4. John Rognes, The Universal Coefficient Theorem, 2025 lecture notes.
https://www.uio.no/studier/emner/matnat/math/MAT4540/h25/uct.pdf

Use: degreewise chain complexes of free abelian groups.

Proof-assistant compilation and novelty comparison remain separate tasks.
'''

def main():
    print(
        "PROJECT 2 — CONSOLIDATED PROOF-DRAFT ASSEMBLY",
        flush=True,
    )

    verified = {}
    provenance = []

    for key,root,status,count in SPECS:
        files,receipt,manifest_hash = read_bundle(
            root,status,count
        )
        verified[key] = (files,receipt)

        provenance.append({
            "label": key,
            "source_directory": str(root),
            "manifest_sha256": manifest_hash,
            "receipt_sha256": sha(files["RECEIPT.json"]),
            "verifier_sha256": sha(files["verify.py"]),
            "preserved_status": receipt["status"],
            "copied_manifested_artifacts": count,
        })

        print(
            key.upper()
            + ": manifest, source identity and receipt status PASS",
            flush=True,
        )

    export = json.loads(
        verified["qq"][0]["inputs/"+EXPORT]
    )

    expected = collections.Counter(
        (i,tuple(degree))
        for i,shifts in enumerate(
            export["module_semigroup_shifts"]
        )
        for degree in shifts
    )

    rows = list(csv.DictReader(io.StringIO(
        verified["divisor"][0][
            "BETTI_MULTIGRADED.csv"
        ].decode()
    )))

    actual = collections.Counter()

    for row in rows:
        i = int(row["homological_degree"])
        degree = tuple(
            int(row[key])
            for key in ["a0","a1","a2","a3","k"]
        )
        multiplicity = int(row["multiplicity"])

        need(
            multiplicity > 0,
            "Nonpositive Betti multiplicity",
        )
        actual[i,degree] += multiplicity

    need(
        actual == expected and len(actual) == 54,
        "Multigraded Betti comparison",
    )

    divisor_results = verified["divisor"][1]["results"]

    need(
        divisor_results["degrees"] == 835
        and divisor_results["boundary_smith_forms"] == 2956
        and divisor_results["integer_unit_reductions"] == 2956
        and divisor_results["torsion_cases"] == 0,
        "Divisor coverage record",
    )

    integral_receipt = verified["integral"][1]

    need(
        integral_receipt["scope"][
            "integral_compositions_verified"
        ] is True,
        "Integral composition record",
    )

    for name,degree,rank in CASES:
        case = json.loads(
            verified["integral"][0][
                "CASE_%s_DEG%d.json" % (name,degree)
            ]
        )

        need(
            case["status"] == "UNIMODULAR_RANK_CERTIFIED"
            and case["unit_pivots"] == rank
            and case["residual_nonzero_entries"] == 0
            and len(case["unit_pivot_trace"]) == rank,
            "Integral case record mismatch",
        )

    dimensions,numerators,upper_table = upper_bounds(
        export["module_scalar_shifts"]
    )

    for key,(files,receipt) in verified.items():
        target = OUT/"evidence"/key
        target.mkdir(parents=True,exist_ok=False)

        for name,data in files.items():
            destination = target.joinpath(
                *pathlib.PurePosixPath(name).parts
            )
            destination.parent.mkdir(
                parents=True,exist_ok=True
            )
            destination.write_bytes(data)

    (OUT/"THEOREM_DRAFT.md").write_text(THEOREM)
    (OUT/"SOURCE_NOTES.md").write_text(SOURCES)

    (OUT/".gitattributes").write_text(
        "* -text -filter -ident -working-tree-encoding\n"
    )

    with (OUT/"UPPER_BOUND_TABLE.csv").open(
        "w",newline=""
    ) as handle:
        writer = csv.writer(handle)
        writer.writerow([
            "map",
            "degree",
            "full_kernel_component_dimension",
            "dependency",
        ])
        writer.writerows(upper_table)

    save("UPPER_BOUND_RECONSTRUCTION.json", {
        "polynomial_ring_dimensions_0_through_9": dimensions,
        "kernel_numerator_coefficients": numerators,
        "scope": (
            "Coefficient arithmetic. K2 and K3 formulas apply "
            "only after the induction steps stated in the draft."
        ),
    })

    save("PROVENANCE.json", {
        "frozen_export_sha256": FROZEN,
        "bundles": provenance,
        "original_files_modified": False,
        "historical_receipt_scope_flags_modified": False,
    })

    save("CLAIM_LEDGER.json", {
        "status": (
            "THEOREM_DRAFT_SUPPORTED_BY_REPLAYED_CERTIFICATES"
        ),
        "proposed_claim": (
            "Fixed frozen matrices give a minimal graded "
            "resolution of K[S] over every field. "
            "Integral exactness is a separate corollary."
        ),
        "automated_assembly_checks": [
            "manifested bytes",
            "receipt/verifier hash linkage",
            "frozen export identity",
            "full multigraded shift comparison",
            "integral case summaries and trace lengths",
            "Hilbert coefficient arithmetic",
        ],
        "not_done_by_assembly": [
            "rerun previous audits",
            "independent peer review",
            "Lean compilation",
            "novelty clearance",
        ],
        "proof_obligations_for_review": [
            "structural semigroup lemmas",
            "pure-difference presentation bridge",
            "complete Betti-degree interval",
            "divisor/Koszul identification",
            "inductive use of kernel dimensions",
            "last shifted-free-module argument",
            "integral universal-coefficient corollary",
        ],
    })

    save("ASSEMBLY_RECEIPT.json", {
        "status": "PROOF_PACKAGE_ASSEMBLED_AND_LINKS_VERIFIED",
        "utc": datetime.datetime.now(
            datetime.timezone.utc
        ).isoformat(),
        "python": sys.version,
        "platform": platform.platform(),
        "source_sha256": sha(
            pathlib.Path(__file__).read_bytes()
        ),
        "theorem_status": "DRAFT_REQUIRING_REVIEW",
        "source_bundles": 3,
        "divisor_degrees": 835,
        "component_cases": 9,
        "new_mathematical_audits_executed": False,
        "git_modified": False,
    })

    checks = []

    for path in sorted(OUT.rglob("*")):
        if (
            path.is_file()
            and path.name != "console.log"
            and path != OUT/"SHA256SUMS"
            and "__pycache__" not in path.parts
        ):
            checks.append(
                sha(path.read_bytes())
                + "  "
                + path.relative_to(OUT).as_posix()
            )

    (OUT/"SHA256SUMS").write_text(
        "\n".join(checks)+"\n"
    )

    print("\nPROOF_PACKAGE_ASSEMBLED_AND_LINKS_VERIFIED")
    print("THEOREM_STATUS=DRAFT_REQUIRING_REVIEW")
    print("ORIGINAL_RECEIPTS=UNCHANGED")
    print("MATHEMATICAL_AUDITS_RERUN=NO")
    print("FILES_MANIFESTED="+str(len(checks)))
    print("RESULTS="+str(OUT))

if __name__ == "__main__":
    try:
        main()
    except BaseException as error:
        for name in (
            "ASSEMBLY_RECEIPT.json",
            "SHA256SUMS",
        ):
            path = OUT/name
            if path.exists():
                path.unlink()

        save("FAILURE.json", {
            "status": "ASSEMBLY_INCOMPLETE",
            "error_type": type(error).__name__,
            "message": str(error),
        })
        raise
