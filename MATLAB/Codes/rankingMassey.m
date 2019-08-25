function [rankingOrder] = rankingMassey(gameFilename, teamFilename, weighting, segmentWeighting, weightHomeWin, weightAwayWin, weightNeutralWin, maxScore)
%% EXAMPLE: INPUT:
%% r=rankingMassey('2008Games.txt','2008Teams.txt', 0, [.5 1], .5, 1, 1,20);
%% 
%% gameFilename - game data file 
%% teamFilename - corresponding team name file
%% weighting:
%%      0 = no (or uniform)
%%      1 = linear time
%%      2 = interval weighting 
%% segmentWeighting - vector where season broken into length(segmentWeighting)
%%       equally spaced intervals where games in that interval are given 
%%       corresponding weight for the game. 
%% weightHomeWin - a win at home is given this weight for the game
%% weightAwayWin - a win away is given this weight for the game
%% weightNeuralWin - a win on neutral court is given this weight for the game
%% maxScore - for any win over maxScore points, treat it as a win by maxScore
%%
%% OUTPUT: rankingOrder = Massey ranking
%%              rankingOrder(1) equals the team index of the 1st place team

% Load the team names into an array
fid = fopen(teamFilename);
counter = 0; 
teamname = fgetl(fid);
while (ischar(teamname))
    counter = counter + 1;
    [token, remain] = strtok(teamname); teamname = strtok(remain); 
    teamname=cellstr(teamname);
    teamNames(counter) = teamname;
    teamname = fgetl(fid);
end
fclose(fid);
numTeams = counter;

%% Load the games
games=load(gameFilename);
% columns of games are: 
%	column 1 = days since 1/1/0000
%	column 2 = date in YYYYMMDD format
%	column 3 = team1 index 
%	column 4 = team1 homefield (1 = home, -1 = away, 0 = neutral) 
%	column 5 = team1 score 
%	column 6 = team2 index 
%	column 7 = team2 homefield (1 = home, -1 = away, 0 = neutral) 
%	column 8 = team2 score 

numGames =  length(games);

%% Calculate the weights of games

%create weight vector w 
w=zeros(numGames, 1); 

if weighting==0
    % No Weighting
    w=ones(numGames, 1); 
elseif weighting==1
    % for linear weighted time
    for i=1:numGames
        w(i)=(days(i)-days(1))/(days(numGames)-days(1)); 
    end
elseif weighting==2   % Segment weighting
    w=ones(numGames, 1); 
    for i=1:numGames
        weightIndex = ceil((days(i)-days(1)+1)/(days(numGames)-days(1)+1)*length(segmentWeighting)); 
        w(i) = segmentWeighting(weightIndex);
    end
else
   fprintf('No weighting indicated so default of uniform weighting will be assumed.\n'); 
   % No Weighting
    w=ones(numGames, 1); 
end

teamTeam = zeros(counter, counter);
b = zeros(numTeams,1); 
for i=1:numGames
    team1ID = games(i, 3);
    team1Score = games(i, 5);
    team1Loc = games(i, 4);
    team2ID = games(i, 6);
    team2Score = games(i, 8);
    team2Loc = games(i, 7);
    
    pointDifferential = abs(team2Score - team1Score); 
    if (pointDifferential > maxScore)
        pointDifferential = maxScore; 
    end
    
    if team1Score > team2Score
        % Team 1 won
        if (team1Loc == 1)       % Home win
            teamTeam(team2ID, team1ID) = teamTeam(team2ID, team1ID) + weightHomeWin*w(i);
            b(team2ID) = b(team2ID) + weightHomeWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightHomeWin*w(i)*( pointDifferential);
        elseif (team1Loc == -1)  % Away win            
            teamTeam(team2ID, team1ID) = teamTeam(team2ID, team1ID) + weightAwayWin*w(i);
            b(team2ID) = b(team2ID) + weightAwayWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightAwayWin*w(i)*( pointDifferential);
        else                       % Neutral court win
            teamTeam(team2ID, team1ID) = teamTeam(team2ID, team1ID) + weightNeutralWin*w(i);
            b(team2ID) = b(team2ID) + weightNeutralWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightNeutralWin*w(i)*( pointDifferential);
        end
    else
        % Team 2 Won
        if (team2Loc == 1)       % Home win
            teamTeam(team1ID, team2ID) = teamTeam(team1ID, team2ID) + weightHomeWin*w(i);
            b(team2ID) = b(team2ID) + weightHomeWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightHomeWin*w(i)*( pointDifferential);
        elseif (team2Loc == -1)  % Away win            
            teamTeam(team1ID, team2ID) = teamTeam(team1ID, team2ID) + weightAwayWin*w(i);
            b(team2ID) = b(team2ID) + weightAwayWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightAwayWin*w(i)*( pointDifferential);
        else                       % Neutral court win
            teamTeam(team1ID, team2ID) = teamTeam(team1ID, team2ID) + weightNeutralWin*w(i);
            b(team2ID) = b(team2ID) + weightNeutralWin*w(i)*(-pointDifferential);
            b(team1ID) = b(team1ID) + weightNeutralWin*w(i)*( pointDifferential);
        end
    end
end

%% Calculate linear system
weightedLosses = teamTeam * ones(numTeams,1); 
weightedWins = (ones(1,numTeams) * teamTeam)';
weightedC = -teamTeam -teamTeam';
diagWeightedC = weightedWins + weightedLosses;
weightedC = weightedC + diag(diagWeightedC);

% Replace last row by ones and RHS by 0
weightedC(end,:) = ones(numTeams,1); b(end) = 0; 

r = weightedC\b; 
[sortedr,index]=sort(r,'descend');

rankingOrder = index;
