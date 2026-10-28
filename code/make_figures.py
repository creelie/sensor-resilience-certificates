"""Publication figures; raster panels illustrate, never certify, topology."""
from pathlib import Path
import json,csv
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
from matplotlib.patches import Circle

ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'paper/figures';OUT.mkdir(exist_ok=True)
rows=json.loads((ROOT/'results/field-results.json').read_text())
shadow=json.loads((ROOT/'results/shadow-edge-audit.json').read_text())
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.spines.top':False,'axes.spines.right':False,
                     'pdf.fonttype':42,'axes.titleweight':'semibold','axes.labelcolor':'#26364b'})
palette=['#236c97','#d89436','#4b8a73','#9d5b83']
def load(entry):
    p=np.loadtxt(ROOT/'data/fields'/entry['field']/'sensors.csv',delimiter=',',skiprows=1)
    return p,entry['radius']
def grid_masks(p,r,domains,costs):
    margin=r+.2;lo=p.min(axis=0)-margin;hi=p.max(axis=0)+margin
    x=np.linspace(lo[0],hi[0],500);y=np.linspace(lo[1],hi[1],500);xx,yy=np.meshgrid(x,y)
    count=np.zeros(xx.shape,dtype=np.int16);weighted=count.copy();groups=np.zeros(xx.shape,dtype=np.uint8)
    for i,(px,py) in enumerate(p):
        active=(xx-px)**2+(yy-py)**2<=r*r
        count+=active;weighted+=active*costs[i];groups|=active.astype(np.uint8)*(1<<domains[i])
    domains_count=sum(((groups>>i)&1) for i in range(4))
    return [count>=2,domains_count>=2,weighted>3],(lo[0],hi[0],lo[1],hi[1])
def panel(ax,entry,model=0):
    p,r=load(entry);images,extent=grid_masks(p,r,entry['domains'],entry['costs'])
    ax.imshow(images[model],origin='lower',extent=extent,cmap=ListedColormap(['#ffffff','#78b6c9']),interpolation='nearest',zorder=0)
    for x,y in p:ax.add_patch(Circle((x,y),r,fill=False,edgecolor='#50697a',linewidth=.25,alpha=.35))
    ax.scatter(p[:,0],p[:,1],s=5,c=[palette[d] for d in entry['domains']],edgecolors='none',zorder=2)
    ax.set_aspect('equal');ax.set_xticks([]);ax.set_yticks([])
    ax.set_xlim(extent[:2]);ax.set_ylim(extent[2:])
fig,axes=plt.subplots(2,3,figsize=(7.3,5.25),constrained_layout=True)
for ax,entry in zip(axes.flat,rows):
    panel(ax,entry);b=entry['models']['k2'];ax.set_title(f"Field {entry['field'][0]}   ($b_0,b_1$)=({b['b0']},{b['b1']})",fontsize=9)
axes.flat[-1].axis('off');axes.flat[-1].text(0,.85,'Two-fold coverage',fontsize=13,color='#173b56',weight='bold')
axes.flat[-1].text(0,.67,'Shading: sampled illustration\nCircles: sensor footprints\nColors: four fault domains\n\nBetti numbers: exact dual model\nNo raster used in the calculation',fontsize=9,linespacing=1.65,va='top')
fig.savefig(OUT/'five-fields.pdf',bbox_inches='tight');plt.close(fig)
fig,axes=plt.subplots(1,2,figsize=(7.3,3.35),constrained_layout=True)
for ax,key,label in [(axes[0],'vertices','Vertices'),(axes[1],'edges','Edges')]:
    x=np.arange(5);old=[s['shadow_k2_'+key] for s in shadow];new=[e['models']['k2'][key] for e in rows]
    ax.bar(x-.18,old,.36,color='#9daaba',label='Coalition shadow');ax.bar(x+.18,new,.36,color='#206f91',label='Facet dual')
    ax.set_yscale('log');ax.set_xticks(x,labels=[e['field'][0] for e in rows]);ax.set_xlabel('Field');ax.set_title(label)
    ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
    for i,(a,b) in enumerate(zip(old,new)):
        if i==4:ax.annotate(f'{a:,}',(i-.18,a),xytext=(0,4),textcoords='offset points',ha='center',fontsize=8)
axes[0].legend(frameon=False,fontsize=8,loc='upper left');fig.savefig(OUT/'compression.pdf',bbox_inches='tight');plt.close(fig)
entry=rows[-1];fig,axes=plt.subplots(1,3,figsize=(7.3,3.1),constrained_layout=True)
for i,(key,label) in enumerate([('k2','Two contacts'),('one_of_four_domains','Two domains'),('weighted_budget_3','Cost exceeds 3')]):
    panel(axes[i],entry,i);b=entry['models'][key];axes[i].set_title(label+f"\n($b_0,b_1$)=({b['b0']},{b['b1']})",fontsize=9)
fig.savefig(OUT/'structured-field-E.pdf',bbox_inches='tight');plt.close(fig)

table=['\\begin{longtable}{llrrrrrr}','\\caption{Complete dual two-skeleton counts and Betti numbers. The domain model survives every loss of one of the four stated domains.}\\label{tab:all-results}\\\\',
       '\\toprule Field & Rule & $V$ & $E$ & $T$ & $\\rank\\partial_2$ & $b_0$ & $b_1$ \\\\ \\midrule\\endfirsthead',
       '\\toprule Field & Rule & $V$ & $E$ & $T$ & $\\rank\\partial_2$ & $b_0$ & $b_1$ \\\\ \\midrule\\endhead',
       '\\bottomrule\\endfoot']
for entry in rows:
    for key,label in [('k1','$k=1$'),('k2','$k=2$'),('k3','$k=3$'),('one_of_four_domains','Domains'),('weighted_budget_3','Budget')]:
        b=entry['models'][key];nums=[b[k] for k in ['vertices','edges','triangles','rank_d2','b0','b1']]
        table.append(entry['field'][0]+' & '+label+' & '+' & '.join(str(n) for n in nums)+r' \\')
    table.append('\\addlinespace')
table.append('\\end{longtable}')
(ROOT/'paper/result-table.tex').write_text('\n'.join(table)+'\n')
print('Created three vector-PDF figures and generated result table.')
