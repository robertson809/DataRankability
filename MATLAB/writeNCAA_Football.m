function writeNCAA_Football()
A = zeros(24,2);
for i=1995:2018
    gamefilename = strcat('../data_files/NCAA_D1_Football/', int2str(i),...
        'games.txt');
    teamfilename = strcat('../data_files/NCAA_D1_Football/', int2str(i),...
        'teams.txt');
    A(i-1994,1)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
    A(i-1994,2)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
end
csvwrite('NCAA_Football_Predict.csv',A)