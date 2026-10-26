"""Structural checks plus optional Node function-level checks."""
from pathlib import Path
import shutil
import subprocess
import unittest

PAGE = Path(__file__).resolve().parents[1] / "static/index.html"

class ActiveScopeSummaryTests(unittest.TestCase):
    def test_label_is_inside_search_form(self):
        page = PAGE.read_text()
        start = page.index('<form id="search"')
        label = page.index('id="active-search-scope"')
        end = page.index("</form>", start)
        self.assertLess(start, label)
        self.assertLess(label, end)

    def test_loading_updates_are_connected(self):
        page = PAGE.read_text()
        self.assertIn('sourceListState = "loaded";', page)
        self.assertIn('sourceListState = "failed";', page)
        self.assertIn('aria-live="polite"', page)
        self.assertNotIn("innerHTML", page)
        start = page.index("function updateSearchScope() {")
        end = page.index("\nfunction validateScopedEvidence(", start)
        functions = page[start:end]
        self.assertNotIn("fetch(", functions)
        self.assertNotIn("sourceSelect.value =", functions)
        self.assertIn("updateSearchScope();", functions)

    @unittest.skipUnless(
        shutil.which("node"),
        "Node unavailable: browser behavior still requires manual checking",
    )
    def test_eight_runtime_states(self):
        javascript = r"""
const fs=require("fs"), vm=require("vm"), assert=require("assert");
const page=fs.readFileSync(0,"utf8");
const start=page.indexOf("function updateSearchScope() {");
const end=page.indexOf("\nfunction validateScopedEvidence(",start);
assert(start>=0 && end>start);
const ctx={
  mode:{value:"passages"},
  sourceSelect:{value:"",disabled:false},
  openSource:{disabled:true},
  sourceEntries:new Map(),
  activeSearchScope:{textContent:""},
  sourceListState:"loading"
};
vm.createContext(ctx);
vm.runInContext(page.slice(start,end),ctx);
function update(){
  vm.runInContext("syncSourceControls()",ctx);
  return ctx.activeSearchScope.textContent;
}
assert(update().includes("source list loading"));
ctx.sourceListState="loaded";
for(const [id,doc] of [["a","Alpha"],["b","Beta"],["c","Gamma"]]){
  ctx.sourceEntries.set(id,{doc});
}
assert(update().includes("3 pinned documents"));
ctx.sourceSelect.value="a";
assert(update().includes("Alpha — one pinned document"));
assert(!ctx.openSource.disabled);
assert.equal(ctx.sourceSelect.value,"a");
ctx.mode.value="claims";
assert(update().includes("claim registry"));
assert(ctx.sourceSelect.disabled && ctx.openSource.disabled);
assert.equal(ctx.sourceSelect.value,"a");
ctx.mode.value="passages";
assert(update().includes("Alpha"));
assert(!ctx.sourceSelect.disabled);
ctx.sourceSelect.value="";
ctx.sourceListState="failed";
assert(update().includes("count unavailable"));
ctx.sourceSelect.value="missing";
assert(update().includes("selected source unavailable"));
assert.equal(ctx.sourceSelect.value,"missing");
ctx.sourceSelect.value="";
ctx.sourceListState="loaded";
ctx.sourceEntries.clear();
ctx.sourceEntries.set("a",{doc:"Alpha"});
assert(update().includes("1 pinned document."));
console.log("SCOPE_STATE_CASES=8 PASS");
"""
        result = subprocess.run(
            [shutil.which("node"), "-e", javascript],
            input=PAGE.read_text(),
            text=True, capture_output=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("SCOPE_STATE_CASES=8 PASS", result.stdout)
        print(result.stdout.strip())


    def test_mode_changes_do_not_submit(self):
        page = PAGE.read_text()
        self.assertNotIn(
            'mode.addEventListener("change", search)', page
        )
        self.assertIn(
            'mode.addEventListener("change", handleModeChange)', page
        )
        body = page.split(
            "function handleModeChange() {", 1
        )[1].split(
            '\n}\n\nmode.addEventListener', 1
        )[0]
        for marker in (
            "++requestId;",
            "controller.abort();",
            "hideSourceView();",
            "out.replaceChildren();",
            "syncSourceControls();",
            "Mode changed. Press Search or Enter.",
        ):
            self.assertIn(marker, body)
        for forbidden in (
            "search(", "fetch(", "sourceSelect.value =",
            "input.value =", "mode.value =",
        ):
            self.assertNotIn(forbidden, body)

    @unittest.skipUnless(
        shutil.which("node"),
        "Node unavailable: mode-change browser check required",
    )
    def test_mode_change_runtime_without_submission(self):
        javascript = r"""
const fs=require("fs"), vm=require("vm"), assert=require("assert");
const page=fs.readFileSync(0,"utf8");
const start=page.indexOf("function handleModeChange() {");
const end=page.indexOf('\n}\n\nmode.addEventListener',start);
assert(start>=0 && end>start);
const code=page.slice(start,end+2);
let aborted=0, hidden=0, cleared=0, synced=0;
const ctx={
  requestId:10,
  controller:{abort(){aborted++;}},
  hideSourceView(){hidden++;},
  out:{replaceChildren(){cleared++;}},
  syncSourceControls(){synced++;},
  status:{textContent:"Old results"},
  sourceSelect:{value:"pinned-source"},
  mode:{value:"claims"},
  input:{value:"Existing question"},
  search(){throw Error("Unexpected search");},
  fetch(){throw Error("Unexpected fetch");}
};
vm.createContext(ctx);
vm.runInContext(code,ctx);
for(const mode of ["claims","passages"]){
  ctx.mode.value=mode;
  vm.runInContext("handleModeChange()",ctx);
  assert.equal(ctx.sourceSelect.value,"pinned-source");
  assert.equal(ctx.input.value,"Existing question");
  assert.equal(ctx.mode.value,mode);
  assert.equal(ctx.status.textContent,
               "Mode changed. Press Search or Enter.");
}
assert.equal(ctx.requestId,12);
assert.equal(aborted,2);
assert.equal(hidden,2);
assert.equal(cleared,2);
assert.equal(synced,2);
console.log("MODE_CHANGE_FUNCTION_CASES=2 PASS");
"""
        result = subprocess.run(
            [shutil.which("node"), "-e", javascript],
            input=PAGE.read_text(),
            text=True, capture_output=True, timeout=20,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MODE_CHANGE_FUNCTION_CASES=2 PASS", result.stdout)
        print(result.stdout.strip())

if __name__ == "__main__":
    unittest.main(verbosity=2)
