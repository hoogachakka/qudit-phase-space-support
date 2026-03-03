import numpy as np
import matplotlib.pyplot as plt
from functools import reduce

def pauli_X(d, p=1): # d = qudit dimension, p (optional) = power
    p %= d
    return np.roll(np.eye(d, dtype=np.complex128), shift=p, axis=0)

def pauli_Z(d, p=1):
    p %= d
    phases = np.exp(2j * np.pi * p * np.arange(d) / d)
    return np.diag(phases.astype(np.complex128))

# computes W(p,q) for a single-qudit gate
def W_single(p, q, d):
    p %= d
    q %= d
    omega = np.exp(2j * np.pi / d)
    inv_two = pow(2, -1, d)
    phase_exp = (-inv_two * p * q) % d
    phase = omega ** phase_exp
    return phase * (pauli_Z(d, p) @ pauli_X(d, q))

# computes W(p,q) for a multi-qudit gate:
# W(p,q) = W_single(p[1],q[1])⊗...⊗W_single(p[n-1],q[n-1])
# where p, q are length-n integer arrays, and n is the number of qudits
def W(p, q, d):
    p = np.asarray(p, dtype=int)
    q = np.asarray(q, dtype=int)
    if p.shape != q.shape:
        raise ValueError("p and q must have same shape")
    mats = [W_single(int(p[i]), int(q[i]), d) for i in range(p.size)]
    return reduce(np.kron, mats, np.array([[1]], dtype=np.complex128))

# compute all Pauli supports for a single-qudit gate M at once
# uses FFT for more efficient computation
def f_all_single(M):
    M = np.asarray(M)
    if M.ndim != 2 or M.shape[0] != M.shape[1]:
        raise ValueError("M must be a square (dxd) matrix")
    d = M.shape[0]
    omega = np.exp(2j * np.pi / d)
    inv_two = pow(2, -1, d)

    r = np.arange(d)
    p = np.arange(d)
    f = np.empty((d, d), dtype=np.complex128)

    for q in range(d):
        diag_q = M[r, (r-q) % d]
        F = np.fft.fft(diag_q)
        phase = omega ** ((inv_two * p * q) % d)
        f[:, q] = (phase * F) / d

    return f

# compute f_M on a n-dim gate with a particular Pauli basis element
def f(M, p, q, d):
    M = np.asarray(M, dtype=np.complex128)
    p = np.asarray(p, dtype=int)
    q = np.asarray(q, dtype=int)
    n = p.size
    return np.trace(W(-p, -q, d) @ M) / (d ** n)

# plot supports for single-qudit gate in phase space
def plot_supp(M, title=None, rel=1e-9, circ_size=255):
    f = f_all_single(M)
    d = f.shape[0]
    mag = np.abs(f)
    eps = rel * mag.max() if mag.size else 0.0
    mask = mag >= eps

    P, Q = np.meshgrid(np.arange(d), np.arange(d), indexing="ij")

    plt.figure()
    plt.scatter(P.flatten(), Q.flatten(), s=12)

    if np.any(mask):
        plt.scatter(P[mask], Q[mask], s=circ_size, facecolors=(1,0,0,0.25), edgecolors="red", linewidths=1.5)
        
    plt.xticks(range(d))
    plt.yticks(range(d))
    plt.xlim(-0.5, d - 0.5)
    plt.ylim(-0.5, d - 0.5)
    plt.gca().set_aspect("equal", adjustable="box")
    plt.xlabel("Z")
    plt.ylabel("X")
    if title:
        plt.title(title)
    plt.tight_layout()
    plt.show()
    
# example from paper
M = pauli_X(5, 2) + (3 * pauli_Z(5, 2) @ pauli_X(5)) - (pauli_Z(5, 3) @ pauli_X(5, 3)) 
plot_supp(M)
