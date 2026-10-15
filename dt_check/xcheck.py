import itertools, sys, time
from prof import rgs, profile
from closure_profile_repo import closure_profile
t0=time.time(); N=int(sys.argv[1]); cases=bad=fails=0; ex=[]
for n in range(1,N+1):
    for T in itertools.product(range(n),repeat=n):
        for lab in rgs(n):
            k=max(lab)+1
            basis=[[1 if lab[x]==b else 0 for x in range(n)] for b in range(k)]
            r=closure_profile(list(T),basis); mine=profile(T,lab)
            rp=tuple(r["profile"]); rp=rp[:-1] if rp and rp[-1]==0 else rp
            cases+=1
            if r["result"]!="PASS": fails+=1
            if (k,rp)!=mine or r["total_linear_repair_cost"]!=sum(mine[1]):
                bad+=1
                if len(ex)<3: ex.append((T,lab,r["profile"],mine))
print(f"n<={N}: cases={cases} repo-vs-independent profile mismatches={bad} repo self-check FAIL={fails} ({time.time()-t0:.0f}s)")
print(ex)
