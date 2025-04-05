import os
#import argparse
import re
import sys


def charge(atom):
  global ato
  if "H" in atom:
    ato=1
  if "C" in atom:
    ato=6   
  if "N" in atom:
    ato=7
  if "O" in atom:
    ato=8
  if "F" in atom:
    ato=9
#  print (ato,eoe)
  return  ato  


                                                                        
rf=open("structures.txt",'r')
lines=rf.readlines()
rf.close()

nrow=1000
max0=23
max00=max0*max0

mxyz=[[0 for col in range(4)] for row in range(30)]
minput=[[0 for col in range(30)] for row in range(30)] 
mlin=[[0 for col in range(max00)] for row in range(nrow)]

men=[0 for row in range(nrow)]

idx=0

for row in range (nrow):
   idx=idx+2
   print ("line",idx,lines[idx])
   num0=int(lines[idx].split()[0])    
   print(num0)
   if num0 > max0:
      max0=num0
 
   idx=idx+1
   for matom in range(num0):
    idx=idx+1 
    linec=lines[idx]  
    print (linec)                     
    atom=str(linec.split()[0])     # atomatic name
    ato=charge(atom) 
    mxyz[matom][0]=float(linec.split()[1])      # x
    mxyz[matom][1]=float(linec.split()[2])       # y
    mxyz[matom][2]=float(linec.split()[3])       # z  
    mxyz[matom][3]=int(ato)  # nuclear charge

   for mx in range (num0):
#    print ("*****************")  
#    print (mxyz[mx][0],mxyz[mx][1],mxyz[mx][2],mxyz[mx][3])
     for my in range (num0):
#      print (mxyz[my][0],mxyz[my][1],mxyz[my][2],mxyz[my][3])
      if (mx != my):    
        disx2=(mxyz[mx][0]-mxyz[my][0])**2
        disy2=(mxyz[mx][1]-mxyz[my][1])**2
        disz2=(mxyz[mx][2]-mxyz[my][2])**2
        dis=(disx2+disy2+disz2)**0.5
        pop=mxyz[mx][3]*mxyz[my][3]
        minput[mx][my]=pop/dis
      if (mx == my):  
        minput[mx][my]=0.5*mxyz[my][3]**2.4
#      fw.write("%i  %i  %.10f\n"%(mx,my,minput[mx][my]))   

   for mx in range (num0):
    for my in range (num0):        
      mxy=mx*max0+my
#      print (mxy) 
      mlin[row][mxy]=minput[mx][my]

##################################################################
  
############# read the energy##################   

eng=open("PBE0energies.txt",'r')
leng=eng.readlines()
eng.close()

for idx in range (100):
   pbe=float(leng[idx+1].split()[0])  
   men[idx]=pbe

###########################################################
from sklearn.kernel_ridge import KernelRidge


y = men
X = mlin

clf = KernelRidge(alpha=1.0)
clf.fit(X, y)
#print (y)
KernelRidge(alpha=1.0)

print ('score',clf.score(X,y))

y1=clf.predict(X)
  
 
mae=0
for mx in range (0,nrow):
   mae=mae+abs(y1[mx][0]-y[mx][0])

print (mae/nrow)     
     

