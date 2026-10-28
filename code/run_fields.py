from pathlib import Path
import json,time,hashlib
import csv
from statistics import median
def load_points(path):
    with path.open(newline="") as f:return [tuple(float(row[key]) for key in ["x","y"]) for row in csv.DictReader(f)]
from robust_coverage import disk_facets,dual_betti,threshold,domain_threshold,weighted_threshold

ROOT=Path(__file__).resolve().parent
INPUT=ROOT.parent/'data/fields'
OUTPUT=ROOT.parent/'results'
results=[]
for folder in sorted(INPUT.iterdir()):
    if not folder.is_dir():continue
    meta=json.loads((folder/'meta.json').read_text());p=load_points(folder/'sensors.csv');t=time.time()
    facets,stats=disk_facets(p,meta['R'])
    # Fixed geometric failure domains, independent of the topology calculation.
    domains=[int(x>median(row[0] for row in p))+2*int(y>median(row[1] for row in p)) for x,y in p]
    costs=[1+i%3 for i in range(len(p))]
    models={f'k{k}':threshold(k) for k in [1,2,3]}
    models['one_of_four_domains']=domain_threshold(domains,2)
    models['weighted_budget_3']=weighted_threshold(costs,3)
    out={'field':folder.name,'radius':meta['R'],'input_sha256':hashlib.sha256((folder/'sensors.csv').read_bytes()).hexdigest(),
         'facets':[hex(f) for f in facets],'geometry':stats,'models':{},'domains':domains,'costs':costs}
    for name,wins in models.items():
        out['models'][name]=dual_betti(facets,wins)
        print(folder.name,name,out['models'][name],flush=True)
    out['elapsed_seconds']=round(time.time()-t,3);results.append(out)
    (OUTPUT/'field-results.json').write_text(json.dumps(results,indent=2)+'\n')
print('Completed all fields.',flush=True)
