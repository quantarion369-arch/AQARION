#!/usr/bin/env python3
"""Exact quotient census of twelve-circuits with eight odd coefficients."""

import hashlib
import itertools as it
import json
import math
import sys
import time
import traceback
from collections import Counter,defaultdict
from datetime import datetime,timezone
from fractions import Fraction
from pathlib import Path

F = [
    [1]
    + [(x>>i)&1 for i in range(6)]
    + [
        ((x>>i)&1)*((x>>j)&1)
        for i,j in it.combinations(range(6),2)
    ]
    for x in range(64)
]

def need(ok,message):
    if not ok:
        raise RuntimeError(message)

def sha(data):
    return hashlib.sha256(data).hexdigest()

def support_hash(supports):
    h=hashlib.sha256()
    for support in sorted(supports):
        h.update(bytes(support))
    return h.hexdigest()

def pattern(coefficients):
    return " ".join(
        str(v)+"^"+str(n)
        for v,n in sorted(Counter(map(abs,coefficients)).items())
    )

def rank_forward(rows):
    a=[[Fraction(v) for v in row] for row in rows]
    rank=0
    for col in range(len(a[0])):
        pivot=next(
            (i for i in range(rank,len(a)) if a[i][col]),
            None,
        )
        if pivot is None:
            continue
        a[rank],a[pivot]=a[pivot],a[rank]
        value=a[rank][col]
        a[rank]=[v/value for v in a[rank]]
        for i in range(rank+1,len(a)):
            value=a[i][col]
            if value:
                a[i]=[
                    x-value*y for x,y in zip(a[i],a[rank])
                ]
        rank+=1
        if rank==len(a):
            break
    return rank

def base_rref(flat):
    a=[
        [Fraction(v) for v in F[x]]
        + [Fraction(i==j) for j in range(8)]
        for i,x in enumerate(flat)
    ]
    pivots=[]
    rank=0
    for col in range(22):
        pivot=next(
            (i for i in range(rank,8) if a[i][col]),
            None,
        )
        if pivot is None:
            continue
        a[rank],a[pivot]=a[pivot],a[rank]
        value=a[rank][col]
        a[rank]=[v/value for v in a[rank]]
        for i in range(8):
            if i!=rank and a[i][col]:
                value=a[i][col]
                a[i]=[
                    x-value*y for x,y in zip(a[i],a[rank])
                ]
        pivots.append(col)
        rank+=1
        if rank==8:
            break
    need(rank==8,"Flat does not have rank eight")
    return a,pivots

def projective(vector):
    divisor=math.gcd(*vector)
    if not divisor:
        return None,0
    sign=1 if next(x for x in vector if x)>0 else -1
    scale=sign*divisor
    return tuple(x//scale for x in vector),scale

def quotient_classes(flat):
    a,pivots=base_rref(flat)
    free=[j for j in range(22) if j not in pivots]
    classes=defaultdict(list)

    for x in sorted(set(range(64))-set(flat)):
        gamma=[F[x][j] for j in pivots]
        residual=[
            Fraction(F[x][j])
            -sum(gamma[i]*a[i][j] for i in range(8))
            for j in range(22)
        ]
        need(all(residual[j]==0 for j in pivots),
             "Projection pivot coordinates did not vanish")

        denominator=math.lcm(
            *(residual[j].denominator for j in free)
        )
        integers=[int(residual[j]*denominator) for j in free]
        vector,rho=projective(integers)
        need(vector is not None,"Zero outside quotient residual")
        scale=Fraction(denominator,rho)

        coordinates=tuple(
            sum(gamma[i]*a[i][22+j] for i in range(8))
            for j in range(8)
        )

        need(all(
            Fraction(F[x][j])
            ==sum(coordinates[i]*F[flat[i]][j] for i in range(8))
              +residual[j]
            for j in range(22)
        ),"Exact quotient reconstruction failed")

        need(all(
            residual[j]==Fraction(vector[k])/scale
            for k,j in enumerate(free)
        ),"Projective scaling failed")

        classes[vector].append((x,scale,coordinates))

    need(sum(map(len,classes.values()))==56,
         "Outside-point coverage failed")
    return classes

def span(basis):
    return tuple(sorted(
        (a*basis[0])^(b*basis[1])^(c*basis[2])
        for a,b,c in it.product((0,1),repeat=3)
    ))

def direction_orbits():
    directions=set()
    for pivots in it.combinations(range(6),3):
        slots=[
            (i,j)
            for i in range(3)
            for j in range(pivots[i]+1,6)
            if j not in pivots
        ]
        for mask in range(1<<len(slots)):
            basis=[1<<p for p in pivots]
            for k,(i,j) in enumerate(slots):
                basis[i]|=((mask>>k)&1)<<j
            directions.add(span(basis))

    need(len(directions)==1395,"Direction count mismatch")
    ranks=Counter()
    rank8=set()

    for flat in sorted(directions):
        rank=rank_forward([F[x] for x in flat])
        need(rank in (7,8),"Unexpected direction rank")
        ranks[rank]+=1
        if rank==8:
            rank8.add(flat)

    need(dict(ranks)=={7:350,8:1045},
         "Exact direction-rank distribution mismatch")

    maps=[
        tuple(
            sum(((x>>i)&1)<<p[i] for i in range(6))
            for x in range(64)
        )
        for p in it.permutations(range(6))
    ]

    remaining=set(rank8)
    orbits=[]
    while remaining:
        flat=min(remaining)
        images={}
        for mapping in maps:
            transformed=tuple(sorted(mapping[x] for x in flat))
            images.setdefault(transformed,mapping)
        need(set(images)<=remaining,"Direction orbit partition failed")
        remaining.difference_update(images)
        orbits.append((flat,images))

    need(len(orbits)==15,"Rank-eight direction orbit count")
    need(sum(len(images) for flat,images in orbits)==1045,
         "Rank-eight direction coverage")
    return orbits

def primitive(values):
    denominator=math.lcm(*(v.denominator for v in values))
    integers=[int(v*denominator) for v in values]
    divisor=math.gcd(*integers)
    need(divisor!=0,"Zero reconstructed relation")
    return [v//divisor for v in integers]

def audit_flat(flat):
    classes=quotient_classes(flat)
    vectors=sorted(classes)
    accepted={}
    counts=Counter()
    stats=Counter()
    dimension=len(vectors[0])
    number=len(vectors)

    for i in range(number):
        u=vectors[i]
        a=next(q for q in range(dimension) if u[q])

        for j in range(i+1,number):
            v=vectors[j]
            b=next(
                (q for q in range(dimension)
                 if u[a]*v[q]-u[q]*v[a]),
                None,
            )
            need(b is not None,"Distinct classes are proportional")
            determinant=u[a]*v[b]-u[b]*v[a]
            groups=defaultdict(list)

            stats["projective_quadruples_covered"]+=math.comb(
                number-j-1,2
            )

            for k in range(j+1,number):
                w=vectors[k]
                A=w[a]*v[b]-w[b]*v[a]
                B=u[a]*w[b]-u[b]*w[a]
                projected=[
                    determinant*w[q]-A*u[q]-B*v[q]
                    for q in range(dimension)
                ]
                signature,rho=projective(projected)
                need(signature is not None,
                     "Dependent distinct projective triple")
                groups[signature].append((k,A,B,rho))
                stats["triple_projections"]+=1

            for group in groups.values():
                for left,right in it.combinations(group,2):
                    k,Ak,Bk,rk=left
                    l,Al,Bl,rl=right
                    relation=(
                        rk*Al-rl*Ak,
                        rk*Bl-rl*Bk,
                        determinant*rl,
                        -determinant*rk,
                    )
                    ids=(i,j,k,l)
                    need(all(relation),"Four-class relation has zero entry")
                    need(all(
                        sum(relation[t]*vectors[ids[t]][q]
                            for t in range(4))==0
                        for q in range(dimension)
                    ),"Exact quotient relation failed")
                    stats["dependent_projective_quadruples"]+=1

                    for choices in it.product(*(
                        classes[vectors[h]] for h in ids
                    )):
                        stats["actual_point_quadruples_tested"]+=1
                        outside=[choice[0] for choice in choices]
                        tail=[
                            Fraction(relation[t])*choices[t][1]
                            for t in range(4)
                        ]
                        head=[
                            -sum(tail[t]*choices[t][2][q]
                                 for t in range(4))
                            for q in range(8)
                        ]
                        coefficients=primitive(head+tail)
                        points=list(flat)+outside

                        need(all(
                            sum(coefficients[t]*F[x][q]
                                for t,x in enumerate(points))==0
                            for q in range(22)
                        ),"Reconstructed integer identity failed")
                        stats["integer_kernel_vector_checks"]+=1

                        rows=[F[x] for x in points]
                        need(rank_forward(rows)==11,
                             "Direct candidate rank is not eleven")
                        stats["direct_candidate_rank_checks"]+=1

                        if not all(coefficients):
                            stats["proper_dependency_rejections"]+=1
                            continue

                        odd={
                            x for x,c in zip(points,coefficients)
                            if c%2
                        }
                        if odd!=set(flat):
                            stats["noncanonical_odd_flat_rejections"]+=1
                            continue

                        pairs=sorted(zip(points,coefficients))
                        support=tuple(x for x,c in pairs)
                        kernel=tuple(c for x,c in pairs)
                        if kernel[0]<0:
                            kernel=tuple(-v for v in kernel)

                        need(support not in accepted,
                             "Repeated canonical support")
                        for deleted in range(12):
                            need(
                                rank_forward(
                                    rows[:deleted]+rows[deleted+1:]
                                )==11,
                                "Direct deletion rank failed",
                            )
                            stats["direct_deletion_rank_checks"]+=1

                        accepted[support]=kernel
                        counts[pattern(kernel)]+=1

    need(
        stats["triple_projections"]==math.comb(number,3),
        "Projective-triple coverage mismatch",
    )
    need(
        stats["projective_quadruples_covered"]==math.comb(number,4),
        "Projective-quadruple coverage mismatch",
    )
    return accepted,counts,stats,len(classes)

def bind_007(path):
    entries=[
        line.split("  ",1)
        for line in (path/"SHA256SUMS").read_text().splitlines()
    ]
    need(all(len(entry)==2 for entry in entries),
         "Malformed 007 manifest")

    for digest,name in entries:
        need(Path(name).name==name,"Unsafe 007 manifest path")
        need(sha((path/name).read_bytes())==digest,
             "007 manifest mismatch: "+name)

    raw=(path/"REPORT.json").read_bytes()
    report=json.loads(raw)
    need(report.get("status")=="PASS","007 is not PASS")
    need(report.get("experiment")=="ODD-TWELVE-HYPERPLANE-007",
         "Wrong 007 experiment")
    source_hash=sha((path/"audit_odd12.py").read_bytes())
    need(source_hash==report.get("source_sha256"),
         "007 source binding failed")
    need(
        source_hash
        =="093518636f2e5127b04f9ce86f05e3a5f03037e8baec61d9ff19e0a6fd982dbe",
        "007 source differs from supplied successful run",
    )
    need(
        report.get("global_pattern_counts")
        =={"1^12":206304,"1^10 3^2":4032},
        "007 pattern counts differ",
    )
    need(report.get("odd_support_twelve_sector_count")==210336,
         "007 sector total differs")
    need((path/"exit.txt").read_text().strip()=="0",
         "007 exit status differs")
    return {
        "source_sha256":source_hash,
        "report_sha256":sha(raw),
        "odd_support_twelve_sector_count":210336,
    }

def audit(report,output,dependency):
    need(rank_forward([[0,1],[1,0]])==2,
         "Row-swap control")
    need(rank_forward([[1,2],[2,4]])==1,
         "Singular control")

    report["dependency_007"]=bind_007(dependency)
    orbits=direction_orbits()
    global_sets=defaultdict(set)
    expected_global=Counter()
    totals=Counter()
    orbit_records=[]
    witness_records=[]

    for number,(flat,images) in enumerate(orbits,1):
        accepted,counts,stats,class_count=audit_flat(flat)
        totals.update(stats)
        expected_global.update({
            key:8*len(images)*count
            for key,count in counts.items()
        })

        for support,kernel in accepted.items():
            witness_records.append({
                "base_flat":flat,
                "support":support,
                "primitive_kernel":kernel,
            })

        for direction,mapping in images.items():
            remaining=set(range(64))
            cosets=[]
            while remaining:
                representative=min(remaining)
                remaining.difference_update({
                    representative^x for x in direction
                })
                cosets.append(representative)
            need(len(cosets)==8,"Coset coverage failed")

            for representative in cosets:
                for support,kernel in accepted.items():
                    transformed=tuple(sorted(
                        mapping[x]^representative for x in support
                    ))
                    key=pattern(kernel)
                    need(transformed not in global_sets[key],
                         "Repeated global canonical support")
                    global_sets[key].add(transformed)

        orbit_records.append({
            "representative_flat":flat,
            "direction_orbit_size":len(images),
            "projective_classes":class_count,
            "canonical_circuits_per_flat":len(accepted),
            "pattern_counts_per_flat":dict(counts),
            "checks":dict(stats),
        })

        print(
            "ORBIT:",number,"/",len(orbits),
            "DIRECTIONS:",len(images),
            "CANONICAL CIRCUITS/FLAT:",len(accepted),
            "PATTERNS:",dict(counts),
            flush=True,
        )

    actual={key:len(supports) for key,supports in global_sets.items()}
    need(Counter(actual)==expected_global,
         "Explicit support sets disagree with symmetry weighting")
    need(
        sum(actual.values())
        ==len(set().union(*global_sets.values())),
        "Primitive-pattern families overlap",
    )

    previous=global_sets.get("1^7 2^4 3^1",set())
    need(
        support_hash(previous)
        =="a0e5c92af5f1902fc9ce7cd11073df3ed0703166d745255076e60806f8f040c3",
        "Retained 44800-support family digest not reproduced",
    )

    sector=sum(actual.values())
    report.update({
        "rank_eight_direction_orbits":len(orbits),
        "rank_eight_directions_covered":
            sum(len(images) for flat,images in orbits),
        "global_pattern_counts":actual,
        "global_support_sha256":{
            key:support_hash(supports)
            for key,supports in global_sets.items()
        },
        "odd_support_eight_sector_count":sector,
        "canonical_representative_supports":len(witness_records),
        "checks":dict(totals),
        "all_global_supports_individually_rank_checked":False,
        "global_certification_method":
            "Exact canonical quotient kernels, separate rational "
            "candidate/deletion ranks, then valid coordinate "
            "permutations and affine translations.",
        "conditional_combined_twelve_count_with_007":
            sector+210336,
        "coverage_dependency":
            "Primitive parity reduction and binary minimum-weight "
            "classification force the eight odd points to be an "
            "affine 3-flat. Circuit minimality gives its rational "
            "rank eight. The primitive odd support selects the "
            "canonical counting flat.",
        "formal_proof":False,
        "novelty_claim":False,
    })

    (output/"ORBIT-CASES.json").write_text(
        json.dumps(orbit_records,indent=2)+"\n"
    )
    (output/"REPRESENTATIVE-CIRCUITS.json").write_text(
        json.dumps(witness_records,indent=2)+"\n"
    )

def main():
    started=time.monotonic()
    source=Path(__file__).resolve()
    original=source.read_bytes()
    output=Path(sys.argv[1]).resolve()
    dependency=Path(sys.argv[2]).resolve()

    report={
        "experiment":"ODD-EIGHT-QUOTIENT-008",
        "status":"RUNNING",
        "started_utc":datetime.now(timezone.utc).isoformat(),
        "source_sha256":sha(original),
        "python_version":sys.version,
        "scope":
            "Exact odd-support-eight twelve-circuit census under "
            "the stated parity-containment reduction. Combined "
            "twelve-point conclusion depends on retained 007 and "
            "the classical parity/support theorems. No formal "
            "proof or novelty claim.",
    }

    try:
        audit(report,output,dependency)
        need(source.read_bytes()==original,"Source changed")
        report["source_unchanged"]=True
        report["status"]="PASS"
    except Exception as exc:
        report["status"]="FAIL"
        report["error"]=type(exc).__name__+": "+str(exc)
        (output/"traceback.txt").write_text(traceback.format_exc())

    report["finished_utc"]=datetime.now(timezone.utc).isoformat()
    report["elapsed_seconds"]=round(time.monotonic()-started,6)
    (output/"REPORT.json").write_text(
        json.dumps(report,indent=2,sort_keys=True)+"\n"
    )
    print(json.dumps(report,indent=2,sort_keys=True),flush=True)
    return 0 if report["status"]=="PASS" else 2

if __name__=="__main__":
    raise SystemExit(main())
