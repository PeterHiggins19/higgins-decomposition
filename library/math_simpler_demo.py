#!/usr/bin/env python3
"""
"Math Hs makes simpler" -- the canonical receipted case: 3D rotation via Euler angles (taught first, complicated,
breaks at gimbal lock, does NOT compose by adding angles) vs the unit quaternion = the D=4 composition Hs reads
(exact, deterministic, one multiplication, never degenerates). Honest: quaternions-over-Euler is KNOWN math; the
contribution is the unifying 'a composition is a quaternion' framing + the deterministic engine.
Deterministic; hash-receipted. Author: Peter Higgins; AI-assisted per HUF-STD-001.
"""
import hashlib, json, math
import numpy as np

def Rx(a): c,s=math.cos(a),math.sin(a); return np.array([[1,0,0],[0,c,-s],[0,s,c]])
def Ry(a): c,s=math.cos(a),math.sin(a); return np.array([[c,0,s],[0,1,0],[-s,0,c]])
def Rz(a): c,s=math.cos(a),math.sin(a); return np.array([[c,-s,0],[s,c,0],[0,0,1]])
def euler_zyx(y,p,r): return Rz(y)@Ry(p)@Rx(r)

def quat_mul(a,b):
    w1,x1,y1,z1=a; w2,x2,y2,z2=b
    return np.array([w1*w2-x1*x2-y1*y2-z1*z2, w1*x2+x1*w2+y1*z2-z1*y2,
                     w1*y2-x1*z2+y1*w2+z1*x2, w1*z2+x1*y2-y1*x2+z1*w2])
def quat_from_euler_zyx(y,p,r):
    qz=np.array([math.cos(y/2),0,0,math.sin(y/2)]); qy=np.array([math.cos(p/2),0,math.sin(p/2),0])
    qx=np.array([math.cos(r/2),math.sin(r/2),0,0]); return quat_mul(quat_mul(qz,qy),qx)
def quat_to_R(q):
    w,x,y,z=q
    return np.array([[1-2*(y*y+z*z),2*(x*y-z*w),2*(x*z+y*w)],[2*(x*y+z*w),1-2*(x*x+z*z),2*(y*z-x*w)],
                     [2*(x*z-y*w),2*(y*z+x*w),1-2*(x*x+y*y)]])

def main():
    e1=np.array([0.7,0.4,0.9]); e2=np.array([0.3,0.8,0.5])
    R1=euler_zyx(*e1); R2=euler_zyx(*e2); R_true=R2@R1
    R_quat=quat_to_R(quat_mul(quat_from_euler_zyx(*e2),quat_from_euler_zyx(*e1)))
    R_euler_add=euler_zyx(*(e1+e2))
    gimbal=[{"pitch_deg":pd,"euler_map_|det|~cos":round(abs(math.cos(math.radians(pd))),5),
             "quaternion_map_degenerate":False} for pd in [0,60,85,89,89.9]]
    out={
     "case":"3D rotation: standard Euler angles vs the unit quaternion = the D=4 composition Hs reads",
     "composition_of_two_rotations":{
       "quaternion_q2*q1_error_vs_true":float(np.linalg.norm(R_quat-R_true)),
       "naive_euler_add_angles_error_vs_true":round(float(np.linalg.norm(R_euler_add-R_true)),4),
       "reading":"Quaternion composition is EXACT (~1e-16); 'add the Euler angles' is WRONG -- rotations do not compose by adding angle-triples; the quaternion route is one multiplication."},
     "gimbal_lock":{"euler_to_SO3_|det|_by_pitch":gimbal,
       "reading":"Euler->rotation loses a DOF as pitch->90deg (|det|->0); the quaternion map (S^3 double cover) is non-degenerate everywhere."},
     "the_Hs_framing":"Hs reads a 4-part composition AS a unit quaternion (the D=4 rung), so compositional change inherits exact, deterministic, singularity-free rotation arithmetic.",
     "honest_note":"Quaternions-over-Euler is KNOWN (Hamilton 1843; standard in graphics/robotics/aerospace). Contribution = the unifying 'a composition is a quaternion' framing + the deterministic, hash-receipted engine. Not a new theorem; a simpler, exact, auditable route."}
    out["content_sha256"]=hashlib.sha256(json.dumps(out,sort_keys=True,default=str).encode()).hexdigest()
    print(json.dumps(out,indent=2))

if __name__=="__main__":
    main()
