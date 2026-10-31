#!/usr/bin/env python3
"""Independent six-spin EO-EO one-interblock-pulse impossibility certificate.
Assumptions: exactly one interblock physical positive Heisenberg exchange pulse; all other pulses act only inside each fixed 3-spin EO block and therefore preserve S_A=S_B=1/2. No measurements, shuttling or extra active spins.
"""
import numpy as np
from scipy.linalg import eigh
n=6;I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Y=np.array([[0,-1j],[1j,0]],complex);Z=np.diag([1,-1]).astype(complex)
Id=np.eye(2**n,dtype=complex)
def op(q,i):
 m=np.array([[1]],complex)
 for j in range(n):m=np.kron(m,q if i==j else I)
 return m
def s2(sites):
 s=np.zeros_like(Id)
 for p in [X,Y,Z]:
  z=sum((op(p,i) for i in sites)) / 2
  s+=z@z
 return s
SA=s2(range(3));SB=s2(range(3,6))
PA=(15/4*Id-SA)/3; PB=(15/4*Id-SB)/3
P=PA@PB; Q=Id-P
assert np.linalg.norm(P@P-P)<1e-13
print('Rank P (logical times gauge):',round(np.trace(P).real))
def swap(i,j):
 M=np.zeros_like(Id)
 for x in range(2**n):
  b=[(x>>(n-1-k))&1 for k in range(n)]; b[i],b[j]=b[j],b[i]
  y=sum(bit<<(n-1-k) for k,bit in enumerate(b));M[y,x]=1
 return M
for i in range(3):
 for j in range(3,6):
  ps=(Id-swap(i,j))/2
  C=Q@ps@P
  _,evec=eigh(P)
  basis=evec[:,-16:]
  svals=np.linalg.svd(C@basis,compute_uv=False)
  pvals=np.linalg.eigvalsh(basis.conj().T@ps@basis)
  print(f'J{i+1}{j+1}: Frobenius ||Q P_s P||={np.linalg.norm(C):.12f}, singular values={np.round(np.sort(svals),8).tolist()}, projected P_s eigenvalues={np.round(pvals,8).tolist()}')
  assert np.linalg.norm(C)>1e-2
  for area in [.25,.5,1,1.75]:
   U=Id+(np.exp(1j*np.pi*area)-1)*ps
   leak=np.linalg.norm(Q@U@P)
   pred=2*abs(np.sin(np.pi*area/2))*np.linalg.norm(C)
   assert abs(leak-pred)<1e-12
print('CERTIFIED: nontrivial single cross pulse leaks; local EO pulses cannot undo block-spin leakage (strict fixed triples).')
