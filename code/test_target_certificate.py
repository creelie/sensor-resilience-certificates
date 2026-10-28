import unittest,random
from decimal import Decimal,localcontext
from fractions import Fraction as Q
from target_certificate import *
from robust_coverage import threshold,domain_threshold

SQUARE=[[(Q(-1),Q(-1)),(Q(1),Q(-1)),(Q(1),Q(1))],
        [(Q(-1),Q(-1)),(Q(1),Q(1)),(Q(-1),Q(1))]]


class TargetControls(unittest.TestCase):
    def test_quadratic_comparison(self):
        self.assertEqual(Quadratic(0,1,8).compare(Quadratic(0,2,2)),0)
        self.assertEqual(Quadratic(3,-1,4).compare(Quadratic(1)),0)
        rng=random.Random(20261028)
        with localcontext() as ctx:
            ctx.prec=100
            for _ in range(400):
                a,b,c,d=[rng.randrange(-7,8) for _ in range(4)];h,k=[rng.randrange(1,12) for _ in range(2)]
                val=Decimal(a-c)+Decimal(b)*Decimal(h).sqrt()-Decimal(d)*Decimal(k).sqrt()
                got=Quadratic(a,b,h).compare(Quadratic(c,d,k))
                if abs(val)>Decimal('1e-80'):self.assertEqual(got,(val>0)-(val<0))

    def test_strict_rational_separation(self):
        pairs=[(Quadratic(0,1,2),Quadratic(Q(1,2**180),1,2)),
               (Quadratic(0,-1,2),Quadratic(-1)),(Quadratic(1),Quadratic(2))]
        for a,b in pairs:
            q=rational_between(a,b)
            self.assertLess(a.compare(q),0);self.assertLess(Quadratic(q).compare(b),0)

    def test_empty_and_single_disk(self):
        empty=target_antichain([],[],SQUARE);self.assertEqual(empty['masks'],(0,))
        cover=target_antichain([(0,0)],2,SQUARE);self.assertEqual(cover['masks'],(1,))
        missing=target_antichain([(0,0)],Q(1,2),SQUARE);self.assertEqual(missing['masks'],(0,))
        self.assertFalse(covers(missing,threshold(1))['covered'])

    def test_boundary_tangency_is_closed(self):
        tri=[[(0,0),(2,0),(0,2)]]
        # A disk centered at (1,1) of squared radius 2 touches the vertices;
        # use rational circle radius 1 and a tangent rational right triangle.
        tri=[[(0,0),(Q(3,5),Q(4,5)),(Q(3,5),Q(-4,5))]]
        cert=target_antichain([(0,0)],1,tri)
        self.assertTrue(covers(cert,threshold(1))['covered'])

    def test_realized_minimal_patterns(self):
        centres=[(-1,0),(1,0),(0,0)];radii=[Q(3,2)]*3
        cert=target_antichain(centres,radii,SQUARE)
        for mask,point in cert['witnesses'].items():
            actual=sum(1<<i for i,p in enumerate(centres) if dot(sub(point,p),sub(point,p))<=radii[i]**2)
            self.assertEqual(mask,actual)
        for i,a in enumerate(cert['masks']):
            self.assertFalse(any(a&b==b for b in cert['masks'][i+1:]))
        rng=random.Random(217283)
        for _ in range(200):
            p=(Q(rng.randrange(-100,101),100),Q(rng.randrange(-100,101),100))
            mask=sum(1<<i for i,c in enumerate(centres) if dot(sub(p,c),sub(p,c))<=radii[i]**2)
            self.assertTrue(any(a&mask==a for a in cert['masks']))

    def test_deletion_update_matches_recomputation(self):
        c=[(-1,0),(1,0),(0,0)];r=[Q(3,2)]*3
        cert=target_antichain(c,r,SQUARE)
        mapped=map_certificate(cert,lambda m:m&5)
        recompute=target_antichain([c[0],c[2]],[r[0],r[2]],SQUARE)
        restore=lambda m:(m&1)|((m&2)<<1)
        self.assertEqual(set(mapped['masks']),{restore(m) for m in recompute['masks']})

    def test_rational_erosion_is_not_rounded(self):
        radius=Q(1)-Q(1,2**80)
        cert=target_antichain([(0,0)],[radius],[[(0,0),(1,0),(0,1)]])
        self.assertFalse(covers(cert,threshold(1))['covered'])

    def test_witness_deletion_cost(self):
        cert=target_antichain([(-1,0),(1,0),(0,0)],[Q(3,2)]*3,SQUARE)
        result=deletion_cost(cert,[Q(1),Q(2),Q(4)])
        self.assertEqual(result['cost'],min(sum([1,2,4][i] for i in range(3) if m>>i&1) for m in cert['masks']))

    def test_degenerate_target_rejected(self):
        with self.assertRaises(ValueError):target_antichain([],[],[[(0,0),(1,0),(2,0)]])


if __name__=='__main__':unittest.main(verbosity=2)
