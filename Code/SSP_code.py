import time
import numpy as np
import pandas as pd
import xlwt
import copy
import random
from docplex.mp.model import Model
import math
##################################################stage-II######################################################
time0 = time.clock()

def data_write(file_path, datas):
    f = xlwt.Workbook()
    sheet1 = f.add_sheet(u'sheet1',cell_overwrite_ok=True) 
    i = 0
    for data in datas:
        for j in range(len(data)):
            sheet1.write(i,j,str(data[j])) 
        i = i + 1       
    f.save(file_path) 



#//////staffing requirements for intervals in 28 days for instance01/////////
require00 = ('[5     6     7     7     7     4     5     5     5     3     3     3     3     3     2],'
'[3     4     5     5     5     3     3     3     4     3     3     3     3     3     2],'
'[2	3	3	4	4	3	4	4	4	3	2	1	1	2   1],'
'[2	2	3	3	3	2	3	4	3	2	2	2	1	1   1],'
'[2	2	2	3	3	2	3	3	3	2	2	1	1	2   1],'
'[1	2	2	3	3	2	3	2	3	2	2	2	1	1   1],'
'[2     2     2     2     3     1     3     2     2     1     1     1     1     1     0],'
'[3     3     4     6     6     3     4     4     4     2     1     1     1     1     1],'
'[3     3     4     4     4     2     3     3     4     2     2     1     1     1     1],'
'[3     3     3     4     4     2     3     4     4     2     1     1     1     1     1],'
'[3     3     3     3     4     2     4     4     4     2     2     1     1     1     1],'
'[2     3     3     4     4     2     4     4     4     2     1     1     1     1     0],'
'[2     2     2     2     2     2     3     2     2     2     2     1     1     1     0],'
'[1     2     2     2     2     1     2     2     2     2     2     1     1     1     1],'
'[3     4     5     5     5     3     3     3     4     3     3     3     3     3     2],'
'[2	3	3	4	4	3	4	4	4	3	2	1	1	2   1],'
'[2	2	3	3	3	2	3	4	3	2	2	2	1	1   1],'
'[2	2	2	3	3	2	3	3	3	2	2	1	1	2   1],'
'[1	2	2	3	3	2	3	2	3	2	2	2	1	1   1],'
'[2     2     2     2     3     1     3     2     2     1     1     1     1     1     0],'
'[1     1     2     2     3     1     2     1     2     1     1     1     1     1     0],'
'[4     5     6     7     6     3     4     4     5     3     3     3     3     3     2],'
'[3	4	4	5	5	3	5	5	5	3	2	1	1	2   1],'
'[3	3	4	4	4	2	4	5	4	2	2	2	1	1   1],'
'[3	3	3	4	4	2	4	4	4	2	2	1	1	2   1],'
'[2	3	3	4	4	2	4	3	4	2	2	2	1	1   1],'
'[3     3     3     3     4     1     4     3     3     1     1     1     1     1     0],'
'[2     2     3     3     4     1     3     2     3     1     1     1     1     1     0]')
    
LB = 11 #the number of employees available



def requirezh(x):
    b = []
    b.append([])
    j = 0
    for i in range(len(x)-1):
#        if j == 17:
#           print(x[i])
        if (x[i] != " ") and (x[i] != "[") and (x[i] != "]") and (x[i] != ",") and (x[i] != "\t") and (x[i] != "/") and (x[i] != ";") and (x[i] != "a"):
            if (x[i+1] != " ") and (x[i+1] != "[") and (x[i+1] != "]") and (x[i+1] != ",") and (x[i+1] != "\t") and (x[i+1] != "/") and (x[i+1] != ";") and (x[i+1] != "a"):                 
                c = 10*int(x[i]) + int(x[i+1])
                b[j].append(c)
                s = list(x)
                s[i+1] = 'a'
                x = ''.join(s)
            if x[i+1] == "\t" or x[i+1] == "]" or x[i+1] == " ":
                b[j].append(int(x[i]))
        if (x[i] == ",") or (x[i] == ";"):
            j += 1
            b.append([])
    return(b)
                
       


require0 = requirezh(require00)

#if the shift can cover the period, it equals 1; otherwise 0.     
cover = [
[1,1,1,1,1,0,1,1,1,0,0,0,0,0,0],
[0,1,1,1,1,0,1,1,1,1,0,0,0,0,0],
[0,0,1,1,1,1,0,1,1,1,1,0,0,0,0],
[0,0,0,1,1,1,0,1,1,1,1,1,0,0,0],
[0,0,0,0,1,1,1,1,1,0,1,1,1,0,0],
[0,0,0,0,0,1,1,1,1,0,1,1,1,1,0],
[0,0,0,0,0,0,1,1,1,1,0,1,1,1,1],
[0,0,1,1,1,1,0,0,0,0,1,1,1,1,0],
[0,0,1,1,1,1,0,0,0,0,0,1,1,1,1],
[0,0,1,1,1,0,0,0,0,1,1,1,1,1,0],
[0,0,1,1,1,0,0,0,0,0,1,1,1,1,1]]




#judge whether all the staffing requirements are fully covered
def pdfg(x):
    numz = 0
    for i in range(len(x)):
        for j in range(len(x[0])):
            if require[i][j] > 0:
                 numz += 1
    return numz



#randomly generated off days in four weeks for one employee
def xj():
    xjsj = []
    a = np.random.choice([5,12,19,26])
    xjsj.extend([a,a+1])
    while xjsj[-2] >= 7:
        a = np.random.choice([a-8, a-7, a-6, a-5, a-4, a-2])
        if a != -1 and a!= 1:
            xjsj.extend([a,a+1])        
        if a == -1:
            xjsj.extend([0,1])            
        if a == 1:
            xjsj.extend([0,1,2])
    xjsj.sort() 
    while xjsj[-2] <= 19:
        a = xjsj[-2] 
        a = np.random.choice([a+8, a+7, a+6, a+5, a+4, a+2]) 
        if a != 27 and a!= 25:
            xjsj.extend([a,a+1]) 
        if a == 27:
            xjsj.extend([26,27])
        if a == 25:
            xjsj.extend([25,26,27])
    while len(xjsj) < 8:
        a = np.random.randint(0,27) 
        while (a in xjsj) or (a-3 in xjsj) or (a+3 in xjsj) or (a+1 in xjsj) or (a == 1) or (a == 25):
             a = np.random.randint(0,27) 
        xjsj.extend([a,a+1])
    xjsj.sort() 
    return xjsj



#randomly generated shift types in four weeks for one employee
def shiftset():
    a = []
    for i in range(4):
        b =  np.random.randint(0,11) 
        a.append(b)
    return a


#judge whether the chosen shift can cover the uncovered staffing requirements
def yxfg(a,d): 
    b = 0
    for i in range(4):
        c = a[i]
        for j in range(7*i,7*i+7):
            if j not in d:
                for k in range(15):
                    if(cover[c][k] == 1) and (require[j][k] > 0):
                        b += 1
    return b


#update the coverage of staffing requirements--add employees
def uprequire(a,b,c): 
    for i in range(len(cover[c])):
        if cover[c][i] == 1:
            a[b][i] -= 1
    return a


#re-organize schedule scheme
def pbfa(a):
    b = len(a)
    c = a[b-1][0]
    d = np.array([[-1 for i in range(len(require))] for j in range(c+1)]) 
    for i in range(len(a)):
        e = a[i][0]
        f = a[i][1]
        d[e][f] = a[i][2]
    return d


#check wether the schedule scheme corresponds to the coverage of staffing requirements
def check(a,b):
    e = 0
    for i in range(len(a)):        
        c = copy.deepcopy(cover)
        d = copy.deepcopy(require0)
        f = copy.deepcopy(a[i]) 
        g = copy.deepcopy(b[i])
        for j in range(len(f)):
            for k in range(28):
                if f[j][k] != -1:
                    h = f[j][k]
                    for m in range(15):
                        if c[h][m] == 1:
                            d[k][m] -= 1
        for j in range(28):
            for k in range(15):
                if g[j][k] != d[j][k]:
                    e = 1
    return e

#check wether the schedule scheme corresponds to the coverage of staffing requirements
def check1(a,b):
    e = 0
    c = copy.deepcopy(cover)
    d = copy.deepcopy(require0)
    f = copy.deepcopy(a)
    g = copy.deepcopy(b) 
    for j in range(len(f)):
        for k in range(28): 
            if f[j][k] != -1:
                h = f[j][k]
                for m in range(15):
                    if c[h][m] == 1:
                        d[k][m] -= 1
    for j in range(28):
        for k in range(15):
            if g[j][k] != d[j][k]:
                e = 1
    return e


#check wether all the staffing requirements are fully covered
def check2(a):
    b = 0
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] > 0:
                b += 1
    return(b)
    
    
#calculate the daily penalty of each employee in four weeks
def score(a):
    b = [[0 for i in range(28)]for j in range(len(a))]    
    for i in range(len(a)):
        k = 0
        for j in  range(28):
            if a[i][j] != -1:
                k +=1
        if k > 20:
            for j in range(28):
                if a[i][j] != -1:
                    b[i][j] += round((k-20)/k,3)
            
    for i in range(len(a)):
        k = []
        for j in range(28):
            if a[i][j] == -1:
                k.append(j) 
        l = []
        for j in k:
            if (j+1 in k):
                l.append(j)
        k0 = copy.deepcopy(k)
        for j in l:
            if j in k:
                k0.remove(j)
        if k0 == []:
            for j in range(28):
                b[i][j] += round(22/28,3)
        if k0 != []:
            x = 0
            for j in range(k0[0]):
                if a[i][j] != -1:
                    x += 1
            if x > 6:
                for j in range(k0[0]):
                    if a[i][j] != -1:
                        b[i][j] += round((x-6)/x,3)
            x = 0
            for j in range(k0[-1],28):
                if a[i][j] != -1:
                    x += 1
            if x > 6:
                for j in range(k0[-1],28):
                    if a[i][j] != -1:
                        b[i][j] += round((x-6)/x,3)
        if len(k0) >= 2:
            for j in range(1,len(k0)):     
                x = 0
                for q in range(k0[j-1]+1,k0[j]):      
                    if a[i][q] != -1:
                        x += 1
                if x > 6:
                    for q in range(k0[j-1]+1,k0[j]):
                        if a[i][q] != -1:
                            b[i][q] += round((x-6)/x,3)
    for i in range(len(a)):
        c = []

        for j in range(1,27):
            if (a[i][j-1] == -1) and (a[i][j] != -1) and (a[i][j+1] == -1):
                c.append(j)

        for j in c:
            for k in range(j-1,j+2):

                b[i][k] += 0.333
        if (a[i][0] != -1) and (a[i][1] == -1) and (a[i][2] == -1):
            b[i][0] += 0.5
            b[i][1] += 0.5
            
        if (a[i][25] == -1) and (a[i][26] == -1) and (a[i][27] != -1):
            b[i][26] += 0.5
            b[i][27] += 0.5
            
    for i in range(len(a)):
        c = []

        for j in range(1,27):
            if (a[i][j-1] != -1) and (a[i][j] == -1) and (a[i][j+1] != -1):
                c.append(j)


        for j in c:
            for k in range(j-1,j+2):
                b[i][k] += 0.333
                   
        if (a[i][0] == -1) and (a[i][1] != -1) and (a[i][2] != -1):
            b[i][0] += 0.5
            b[i][1] += 0.5
            
        if (a[i][25] != -1) and (a[i][26] != -1) and (a[i][27] == -1):
            b[i][26] += 0.5
            b[i][27] += 0.5



    for i in range(len(a)):
        c = 0
        for j in range(4):
            if (a[i][7*j+5] != -1) or (a[i][7*j+6] != -1):
                c += 1
        if c == 4:
            for j in range(4):
                if a[i][7*j+5] != -1 and a[i][7*j+6] != -1:
                    b[i][7*j+5] += 0.125
                    b[i][7*j+6] += 0.125
                if a[i][7*j+5] == -1 and a[i][7*j+6] != -1:
                    b[i][7*j+6] += 0.25
                if a[i][7*j+5] != -1 and a[i][7*j+6] == -1:
                    b[i][7*j+5] += 0.25    
     
    return b


#calculate the total penalty of each employee in four weeks
def totalscore(a): 
    b = 0
    for i in range(len(a)):
        for j in range(28):
            b += a[i][j]
    return b


fadict = {} #schedule schemes for all the food sources
requiredict = {} #the coverage of staffing requirements for all the food sources
N = 5 #the number of food sources
obj = [] #the objective values of food sources obtained by the algorithm in stage-I

####the process to generate initial food sources
for sn in range(N):
    enum = 0 
    xeds = []
    require = copy.deepcopy(require0)
    pd0 = pdfg(require) 
    while pd0 > 0:

        xjjh = []            
        xjjh = xj() 

        shiftsj = shiftset() 

        if yxfg(shiftsj,xjjh) > 0:
            for day in range(len(require)):
 
                if day not in xjjh:
                    xeds.append([enum, day, shiftsj[day//7]])

                    require = uprequire(require,day,shiftsj[day//7])

            enum += 1
        pd0 = pdfg(require)    
           
    fa = pbfa(xeds).tolist()          
            
  

 
    fadict[sn] = fa 

 
    requiredict[sn] = require 

    obj.append(len(fa))
    

minitial = 100000
for i in range(N):
    if obj[i] <= minitial:
        minitial = obj[i]

   
    
      
    
time1 = time.clock()-time0
print(time1)


print(check(fadict,requiredict))


fadict0 = copy.deepcopy(fadict)
requiredict0 = copy.deepcopy(requiredict)

##############################################################################################################

fadict = copy.deepcopy(fadict0)
requiredict = copy.deepcopy(requiredict0)

for sn in range(N):
    obj[sn] = len(fadict[sn])


#judge wether the employee can be off work on that day
def pddel(a,b,c,d):
    e = a[b][c]
    f = 0
    for i in range(15):
        if (cover[e][i] == 1) and (d[c][i] == 0):
            f += 1
    return f

#update the coverage of staffing requirements--remove employee
def uprequire1(a,b,c):
    for i in range(len(cover[c])):
        if cover[c][i] == 1:
            a[b][i] += 1
    return a    






#adjust scheme
def fadjust(a):
    b = len(a)
    c = [] 
    for i in range(4):
        c.append([])
        for j in range(b):
            d = 0
            for k in range(7*i,7*i+7):
                if (a[j][k] == -1):
                    d += 1
            if d == 7:
                c[i].append(j)

    d = list(set(c[0]) & set(c[1]) & set(c[2]) & set(c[3]))

    while d != []:
        y = d[0]

        del a[y]       
        b = len(a)
        c = []
        for i in range(4):
            c.append([])
            for j in range(b):
                d = 0
                for k in range(7*i,7*i+7):
                    if (a[j][k] == -1):
                        d += 1
                if d == 7:
                    c[i].append(j)


        d = list(set(c[0]) & set(c[1]) & set(c[2]) & set(c[3]))

    b = len(a)
    for i in range(4):
        c = []
        for j in range(b):
            for k in range(7*i,7*i+7):
                if a[j][k] != -1:
                    c.append(j)
                    break

        for j in range(b):
            d = 0
            for k in range(7*i,7*i+7):
                if (a[j][k] == -1):
                    d += 1
            if d == 7:
                if c[-1] > j:                   
                    e = c[-1]

                    for k in range(7*i,7*i+7):
                        a[j][k] = a[e][k]
                        a[e][k] = -1
                    del c[-1]
            if c == []:
                break                    

                    
    
    f = []
    for j in range(b):
        d = 0
        for i in range(4):
            for k in range(7*i,7*i+7):
                if a[j][k] == -1:
                    d += 1
        if d == 28:
            f.append(j)

   
    for j in range(len(f)-1,-1,-1):
        h = f[j]

        del a[h]              
    return a


#pick out employees with no assignment in one week
def noattenwork(a,b):
    c = []
    for i in range(len(a)):
        d = 0
        for j in range(7*b,7*b+7):
            if a[i][j] == -1:
                d += 1
        if d == 7:
            c.append(i)
    return c
               
#pick out employees with low attendance    
def lowattenwork(a):
    b = len(a)
    c = []
    f = []
    for i in range(b):
        d = 0
        for j in range(28):
            if a[i][j] != -1:
                d += 1
        c.append(d)
    for i in range(b):
        if c[i] < 20:
            f.append(i) 
    return f

#pick out employees with no attendance and off work on that day
def lowattennonwork(a,e): 
    b = len(a)
    c = []
    f = []
    g = []
    for i in range(b):
        d = 0
        for j in range(28):
            if a[i][j] != -1:
                d += 1
        c.append(d)
    for i in range(b):
        if c[i] < 20:
            f.append(i) 

    g = copy.deepcopy(f)

    for i in f:

        if a[i][e] != -1:
            g.remove(i)
    return g

#pick out employees with full attendance
def fullattenwork0(a): 
    b = len(a)
    c = []
    f = []
    for i in range(b):
        d = 0
        for j in range(28):
            if a[i][j] != -1:
                d += 1
        c.append(d)
    for i in range(b):
        if c[i] >= 20:
            f.append(i) 
    return f


#the shift type of an employee in one week
def shiftnum(a,b,c):
    d = b//7
    e = -1
    for i in range(7*d,7*d+7):
        if a[c][i] != -1:
            e = a[c][i]
            break
    return e


#judge wether shift c can convert into d
def pdshiftzh(a,b,c,d):
    e = 1
    for i in range(15):
        if (cover[c][i] == 1) and (cover[d][i] == 0) and (a[b][i] == 0):

            e = 0
            break
    return e


#the shift types involved in the weekly scheme
def workshift(a,b):
    c = []
    for i in range(len(a)):
        for j in range(7*b,7*b+7):
            if a[i][j] != -1:
                c.append(a[i][j])
                break

    c = list(set(c))
    return c

#pick out the intervals with the most and fewest redundancies
def requireminmaxp(a,b): 
    d = 0
    g = 0
    for i in range(7*a,7*a+7):
        d -= b[i][0]
        g -= b[i][0]
        e = 0
        f = 0
   
    for i in range(1,15):
        c = 0
        for j in range(7*a,7*a+7):
            c -= b[j][i]

        if c < d:
            d = c
            e = i
        if c >= g:
            g = c
            f = i
    return [e,f] 


#pick out the shifts that can cover interval a
def shiftminmaxp(a):
    b = []
    for i in range(len(cover)):
        if cover[i][a] == 1:
            b.append(i)
    return b

#calculate the intersection of two lists
def shiftjiaoji(a,b):
    c = []
    for i in a:
        if i in b:
            c.append(i)
    return c

#pick out employees that work for shift c on week b in the scheme a                
def shiftemployee(a,b,c):
    d = []
    for i in range(len(a)):
        for j in range(7*b,7*b+7):
            if a[i][j] == c:
                d.append(i)
                break
    return d

penaltyinifa = {}#schedule schemes for all the food sources in stage-II
penaltyinirequire = {}#the coverage of staffing requirements for all the food sources in stage-II
obj0 = [0 for i in range(N)] 
iteration = 0
recoper = {}
recoperyx = {}
first_time = time.time()
zuizhongobj = 1000000000000
reciterationobj = []
v = 1
nonoptiteration = 0
nonopt = [0 for i in range(N)]

recordtime = []

while ((time.time() - first_time <= 90) and (nonoptiteration <= 200)):
    print("第%d次迭代"%(iteration))
    recoper[iteration] = [0,0,0,0]
    recoperyx[iteration] = [0,0,0,0]
#################################################employed bee stage#####################################################
    for sn in range(N):

        #dynamic selection probability for neighborhood structures
        random01 = random.random()
        pro1 = 0.4 - 0.9*iteration/(600+iteration)  
        if random01 <= pro1:
            oper = 0
        else:
            oper = np.random.choice([1,2,3])

        recoper[iteration][oper] += 1

        #redundancy removal operator
        if oper == 0:
            judge = 0
            a0 = copy.deepcopy(fadict[sn])  
            b0 = copy.deepcopy(requiredict[sn]) 
   
            for weeknum in range(4):

                empnumsj = [i for i in range(len(fadict[sn]))]
                random.shuffle(empnumsj)
                for enum in empnumsj:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[enum][day] != -1:

                            if (pddel(a0,enum,day,b0) == 0):
                                uprequire1(b0,day,a0[enum][day])
                                a0[enum][day] = -1
                                judge = 1
        
            fadjust(a0)
            if judge == 1: 
                fadict[sn] = copy.deepcopy(a0)
                requiredict[sn] = copy.deepcopy(b0)
                obj[sn] = len(fadict[sn])
                recoperyx[iteration][oper] += 1
            else:
                nonopt[sn] += 1
        
        
        #shift fusion operator
        if oper == 1:
            judge = 0
            a0 = copy.deepcopy(fadict[sn])  
            b0 = copy.deepcopy(requiredict[sn])  

            if lowattenwork(a0) != []:
                e0 = np.random.choice(lowattenwork(a0))       
                weekset = [i for i in range(4)]
                random.shuffle(weekset)      
                for weeknum in weekset:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[e0][day] != -1:
                            s0 = a0[e0][day]

                            lowattennonworkset = lowattennonwork(a0,day)
                            random.shuffle(lowattennonworkset)

                            for enum in lowattennonworkset:
                                s1 = shiftnum(a0,day,enum)
                                if s1 == -1:
                                    a0[e0][day] = -1
                                    a0[enum][day] = s0
                                    judge = 1
                                    break                            
                                if s1 != -1:
                                    if pdshiftzh(b0,day,s0,s1) == 1:

                                        a0[e0][day] = -1
                                        a0[enum][day] = s1
                                        uprequire1(b0,day,s0)
                                        uprequire(b0,day,s1)
                                        judge = 1
                                        break

        
                fadjust(a0)
                if judge == 1: 
                    fadict[sn] = copy.deepcopy(a0)
                    requiredict[sn] = copy.deepcopy(b0)
                    obj[sn] = len(fadict[sn])
                    recoperyx[iteration][oper] += 1
                else:
                 nonopt[sn] += 1       
                    
        
        
        
        #redundancy balance operator
        if oper == 2:
            a0 = copy.deepcopy(fadict[sn]) 
            b0 = copy.deepcopy(requiredict[sn])
            judge = 0        
            for weeknum in range(4):
                workshiftset = workshift(a0,weeknum) 

                minmaxp = requireminmaxp(weeknum,b0) 
                minp = minmaxp[0] 
                maxp = minmaxp[1] 

                shift0 = shiftminmaxp(minp)

                shift1 = shiftminmaxp(maxp)

                kxshift1 = shiftjiaoji(shift1,workshiftset)

                if kxshift1 != []:
                    selectshift1 = np.random.choice(kxshift1)

                selectshift0 = np.random.choice(shift0)    

                kxemployee1 = shiftemployee(a0,weeknum,selectshift1)

                employee1 = np.random.choice(kxemployee1)

                workingdays = 0
                for day in range(7*weeknum,7*weeknum+7):
                    if a0[employee1][day] != -1:
                        workingdays += 1

                khworkingdays = 0
                for day in range(7*weeknum,7*weeknum+7):
                    if a0[employee1][day] != -1:

                        khworkingdays += pdshiftzh(b0,day,selectshift1,selectshift0)

                if workingdays == khworkingdays:

                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[employee1][day] != -1:

                            a0[employee1][day] = selectshift0
                            uprequire1(b0,day,selectshift1)
                            uprequire(b0,day,selectshift0)
                            judge = 1
                if workingdays != khworkingdays:



                    if oper == 2:
                        for day in range(7*weeknum,7*weeknum+7):
                            if a0[employee1][day] != -1:

                                if shiftemployee(a0,weeknum,selectshift0) != []:
                                    kxemployee0 = shiftemployee(a0,weeknum,selectshift0)
 
                                    random.shuffle(kxemployee0)
 
                                    for employee0 in kxemployee0:
                                        if a0[employee0][day] == -1:
                                            a0[employee0][day] = selectshift0
                                            uprequire(b0,day,selectshift0)
  
                                            judge = 1
                                            break

                               
            fadict[sn] = copy.deepcopy(a0)
            requiredict[sn] = copy.deepcopy(b0)
            if judge == 1:
                recoperyx[iteration][oper] += 1
            else:
                nonopt[sn] += 1

        #shift split operator
        if oper == 3:
            a0 = copy.deepcopy(fadict[sn])
            b0 = copy.deepcopy(requiredict[sn]) 
            judge = 0

            if fullattenwork0(a0) != []:


                e0 = np.random.choice(fullattenwork0(a0))     

                weekset = [i for i in range(4)]
                random.shuffle(weekset) 
                for weeknum in weekset:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[e0][day] != -1:
                            s0 = a0[e0][day]

                            lowattennonworkset = lowattennonwork(a0,day)
                            random.shuffle(lowattennonworkset)

                            for enum in lowattennonworkset:

                                s1 = shiftnum(a0,day,enum)
                                if s1 == -1:

                                    a0[e0][day] = -1
                                    a0[enum][day] = s0
                                    judge = 1
                                    break  
                                if s1 != -1:
                                    if pdshiftzh(b0,day,s0,s1) == 1:

                                        a0[e0][day] = -1
                                        a0[enum][day] = s1
                                        uprequire1(b0,day,s0)
                                        uprequire(b0,day,s1)
                                        judge = 1
                                        break
     

            fadjust(a0)
            if judge == 1: 
                fadict[sn] = copy.deepcopy(a0)
                requiredict[sn] = copy.deepcopy(b0)
                obj[sn] = len(fadict[sn])
                recoperyx[iteration][oper] += 1
            else:
                nonopt[sn] += 1               


#############################################onlooker bee stage#############################################################    
###roulete wheel selection method  
    
    for sn in range(N):

        zz = 10000
        for i in range(N):
            if obj[i] <= zz:
                zz = obj[i]
        

        
        fit = []
        for i in range(N):
            fit.append(round((1/(1+obj[i]-zz)),2))

        
        
        sum = 0
        for i in range(N):
            sum += fit[i]
        

        
        prob = []
        for i in range(N):
            prob.append(round(fit[i]/sum,3))

        
        
        for i in range(1,N):
            prob[i] += prob[i-1]
            

      
        random01 = random.random()
    

        if random01 <= prob[0]:
            selectn = 0
        else:
            for i in range(1,N):
                if (random01 > prob[i-1]) and (random01 <= prob[i]):
                    selectn = i
                    

        
        #dynamic selection probability for neighborhood structures
        random01 = random.random()
        pro1 = 0.4 - 0.9*iteration/(600+iteration) 
        if random01 <= pro1:
            oper = 0
        else:
            oper = np.random.choice([1,2,3])
            


        
        recoper[iteration][oper] += 1        
        
        #redundancy removal operator
        if oper == 0:
            judge = 0
            a0 = copy.deepcopy(fadict[selectn])  
            b0 = copy.deepcopy(requiredict[selectn])

            for weeknum in range(4):
  
                empnumsj = [i for i in range(len(fadict[selectn]))]
                random.shuffle(empnumsj)

                for enum in empnumsj:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[enum][day] != -1:
 
                            if (pddel(a0,enum,day,b0) == 0):
                                uprequire1(b0,day,a0[enum][day])
                                a0[enum][day] = -1
                                judge = 1
        
            fadjust(a0)
            if judge == 1: 
                fadict[selectn] = copy.deepcopy(a0)
                requiredict[selectn] = copy.deepcopy(b0)
                obj[selectn] = len(fadict[selectn])
                recoperyx[iteration][oper] += 1
            else:
                nonopt[selectn] += 1
        
        
         #shift fusion operator
        if oper == 1:
            judge = 0
            a0 = copy.deepcopy(fadict[selectn])  
            b0 = copy.deepcopy(requiredict[selectn])  

            if lowattenwork(a0) != []:
                e0 = np.random.choice(lowattenwork(a0)) 
   
                weekset = [i for i in range(4)]
                random.shuffle(weekset)       
                for weeknum in weekset:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[e0][day] != -1:
                            s0 = a0[e0][day]

                            lowattennonworkset = lowattennonwork(a0,day)
                            random.shuffle(lowattennonworkset)

                            for enum in lowattennonworkset:

                                s1 = shiftnum(a0,day,enum)
                                if s1 == -1:

                                    a0[e0][day] = -1
                                    a0[enum][day] = s0
                                    judge = 1
                                    break                            
                                if s1 != -1:
                                    if pdshiftzh(b0,day,s0,s1) == 1:

                                        a0[e0][day] = -1
                                        a0[enum][day] = s1
                                        uprequire1(b0,day,s0)
                                        uprequire(b0,day,s1)
                                        judge = 1
                                        break
      
        
                fadjust(a0)
                if judge == 1: 
                    fadict[selectn] = copy.deepcopy(a0)
                    requiredict[selectn] = copy.deepcopy(b0)
                    obj[selectn] = len(fadict[selectn])
                    recoperyx[iteration][oper] += 1
                else:
                 nonopt[selectn] += 1       
                    
        
        
        
        #redundancy balance operator
        if oper == 2:
            a0 = copy.deepcopy(fadict[selectn])  
            b0 = copy.deepcopy(requiredict[selectn]) 

            judge = 0        
            for weeknum in range(4):
                workshiftset = workshift(a0,weeknum) 


                minmaxp = requireminmaxp(weeknum,b0) 
                minp = minmaxp[0] 

                maxp = minmaxp[1]

                shift0 = shiftminmaxp(minp)

                shift1 = shiftminmaxp(maxp)

                kxshift1 = shiftjiaoji(shift1,workshiftset)

                if kxshift1 != []:
                    selectshift1 = np.random.choice(kxshift1)

                selectshift0 = np.random.choice(shift0)    

                kxemployee1 = shiftemployee(a0,weeknum,selectshift1)

                employee1 = np.random.choice(kxemployee1)

                workingdays = 0
                for day in range(7*weeknum,7*weeknum+7):
                    if a0[employee1][day] != -1:
                        workingdays += 1

                khworkingdays = 0
                for day in range(7*weeknum,7*weeknum+7):
                    if a0[employee1][day] != -1:

                        khworkingdays += pdshiftzh(b0,day,selectshift1,selectshift0)

                if workingdays == khworkingdays:

                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[employee1][day] != -1:

                            a0[employee1][day] = selectshift0
                            uprequire1(b0,day,selectshift1)
                            uprequire(b0,day,selectshift0)
                            judge = 1
                if workingdays != khworkingdays:

                    if oper == 2:
                        for day in range(7*weeknum,7*weeknum+7):
                            if a0[employee1][day] != -1:

                                if shiftemployee(a0,weeknum,selectshift0) != []:
                                    kxemployee0 = shiftemployee(a0,weeknum,selectshift0)

                                    random.shuffle(kxemployee0)

                                    for employee0 in kxemployee0:
                                        if a0[employee0][day] == -1:
                                            a0[employee0][day] = selectshift0
                                            uprequire(b0,day,selectshift0)

                                            judge = 1
                                            break
                      
                               
            fadict[selectn] = copy.deepcopy(a0)
            requiredict[selectn] = copy.deepcopy(b0)
            if judge == 1:
                recoperyx[iteration][oper] += 1
            else:
                nonopt[selectn] += 1
    
        #shift split operator
        if oper == 3:
            a0 = copy.deepcopy(fadict[selectn]) 
            b0 = copy.deepcopy(requiredict[selectn]) 
            judge = 0

            if fullattenwork0(a0) != []:

                e0 = np.random.choice(fullattenwork0(a0))   

                weekset = [i for i in range(4)]
                random.shuffle(weekset)     
                for weeknum in weekset:
                    for day in range(7*weeknum,7*weeknum+7):
                        if a0[e0][day] != -1:
                            s0 = a0[e0][day]

                            lowattennonworkset = lowattennonwork(a0,day)
                            random.shuffle(lowattennonworkset)

                            for enum in lowattennonworkset:

                                s1 = shiftnum(a0,day,enum)
                                if s1 == -1:

                                    a0[e0][day] = -1
                                    a0[enum][day] = s0
                                    judge = 1
                                    break  
                                if s1 != -1:
                                    if pdshiftzh(b0,day,s0,s1) == 1:

                                        a0[e0][day] = -1
                                        a0[enum][day] = s1
                                        uprequire1(b0,day,s0)
                                        uprequire(b0,day,s1)
                                        judge = 1
                                        break
 

            fadjust(a0)
            if judge == 1: 
                fadict[selectn] = copy.deepcopy(a0)
                requiredict[selectn] = copy.deepcopy(b0)
                obj[selectn] = len(fadict[selectn])
                recoperyx[iteration][oper] += 1
            else:
                nonopt[selectn] += 1        
        
    ###########################################scouts stage##########################################                
    for sn in range(N):
        if nonopt[sn] > 25: #limit       
            enum = 0 
            xeds = []
            require = copy.deepcopy(require0)
            pd0 = pdfg(require) 
            while pd0 > 0:
                xjjh = []            
                xjjh = xj() 

                shiftsj = shiftset() 

                if yxfg(shiftsj,xjjh) > 0:
                    for day in range(len(require)):

                        if day not in xjjh:
                            xeds.append([enum, day, shiftsj[day//7]])

                            require = uprequire(require,day,shiftsj[day//7])

                    enum += 1
                pd0 = pdfg(require)    
                   
            fa = pbfa(xeds).tolist()         
                    
          
        
 
            fadict[sn] = fa 
        
         
            requiredict[sn] = require 
            obj[sn] = len(fadict[sn])
            nonopt[sn] = 0
        
        
    
    iteration += 1
    bestobj = obj[0]
    bestsn = 0

    for sn in range(1,N):
        if obj[sn] <= bestobj:
            bestobj = obj[sn]
            bestsn = sn

    if iteration <= N:
        penaltyinifa[iteration-1] = copy.deepcopy(fadict[bestsn])        
        penaltyinirequire[iteration-1] = copy.deepcopy(requiredict[bestsn])
        obj0[iteration-1] = bestobj
        
    
    if iteration > N:
        worstobj = obj0[0]
        worstsn = 0
        for sn in range(1,N):
            if obj0[sn] >= worstobj:
                worstobj = obj0[sn]
                worstsn = sn
        if bestobj < worstobj:
            penaltyinifa[worstsn] = copy.deepcopy(fadict[bestsn])
            penaltyinirequire[worstsn] = copy.deepcopy(requiredict[bestsn])
            obj0[worstsn] = bestobj

       
    if bestobj < zuizhongobj:
        zuizhongobj = bestobj   
        bestfa = copy.deepcopy(fadict[bestsn])
        bestrequire = copy.deepcopy(requiredict[bestsn])
        nonoptiteration = 0
    else:
        nonoptiteration += 1
    
    reciterationobj.append(zuizhongobj)        
    
    print("此时时间为",time.time()-first_time)
    recordtime.append(time.time()-first_time)
    print("截止此时目标值为:",zuizhongobj)
#




   

penaltyinifa0 = copy.deepcopy(penaltyinifa)
penaltyinirequire0 = copy.deepcopy(penaltyinirequire)



#####################################################preprocess############################################################
penaltyinifa = copy.deepcopy(penaltyinifa0)
penaltyinirequire = copy.deepcopy(penaltyinirequire0)

LB = 11 ###the number of employees available

foodscorelist = [0 for i in range(N)] #penalty for all the food sources
for sn in range(N):
    foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn]))) 



##add employees available but assigned no work 
for sn in range(N):
    if len(penaltyinifa[sn]) < LB:
        a0 = copy.deepcopy(penaltyinifa[sn])
        for i in range(len(penaltyinifa[sn]),LB):
            a0.append([-1 for i in range(28)])                      
        penaltyinifa[sn] = copy.deepcopy(a0)


###pick out employees working from Monday to Sunday in week b of scheme a
def fullattenwork(a,b):
    c = []
    for i in range(len(a)):
        d = 0
        for j in range(7*b,7*b+7):
            if a[i][j] >= 0:
                d += 1
        if d == 7:
            c.append(i)
    return c



for sn in range(N):

    a0 = copy.deepcopy(penaltyinifa[sn])
    for weeknum in range(4): 
        kxemployee0 = noattenwork(a0,weeknum)

        if kxemployee0 != []:                
            for employee0 in kxemployee0:

                kxemployee1 = fullattenwork(a0,weeknum)

                if kxemployee1 != []:
                    employee1 = np.random.choice(kxemployee1)

                    day = np.random.choice([7*weeknum,7*weeknum+2,7*weeknum+3,7*weeknum+5])

                    shift1 = a0[employee1][day]
                    a0[employee0][day] = shift1
                    a0[employee1][day] = -1
                    a0[employee0][day+1] = shift1
                    a0[employee1][day+1] = -1            
    penaltyinifa[sn] = copy.deepcopy(a0)
                

###pick out employees having no complete weekend off in four weeks
def noweekendemp(a):
    b = []
    for j in range(len(a)):
        c = 0
        for i in range(4):
            if a[j][7*i+5] != -1 or a[j][7*i+6] != -1:
                c += 1
        if c == 4:
            b.append(j)
    return(b)


###pick out employees having at least one complete weekend off in four weeks
def weekendemp(a):
    b = []
    for j in range(len(a)):
        c = 0
        for i in range(4):
            if a[j][7*i+5] == -1 and a[j][7*i+6] == -1:
                c += 1
        if c > 1:
            b.append(j)
    return(b)

for sn in range(N):
    a0 = penaltyinifa[sn]                
    kxemployee0 = noweekendemp(a0)

    random.shuffle(kxemployee0)
    for employee0 in kxemployee0:

        kxemployee1 = weekendemp(a0)

        if kxemployee1 != []:
            employee1 = np.random.choice(kxemployee1)

            kxweeknum = []
            for weeknum in range(4):
                if a0[employee1][7*weeknum+5] == -1 and a0[employee1][7*weeknum+6] == -1:
                    kxweeknum.append(weeknum)

            weeknum = np.random.choice(kxweeknum)

            c0 = copy.deepcopy(a0[employee0][7*weeknum:7*weeknum+7])
            for day in range(7*weeknum,7*weeknum+7):
                a0[employee0][day] = a0[employee1][day]
                a0[employee1][day] = c0[day-7*weeknum]    
    penaltyinifa[sn] = copy.deepcopy(a0)        
    

foodscorelist = [0 for i in range(N)]   
for sn in range(N):
    foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn]))) 
print("预处理后的食物源的惩罚值")
print(foodscorelist)




    
penaltyinifa0 = copy.deepcopy(penaltyinifa)
penaltyinirequire0 = copy.deepcopy(penaltyinirequire)



            
#######################################################################stage-II###################################
penaltyinifa = copy.deepcopy(penaltyinifa0)
penaltyinirequire = copy.deepcopy(penaltyinirequire0)




foodscorelist = [0 for i in range(N)] ##penalty for all the food sources
for sn in range(N):
    foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn]))) 


#pick out employees whose assighments incur penalty in week b of sheme a
def emppenaltyweek(a,b):
    c = []
    d = score(a)
    for i in range(len(a)):
        for j in range(7*b,7*b+7):
            if d[i][j] > 0:
                c.append(i)
                break
    return(c)
        
    



###pick out the days with penalty for each employee    
def workdaypenalty(a):
    b = len(a)
    c = {}
    d = score(a)
    for i in range(b):
        c[i] = []
        for j in range(28):
            if (a[i][j] != -1) and (d[i][j] != 0):
                c[i].append(j)
    return(c)


#pick out employees whose assighments incur penalty on day b of sheme a
def workemppenalty(a,b):
    c = []
    d = score(a)
    for i in range(len(a)):
        if d[i][b] > 0 and a[i][b] != -1:
            c.append(i)
    return(c)
    


##pick out employees having no assignment on day b of scheme a
def nonworkemp(a,b):
    c = []
    for i in range(len(a)):
        if a[i][b] == -1:
            c.append(i)
    return(c)

#pick out employees having a single isolated off day    
def seperateworkemp(a):
    b = []
    for j in range(len(a)):
        for i in range(1,27):
            if a[j][i] == -1 and a[j][i-1] != -1 and a[j][i+1] != -1:
                b.append(j)
                break
    return(b)

#pick out employees who having no assignment but incur penalty on day b of sheme a            
def penaltynonworkemp(a,b):
    c = []
    d = score(a)
    for i in range(len(a)):
        if a[i][b] == -1 and d[i][b] > 0:
            c.append(i)
    return(c)

#calculate the total penalty for each employee
def employeescore(a):
    b = len(a)
    c = []
    for i in range(b):
        d = 0
        for j in range(28):
            d += a[i][j]
        c.append(d)
    return c




#principle(I)
#def deleteemp(a,b): 
#    c = score(a)
#    d = employeescore(c)

#    g = -100000
#    for i in range(len(d)):
#        if d[i] > g:
#            g = d[i]
#            f = i
#            

#            
#    z = 0
#    for i in range(28):
#        z += c[f][i]
#    for i in range(len(a[0])):
#        if a[f][i] != -1:
#            uprequire1(b,i,a[f][i])                
#    del a[f]
#    
#    c = []    
#    for i in range(28):
#        c.append([])
#        for j in range(15):
#            if b[i][j] <= 0:          
#                c[i].append(0)
#            else:
#                c[i].append(b[i][j])
#    return [a,b,c,z]    



#principle(II)
def deleteemp(a,b):
    c = score(a)
    g = [i for i in range(len(a))]  
    f = np.random.choice(g)
    z = 0
    for i in range(28):
        z += c[f][i]
    for i in range(len(a[0])):
        if a[f][i] != -1:
            uprequire1(b,i,a[f][i])                
    del a[f]
    
    c = []    
    for i in range(28):
        c.append([])
        for j in range(15):
            if b[i][j] <= 0:          
                c[i].append(0)
            else:
                c[i].append(b[i][j])
    return [a,b,c,z] 

#principle(III)
#def deleteemp(a,b): 
#    c = score(a)

#    d = employeescore(c)

#    g = []
#    for i in range(len(d)):
#        if d[i] != 0:
#            g.append(i)
#            

#            
#    if g != []:
#        f = np.random.choice(g)
#        z = 0
#        for i in range(28):
#            z += c[f][i]
#        for i in range(len(a[0])):
#            if a[f][i] != -1:
#                uprequire1(b,i,a[f][i])                
#        del a[f]
#        
#        c = []    
#        for i in range(28):
#            c.append([])
#            for j in range(15):
#                if b[i][j] <= 0:          
#                    c[i].append(0)
#                else:
#                    c[i].append(b[i][j])
#        return [a,b,c,z]    
    

  
#pick put shifs which can cover at least 7 same intervals as shift a
def shiftkz(a):
    b = []
    for i in range(len(cover[0])):
        if cover[a][i] == 1:
            b.append(i)
    c = []
    for i in range(len(cover)):
        if i != a:
            d = 0
            for j in b:
                if cover[i][j] == 1:
                    d += 1
            if d >= 7:
                c.append(i)
    return c



     

recoper0 = {}
recoperyx0 = {}
iteration = 0
zuizhongobj = 1000000000000
nonopt = [0 for i in range(N)]
reciterationobj0 = []
recordtime = []
nonoptiteration = 0
reiternonopt = {}

first_time = time.time()
while time.time() - first_time <= 500  and zuizhongobj != 0:

    print("第%d次迭代"%(iteration))
    recoper0[iteration] = [0,0,0]
    recoperyx0[iteration] = [0,0,0]
#######################################################employed###############################    
    for sn in range(N):

        oper = np.random.choice([0,1,2])
        recoper0[iteration][oper] += 1
        #Single-exchange operator
        if oper == 0:

            judge = 0
            a0 = copy.deepcopy(penaltyinifa[sn])
            b0 = copy.deepcopy(penaltyinirequire[sn])
            kxemployee = seperateworkemp(a0)
            if kxemployee != []:
                employee0 = np.random.choice(kxemployee)
                kxday = []
                for day in range(1,27):
                    if a0[employee0][day] == -1 and a0[employee0][day-1] != -1 and a0[employee0][day+1] != -1:
                        kxday.append(day)
                for day in kxday:
                    shift0 = a0[employee0][day-1]
                    empnonworkingset = penaltynonworkemp(a0,day-1)
                    if empnonworkingset != []:
                        employee1 = np.random.choice(empnonworkingset)
                        shift1 = shiftnum(a0,day-1,employee1)
                        if pdshiftzh(b0,day-1,shift0,shift1) == 1 and shift1 != -1:

                            a0[employee0][day-1] = -1
                            a0[employee1][day-1] = shift1
                            uprequire(b0,day-1,shift1)
                            uprequire1(b0,day-1,shift0)     
                            if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[sn]))):
                                penaltyinifa[sn] = copy.deepcopy(a0)
                                penaltyinirequire[sn] = copy.deepcopy(b0)
                                judge = 1
                                
                            else:
                                a0[employee0][day-1] = shift0
                                a0[employee1][day-1] = -1
                                uprequire(b0,day-1,shift0)
                                uprequire1(b0,day-1,shift1) 
                                
            if judge == 0:              
                nonopt[sn] += 1
            if judge == 1:
                nonopt[sn] = 0
                recoperyx0[iteration][oper] += 1  
                foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn])))                  
                        
            if check1(penaltyinifa[sn],penaltyinirequire[sn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")                              
            if check2(penaltyinirequire[sn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")                                                         
                                              
 
                    
        #Block-exchange operator
        if oper == 1:
            judge = 0
            a0 = copy.deepcopy(penaltyinifa[sn])
            b0 = copy.deepcopy(penaltyinirequire[sn])
            weekset = [0,1,2,3]
            random.shuffle(weekset)
            for weeknum in weekset:
                kxemployee = emppenaltyweek(a0,weeknum)
                if kxemployee != []:
                    emprandom0 = np.random.choice(kxemployee)
                    kxemployee.remove(emprandom0)
                    if kxemployee != []:
                        emprandom1 = np.random.choice(kxemployee)
                        c0 = copy.deepcopy(a0[emprandom0][7*weeknum:7*weeknum+7])
                        for day in range(7*weeknum,7*weeknum+7):
                            a0[emprandom0][day] = a0[emprandom1][day]
                            a0[emprandom1][day] = c0[day-7*weeknum]
                        if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[sn]))):                                              
                            penaltyinifa[sn] = copy.deepcopy(a0)
                            judge = 1
                        else:
                            a0 = copy.deepcopy(penaltyinifa[sn]) 
            if judge == 1:
                foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn])))
                nonopt[sn] = 0
                recoperyx0[iteration][oper] += 1  
            else:
                nonopt[sn] += 1
                                                    
            if check1(penaltyinifa[sn],penaltyinirequire[sn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")                                
            if check2(penaltyinirequire[sn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")                 
                
               
        #Double-exchange operator
        if oper == 2:
            judge = 0

            a0 = copy.deepcopy(penaltyinifa[sn])
            b0 = copy.deepcopy(penaltyinirequire[sn])
            weekset = [0,1,2,3]
            random.shuffle(weekset)
            for weeknum in weekset:           
                shift0 = np.random.choice([i for i in range(len(cover))])
                if len(shiftemployee(a0,weeknum,shift0)) >= 2:
                    kxemployee = shiftemployee(a0,weeknum,shift0)
                    employee0 = np.random.choice(kxemployee)
                    kxemployee.remove(employee0)
                    employee1 = np.random.choice(kxemployee)
                    daynum = np.random.choice([i for i in range(7*weeknum,7*weeknum+6)])
                    c0 = copy.deepcopy(a0[employee0][daynum:daynum+2])
                    for day in range(daynum,daynum+2):
                        a0[employee0][day] = a0[employee1][day]
                        a0[employee1][day] = c0[day-daynum]                   
                    if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[sn]))):                                              
                        penaltyinifa[sn] = copy.deepcopy(a0)
                        judge = 1
                    else:
                        a0 = copy.deepcopy(penaltyinifa[sn]) 
            if judge == 1:
                foodscorelist[sn] = round(totalscore(score(penaltyinifa[sn])))
                nonopt[sn] = 0
                recoperyx0[iteration][oper] += 1  
            else:
                nonopt[sn] += 1
            
            if check1(penaltyinifa[sn],penaltyinirequire[sn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")  
            if check2(penaltyinirequire[sn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")                 

           
                                        

#######################################################onlookers###############################     
######roulette wheel selection method     
    for sn in range(N):

        maxscore = 0
        for i in range(N):
            if foodscorelist[i] >= maxscore:
                maxscore = foodscorelist[i]

                
        gap = []
        for i in range(N):
            gap.append(maxscore+10-foodscorelist[i])
            

        sum = 0
        for i in range(N):
            sum += gap[i]

        
        prob = []
        for i in range(N):
            prob.append(round(gap[i]/sum,3))

                

        
        for i in range(1,N):
            prob[i] += prob[i-1]
            

      
        random01 = random.random()
    

        if random01 <= prob[0]:
            selectn = 0
        else:
            for i in range(1,N):
                if (random01 > prob[i-1]) and (random01 <= prob[i]):
                    selectn = i
        
        

        worstsn = 0
        for i in range(1,N):
            if foodscorelist[i] > foodscorelist[worstsn]:
                worstsn = i
                


        oper = np.random.choice([0,1,2])
        recoper0[iteration][oper] += 1
                  
        #Single-exchange operator
        if oper == 0:

            judge = 0
            a0 = copy.deepcopy(penaltyinifa[selectn])
            b0 = copy.deepcopy(penaltyinirequire[selectn])
            kxemployee = seperateworkemp(a0)
            if kxemployee != []:
                employee0 = np.random.choice(kxemployee)
                kxday = []
                for day in range(1,27):
                    if a0[employee0][day] == -1 and a0[employee0][day-1] != -1 and a0[employee0][day+1] != -1:
                        kxday.append(day)
                for day in kxday:
                    shift0 = a0[employee0][day-1]
                    empnonworkingset = penaltynonworkemp(a0,day-1)
                    if empnonworkingset != []:
                        employee1 = np.random.choice(empnonworkingset)
                        shift1 = shiftnum(a0,day-1,employee1)
                        if pdshiftzh(b0,day-1,shift0,shift1) == 1 and shift1 != -1:

                            a0[employee0][day-1] = -1
                            a0[employee1][day-1] = shift1
                            uprequire(b0,day-1,shift1)
                            uprequire1(b0,day-1,shift0)     
                            if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[selectn]))):
                                penaltyinifa[worstsn] = copy.deepcopy(a0)
                                penaltyinirequire[worstsn] = copy.deepcopy(b0)
                                judge = 1
                                
                            else:
                                a0[employee0][day-1] = shift0
                                a0[employee1][day-1] = -1
                                uprequire(b0,day-1,shift0)
                                uprequire1(b0,day-1,shift1) 
                                
            if judge == 0:              
                nonopt[selectn] += 1
            if judge == 1:
                nonopt[worstsn] = 0
                recoperyx0[iteration][oper] += 1  
                foodscorelist[worstsn] = round(totalscore(score(penaltyinifa[worstsn])))                  
                        
            if check1(penaltyinifa[selectn],penaltyinirequire[selectn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")
            if check1(penaltyinifa[worstsn],penaltyinirequire[worstsn]) != 0:
                print("该操作1有问题！！！！！！！！！！！！！")  
            if check2(penaltyinirequire[selectn]) != 0 or check2(penaltyinirequire[worstsn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")                                                          
                                              
 
                    
        #Block-exchange operator
        if oper == 1:

            judge = 0
            a0 = copy.deepcopy(penaltyinifa[selectn])
            b0 = copy.deepcopy(penaltyinirequire[selectn])
            weekset = [0,1,2,3]
            random.shuffle(weekset)
            for weeknum in weekset:
                kxemployee = emppenaltyweek(a0,weeknum)
                if kxemployee != []:
                    emprandom0 = np.random.choice(kxemployee)
                    kxemployee.remove(emprandom0)
                    if kxemployee != []:
                        emprandom1 = np.random.choice(kxemployee)
                        c0 = copy.deepcopy(a0[emprandom0][7*weeknum:7*weeknum+7])
                        for day in range(7*weeknum,7*weeknum+7):
                            a0[emprandom0][day] = a0[emprandom1][day]
                            a0[emprandom1][day] = c0[day-7*weeknum]
                        if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[selectn]))):                                              
                            penaltyinifa[worstsn] = copy.deepcopy(a0)
                            penaltyinirequire[worstsn] = copy.deepcopy(b0)
                            judge = 1
                        else:
                            a0 = copy.deepcopy(penaltyinifa[selectn]) 
            if judge == 1:
                foodscorelist[worstsn] = round(totalscore(score(penaltyinifa[worstsn])))
                nonopt[worstsn] = 0
                recoperyx0[iteration][oper] += 1  
            else:
                nonopt[selectn] += 1
                            
       
                 
                        
            if check1(penaltyinifa[selectn],penaltyinirequire[selectn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")
            if check1(penaltyinifa[worstsn],penaltyinirequire[worstsn]) != 0:
                print("该操作1有问题！！！！！！！！！！！！！")  
            if check2(penaltyinirequire[selectn]) != 0 or check2(penaltyinirequire[worstsn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")                 
                
                
       #Double-exchange operator
        if oper == 2:
            judge = 0

            a0 = copy.deepcopy(penaltyinifa[selectn])
            b0 = copy.deepcopy(penaltyinirequire[selectn])
            weekset = [0,1,2,3]
            random.shuffle(weekset)
            for weeknum in weekset:           
                shift0 = np.random.choice([i for i in range(len(cover))])
                if len(shiftemployee(a0,weeknum,shift0)) >= 2:
                    kxemployee = shiftemployee(a0,weeknum,shift0)
                    employee0 = np.random.choice(kxemployee)
                    kxemployee.remove(employee0)
                    employee1 = np.random.choice(kxemployee)
                    daynum = np.random.choice([i for i in range(7*weeknum,7*weeknum+6)])
                    c0 = copy.deepcopy(a0[employee0][daynum:daynum+2])
                    for day in range(daynum,daynum+2):
                        a0[employee0][day] = a0[employee1][day]
                        a0[employee1][day] = c0[day-daynum]                   
                    if round(totalscore(score(a0))) <= round(totalscore(score(penaltyinifa[selectn]))):                                              
                        penaltyinifa[worstsn] = copy.deepcopy(a0)
                        penaltyinirequire[worstsn] = copy.deepcopy(b0)
                        judge = 1
                    else:
                        a0 = copy.deepcopy(penaltyinifa[selectn]) 
            if judge == 1:
                foodscorelist[worstsn] = round(totalscore(score(penaltyinifa[worstsn])))
                nonopt[worstsn] = 0
                recoperyx0[iteration][oper] += 1  
            else:
                nonopt[selectn] += 1
                
            if check1(penaltyinifa[selectn],penaltyinirequire[selectn]) != 0:
                print("该操作0有问题！！！！！！！！！！！！！")
            if check1(penaltyinifa[worstsn],penaltyinirequire[worstsn]) != 0:
                print("该操作1有问题！！！！！！！！！！！！！")  
            if check2(penaltyinirequire[selectn]) != 0 or check2(penaltyinirequire[worstsn]) != 0:
                print("该操作有问题！！！！！！！！！！！！！")  
                
                   

#####################################scouts############################################


    for sn in range(N):
        if nonopt[sn] > 15:##limt

            ################ipruin-and-recreate block(cplex)#############
            a0 = copy.deepcopy(penaltyinifa[sn])
            b0 = copy.deepcopy(penaltyinirequire[sn])

            yyy = employeescore(score(a0))
            count = 0
            for i in range(len(a0)):
                if yyy[i] > 0:
                    count += 1


 
            selectscorelist = deleteemp(a0,b0) 
            a0 = copy.deepcopy(selectscorelist[0]) 
            b0 = copy.deepcopy(selectscorelist[1])

            b1 = copy.deepcopy(selectscorelist[2])

            zz0 = copy.deepcopy(selectscorelist[3])
            selectscorelist = deleteemp(a0,b0) 
            a0 = copy.deepcopy(selectscorelist[0]) 
            b0 = copy.deepcopy(selectscorelist[1])

            b1 = copy.deepcopy(selectscorelist[2])
            zz1 = copy.deepcopy(selectscorelist[3])

            selectscorelist = deleteemp(a0,b0) 
            a0 = copy.deepcopy(selectscorelist[0]) 
            b0 = copy.deepcopy(selectscorelist[1])

            b1 = copy.deepcopy(selectscorelist[2])
            zz2 = copy.deepcopy(selectscorelist[3])

            zz3 = 0
            zz4 = 0 
            zz5 = 0
            zz6 = 0 
            zz7 = 0  
            zz8 = 0 
            zz9 = 0      
            


            shift = [i for i in range(len(cover))] 
            

            
            nbemployee = [i for i in range(0, 3)]
            
            
            week = [i for i in range(0, 4)]
            
            day = [i for i in range(len(require))] 
            
            period = [i for i in range(len(cover[0]))] 
            
            assign = [(i,j,k) for i in nbemployee for j in day for k in shift] 
            
            assignds = [(i,j) for i in day for j in shift] 
            
            assignew = [(i,j) for i in nbemployee for j in week] 
            
            assigned = [(i,j) for i in nbemployee for j in day] 
            
            supply = [(i,j) for i in day for j in period] 
            
            mdl = Model('CC')
            xed = mdl.binary_var_dict(assigned,name='xed') 
            nds = mdl.continuous_var_dict(assignds,name='nds') 
            xeds = mdl.binary_var_dict(assign,name='xeds') 
            xew = mdl.binary_var_dict(assignew,name='xew') 
            sup = mdl.continuous_var_dict(supply,name='sup') 
            f1 =  mdl.continuous_var_dict(nbemployee,name='f1') 
            f10 =  mdl.continuous_var_dict(assigned,name='f10') 
            f2 =  mdl.continuous_var_dict(nbemployee,name='f2') 
            f20 =  mdl.continuous_var_dict(assigned,name='f20') 
            f3 =  mdl.continuous_var_dict(nbemployee,name='f3') 
            f30 =  mdl.continuous_var_dict(assigned,name='f30') 
            f4 =  mdl.continuous_var_dict(nbemployee,name='f4')
            f5 =  mdl.continuous_var_dict(nbemployee,name='f5') 
            
            mdl.minimize(mdl.sum(f1[i]+f2[i]+f3[i]+f4[i]+f5[i] for i in nbemployee))
            
            mdl.add_constraints(mdl.sum(xeds[i,j,k]for k in shift) == xed[i,j]  for i,j in assigned) 
            mdl.add_constraints(mdl.sum(xeds[i,j,k]for i in nbemployee) == nds[j,k] for j,k in assignds) 
            mdl.add_constraints(mdl.sum(nds[i,j]*cover[j][k] for j in shift) == sup [i,k] for i,k in supply) 
            mdl.add_constraints(sup[i,j] >= b1[i][j] for i,j in supply)
            
            mdl.add_constraints(f10[i,j]>=-xed[i,j-1] + xed[i,j] - xed[i,j+1] for i in nbemployee for j in range(1,27)) 
            mdl.add_constraints(f10[i,j]>= 0 for i in nbemployee for j in range(1,27))
            mdl.add_constraints(f10[i,0]>= xed[i,0] - xed[i,1] for i in nbemployee)
            mdl.add_constraints(f10[i,0]>= 0 for i in nbemployee)
            mdl.add_constraints(f10[i,27]>= xed[i,27] - xed[i,26] for i in nbemployee)
            mdl.add_constraints(f10[i,27]>= 0 for i in nbemployee)
            mdl.add_constraints(mdl.sum(f10[i,j]for j in day) == f1[i]  for i in nbemployee)
            
            
            mdl.add_constraints(f20[i,j]>=xed[i,j-1] - xed[i,j] + xed[i,j+1] - 1 for i in nbemployee for j in range(1,27)) 
            mdl.add_constraints(f20[i,j]>= 0 for i in nbemployee for j in range(1,27))
            mdl.add_constraints(f20[i,0]>= -xed[i,0] - xed[i,1] for i in nbemployee) 
            mdl.add_constraints(f10[i,0]>= 0 for i in nbemployee)
            mdl.add_constraints(f10[i,27]>= -xed[i,27] + xed[i,26] for i in nbemployee)
            mdl.add_constraints(f10[i,27]>= 0 for i in nbemployee)
            mdl.add_constraints(mdl.sum(f20[i,j]for j in day) == f2[i]  for i in nbemployee)
            
            
            
            mdl.add_constraints(f30[i,j] >= xed[i,j-6] + xed[i,j-5] + xed[i,j-4] + xed[i,j-3] + xed[i,j-2] + xed[i,j-1] +xed[i,j]- 6 for i in nbemployee for j in range(6,28))
            mdl.add_constraints(f30[i,j] >= 0 for i in nbemployee for j in range(6,28)) 
            mdl.add_constraints(f30[i,j] == 0 for i in nbemployee for j in range(0,6)) 
            mdl.add_constraints(mdl.sum(f30[i,j]for j in day) == f3[i]  for i in nbemployee)
            
            
            mdl.add_constraints(f4[i] >= mdl.sum(xew[i,j] for j in week) - 3 for i in nbemployee) 
            mdl.add_constraints(f4[i] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,0] - xed[i,5] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,0] - xed[i,6] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,0] <= xed[i,5] + xed[i,6] for i in nbemployee) 
            mdl.add_constraints(xew[i,1] - xed[i,12] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,1] - xed[i,13] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,1] <= xed[i,12] + xed[i,13] for i in nbemployee)
            mdl.add_constraints(xew[i,2] - xed[i,19] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,2] - xed[i,20] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,2] <= xed[i,19] + xed[i,20] for i in nbemployee) 
            mdl.add_constraints(xew[i,3] - xed[i,26] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,3] - xed[i,27] >= 0 for i in nbemployee) 
            mdl.add_constraints(xew[i,3] <= xed[i,26] + xed[i,27] for i in nbemployee)             
            mdl.add_constraints(mdl.sum(xeds[i,j,k] for j in range(0,7)) >= mdl.sum(xed[i,j] for j in range(0,7)) + (xeds[i,m,k] + xed[i,m] -2) * 10000 for i in nbemployee for m in range(0,7) for k in shift)
            mdl.add_constraints(mdl.sum(xeds[i,j,k] for j in range(7,14)) >= mdl.sum(xed[i,j] for j in range(7,14)) + (xeds[i,m,k] + xed[i,m] -2) * 10000 for i in nbemployee for m in range(7,14) for k in shift) 
            mdl.add_constraints(mdl.sum(xeds[i,j,k] for j in range(14,21)) >= mdl.sum(xed[i,j] for j in range(14,21)) + (xeds[i,m,k] + xed[i,m] -2) * 10000 for i in nbemployee for m in range(14,21) for k in shift) 
            mdl.add_constraints(mdl.sum(xeds[i,j,k] for j in range(21,28)) >= mdl.sum(xed[i,j] for j in range(21,28)) + (xeds[i,m,k] + xed[i,m] -2) * 10000 for i in nbemployee for m in range(21,28) for k in shift) 
            
            mdl.add_constraints(f5[i] >= mdl.sum(xed[i,j] for j in day) - 20 for i in nbemployee) 
            mdl.add_constraints(f5[i] >= 0 for i in nbemployee)    
            
            mdl.parameters.timelimit=600 
            solution=mdl.solve(log_output=True)
            mdl.get_solve_status()
            print(solution.solve_status)
            zzobj = mdl.objective_value
            print('此方案惩罚为',zzobj)
            employday = [[i,j] for i,j in assigned if xed[i,j].solution_value > 0.9]
            employdayshift =[[i,j,k] for i,j,k in assign if xeds[i,j,k].solution_value > 0.9]
            employweek = [[i,j] for i,j in assignew if xew[i,j].solution_value > 0.9] 
            dayshift = [[nds[i,j].solution_value for j in shift] for i in day] 
            supply0 = [[sup[i,j].solution_value for j in period] for i in day] 


            
            
            probability = math.exp( -1/(0.95**iteration))
            
            random01 = random.random()
            ###judge whether the newly generated food source is better than the old one
            if (zz0 + zz1 + zz2 + zz3 + zz4 + zz5 + zz6 + zz7 + zz8 + zz9  >= zzobj) and (solution != None):
                print("该操作有效！！！")
                a0.append([-1 for l in range(28)])
                m = len(a0)
                n = employdayshift[0][1] 
                a0[m-1][n] = employdayshift[0][2] 
                for i in range(1,len(employdayshift)):
                    if employdayshift[i][0] == employdayshift[i-1][0]:
                        n = employdayshift[i][1]
                        a0[m-1][n] = employdayshift[i][2]
                    else:
                        a0.append([-1 for l in range(28)])
                        m = len(a0)
                        n = employdayshift[i][1]
                        a0[m-1][n] = employdayshift[i][2]                    
                for i in range(len(supply0)):
                    for j in range(len(supply0[0])):
                        b0[i][j] -= round(supply0[i][j])
                penaltyinifa[sn] = copy.deepcopy(a0)
                penaltyinirequire[sn] = copy.deepcopy(b0)
                foodscorelist[sn] = round(totalscore(score(a0)))
                nonopt[sn] = 0

                if check1(penaltyinifa[sn],penaltyinirequire[sn]) != 0:
                    print("该操作有问题！！！！！！！！！！！！！")                 

            #accept the worse food source with possibilities
            if (zz0 + zz1 + zz2 + zz3 + zz4 + zz5 + zz6 + zz7 + zz8 + zz9 < zzobj) and (solution != None) and (random01 <= probability):
                print("该操作有效！！！")
                a0.append([-1 for l in range(28)])
                m = len(a0)
                n = employdayshift[0][1] 
                a0[m-1][n] = employdayshift[0][2] 
                for i in range(1,len(employdayshift)):
                    if employdayshift[i][0] == employdayshift[i-1][0]:
                        n = employdayshift[i][1]
                        a0[m-1][n] = employdayshift[i][2]
                    else:
                        a0.append([-1 for l in range(28)])
                        m = len(a0)
                        n = employdayshift[i][1]
                        a0[m-1][n] = employdayshift[i][2]                    
                for i in range(len(supply0)):
                    for j in range(len(supply0[0])):
                        b0[i][j] -= round(supply0[i][j])
                penaltyinifa[sn] = copy.deepcopy(a0)
                penaltyinirequire[sn] = copy.deepcopy(b0)
                foodscorelist[sn] = round(totalscore(score(a0)))
                nonopt[sn] = 0

    
    reiternonopt[iteration] =  nonopt           
   
             
    iteration += 1                         

    bestobj = foodscorelist[0]
    bestsn = 0
    for sn in range(1,N):
        if foodscorelist[sn] <= bestobj:
            bestobj = foodscorelist[sn]
            bestsn = sn
    
    print("此时时间为",time.time()-first_time)
    
  
    
    if bestobj < zuizhongobj:
        zuizhongobj = bestobj   
        bestfa = copy.deepcopy(penaltyinifa[bestsn])
        bestrequire = copy.deepcopy(penaltyinirequire[bestsn])
        nonoptiteration = 0
    else:
        nonoptiteration += 1
        
    
    reciterationobj0.append(zuizhongobj)

    print("当前最优解为",zuizhongobj)###the objective value of the final solution





print(check1(bestfa,bestrequire)) 


