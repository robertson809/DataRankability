function percentCorrect = MasseySeasonPercentageCorrect(gameFilename, teamFilename, verbose)
%% EXAMPLE: INPUT:
% r=MasseySeasonPercentageCorrect('NCAA_2008_Games.txt','NCAA_2008_Teams.txt', 'NCAA_2008_Madness_Teams.txt');
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
% Pull off just the days
% days=games(:,1); days may not match 

numGames = size(games, 1);

%% Build the Massey linear system

teamTeam = zeros(counter, counter);
b = zeros(numTeams,1); 
for i=1:numGames
    team1ID = games(i, 3);
    team1Score = games(i, 5);
    team2ID = games(i, 6);
    team2Score = games(i, 8);
    
    pointDifferential = abs(team2Score - team1Score); 
    
    if team1Score > team2Score
        % Team 1 won
        teamTeam(team2ID, team1ID) = teamTeam(team2ID, team1ID) + 1;
        b(team2ID) = b(team2ID) + (-pointDifferential);
        b(team1ID) = b(team1ID) + ( pointDifferential);
    else
        teamTeam(team1ID, team2ID) = teamTeam(team1ID, team2ID) + 1;
        b(team2ID) = b(team2ID) + (-pointDifferential);
        b(team1ID) = b(team1ID) + ( pointDifferential);
    end
end

%% Calculate linear system
losses = teamTeam * ones(numTeams,1); 
wins = (ones(1,numTeams) * teamTeam)';
masseyMatrix = -teamTeam -teamTeam';
diagM = wins + losses;
masseyMatrix = masseyMatrix + diag(diagM);

% Replace last row by ones and RHS by 0
masseyMatrix(end,:) = ones(numTeams,1); b(end) = 0; 

r = masseyMatrix\b; 
[sortedr,index]=sort(r,'descend');

%% Statistics to Output to Screen 
if (verbose)
    fprintf('\n\n************** MASSEY Rating Method **************\n\n');
    fprintf('===========================\n');
    fprintf('Rank   Rating      Team   \n');
    fprintf('===========================\n');
    for i=1:numTeams
        fprintf('%4d  %10.5f  %s\n',i,sortedr(i),cell2mat(teamNames(index(i))));
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

