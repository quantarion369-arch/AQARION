#!/usr/bin/env python3
import hashlib,json,re,subprocess,sys
from datetime import datetime,timezone
from pathlib import Path
REQUIRED=("PBCore006.lean","lakefile.lean","lean-toolchain")
FORBIDDEN=[("sorry",r"\bsorry\b"),("admit",r"\badmit\b"),("sorryAx",r"\bsorryAx\b"),("native_decide",r"\bnative_decide\b")]
AXIOM=re.compile(r"^\s*axiom\b", re.MULTILINE)
NL=chr(10)
def sha(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for c in iter(lambda:f.read(1<<20),b""): h.update(c)
    return h.hexdigest()
def main():
    if len(sys.argv)!=2: print("Usage: audit_protocol.py REPO",file=sys.stderr); return 2
    repo=Path(sys.argv[1]).resolve()
    if not repo.is_dir(): print("not a dir",file=sys.stderr); return 2
    paths={n:repo/n for n in REQUIRED}
    missing=[n for n,p in paths.items() if not p.is_file()]
    checks=[]; hashes={}
    if missing:
        checks.append({"name":"required_files","status":"FAIL","detail":"missing: "+", ".join(missing)})
    else:
        checks.append({"name":"required_files","status":"PASS","detail":"all present"})
        for n,p in paths.items(): hashes[n]=sha(p)
        r=subprocess.run(["git","-C",str(repo),"rev-parse","HEAD"],capture_output=True,text=True)
        commit=r.stdout.strip() if r.returncode==0 else None
        checks.append({"name":"git_commit","status":"PASS" if commit else "FAIL","detail":commit or r.stderr.strip()})
        src=paths["PBCore006.lean"].read_text(encoding="utf-8")
        found=[]
        for name,pat in FORBIDDEN:
            for m in re.finditer(pat,src):
                line=src[:m.start()].count(NL)+1; found.append(f"{name} line {line}")
        for m in AXIOM.finditer(src):
            line=src[:m.start()].count(NL)+1; found.append(f"axiom line {line}")
        checks.append({"name":"forbidden_constructs","status":"FAIL" if found else "PASS","detail":"; ".join(found) or "clean"})
        overall="PASS" if all(c["status"]=="PASS" for c in checks) else "FAIL"
        print(json.dumps({"timestamp":datetime.now(timezone.utc).isoformat(),"commit_sha":commit,"file_hashes":hashes,"checks":checks,"overall":overall},sort_keys=True))
        return 0 if overall=="PASS" else 1
    print(json.dumps({"timestamp":datetime.now(timezone.utc).isoformat(),"commit_sha":None,"file_hashes":hashes,"checks":checks,"overall":"FAIL"},sort_keys=True))
    return 1
if __name__=="__main__": raise SystemExit(main())
