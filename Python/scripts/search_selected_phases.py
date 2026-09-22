#!/usr/bin/env python3
from pathlib import Path
import json, sys
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import optimize_vpc_phases, vpc_metric
from vpc.presets import T1,SPINS

def main():
    out=Path(__file__).resolve().parents[1]/"results"; out.mkdir(exist_ok=True)
    data={}
    for I in SPINS:
        p,val=optimize_vpc_phases(I,T1[I],metric="ku",n_starts=28,seed=20260922+int(10*I))
        pw,valw=optimize_vpc_phases(I,T1[I],metric="wineland",n_starts=28,seed=20261022+int(10*I),warm_starts=[p])
        data[str(I)]={"t1":T1[I],"ku_phases":[float(x) for x in p],"ku_xi":float(val),
                      "wineland_phases":[float(x) for x in pw],"wineland_xi":float(valw)}
        print(I,"KU",val,p,"Wineland",valw,pw)
    (out/"selected_python_optimized_phases.json").write_text(json.dumps(data,indent=2))
if __name__=="__main__": main()
