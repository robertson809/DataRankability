function writeWestCoastMBB()
A = zeros(18,2);
for i=2002:2019
    gamefilename = strcat('../data_files/ConferencesMBB/West_Coast/', int2str(i),...
        'games.txt');
    teamfilename = strcat('../data_files/ConferencesMBB/West_Coast/', int2str(i),...
        'teams.txt');
    A(i-2001,1)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
    A(i-2001,2)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
end
csvwrite('WestCoastMBBPredict.csv',A)