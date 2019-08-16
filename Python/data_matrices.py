# DATA_MATRICES: Create data matrices from games data for college football and basketball
#
# Author: Thomas R. Cameron
# Date: 6/23/2019
import os
import errno
import numpy as np

#####################################################
#                 MKDIR_P                           # 
#####################################################
#  Creates directory in Write Data function so that
#   Python 2.7 can be used.
#####################################################
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

#####################################################
#                 Read Data                         # 
#####################################################
#   Reads in data from MBB or CFB and returns three data
#   matrices d1, d2, d3, and d4. Note that d1 is 
#   point-differential data, d2 is point-score data, 
#   d3 is point-ratio data, and d4 is simply win-loss
#   data. If teams played more than once, then we take 
#   the cummalitive measure for d1, and the average 
#   measures for d2, d3, and d4. 
#####################################################
def Read_Data(sport,conf,year):
    # open game file
    if(sport=='MBB'):
        f = open('../data_files/MBB/conference/'+conf+'/'+str(year)+'games.txt')
    else:
        f = open('../data_files/CFB/'+conf+'/'+str(year)+'games.txt')
    # read lines
    lineList = f.readlines()
    # store team and score info
    numGames = len(lineList)
    teami = []
    scorei = []
    teamj = []
    scorej = []
    for k in range(numGames):
        row = lineList.pop(0)
        row = row.split(",")
        teami.append(eval(row[2]))
        scorei.append(eval(row[4]))
        teamj.append(eval(row[5]))
        scorej.append(eval(row[7]))
    # create data matrices
    numTeams = max(max(teami),max(teamj))
    d1 = np.zeros((numTeams,numTeams))
    d2 = np.zeros((numTeams,numTeams))
    d3 = np.zeros((numTeams,numTeams))
    d4 = np.zeros((numTeams,numTeams))
    games = np.zeros((numTeams,numTeams))
    for k in range(numGames):
        i = teami[k] - 1
        j = teamj[k] - 1
        # record game
        games[i,j] = games[i,j] + 1
        games[j,i] = games[j,i] + 1
        # point-differential
        if(scorei[k]>scorej[k]):
            d1[i,j] = d1[i,j] + (scorei[k] - scorej[k])
        else:
            d1[j,i] = d1[j,i] + (scorej[k] - scorei[k])
        # point-score
        d2[i,j] = d2[i,j] + scorei[k]
        d2[j,i] = d2[j,i] + scorej[k]
        # point-ratio
        d3[i,j] = d3[i,j] + scorei[k]/(scorei[k]+scorej[k])
        d3[j,i] = d3[j,i] + scorej[k]/(scorei[k]+scorej[k])
        # win-loss
        if(scorei[k]>scorej[k]):
            d4[i,j] = d4[i,j] + 1
        else:
            d4[j,i] = d4[j,i] + 1
    # normalize d2, d3, and d4
    for i in range(numTeams):
        for j in range(numTeams):
            if(games[i,j]!=0):
                d2[i,j] = d2[i,j]/games[i,j]
                d3[i,j] = d3[i,j]/games[i,j]
                d4[i,j] = d4[i,j]/games[i,j]
    # return
    return d1, d2, d3, d4
    
#####################################################
#                 Write Data                        # 
#####################################################
#   Write MBB or CFB data matrices to file and save in 
#   respective conference and year folder. 
#####################################################
def Write_Data(sport,conf,year,num,d):
    #os.makedirs(os.path.dirname('DataMatrices/'+sport+'/'+conf+'/'),exist_ok=True)
    mkdir_p('DataMatrices/'+sport+'/'+conf+'/')
    f = open('DataMatrices/'+sport+'/'+conf+'/'+str(year)+'d'+str(num)+'Matrix.csv','w+')
    n = len(d)
    for i in range(n):
        # write ith row
        for j in range(n-1):
            f.write(str('%.2f' % d[i,j])+', ')
        # last entry
        j = n-1
        f.write(str('%.2f' % d[i,j])+'\n')
    # close file
    f.close()

#####################################################
#                 Main                              # 
#####################################################
#   Create data matrices for specified conferenes
#   and years of CFB and MBB.
#####################################################
def main():
    # MBB Data
    conf = ['America East','Atlantic 10','Atlantic Coast','Atlantic Sun','Big 10','Big 12','Big East','Big Sky',
            'Big South','Big West','Colonial','Conference USA','Horizon','Ivy League','Metro Atlantic','Mid-American',
            'Mid-Eastern AC','Missouri Val','Mountain West','Northeast','OH Valley','Patriot League','Southeastern',
            'Southern','Southland','Southwestern AC','Sun Belt','West Coast']
    for k in range(len(conf)):
        for year in range(2002,2020):
            d1, d2, d3, d4 = Read_Data('MBB',conf[k],year)
            Write_Data('MBB',conf[k],year,1,d1)
            Write_Data('MBB',conf[k],year,2,d2)
            Write_Data('MBB',conf[k],year,3,d3)
            Write_Data('MBB',conf[k],year,4,d4)
    # CFB Data
    # Atlantic Coast
    for year in range(1995,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Atlantic Coast',year)
        Write_Data('CFB','Atlantic Coast',year,1,d1)
        Write_Data('CFB','Atlantic Coast',year,2,d2)
        Write_Data('CFB','Atlantic Coast',year,3,d3)
        Write_Data('CFB','Atlantic Coast',year,4,d4)
    # Big 10
    for year in range(1995,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Big 10',year)
        Write_Data('CFB','Big 10',year,1,d1)
        Write_Data('CFB','Big 10',year,2,d2)
        Write_Data('CFB','Big 10',year,3,d3)
        Write_Data('CFB','Big 10',year,4,d4)
    # Big 12
    for year in range(1996,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Big 12',year)
        Write_Data('CFB','Big 12',year,1,d1)
        Write_Data('CFB','Big 12',year,2,d2)
        Write_Data('CFB','Big 12',year,3,d3)
        Write_Data('CFB','Big 12',year,4,d4)
    # Big East
    for year in range(1995,2013):
        d1, d2, d3, d4 = Read_Data('CFB','Big East',year)
        Write_Data('CFB','Big East',year,1,d1)
        Write_Data('CFB','Big East',year,2,d2)
        Write_Data('CFB','Big East',year,3,d3)
        Write_Data('CFB','Big East',year,4,d4)
    # Mid-American
    for year in range(1995,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Mid-American',year)
        Write_Data('CFB','Mid-American',year,1,d1)
        Write_Data('CFB','Mid-American',year,2,d2)
        Write_Data('CFB','Mid-American',year,3,d3)
        Write_Data('CFB','Mid-American',year,4,d4)
    # Mountain West
    for year in range(1999,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Mountain West',year)
        Write_Data('CFB','Mountain West',year,1,d1)
        Write_Data('CFB','Mountain West',year,2,d2)
        Write_Data('CFB','Mountain West',year,3,d3)
        Write_Data('CFB','Mountain West',year,4,d4)
    # Pac 12
    for year in range(2013,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Pac 12',year)
        Write_Data('CFB','Pac 12',year,1,d1)
        Write_Data('CFB','Pac 12',year,2,d2)
        Write_Data('CFB','Pac 12',year,3,d3)
        Write_Data('CFB','Pac 12',year,4,d4)
    # SEC
    for year in range(1995,2019):
        d1, d2, d3, d4 = Read_Data('CFB','Southeastern',year)
        Write_Data('CFB','Southeastern',year,1,d1)
        Write_Data('CFB','Southeastern',year,2,d2)
        Write_Data('CFB','Southeastern',year,3,d3)
        Write_Data('CFB','Southeastern',year,4,d4)

main()