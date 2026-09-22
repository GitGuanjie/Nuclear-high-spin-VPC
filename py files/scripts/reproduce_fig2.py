#!/usr/bin/env python3
from pathlib import Path
import sys, json
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *

ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'; OUT.mkdir(exist_ok=True)

def unitary_curve(I,H,psi0,times,fn=xi_ku):
    return np.array([fn(unitary_state(H,psi0,float(t)),I) for t in times])

def one_spin(I,n=35,nstarts=2):
    times=np.linspace(0,np.pi/2,n)
    configs=[('VPC_CSS_equatorial',np.pi/2,np.pi/2),('VPC_CSS_pi4',np.pi/4,np.pi/2),('VPC_CSS_polar',0,np.pi/2)]
    data={'time':times}
    for name,th,ph in configs:
        vals,phases=optimized_vpc_curve(I,times,th,ph,'ku',nstarts,seed=20260922+int(100*I)+int(1000*th))
        data[name]=vals
        np.save(OUT/f'Fig2_I{I:g}_{name}_phases.npy',phases)
    data['OAT_CSS_equatorial']=unitary_curve(I,h_oat(I),css_state(I,np.pi/2,np.pi/2),times)
    data['TACT_CSSy']=unitary_curve(I,h_tact(I),css_state(I,np.pi/2,np.pi/2),times)
    data['TACT_CSSz_corrected']=unitary_curve(I,h_tact(I),css_state(I,0,np.pi/2),times)
    df=pd.DataFrame(data); df.to_csv(OUT/f'Fig2_I{I:g}_python.csv',index=False)
    fig,ax=plt.subplots(figsize=(6.5,4.5))
    ax.plot(times,data['VPC_CSS_equatorial'],label='VPC CSS equatorial')
    ax.plot(times,data['VPC_CSS_pi4'],label='VPC CSS pi/4')
    ax.plot(times,data['VPC_CSS_polar'],label='VPC CSS polar')
    ax.plot(times,data['OAT_CSS_equatorial'],label='OAT')
    ax.plot(times,data['TACT_CSSy'],label='TACT CSS_y')
    ax.plot(times,data['TACT_CSSz_corrected'],label='TACT CSS_z corrected')
    ax.set(xlabel='dimensionless time',ylabel=r'$\xi_S^2$',title=f'I={I:g}')
    ax.set_ylim(0,1.05); ax.legend(fontsize=7,ncol=2); fig.tight_layout()
    tag={1.5:'a',2.5:'b',3.5:'c'}[I]; fig.savefig(OUT/f'Fig2{tag}_python.png',dpi=180); plt.close(fig)
    return {k:float(np.min(v)) for k,v in data.items() if k!='time'}

def main():
    summary={}
    import argparse
    ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,choices=[1.5,2.5,3.5]); ap.add_argument('--points',type=int,default=35); ap.add_argument('--starts',type=int,default=2); a=ap.parse_args()
    spins=[a.spin] if a.spin else [1.5,2.5,3.5]
    for I in spins:
        s=one_spin(I,a.points,a.starts); summary[str(I)]=s; print(I,s)
    p=OUT/'Fig2_python_summary.json'
    old=json.loads(p.read_text()) if p.exists() else {}; old.update(summary); p.write_text(json.dumps(old,indent=2))
if __name__=='__main__': main()
