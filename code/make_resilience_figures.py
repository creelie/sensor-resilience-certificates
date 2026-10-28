"""Vector illustrations generated from exact saved resilience results."""
from pathlib import Path
from fractions import Fraction as Q
import json,sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import Circle,Polygon
from matplotlib.colors import ListedColormap
from critical_radius import order_candidates,support_candidates
from target_certificate import _validated,_edges,critical_x

ROOT=Path(__file__).resolve().parent.parent;OUT=ROOT/'standalone/figures';OUT.mkdir(exist_ok=True)
cases=json.loads((ROOT/'results/resilience/engineering-results.json').read_text());wiring=json.loads((ROOT/'results/resilience/wiring-results.json').read_text())
uncertain=json.loads((ROOT/'results/resilience/uncertainty-results.json').read_text())
f=lambda x:float(Q(x));blue='#246c91';teal='#4a987b';red='#c3544e';gold='#d8a13c';gray='#8e9dab'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'axes.titlesize':10,'axes.titleweight':'bold',
 'axes.spines.top':False,'axes.spines.right':False,'pdf.fonttype':42,'savefig.bbox':'tight'})
def save(fig,name):fig.savefig(OUT/(name+'.pdf'));plt.close(fig)
def geom(ax,case,colors=None,radius=None):
    c=np.array([[f(v) for v in p] for p in case['centres']]);r=f(case['radius']) if radius is None else radius
    for t in case['target']:ax.add_patch(Polygon([[f(v) for v in p] for p in t],facecolor='#dde7eb',edgecolor='#173c50',linewidth=.8,alpha=.45))
    for i,p in enumerate(c):
        col=blue if colors is None else [blue,gold,teal,red][colors[i]%4]
        ax.add_patch(Circle(p,r,fill=False,edgecolor=col,linewidth=.7,alpha=.65));ax.scatter(*p,color=col,s=24,zorder=4)
        ax.annotate(str(i+1),p,xytext=(5,5),textcoords='offset points',fontsize=8)
    ax.set_aspect('equal');ax.set_xlabel('$x$');ax.set_ylabel('$y$');ax.grid(alpha=.1)
    ax.autoscale_view();return c
def witnesses(ax,case):
    for j,(mask,p) in enumerate(case['certificate']['witnesses'].items()):
        x,y=map(f,p);ax.plot(x,y,'x',color=red,ms=6);ax.annotate('$A_{'+str(j+1)+'}$',(x,y),xytext=(4,-9),textcoords='offset points',fontsize=8,color=red)
def graph(ax,case):
    c=np.array([[f(v) for v in p] for p in case['centres']]);ax.axis('off');ax.set_aspect('equal')
    for mask in case['certificate']['masks']:
        ids=[i for i in range(len(c)) if int(mask)>>i&1]
        if len(ids)==2:ax.plot(c[ids,0],c[ids,1],color=blue,lw=2)
    ax.scatter(c[:,0],c[:,1],s=420,color='#dceaf0',edgecolor=blue,zorder=3)
    for i,p in enumerate(c):ax.text(*p,str(i+1),ha='center',va='center',weight='bold',zorder=4)
    ax.margins(.35)

fig,ax=plt.subplots(1,2,figsize=(7.2,3.6),constrained_layout=True);geom(ax[0],cases[1]);witnesses(ax[0],cases[1]);ax[0].set_title('Target and exact weak-point witnesses');graph(ax[1],cases[1]);ax[1].set_title('Four minimal contact patterns');save(fig,'target-patterns')
fig,ax=plt.subplots(figsize=(6.8,4),constrained_layout=True);case=cases[1];geom(ax,case);witnesses(ax,case)
c,r,t=_validated(case['centres'],Q(case['radius']),[[[Q(v) for v in p] for p in tri] for tri in case['target']])
for q in critical_x(c,r,_edges(t)):
    val=f(q.a)+f(q.b)*np.sqrt(f(q.h))
    if -.61<=val<=.61:ax.axvline(val,color=gold,alpha=.8,linestyle='--',lw=.65)
ax.set_xlim(-1,1);ax.set_ylim(-.85,.85);ax.set_title('Exact critical abscissae define rational sample slabs');save(fig,'vertical-slices')
fig,axes=plt.subplots(1,2,figsize=(7.2,3.8),constrained_layout=True)
for ax,key in zip(axes,['columns','diagonal']):
    s=f(wiring[key]['critical_radius_squared']);geom(ax,cases[1],colors=wiring[key]['colors'],radius=np.sqrt(s))
    q=np.array(list(map(f,wiring[key]['worst_point'])));ax.scatter(*q,marker='*',s=100,color=red,zorder=6)
    ax.set_title(key.capitalize()+' wiring\n$r_*^2='+wiring[key]['critical_radius_squared']+'$')
    ax.set_xlim(-2.2,2.2);ax.set_ylim(-2.2,2.2)
save(fig,'radius-supports')
sites=[(-2,0),(1,0),(0,2),(1,-2)];target=[[(-1.5,-.75),(1.5,-.75),(1.5,.75)],[(-1.5,-.75),(1.5,.75),(-1.5,.75)]]
full=order_candidates(sites,target);small=support_candidates(sites,target)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.4),constrained_layout=True)
for ax,master,title in [(axes[0],full,'Full order arrangement'),(axes[1],small,'Three-site support construction')]:
    pts=np.array([[f(x) for x in p] for p in master['points']]);ax.scatter(pts[:,0],pts[:,1],s=16,color=blue)
    ax.add_patch(Polygon([(-1.5,-.75),(1.5,-.75),(1.5,.75),(-1.5,.75)],fill=False,edgecolor=gray))
    ax.set_aspect('equal');ax.set_title(title+f'\n{len(pts)} rational candidates');ax.set_xlabel('$x$');ax.set_ylabel('$y$')
save(fig,'support-comparison')

fig,axes=plt.subplots(1,2,figsize=(7.2,3.4),constrained_layout=True)
for ax,title in zip(axes,['Independent displacement choices','One shared displacement vector']):
    for x in [-.6,.6]:ax.add_patch(Circle((x,0),1,fill=False,edgecolor=blue));ax.add_patch(Circle((x,0),.6,fill=False,linestyle=':',edgecolor=gold));ax.plot(x,0,'o',color=blue)
    ax.add_patch(Polygon([(-.1,-.1),(.1,-.1),(.1,.1),(-.1,.1)],facecolor=teal,alpha=.5));ax.set_xlim(-1.8,1.8);ax.set_ylim(-1.2,1.2);ax.set_aspect('equal');ax.set_title(title);ax.set_xlabel('$x$')
for x,dx in [(-.6,-.6),(.6,.6)]:axes[0].annotate('',(x+dx,0),(x,0),arrowprops={'arrowstyle':'->','color':red,'lw':2})
for x in [-.6,.6]:axes[1].annotate('',(x+.3,.4),(x,0),arrowprops={'arrowstyle':'->','color':teal,'lw':2})
save(fig,'product-errors')

grid=np.linspace(-.6,.6,301);xx,yy=np.meshgrid(grid,grid)
fig,axes=plt.subplots(1,2,figsize=(7.2,3.5),constrained_layout=True)
for ax,key in zip(axes,['columns','diagonal']):
    groups=np.zeros(xx.shape,dtype=np.uint8)
    for i,(x,y) in enumerate(cases[1]['centres']):groups|=(((xx-x)**2+(yy-y)**2<=1.8**2).astype(np.uint8))*(1<<wiring[key]['colors'][i])
    good=(groups==3);ax.imshow(good,origin='lower',extent=[-.6,.6,-.6,.6],cmap=ListedColormap(['#ebc3bf','#c4e1d4']),interpolation='nearest',vmin=0,vmax=1)
    for i,(x,y) in enumerate(cases[1]['centres']):ax.scatter(x,y,s=30,color=[blue,gold][wiring[key]['colors'][i]]);ax.annotate(str(i+1),(x,y),xytext=(4,4),textcoords='offset points')
    ax.set_xlim(-1.25,1.25);ax.set_ylim(-1.25,1.25);ax.set_aspect('equal');ax.set_title(key.capitalize()+': minimum domain cut '+wiring[key]['minimum_domain_deletions']['cost']);ax.set_xlabel('$x$');ax.set_ylabel('$y$')
save(fig,'wiring-comparison')
fig,axes=plt.subplots(2,2,figsize=(7.2,6),constrained_layout=True)
for ax,(kind,error,label) in zip(axes.flat,[('ball',0,'Nominal'),('ball',.1,'Independent ball error 1/10'),('ball',.2,'Independent ball error 1/5'),('box',.1,'Independent box halfwidth 1/10')]):
    count=np.zeros(xx.shape,dtype=np.int16)
    for x,y in cases[1]['centres']:
        if kind=='ball':active=(xx-x)**2+(yy-y)**2<=(1.8-error)**2
        else:active=np.logical_and.reduce([((xx-x-dx)**2+(yy-y-dy)**2<=1.8**2) for dx in [-.1,.1] for dy in [-.1,.1]])
        count+=active
    ax.imshow(count>=2,origin='lower',extent=[-.6,.6,-.6,.6],cmap=ListedColormap(['#ebc3bf','#c4e1d4']),interpolation='nearest',vmin=0,vmax=1);ax.set_aspect('equal');ax.set_title(label);ax.set_xlabel('$x$');ax.set_ylabel('$y$')
save(fig,'uncertainty-panel')
fig,axes=plt.subplots(3,2,figsize=(7.2,7.2),constrained_layout=True)
for ax,case in zip(axes.flat,cases):
    alloc=[f(x) for x in case['protection']['allocation']];n=len(alloc);x=np.arange(n)
    ax.bar(x-.16,[1/n]*n,.32,color='#b9c2cb',label='Uniform');ax.bar(x+.16,alloc,.32,color=blue,label='Certified optimum')
    ax.set_xticks(x,labels=[str(i+1) for i in x]);ax.set_ylim(0,1.05);ax.set_title(case['name'].replace('_',' ')+'\n$V='+case['protection']['lower']+'$');ax.set_ylabel('Protection allocation')
axes[0,0].legend(frameon=False,fontsize=7);save(fig,'protection-allocations')
p=np.linspace(0,1,301);fig,axes=plt.subplots(1,2,figsize=(7.2,3.5),constrained_layout=True)
for ax,key in zip(axes,['columns','diagonal']):
    if key=='columns':v=(1-p)**2;lo=np.maximum(0,1-2*p);hi=1-p
    else:v=1-p*p;lo=1-p;hi=np.minimum(1,2-2*p)
    ax.fill_between(p,lo,hi,color='#dbe6eb',label='All dependence laws');ax.plot(p,v,color=blue,lw=2,label='Independent domains')
    ax.scatter([.1],[float(Q(wiring[key]['reliability_at_p_0_1']))],color=red);ax.set_title(key.capitalize()+' wiring');ax.set_xlabel('Marginal domain failure probability');ax.set_ylabel('Full-target coverage probability');ax.set_xlim(0,1);ax.set_ylim(0,1);ax.grid(alpha=.15)
axes[0].legend(frameon=False,fontsize=7);save(fig,'reliability-curves')
fig,axes=plt.subplots(1,2,figsize=(7.2,3.8),constrained_layout=True);labels=['Cycle 3','Panel 4','Grid 9','Weak 9','Panel 5','Copies 8'];x=np.arange(6)
axes[0].bar(x,[len(c['certificate']['masks']) for c in cases],color=blue);axes[0].set_title('Minimal target patterns');axes[1].bar(x,[f(c['minimum_individual_deletions']['cost']) for c in cases],color=teal);axes[1].set_title('Minimum individual deletions')
for ax in axes:ax.set_xticks(x,labels=labels,rotation=35,ha='right');ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True)
save(fig,'benchmark-cuts')
fig,ax=plt.subplots(1,2,figsize=(7.2,3.6),constrained_layout=True);geom(ax[0],cases[0]);witnesses(ax[0],cases[0]);ax[0].set_title('Three small target assets');graph(ax[1],cases[0]);ax[1].set_title('Pair cuts form an odd cycle\nThree domains are necessary');save(fig,'odd-cycle')
triples=[]
for i in range(31):
    for j in range(31-i):a=i/30;b=j/30;triples.append((a,b,1-max(a,b,1-a-b)))
v=np.array(triples);fig=plt.figure(figsize=(7.2,3.4),constrained_layout=True);ax=fig.add_subplot(121);sc=ax.tricontourf(v[:,0],v[:,1],v[:,2],levels=15,cmap='viridis');ax.plot(1/3,1/3,'*',color='white',ms=12);ax.set_xlabel('$c_1$');ax.set_ylabel('$c_2$');ax.set_aspect('equal');ax.set_title('$c_3=1-c_1-c_2$');fig.colorbar(sc,ax=ax,label='Guaranteed deletion cost')
ax=fig.add_subplot(122,projection='3d');ax.plot_trisurf(v[:,0],v[:,1],v[:,2],cmap='viridis',linewidth=.1,alpha=.9);ax.scatter([1/3],[1/3],[2/3],color=red,s=25);ax.set_xlabel('$c_1$');ax.set_ylabel('$c_2$');ax.set_zlabel('$\\kappa_T$');ax.set_title('Exact piecewise-linear game');ax.view_init(26,-55);save(fig,'budget-game')
fig,ax=plt.subplots(figsize=(7.2,3.9),constrained_layout=True)
for j,(key,label,col) in enumerate([('one_contact','One contact',gray),('two_contacts','Two contacts',blue),('three_contacts','Three contacts',teal)]):
    ax.bar(x+(j-1)*.24,[np.sqrt(f(c['critical_radii']['rules'][key]['squared'])) for c in cases],.24,label=label,color=col)
ax.set_xticks(x,labels=labels,rotation=20,ha='right');ax.set_ylabel('Exact critical radius displayed numerically');ax.legend(frameon=False,fontsize=8);ax.grid(axis='y',alpha=.15);ax.set_axisbelow(True);save(fig,'critical-radius-bars')

table=['\\begin{table}[!htbp]','\\centering\\small','\\caption{Exact synthetic target results with unit protection budget and unit protection coefficients. A dash means that a singleton cut makes one-domain-loss tolerance impossible.}\\label{tab:engineering}',
       '\\begin{tabular}{lrrrrrr}\\toprule Design & $n$ & $|\\mathcal A_T|$ & $\\kappa_T(\\mathbf1)$ & $V_T$ & Domains & $|Q_T^{\\rm supp}|$ \\\\ \\midrule']
for label,case in zip(labels,cases):
    table.append(label+' & '+str(len(case['centres']))+' & '+str(len(case['certificate']['masks']))+' & '+case['minimum_individual_deletions']['cost']+' & $'+case['protection']['lower']+'$ & '+str(case['minimum_domains_for_one_domain_loss'] or '--')+' & '+str(case['critical_radii']['candidate_count'])+r' \\')
table+=['\\bottomrule\\end{tabular}','\\end{table}'];(ROOT/'standalone/engineering-table.tex').write_text('\n'.join(table)+'\n')
print('Created thirteen new vector figures and the engineering result table.')
