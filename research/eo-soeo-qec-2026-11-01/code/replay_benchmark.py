#!/usr/bin/env python3
"""Model benchmark: persistent independent gains by physical bond, iid per pulse, gauge-averaged fidelity.
Change N=... for greater sample count. Uses pure NumPy and NumPy default_rng; no experiments.
"""
import numpy as np,csv
from pathlib import Path
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
Ps=[(I+Z)/2,(I-.8660254037844386*X-.5*Z)/2]
Ts={'H':(X+Z)/np.sqrt(2),'S':np.diag([np.exp(-1j*np.pi/4),np.exp(1j*np.pi/4)]),'Z':Z}
root=Path(__file__).resolve().parent.parent
rng=np.random.default_rng(20261031);N=3000
cases=[('EO_H_3P_REFERENCE.csv','H'),('EO_H_9P_BASELINE.csv','H'),('EO_H_11P.csv','H'),('EO_S_13P.csv','S'),('EO_Z_13P.csv','Z')]
gains=rng.normal(0,.015,(N,2));iid=rng.normal(0,.0006,(N,13))
for file,target in cases:
 with open(root/'sequences'/file) as f: rows=list(csv.DictReader(f))
 bs=[0 if r['bond']=='J12' else 1 for r in rows];a=[float(r['area_a']) for r in rows]
 vals=[]
 for m in range(N):
  U=I.copy()
  for k,(b,aa) in enumerate(zip(bs,a)):
   theta=np.pi*aa*(1+gains[m,b]+iid[m,k]);U=(I+(np.exp(1j*theta)-1)*Ps[b])@U
  tr=np.trace(Ts[target].conj().T@U)
  vals.append(max(0.,(4-abs(tr)**2)/5))
 vals=np.array(vals)
 print(f'{file}: mean={vals.mean():.9g}, SEM={vals.std()/np.sqrt(N):.3g}, n={N}')
