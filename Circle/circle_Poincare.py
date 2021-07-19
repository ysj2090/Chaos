from turtle import TurtleScreen, RawTurtle, TK
import math as m
import matplotlib.pyplot as plt
import time 

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

def write_dots(win,xpos,ypos,xdir,ydir,nside) :
# xposition is distance along the sides 
    theta=m.atan2(ypos,xpos)
    if theta < 0. :
        theta += 2*m.pi
    iside=int(theta*nside/(2*m.pi))
    delta=m.pi*(2*iside+1)/nside
    norm_x=m.cos(delta)
    norm_y=m.sin(delta)
    # angle between n vector and position vector
    prod=(norm_x*m.sin(theta)-norm_y*m.cos(theta))
    phi=m.asin(prod)
    xx=(m.tan(phi)/m.tan(m.pi/nside)+1.)/2.
    prod=-norm_x*ydir+norm_y*xdir   # angle between -n vector and dir vector.
    phi=m.asin(prod)+m.pi/2
    jump(win,(xx,phi))
    win.dot(3)
    
def write_dots_old(win,xpos,ypos,xdir,ydir,nside) :
# xposition is transformed to angle theta
    theta=m.atan2(ypos,xpos)
    if theta < 0. :
        theta += 2*m.pi
    iside=int(theta*nside/(2*m.pi))
    delta=m.pi*(2*iside+1)/nside
    norm_x=-m.cos(delta)
    norm_y=-m.sin(delta)
    prod=(norm_x*xdir+norm_y*ydir)
    phi=m.acos(abs(prod))
    if xdir*norm_y > ydir*norm_x :
        phi=-phi
    phi=phi+m.pi/2
    jump(win,(theta,phi))
    win.dot(3)

def set_grid(win,width, height):
    win.ht()
    nxstp=20
    nystp=12
    
    xstp=width/nxstp
    ystp=height/nystp
    xvalstp=0.05
    yvalstp=180/nystp
    
    win.home()
    win.forward(width)
    win.lt(90)
    win.forward(height)
    win.lt(90)
    win.forward(width)
    win.lt(90)
    win.forward(height)

    xpos=0.
    ypos=0.
    xmag=width/40.
    ymag=height/40.
    for i in range(nxstp+1):
        jump(win,(xpos, ypos))
        win.setheading(-90)
        if (i%2 == 0) :
            win.forward(ymag)
            jump(win,(xpos, ypos-3.3*ymag))
            val=i*xvalstp
            win.write(str(val)[0:3],
                     align="center", font=("Courier", 14, "bold"))
        else :
            win.forward(0.6*ymag)
        xpos+=xstp

    xpos=width
    ypos=0.
    val=0.
    for i in range(nystp+1):
        jump(win,(xpos, ypos))
        win.setheading(0)
        if (i%3 == 0) :
            win.forward(xmag)
        else :
            win.forward(0.6*xmag)
        ypos+=ystp

    xpos=0.
    ypos=height
    for i in range(nxstp+1):
        jump(win,(xpos, ypos))
        win.setheading(90)
        if (i%2 == 0) :
            win.forward(ymag)
        else :
            win.forward(0.6*ymag)
        xpos+=xstp

    xpos=0.
    ypos=0.
    val=0.
    for i in range(nystp+1):
        jump(win,(xpos, ypos))
        win.setheading(180)
        if (i%3 == 0) :
            win.forward(xmag)
            jump(win,(xpos-2.5*xmag, ypos-1.3*ymag))
            val=i*yvalstp
            win.write(str(int(val)),
                     align="center", font=("Courier", 14, "bold"))
        else :
            win.forward(0.6*xmag)
        ypos+=ystp

def doSomething(event):
    print("Mouse coordinates: "+str(event.x)+","+str(event.y))
    print("Mouse coordinates: "+str(event.xdata)+","+str(event.ydata))
    # print("subwindow=",event.S)
        

#####################
# open two windows
root = TK.Tk()
cv1 = TK.Canvas(root, width=700, height=500, bg="#ddffff")
cv2 = TK.Canvas(root, width=700, height=500, bg="#ffeeee")
cv1.pack()
cv2.pack()

root.bind("<Button-1>",doSomething)

s1 = TurtleScreen(cv1)
s1.bgcolor(0.85, 0.85, 1)
s2 = TurtleScreen(cv2)
s2.bgcolor(1, 0.85, 0.85)

p = RawTurtle(s1)
q = RawTurtle(s2)

p.color("red", (1, 0.85, 0.85))
q.color("blue", (0.85, 0.85, 1))

width=1.
height=m.pi
xoffset=0.1*width
yoffset=0.2*height
s2.setworldcoordinates(-xoffset, -yoffset, width+0.5*xoffset, height+0.5*yoffset)
set_grid(q,width,height)

p.ht()
q.ht()

r1=200.
p.home()
p.dot(4)
jump(p, (r1,0))
p.lt(90.)
p.circle(r1)
p.pu()

nside=10
bb=250.
aside=2.*bb*m.tan(m.pi/nside)
r2=bb/m.cos(m.pi/nside)

jump(q,(0.5,3.22))
q.write(str(nside)+', '+str(int(r1))+', '+str(int(bb)),
                     align="center", font=("Courier", 14, "bold"))
time_label = TK.Label(cv2, font=("Arial", 10), bg="#ffeeee")
time_label.place(x=500, y=8)
time_string = time.strftime("%I:%M:%S %p %B %d, %Y")
time_label.config(text=time_string)

p.home()
#t.setheading(90.)
p.lt(90.*(nside+2)/nside)
jump(p, (r2,0))
for i in range(nside) :
    p.forward(aside)
    p.lt(360./nside)

print('asin(r1/bb)=%.2f' %(m.asin(r1/bb)*180./m.pi))
print('half angle= %.2f' %(90.*(nside-2)/nside))

# initial position and direction
theta=m.pi/nside
#theta=float(input('position[0-180]?'))*m.pi/180.
xpos=bb*m.cos(theta)
ypos=bb*m.sin(theta)
jump(p, (xpos,ypos))

phi=float(input('direction[0-180]?'))*m.pi/180.
phi=m.pi/2+theta+phi
xdir=m.cos(phi)
ydir=m.sin(phi)

nmax=16000
pmax=200
for i in range(nmax):
    print(i, end=' ')
    if abs(xpos*ydir-ypos*xdir) < r1 :
        xpos,ypos,xdir,ydir=to_circle(r1, xpos,ypos,xdir,ydir)
        if i < pmax :
            p.goto(xpos,ypos)
        xpos,ypos,xdir,ydir=from_circle(r2, xpos,ypos,xdir,ydir,nside)
        if i < pmax :
            p.goto(xpos,ypos)
        write_dots(q,xpos,ypos,xdir,ydir,nside)
    else :
        xpos,ypos,xdir,ydir=polygons(r2, xpos,ypos,xdir,ydir,nside)
        if i < pmax :
            p.goto(xpos,ypos)
        write_dots(q,xpos,ypos,xdir,ydir,nside)
        

    
