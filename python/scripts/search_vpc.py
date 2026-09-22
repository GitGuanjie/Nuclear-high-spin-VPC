#!/usr/bin/env python3
"""Python replacement for VPC Sequence search 3half2/5half2/7half2.nb."""
from pathlib import Path
import sys,json,argparse
import numpy as np
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import optimize_vpc_phases

def main():
    p=argparse.ArgumentParser(); p.add_argument('--spin',type=float,required=True,choices=[1.5,2.5,3.5]); p.add_argument('--time',type=float,required=True); p.add_argument('--theta',type=float,default=np.pi/2); p.add_argument('--phi',type=float,default=np.pi/2); p.add_argument('--metric',choices=['ku','wineland'],default='ku'); p.add_argument('--starts',type=int,default=200); p.add_argument('--seed',type=int,default=20260922); p.add_argument('--out',default=None); a=p.parse_args()
    ph,val=optimize_vpc_phases(a.spin,a.time,a.theta,a.phi,a.metric,a.starts,a.seed)
    obj={'spin':a.spin,'time':a.time,'theta':a.theta,'phi':a.phi,'metric':a.metric,'random_starts':a.starts,'seed':a.seed,'minimum':val,'phases':ph.tolist()}
    print(json.dumps(obj,indent=2));
    if a.out: Path(a.out).write_text(json.dumps(obj,indent=2))
if __name__=='__main__': main()
