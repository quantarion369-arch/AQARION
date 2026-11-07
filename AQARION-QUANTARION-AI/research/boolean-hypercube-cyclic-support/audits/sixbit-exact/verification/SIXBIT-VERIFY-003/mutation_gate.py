#!/usr/bin/env python3
import ast, hashlib, json, shutil, subprocess, sys, tempfile
from pathlib import Path
from datetime import datetime, timezone

OUT = Path(__file__).resolve().parent
BASE = OUT.parent.parent
V2 = BASE / "verification/SIXBIT-VERIFY-002-cSnALgW3/verify.py"
V2_SHA = "3d6d796e9df7c6bcd8d396c6e2717d39dcfb65d3d87364cd96f43c8c0f972322"
JSONS = ["flat_census.json", "ten_point_circuit_search.json", "run_receipt.json"]
ALL = JSONS + ["sixbit_flats.py"]

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p): return json.loads(p.read_text())
def save(p,x): p.write_text(json.dumps(x,indent=2,sort_keys=True)+"\n")
def need(x,m):
    if not x: raise RuntimeError(m)

def pin_node(src):
    nodes=[n for n in ast.parse(src).body
           if isinstance(n,ast.Assign) and any(
           isinstance(t,ast.Name) and t.id=="PIN" for t in n.targets)]
    need(len(nodes)==1,"PIN assignment not unique")
    return nodes[0]

def rewrite_pins(src,pins):
    n=pin_node(src)
    lines=src.splitlines(keepends=True)
    return "".join(lines[:n.lineno-1]+["PIN = "+repr(pins)+"\n"]+lines[n.end_lineno:])

def rebind(data):
    h=sha(data/"flat_census.json")
    r=load(data/"run_receipt.json"); r["flat_census_sha256"]=h
    save(data/"run_receipt.json",r)
    q=load(data/"ten_point_circuit_search.json"); q["census_sha256"]=h
    save(data/"ten_point_circuit_search.json",q)

def metadata(d):
    x=load(d/"flat_census.json"); x["point_count"]=63
    save(d/"flat_census.json",x)

def prime(d):
    x=load(d/"run_receipt.json"); x["prime_verified"]=False
    save(d/"run_receipt.json",x)

def gate(d):
    x=load(d/"run_receipt.json"); x["geometry_gate"]="FAIL"
    save(d/"run_receipt.json",x)

def history(d):
    x=load(d/"ten_point_circuit_search.json"); x["status"]="UNVERIFIED"
    save(d/"ten_point_circuit_search.json",x)

def generator(d):
    p=d/"sixbit_flats.py"; p.write_bytes(p.read_bytes()+b"\n# MUTATION\n")

def geometry(d):
    p=d/"flat_census.json"; x=load(p); pts=x["flats"][0]["points"]
    pts[0]=next(v for v in range(64) if v not in pts)
    save(p,x)

def rankq(d):
    p=d/"flat_census.json"; x=load(p); f=x["flats"][0]
    f["rank_Q"]=8 if f["rank_Q"]==7 else 7
    save(p,x)

def rankfp(d):
    p=d/"flat_census.json"; x=load(p); f=x["flats"][0]
    f["rank_Fp"]=8 if f["rank_Fp"]==7 else 7
    save(p,x)

def run(work,source,name,mut,expected):
    c=work/name; d=c/"inputs"; r=c/"runner"
    d.mkdir(parents=True); r.mkdir()
    for f in ALL: shutil.copy2(BASE/f,d/f)
    if mut:
        mut(d); rebind(d)
    pins={f:sha(d/f) for f in JSONS}
    vf=r/"verify.py"; vf.write_text(rewrite_pins(source,pins))
    print("RUN",name,flush=True)
    z=subprocess.run([sys.executable,str(vf),str(d)],cwd=r,
                     capture_output=True,text=True,timeout=180)
    (c/"stdout.txt").write_text(z.stdout)
    (c/"stderr.txt").write_text(z.stderr)
    (c/"exit.txt").write_text(str(z.returncode)+"\n")
    if expected is None:
        need(z.returncode==0,name+": baseline failed")
        rec=load(r/"PASS.json")
        need(rec.get("status")=="PASS","positive receipt missing")
        err=None; verdict="ACCEPTED"
    else:
        need(z.returncode==2,name+": expected exit 2")
        rec=load(r/"FAIL.json")
        need(rec.get("status")=="FAIL","failure receipt invalid")
        err=rec.get("error")
        need(err==expected,name+": wrong error "+repr(err))
        verdict="REJECTED_AS_EXPECTED"
    print("PASS",name,flush=True)
    return {"case":name,"verdict":verdict,"exit":z.returncode,
            "expected_error":expected,"actual_error":err}

def main():
    need(sha(V2)==V2_SHA,"VERIFY-002 source hash mismatch")
    src=V2.read_text()
    pins=ast.literal_eval(pin_node(src).value)
    for f,h in pins.items(): need(sha(BASE/f)==h,"PIN mismatch "+f)
    protected=[V2]+[BASE/f for f in ALL]
    before={str(p):sha(p) for p in protected}
    work=Path(tempfile.mkdtemp(prefix="run-",dir=OUT))
    cases=[
      ("positive_baseline",None,None),
      ("census_metadata",metadata,"Census metadata: point_count"),
      ("prime_flag",prime,"Receipt prime flag"),
      ("geometry_gate",gate,"Receipt field: geometry_gate"),
      ("historical_status",history,"Historical status"),
      ("generator_hash",generator,"Historical generator hash mismatch"),
      ("flat_geometry",geometry,"Flat coverage/duplication"),
      ("rank_Q",rankq,"Incorrect rank_Q"),
      ("rank_Fp",rankfp,"Incorrect rank_Fp"),
    ]
    report={"gate":"SIXBIT-VERIFY-003","status":"RUNNING",
      "started_utc":datetime.now(timezone.utc).isoformat(),
      "baseline_sha256":V2_SHA,"cases":[]}
    try:
        for args in cases: report["cases"].append(run(work,src,*args))
        report["status"]="PASS"
        report["positive_controls_passed"]=1
        report["mutations_rejected_as_expected"]=8
    except Exception as e:
        report["status"]="FAIL"; report["error"]=repr(e)
    report["protected_files_unchanged"]=all(
        p.is_file() and sha(p)==before[str(p)] for p in protected)
    report["finished_utc"]=datetime.now(timezone.utc).isoformat()
    save(work/"MUTATION-REPORT.json",report)
    files=[p for p in work.rglob("*") if p.is_file()]
    (work/"SHA256SUMS").write_text("".join(
        sha(p)+"  "+p.relative_to(work).as_posix()+"\n"
        for p in sorted(files)))
    print(json.dumps(report,indent=2,sort_keys=True))
    print("RETAINED:",work)
    return 0 if report["status"]=="PASS" and report["protected_files_unchanged"] else 1

if __name__=="__main__": sys.exit(main())
