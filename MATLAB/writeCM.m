function writeBigEast()
A = zeros(18,2);
for i=1995:2012
    gamefilename = strcat('../data_files/Big_East/', int2str(i),...
        'games.txt');
    teamfilename = strcat('../data_files/Big_East/', int2str(i),...
        'teams.txt');
    A(i-1994,1)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
    A(i - 1994,2)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
end
csvwrite('output.csv',A)