"""Exact disk facets and dual complexes for downward-closed failures.

Binary64 input coordinates/radii are interpreted as exact rationals. The
geometry uses signs in quadratic extensions, with no tolerance or raster.
Homology reported here is H0,H1 over GF(2); no higher Betti claim is made.
"""
from fractions import Fraction as Q
from itertools import combinations
import math
import numbers


def _q(value):
    value=float(value)
    if not math.isfinite(value):raise ValueError('input must be finite')
    return Q(value)


def radical_nonpositive(a,b,h):
    """Decide a+b sqrt(h)<=0 for rational a,b and h>=0, exactly."""
    if h<0:raise ValueError('negative radicand')
    if h==0 or b==0:return a<=0
    if a==0:return b<0
    if a<0 and b<0:return True
    if a>0 and b>0:return False
    if a>0:return a*a<=b*b*h
    return b*b*h<=a*a


def maximal_masks(masks):
    out=[]
    for mask in sorted(set(masks)-{0},key=lambda x:(-x.bit_count(),x)):
        if not any(mask&big==mask for big in out):out.append(mask)
    return tuple(out)


def disk_facets(centres,radii):
    """All inclusion-maximal faces of the nerve of finite closed disks.

    A leftmost circle point or a pairwise circle intersection witnesses each
    maximal face. Unequal and zero radii and coincident disks are allowed.
    """
    c=[tuple(_q(x) for x in row) for row in centres]
    if not c or any(len(row)!=2 for row in c):raise ValueError('nonempty planar centres required')
    if isinstance(radii,(int,float,Q)):radii=[radii]*len(c)
    r=[_q(x) for x in radii]
    if len(r)!=len(c) or any(x<0 for x in r):raise ValueError('one nonnegative radius per centre required')
    r2=[x*x for x in r]; candidates=set();witnesses=0
    def membership(base,perp=None,h=Q(0),sign=1):
        mask=0
        for k,p in enumerate(c):
            x,y=base[0]-p[0],base[1]-p[1]
            if perp is None:inside=x*x+y*y<=r2[k]
            else:
                a=x*x+y*y+h*(perp[0]*perp[0]+perp[1]*perp[1])-r2[k]
                b=sign*2*(x*perp[0]+y*perp[1])
                inside=radical_nonpositive(a,b,h)
            if inside:mask|=1<<k
        return mask
    for p,rr in zip(c,r):candidates.add(membership((p[0]-rr,p[1])));witnesses+=1
    for i,j in combinations(range(len(c)),2):
        dx,dy=c[j][0]-c[i][0],c[j][1]-c[i][1];d2=dx*dx+dy*dy
        if d2==0:continue
        a=(d2+r2[i]-r2[j])/(2*d2);h=r2[i]/d2-a*a
        if h<0:continue
        base=(c[i][0]+a*dx,c[i][1]+a*dy);perp=(-dy,dx)
        for sign in ([1] if h==0 else [-1,1]):
            mask=membership(base,perp,h,sign)
            assert mask&(1<<i) and mask&(1<<j)
            candidates.add(mask);witnesses+=1
    return maximal_masks(candidates),{'witnesses':witnesses,'distinct_witness_labels':len(candidates),'sensors':len(c)}


def threshold(k):
    if not isinstance(k,int) or k<1:raise ValueError('k must be a positive integer')
    return lambda mask:mask.bit_count()>=k


def domain_threshold(domains,k=2):
    if not isinstance(k,int) or k<1:raise ValueError('k must be a positive integer')
    domains=tuple(domains)
    for domain in domains:hash(domain)
    def wins(mask):
        if mask<0 or mask>>len(domains):raise ValueError('mask outside contact set')
        return len({d for i,d in enumerate(domains) if mask>>i&1})>=k
    return wins


def weighted_threshold(costs,budget):
    costs=tuple(costs)
    if any(not isinstance(c,numbers.Integral) or c<0 for c in costs):
        raise ValueError('costs must be nonnegative integers')
    if not isinstance(budget,numbers.Integral) or budget<0:
        raise ValueError('budget must be a nonnegative integer')
    def wins(mask):
        if mask<0 or mask>>len(costs):raise ValueError('mask outside contact set')
        return sum(c for i,c in enumerate(costs) if mask>>i&1)>budget
    return wins


def triangle_certificate(centres,radii,triangle,wins):
    """Sufficient continuous closed-triangle coverage certificate, exactly.

    At each vertex retain disks containing the radius D/sqrt(3) neighborhood,
    where D is the triangle diameter. Every retained contact set must win.
    A false return is inconclusive, not a proof of failed coverage.
    """
    c=[tuple(_q(x) for x in row) for row in centres]
    t=[tuple(_q(x) for x in row) for row in triangle]
    if len(t)!=3 or any(len(row)!=2 for row in t+c):raise ValueError('three planar vertices required')
    if isinstance(radii,(int,float,Q)):radii=[radii]*len(c)
    r=[_q(x) for x in radii]
    if len(r)!=len(c) or any(x<0 for x in r):raise ValueError('invalid radii')
    d2=max(sum((a-b)**2 for a,b in zip(t[i],t[j])) for i,j in combinations(range(3),2))
    h=d2/3;masks=[]
    for v in t:
        mask=0
        for i,p in enumerate(c):
            distance2=sum((a-b)**2 for a,b in zip(v,p))
            if r[i]*r[i]>=h and radical_nonpositive(distance2-r[i]*r[i]-h,2*r[i],h):mask|=1<<i
        masks.append(mask)
    return {'certified':all(wins(mask) for mask in masks),'vertex_masks':[hex(mask) for mask in masks],
            'diameter_squared':[d2.numerator,d2.denominator]}


def gf2_rank(columns):
    pivots={}
    for c in columns:
        while c:
            lead=c.bit_length()-1
            if lead in pivots:c^=pivots[lead]
            else:pivots[lead]=c;break
    return len(pivots)


def dual_betti(facets,wins):
    """H0,H1 of the facet-intersection complex, including its full 2-skeleton."""
    v=[f for f in facets if wins(f)]
    parent=list(range(len(v)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    edges=[];lookup={}
    for i,j in combinations(range(len(v)),2):
        if wins(v[i]&v[j]):
            lookup[i,j]=len(edges);edges.append((i,j))
            a,b=find(i),find(j)
            if a!=b:parent[b]=a
    columns=[];triangles=0
    for i,j,k in combinations(range(len(v)),3):
        if (i,j) in lookup and (i,k) in lookup and (j,k) in lookup and wins(v[i]&v[j]&v[k]):
            columns.append((1<<lookup[i,j])^(1<<lookup[i,k])^(1<<lookup[j,k]));triangles+=1
    b0=len({find(i) for i in range(len(v))});rank=gf2_rank(columns)
    return {'vertices':len(v),'edges':len(edges),'triangles':triangles,'rank_d2':rank,
            'b0':b0,'b1':len(edges)-len(v)+b0-rank}


def minimal_winners(n,wins):
    return [s for s in range(1,1<<n) if wins(s) and all(not wins(s^(1<<i)) for i in range(n) if s>>i&1)]


def shadow_betti_small(facets,n,wins):
    """Independent minimal-coalition construction for exhaustive small controls."""
    coalitions=[s for s in minimal_winners(n,wins) if any(s&f==s for f in facets)]
    # For an arbitrary union-nerve, count H0,H1 by the same boundary algebra,
    # using unions and a face oracle rather than intersections of facets.
    def face(mask):return any(mask&f==mask for f in facets)
    edges=[];lookup={}
    for i,j in combinations(range(len(coalitions)),2):
        if face(coalitions[i]|coalitions[j]):lookup[i,j]=len(edges);edges.append((i,j))
    parent=list(range(len(coalitions)))
    def find(i):
        while parent[i]!=i:parent[i]=parent[parent[i]];i=parent[i]
        return i
    for i,j in edges:
        a,b=find(i),find(j)
        if a!=b:parent[b]=a
    columns=[]
    for i,j,k in combinations(range(len(coalitions)),3):
        if (i,j) in lookup and (i,k) in lookup and (j,k) in lookup and face(coalitions[i]|coalitions[j]|coalitions[k]):
            columns.append((1<<lookup[i,j])^(1<<lookup[i,k])^(1<<lookup[j,k]))
    b0=len({find(i) for i in range(len(coalitions))})
    return b0,len(edges)-len(coalitions)+b0-gf2_rank(columns)
