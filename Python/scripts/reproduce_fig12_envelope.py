#!/usr/bin/env python3
from pathlib import Path
import sys,json
import numpy as np,pandas as pd
import matplotlib.pyplot as plt
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *
OUT=Path(__file__).resolve().parents[1]/'results'; OUT.mkdir(exist_ok=True)

def one(I,n=25,nstarts=2):
    t=np.linspace(0,np.pi/2,n)
    vpc,p=optimized_vpc_curve(I,t,np.pi/2,np.pi/2,'wineland',nstarts,seed=20261200+int(10*I))
    oat=np.array([xi_wineland(unitary_state(h_oat(I),css_state(I,np.pi/2,np.pi/2),x),I) for x in t])
    ty=np.array([xi_wineland(unitary_state(h_tact(I),css_state(I,np.pi/2,np.pi/2),x),I) for x in t])
    tz=np.array([xi_wineland(unitary_state(h_tact(I),css_state(I,0,np.pi/2),x),I) for x in t])
    pd.DataFrame({'time':t,'VPC_optimized_xiR':vpc,'OAT':oat,'TACT_CSSy':ty,'TACT_CSSz_corrected':tz}).to_csv(OUT/f'Fig12_envelope_I{I:g}_python.csv',index=False)
    np.save(OUT/f'Fig12_envelope_I{I:g}_phases.npy',p)
    fig,ax=plt.subplots(figsize=(6.4,4.3)); ax.plot(t,vpc,label='VPC optimized for xi_R'); ax.plot(t,oat,label='OAT'); ax.plot(t,ty,label='TACT CSS_y'); ax.plot(t,tz,label='TACT CSS_z corrected'); ax.set(xlabel='dimensionless time',ylabel=r'$\xi_R^2$',title=f'Wineland optimized envelope I={I:g}',ylim=(0,1.05)); ax.legend(fontsize=7); fig.tight_layout(); fig.savefig(OUT/f'Fig12_envelope_I{I:g}_python.png',dpi=180); plt.close(fig)
    tm,xm=first_tact_minimum(I,metric='wineland',css='z')
    return {'VPC_grid_min':float(vpc.min()),'VPC_grid_t':float(t[vpc.argmin()]),'TACT_CSSz_exact_min':xm,'TACT_CSSz_exact_t':tm}

def main():
    import argparse; ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,choices=[1.5,2.5,3.5]); ap.add_argument('--points',type=int,default=25); ap.add_argument('--starts',type=int,default=2); a=ap.parse_args(); ss=[a.spin] if a.spin else [1.5,2.5,3.5]; all={}
    for I in ss: all[str(I)]=one(I,a.points,a.starts); print(I,all[str(I)])
    p=OUT/'Fig12_envelope_summary.json'; old=json.loads(p.read_text()) if p.exists() else {}; old.update(all); p.write_text(json.dumps(old,indent=2))
if __name__=='__main__': main()
