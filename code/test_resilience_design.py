import unittest,random
from fractions import Fraction as Q
from critical_radius import order_candidates,support_candidates,critical_radii,antichain_at_radius
from resilience_design import *
from target_certificate import target_antichain,covers
from robust_coverage import threshold,domain_threshold


def rectangle(a,b):
    return [[(-a,-b),(a,-b),(a,b)],[(-a,-b),(a,b),(-a,b)]]


class ResilienceControls(unittest.TestCase):
    def test_single_disk_critical_radius(self):
        t=rectangle(Q(1),Q(1));result=critical_radii([(0,0)],t,{'one':threshold(1)})
        self.assertEqual(result['rules']['one']['squared'],2)

    def test_two_domains_have_exact_distinct_thresholds(self):
        c=[(-1,-1),(-1,1),(1,-1),(1,1)];t=rectangle(Q(3,5),Q(3,5))
        result=critical_radii(c,t,{'two':threshold(2),'columns':domain_threshold([0,0,1,1],2),
                                  'diagonal':domain_threshold([0,1,1,0],2)})
        self.assertEqual(result['rules']['columns']['squared'],Q(89,25))
        self.assertEqual(result['rules']['diagonal']['squared'],Q(68,25))
        self.assertEqual(result['rules']['two']['squared'],Q(68,25))

    def test_radius_threshold_against_independent_sweep(self):
        c=[(-1,-1),(-1,1),(1,-1),(1,1)];t=rectangle(Q(3,5),Q(3,5))
        for radius in [Q(3,2),Q(7,4),Q(9,5),Q(19,10),Q(2)]:
            cert=target_antichain(c,radius,t)
            self.assertEqual(covers(cert,threshold(2))['covered'],radius*radius>=Q(68,25))
            self.assertEqual(covers(cert,domain_threshold([0,0,1,1],2))['covered'],radius*radius>=Q(89,25))
            self.assertEqual(set(cert['masks']),set(antichain_at_radius(support_candidates(c,t),radius)['masks']))

    def test_all_monotone_rules_on_four_contacts(self):
        sites=[(-2,0),(1,0),(0,2),(1,-2)];target=rectangle(Q(3,2),Q(3,4));rules={}
        for selection in range(1,1<<15):
            minimal=[i+1 for i in range(15) if selection>>i&1]
            if any(a&b in [a,b] for j,a in enumerate(minimal) for b in minimal[j+1:]):continue
            rules[str(len(rules))]=lambda s,ms=tuple(minimal):any(a&s==a for a in ms)
        self.assertEqual(len(rules),166)
        reduced=critical_radii(sites,target,rules)
        full=critical_radii(sites,target,rules,master=order_candidates(sites,target))
        self.assertEqual({k:v['squared'] for k,v in reduced['rules'].items()},
                         {k:v['squared'] for k,v in full['rules'].items()})

    def test_random_five_contact_support_controls(self):
        rng=random.Random(15750);target=rectangle(Q(1),Q(1))
        for _ in range(10):
            sites=[(Q(rng.randrange(-5,6),3),Q(rng.randrange(-5,6),3)) for _ in range(5)]
            rules={}
            for j in range(25):
                coalitions=tuple(rng.randrange(1,32) for _ in range(5))
                rules[str(j)]=lambda s,c=coalitions:any(a&s==a for a in c)
            small=critical_radii(sites,target,rules)
            full=critical_radii(sites,target,rules,master=order_candidates(sites,target))
            self.assertEqual({k:v['squared'] for k,v in small['rules'].items()},
                             {k:v['squared'] for k,v in full['rules'].items()})
            for radius in [Q(3,2),Q(2)]:
                sweep=target_antichain(sites,radius,target)
                master=antichain_at_radius(small['master'],radius)
                self.assertEqual(set(sweep['masks']),set(master['masks']))

    def test_bundle_truth_table(self):
        f=bundle_activation([(0,1),None,(2,)])
        self.assertEqual(f(7),5);self.assertEqual(f(1),0);self.assertEqual(f(4),4)

    def test_coloring_and_reliability_on_odd_cycle(self):
        cert={'masks':(3,5,6),'witnesses':{3:(0,0),5:(0,1),6:(1,0)}}
        self.assertIsNone(color_domains(cert,3,2));self.assertIsNotNone(color_domains(cert,3,3))
        for p in [Q(0),Q(1,10),Q(1,2),Q(1)]:self.assertEqual(reliability(cert,[p]*3),1-3*p*p+2*p**3)

    def test_rational_protection_certificate(self):
        try:import scipy
        except ImportError:self.skipTest('SciPy proposes LP candidates; exact verification is standard-library only')
        cert={'masks':(3,5,6),'witnesses':{3:(0,0),5:(0,1),6:(1,0)}}
        result=protection_optimum(cert,[1,1,1])
        self.assertEqual(result['lower'],Q(2,3));self.assertTrue(verify_protection(cert,result))

    def test_known_certificate_without_lp_solver(self):
        cert={'masks':(3,5,6),'witnesses':{3:(0,0),5:(0,1),6:(1,0)}}
        result={'allocation':[Q(1,3)]*3,'lambda':[Q(1,3)]*3,'mu':Q(2,3),'unit_costs':[Q(1)]*3,
                'budget':Q(1),'lower':Q(2,3),'upper':Q(2,3)}
        self.assertTrue(verify_protection(cert,result))
        self.assertFalse(verify_protection(cert,dict(result,allocation=[Q(1),Q(0),Q(0)])))


if __name__=='__main__':unittest.main(verbosity=2)
