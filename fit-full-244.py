import pandas as pd
import ezodf
import sys
import numpy
import operator
import math
import os

doc = ezodf.opendoc('file3.ods')

print("Spreadsheet contains %d sheet(s)." % len(doc.sheets))

sheet=doc.sheets[0]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )


sheet.head()

sys.exit()

nrow=237
npr=52

# z0 is the matrix for read the old_dev and new_dev 
z0=[[0 for row in range(2)] for col in range(nrow)]

#z is the matrix for the parameter (238 molecule and 51 parameter)
z=[[0 for row in range(npr)] for col in range(nrow)]


# below is the program to read the parameters form the sheet  

sheet=doc.sheets[0]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )

nb=1
# for row (3,27)
for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,21):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col-4]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 
    print (sheet[row,1].value)  
    print (z0[row-1][0],z0[row-1][1])
    print (z[row-1][0],z[row-nb][1],z[row-nb][2],z[row-nb][3],z[row-nb][4],z[row-nb][5])
    print (z[row-1][6],z[row-nb][7],z[row-nb][8],z[row-nb][9],z[row-nb][10],z[row-nb][11])
    print (z[row-1][12],z[row-nb][13],z[row-nb][14],z[row-nb][15],z[row-nb][16])
#num=row-2
#print (num)

#sys.exit()


nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[1]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,12):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+13]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][17],z[row-nb][18],z[row-nb][19],z[row-nb][20],z[row-nb][21],z[row-nb][22],z[row-nb][23],z[row-nb][24])

#sys.exit()


nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[2]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,9):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+21]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][25],z[row-nb][26],z[row-nb][27],z[row-nb][28],z[row-nb][29])



nb=nb-sheet.nrows()+1
print (nb)
#sys.exit()
sheet=doc.sheets[3]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,10):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][5]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][5])


nb=nb-sheet.nrows()+1
print (nb)
#sys.exit()
sheet=doc.sheets[4]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+26]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][30],z[row-nb][31])


nb=nb-sheet.nrows()+1
print (nb)
#sys.exit()
sheet=doc.sheets[5]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,5):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][5]=cell.value

    for col in range(5,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][9]=cell.value     


    for col in range(6,10):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+26]=cell.value
 

    for col in range(10,11):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+40]=cell.value


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][5],z[row-nb][9],z[row-nb][32],z[row-nb][33],z[row-nb][34],z[row-nb][35],z[row-nb][50])

#sys.exit()

nb=nb-sheet.nrows()+1
print (nb)
#sys.exit()
sheet=doc.sheets[6]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
#sys.exit()

for row in range(1,sheet.nrows()):
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,5):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][5]=cell.value

    for col in range(5,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+9]=cell.value


    for col in range(7,9):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+16]=cell.value 

    
    for col in range(9,11):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+39]=cell.value 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][5],z[row-nb][14],z[row-nb][15],z[row-nb][23],z[row-nb][24],z[row-nb][48],z[row-nb][49])

#sys.exit()

nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[7]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+10]=cell.value


    for col in range(6,8):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+17]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 


    for col in range(8,11):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+28]=cell.value  


    for col in range(11,13):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+37]=cell.value 

    for col in range(13,14):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][51]=cell.value

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][14],z[row-nb][15],z[row-nb][23],z[row-nb][24],z[row-nb][36],z[row-nb][37],z[row-nb][38],z[row-nb][48],z[row-nb][49],z[row-nb][51])

#sys.exit()

nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[8]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+33]=cell.value


    for col in range(7,9):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+7]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][37],z[row-nb][38],z[row-nb][39],z[row-nb][14],z[row-nb][15])


nb=nb-sheet.nrows()+1
print (nb)
sheet=doc.sheets[9]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+36]=cell.value

#        z[row-2][col-4].value=num 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][40],z[row-nb][41],z[row-nb][42])


#sys.exit()


nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[10]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,5):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][4]=cell.value

    for col in range(5,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][2]=cell.value


    for col in range(6,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][6]=cell.value 


    for col in range(7,9):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+16]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 

    for col in range(9,11):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+39]=cell.value
 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][4],z[row-nb][2],z[row-nb][6],z[row-nb][23],z[row-nb][24],z[row-nb][48],z[row-nb][49])

   
     

#sys.exit()


nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[11]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+39]=cell.value

#        z[row-2][col-4].value=num 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][43],z[row-nb][44])


nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[12]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,sheet.nrows()):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+41]=cell.value

#        z[row-2][col-4].value=num 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][45],z[row-nb][46],z[row-nb][47])

#sys.exit()

# in this sheet, two molecular GeH3 and AsH2 not read, since they are only dependent on RH and RA
nb=nb-sheet.nrows()+1
print (nb)

sheet=doc.sheets[13]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,3):
    print (row-nb)
    z0[row-nb][0]=sheet[row,2].value
    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,5):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][16]=cell.value

#        z[row-2][col-4].value=num 
    for col in range(5,7):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+43]=cell.value 


    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][16],z[row-nb][48],z[row-nb][49])



nb=nb-sheet.nrows()+3
print (nb)


# read information of C2, BN, LiN and BC
sheet=doc.sheets[14]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,3):
    print (row-nb)
#    z0[row-nb][0]=sheet[row,2].value
#    z0[row-nb][1]=sheet[row,3].value

    for col in range(4,6):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+10]=cell.value


    for col in range(6,8):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+17]=cell.value
#      if cell.value == None:
#        z[row-2][col-4].value=num 


    for col in range(8,11):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+28]=cell.value


    for col in range(11,13):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][col+37]=cell.value

    for col in range(13,14):
      cell = sheet[row,col]
      if cell.value != None:
        z[row-nb][29]=cell.value 

    print (sheet[row,1].value)
    print (z0[row-nb][0],z0[row-nb][1])
    print (z[row-nb][14],z[row-nb][15],z[row-nb][23],z[row-nb][24],z[row-nb][36],z[row-nb][37],z[row-nb][38],z[row-nb][48],z[row-nb][49],z[row-nb][29])




# up to here, all the parameters are in z 

#sys.exit()

#PZ old fitting parameter from G Li
# the old LOC from G-LI, used to test all the reading parameter as matrix z


#PZ=[[0 for row in range(1)] for col in range(npr)]
#CC=[[0 for row in range(1)] for col in range(nrow)]


#sheet=doc.sheets[15]
#print("   Sheet name : '%s'" % sheet.name)
#print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

#for row in range(1,sheet.nrows()):
#  PZ[row-1][0]=sheet[row,2].value    
#  print (PZ[row-1][0]) 

#z=numpy.matrix(z)
#PZ=numpy.matrix(PZ)
#CC=z*PZ

#aprint (CC)

# check the final LOC, whether it is same to the previous results, same means the reading are perfect
#fw = open('loc.dat','w')

#for row in range (0,nrow):
#    print (z0[row,0])
#    fw.write("%f\n" %(CC[row][0]))

#sys.exit()

# here CC is compared to the old obtained LOC, to make sure the whole sheet paremertes are read 

#b3lyp the value from DFT/b3lyp
#oldE old experiment from G Li
#newE the combined expeiment with Ben and James
#oldev and newdev indicting the deviation (oldE or newE minus b3lyp ) 

b3lyp=[[0 for row in range(1)] for col in range(nrow)]
oldE=[[0 for row in range(1)] for col in range(nrow)]
newE=[[0 for row in range(1)] for col in range(nrow)]
olddev=[[0 for row in range(1)] for col in range(nrow)]
newdev=[[0 for row in range(1)] for col in range(nrow)]


sheet=doc.sheets[16]
print("   Sheet name : '%s'" % sheet.name)
print("Size of Sheet : (rows=%d, cols=%d)" % (sheet.nrows(), sheet.ncols()) )
# for row (78,115)

for row in range(1,nrow+1):
  b3lyp[row-1][0]=sheet[row,1].value
  oldE[row-1][0]=sheet[row,2].value
  newE[row-1][0]=sheet[row,5].value
  olddev[row-1][0]=sheet[row,2].value-sheet[row,1].value
  newdev[row-1][0]=sheet[row,5].value-sheet[row,1].value


fw = open('dev.dat','w')

for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%f\n" %(olddev[row][0]))

fw.write("-----")


for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%f\n" %(newdev[row][0]))


#sys.exit()


# obtain the LOC part from  RH=0.023eV, RA=0.092eV, CT=0.222eV, designed by the former work  

RCT=[[0 for row in range(1)] for col in range(nrow)]



z=numpy.matrix(z)

for row in range(0,nrow):
#     print (z[row,48])
     sum0=z[row,48]*0.023
     sum0=sum0+z[row,49]*0.092
     sum0=sum0+z[row,50]*0.222
     RCT[row][0]=sum0


fw = open('rct.dat','w')

for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%f\n" %(RCT[row][0]))


#sys.exit()

# set the whole 238 test case (nrow=238)

n1=nrow


# remove the three pre-designed parameter RH,RA and CT from the 51 list
n2=npr-3

# use Y0, Y1, Y2 to copy matrix z 
Y0=[[0 for row in range(n2)] for col in range(n1)]
Y1=[[0 for row in range(n2)] for col in range(n1)]
Y2=[[0 for row in range(n2)] for col in range(n1)]


# the fitting program use formula:  A=BC  then C= ( B^T B -\lambda Unit ) ^(-1) B^T A    T the transfer matrix 
# here \lambda is set to zero
# B in AB=C is z, inputting parameter matrix 

#A and AI 
# here A is the matrix as ( B^T B -\lambda Unit ) with set \lambda=0
A=[[0 for row in range(n2)] for col in range(n2)]

# AI the inverse of A
AI=[[0 for row in range(n2)] for col in range(n2)]

# dev is the deviation matrix
dev=[[0 for row in range(1)] for col in range(n1)]

# P0 is the input matrix as A in AB=C, obtained with dev minus RCT 
P0=[[0 for row in range(1)] for col in range(n1)]

#C0 the fitting parameter as C in AB=C
C0=[[0 for row in range(1)] for col in range(n2)]

C4=[[0 for row in range(1)] for col in range(n1)]

#final LOC
LOC=[[0 for row in range(1)] for col in range(n1)]


for row in range (0,n1):
    for col in range (0,n2-1):
      Y0[row][col]=z[row,col]
      Y1[row][col]=z[row,col]
      Y2[row][col]=z[row,col]
    for col in range (n2-1,n2):
      Y0[row][col]=z[row,51]
      Y1[row][col]=z[row,51]
      Y2[row][col]=z[row,51]  

# using old dev or new dev (combined with ben's value)

for row in range (0,n1):
#   using G Li derivation
#    dev[row][0]=olddev[row][0]
#   using derivation + Ben Exp 
    dev[row][0]=newdev[row][0]

# obtain the new dev after minus the RCT
for row in range (0,n1):
    P0[row][0]=dev[row][0]-RCT[row][0]
#    P0[row][0]=newdev[row][0]-RCT[row][0]    



#print (P0)
Y0=numpy.matrix(Y0)
Y1=numpy.matrix(Y1)


A= Y0.T*Y1 #- I0

A=numpy.matrix(A)

#print (I0)
#print (A)

AI=A.I
#print (AI)
P0=numpy.matrix(P0)
AI=numpy.matrix(AI)
C0=numpy.matrix(C0)


# obtain the fitting parameters
C0=AI*Y1.T*P0

# obtain the LOC (C4)
C4=Y2*C0
C4=numpy.matrix(C4)


#parameter
fw = open('pra.dat','w')

for row in range (0,n2):
    fw.write("%.3f\n" %(C0[row][0]))

print ('------')

#final loc
#for row in range (0,n1):
#    print(C4[row,0])


# the obtained LOC(C4) plus RCT (RH, RA and CT) generating the final LOC
for row in range (0,n1):
    LOC[row][0]=C4[row,0]+RCT[row][0]

#write LOC
fw = open('loc.dat','w')

for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%.3f\n" %(LOC[row][0]))

fw.write('------final error\n')

# final error between the deviation and the LOC
for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%.3f\n" %(dev[row][0]-LOC[row][0]))


#write dev
fw = open('dev.dat','w')

for row in range (0,nrow):
#    print (z0[row,0])
    fw.write("%.2f\n" %(dev[row][0]))


#print ('------MAE')

#print ('------P0')
# for Mae

#print (C4)

def Mae(n3,n4):
#   d0=[[0 for row in range(1)] for col in range(n3,n4)]
#   print (C4)
    sum0=0
    sum1=0
    sum2=0
    n5=n4-n3
    for row in range (n3,n4):
      sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
      sum1=sum1+abs(C4[row,0]-P0[row][0])
      sum2=sum2+abs(dev[row][0])
#    print ("RMSE")
#    print (math.sqrt(sum0/n5))
    print ("MAE")
    print (abs(sum1/n5))
    print ("MAE of dev")
    print (abs(sum2/n5))
    print('------------')
    






Mae(0,25)
print('------------')
Mae(25,68)
print('------------')
Mae(68,106)
print('------------')
Mae(107,114)
print('------------')
Mae(114,127)
print('------------')
Mae(127,135)
print('------------')
Mae(135,198)
print('---------triplet ion')
Mae(194,198)
print('------------')
Mae(198,205)
print('------------')
Mae(205,215)
print('------------')
Mae(215,220)
print('------------')
Mae(220,233)
print('------------')

Mae(0,233)
print('------------')



sys.exit()


sum0=0
sum1=0
for row in range (0,25):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only single atom")
print (math.sqrt(sum0/25))
print ("MAE for only single atom")
print (abs(sum1/25))
print('------------')


sys.exit()

sum0=0
sum1=0
for row in range (25,68):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only single bond")
print (math.sqrt(sum0/43))
print ("MAE for only single bond")
print (abs(sum1/43))
print('------------')

sum0=0
sum1=0
for row in range (68,106):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only multi bond")
print (math.sqrt(sum0/38))
print ("MAE for only multi bond")
print (abs(sum1/38))
print('------------')

sum0=0
sum1=0
for row in range (107,115):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only multi bond")
print (math.sqrt(sum0/8))
print ("MAE for only multi bond")
print (abs(sum1/8))
print('------------')


sum0=0
sum1=0
for row in range (115,128):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only multi bond")
print (math.sqrt(sum0/13))
print ("MAE for only multi bond")
print (abs(sum1/13))
print('------------')


sum0=0
sum1=0
for row in range (128,136):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("RMSE for only multi bond")
print (math.sqrt(sum0/8))
print ("MAE for only multi bond")
print (abs(sum1/8))
print('------------')


sum0=0
sum1=0
for row in range (136,199):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
    
print ("RMSE for only radical")
print (math.sqrt(sum0/63))

print ("MAE for only radical")
print (abs(sum1/63))

print('------------')


sum0=0
sum1=0
for row in range (199,206):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])

print ("RMSE for only radical")
print (math.sqrt(sum0/59))

print ("MAE for only radical")
print (abs(sum1/59))

print('------------')

sum0=0
sum1=0
for row in range (206,216):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])

print ("RMSE for only radical")
print (math.sqrt(sum0/59))

print ("MAE for only radical")
print (abs(sum1/59))

print('------------')


sum0=0
sum1=0
for row in range (216,221):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])

print ("RMSE for only radical")
print (math.sqrt(sum0/59))

print ("MAE for only radical")
print (abs(sum1/59))

print('------------')


sum0=0
sum1=0
for row in range (221,234):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])

print ("RMSE for only radical")
print (math.sqrt(sum0/59))

print ("MAE for only radical")
print (abs(sum1/59))

print('------------')




sum0=0
sum1=0
for row in range (0,n1):
    sum0=sum0+(C4[row,0]-P0[row][0])*(C4[row,0]-P0[row][0])
    sum1=sum1+abs(C4[row,0]-P0[row][0])
print ("total RMSE with whole fitting")
print (math.sqrt(sum0/n1))

print ("total MAE")
print (abs(sum1/n1))


sum0=0
sum1=0
for row in range (0,n1):
    sum0=sum0+(newdev[row][0])**2
    sum1=sum1+abs(newdev[row][0])
print ("old RMSE without LOC")
print (math.sqrt(sum0/n1))
print ("old MAE without LOC")
print (abs(sum1/n1))



#check old MAE
#sum0=0
#for row in range (0,nrow):
#    sum0=sum0+(CC[row,0]-olddev[row][0])*(CC[row,0]-olddev[row][0])

#print ("old MAE")
#print (math.sqrt(sum0/nrow))


fw = open('p233.dat','w')
for row in range (0,nrow):
    for col in range (0,npr):
#     value=z[row,col]   
     fw.write("%d\n" %z[row,col])



#print (z0)


