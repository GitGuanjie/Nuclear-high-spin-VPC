#!/usr/bin/env python3
from pathlib import Path
import sys,json
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *
from vpc.presets import T1,SPINS
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'
PH=json.loads((OUT/'selected_python_optimized_phases.json').read_text())

def mcurve(rhos,I): return np.array([xi_wineland(r,I) for r in rhos])
def direct(I,H,psi,times,noise):
    cs,rs=noise_channel(I,noise); r0=rho_of(psi)
    return np.array([xi_wineland(evolve_lindblad(H,r0,float(t),cs,rs),I) for t in times])
def piece(I,p,times,axis,noise):
    cs,rs=noise_channel(I,noise)
    return mcurve(piecewise_vpc_rotation_curve(I,p,times,T1[I],axis,cs,rs),I)
def cont(I,p,times,noise):
    cs,rs=noise_channel(I,noise); r0=rho_of(css_state(I,np.pi/2,np.pi/2)); H=h_vpc(I,p)
    return np.array([xi_wineland(evolve_lindblad(H,r0,float(t),cs,rs),I) for t in times])

def one(I,n=41,tmax=1.1):
    times=np.linspace(0,tmax,n); pku=np.array(PH[str(I)]['ku_phases']); pr=np.array(PH[str(I)]['wineland_phases']); d={'time':times}
    for noise in ['none','Iz','Iz2']:
        d[f'OAT_{noise}']=direct(I,h_oat(I),css_state(I,np.pi/2,np.pi/2),times,noise)
        d[f'TACT_CSSy_{noise}']=direct(I,h_tact(I),css_state(I,np.pi/2,np.pi/2),times,noise)
        d[f'TACT_CSSz_{noise}']=direct(I,h_tact(I),css_state(I,0,np.pi/2),times,noise)
        d[f'VPC_KUphases_continue_{noise}']=cont(I,pku,times,noise)
        d[f'VPC_Rphases_rotX_{noise}']=piece(I,pr,times,'x',noise)
        d[f'VPC_Rphases_rotY_{noise}']=piece(I,pr,times,'y',noise)
    pd.DataFrame(d).to_csv(OUT/f'Fig12_I{I:g}_python.csv',index=False)
    fig,ax=plt.subplots(figsize=(7.2,4.9))
    # noiseless core curves
    for key in ['OAT_none','TACT_CSSy_none','TACT_CSSz_none','VPC_KUphases_continue_none','VPC_Rphases_rotX_none','VPC_Rphases_rotY_none']:
        ax.plot(times,d[key],label=key)
    # representative noisy VPC + corrected TACT curves
    for key,ls in [('TACT_CSSz_Iz','--'),('TACT_CSSz_Iz2',':'),('VPC_Rphases_rotX_Iz','--'),('VPC_Rphases_rotX_Iz2',':'),('VPC_Rphases_rotY_Iz','--'),('VPC_Rphases_rotY_Iz2',':')]:
        ax.plot(times,d[key],label=key,ls=ls,alpha=.8)
    ax.axvline(T1[I],lw=1,ls=':'); ax.set(xlabel='dimensionless time',ylabel=r'$\xi_R^2$',title=f'Fig. 12 Python reproduction, I={I:g}'); ax.set_ylim(0,2.0); ax.legend(fontsize=5.7,ncol=3); fig.tight_layout()
    tag={1.5:'a',2.5:'b',3.5:'c'}[I]; fig.savefig(OUT/f'Fig12{tag}_python.png',dpi=180); plt.close(fig)
    return {k:float(np.nanmin(v[np.isfinite(v)])) for k,v in d.items() if k!='time' and np.isfinite(v).any()}

def main():
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,choices=[1.5,2.5,3.5]); ap.add_argument('--points',type=int,default=41); ap.add_argument('--tmax',type=float,default=1.1); a=ap.parse_args(); summary={}
    for I in ([a.spin] if a.spin else SPINS):
        summary[str(I)]=one(I,a.points,a.tmax); print(I,summary[str(I)])
    p=OUT/'Fig12_python_summary.json'; old=json.loads(p.read_text()) if p.exists() else {}; old.update(summary); p.write_text(json.dumps(old,indent=2))
if __name__=='__main__': main()
