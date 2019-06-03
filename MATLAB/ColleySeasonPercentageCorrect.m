function [percentCorrect] = ColleySeasonPercentageCorrect(gameFilename, teamFilename, verbose)
%% EXAMPLE: INPUT:%% r=ColleySeasonPercentageCorrectCFB('NCAA_2008_Games.txt','NCAA_2008_Teams.txt');
%
% 'NCAA-3-9-09.txt' is a game data file from Massey rating data server,
% which can be found at http://www.masseyratings.com/. For 2010 results go
% to http://masseyratings.com/scoresx.php?t=11590&s=97288&all=1 and
% download a matlab file of games selecting the intra option.
% '2009_teams.txt' is the corresponding team name file from the Massey data server.
% verbose 
%    0 - minimal output
%    1 - print more output 
%% Load the team names into an array
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

numGames = size(games, 1);

%% Build Colley linear system

teamTeam = zeros(numTeams, numTeams);
for i=1:numGames
    %   daysAfter2000 = games(i, 1);
    team1ID = games(i, 3);
    team1Score = games(i, 5);
    team2ID = games(i, 6);
    team2Score = games(i, 8);
    
    if team1Score > team2Score
        teamTeam(team2ID, team1ID) = teamTeam(team2ID, team1ID) + 1;
    else
        teamTeam(team1ID, team2ID) = teamTeam(team1ID, team2ID) + 1;
    end
end

%% Calculate linear system
losses = teamTeam * ones(numTeams,1);
wins = (ones(1,numTeams) * teamTeam)';
colleyMatrix = -teamTeam -teamTeam';
diagC = wins + losses + 2;
colleyMatrix = colleyMatrix + diag(diagC);

b = .5*(wins-losses) + 1;

r = colleyMatrix\b;
[sortedr,index]=sort(r,'descend');

%% Statistics to Output to Screen 
if (verbose)
    fprintf('\n\n************** COLLEY Rating Method **************\n\n');
    fprintf('===========================\n');
    fprintf('Rank   Rating    Team   \n');
    fprintf('===========================\n');
    for i=1:numTeams
        fprintf('%4d  %8.5f  %s\n',i,sortedr(i),cell2mat(teamNames(index(i))));
    end
    
    fprintf('\n');   % extra carriage return
end

%% Find the number of correct predictions
predictedWins = zeros(numTeams,1);
missedWins = zeros(numTeams,1);
for i=1:numGames
    team1ID = games(i, 3);
    team1Score = games(i, 5);
    team2ID = games(i, 6);
    team2Score = games(i, 8);
    
    if (r(team1ID) == r(team2ID))
        fprintf('There is a tie between %s and %s\n',cell2mat(teamNames(team1ID)), cell2mat(teamNames(team2ID)))
    elseif (team1Score > team2Score) && (r(team1ID) > r(team2ID))
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

if verbose
    fprintf('\nPredictability = %d/%d = %f\n',sum(predictedWins),sum(predictedWins) + sum(missedWins), percentCorrect);
end

