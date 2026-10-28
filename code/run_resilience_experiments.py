from pathlib import Path
from fractions import Fraction as Q
import json,time,hashlib
from target_certificate import target_antichain,map_certificate,deletion_cost
from resilience_design import protection_optimum,verify_protection,color_domains,reliability,bundle_activation,domain_activation
from critical_radius import critical_radii
from robust_coverage import threshold,domain_threshold

ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'results/resilience';OUT.mkdir(exist_ok=True)
def rectangle(a,b):return [[(-a,-b),(a,-b),(a,b)],[(-a,-b),(a,b),(-a,b)]]
def patch(x,y,h=Q(1,20)):return [(x-h,y-h),(x+h,y-h),(x,y+h)]
corners=[(-1,-1),(-1,1),(1,-1),(1,1)];panel=rectangle(Q(3,5),Q(3,5))
grid=[(x,y) for x in [-1,0,1] for y in [-1,0,1]]
cases=[{'name':'three_asset_cycle','centres':[(-1,0),(1,0),(0,Q(3,2))],'radius':Q(6,5),
        'target':[patch(0,0),patch(Q(-1,2),Q(3,4)),patch(Q(1,2),Q(3,4))]},
       {'name':'four_corner_panel','centres':corners,'radius':Q(9,5),'target':panel},
       {'name':'nine_contact_panel','centres':grid,'radius':Q(11,10),'target':rectangle(Q(4,5),Q(4,5))},
       {'name':'weak_nine_contact_panel','centres':grid,'radius':Q(4,5),'target':rectangle(Q(4,5),Q(4,5))},
       {'name':'five_contact_panel','centres':corners+[(0,0)],'radius':Q(9,5),'target':panel},
       {'name':'duplicated_panel','centres':[p for p in corners for _ in range(2)],'radius':Q(9,5),'target':panel}]
def encode(obj):
    if isinstance(obj,Q):return str(obj)
    if isinstance(obj,dict):return {str(k):encode(v) for k,v in obj.items()}
    if isinstance(obj,(list,tuple)):return [encode(v) for v in obj]
    return obj
results=[]
for case in cases:
    start=time.time();c=case['centres'];n=len(c);cert=target_antichain(c,case['radius'],case['target'])
    uniform=deletion_cost(cert,[1]*n);opt=protection_optimum(cert,[1]*n);assert verify_protection(cert,opt)
    colors=None;groups=None
    if uniform['cost']>=2:
        for groups in [2,3]:
            colors=color_domains(cert,n,groups)
            if colors is not None:break
    rules={'one_contact':threshold(1),'two_contacts':threshold(2),'three_contacts':threshold(3)}
    radii=critical_radii(c,case['target'],rules)
    row=dict(case,certificate=cert,minimum_individual_deletions=uniform,protection=opt,
             minimum_domains_for_one_domain_loss=groups if colors is not None else None,domain_assignment=colors,
             independent_contact_reliability_at_p_0_1=reliability(cert,[Q(1,10)]*n),
             critical_radii={k:v for k,v in radii.items() if k!='master'},seconds=round(time.time()-start,3))
    results.append(row);(OUT/'engineering-results.json').write_text(json.dumps(encode(results),indent=2)+'\n')
    print(case['name'],'patterns',len(cert['masks']),'cuts',cert['x_events'],'deletions',uniform['cost'],
          'LP',opt['lower'],'domains',row['minimum_domains_for_one_domain_loss'],'seconds',row['seconds'],flush=True)

base=results[1]['certificate'];wiring={}
for name,colors in [('columns',[0,0,1,1]),('diagonal',[0,1,1,0])]:
    mapped=map_certificate(base,domain_activation(colors))
    radius=critical_radii(corners,panel,{'survive_one_domain':domain_threshold(colors,2)})
    wiring[name]={'colors':colors,'domain_certificate':mapped,'minimum_domain_deletions':deletion_cost(mapped,[1,1]),
                  'reliability_at_p_0_1':reliability(mapped,[Q(1,10)]*2),
                  'critical_radius_squared':radius['rules']['survive_one_domain']['squared'],
                  'worst_point':radius['rules']['survive_one_domain']['witness']}
(OUT/'wiring-results.json').write_text(json.dumps(encode(wiring),indent=2)+'\n')
uncertain=[]
for error in [Q(0),Q(1,10),Q(1,5),Q(3,10)]:
    cert=target_antichain(corners,Q(9,5)-error,panel)
    uncertain.append({'type':'independent_displacement_balls','error':error,'certificate':cert,
                      'minimum_deletions':deletion_cost(cert,[1]*4)})
primitive=[];bundles=[]
for x,y in corners:
    ids=[]
    for dx in [Q(-1,10),Q(1,10)]:
        for dy in [Q(-1,10),Q(1,10)]:ids.append(len(primitive));primitive.append((x+dx,y+dy))
    bundles.append(ids)
activation=bundle_activation(bundles);start=time.time()
cert=target_antichain(primitive,Q(9,5),panel,activation)
radius=critical_radii(primitive,panel,{'two_contacts':threshold(2)},activation=activation)
uncertain.append({'type':'independent_displacement_boxes','halfwidth':Q(1,10),'primitive_centres':primitive,'bundles':bundles,
                  'certificate':cert,'minimum_deletions':deletion_cost(cert,[1]*4),
                  'critical_radius_squared':radius['rules']['two_contacts']['squared'],
                  'critical_radius_witness':radius['rules']['two_contacts']['witness'],
                  'radius_candidate_count':radius['candidate_count'],'seconds':round(time.time()-start,3)})
(OUT/'uncertainty-results.json').write_text(json.dumps(encode(uncertain),indent=2)+'\n')
print('Wiring and product uncertainty computations completed.',flush=True)
