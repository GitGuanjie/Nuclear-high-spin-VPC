#!/usr/bin/env python3
from pathlib import Path
import json,sys
import numpy as np
from scipy.linalg import expm
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *

def main():
    checks={}
    # Hmuti conversion: fast gauge evolution must equal direct MatrixExp evolution.
    for I in (1.5,2.5,3.5):
        rng=np.random.default_rng(100+int(2*I)); p=rng.uniform(-np.pi,np.pi,int(2*I)); t=.371
        a=vpc_state_fast(I,p,t); b=unitary_state(h_vpc(I,p),css_state(I,np.pi/2,np.pi/2),t)
        checks[f"vpc_gauge_vs_expm_I{I}"]=float(np.linalg.norm(a-b))
    # coherent state should have KU=Wineland=1.
    for I in (1.5,2.5,3.5):
        psi=css_state(I,np.pi/2,np.pi/2)
        checks[f"css_ku_I{I}"]=xi_ku(psi,I); checks[f"css_wineland_I{I}"]=xi_wineland(psi,I)
    tact={}
    expected={1.5:(0.3022999,1/3),2.5:(0.2285606,0.2280944),3.5:(0.1818400,0.1800911)}
    for I in expected:
        t,x=first_tact_minimum(I); tact[str(I)]={"time":t,"xi_ku":x}
        assert abs(t-expected[I][0])<5e-5 and abs(x-expected[I][1])<5e-6
    assert max(checks[k] for k in checks if k.startswith("vpc_gauge"))<1e-10
    assert max(abs(checks[k]-1) for k in checks if "css_" in k)<1e-10
    out=Path(__file__).resolve().parents[1]/"results"; out.mkdir(exist_ok=True)
    payload={"checks":checks,"corrected_tact_cssz":tact,"status":"PASS"}
    (out/"validation_summary.json").write_text(json.dumps(payload,indent=2))
    print(json.dumps(payload,indent=2))
if __name__=="__main__": main()
