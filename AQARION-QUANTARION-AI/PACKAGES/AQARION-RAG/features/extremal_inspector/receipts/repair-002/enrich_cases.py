import hashlib
import json
from pathlib import Path
import runpy
import sys

feature = Path(sys.argv[1]).resolve()
output = Path(sys.argv[2]).resolve()
recognizer = Path(sys.argv[3]).resolve()

output.mkdir(parents=True, exist_ok=True)

for name in ("cases.json", "inspector.html", "page-template.html"):
    if (output / name).exists():
        raise RuntimeError("Refusing to overwrite generated build: " + name)

base = feature / "build-001"
data = json.loads((base / "cases.json").read_text())
module = runpy.run_path(str(recognizer))

recognize = module["recognize_extremal"]
verify = module["verify_terminal_repair"]

certified = set()

for case in data["cases"].values():
    old = case["recognition"]
    new = recognize(case["T"], data["observation"])

    if {key: new[key] for key in old} != old:
        raise AssertionError("Historical recognition fields changed")

    if new["classification"] == "NONLITERAL_TERMINAL":
        certificate = new["repair_certificate"]

        if not verify(new["terminal_truth_table"], certificate):
            raise AssertionError("Saved-case repair certificate failed")

        certified.add(tuple(case["T"]))

    case["recognition"] = new

if len(certified) != 8:
    raise AssertionError("Expected eight distinct certified nonliteral cases")

data["base_recognizer_sha256"] = data["recognizer_sha256"]
data["recognizer_sha256"] = hashlib.sha256(
    recognizer.read_bytes()
).hexdigest()
data["extension"] = {
    "kind": "CONSTRUCTIVE_TERMINAL_REPAIR",
    "base_build": "build-001",
    "rank_calculations_repeated": False,
    "historical_rank_values_preserved": True,
    "distinct_nonliteral_cases_certified": 8,
}

template = (base / "page-template.html").read_text()

marker = '<section>\n<h2>Why the old certificate changes</h2>'

panel = '''<section>
<h2>Constructive terminal repair</h2>
<pre id="repair"></pre>
<p class="small">This uses the elementary Boolean-terminal repair lemma.
The detecting feature's degree need not be the degree at which the whole
function space becomes full. No new rank calculation is performed here.</p>
</section>

'''

if template.count(marker) != 1:
    raise AssertionError("Cannot identify unique panel insertion point")

template = template.replace(marker, panel + marker, 1)

render_marker = "  graph(item.T);\n"

render = '''  const repair=r.repair_certificate;
  el("repair").textContent=repair
    ? "Detecting feature: "+
      repair.temporal_product_coordinates.map(t=>"h_"+t).join(" × ")+
      "\\nExact parity moment: "+repair.parity_moment+
      "\\nCertified full-rank degree: "+repair.full_rank_degree+
      "\\nCertified rank at that degree: "+repair.full_rank+
      "\\n\\n"+JSON.stringify(repair,null,2)
    : r.classification==="PREFIX_COLLISION"
      ? "No terminal-repair certificate: prefix coordinates are not bijective."
      : "Constant/literal terminal: the extremal obstruction remains.";
'''

if template.count(render_marker) != 1:
    raise AssertionError("Cannot identify unique render insertion point")

template = template.replace(
    render_marker, render + render_marker, 1
)

serialized = json.dumps(
    data, separators=(",", ":")
).replace("<", "\\u003c")

(output / "cases.json").write_text(
    json.dumps(data, indent=2) + "\n"
)
(output / "page-template.html").write_text(template)
(output / "inspector.html").write_text(
    template.replace("__CASE_DATA__", serialized)
)
(output / "extension.json").write_text(
    json.dumps(data["extension"], indent=2) + "\n"
)

print("NONLITERAL_SAVED_CASES_CERTIFIED=8")
print("HISTORICAL_RECOGNITION_FIELDS_PRESERVED=YES")
print("RANK_VALUES_RECOMPUTED=NO")
