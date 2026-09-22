#!/usr/bin/env python3
from pathlib import Path
import sys,json
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *
from vpc.presets import T1,SPINS
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'results'; PH=json.loads((OUT/'selected_python_optimized_phases.json').read_text())

def storage_fidelity(I,psi,times,noise):
    cs,rs=noise_channel(I,noise); H=np.zeros((int(2*I+1),int(2*I+1)),complex); r0=rho_of(psi)
    return np.array([fidelity(r0,evolve_lindblad(H,r0,float(t),cs,rs)) for t in times])

def main():
    times=np.linspace(0,3,121)
    figA,axA=plt.subplots(figsize=(6.2,4.2)); figB,axB=plt.subplots(figsize=(6.2,4.2))
    for I in SPINS:
        p=np.array(PH[str(I)]['ku_phases']); psi=vpc_state_fast(I,p,T1[I]); cat=cat_z_state(I)
        fv_z=storage_fidelity(I,psi,times,'Iz'); fc_z=storage_fidelity(I,cat,times,'Iz')
        fv_q=storage_fidelity(I,psi,times,'Iz2'); fc_q=storage_fidelity(I,cat,times,'Iz2')
        pd.DataFrame({'time':times,'VPC_Iz':fv_z,'cat_Iz':fc_z,'VPC_Iz2':fv_q,'cat_Iz2':fc_q}).to_csv(OUT/f'Fig13_I{I:g}_python.csv',index=False)
        axA.plot(times,fv_z,label=f'VPC I={I:g}'); axA.plot(times,fc_z,ls='--',label=f'cat I={I:g}')
        axB.plot(times,fv_q,label=f'VPC I={I:g}'); axB.plot(times,fc_q,ls='--',label=f'cat I={I:g}')
    for ax,title in [(axA,'Linear Iz noise'),(axB,'Quadratic Iz^2 noise')]: ax.set(xlabel='storage time',ylabel='fidelity',title=title,ylim=(0,1.02)); ax.legend(fontsize=7,ncol=2)
    figA.tight_layout(); figB.tight_layout(); figA.savefig(OUT/'Fig13a_python.png',dpi=180); figB.savefig(OUT/'Fig13b_python.png',dpi=180); plt.close(figA); plt.close(figB)
if __name__=='__main__': main()
