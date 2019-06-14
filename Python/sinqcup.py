# SinquefieldCup: Rankability Measures for Sinquefield Cup
#
# Author: Thomas R. Cameron
# Date: 4/9/2019
from srm_module import specR, connR
from copy import deepcopy
import numpy as np

#####################################################
#                 Data                              #      
#####################################################
def data(year):
    if(year==2013):
        adj = [np.array([[0.,0,0,1],[0,0.,1,0],[0,0,0.,0],[0,0,0,0.]]),
        np.array([[0.,0,0,1],[0,0.,1,1],[0,0,0.,0],[0,0,0,0.]]),
        np.array([[0.,0,0,1],[0,0.,1,1],[0,0,0.,0],[0,0,0,0.]]),
        np.array([[0.,0,0,1],[0,0.,0,1],[0,0,0.,0],[0,0,0,0.]]),
        np.array([[0.,0,0,1],[0,0.,0,1],[0,0,0.,0],[0,0,0,0.]]),
        np.array([[0.,0,1,1],[0,0.,0,1],[0,0,0.,0],[0,0,0,0.]])]
    elif(year==2014):
        adj = [np.array([[0.,0,0,0,0,0],[0,0.,0,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,0,0],[0,1,0,0,0.,0],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,0,0,0,0],[0,0,0.,0,0,0],[0,0,0,0.,0,0],[0,1,1,0,0.,0],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,0,0,0,1],[1,0,0.,0,0,0],[0,0,0,0.,0,0],[0,1,1,1,0.,0],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,0,0,0,1],[1,0,0.,0,0,0],[0,0,0,0.,0,0],[1,1,1,1,0.,0],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,0],[1,1,1,1,0.,1],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,0],[1,1,1,1,0.,1],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,1],[1,1,1,1,0.,1],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,1],[1,1,1,1,0.,1],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,1],[1,1,1,1,0.,1],[0,0,0,0,0,0.]]),
        np.array([[0.,1,0,0,0,0],[0,0.,1,0,0,1],[1,0,0.,0,0,0],[1,0,0,0.,0,1],[1,1,1,1,0.,1],[0,0,0,0,0,0.]])]
    elif(year==2015):
        adj = [np.zeros((10,10)) for k in range(9)]
        # round 1
        adj[0][0,9]=1; adj[0][8,1]=1; adj[0][2,7]=1; adj[0][6,3]=1; adj[0][4,5]=1
        # round 2
        adj[1] = deepcopy(adj[0])
        adj[1][9,5]=1; adj[1][6,4]=1; adj[1][3,7]=1
        # round 3
        adj[2] = deepcopy(adj[1])
        adj[2][1,9]=1; adj[2][3,8]=1
        # round 4
        adj[3] = deepcopy(adj[2])
        adj[3][2,1]=1
        # round 5
        adj[4] = deepcopy(adj[3])
        adj[4][3,1]=1; adj[4][7,6]=1
        # round 6
        adj[5] = deepcopy(adj[4])
        adj[5][9,7]=1; adj[5][8,6]=1; adj[5][4,1]=1
        # round 7
        adj[6] = deepcopy(adj[5])
        adj[6][9,3]=1; adj[6][2,4]=1
        # round 8
        adj[7] = deepcopy(adj[6])
        # round 9
        adj[8] = deepcopy(adj[7])
        adj[8][4,9]=1
    elif(year==2016):
        adj = [np.zeros((10,10)) for k in range(9)]
        # round 1
        adj[0][0,6]=1; adj[0][4,8]=1
        # round 2
        adj[1] = deepcopy(adj[0])
        adj[1][2,8]=1; adj[1][1,5]=1; adj[1][6,9]=1
        # round 3
        adj[2] = deepcopy(adj[1])
        # round 4
        adj[3] = deepcopy(adj[2])
        # round 5
        adj[4] = deepcopy(adj[3])
        adj[4][5,7]=1
        # round 6
        adj[5] = deepcopy(adj[4])
        adj[5][0,4]=1; adj[5][5,2]=1; adj[5][7,8]=1
        # round 7
        adj[6] = deepcopy(adj[5])
        # round 8
        adj[7] = deepcopy(adj[6])
        adj[7][2,6]=1; adj[7][8,9]=1
        # round 9
        adj[8] = deepcopy(adj[7])
        adj[8][3,9]=1; adj[8][6,7]=1
    elif(year==2017):
        adj = [np.zeros((10,10)) for k in range(9)]
        # round 1
        adj[0][0,9]=1; adj[0][2,7]=1; adj[0][4,5]=1
        # round 2
        adj[1] = deepcopy(adj[0])
        adj[1][5,9]=1; adj[1][8,2]=1; adj[1][1,0]
        # round 3
        adj[2] = deepcopy(adj[1])
        # round 4
        adj[3] = deepcopy(adj[2])
        adj[3][9,6]=1; adj[3][4,8]=1
        # round 5
        adj[4] = deepcopy(adj[3])
        adj[4][3,1]=1; adj[4][8,5]=1
        # round 6
        adj[5] = deepcopy(adj[4])
        adj[5][0,5]=1
        # round 7
        adj[6] = deepcopy(adj[5])
        adj[6][3,9]=1; adj[6][0,6]
        # round 8
        adj[7] = deepcopy(adj[6])
        adj[7][2,5]=1
        # round 9
        adj[8] = deepcopy(adj[7])
        adj[8][4,9]=1; adj[8][7,1]; adj[8][8,0]
    elif(year==2018):
        adj = [np.zeros((10,10)) for k in range(9)]
        # round 1
        adj[0][1,5]=1; adj[0][6,8]=0
        # round 2
        adj[1] = deepcopy(adj[0])
        adj[1][2,5]=1; 
        # round 3
        adj[2] = deepcopy(adj[1])
        adj[2][4,7]=1
        # round 4
        adj[3] = deepcopy(adj[2])
        adj[3][3,7]=1
        # round 5
        adj[4] = deepcopy(adj[3])
        # round 6
        adj[5] = deepcopy(adj[4])
        adj[5][3,5]=1
        # round 7
        adj[6] = deepcopy(adj[5])
        # round 8
        adj[7] = deepcopy(adj[6])
        # round 9
        adj[8] = deepcopy(adj[7])
        adj[8][1,4]=1; adj[8][2,7]=1
    return adj
            
#####################################################
#                 main                              #      
#####################################################
def main():
    years = [2013,2014,2015,2016,2017,2018]
    for k in range(len(years)):
        adj = data(years[k])
        print('Year'+str(years[k])+': ')
        for r in range(len(adj)):
            a = adj[r]
            print('\t Round'+str(r+1)+': ')
            print('\t \t specR = '+str('%.4f' % specR(a)))
            

main()