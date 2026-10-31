#!/usr/bin/env python3
"""Second independent 64D physical checker via bit-permutation swap matrices, not Pauli Hamiltonian."""
import csv,numpy as np
from pathlib import Path
base=Path(__file__).resolve().parent.parent
src=base/'sequences/SOURCE_R4_43P.csv';nws=base/'sequences/CZ_41P_REWRITE.csv'
u=np.array([1,0],complex);d=np.array([0,1],complex)
k=lambda a,b,c:np.kron(np.kron(a,b),c)
v0=(k(u,d,u)-k(d,u,u))/np.sqrt(2)
v1=np.sqrt(2/3)*k(u,u,d)-(k(u,d,u)+k(d,u,u))/np.sqrt(6)
sm=np.array([[0,0],[1,0]],complex)
L=np.kron(sm,np.eye(4))+np.kron(np.eye(2),np.kron(sm,np.eye(2)))+np.kron(np.eye(4),sm)
BC=[v0,L@v0,v1,L@v1]
E=np.column_stack([np.kron(BC[2*a+ga],BC[2*b+gb]) for a in range(2) for ga in range(2) for b in range(2) for gb in range(2)])
P=E@E.conj().T
Id=np.eye(64, dtype=complex)
def physical(b1,b2):
 m=np.zeros((64,64),complex)
 for k in range(64):
  bit=[(k>>(5-i))&1 for i in range(6)];bit[b1],bit[b2]=bit[b2],bit[b1]
  dest=sum(int(b)<<(5-i) for i,b in enumerate(bit));m[dest,k]=1
 return (Id-m)/2
pp={(i,j):physical(i,j) for i in range(6) for j in range(i+1,6)}
def calc(f):
 U=Id.copy();rows=list(csv.DictReader(open(f)))
 for r in rows:
  p=pp[(int(r['bond_i'])-1,int(r['bond_j'])-1)]
  U=(Id+(np.exp(1j*np.pi*float(r['area_a']))-1)*p)@U
 return U,len(rows)
U1,n1=calc(src);U2,n2=calc(nws)
# Rotated CZ: I - 2 |vv><vv| on logicals; identity on gauges
v=np.array([np.sqrt(3)/2,1/2]);w=np.kron(v,v);R=np.eye(4)-2*np.outer(w,w)
target=np.zeros((16,16),complex)
for la in range(2):
 for ga in range(2):
  for lb in range(2):
   for gb in range(2):
    r=8*la+4*ga+2*lb+gb
    for ma in range(2):
     for mb in range(2):target[r,8*ma+4*ga+2*mb+gb]=R[2*la+lb,2*ma+mb]
for name,U in [('43P',U1),('41P',U2)]:
 print(name,'full code target Fro',np.linalg.norm(E.conj().T@U@E-target),'leakage',np.linalg.norm((Id-P)@U@E))
 assert np.linalg.norm(E.conj().T@U@E-target)<1e-11
 assert np.linalg.norm((Id-P)@U@E)<1e-11
print('Full physical 64D U difference:',np.linalg.norm(U1-U2))
assert np.linalg.norm(U1-U2)<1e-11
print('PASS 43P->41P exact rewrite on ALL physical states, 6-spin rotated CZ gauge identity.')
