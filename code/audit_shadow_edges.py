"""Recount the v2 shadow vertices and edges without an unfinished 2-skeleton."""
from pathlib import Path
from itertools import combinations
import json,time
ROOT=Path(__file__).resolve().parent.parent
out=[]
for entry in json.loads((ROOT/'results/field-results.json').read_text()):
    start=time.time();facets=[int(f,16) for f in entry['facets']];n=entry['geometry']['sensors']
    vertices=[(1<<i)|(1<<j) for i,j in combinations(range(n),2) if any(f>>i&1 and f>>j&1 for f in facets)]
    edges=0
    for a,b in combinations(vertices,2):
        union=a|b
        edges+=any(union&f==union for f in facets)
    row={'field':entry['field'],'shadow_k2_vertices':len(vertices),'shadow_k2_edges':edges,'seconds':round(time.time()-start,3)}
    print(json.dumps(row),flush=True);out.append(row)
    (ROOT/'results/shadow-edge-audit.json').write_text(json.dumps(out,indent=2)+'\n')
