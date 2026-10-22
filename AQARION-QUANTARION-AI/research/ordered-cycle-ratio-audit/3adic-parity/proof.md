# Source-dependent 3-adic exclusion

## Source and convention

The external theorem is Theorem 1.1 of:
Min Qiu, Yulu Feng, Shaofang Hong,
"The 3-adic valuations of Stirling numbers of the first kind",
arXiv:2109.13458v1, dated 28 September 2021.
https://arxiv.org/abs/2109.13458

Its Stirling numbers count permutation cycles, matching the unsigned
convention used here. This source is not to be conflated with a later
similarly titled paper.

The result below is a corollary of that external theorem and Legendre's
formula. No independent proof of the external valuation theorem is supplied.

## Same-parity corollary

Let N=a*3^r, a in {1,2}, r>=1.
For 1<=m<N with m congruent to a modulo 2, choose the smallest ell>=1
such that m<=a*3^ell-2, and put k=a*3^ell-m.

Then ell<=r and k is even.
Except for a=1,m=1, the written hypotheses of the source theorem hold:
    2<=k<=2*a*3^(ell-1)+1<a*3^ell.

In its even-offset case the source gives
v3(c(N,m)) =
    a(3^r-3^ell)/2 - (r-ell)m + ell-1-v3(k).

The exceptional a=1,m=1 case is handled directly:
    c(N,1)=(N-1)!.

Digit complementation gives
    s3(m)=a-1+2ell-s3(k-1).
Legendre's formula then yields the exact gap
    v3(N!/m!)-v3(c(N,m))
      =1+(r-ell)m+v3(k!) > 0.

For a=1,m=1 the gap is r, agreeing with the same expression at ell=1,k=2.

Equality R(N,m)=1 would require
    c(N,m)=(N!/m!)P(N,m),
where P(N,m) is a positive integer. The positive gap contradicts this.

More strongly,
    v3(R(N,m))=-gap-v3(P(N,m))<0,
so the ratio is not an integer.

Thus every odd m<N is excluded when N=3^r, and every even m<N is
excluded when N=2*3^r. The Case B subset has N>2m.

## Original five-case family

For N=3^r and m=3^(r-1)-2, r>=2:
    v3(c(N,m))=r,
    v3(N!/m!)=3^(r-1)+r-1,
    gap=3^(r-1)-1.

Use the direct factorial identity for r=2; the written source-theorem
hypotheses apply to the chosen offset for r>=3.

## Evidence boundaries

The original audit directly checks five cases r=2,...,6.
The expanded audit checks 1629 same-parity instances across twelve
selected totals through N=1458, including 816 Case B instances.

Finite checks validate the implementation and source translation.
The infinite assertion depends on the stated external theorem.
No opposite-parity or arbitrary-total classification is asserted.

The global ratio classification, formal certification, and novelty
determination remain open.
This proof note was authored at packaging time.
