import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
for f in ['Kalam-Regular.ttf','Kalam-Bold.ttf']: fm.fontManager.addfont(f)
ink='#1d3a8a'
plt.rcParams.update({'font.family':'Kalam','font.size':12,'text.color':ink,'axes.labelcolor':ink,
 'xtick.color':ink,'ytick.color':ink,'axes.edgecolor':ink,'figure.facecolor':'white','savefig.dpi':200})
x=np.array([1,1,2,2,3,3,4,4,5,5]);y=np.array([5,3,3,1,2,1,2,1,1,2]);L=np.array([1,0,1,0,1,0,1,0,0,1])
d=['D%d'%i for i in range(1,11)]
c1,c0='#1a8a3a','#c0262d'
def style(ax,zl,title):
    ax.set_xlabel('x  (crew productivity, m³/hr)',labelpad=8)
    ax.set_ylabel('y  (equipment util., hr/day)',labelpad=8)
    ax.set_zlabel(zl,labelpad=6); ax.set_xticks([1,2,3,4,5]); ax.set_yticks([1,2,3,4,5]); ax.set_title(title,fontsize=15,fontweight='bold',pad=4)
    for a in (ax.xaxis,ax.yaxis,ax.zaxis):
        a.set_pane_color((1,1,1,0)); a._axinfo['grid'].update(color='#9db3d9',linewidth=0.5,linestyle='--')
def pts(ax,z,lab=True):
    for cls,col,m,name in [(1,c1,'o','Class 1 (Acceptable)'),(0,c0,'^','Class 0 (Unacceptable)')]:
        k=L==cls; ax.scatter(x[k],y[k],z[k],c=col,marker=m,s=70,edgecolors='k',linewidths=.6,depthshade=False,label=name)
    if lab:
        for i in range(10): ax.text(x[i],y[i],z[i]+(0.08 if z.max()<2 else 0.5),d[i],fontsize=9,color=ink)
# a) dataset
fig=plt.figure(figsize=(7,5.6));ax=fig.add_subplot(projection='3d')
for i in range(10): ax.plot([x[i]]*2,[y[i]]*2,[0,L[i]],color='#7a8fc0',lw=1,ls=':')
pts(ax,L.astype(float)); ax.set_zticks([0,1]); style(ax,'Label (0 / 1)','Fig 1: 3D plot of the given dataset')
ax.view_init(22,-58); ax.legend(loc='upper left',fontsize=10,frameon=False); fig.tight_layout(); fig.savefig('fig1.png'); plt.close()
X,Y=np.meshgrid(np.linspace(1,5,40),np.linspace(1,5,40))
# b1) z=xy
fig=plt.figure(figsize=(7,5.6));ax=fig.add_subplot(projection='3d')
ax.plot_surface(X,Y,X*Y,cmap='Blues',alpha=.35,edgecolor='none')
ax.plot_wireframe(X,Y,X*Y,rstride=8,cstride=8,color='#5b7bc0',lw=.5)
z1=(x*y).astype(float); pts(ax,z1)
ax.plot_surface(X,Y,np.full_like(X,5.5),color='orange',alpha=.18)
ax.text(5,5,6.2,'threshold z = 5.5',color='#c66a00',fontsize=10)
style(ax,'z = xy','Fig 2: z = xy plotted on the dataset'); ax.view_init(24,-130)
ax.legend(loc='upper left',fontsize=10,frameon=False); fig.tight_layout(); fig.savefig('fig2.png'); plt.close()
# b2) z=-log x
fig=plt.figure(figsize=(7,5.6));ax=fig.add_subplot(projection='3d')
Z=-np.log10(X); ax.plot_surface(X,Y,Z,cmap='Purples',alpha=.35,edgecolor='none')
ax.plot_wireframe(X,Y,Z,rstride=8,cstride=8,color='#7d5bb0',lw=.5)
z2=-np.log10(x); pts(ax,z2)
ax.plot_surface(X,Y,np.full_like(X,-0.4),color='orange',alpha=.18)
ax.text(1,1,-0.37,'threshold z = -0.4',color='#c66a00',fontsize=10)
style(ax,'z = -log(x)','Fig 3: z = -log(x) plotted on the dataset'); ax.view_init(24,-60)
ax.legend(loc='upper right',fontsize=10,frameon=False); fig.tight_layout(); fig.savefig('fig3.png'); plt.close()
# c) 2D check of threshold
fig,axs=plt.subplots(1,2,figsize=(10,3.8))
for a,z,t,ttl in [(axs[0],z1,5.5,'z = xy  (threshold = 5.5)'),(axs[1],z2,-0.4,'z = -log(x)  (threshold = -0.4)')]:
    idx=np.arange(1,11)
    a.scatter(idx[L==1],z[L==1],c=c1,s=60,edgecolors='k',label='actual 1')
    a.scatter(idx[L==0],z[L==0],c=c0,marker='^',s=60,edgecolors='k',label='actual 0')
    a.axhline(t,color='#c66a00',ls='--',lw=1.5); a.set_xticks(idx); a.set_xticklabels(d,fontsize=9)
    a.set_title(ttl,fontweight='bold'); a.set_ylabel('z value'); a.grid(color='#cfd9ee',ls='--',lw=.5)
    for s in ['top','right']: a.spines[s].set_visible(False)
axs[0].legend(frameon=False,fontsize=10); fig.suptitle('Fig 4: Points above the dashed line are predicted as Class 1',fontsize=13)
fig.tight_layout(); fig.savefig('fig4.png'); plt.close()
