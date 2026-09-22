#!/usr/bin/env python3
"""Python analogue of the solution-comparison notebooks: retain every local optimum."""
from pathlib import Path
import sys,argparse,json
import numpy as np
from scipy.optimize import minimize
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import vpc_metric

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--spin',type=float,required=True,choices=[1.5,2.5,3.5]); ap.add_argument('--time',type=float,required=True); ap.add_argument('--starts',type=int,default=200); ap.add_argument('--seed',type=int,default=20260922); ap.add_argument('--out',required=True); a=ap.parse_args(); rng=np.random.default_rng(a.seed); n=int(2*a.spin); rows=[]
    f=lambda x:vpc_metric(a.spin,np.mod(x,2*np.pi),a.time,np.pi/2,np.pi/2,'ku')
    for k in range(a.starts):
        x0=rng.uniform(-np.pi,np.pi,n); r=minimize(f,x0,method='L-BFGS-B',bounds=[(-2*np.pi,2*np.pi)]*n,options={'maxiter':300,'ftol':1e-12}); rows.append({'start':k,'xi':float(r.fun),'phases':np.mod(r.x,2*np.pi).tolist(),'success':bool(r.success)})
    rows.sort(key=lambda q:q['xi']); Path(a.out).write_text(json.dumps(rows,indent=2)); print('best',rows[0]); print('top unique xi',sorted(set(round(x['xi'],9) for x in rows))[:12])
if __name__=='__main__': main()
