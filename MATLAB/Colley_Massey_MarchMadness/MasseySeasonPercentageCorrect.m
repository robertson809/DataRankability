function percentCorrect = MasseySeasonPercentageCorrect(gameFilename, teamFilename, weighting, weightHomeWin, weightAwayWin, weightNeutralWin, maxScore, k)
%% EXAMPLE: INPUT:
%% r=scoreMasseyESPN('NCAA_2008_Games.txt','NCAA_2008_Teams.txt', 'NCAA_2008_Madness_Teams.txt', 0, 20);
%% 
%% 'NCAA-3-9-09.txt' is a game data file from Massey rating data server, 
%% which can be found at http://www.masseyratings.com/. For 2010 results go
%% to http://masseyratings.com/scoresx.php?t=11590&s=97288&all=1 and
%% download a matlab file of games selecting the intra option.
%% '2009_teams.txt' is the corresponding team name file from the Massey data server.
%% weighting:
%%      0 means no (or uniform)
%%      1 means linear time
%% k = scalar for number of top ranked teams to list 
%% OUTPUT: r = Masseyrating vector

selectionSundayList = {'03/10/2002','03/16/2003','03/14/2004','03/13/2005','03/12/2006',...
    '03/11/2007','03/16/2008','03/15/2009','03/14/2010','03/13/2011',...
    '03/11/2012','03/17/2013','03/16/2014','03/15/2015','03/13/2016','03/12/2017','03/11/2018'};

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
% Pull off just the days
% days=games(:,1); days may not match 
dayColumn = mod(games(:,2),100); 
monthColumn = mod(floor(games(:,2)/100),100);
yearColumn = floor(games(:,2)/(100*100)); 
days = datenum(yearColumn,monthColumn,dayColumn); 

%% Pull off year
lastDateYear = games(end,2);
yearOfData = floor(lastDateYear/10000);
selectionSunday = datenum(selectionSundayList{yearOfData - 2001});

numGames =  length(find(days <= selectionSunday));
% This is the number of games played prior to the tournament. 

%% Find March Madness teams 
marchMadnessTeams = [games(end,3), games(end,6)];
numTotalGames = size(games,1);
for i=numTotalGames:-1:1
    currentDay = mod(games(i,2),100); 
	currentMonth = mod(floor(games(i,2)/100),100);
	currentYear = floor(games(i,2)/(100*100)); 
    daysAfter2000 = datenum(currentYear,currentMonth,currentDay); 

    if (daysAfter2000 <= selectionSunday)
        break;
    end
    teamsInGame = [games(i,3),games(i,6)];
    if ~isempty(intersect(teamsInGame,marchMadnessTeams))
        marchMadnessTeams = union(teamsInGame,marchMadnessTeams);
    end
end

%% Calculate the weights

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
elseif weighting==2   
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   % INSERT YOUR WEIGHTING HERE
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
    fprintf('\nPerforming my personal weighting.\n'); 
%    segmentWeighting = [.3 .8 1.2 1.5]; 
    segmentWeighting = [1,1.5,2,3,4,7];
    w=ones(numGames, 1); 
    for i=1:numGames
        weightIndex = ceil((days(i)-days(1)+1)/(days(numGames)-days(1)+1)*length(segmentWeighting)); 
        w(i) = segmentWeighting(weightIndex);
    end
    %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
   % EDIT BELOW THIS LINE AT YOUR OWN RISK! :-) 
   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%   
else
   fprintf('No weighting indicated so default of uniform weighting will be assumed.\n'); 
   % No Weighting
    w=ones(numGames, 1); 
end

teamTeam = zeros(counter, counter);
b = zeros(numTeams,1); 
for i=1:numGames
%   daysAfter2000 = games(i, 1);
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

%% Find the number of correct predictions
predictedWins = zeros(numTeams,1); 
missedWins = zeros(numTeams,1); 
for i=1:numGames
    team1ID = games(i, 3);
    team1Score = games(i, 5);
    team2ID = games(i, 6);
    team2Score = games(i, 8);
    
    if (team1Score > team2Score) && (r(team1ID) > r(team2ID))
        predictedWins(team1ID) = predictedWins(team1ID) + 1;
    elseif (team1Score > team2Score) && (r(team1ID) < r(team2ID))
        missedWins(team1ID) = missedWins(team1ID) + 1;
    elseif (team2Score > team1Score) && (r(team2ID) > r(team1ID))
        predictedWins(team2ID) = predictedWins(team2ID) + 1;
    elseif (team2Score > team1Score) && (r(team2ID) < r(team1ID))
        missedWins(team2ID) = missedWins(team2ID) + 1;
    end
end

percentCorrect = sum(predictedWins)/(sum(predictedWins) + sum(missedWins));
