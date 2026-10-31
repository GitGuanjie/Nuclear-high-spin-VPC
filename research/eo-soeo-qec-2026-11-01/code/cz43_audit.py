#!/usr/bin/env python3
"""Full 64D two-EO audit of recovered pre-existing 43P control word; independent Pauli construction.
Source: library file R4_SANDWICH_CZ25_LINE6_Hpb.csv, no claim of new CZ or numerical novelty.
Six physical spin basis standard groups 123 and 456; all 16 logical x gauge input columns.
"""
import numpy as np,csv,json,sys,os
from pathlib import Path
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
up=np.array([1.,0.]);dn=np.array([0.,1.]);m=np.array([[0.,0.],[1.,0.]],complex)
k=lambda a,b,c:np.kron(np.kron(a,b),c)
k0=(k(up,dn,up)-k(dn,up,up))/np.sqrt(2)
k1=np.sqrt(2/3)*k(up,up,dn)-(k(up,dn,up)+k(dn,up,up))/np.sqrt(6)
F=np.kron(m,np.eye(4))+np.kron(I,np.kron(m,I))+np.kron(np.eye(4),m)
vecs=[k0,F@k0,k1,F@k1]
E=np.column_stack([np.kron(vecs[2*a+ga],vecs[2*b+gb]) for a in range(2) for ga in range(2) for b in range(2) for gb in range(2)])
D=64;Id=np.eye(D);P=E@E.conj().T;Q=Id-P

def o(q,k):
 r=np.array([[1.]],complex)
 for i in range(6):r=np.kron(r,q if i==k else I)
 return r
PP={}
for i in range(6):
 for j in range(i+1,6):
  PP[f'{i+1}{j+1}']=(Id-sum(o(s,i)@o(s,j) for s in [X,Y,Z]))/4
  assert np.linalg.norm(PP[f'{i+1}{j+1}']@PP[f'{i+1}{j+1}']-PP[f'{i+1}{j+1}'])<1e-12
src=Path(sys.argv[1]);rows=list(csv.DictReader(src.open()))
U=Id.astype(complex);G={};bonds=[]
for row in rows:
 i=int(row['bond_i']);j=int(row['bond_j']);bond=f'{i}{j}';a=float(row['area_a']);theta=np.pi*a
 T=PP[bond]
 if bond not in G:G[bond]=np.zeros_like(U)
 G[bond]+=theta*(U.conj().T@T@U)
 U=(Id+(np.exp(1j*theta)-1)*T)@U
 bonds.append(bond)
C=E.conj().T@U@E
# rank-one local rotated reflection U = I - 2 |v v><v v|
v=np.array([np.sqrt(3)/2,1/2]);ee=np.kron(v,v)
R=np.eye(4)-2*np.outer(ee,ee)
Target=np.zeros((16,16),complex)
for la in range(2):
 for ga in range(2):
  for lb in range(2):
   for gb in range(2):
    j=8*la+4*ga+2*lb+gb
    for la2 in range(2):
     for lb2 in range(2):
      jj=8*la2+4*ga+2*lb2+gb
      Target[j,jj]=R[2*la+lb,2*la2+lb2]
phi=np.trace(Target.conj().T@C)/16
endpoint=float(np.linalg.norm(C-phi*Target));leak=float(np.linalg.norm(Q@U@E))
chs={}
for b,g in G.items():
 A=E.conj().T@g@E
 c=(np.trace(A)/16).real
 L=A-c*np.eye(16)
 leakmat=Q@g@E
 harm=(np.linalg.norm(L)**2+np.linalg.norm(leakmat)**2)/16
 chs[b]={'occurrences':bonds.count(b),'scalar_phase_derivative':float(c),'logic_gauge_tangent_fro':float(np.linalg.norm(L)),'leakage_tangent_fro':float(np.linalg.norm(leakmat)),'mean_square_tangent':float(harm)}
out={'name':src.name,'n_pulses':len(rows),'total_area_pi':sum(float(x['area_a']) for x in rows),'phase':str(phi),'endpoint_target_fro':endpoint,'leak_nominal_fro':leak,'target':'rotated CZ reflection I-2|v,v><v,v|, v=(sqrt3/2,1/2), identity on gauge','per_bond':chs,'sum_mean_square_tangent':sum(x['mean_square_tangent'] for x in chs.values())}
print(json.dumps(out,indent=2))
if len(sys.argv)>2:Path(sys.argv[2]).write_text(json.dumps(out,indent=2))
assert endpoint<1e-10 and leak<1e-10
assert all(v['logic_gauge_tangent_fro']>1e-5 or v['leakage_tangent_fro']>1e-5 for v in chs.values())
