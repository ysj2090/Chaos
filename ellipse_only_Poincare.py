import turtle as t
import random
import math as m
import matplotlib.pyplot as plt

def q_conjugate(q):
    w,x,y,z=q
    return (w,-x,-y,-z)

def q_mult(q1, q2):
    w1, x1, y1, z1 = q1
    w2, x2, y2, z2 = q2    
    w = w1 * w2 - x1 * x2 - y1 * y2 - z1 * z2
    x = w1 * x2 + x1 * w2 + y1 * z2 - z1 * y2
    y = w1 * y2 - x1 * z2 + y1 * w2 + z1 * x2 
    z = w1 * z2 + x1 * y2 - y1 * x2 + z1 * w2 
    return w, x, y, z

def qv_rot(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q_conjugate(q1))[1:]

def qv_reflect(q1, v1):
    q2 = (0.0,) + v1
    return q_mult(q_mult(q1, q2), q1)[1:]


def euler_to_quaternion(phi, theta, psi):
 
        qw = m.cos(phi/2) * m.cos(theta/2) * m.cos(psi/2) + m.sin(phi/2) * m.sin(theta/2) * m.sin(psi/2)
        qx = m.sin(phi/2) * m.cos(theta/2) * m.cos(psi/2) - m.cos(phi/2) * m.sin(theta/2) * m.sin(psi/2)
        qy = m.cos(phi/2) * m.sin(theta/2) * m.cos(psi/2) + m.sin(phi/2) * m.cos(theta/2) * m.sin(psi/2)
        qz = m.cos(phi/2) * m.cos(theta/2) * m.sin(psi/2) - m.sin(phi/2) * m.sin(theta/2) * m.cos(psi/2)
 
        return [qw, qx, qy, qz]

def quaternion_to_euler(w, x, y, z):
 
        t0 = 2 * (w * x + y * z)
        t1 = 1 - 2 * (x * x + y * y)
        X = m.atan2(t0, t1)
 
        t2 = 2 * (w * y - z * x)
        t2 = 1 if t2 > 1 else t2
        t2 = -1 if t2 < -1 else t2
        Y = m.asin(t2)
         
        t3 = 2 * (w * z + x * y)
        t4 = 1 - 2 * (y * y + z * z)
        Z = m.atan2(t3, t4)
 
        return X, Y, Z
    
def jump(pos):
    t.pu()
    t.goto(pos)
    t.pd()
    
def p_ellipse(a,b):
    t.ht()
    t.speed("fastest")
    rad=m.pi/180
    for i in range(361):
        x = a * m.cos(i * rad)
        y = b * m.sin(i * rad)
        if i == 0:
            jump((x,y))
        else:
            t.goto(x,y)
'''
#   mark positions around the ellipse
    for i in range(121):
        x = a * m.cos(3 * i * rad)
        y = b * m.sin(3 * i * rad)
        jump(win, (x,y))
        xdir=x/a**2
        ydir=y/b**2
        mag=m.sqrt(xdir**2+ydir**2)
        xdir/=mag
        ydir/=mag
        x=x-15*xdir
        y=y-15*ydir
        t.goto((x,y))
'''        
    
def next_move(a, b, xpos,ypos,xdir,ydir):
    ll=xpos*ydir-ypos*xdir
    theta=m.atan2(-xdir*b, ydir*a)
    delta=m.acos(ll/m.sqrt(a*a*ydir*ydir+b*b*xdir*xdir))
    x1=a*m.cos(theta-delta)
    y1=b*m.sin(theta-delta)
    x2=a*m.cos(theta+delta)
    y2=b*m.sin(theta+delta)
    dist1=m.sqrt((x2-x1)**2+(y2-y1)**2)
    dist2=m.sqrt((xpos-x1)**2+(ypos-y1)**2)
    if dist2 > dist1*0.001 :
        xnew=x1
        ynew=y1
        theta=theta-delta
        
    else :
        xnew=x2
        ynew=y2
        theta=theta+delta
    
    w=0.
    x=xnew/a**2
    y=ynew/b**2
    z=0.
    mag=m.sqrt(x**2+y**2)
    x/=mag
    y/=mag
    nn=(w,x,y,z)
# angle between normal and dirction cos
    if theta < 0 :
        theta=theta+2*m.pi
    prod=x*xdir+y*ydir
    phi=m.acos(abs(prod))
    if xdir*y > ydir*x :
        phi=-phi
    phi=phi+m.pi/2
    xdir,ydir,z=qv_reflect(nn,(xdir,ydir,0.))
    
    return xnew,ynew,xdir,ydir, theta, phi

def q_square(win, width, height):
    t.setworldcoordinates(0.,0., width, height)
    
#####################
    
eccentricity=0.9
#eccentricity=float(input('eccentricity?'))

phi=float(input('direction[0-180]?'))*m.pi/180.

aa=300
bb=aa*m.sqrt(1.-eccentricity**2)
#p_ellipse(p, aa,bb)
width=2*m.pi
height=m.pi
#q_square(q,width,height)
t.setworldcoordinates(0.,0., width, height)
t.ht()

xdir=m.cos(2*m.pi*phi)
ydir=m.sin(2*m.pi*phi)
xpos=0.
ypos=0.

theta=0.
phi=0.

nmax=500
for i in range(nmax):
    print(i)
    xpos,ypos,xdir,ydir, theta, phi=next_move(aa, bb, xpos,ypos,xdir,ydir)
    jump((theta,phi))
    t.dot(3)








