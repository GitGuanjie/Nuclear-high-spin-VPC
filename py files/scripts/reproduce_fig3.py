#!/usr/bin/env python3
from pathlib import Path
import sys,json,argparse
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import optimize_vpc_phases
from vpc.presets import T1
OUT=Path(__file__).resolve().parents[1]/'results'; OUT.mkdir(exist_ok=True)
PH=json.loads((OUT/'selected_python_optimized_phases.json').read_text())

def one(I,n=19,starts=1):
    th=np.linspace(0,np.pi,n); vals=[]; anchor=np.array(PH[str(I)]['ku_phases']); prev=[anchor]
    for k,x in enumerate(th):
        p,v=optimize_vpc_phases(I,T1[I],theta=float(x),phi=np.pi/2,metric='ku',n_starts=starts,seed=20262000+k+int(10*I),warm_starts=prev+[anchor])
        vals.append(v); prev=[p]
    df=pd.DataFrame({'theta':th,'xi_ku_optimized':vals}); df.to_csv(OUT/f'Fig3_I{I:g}_python.csv',index=False)
    return th,np.asarray(vals)

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,choices=[1.5,2.5,3.5]); ap.add_argument('--points',type=int,default=19); ap.add_argument('--starts',type=int,default=1); a=ap.parse_args(); spins=[a.spin] if a.spin else [1.5,2.5,3.5]
    fig,ax=plt.subplots(figsize=(6.5,4.4))
    for I in spins:
        x,y=one(I,a.points,a.starts); ax.plot(x,y,marker='o',ms=2,label=f'I={I:g}'); print(I,'min',y.min(),'theta',x[y.argmin()])
    ax.set(xlabel='initial polar angle theta',ylabel=r'$\xi_S^2$',title='Fig. 3 Python reproduction'); ax.legend(); fig.tight_layout(); fig.savefig(OUT/'Fig3_python.png',dpi=180); plt.close(fig)
if __name__=='__main__': main()
