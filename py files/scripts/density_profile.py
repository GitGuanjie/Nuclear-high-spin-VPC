#!/usr/bin/env python3
"""Python replacement for the three Mathematica density-profile notebooks."""
from pathlib import Path
import sys,argparse
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import vpc_metric

def sym_phases(I,pars,center=np.pi/2):
    n=int(2*I); p=np.zeros(n); mid=n//2
    p[mid]=center
    for k,x in enumerate(pars): p[k]=x; p[n-1-k]=np.pi-x
    return p

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,required=True,choices=[1.5,2.5,3.5]); ap.add_argument('--time',type=float,required=True); ap.add_argument('--n',type=int,default=81); ap.add_argument('--fixed-third',type=float,default=.9); ap.add_argument('--outdir',default='results'); a=ap.parse_args(); out=Path(a.outdir); out.mkdir(exist_ok=True)
    if a.spin==1.5:
        x=np.linspace(-np.pi,np.pi,a.n); z=np.array([vpc_metric(a.spin,sym_phases(a.spin,[xx]),a.time) for xx in x]); pd.DataFrame({'phi_a':x,'xi_ku':z}).to_csv(out/'density_I1.5_python.csv',index=False); fig,ax=plt.subplots(); ax.plot(x,z); ax.set(xlabel='phi_a',ylabel='xi_S^2'); fig.tight_layout(); fig.savefig(out/'density_I1.5_python.png',dpi=180)
    else:
        x=np.linspace(-np.pi,np.pi,a.n); y=np.linspace(-np.pi,np.pi,a.n); Z=np.empty((a.n,a.n))
        for i,xx in enumerate(x):
            for j,yy in enumerate(y):
                pars=[xx,yy] if a.spin==2.5 else [xx,yy,a.fixed_third]
                Z[j,i]=vpc_metric(a.spin,sym_phases(a.spin,pars),a.time)
        np.savez_compressed(out/f'density_I{a.spin:g}_python.npz',x=x,y=y,xi=Z)
        fig,ax=plt.subplots(); im=ax.imshow(Z,origin='lower',extent=[x[0],x[-1],y[0],y[-1]],aspect='auto'); fig.colorbar(im,ax=ax,label='xi_S^2'); ax.set(xlabel='phi_a',ylabel='phi_b'); fig.tight_layout(); fig.savefig(out/f'density_I{a.spin:g}_python.png',dpi=180)
if __name__=='__main__': main()
