"""Exact full-target certificates using rational vertical slices.

Targets are finite unions of nondegenerate closed rational triangles. Fraction
and integer values are preserved; floats are interpreted as their binary64
rationals. Subsequent arithmetic is rational or exact quadratic comparison.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
from functools import cmp_to_key
from itertools import combinations
from math import isqrt
from robust_coverage import radical_nonpositive,_q


def exact(value):
    return value if isinstance(value,Q) else Q(value) if isinstance(value,int) else _q(value)


def sign_rational(q):return (q>0)-(q<0)


def radical_sign(a,b,h):
    if radical_nonpositive(a,b,h):
        return 0 if radical_nonpositive(-a,-b,h) else -1
    return 1


@dataclass(frozen=True)
class Quadratic:
    a: Q
    b: Q=Q(0)
    h: Q=Q(0)

    def __post_init__(self):
        object.__setattr__(self,'a',Q(self.a));object.__setattr__(self,'b',Q(self.b));object.__setattr__(self,'h',Q(self.h))
        if self.h<0:raise ValueError('negative radicand')

    def compare(self,other):
        if not isinstance(other,Quadratic):other=Quadratic(other)
        a=self.a-other.a;b=self.b;h=self.h;d=other.b;k=other.h
        sx=radical_sign(a,b,h);sy=sign_rational(d) if k else 0
        if sx!=sy:return sign_rational(sx-sy)
        if not sx:return 0
        return sx*radical_sign(a*a+b*b*h-d*d*k,2*a*b,h)

    def enclosure(self,bits):
        scale=1<<bits;t=(self.h.numerator<<(2*bits))//self.h.denominator
        root=isqrt(t);lo=Q(root,scale)
        hi=lo if root*root*self.h.denominator==self.h.numerator<<(2*bits) else Q(root+1,scale)
        if self.b>=0:return self.a+self.b*lo,self.a+self.b*hi
        return self.a+self.b*hi,self.a+self.b*lo


def sorted_unique(values):
    values=sorted(values,key=cmp_to_key(lambda x,y:x.compare(y)));out=[]
    for x in values:
        if not out or x.compare(out[-1]):out.append(x)
    return out


def rational_between(left,right):
    if left.compare(right)>=0:raise ValueError('strictly ordered endpoints required')
    bits=4
    while True:
        _,a=left.enclosure(bits);b,_=right.enclosure(bits)
        if a<b:return (a+b)/2
        bits*=2


def cross(a,b):return a[0]*b[1]-a[1]*b[0]
def sub(a,b):return (a[0]-b[0],a[1]-b[1])
def dot(a,b):return a[0]*b[0]+a[1]*b[1]


def inside_triangle(point,triangle,strict=False):
    signs=[cross(sub(triangle[(i+1)%3],triangle[i]),sub(point,triangle[i])) for i in range(3)]
    return all(s>0 for s in signs) or all(s<0 for s in signs) if strict else all(s>=0 for s in signs) or all(s<=0 for s in signs)


def _validated(centres,radii,triangles):
    centres=[tuple(exact(x) for x in row) for row in centres]
    if any(len(p)!=2 for p in centres):raise ValueError('planar centres required')
    if isinstance(radii,(int,float,Q)):radii=[radii]*len(centres)
    radii=[exact(r) for r in radii]
    if len(radii)!=len(centres) or any(r<0 for r in radii):raise ValueError('nonnegative radii required')
    triangles=[tuple(tuple(exact(x) for x in row) for row in t) for t in triangles]
    if not triangles:raise ValueError('nonempty regular closed target required')
    for t in triangles:
        if len(t)!=3 or any(len(v)!=2 for v in t) or cross(sub(t[1],t[0]),sub(t[2],t[0]))==0:
            raise ValueError('nondegenerate planar triangles required')
    return centres,radii,triangles


def _edges(triangles):
    return sorted(set(tuple(sorted((t[i],t[(i+1)%3]))) for t in triangles for i in range(3)))


def critical_x(centres,radii,edges):
    events=[Quadratic(p[0]) for e in edges for p in e]
    events += [Quadratic(c[0]+s*r) for c,r in zip(centres,radii) for s in [-1,1]]
    for i,j in combinations(range(len(centres)),2):
        d=sub(centres[j],centres[i]);s=dot(d,d)
        if not s:continue
        a=(s+radii[i]**2-radii[j]**2)/(2*s);h=radii[i]**2/s-a*a
        if h>=0:
            for sign in [-1,1]:events.append(Quadratic(centres[i][0]+a*d[0],-sign*d[1],h))
    for c,r in zip(centres,radii):
        for p,q in edges:
            d=sub(q,p);z=sub(p,c);a=dot(d,d);b=2*dot(d,z);v=dot(z,z)-r*r;disc=b*b-4*a*v
            if disc<0:continue
            for sign in [-1,1]:
                t=Quadratic(-b/(2*a),Q(sign,2*a),disc)
                if t.compare(Q(0))>=0 and t.compare(Q(1))<=0:
                    events.append(Quadratic(p[0]-d[0]*b/(2*a),d[0]*Q(sign,2*a),disc))
    for (p,q),(u,v) in combinations(edges,2):
        d=sub(q,p);e=sub(v,u);den=cross(d,e)
        if not den:continue
        t=cross(sub(u,p),e)/den;s=cross(sub(u,p),d)/den
        if 0<=t<=1 and 0<=s<=1:events.append(Quadratic(p[0]+t*d[0]))
    return sorted_unique(events)


def minimal_label_witnesses(witnesses):
    out={}
    for mask,point in sorted(witnesses.items(),key=lambda item:(item[0].bit_count(),item[0])):
        if not any(s&mask==s for s in out):out[mask]=point
    return out


def target_antichain(centres,radii,triangles,activation=None):
    """Canonical minimal contact patterns; include a rational witness per mask.

    activation, when supplied, must be an inclusion-monotone integer-mask map.
    It can implement bundled virtual contacts or fault-domain coarsening.
    """
    c,r,tri=_validated(centres,radii,triangles);edges=_edges(tri)
    events=critical_x(c,r,edges);witnesses={};bands=0;target_samples=0
    minx=min(v[0] for t in tri for v in t);maxx=max(v[0] for t in tri for v in t)
    events=[v for v in events if v.compare(minx)>=0 and v.compare(maxx)<=0]
    for left,right in zip(events,events[1:]):
        x=rational_between(left,right);ys=[]
        for p,q in edges:
            if min(p[0],q[0])<x<max(p[0],q[0]):ys.append(Quadratic(p[1]+(x-p[0])*(q[1]-p[1])/(q[0]-p[0])))
        for centre,radius in zip(c,r):
            h=radius*radius-(x-centre[0])**2
            if h>0:ys += [Quadratic(centre[1],Q(-1),h),Quadratic(centre[1],Q(1),h)]
        ys=sorted_unique(ys)
        for lower,upper in zip(ys,ys[1:]):
            y=rational_between(lower,upper);bands+=1;point=(x,y)
            if not any(inside_triangle(point,t,strict=True) for t in tri):continue
            target_samples+=1;mask=0
            for i,(centre,radius) in enumerate(zip(c,r)):
                if dot(sub(point,centre),sub(point,centre))<=radius*radius:mask|=1<<i
            if activation is not None:mask=activation(mask)
            witnesses.setdefault(mask,point)
    if not witnesses:raise RuntimeError('no target samples: decomposition is incomplete')
    minimal=minimal_label_witnesses(witnesses)
    return {'masks':tuple(minimal),'witnesses':minimal,'distinct_labels':len(witnesses),
            'x_events':len(events),'bands':bands,'target_samples':target_samples,'primitive_disks':len(c),'target_edges':len(edges)}


def covers(certificate,wins):
    losing=[mask for mask in certificate['masks'] if not wins(mask)]
    return {'covered':not losing,'losing_mask':None if not losing else losing[0],
            'witness':None if not losing else certificate['witnesses'][losing[0]]}


def map_certificate(certificate,activation):
    mapped={}
    for mask in certificate['masks']:mapped.setdefault(activation(mask),certificate['witnesses'][mask])
    minimal=minimal_label_witnesses(mapped)
    return dict(certificate,masks=tuple(minimal),witnesses=minimal)


def deletion_cost(certificate,costs):
    costs=tuple(Q(c) for c in costs)
    if any(c<0 for c in costs):raise ValueError('nonnegative costs required')
    if any(m>>len(costs) for m in certificate['masks']):raise ValueError('cost vector too short')
    mask=min(certificate['masks'],key=lambda m:sum(c for i,c in enumerate(costs) if m>>i&1))
    return {'cost':sum(c for i,c in enumerate(costs) if mask>>i&1),'mask':mask,'witness':certificate['witnesses'][mask]}
