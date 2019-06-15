function writeMBB()
    A = zeros(17,2);
    for i=2002:2018
        gamefilename = strcat('../data_files/ALLMBB-Verbos/', int2str(i),...
            'games.txt');
        teamfilename = strcat('../data_files/ALLMBB-Verbos/', int2str(i),...
            'teams.txt');
        A(i-2001,1)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
        A(i-2001,2)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
    end
    csvwrite('MBBPredict.csv',A)