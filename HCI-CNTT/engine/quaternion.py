"""CN-TT v4 — D=4 quaternion layer. Pure numpy, port-ready.
The improvement over the oracle: bearing/angular-velocity use the atan2-stable
form atan2(||a x b||, a.b) instead of arccos(clip(a.b))."""
from __future__ import annotations
import numpy as np

def qmul(a, b):
    w1,x1,y1,z1 = a; w2,x2,y2,z2 = b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2,
                     w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2,
                     w1*z2+x1*y2-y1*x2+z1*w2])

def qconj(q):
    return np.array([q[0], -q[1], -q[2], -q[3]])

def sandwich(q, v3):
    """Rotate a 3-vector v by unit quaternion q via q v q*  (exact SO(3) action)."""
    r = qmul(qmul(q, np.array([0.0, *v3])), qconj(q))
    return r[1:]

def angle_between(a, b):
    """atan2-stable angle between two 3-vectors (radians). Recovers ~8 digits
    near 0 and pi where arccos(clip(a.b)) collapses."""
    a = np.asarray(a, float); b = np.asarray(b, float)
    cross = np.linalg.norm(np.cross(a, b))
    dot = float(np.dot(a, b))
    return float(np.arctan2(cross, dot))

def unit_quaternion_from_axis_angle(axis, theta):
    axis = np.asarray(axis, float); axis = axis / np.linalg.norm(axis)
    return np.array([np.cos(theta/2.0), *(np.sin(theta/2.0)*axis)])
