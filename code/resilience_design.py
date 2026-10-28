"""Finite design consequences of an exact geometric target antichain."""
from fractions import Fraction as Q
from itertools import product
from target_certificate import map_certificate


def bundle_activation(bundles):
    bundles=tuple(None if b is None else tuple(b) for b in bundles)
    def activate(mask):
        return sum(1<<i for i,bundle in enumerate(bundles)
                   if bundle is not None and all(mask>>j&1 for j in bundle))
    return activate


def domain_activation(domains):
    domains=tuple(domains)
    if any(not isinstance(g,int) or g<0 for g in domains):raise ValueError('nonnegative integer domain labels required')
    return lambda mask:sum(1<<g for g in {domains[i] for i in range(len(domains)) if mask>>i&1})


def survives_loss(mask,failed):return bool(mask&~failed)


def reliability(certificate,probabilities):
    """Exact enumeration for independent Bernoulli failures, not polynomial time."""
    p=tuple(Q(x) for x in probabilities)
    if any(x<0 or x>1 for x in p):raise ValueError('probabilities outside [0,1]')
    if any(mask>>len(p) for mask in certificate['masks']):raise ValueError('probability vector too short')
    total=Q(0)
    for failed in range(1<<len(p)):
        if all(survives_loss(mask,failed) for mask in certificate['masks']):
            total+=product_rational(p[i] if failed>>i&1 else 1-p[i] for i in range(len(p)))
    return total


def product_rational(values):
    result=Q(1)
    for v in values:result*=v
    return result


def color_domains(certificate,n,groups,losses=1):
    """Exact small-instance search. The first contact uses domain 0 by symmetry."""
    if n<1 or groups<1 or losses<0:raise ValueError('invalid coloring dimensions')
    if any(mask>>n for mask in certificate['masks']):raise ValueError('contact count too small')
    for rest in product(range(groups),repeat=n-1):
        colors=(0,)+rest
        if all(len({colors[i] for i in range(n) if mask>>i&1})>losses for mask in certificate['masks']):return colors
    return None


def protection_optimum(certificate,unit_costs,budget=Q(1),denominator=1000000):
    """Use SciPy only to propose a solution, then certify it with rational arithmetic.

    If recovered bounds do not coincide exactly, return a valid interval and
    verified_optimal=False. This routine never treats solver success as proof.
    """
    import numpy as np
    from scipy.optimize import linprog
    d=tuple(Q(x) for x in unit_costs);budget=Q(budget);n=len(d);masks=certificate['masks'];m=len(masks)
    if not n or any(x<=0 for x in d) or budget<0:raise ValueError('positive unit costs and nonnegative budget required')
    if any(mask>>n for mask in masks):raise ValueError('unit cost vector too short')
    matrix=np.array([[-int(mask>>i&1) for i in range(n)]+[1] for mask in masks]+[[float(x) for x in d]+[0]],dtype=float)
    rhs=np.array([0]*m+[float(budget)]);objective=np.array([0]*n+[-1.])
    hint=linprog(objective,A_ub=matrix,b_ub=rhs,bounds=[(0,None)]*n+[(None,None)],method='highs')
    if not hint.success:raise RuntimeError('LP hint solver did not return a solution')
    rational=lambda x:Q(float(x)).limit_denominator(denominator)
    c=[max(Q(0),rational(x)) for x in hint.x[:n]];used=sum(x*y for x,y in zip(c,d))
    if used>budget:c=[x*budget/used for x in c]
    lower=min(sum(c[i] for i in range(n) if mask>>i&1) for mask in masks)
    lam=[max(Q(0),rational(-x)) for x in hint.ineqlin.marginals[:m]]
    if not sum(lam):lam=[Q(1,m)]*m
    else:
        normalizer=sum(lam);lam=[x/normalizer for x in lam]
    mu=max(sum(lam[j] for j,mask in enumerate(masks) if mask>>i&1)/d[i] for i in range(n))
    upper=budget*mu
    assert sum(c[i]*d[i] for i in range(n))<=budget and sum(lam)==1
    assert lower<=upper
    return {'allocation':c,'lambda':lam,'mu':mu,'lower':lower,'upper':upper,
            'verified_optimal':lower==upper,'budget':budget,'unit_costs':d}


def verify_protection(certificate,result):
    c=result['allocation'];lam=result['lambda'];mu=result['mu'];d=result['unit_costs'];budget=result['budget'];masks=certificate['masks']
    if len(lam)!=len(masks) or any(x<0 for x in c+lam) or sum(lam)!=1:return False
    if sum(a*b for a,b in zip(c,d))>budget:return False
    if any(sum(lam[j] for j,m in enumerate(masks) if m>>i&1)>mu*d[i] for i in range(len(c))):return False
    value=min(sum(c[i] for i in range(len(c)) if m>>i&1) for m in masks)
    return value==budget*mu==result['lower']==result['upper']
