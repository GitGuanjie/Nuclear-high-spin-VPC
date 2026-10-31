#!/usr/bin/env python3
"""Single-cross-bond all-spin EO/SOEO obstruction for fixed blocks and strictly block-local frames."""
import numpy as np
I2=np.eye(2,dtype=complex)
u=np.array([1.,0.]);d=np.array([0.,1.]);sing=(np.kron(u,d)-np.kron(d,u))/np.sqrt(2);trip0=(np.kron(u,d)+np.kron(d,u))/np.sqrt(2)
Tplus=np.kron(u,u);Tminus=np.kron(d,d)
B4=np.column_stack([np.kron(sing,sing),(np.kron(trip0,trip0)-np.kron(Tplus,Tminus)-np.kron(Tminus,Tplus))/np.sqrt(3)])
k=lambda a,b,c:np.kron(np.kron(a,b),c)
p0=(k(u,d,u)-k(d,u,u))/np.sqrt(2)
p1=np.sqrt(2/3)*k(u,u,d)-(k(u,d,u)+k(d,u,u))/np.sqrt(6)
low=np.array([[0,0],[1,0]],complex)
L=np.kron(low,np.eye(4))+np.kron(I2,np.kron(low,I2))+np.kron(np.eye(4),low)
B3=np.column_stack([p0,L@p0,p1,L@p1])
for ta,tb,A,B in [('EO','SOEO',B3,B4),('SOEO','SOEO',B4,B4),('EO','EO',B3,B3)]:
 nA=int(round(np.log2(A.shape[0])));nB=int(round(np.log2(B.shape[0])));n=nA+nB
 E=np.kron(A,B);D=2**n;Id=np.eye(D,dtype=complex);P=E@E.conj().T;Q=Id-P
 seen=[]
 for a in range(nA):
  for b in range(nA,n):
   S=np.zeros((D,D),complex)
   for k in range(D):
    s=[(k>>(n-1-j))&1 for j in range(n)];s[a],s[b]=s[b],s[a]
    v=sum(bit<<(n-1-j) for j,bit in enumerate(s));S[v,k]=1
   Ps=(Id-S)/2
   M=E.conj().T@Ps@E
   cross=np.linalg.norm(Q@Ps@E)
   seen.append((round(np.linalg.norm(M-np.trace(M)/len(M)*np.eye(len(M))),10),cross))
 nontriv=max(x[0] for x in seen);ls=np.array([x[1] for x in seen]);
 print(ta+'+'+tb,'Nspins',n,'encoded_rank',E.shape[1],'projected_scalar_resid_max',nontriv,'cross_leak_norm_range',ls.min(),ls.max())
 if ta=='SOEO' or tb=='SOEO':
  expected=np.sqrt(3*E.shape[1]/16)
  assert abs(ls[0]-expected)<1e-12 and nontriv<1e-12
