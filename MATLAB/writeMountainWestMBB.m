function writeMountainWestMBB()
A = zeros(14,2);
for i=2002:2015
    gamefilename = strcat('../data_files/ConferencesMBB/Mountain_West/', int2str(i),...
        'games.txt');
    teamfilename = strcat('../data_files/ConferencesMBB/Mountain_West/', int2str(i),...
        'teams.txt');
    A(i-2001,1)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
    A(i-2001,2)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
end
csvwrite('MountainWestMBBPredict.csv',A)