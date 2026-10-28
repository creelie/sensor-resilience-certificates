"""Display exact symbolic examples; no plotted point is used in a proof."""
from pathlib import Path
from fractions import Fraction as Q
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

OUT=Path(__file__).resolve().parent.parent/'standalone/figures'
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':9,'pdf.fonttype':42,'axes.spines.top':False,'axes.spines.right':False})
blue='#246c91';teal='#4a987b';red='#c3544e';gold='#d8a13c'
fig,axes=plt.subplots(1,2,figsize=(7.2,3.4),constrained_layout=True)
x=[0,2,68/25,89/25,128/25,5.8];y=[0,1,2,3,4,4]
axes[0].step(x,y,where='post',color=blue,lw=2)
for i in range(1,5):
    axes[0].plot(x[i],y[i],'o',color=blue,ms=4)
    axes[0].plot(x[i],y[i-1],'o',markerfacecolor='white',markeredgecolor=blue,ms=4)
axes[0].set_xticks(x[1:5],labels=['2','68/25','89/25','128/25'],rotation=25);axes[0].set_yticks(range(5));axes[0].set_xlabel('Common squared radius $t$');axes[0].set_ylabel('Minimum unit-cost deletions');axes[0].set_title('Exact target resilience staircase');axes[0].grid(alpha=.15)
ax=axes[1];ax.axis('off');ax.set_xlim(0,1);ax.set_ylim(0,1)
boxes=[(.1,.69,.8,.2,'One support set\n$Q_T^{\\mathrm{supp}}$'),(.03,.1,.27,.25,'Radius\nthreshold'),(.365,.1,.27,.25,'Failure\nbudget'),(.7,.1,.27,.25,'Domain\nquery')]
for xx,yy,w,h,label in boxes:
    ax.add_patch(FancyBboxPatch((xx,yy),w,h,boxstyle='round,pad=.012',facecolor='#e3edf1',edgecolor=blue,lw=1));ax.text(xx+w/2,yy+h/2,label,ha='center',va='center',fontsize=10)
for xx in [.165,.5,.835]:ax.annotate('',(xx,.37),(.5,.68),arrowprops={'arrowstyle':'->','color':blue,'lw':1.2})
ax.set_title('Reuse geometry across requirements');fig.savefig(OUT/'analytical-frontier.pdf',bbox_inches='tight');plt.close(fig)

c=np.array([(1,1,1),(1,-1,-1),(-1,1,-1),(-1,-1,1)],dtype=float)
fig=plt.figure(figsize=(6.6,4.7),constrained_layout=True);ax=fig.add_subplot(111,projection='3d')
faces=[[c[i] for i in ids] for ids in [(0,1,2),(0,1,3),(0,2,3),(1,2,3)]]
ax.add_collection3d(Poly3DCollection(faces,facecolors=teal,edgecolors=blue,alpha=.13,linewidths=.8))
u=np.linspace(0,2*np.pi,48);v=np.linspace(0,np.pi,25);r=np.sqrt(3)
ax.plot_wireframe(r*np.outer(np.cos(u),np.sin(v)),r*np.outer(np.sin(u),np.sin(v)),r*np.outer(np.ones_like(u),np.cos(v)),rstride=4,cstride=3,color='#94a8b4',linewidth=.35,alpha=.45)
ax.scatter(c[:,0],c[:,1],c[:,2],s=35,color=blue,depthshade=False);ax.scatter([0],[0],[0],color=red,s=55,marker='*',depthshade=False)
for i,p in enumerate(c):
    ax.text(*(p*1.11),f'$c_{i+1}$',fontsize=10);ax.plot([0,p[0]],[0,p[1]],[0,p[2]],color=gold,linestyle='--',lw=.85)
ax.text(.08,.08,.12,'$q=0$',color=red,fontsize=10);ax.set_xlabel('$x$');ax.set_ylabel('$y$');ax.set_zlabel('$z$');ax.set_box_aspect([1,1,1]);ax.set_xlim(-1.9,1.9);ax.set_ylim(-1.9,1.9);ax.set_zlim(-1.9,1.9);ax.view_init(22,-48)
ax.set_title('Four-site support in three dimensions\n$\\|c_i\\|^2=3$ and $r_*=\\sqrt{3}$');fig.savefig(OUT/'tetrahedron-support.pdf',bbox_inches='tight');plt.close(fig)
print('Created the symbolic frontier schematic and three-dimensional support diagram.')
