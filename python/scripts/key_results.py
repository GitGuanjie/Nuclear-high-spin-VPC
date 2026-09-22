#!/usr/bin/env python3
from pathlib import Path
import sys,csv,json
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from vpc.core import *
OUT=Path(__file__).resolve().parents[1]/'results'
# Representative target times used in the reported calculations / Python optimization neighborhoods.
ku_targets={1.5:0.534,2.5:1.223,3.5:1.119}
wr_targets={1.5:0.54,2.5:1.40,3.5:1.10}
rows=[]; details={}
for I in (1.5,2.5,3.5):
    tt,tx=first_tact_minimum(I,'ku','z'); tw,wx=first_tact_minimum(I,'wineland','z')
    pk,vk=optimize_vpc_phases(I,ku_targets[I],metric='ku',n_starts=60,seed=123)
    pr,vr=optimize_vpc_phases(I,wr_targets[I],metric='wineland',n_starts=60,seed=123)
    rows.append([I,tt,tx,ku_targets[I],vk,tw,wx,wr_targets[I],vr])
    details[str(I)]={'tact_ku':{'t':tt,'xi':tx},'vpc_ku':{'t':ku_targets[I],'xi':vk,'phases':pk.tolist()},'tact_wineland':{'t':tw,'xi':wx},'vpc_wineland':{'t':wr_targets[I],'xi':vr,'phases':pr.tolist()}}
with open(OUT/'key_results_python.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['I','TACT_CSSz_t_KU','TACT_CSSz_xi_KU','VPC_t_KU','VPC_xi_KU','TACT_CSSz_t_Wineland','TACT_CSSz_xi_Wineland','VPC_t_Wineland','VPC_xi_Wineland']); w.writerows(rows)
(OUT/'key_results_python.json').write_text(json.dumps(details,indent=2))
print((OUT/'key_results_python.csv').read_text())
