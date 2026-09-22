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

def metric_curve(rhos,I,fn=xi_ku): return np.array([fn(r,I) for r in rhos])

def direct_protocol_curve(I,H,psi0,times,noise):
    cs,rs=noise_channel(I,noise); rho0=rho_of(psi0)
    return metric_curve([evolve_lindblad(H,rho0,float(t),cs,rs) for t in times],I)

def vpc_piece(I,p,times,axis,noise):
    cs,rs=noise_channel(I,noise)
    return metric_curve(piecewise_vpc_rotation_curve(I,p,times,T1[I],axis,cs,rs),I)

def vpc_continue(I,p,times,noise='none'):
    cs,rs=noise_channel(I,noise); rho0=rho_of(css_state(I,np.pi/2,np.pi/2)); H=h_vpc(I,p)
    return metric_curve([evolve_lindblad(H,rho0,float(t),cs,rs) for t in times],I)

def fig6(I,n=61,tmax=1.2):
    p=np.array(PH[str(I)]['ku_phases']); times=np.linspace(0,tmax,n); d={'time':times}
    d['VPC_continue_noiseless']=vpc_continue(I,p,times)
    d['VPC_rotX_noiseless']=vpc_piece(I,p,times,'x','none'); d['VPC_rotY_noiseless']=vpc_piece(I,p,times,'y','none')
    for noise in ['Iz','Ix','IzIx']:
        d[f'VPC_rotX_{noise}']=vpc_piece(I,p,times,'x',noise); d[f'VPC_rotY_{noise}']=vpc_piece(I,p,times,'y',noise)
    d['OAT_noiseless']=direct_protocol_curve(I,h_oat(I),css_state(I,np.pi/2,np.pi/2),times,'none')
    for noise in ['none','Iz','Ix','IzIx']:
        d[f'TACT_CSSz_{noise}']=direct_protocol_curve(I,h_tact(I),css_state(I,0,np.pi/2),times,noise)
    pd.DataFrame(d).to_csv(OUT/f'Fig6_I{I:g}_python.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,4.8)); ax.plot(times,d['VPC_continue_noiseless'],label='VPC continue')
    ax.plot(times,d['VPC_rotX_noiseless'],label='VPC->Ix no noise'); ax.plot(times,d['VPC_rotY_noiseless'],label='VPC->Iy no noise')
    for noise in ['Iz','Ix','IzIx']:
        ax.plot(times,d[f'VPC_rotX_{noise}'],label=f'VPC->Ix {noise}',alpha=.75)
        ax.plot(times,d[f'VPC_rotY_{noise}'],label=f'VPC->Iy {noise}',ls='--',alpha=.75)
    ax.plot(times,d['OAT_noiseless'],label='OAT',lw=1.5)
    for noise,ls in [('none','-'),('Iz','--'),('Ix',':'),('IzIx','-.')]: ax.plot(times,d[f'TACT_CSSz_{noise}'],label=f'TACT CSSz {noise}',ls=ls,lw=1.5)
    ax.axvline(T1[I],lw=1,ls=':'); ax.set(xlabel='dimensionless time',ylabel=r'$\xi_S^2$',title=f'Fig. 6 Python reproduction, I={I:g}',ylim=(0,1.05)); ax.legend(fontsize=6,ncol=3); fig.tight_layout()
    tag={1.5:'a',2.5:'b',3.5:'c'}[I]; fig.savefig(OUT/f'Fig6{tag}_python.png',dpi=180); plt.close(fig)

def fig7(I,n=61,tmax=1.2):
    p=np.array(PH[str(I)]['ku_phases']); times=np.linspace(0,tmax,n); d={'time':times}
    for noise in ['none','Iz2']:
        d[f'OAT_{noise}']=direct_protocol_curve(I,h_oat(I),css_state(I,np.pi/2,np.pi/2),times,noise)
        d[f'TACT_CSSy_{noise}']=direct_protocol_curve(I,h_tact(I),css_state(I,np.pi/2,np.pi/2),times,noise)
        d[f'TACT_CSSz_{noise}']=direct_protocol_curve(I,h_tact(I),css_state(I,0,np.pi/2),times,noise)
    d['VPC_rotX_none']=vpc_piece(I,p,times,'x','none'); d['VPC_rotX_Iz2']=vpc_piece(I,p,times,'x','Iz2'); d['VPC_rotY_Iz2']=vpc_piece(I,p,times,'y','Iz2')
    pd.DataFrame(d).to_csv(OUT/f'Fig7_I{I:g}_python.csv',index=False)
    fig,ax=plt.subplots(figsize=(7,4.8))
    for key,ls in [('OAT_none','-'),('OAT_Iz2','--'),('TACT_CSSy_none','-'),('TACT_CSSy_Iz2','--'),('TACT_CSSz_none','-'),('TACT_CSSz_Iz2','--')]: ax.plot(times,d[key],label=key,ls=ls)
    ax.plot(times,d['VPC_rotX_none'],label='VPC->Ix no noise'); ax.plot(times,d['VPC_rotX_Iz2'],label='VPC->Ix Iz2',ls='--'); ax.plot(times,d['VPC_rotY_Iz2'],label='VPC->Iy Iz2',ls=':')
    ax.axvline(T1[I],lw=1,ls=':'); ax.set(xlabel='dimensionless time',ylabel=r'$\xi_S^2$',title=f'Fig. 7 Python reproduction, I={I:g}',ylim=(0,1.05)); ax.legend(fontsize=6,ncol=3); fig.tight_layout()
    tag={1.5:'a',2.5:'b',3.5:'c'}[I]; fig.savefig(OUT/f'Fig7{tag}_python.png',dpi=180); plt.close(fig)

def main():
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,choices=[1.5,2.5,3.5]); ap.add_argument('--points',type=int,default=61); ap.add_argument('--tmax',type=float,default=1.2); a=ap.parse_args()
    for I in ([a.spin] if a.spin else SPINS):
        print('running I=',I); fig6(I,a.points,a.tmax); fig7(I,a.points,a.tmax)
if __name__=='__main__': main()
