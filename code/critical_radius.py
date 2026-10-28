"""Exact common-radius thresholds for arbitrary monotone contact rules.

The main construction uses three-site circumcenters and boundary support points.
A full bisector arrangement is retained as an independent control. Both sets
suffice for every winning rule on the same sites and target.
"""
from fractions import Fraction as Q
from itertools import combinations
from functools import reduce
from math import gcd,lcm
from target_certificate import _validated,sub,dot,inside_triangle


def line(a,b,c):
    values=[Q(a),Q(b),Q(c)]
    if not values[0] and not values[1]:return None
    scale=lcm(*(v.denominator for v in values));ints=[int(v*scale) for v in values]
    divisor=reduce(gcd,(abs(v) for v in ints));ints=[v//divisor for v in ints]
    if next(v for v in ints if v)<0:ints=[-v for v in ints]
    return tuple(ints)


def order_candidates(centres,triangles):
    c,_,tri=_validated(centres,[0]*len(centres),triangles)
    if not c:raise ValueError('at least one primitive site required')
    lines=set()
    for p,q in combinations(c,2):
        v=line(2*(q[0]-p[0]),2*(q[1]-p[1]),dot(p,p)-dot(q,q))
        if v is not None:lines.add(v)
    for t in tri:
        for i in range(3):
            p,q=t[i],t[(i+1)%3];d=sub(q,p)
            lines.add(line(d[1],-d[0],d[0]*p[1]-d[1]*p[0]))
    candidates={v for t in tri for v in t}
    for (a,b,d),(e,f,g) in combinations(sorted(lines),2):
        det=a*f-e*b
        if det:
            point=(Q(b*g-f*d,det),Q(d*e-g*a,det))
            if any(inside_triangle(point,t) for t in tri):candidates.add(point)
    return {'centres':tuple(c),'triangles':tri,'lines':tuple(sorted(lines)),'points':tuple(sorted(candidates))}


def distance_prefixes(centres,point):
    ranked=sorted((dot(sub(point,c),sub(point,c)),i) for i,c in enumerate(centres))
    mask=0;j=0
    while j<len(ranked):
        squared=ranked[j][0]
        while j<len(ranked) and ranked[j][0]==squared:
            mask|=1<<ranked[j][1];j+=1
        yield squared,mask


def support_candidates(centres,triangles):
    """Three-site support theorem: circumcenters and boundary bisector events."""
    c,_,tri=_validated(centres,[0]*len(centres),triangles)
    if not c:raise ValueError('at least one primitive site required')
    points={v for t in tri for v in t};edges={tuple(sorted((t[i],t[(i+1)%3]))) for t in tri for i in range(3)}
    bisectors=set()
    for p,q in combinations(c,2):
        b=line(2*(q[0]-p[0]),2*(q[1]-p[1]),dot(p,p)-dot(q,q))
        if b is None:continue
        bisectors.add(b);a,beta,gamma=b
        for u,v in edges:
            d=sub(v,u);den=a*d[0]+beta*d[1]
            if not den:continue
            t=-(a*u[0]+beta*u[1]+gamma)/den
            if 0<=t<=1:points.add((u[0]+t*d[0],u[1]+t*d[1]))
    for p,q,r in combinations(c,3):
        a=2*(q[0]-p[0]);b=2*(q[1]-p[1]);u=dot(q,q)-dot(p,p)
        d=2*(r[0]-p[0]);e=2*(r[1]-p[1]);v=dot(r,r)-dot(p,p);det=a*e-d*b
        if det:
            point=((u*e-v*b)/det,(a*v-d*u)/det)
            if any(inside_triangle(point,t) for t in tri):points.add(point)
    return {'centres':tuple(c),'triangles':tri,'lines':tuple(sorted(bisectors)),'points':tuple(sorted(points)),'construction':'three_site_support'}


def antichain_at_radius(master,radius,activation=None):
    """Reuse the universal support set at any exact rational common radius."""
    from target_certificate import minimal_label_witnesses,exact
    radius=exact(radius)
    if radius<0:raise ValueError('nonnegative radius required')
    labels={}
    for point in master['points']:
        mask=sum(1<<i for i,c in enumerate(master['centres']) if dot(sub(point,c),sub(point,c))<=radius*radius)
        if activation is not None:mask=activation(mask)
        labels.setdefault(mask,point)
    minimal=minimal_label_witnesses(labels)
    return {'masks':tuple(minimal),'witnesses':minimal,'distinct_labels':len(labels),'candidate_count':len(master['points'])}


def critical_radii(centres,triangles,rules,activation=None,master=None):
    master=support_candidates(centres,triangles) if master is None else master
    c=master['centres'];activate=(lambda mask:mask) if activation is None else activation
    if any(not rule(activate((1<<len(c))-1)) for rule in rules.values()):raise ValueError('a rule never wins at any finite radius')
    out={name:{'squared':Q(-1),'witness':None,'prefix':None} for name in rules}
    for point in master['points']:
        pending=dict(rules)
        for squared,mask in distance_prefixes(c,point):
            active=activate(mask)
            for name,rule in list(pending.items()):
                if rule(active):
                    if squared>out[name]['squared']:out[name]={'squared':squared,'witness':point,'prefix':active}
                    del pending[name]
            if not pending:break
    return {'rules':out,'candidate_count':len(master['points']),'line_count':len(master['lines']),'master':master}
