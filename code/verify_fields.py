"""Independent exact enclosing-circle and GF(2) controls.

Every disk pair and triple is compared with the stored facet face oracle.
All facets and every one-contact extension are checked by the same independent
equal-radius circle criterion. Ranks use lowest-pivot set elimination.
"""
from pathlib import Path
import json,time,hashlib
from fractions import Fraction as Q
from itertools import combinations
import csv
from statistics import median
def load_points(path):
    with path.open(newline="") as f:return [tuple(float(row[key]) for key in ["x","y"]) for row in csv.DictReader(f)]
from test_robust_coverage import mec_squared,small_rank
from robust_coverage import threshold

ROOT=Path(__file__).resolve().parent
DATA=ROOT.parent/'data/fields'
OUTPUT=ROOT.parent/'results'
results=json.loads((OUTPUT/'field-results.json').read_text());out=[]
for entry in results:
    start=time.time();folder=DATA/entry['field'];p=load_points(folder/'sensors.csv')
    pts=[tuple(Q(float(x)) for x in row) for row in p];r2=Q(entry['radius'])**2
    facets=[int(x,16) for x in entry['facets']];counts={};tangencies=0;checked=0;positive_masks=set()
    for size in [2,3]:
        positive=0
        for subset in combinations(range(len(p)),size):
            mask=sum(1<<i for i in subset);radius=mec_squared([pts[i] for i in subset])
            oracle=radius<=r2;by_facets=any(mask&f==mask for f in facets)
            assert oracle==by_facets,(entry['field'],subset)
            if oracle:positive_masks.add(mask)
            positive+=oracle;tangencies+=radius==r2;checked+=1
        counts[str(size)]=positive
    # Facet and maximality controls need only triples by planar Helly.
    for f in facets:
        inside=[i for i in range(len(p)) if f>>i&1]
        assert all(sum(1<<i for i in s) in positive_masks for s in combinations(inside,min(3,len(inside)))) if len(inside)>1 else True
        for j in range(len(p)):
            if f>>j&1:continue
            assert any((1<<j)|sum(1<<i for i in s) not in positive_masks for s in combinations(inside,min(2,len(inside))))
    v=[f for f in facets if f.bit_count()>=2];edges={};columns=[]
    for i,j in combinations(range(len(v)),2):
        if (v[i]&v[j]).bit_count()>=2:edges[i,j]=len(edges)
    for i,j,k in combinations(range(len(v)),3):
        if (i,j) in edges and (i,k) in edges and (j,k) in edges and (v[i]&v[j]&v[k]).bit_count()>=2:
            columns.append((1<<edges[i,j])^(1<<edges[i,k])^(1<<edges[j,k]))
    rank=small_rank(columns);assert rank==entry['models']['k2']['rank_d2']
    item={'field':entry['field'],'pairs_and_triples_checked':checked,'nerve_faces':counts,
          'exact_tangencies':tangencies,'all_facets_and_extensions_checked':True,
          'independent_k2_rank_d2':rank,'seconds':round(time.time()-start,3)}
    out.append(item);(OUTPUT/'independent-verification.json').write_text(json.dumps(out,indent=2)+'\n')
    print(json.dumps(item),flush=True)
