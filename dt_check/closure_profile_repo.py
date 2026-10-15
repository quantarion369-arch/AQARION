from fractions import Fraction
def validate_transition(T):
    T=list(T); n=len(T)
    if n==0: raise ValueError("state space must be nonempty")
    for t in T:
        if not isinstance(t,int) or t<0 or t>=n: raise ValueError("T must map {0,...,n-1} into itself")
    return T
def validate_basis(T, initial_basis):
    n=len(T)
    if not initial_basis: raise ValueError("initial_basis must be nonempty")
    cols=[]
    for c in initial_basis:
        if len(c)!=n: raise ValueError("each observable column must have length n")
        cols.append([Fraction(v) for v in c])
    return cols
def koopman_matrix(T):
    n=len(T); return [[Fraction(int(T[x]==y)) for y in range(n)] for x in range(n)]
def koopman_apply_column(T,column): return [column[T[x]] for x in range(len(T))]
def columns_to_matrix(columns):
    if not columns: return []
    n=len(columns[0])
    if any(len(c)!=n for c in columns): raise ValueError("all observable columns must have equal length")
    return [[c[x] for c in columns] for x in range(n)]
def matmul(A,B): return [[sum(A[i][r]*B[r][j] for r in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]
def rank_q(matrix):
    A=[[Fraction(v) for v in row] for row in matrix]
    if not A: return 0
    rows,cols=len(A),len(A[0]); pr=0
    for col in range(cols):
        piv=None
        for row in range(pr,rows):
            if A[row][col]!=0: piv=row; break
        if piv is None: continue
        A[pr],A[piv]=A[piv],A[pr]; pv=A[pr][col]; A[pr]=[v/pv for v in A[pr]]
        for row in range(rows):
            if row==pr or A[row][col]==0: continue
            f=A[row][col]; A[row]=[v-f*p for v,p in zip(A[row],A[pr])]
        pr+=1
        if pr==rows: break
    return pr
def orthogonal_projection_from_columns(columns):
    n=len(columns[0]); proj=[[Fraction(0)]*n for _ in range(n)]; ob=[]
    for vec in columns:
        vec=[Fraction(v) for v in vec]
        for b in ob:
            dp=sum(l*r for l,r in zip(vec,b)); bn=sum(v*v for v in b); c=dp/bn
            vec=[l-c*r for l,r in zip(vec,b)]
        ns=sum(v*v for v in vec)
        if ns==0: continue
        ob.append(vec)
        for x in range(n):
            for y in range(n): proj[x][y]+=vec[x]*vec[y]/ns
    return proj
def closure_profile(T, initial_basis):
    T=validate_transition(T); columns=validate_basis(T,initial_basis); K=koopman_matrix(T)
    dims=[rank_q(columns_to_matrix(columns))]; inc=[]; dr=[]
    for stage in range(len(T)+1):
        P=orthogonal_projection_from_columns(columns)
        IP=[[Fraction(int(x==y))-P[x][y] for y in range(len(T))] for x in range(len(T))]
        D=matmul(IP,matmul(K,P)); dr.append(rank_q(D))
        img=[koopman_apply_column(T,c) for c in columns]; enl=columns+img
        ed=rank_q(columns_to_matrix(enl)); i=ed-dims[-1]; inc.append(i); dims.append(ed)
        if i==0: break
        columns=enl
    checks={"increment_identity":all(dr[j]==inc[j] for j in range(len(inc))),
            "monotonicity":all(inc[j+1]<=inc[j] for j in range(len(inc)-1)),
            "telescoping_sum":(dims[-1]-dims[0]==sum(inc))}
    return {"state_count":len(T),"initial_dimension":dims[0],"final_dimension":dims[-1],"profile":inc,"defect_ranks":dr,
            "stabilization_stage":len(inc)-1,"total_linear_repair_cost":dims[-1]-dims[0],"checks":checks,
            "result":"PASS" if all(checks.values()) else "FAIL"}
