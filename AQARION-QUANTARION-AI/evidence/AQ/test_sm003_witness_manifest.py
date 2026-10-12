"""Witness-manifest regression (hardened). Uses repo helpers mutations.witness_detection_sets / case_values
and manifest keys: mutant_ids_explicit, mutant_semantics, aliases, witness_suite.{instances,requires}.
Negative controls are executable tests."""
import copy, json, unittest
from pathlib import Path
import mutations as M

MANIFEST = json.loads((Path(__file__).parent / "manifest.json").read_text())
VALID = set(M.D_MUTANTS) | set(M.R_MUTANTS)
INVALID = set(M.INVALID_MUTANTS)

def problems(manifest):
    P = {k: [] for k in ("dup_witness_id","bad_instance","dup_mutant_id","inventory","semantics",
                         "unknown_id","false_claim","missing_claim","id_set","requirements","dup_detects","alias")}
    ids = manifest["mutant_ids_explicit"]
    inst = manifest["witness_suite"]["instances"]
    if len(ids) != len(set(ids)): P["dup_mutant_id"].append("duplicate mutant ids")
    if set(ids) != VALID | INVALID: P["inventory"].append(sorted(set(ids) ^ (VALID | INVALID)))
    sem = manifest.get("mutant_semantics", {})
    if set(sem) != set(ids): P["semantics"].append(("keys differ", sorted(set(sem) ^ set(ids))))
    for k, v in sem.items():
        want = ("zero_test" if k in M.D_MUTANTS else "rank_prediction" if k in M.R_MUTANTS else "invalid")
        if v.get("kind") != want: P["semantics"].append((k, v.get("kind"), want))
        if k in INVALID and v.get("coverage_credit") is not False: P["semantics"].append((k, "invalid mutant gets credit"))
    for grp, members in manifest.get("aliases", {}).items():
        if grp == "policy": continue
        if any(m not in VALID for m in members): P["alias"].append(grp)
    wids = [w.get("w") for w in inst]
    if len(wids) != len(set(wids)): P["dup_witness_id"].append(wids)
    ok = []
    for w in inst:
        try:
            t, blocks = M.witness_instance(w); M.validate_instance(t, [list(b) for b in blocks]); ok.append(w)
        except Exception as e:
            P["bad_instance"].append((w.get("w"), str(e)))
    if P["dup_witness_id"] or P["bad_instance"]: return P
    got = M.witness_detection_sets(manifest)
    if set(got) != set(wids): P["id_set"].append((sorted(got), sorted(wids)))
    for w in inst:
        d = w["detects"]
        if len(d) != len(set(d)): P["dup_detects"].append(w["w"])
        if w["w"] not in got:      # recorded in id_set above; do not crash
            continue
        bad = set(d) - VALID
        if bad: P["unknown_id"].append((w["w"], sorted(bad)))
        if set(d) - set(got[w["w"]]): P["false_claim"].append((w["w"], sorted(set(d) - set(got[w["w"]]))))
        if set(got[w["w"]]) - set(d): P["missing_claim"].append((w["w"], sorted(set(got[w["w"]]) - set(d))))
    req, unreached = manifest["witness_suite"]["requires"], False
    for w in inst:
        f, blocks = w["f"], w["partition"]
        if req["every_witness_non_injective"] and len(set(f)) == len(f): P["requirements"].append((w["w"], "injective"))
        if req["every_witness_non_constant"] and len(set(f)) == 1: P["requirements"].append((w["w"], "constant"))
        if req["every_witness_has_non_singleton_block"] and not any(len(b) > 1 for b in blocks): P["requirements"].append((w["w"], "all singleton"))
        bo = {x: i for i, b in enumerate(blocks) for x in b}
        unreached = unreached or len({bo[f[x]] for x in range(len(f))}) < len(blocks)
    if req["at_least_one_witness_has_unreached_block"] and not unreached: P["requirements"].append("no unreached block")
    return P

def mutated(fn):
    m = copy.deepcopy(MANIFEST); fn(m); return problems(m)

REC = M.witness_detection_sets(MANIFEST)          # recomputed truth, not declarations
def _pick(pred):
    """Pick (index, witness id, mutant) by property, not by position/name."""
    for i, w in enumerate(MANIFEST["witness_suite"]["instances"]):
        for mu in sorted(VALID):
            if pred(mu in REC[w["w"]]): return i, w["w"], mu
    raise unittest.SkipTest("no suitable fixture element")

class Baseline(unittest.TestCase):
    def test_manifest_has_no_problems(self):
        self.assertEqual({k: v for k, v in problems(MANIFEST).items() if v}, {})
    def test_invariant_under_witness_reordering(self):
        m = copy.deepcopy(MANIFEST); m["witness_suite"]["instances"].reverse()
        self.assertEqual({k: v for k, v in problems(m).items() if v}, {})

class NegativeControls(unittest.TestCase):
    def test_false_claim(self):
        i, _, mu = _pick(lambda detected: not detected)
        self.assertTrue(mutated(lambda m: m["witness_suite"]["instances"][i]["detects"].append(mu))["false_claim"])
    def test_missing_claim(self):
        i, _, mu = _pick(lambda detected: detected)
        self.assertTrue(mutated(lambda m: m["witness_suite"]["instances"][i]["detects"].remove(mu))["missing_claim"])
    def test_unknown_id(self):       self.assertTrue(mutated(lambda m: m["witness_suite"]["instances"][0]["detects"].append("D:FAKE"))["unknown_id"])
    def test_duplicate_witness_id(self):
        def f(m): m["witness_suite"]["instances"][-1]["w"] = m["witness_suite"]["instances"][0]["w"]
        self.assertTrue(mutated(f)["dup_witness_id"])
    def test_bad_partition(self):    self.assertTrue(mutated(lambda m: m["witness_suite"]["instances"][0].__setitem__("partition", [[0]]))["bad_instance"])
    def test_duplicate_mutant_id(self): self.assertTrue(mutated(lambda m: m["mutant_ids_explicit"].append(m["mutant_ids_explicit"][0]))["dup_mutant_id"])
    def test_inventory_mismatch(self):  self.assertTrue(mutated(lambda m: m["mutant_ids_explicit"].pop())["inventory"])
    def test_semantics_kind(self):
        def f(m):
            k = next(iter(M.D_MUTANTS)); m["mutant_semantics"][k]["kind"] = "rank_prediction"
        self.assertTrue(mutated(f)["semantics"])
    def test_duplicate_detects(self):
        def f(m):
            d = m["witness_suite"]["instances"][0]["detects"]; d.append(d[0])
        self.assertTrue(mutated(f)["dup_detects"])
    def test_injective_witness(self):
        def f(m):
            w = m["witness_suite"]["instances"][0]; w["f"] = list(range(len(w["f"])))
        self.assertTrue(mutated(f)["requirements"])
    def test_missing_recomputed_witness_does_not_crash(self):
        from unittest import mock
        real = M.witness_detection_sets
        def drop_first(man):
            r = real(man); r.pop(next(iter(r))); return r
        with mock.patch.object(M, "witness_detection_sets", drop_first):
            P = problems(MANIFEST)
        self.assertTrue(P["id_set"])

if __name__ == "__main__":
    unittest.main()
