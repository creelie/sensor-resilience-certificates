"""Controls independent of the five reported field outputs."""
import unittest,random
from itertools import combinations
from fractions import Fraction as Q
from robust_coverage import *


def small_rank(columns):
    """Set-based elimination using the smallest, rather than largest, pivot."""
    pivots={}
    for value in columns:
        c={i for i in range(value.bit_length()) if value>>i&1}
        while c:
            low=min(c)
            if low in pivots:c.symmetric_difference_update(pivots[low])
            else:pivots[low]=set(c);break
    return len(pivots)


def mec_squared(points):
    if len(points)==1:return Q(0)
    if len(points)>3:return max(mec_squared(s) for s in combinations(points,3))
    def d2(a,b):return sum((x-y)**2 for x,y in zip(a,b))
    if len(points)==2:return d2(*points)/4
    a,b,c=points;l=[d2(a,b),d2(a,c),d2(b,c)]
    if 2*max(l)>=sum(l):return max(l)/4
    cross=(b[0]-a[0])*(c[1]-a[1])-(b[1]-a[1])*(c[0]-a[0])
    return l[0]*l[1]*l[2]/(4*cross**2)


class ExactControls(unittest.TestCase):
    def test_radical_square_comparisons(self):
        for a in range(-6,7):
            for b in range(-6,7):
                for root in [Q(0),Q(1,2),Q(2),Q(7,3)]:
                    self.assertEqual(radical_nonpositive(Q(a),Q(b),root*root),a+b*root<=0)
        self.assertTrue(radical_nonpositive(Q(-2),Q(1),Q(2)))
        self.assertFalse(radical_nonpositive(Q(-1),Q(1),Q(2)))
        self.assertTrue(radical_nonpositive(Q(1),Q(-1),Q(2)))
        with self.assertRaises(ValueError):radical_nonpositive(Q(0),Q(0),Q(-1))

    def test_tangencies_nested_and_zero_disks(self):
        self.assertEqual(disk_facets([(0,0),(2,0)],1)[0],(3,))
        self.assertEqual(disk_facets([(0,0),(2.0000000000000004,0)],1)[0],(1,2))
        self.assertEqual(disk_facets([(0,0),(0,0),(0,0)],[0,1,2])[0],(7,))
        self.assertEqual(disk_facets([(0,0),(0,0),(5,0)],[1,2,0])[0],(3,4))
        self.assertEqual(disk_facets([(0,0),(3,0),(0,4)],2.5)[0],(7,))

    def test_scale_invariance(self):
        p=[(0,0),(1.5,0),(.5,1),(4,0)]
        expected=disk_facets(p,1)[0]
        for exponent in [-450,450]:
            scale=2.0**exponent
            self.assertEqual(disk_facets([(x*scale,y*scale) for x,y in p],scale)[0],expected)

    def test_equal_disk_exhaustive_subset_oracle(self):
        rng=random.Random(220964)
        for trial in range(50):
            n=7;p=[(rng.randrange(-10,11)/4,rng.randrange(-10,11)/4) for _ in range(n)]
            r=Q(rng.randrange(1,9),4);exact=[tuple(Q(x) for x in row) for row in p]
            expected=maximal_masks(s for s in range(1,1<<n)
                if mec_squared([exact[i] for i in range(n) if s>>i&1])<=r*r)
            self.assertEqual(disk_facets(p,float(r))[0],expected)

    def test_rank_independent_controls(self):
        rng=random.Random(1787932)
        for n in range(1,25):
            columns=[rng.getrandbits(n) for _ in range(2*n)]
            self.assertEqual(gf2_rank(columns),small_rank(columns))

    def test_dual_against_independent_coalition_models(self):
        rng=random.Random(23731783)
        for trial in range(150):
            n=rng.randrange(2,8);facets=maximal_masks([rng.randrange(1,1<<n) for _ in range(9)])
            models=[threshold(rng.randrange(1,n+2)),
                    domain_threshold([rng.randrange(3) for _ in range(n)],rng.randrange(1,4)),
                    weighted_threshold([rng.randrange(4) for _ in range(n)],rng.randrange(7))]
            # A completely arbitrary downward failure family, via its maximal masks.
            failures=maximal_masks([rng.randrange(1<<n) for _ in range(4)])
            models.append(lambda s:bool(s) and not any(s&f==s for f in failures))
            for wins in models:
                b=dual_betti(facets,wins)
                self.assertEqual((b['b0'],b['b1']),shadow_betti_small(facets,n,wins))

    def test_correlated_failure_counterexample(self):
        self.assertTrue(threshold(2)(3))
        self.assertFalse(domain_threshold(['same','same'],2)(3))

    def test_reject_silent_cost_truncation(self):
        for costs,budget in [([1.5,2],2),([1,-1],2),([1,2],2.5),([1,2],-1)]:
            with self.assertRaises(ValueError):weighted_threshold(costs,budget)
        with self.assertRaises(ValueError):weighted_threshold([1,2],1)(4)
        with self.assertRaises(ValueError):domain_threshold([0,1])(4)

    def test_geometry_validation(self):
        for p,r in [([],1),([(0,0)],-1),([(float('nan'),0)],1),([(0,0)],[1,2]),([(0,0,0)],1)]:
            with self.assertRaises(ValueError):disk_facets(p,r)

    def test_continuous_triangle_certificate(self):
        triangle=[(0,0),(2,0),(1,1.5)]
        self.assertTrue(triangle_certificate(triangle,1.16,triangle,threshold(1))['certified'])
        self.assertFalse(triangle_certificate(triangle,1,triangle,threshold(1))['certified'])
        self.assertTrue(triangle_certificate([(0,0)],0,[(0,0)]*3,threshold(1))['certified'])
        # Two contacts at each site can share a single failure domain.
        centres=[p for p in triangle for _ in range(2)]
        self.assertTrue(triangle_certificate(centres,1.16,triangle,threshold(2))['certified'])
        self.assertFalse(triangle_certificate(centres,1.16,triangle,domain_threshold([0]*6,2))['certified'])


if __name__=='__main__':unittest.main(verbosity=2)
