from socket import *
import time
import datetime
import struct,os,sys
import select
import termios
import ephem
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import string


getlocal = ephem.Observer()
getlocal.long, getlocal.lat = '116.97345','40.55666' # at Miyun


# First set up the figure, the axis, and the plot element we want to animate  
fig = plt.figure()  
ax = plt.axes(xlim=(0, 360), ylim=(-90, 90),axisbg='#000000')  
line, = ax.plot([], [], 'yo')  
line2, = ax.plot([], [], 'r>')  
line3, = ax.plot([], [], color='green',ls='*',marker='.',markersize=3)  
line4, = ax.plot([], [], color='red',marker='*',markersize=20)  
line5, = ax.plot([], [], 'r-')  
line6, = ax.plot([], [], color='yellow',ls='*',marker='.',markersize=3)  
line7, = ax.plot([], [], 'ro')  

flag=0
convert=np.pi/180.0

  
# initialization function: plot the background of each frame  
def init():  
    line.set_data([], [])  
    return line, 
def azalt(ra,dec,ct3):
    global convert
    getlocal.date = ct3 # UT
    body = ephem.FixedBody()
    body._ra = ra*convert
    body._dec = dec*convert
    body._epoch = ephem.J2000
    body.compute(getlocal)
    x= float(body.az)*180/np.pi
    y= float(body.alt)*180/np.pi
    return x,y

def azalt_of_mw(ct3):
    mwx = range(0,360,5)
    mwy = range(0,360,5)
    j=0
    global convert
    for i in mwx:
        body_gl=i*convert
        body_gb=0*convert
        galactic_coord = ephem.Galactic(body_gl, body_gb)
        eq = ephem.Equatorial(galactic_coord)
   
        getlocal = ephem.Observer()
        getlocal.long, getlocal.lat = '116.97345','40.55666' # at Miyun
        getlocal.date = ct3 # UT
   
        body = ephem.FixedBody()
        body._ra = eq.ra
        body._dec = eq.dec
        body._epoch = ephem.J2000
        body.compute(getlocal)
        mwx[j]=float(body.az)*180/np.pi
        mwy[j]=float(body.alt)*180/np.pi
        j=j+1
    return mwx,mwy

def azalt_of_eq(ct3):
    eqx = range(0,360,5)
    eqy = range(0,360,5)
    j=0
    global convert
    for i in eqx:
        body = ephem.FixedBody()
        body._ra = i*convert
        body._dec = 0.0*convert
        body._epoch = ephem.J2000
        body.compute(getlocal)
        eqx[j]=float(body.az)*180/np.pi
        eqy[j]=float(body.alt)*180/np.pi
        j=j+1
    return eqx,eqy

def gc2azalt(gl,gb,ct3):
    global convert
    body_gl=gl*convert
    body_gb=gb*convert
    galactic_coord = ephem.Galactic(body_gl, body_gb)
    eq = ephem.Equatorial(galactic_coord)
   
    getlocal = ephem.Observer()
    getlocal.long, getlocal.lat = '116.97345','40.55666' # at Miyun
    getlocal.date = ct3 # UT
   
    body = ephem.FixedBody()
    body._ra = eq.ra
    body._dec = eq.dec
    body._epoch = ephem.J2000
    body.compute(getlocal)
    return float(body.az)*180/np.pi,float(body.alt)*180/np.pi


def kbhit():
    fd = sys.stdin.fileno()
    r = select.select([sys.stdin],[],[],0.01)
    rcode = ''
    if len(r[0]) >0:
        rcode  = sys.stdin.read(1)
    return rcode
  
# animation function.  This is called sequentially  
# note: i is framenumber  
def animate(i):  
    global flag
    global convert
    x = np.random.rand(8)
    y = np.random.rand(8)
    ct = time.gmtime()
    ct2 = time.strftime("%Y/%m/%d",ct)
    ct3 = time.strftime("%Y/%m/%d %H:%M:%S",ct)

    sat = ephem.Saturn(ct2)
    jup = ephem.Jupiter(ct2)
    mar = ephem.Mars(ct2)
    ven = ephem.Venus(ct2)
    sun = ephem.Sun(ct3)
    ura = ephem.Uranus(ct3)
    nep = ephem.Neptune(ct3)
    mon = ephem.Moon(ct3)

    getlocal.date = ct3 # UT
    body = ephem.FixedBody()
    body._ra = sun.ra
    body._dec = sun.dec
    body._epoch = ephem.J2000
    body.compute(getlocal)
    x[0]= float(body.az)*180/np.pi
    y[0]= float(body.alt)*180/np.pi
#    x[0],y[0]=azalt(sun.ra/convert,sun.dec/convert,ct3)
    #print ct3,sun.name, x[0],y[0]
    x[1],y[1]=azalt(sat.ra/convert,sat.dec/convert,ct3)
    #print ct3,sat.name, x[1],y[1]
    x[2],y[2]=azalt(jup.ra/convert,jup.dec/convert,ct3)
    #print ct3,jup.name, x[2],y[2]
    x[3],y[3]=azalt(mar.ra/convert,mar.dec/convert,ct3)
    #print ct3,mar.name, x[3],y[3]
    x[4],y[4]=azalt(ven.ra/convert,ven.dec/convert,ct3)
    #print ct3,ven.name, x[4],y[4]
    x[5],y[5]=azalt(ura.ra/convert,ura.dec/convert,ct3)
    #print ct3,ura.name, x[5],y[5]
    x[6],y[6]=azalt(nep.ra/convert,nep.dec/convert,ct3)
    #print ct3,nep.name, x[6],y[6]
    x[7],y[7]=azalt(mon.ra/convert,mon.dec/convert,ct3)
    #print ct3,mon.name, x[7],y[7]
    #print ct3,mon.name, mon.ra/convert, mon.dec/convert
    
    line.set_data(x, y)  
    line2.set_data(x, y+10)  
    mwx,mwy = azalt_of_mw(ct3)
    line3.set_data(mwx,mwy)
    gcx,gcy=gc2azalt(0,0,ct3)
    line4.set_data(gcx,gcy)
    groundx=[0,360]
    groundy=[0,0]
    line5.set_data(groundx,groundy)
    eqx,eqy = azalt_of_eq(ct3)
    line6.set_data(eqx,eqy)
    time_text = ax.text(x[0],y[0]+5,'Sun',color='green')
    time_text2 = ax.text(x[1],y[1]+5,'Saturn',color='green')
    time_text3 = ax.text(x[2],y[2]+5,'Jupiter',color='green')
    time_text4 = ax.text(x[3],y[3]+5,'Mars',color='green')
    time_text5 = ax.text(x[4],y[4]+5,'Venus',color='green')
    time_text6 = ax.text(x[5],y[5]+5,'Uranus',color='green')
    time_text7 = ax.text(x[6],y[6]+5,'Neptune',color='green')
    time_text8 = ax.text(x[7],y[7]+5,'Moon',color='green')
    time_text9 = ax.text(gcx,gcy+5,'GC',color='green')


#    c = kbhit()
#    if len(c) !=0 :
    catfile=open('catalog.txt')
    id=[]
    catra=[]
    catdec=[]
    catx=[]
    caty=[]
    for txtline in catfile:
        id,rad,ram,ras,decd,decm,decs=txtline.split(' ')
        catra=(string.atof(rad)+string.atof(ram)/60+string.atof(ras)/3600)*15.0
        catdec=string.atof(decd)+string.atof(decm)/60+string.atof(decs)/3600
        tempx,tempy=azalt(catra,catdec,ct3)
        catx.extend([tempx])
        caty.extend([tempy])
#    print catx,caty
    line7.set_data(catx,caty)
    flag=1
#    rad,ram,ras,decd,decm,decs = np.loadtxt('catalog.txt',unpack=True,usecols=[1,2,3,4,5,6])
#    print rad

    return line,line2,line3,line4,line5,line6,line7,time_text,time_text2,time_text3,time_text4,time_text5,time_text6,time_text7,time_text8,time_text9

  
# call the animator.  blit=True means only re-draw the parts that have changed.  
#anim = animation.FuncAnimation(fig, animate, init_func=init,  
#                               frames=200, interval=2000, blit=True)  
anim = animation.FuncAnimation(fig, animate, init_func=init,  
                                interval=2000, blit=True)  
  
#anim.save('basic_animation.mp4', fps=30, extra_args=['-vcodec', 'libx264'])  
  
plt.show()

