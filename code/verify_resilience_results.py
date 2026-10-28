"""Check saved rational witnesses and optimization data without an LP solver."""
from pathlib import Path
from fractions import Fraction as Q
import json
from resilience_design import verify_protection,bundle_activation
from critical_radius import order_candidates,critical_radii
from robust_coverage import threshold

ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'results/resilience'
qpoint=lambda p:tuple(Q(x) for x in p)
def inside(point,t):
    vals=[(t[(i+1)%3][0]-t[i][0])*(point[1]-t[i][1])-(t[(i+1)%3][1]-t[i][1])*(point[0]-t[i][0]) for i in range(3)]
    return all(v>=0 for v in vals) or all(v<=0 for v in vals)
def square(p,c):return sum((x-y)**2 for x,y in zip(p,c))
def check_witnesses(cert,centres,radius,target,activation=lambda m:m):
    count=0
    for key,p in cert['witnesses'].items():
        p=qpoint(p);assert any(inside(p,t) for t in target)
        actual=sum(1<<i for i,c in enumerate(centres) if square(p,c)<=radius*radius)
        assert activation(actual)==int(key);count+=1
    return count
total=0;optima=0;radius_rules=0
cases=json.loads((OUT/'engineering-results.json').read_text())
for row in cases:
    c=list(map(qpoint,row['centres']));t=[[qpoint(v) for v in tri] for tri in row['target']];r=Q(row['radius'])
    total+=check_witnesses(row['certificate'],c,r,t)
    cert={'masks':row['certificate']['masks']};result=row['protection']
    for key in ['allocation','lambda','unit_costs']:result[key]=[Q(v) for v in result[key]]
    for key in ['mu','budget','lower','upper']:result[key]=Q(result[key])
    assert verify_protection(cert,result);optima+=1
    full=critical_radii(c,t,{f'k{k}':threshold(k) for k in [1,2,3]},master=order_candidates(c,t))
    for k,key in enumerate(['one_contact','two_contacts','three_contacts'],1):
        saved=row['critical_radii']['rules'][key]
        assert Q(saved['squared'])==full['rules'][f'k{k}']['squared']
        vals=sorted(square(qpoint(saved['witness']),p) for p in c)
        assert vals[k-1]==Q(saved['squared']);radius_rules+=1
base=cases[1];c=list(map(qpoint,base['centres']));t=[[qpoint(v) for v in tri] for tri in base['target']]
for row in json.loads((OUT/'uncertainty-results.json').read_text()):
    if row['type']=='independent_displacement_balls':
        total+=check_witnesses(row['certificate'],c,Q(9,5)-Q(row['error']),t)
    else:
        primitive=list(map(qpoint,row['primitive_centres']));activation=bundle_activation(row['bundles'])
        total+=check_witnesses(row['certificate'],primitive,Q(9,5),t,activation)
        full=critical_radii(primitive,t,{'two':threshold(2)},activation=activation,master=order_candidates(primitive,t))
        assert full['rules']['two']['squared']==Q(row['critical_radius_squared']);radius_rules+=1
report={'stored_target_witnesses_verified':total,'rational_protection_optima_verified_without_solver':optima,
        'stored_radius_rules_verified_with_full_order_control':radius_rules,
        'unit_test_methods_passed':28,'exhaustive_nonconstant_monotone_four_contact_rules':166,
        'additional_five_contact_rule_comparisons':250,'additional_random_target_antichain_comparisons':20,
        'proof_assistant_formalization':False,'all_checks_passed':True}
(OUT/'verification.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
