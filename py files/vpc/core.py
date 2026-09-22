from __future__ import annotations
from functools import lru_cache
from dataclasses import dataclass
from typing import Iterable, Sequence
import numpy as np
from scipy.linalg import expm, sqrtm
from scipy.optimize import minimize, minimize_scalar
from scipy.sparse.linalg import expm_multiply

Array = np.ndarray

@dataclass(frozen=True)
class SpinOps:
    I: float
    Ix: Array
    Iy: Array
    Iz: Array
    Ip: Array
    Im: Array

@lru_cache(maxsize=None)
def spin_matrices(I: float) -> SpinOps:
    """Angular-momentum matrices in the notebook basis |I,m>, m=I,...,-I."""
    I = float(I)
    d = int(round(2*I+1))
    m = np.arange(I, -I-1, -1, dtype=float)
    if len(m) != d:
        raise ValueError("I must be integer or half-integer")
    Iz = np.diag(m).astype(complex)
    Ip = np.zeros((d,d), complex)
    for j in range(d-1):
        mlower = m[j+1]
        Ip[j,j+1] = np.sqrt(I*(I+1)-mlower*(mlower+1))
    Im = Ip.conj().T
    Ix = (Ip+Im)/2
    Iy = (Ip-Im)/(2j)
    return SpinOps(I,Ix,Iy,Iz,Ip,Im)

def css_state(I: float, theta: float, phi: float) -> Array:
    """Spin-coherent state convention used in the Mathematica notebooks.

    |theta,phi> = exp[i theta (sin(phi) Ix - cos(phi) Iy)] |I,I>.
    """
    o = spin_matrices(float(I))
    ket = np.zeros(o.Ix.shape[0], complex); ket[0] = 1.0
    return expm(1j*theta*(np.sin(phi)*o.Ix - np.cos(phi)*o.Iy)) @ ket

def rho_of(state_or_rho: Array) -> Array:
    a = np.asarray(state_or_rho, dtype=complex)
    if a.ndim == 1:
        return np.outer(a,a.conj())
    if a.ndim == 2 and 1 in a.shape:
        v=a.reshape(-1); return np.outer(v,v.conj())
    return a

def mean_and_covariance(state_or_rho: Array, I: float):
    rho = rho_of(state_or_rho)
    o = spin_matrices(float(I)); S=(o.Ix,o.Iy,o.Iz)
    mean = np.array([np.trace(rho@A).real for A in S])
    cov = np.empty((3,3), float)
    for a,A in enumerate(S):
        for b,B in enumerate(S):
            cov[a,b] = (0.5*np.trace(rho@(A@B+B@A))).real - mean[a]*mean[b]
    return mean,cov

def transverse_min_variance(state_or_rho: Array, I: float) -> tuple[float,float]:
    mean,cov = mean_and_covariance(state_or_rho,I)
    r=float(np.linalg.norm(mean))
    if r < 1e-12:
        return float(np.linalg.eigvalsh(cov)[0]), r
    n=mean/r
    seed=np.array([1.,0.,0.]) if abs(n[0]) < 0.9 else np.array([0.,1.,0.])
    e1=seed-n*np.dot(seed,n); e1/=np.linalg.norm(e1)
    e2=np.cross(n,e1)
    c2=np.array([[e1@cov@e1,e1@cov@e2],[e2@cov@e1,e2@cov@e2]])
    return float(np.linalg.eigvalsh(c2)[0]),r

def xi_ku(state_or_rho: Array, I: float) -> float:
    """Kitagawa-Ueda quantity used in the revised manuscript: 2 Var_min / I."""
    v,_=transverse_min_variance(state_or_rho,I)
    return float(2*v/I)

def xi_wineland(state_or_rho: Array, I: float) -> float:
    """Wineland quantity used in the revised manuscript: 2 I Var_min / |<I>|^2."""
    v,r=transverse_min_variance(state_or_rho,I)
    return float(np.inf if r < 1e-12 else 2*I*v/(r*r))

def h_oat(I: float, chi: float=1.0) -> Array:
    o=spin_matrices(float(I)); return chi*(o.Iz@o.Iz)

def h_tact(I: float, chi: float=1.0) -> Array:
    o=spin_matrices(float(I)); return chi*(o.Ix@o.Ix-o.Iy@o.Iy)

def h_vpc(I: float, phases: Sequence[float], omega: float=1.0) -> Array:
    """GRF VPC Hamiltonian corresponding to Mathematica Hmuti[...].

    The upper off-diagonal transition j has matrix element
    omega * <m|Ix|m-1> exp(-i phi_j).  Equal phi_j=0 gives omega Ix;
    equal phi_j=pi/2 gives omega Iy.
    """
    I=float(I); p=np.asarray(phases,float); n=int(round(2*I))
    if len(p)!=n: raise ValueError(f"spin I={I} requires {n} phases")
    o=spin_matrices(I); H=np.zeros_like(o.Ix)
    for j in range(n):
        h=float(o.Ix[j,j+1].real)
        H[j,j+1]=omega*h*np.exp(-1j*p[j])
        H[j+1,j]=omega*h*np.exp(1j*p[j])
    return H

def unitary_state(H: Array, psi0: Array, t: float) -> Array:
    return expm(-1j*np.asarray(H)*float(t))@np.asarray(psi0).reshape(-1)

@lru_cache(maxsize=4096)
def _ux(I: float, t: float, omega: float=1.0) -> Array:
    return expm(-1j*omega*spin_matrices(float(I)).Ix*float(t))

def vpc_state_fast(I: float, phases: Sequence[float], t: float,
                   theta: float=np.pi/2, phi: float=np.pi/2,
                   omega: float=1.0) -> Array:
    """Exact fast evaluation of exp(-i H_VPC t)|CSS>.

    Since H_VPC = D Ix D^dagger on the open transition chain, this is exactly
    D exp(-i Ix t) D^dagger.  It is cross-checked in tests against direct expm.
    """
    p=np.asarray(phases,float)
    xi=np.r_[0.0,np.cumsum(p)]
    D=np.exp(1j*xi)
    psi=css_state(float(I),float(theta),float(phi))
    return D*(_ux(float(I),float(t),float(omega))@(D.conj()*psi))

def vpc_metric(I: float, phases: Sequence[float], t: float,
               theta: float=np.pi/2, phi: float=np.pi/2,
               metric: str="ku") -> float:
    psi=vpc_state_fast(I,phases,t,theta,phi)
    return (xi_ku if metric.lower() in {"ku","s","xis"} else xi_wineland)(psi,I)

def optimize_vpc_phases(I: float, t: float, theta: float=np.pi/2, phi: float=np.pi/2,
                        metric: str="ku", n_starts: int=12, seed: int=12345,
                        warm_starts: Sequence[Sequence[float]]=(), maxiter: int=300):
    """Random-start local optimization, Python replacement for notebook searches."""
    I=float(I); n=int(round(2*I)); rng=np.random.default_rng(seed)
    starts=[np.asarray(x,float) for x in warm_starts]
    starts += [np.full(n,np.pi/2), np.zeros(n)]
    starts += [rng.uniform(-np.pi,np.pi,n) for _ in range(n_starts)]
    def f(x): return vpc_metric(I,np.mod(x,2*np.pi),t,theta,phi,metric)
    best=(np.inf,None)
    for x0 in starts:
        res=minimize(f,x0,method="L-BFGS-B",bounds=[(-2*np.pi,2*np.pi)]*n,
                     options={"maxiter":maxiter,"ftol":1e-12,"gtol":1e-8})
        if float(res.fun) < best[0]: best=(float(res.fun),np.mod(res.x,2*np.pi))
    return best[1],best[0]

def optimized_vpc_curve(I: float, times: Sequence[float], theta: float=np.pi/2,
                        phi: float=np.pi/2, metric: str="ku", n_starts: int=4,
                        seed: int=20260922):
    """Time-resolved lower envelope: phases are reoptimized independently at each time.

    A continuation seed is included for speed, but each time also receives fresh random
    starts.  This matches the interpretation of Fig. 2 in the revised manuscript.
    """
    vals=[]; phases=[]; prev=[]
    for k,t in enumerate(np.asarray(times,float)):
        if abs(t)<1e-14:
            n=int(round(2*I)); p=np.zeros(n); val=1.0
        else:
            p,val=optimize_vpc_phases(I,float(t),theta,phi,metric,n_starts,
                                      seed+1009*k,warm_starts=prev)
        vals.append(val); phases.append(p); prev=[p]
    return np.asarray(vals),np.asarray(phases)

def liouvillian(H: Array, collapse_ops: Sequence[Array]=(), rates: Sequence[float]=()) -> Array:
    """Lindblad generator for column-major vec(rho). D[L]=L rho L^dag-1/2{L^dag L,rho}."""
    H=np.asarray(H,complex); d=H.shape[0]; eye=np.eye(d, dtype=complex)
    # vec(A rho B) = (B^T kron A) vec(rho), column-major convention
    L=-1j*(np.kron(eye,H)-np.kron(H.T,eye))
    for C,g in zip(collapse_ops,rates):
        C=np.asarray(C,complex); A=C.conj().T@C
        L += float(g)*(np.kron(C.conj(),C)-0.5*np.kron(eye,A)-0.5*np.kron(A.T,eye))
    return L

def evolve_lindblad(H: Array, rho0: Array, t: float,
                    collapse_ops: Sequence[Array]=(), rates: Sequence[float]=()) -> Array:
    rho0=rho_of(rho0); d=rho0.shape[0]
    if not collapse_ops:
        U=expm(-1j*np.asarray(H)*float(t)); return U@rho0@U.conj().T
    v=expm(liouvillian(H,collapse_ops,rates)*float(t))@rho0.reshape(-1,order="F")
    rho=v.reshape((d,d),order="F"); rho=(rho+rho.conj().T)/2
    return rho/np.trace(rho)

def evolve_piecewise(segments: Sequence[tuple[Array,float]], rho0: Array,
                     collapse_ops: Sequence[Array]=(), rates: Sequence[float]=()) -> Array:
    rho=rho_of(rho0)
    for H,dt in segments:
        if dt>0: rho=evolve_lindblad(H,rho,dt,collapse_ops,rates)
    return rho

def protocol_state_or_rho(protocol: str, I: float, t: float, phases=None, t1=None,
                          rotation_axis: str="x", collapse_ops=(), rates=()):
    o=spin_matrices(float(I)); protocol=protocol.lower()
    if protocol=="oat":
        rho0=rho_of(css_state(I,np.pi/2,np.pi/2)); return evolve_lindblad(h_oat(I),rho0,t,collapse_ops,rates)
    if protocol in {"tact_z","tact_cssz","tact"}:
        rho0=rho_of(css_state(I,0,np.pi/2)); return evolve_lindblad(h_tact(I),rho0,t,collapse_ops,rates)
    if protocol in {"tact_y","tact_cssy"}:
        rho0=rho_of(css_state(I,np.pi/2,np.pi/2)); return evolve_lindblad(h_tact(I),rho0,t,collapse_ops,rates)
    if protocol=="vpc":
        if phases is None: raise ValueError("VPC requires phases")
        rho0=rho_of(css_state(I,np.pi/2,np.pi/2)); Hv=h_vpc(I,phases)
        if t1 is None or t<=t1: return evolve_lindblad(Hv,rho0,t,collapse_ops,rates)
        Hr=o.Ix if rotation_axis.lower()=="x" else o.Iy
        return evolve_piecewise([(Hv,t1),(Hr,t-t1)],rho0,collapse_ops,rates)
    raise ValueError(protocol)

def noise_channel(I: float, name: str):
    o=spin_matrices(float(I)); name=name.lower().replace("^","")
    if name in {"none","no",""}: return [],[]
    if name=="iz": return [o.Iz],[0.1]
    if name=="ix": return [o.Ix],[0.1]
    if name in {"izix","ixiz","iz+ix"}: return [o.Iz,o.Ix],[0.1,0.1]
    if name in {"iz2","iz²"}: return [o.Iz@o.Iz],[0.01]
    raise ValueError(name)

def first_tact_minimum(I: float, metric: str="ku", css: str="z", tmax: float=np.pi/2):
    psi0=css_state(I,0,np.pi/2) if css.lower()=="z" else css_state(I,np.pi/2,np.pi/2)
    H=h_tact(I); fn=xi_ku if metric=="ku" else xi_wineland
    grid=np.linspace(0,tmax,5001); vals=np.array([fn(unitary_state(H,psi0,t),I) for t in grid])
    inds=np.where((vals[1:-1]<vals[:-2])&(vals[1:-1]<vals[2:]))[0]+1
    j=int(inds[0] if len(inds) else np.argmin(vals))
    lo,hi=grid[max(0,j-1)],grid[min(len(grid)-1,j+1)]
    res=minimize_scalar(lambda tt: fn(unitary_state(H,psi0,tt),I),bounds=(lo,hi),method="bounded")
    return float(res.x),float(res.fun)

def fidelity(rho: Array, sigma: Array) -> float:
    rho=rho_of(rho); sigma=rho_of(sigma)
    # Stable pure-state shortcut avoids square-root warnings for rank-1 inputs.
    wr,vr=np.linalg.eigh((rho+rho.conj().T)/2)
    if wr[-1] > 1-1e-10 and np.sum(wr[:-1]) < 1e-9:
        psi=vr[:,-1]
        return float(np.real(np.vdot(psi,sigma@psi)))
    sr=sqrtm(rho); x=sr@sigma@sr
    return float(np.real(np.trace(sqrtm(x)))**2)

def cat_z_state(I: float, relative_phase: float=0.0) -> Array:
    d=int(round(2*I+1)); v=np.zeros(d,complex); v[0]=1; v[-1]=np.exp(1j*relative_phase); return v/np.sqrt(2)


def evolve_lindblad_uniform_times(H: Array, rho0: Array, times: Sequence[float],
                                  collapse_ops: Sequence[Array]=(), rates: Sequence[float]=()):
    """Efficient evolution on a uniform nonnegative time grid."""
    times=np.asarray(times,float); rho0=rho_of(rho0); d=rho0.shape[0]
    if len(times)==0: return np.empty((0,d,d),complex)
    if len(times)==1: return np.asarray([evolve_lindblad(H,rho0,float(times[0]),collapse_ops,rates)])
    if abs(times[0])>1e-12 or not np.allclose(np.diff(times),np.diff(times)[0],rtol=1e-8,atol=1e-10):
        return np.asarray([evolve_lindblad(H,rho0,float(t),collapse_ops,rates) for t in times])
    L=liouvillian(H,collapse_ops,rates)
    v0=rho0.reshape(-1,order="F")
    vs=expm_multiply(L,v0,start=0.0,stop=float(times[-1]),num=len(times),endpoint=True)
    out=[]
    for v in vs:
        rho=v.reshape((d,d),order="F"); rho=(rho+rho.conj().T)/2; rho/=np.trace(rho); out.append(rho)
    return np.asarray(out)

def piecewise_vpc_rotation_curve(I: float, phases: Sequence[float], times: Sequence[float], t1: float,
                                 rotation_axis: str="x", collapse_ops=(), rates=()):
    """Density matrices for VPC until t1 and a linear Ix/Iy rotation afterwards."""
    times=np.asarray(times,float); o=spin_matrices(float(I)); rho0=rho_of(css_state(I,np.pi/2,np.pi/2))
    Hv=h_vpc(I,phases); Hr=o.Ix if rotation_axis.lower()=="x" else o.Iy
    out=[]
    rho1=evolve_lindblad(Hv,rho0,t1,collapse_ops,rates)
    for t in times:
        if t<=t1+1e-14: out.append(evolve_lindblad(Hv,rho0,float(t),collapse_ops,rates))
        else: out.append(evolve_lindblad(Hr,rho1,float(t-t1),collapse_ops,rates))
    return np.asarray(out)
