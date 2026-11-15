import tarfile,json,hashlib,itertools
from fractions import Fraction as F
from pathlib import Path
a=Path.home()/"AQARION-resolution-evidence-20261114T171514834259Z.tar.gz"
print("ARCHIVE",hashlib.sha256(a.read_bytes()).hexdigest())
def rank(M):
    M=[r[:] for r in M];r=0
    for c in range(len(M[0])):
        pv=next((i for i in range(r,len(M)) if M[i][c]!=0),None)
        if pv is None: continue
        M[r],M[pv]=M[pv],M[r]
        for i in range(len(M)):
            if i!=r and M[i][c]!=0:
                f=M[i][c]/M[r][c];M[i]=[x-f*y for x,y in zip(M[i],M[r])]
        r+=1
    return r
with tarfile.open(a,"r:gz") as tf:
    for m in tf.getmembers():
        if m.isfile(): print("MEMBER",hashlib.sha256(tf.extractfile(m).read()).hexdigest()[:16],m.size,m.name)
    wn=next(m.name for m in tf.getmembers() if "D4-rank13" in m.name)
    w=json.loads(tf.extractfile(wn).read())
D4=[[F(x) for x in r] for r in w["D4_value"]];D5=[F(x) for x in w["D5_value"]]
print("shape",len(D4),len(D4[0]),len(D5))
print("rank D4:",rank(D4),"(expect 13)")
print("D4*D5==0:",all(sum(x*y for x,y in zip(r,D5))==0 for r in D4))
print("D5 nonzero:",any(D5))
print("complex_sha256:",w.get("complex_sha256"))
