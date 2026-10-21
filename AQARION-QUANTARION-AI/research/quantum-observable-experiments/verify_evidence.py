from pathlib import Path
import hashlib, json, subprocess, sys, tempfile

B = Path(__file__).resolve().parent
R = B.parents[2]
S = B.relative_to(R).as_posix()
W = ".github/workflows/quantum-observable-ci.yml"
U = {
 "coherence-02": (6,"QUANTUM_OBSERVABLE_PILOT=PASS"),
 "generator-closure-01": (5,"GENERATOR_CLOSURE_EXPERIMENT=PASS"),
 "generator-closure-02": (5,"GENERAL_GENERATOR_CLOSURE_EXPERIMENT=PASS"),
 "sampling-aliasing-01-oqp1w92w": (4,"SAMPLING_ALIASING_EXPERIMENT=PASS"),
 "sampling-classification-01-gx4ryktu": (4,"GENERAL_SAMPLING_CLASSIFICATION_EXPERIMENT=PASS"),
 "observable-matrix-audit-01-38vwidg2": (4,"DIRECT_MATRIX_GENERATOR_AUDIT=PASS"),
 "switched-generator-01-zfd5_qx8": (4,"SWITCHED_GENERATOR_CLOSURE_EXPERIMENT=PASS"),
 "qutrit-observability-01-iavq0kwu": (4,"QUTRIT_OBSERVABILITY_EXPERIMENT=PASS")
}

def check(ok,msg):
 if not ok: raise RuntimeError(msg)

def sha(data): return hashlib.sha256(data).hexdigest()

def safe(root,rel):
 p=Path(rel)
 check(not p.is_absolute() and ".." not in p.parts,"unsafe path")
 p=root/p
 cur=p
 while cur!=root:
  check(not cur.is_symlink(),"symlink: "+str(p))
  cur=cur.parent
 check(p.is_file(),"missing: "+str(p))
 return p

def main():
 check(sys.argv[1:] in ([],["--manifest-only"]),"unknown argument")
 p=safe(B,"EVIDENCE_MANIFEST.json")
 raw=p.read_bytes()
 m=json.loads(raw)
 watch={p:sha(raw)}
 check(m.get("schema")=="aqarion.quantum-observable-evidence.v1","schema")
 records=m["experiments"]
 names=[x["directory"] for x in records]
 check(len(names)==8 and set(names)==set(U),"experiment selection")
 check(len(m["artifacts"])==36,"artifact count")
 counts={n:0 for n in U}
 for rel,h in m["artifacts"].items():
  parts=Path(rel).parts
  check(len(parts)==2 and parts[0] in U,"artifact scope")
  p=safe(B,rel)
  check(sha(p.read_bytes())==h,"artifact hash: "+rel)
  watch[p]=h
  counts[parts[0]]+=1
 check(all(counts[n]==U[n][0] for n in U),"per-unit counts")
 check(set(m["documentation"])=={"README.md"},"documentation selection")
 for rel,h in m["documentation"].items():
  p=safe(B,rel)
  check(sha(p.read_bytes())==h,"documentation hash")
  watch[p]=h
 check(set(m["verification_assets"])=={S+"/verify_evidence.py",W},"verification assets")
 for rel,h in m["verification_assets"].items():
  p=safe(R,rel)
  check(sha(p.read_bytes())==h,"verification asset hash")
  watch[p]=h
 for x in records:
  n=x["directory"]
  p=safe(B,n+"/experiment.py")
  check(x["recorded_exit"]==0 and safe(B,n+"/exit.txt").read_text().strip()=="0","saved exit")
  check(sha(p.read_bytes())==x["source_sha256"],"source record")
  check(U[n][1] in safe(B,n+"/output.log").read_text(),"saved marker")
  compile(p.read_bytes(),str(p),"exec")
 print("ARCHIVED_HASHES_AND_RECORDS=PASS",flush=True)
 if sys.argv[1:]:
  print("MANIFEST_ONLY_CHECK=PASS; NO_EXPERIMENTS_EXECUTED")
  return
 try:
  with tempfile.TemporaryDirectory(prefix="aqarion-quantum-") as tmp:
   for n in U:
    d=Path(tmp)/n
    d.mkdir()
    for rel in m["artifacts"]:
     if Path(rel).parts[0]==n:
      (d/Path(rel).name).write_bytes(safe(B,rel).read_bytes())
    print("REPLAY_START: "+n,flush=True)
    p=subprocess.run(
     [sys.executable,"-I","-B","-u",str(d/"experiment.py")],
     cwd=d,stdin=subprocess.DEVNULL,capture_output=True,
     text=True,errors="replace",timeout=120)
    print(p.stdout,end="",flush=True)
    if p.stderr: print(p.stderr,end="",file=sys.stderr,flush=True)
    check(p.returncode==0 and U[n][1] in p.stdout,"replay failed: "+n)
    print("REPLAY_PASS: "+n,flush=True)
 finally:
  for p,h in watch.items():
   check(p.is_file() and sha(p.read_bytes())==h,"archive changed: "+str(p))
 print("ARCHIVED_EVIDENCE_UNCHANGED=PASS")
 print("QUANTUM_REPLAY_VERIFICATION=PASS")
 print("SCOPE=REPLAY_NOT_FORMAL_PROOF_OR_SECURITY_SANDBOX")

if __name__=="__main__":
 main()
