#!/usr/bin/env python3
"""Standalone full spin-Hilbert check for EO (8D) and SOEO (16D), 2 gauge sectors on EO.
Pure NumPy; reads CSV in ../sequences. No optimizer or pre-existing data dependencies.
"""
from pathlib import Path
import numpy as np,csv
I=np.eye(2,dtype=complex); X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
H=(X+Z)/np.sqrt(2)
T={'H':H,'S':np.diag([np.exp(-1j*np.pi/4),np.exp(1j*np.pi/4)]),'Z':Z}
u=np.array([1.,0]);d=np.array([0.,1.]); sing=(np.kron(u,d)-np.kron(d,u))/np.sqrt(2); trip0=(np.kron(u,d)+np.kron(d,u))/np.sqrt(2)
tp=np.kron(u,u);tm=np.kron(d,d)
B4=np.column_stack((np.kron(sing,sing),(np.kron(trip0,trip0)-np.kron(tp,tm)-np.kron(tm,tp))/np.sqrt(3)))
ket=lambda a,b,c:np.kron(np.kron(a,b),c)
k0=(ket(u,d,u)-ket(d,u,u))/np.sqrt(2);k1=np.sqrt(2/3)*ket(u,u,d)-(ket(u,d,u)+ket(d,u,u))/np.sqrt(6)
sm=np.array([[0.,0.],[1.,0.]])
L=np.kron(sm,np.eye(4))+np.kron(I,np.kron(sm,I))+np.kron(np.eye(4),sm)
B3=np.column_stack((k0,k1,L@k0,L@k1))
def projector(i,j,n):
  D=2**n;sw=np.zeros((D,D),complex)
  for k in range(D):
    bs=[(k>>(n-1-t))&1 for t in range(n)];bs[i],bs[j]=bs[j],bs[i]
    kk=sum(b<<(n-1-t) for t,b in enumerate(bs));sw[kk,k]=1
  return (np.eye(D)-sw)/2
root=Path(__file__).resolve().parent.parent
for name in ['EO_H_11P.csv','EO_S_11P.csv','EO_S_13P.csv','EO_Z_13P.csv']:
  with open(root/'sequences'/name) as f:rows=list(csv.DictReader(f))
  target=name.split('_')[1];areas=[float(r['area_a']) for r in rows];bonds=[0 if r['bond']=='J12' else 1 for r in rows]
  for platform,n,B,indices in [('EO',3,B3,[(0,1),(1,2)]),('SOEO',4,B4,[(0,1),(0,2)])]:
    pp=[projector(i,j,n) for i,j in indices];D=2**n
    U=np.eye(D,dtype=complex);G=[np.zeros((D,D),complex) for _ in range(2)]
    for a,b in zip(areas,bonds):
      P=pp[b];angle=np.pi*a
      G[b]+=angle*(U.conj().T@P@U)
      U=(np.eye(D)+(np.exp(1j*angle)-1)*P)@U
    ideal=np.kron(np.eye(2),T[target]) if platform=='EO' else T[target]
    M=B.conj().T@U@B;phase=np.trace(ideal.conj().T@M)/B.shape[1]
    codeproj=B@B.conj().T
    err=np.linalg.norm(M/phase-ideal)
    leak=np.linalg.norm((np.eye(D)-codeproj)@U@B)
    channels=[]
    for g in G:
      a=B.conj().T@g@B;scalar=np.trace(a)/B.shape[1]
      channels.append(float(np.linalg.norm(a-scalar*np.eye(B.shape[1]))))
    assert err<1e-9 and leak<1e-12 and max(channels)<1e-9
    print(f'PASS {name} {platform}: P={len(rows)}, area={sum(areas):.12f}, gate={err:.3e}, tangents={channels}, leakage={leak:.3e}')
