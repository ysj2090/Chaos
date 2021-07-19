import turtle as t
import math as m

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
    
def jump(win, pos):
    win.pu()
    win.goto(pos)
    win.pd()

def to_circle(rr, xpos,ypos,xdir,ydir):
    ll=xpos*ydir-ypos*xdir
    theta=m.atan2(-xdir, ydir)
    delta=m.acos(ll/rr)
    x1=rr*m.cos(theta-delta)
    y1=rr*m.sin(theta-delta)
    x2=rr*m.cos(theta+delta)
    y2=rr*m.sin(theta+delta)
    dist1=m.sqrt((x1-xpos)**2+(y1-ypos)**2)
    dist2=m.sqrt((x2-xpos)**2+(y2-ypos)**2)
        
    if dist2 > dist1 :
        xnew=x1
        ynew=y1
        theta=theta-delta
        
    else :
        xnew=x2
        ynew=y2
        theta=theta+delta
    
    w=0.
    x=m.cos(theta)
    y=m.sin(theta)
    z=0.
    nn=(w,x,y,z)
    xdir,ydir,z=qv_reflect(nn,(xdir,ydir,0.))
    
    return xnew,ynew,xdir,ydir

def from_circle(rr, xpos,ypos,xdir,ydir,nside):
    ll=xpos*ydir-ypos*xdir
    theta=m.atan2(-xdir, ydir)
    delta=m.acos(ll/rr)
    x1=rr*m.cos(theta-delta)
    y1=rr*m.sin(theta-delta)
    x2=rr*m.cos(theta+delta)
    y2=rr*m.sin(theta+delta)
    dist1=m.sqrt((x1-xpos)**2+(y1-ypos)**2)
    dist2=m.sqrt((x2-xpos)**2+(y2-ypos)**2)
        
    if dist2 > dist1 :
        xnew=x1
        ynew=y1
        theta=theta-delta
        
    else :
        xnew=x2
        ynew=y2
        theta=theta+delta

    if theta < 0 :
        theta=theta+2*m.pi
        
    iside=int(theta*nside/(2*m.pi))
    delta=m.pi*(2*iside+1)/nside

    w=0.
    x=m.cos(delta)
    y=m.sin(delta)
    z=0.

    nn=(w,x,y,z)
    xdir0,ydir0,z=qv_reflect(nn,(xdir,ydir,0.))
#    xdir,ydir,z=qv_reflect(nn,(xdir,ydir,0.))
# intersecting point of two lines
# first line normal nn, with a point on the circle
# second line direction (xdir, ydir) with a point (xpos,ypos)
    delta=2*iside*m.pi/nside
    x1=rr*m.cos(delta)
    y1=rr*m.sin(delta)
    
    dist1=x*x1+y*y1
    dist2=ydir*xpos-xdir*ypos
    w=x*xdir+y*ydir
    xnew=(xdir*dist1+y*dist2)/w
    ynew=(ydir*dist1-x*dist2)/w
    
    return xnew,ynew,xdir0,ydir0

def polygons(rr, xpos,ypos,xdir,ydir,nside):
    theta_0=m.atan2(ypos,xpos)
    if theta_0 < 0. :
        theta_0 += 2*m.pi
    kside=int(theta_0*nside/(2*m.pi))
    
    ll=xpos*ydir-ypos*xdir
    theta=m.atan2(-xdir, ydir)
    delta=m.acos(ll/rr)
    theta1=theta-delta
    if theta1 < 0. :
        theta1+=2*m.pi
    iside=int(theta1*nside/(2*m.pi))
    if iside == kside :
        theta1=theta+delta
        if theta1 < 0. :
            theta1+=2*m.pi
        iside=int(theta1*nside/(2*m.pi))

    delta=m.pi*(2*iside+1)/nside
    w=0.
    x=m.cos(delta)
    y=m.sin(delta)
    z=0.

    nn=(w,x,y,z)
    xdir0,ydir0,z=qv_reflect(nn,(xdir,ydir,0.))
    
#    xdir,ydir,z=qv_reflect(nn,(xdir,ydir,0.))
# intersecting point of two lines
# first line normal nn, with a point on the circle
# second line direction (xdir, ydir) with a point (xpos,ypos)
    delta=2*iside*m.pi/nside
    x1=rr*m.cos(delta)
    y1=rr*m.sin(delta)
    
    dist1=x*x1+y*y1
    dist2=ydir*xpos-xdir*ypos
    w=x*xdir+y*ydir
    xnew=(xdir*dist1+y*dist2)/w
    ynew=(ydir*dist1-x*dist2)/w
    
    return xnew,ynew,xdir0,ydir0


t.ht()
r1=100.
t.home()
t.dot(4)
jump(t, (r1,0))
t.lt(90.)
t.circle(r1)
t.pu()

nside=7
bb=200.
aside=2.*bb*m.tan(m.pi/nside)
r2=bb/m.cos(m.pi/nside)
t.home()
#t.setheading(90.)
t.lt(90.*(nside+2)/nside)
jump(t, (r2,0))
for i in range(nside) :
    t.forward(aside)
    t.lt(360./nside)

# initial position and direction
theta=-90.*m.pi/180.
#theta=float(input('position[0-180]?'))*m.pi/180.
xpos=r2*m.cos(theta)
ypos=r2*m.sin(theta)
jump(t, (xpos,ypos))

phi=float(input('direction[0-180]?'))*m.pi/180.
xdir=m.cos(phi)
ydir=m.sin(phi)

nmax=800
for i in range(nmax):
    print(i, end=' ')
    if abs(xpos*ydir-ypos*xdir) < r1 :
        xpos,ypos,xdir,ydir=to_circle(r1, xpos,ypos,xdir,ydir)
        t.goto(xpos,ypos)
        xpos,ypos,xdir,ydir=from_circle(r2, xpos,ypos,xdir,ydir,nside)
        t.goto(xpos,ypos)
    else :
        xpos,ypos,xdir,ydir=polygons(r2, xpos,ypos,xdir,ydir,nside)
        t.goto(xpos,ypos)
        

    
