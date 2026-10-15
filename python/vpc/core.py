"""Independent NumPy/SciPy engine for high-spin VPC reproduction.

Convention: h_vpc has (j,j+1) = (I_x)_(j,j+1) exp(-i phi_j)
with the Rabi-rate normalisation Omega=1.  Nuclear-spin Hilbert space
basis is |I,m> in descending m order. h_oat=I_z^2,
h_tact=I_x^2-I_y^2 (chi=1).
"""
from functools import lru_cache
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize, minimize_scalar


@lru_cache(maxsize=None)
def spin_operators(I):
    I = float(I)
    n = int(round(2 * I + 1))
    if abs(n - (2 * I + 1)) > 1e-10 or I < 0.5:
        raise ValueError("I must be a positive integer or half-integer")
    m = np.arange(n, dtype=float)
    m = I - m
    iz = np.diag(m).astype(complex)
    ip = np.zeros((n,n),complex)
    for j in range(n-1):
        ip[j, j+1] = np.sqrt(I*(I+1) - m[j+1]*(m[j+1]+1))
    im = ip.conj().T
    ix = (ip + im)/2
    iy = (ip - im)/(2j)
    return ix,iy,iz


def css_state(I,theta=np.pi/2,phi=np.pi/2):
    ix, iy, iz = spin_operators(I)
    ket = np.zeros(ix.shape[0],complex); ket[0]=1.0
    return expm(-1j*float(theta)*(np.cos(phi)*iy-np.sin(phi)*ix))@ket


def phase_diagonal(I,phases):
    p=np.asarray(phases,dtype=float).ravel()
    n=int(round(2*float(I)+1))
    if p.size != n-1:
        raise ValueError(f"Expected {n-1} phases, got {p.size}")
    return np.exp(1j*np.r_[0,np.cumsum(p)])


def h_vpc(I,phases):
    d=phase_diagonal(I,phases)
    ix,_,_=spin_operators(I)
    return d[:,None]*ix*d.conj()[None,:]


def h_oat(I):
    iz=spin_operators(I)[2]
    return iz@iz


def h_tact(I):
    ix,iy,_=spin_operators(I)
    return ix@ix-iy@iy


def unitary_state(H,initial,t):
    return expm(-1j*np.asarray(H)*float(t))@np.asarray(initial,dtype=complex)


def vpc_state_fast(I,phases,t,theta=np.pi/2,phi=np.pi/2):
    d=phase_diagonal(I,phases)
    ix=spin_operators(I)[0]
    psi0=css_state(I,theta,phi)
    # D exp(-i I_x t) D^\dagger, diagonal D; exact phase gauge identity.
    return d * (expm(-1j*float(t)*ix)@(d.conj()*psi0))


def rho_of(state):
    a=np.asarray(state,dtype=complex)
    if a.ndim == 2:
        return a
    return np.outer(a,a.conj())


def expectation(rho,op):
    return np.trace(rho_of(rho)@op)


def _covariance(rho,I):
    ops=spin_operators(I)
    density=rho_of(rho)
    mean=np.real(np.array([np.trace(density@a) for a in ops]))
    cov=np.array([[np.real(np.trace(density@(a@b+b@a)))/2 - mean[j]*mean[k]
                    for k,b in enumerate(ops)] for j,a in enumerate(ops)])
    return mean,(cov+cov.T)/2


def transverse_min_variance(rho,I):
    mean,cov=_covariance(rho,I)
    norm=np.linalg.norm(mean)
    if norm < 1e-12:
        # Conventional mean-spin transverse direction undefined here.
        # Return NaN rather than silently selecting an arbitrary plane.
        return float('nan')
    n0=mean/norm
    # Pick a stable transverse basis and diagonalize its 2x2 covariance.
    a=np.array([0.,0.,1.]) if abs(n0[2]) < .9 else np.array([1.,0.,0.])
    n1=np.cross(n0,a); n1/=np.linalg.norm(n1)
    n2=np.cross(n0,n1)
    basis=np.stack([n1,n2],axis=1)
    return max(0.,float(np.linalg.eigvalsh(basis.T@cov@basis)[0]))


def xi_ku(rho,I):
    var=transverse_min_variance(rho,I)
    return float(2*var/float(I))


def xi_wineland(rho,I):
    m,_=_covariance(rho,I)
    r2=np.dot(m,m)
    if r2 < 1e-24:
        return float('inf')
    return float(2*float(I)*transverse_min_variance(rho,I)/r2)


def vpc_metric(I,phases,t,theta=np.pi/2,phi=np.pi/2,metric='ku'):
    psi=vpc_state_fast(I,phases,t,theta,phi)
    fn=xi_ku if metric in ('ku','KU','kitagawa') else xi_wineland
    val=fn(psi,I)
    return val if np.isfinite(val) else 1.e8


def optimize_vpc_phases(I,t,theta=np.pi/2,phi=np.pi/2,metric='ku',
                        n_starts=20,seed=20260922,warm_starts=None):
    rng=np.random.default_rng(seed)
    n=int(round(2*I))
    starts=[]
    if warm_starts is not None:
        for x in warm_starts:
            if x is not None:
                z=np.asarray(x,float).ravel()
                if len(z)==n: starts.append(np.mod(z,2*np.pi))
    if int(n_starts)<1 and not starts:
        starts=[np.full(n,np.pi/2)]
    starts.extend([rng.uniform(0,2*np.pi,n) for _ in range(int(n_starts))])
    f=lambda x:vpc_metric(I,x,t,theta,phi,metric)
    best=np.inf; bestp=None
    for x in starts:
        res=minimize(f,x,method='L-BFGS-B',bounds=[(0,2*np.pi)]*n,
                     options={'ftol':2e-13,'maxiter':350})
        if np.isfinite(res.fun) and res.fun<best:
            best=float(res.fun); bestp=np.mod(res.x,2*np.pi)
    return np.asarray(bestp),float(best)


def optimized_vpc_curve(I,times,theta=np.pi/2,phi=np.pi/2,metric='ku',
                        n_starts=2,seed=20260922):
    times=np.asarray(times,float)
    vals=np.empty(len(times)); p=np.zeros((len(times),int(2*I)))
    for j,t in enumerate(times):
        # Stable independent seeds; the previous time's solution is a warm start.
        warm=[p[j-1]] if j else None
        ph,v=optimize_vpc_phases(I,float(t),theta,phi,metric,n_starts,
                                seed+j,warm)
        p[j]=ph; vals[j]=v
    return vals,p


def first_tact_minimum(I,metric='ku',css='z'):
    psi0=css_state(I,0,np.pi/2) if css=='z' else css_state(I,np.pi/2,np.pi/2)
    H=h_tact(I)
    fn=xi_ku if metric=='ku' else xi_wineland
    f=lambda t:fn(unitary_state(H,psi0,t),I)
    # Scan for the first local minimum, then refine within its bracket.
    grid=np.linspace(0,2.0,2001)
    vals=np.array([f(x) for x in grid])
    for i in range(1,len(grid)-1):
        if vals[i]<vals[i-1] and vals[i]<vals[i+1]:
            opt=minimize_scalar(f,bounds=(grid[i-1],grid[i+1]),method='bounded',
                                options={'xatol':1e-13})
            return float(opt.x),float(opt.fun)
    i=int(np.nanargmin(vals))
    return float(grid[i]),float(vals[i])


def noise_channel(I,kind):
    ix,iy,iz=spin_operators(I)
    mapping={'Iz':[(iz,.1)],'Ix':[(ix,.1)],
             'IzIx':[(iz,.1),(ix,.1)],'Iz2':[(iz@iz,.01)],
             'none':[]}
    if kind not in mapping:
        raise ValueError(f'Unknown noise channel {kind!r}')
    return [x for x,_ in mapping[kind]],[r for _,r in mapping[kind]]


def lindblad_liouvillian(H,collapse_ops=(),rates=()):
    H=np.asarray(H,complex); n=H.shape[0]
    eye=np.eye(n,dtype=complex)
    L=-1j*(np.kron(eye,H)-np.kron(H.T,eye))
    for C,gamma in zip(collapse_ops,rates):
        C=np.asarray(C,complex); q=C.conj().T@C
        L+=float(gamma)*(np.kron(C.conj(),C)
          -.5*np.kron(eye,q)-.5*np.kron(q.T,eye))
    return L


def evolve_lindblad(H,rho,t,collapse_ops=(),rates=()):
    rho=rho_of(rho)
    if float(t)==0: return rho.copy()
    if not collapse_ops:
        U=expm(-1j*float(t)*H)
        return U@rho@U.conj().T
    L=lindblad_liouvillian(H,collapse_ops,rates)
    z=expm(float(t)*L)@rho.reshape((-1,),order='F')
    out=z.reshape(rho.shape,order='F')
    return (out+out.conj().T)/2


def piecewise_vpc_rotation_curve(I,phases,times,t1,axis='x',
                                 collapse_ops=(),rates=()):
    xi,yi,_=spin_operators(I)
    H1=h_vpc(I,phases); H2=xi if axis=='x' else yi
    initial=rho_of(css_state(I,np.pi/2,np.pi/2))
    r1=evolve_lindblad(H1,initial,t1,collapse_ops,rates)
    return [evolve_lindblad(H1,initial,t,collapse_ops,rates) if t<=t1
            else evolve_lindblad(H2,r1,t-t1,collapse_ops,rates) for t in times]


def cat_z_state(I):
    n=int(2*I+1)
    ket=np.zeros(n,complex)
    ket[0]=ket[-1]=1/np.sqrt(2)
    return ket


def fidelity(ref,other):
    # All current scripts use a PURE target reference. Return overlap probability.
    a=np.asarray(ref);b=np.asarray(other)
    if a.ndim==1: a=rho_of(a)
    if b.ndim==1: b=rho_of(b)
    return float(np.clip(np.real(np.trace(a@b)),0,1))

__all__=[n for n in globals() if not n.startswith('_')]
