%% CFB SIMOD Rankability
format long
conf = ['Big 12','FBS Indep','Mid-American'];
r = zeros(23,3);
for k=1:3
    for year=1995:2012
        % print year
        year
        % open file
        fid = fopen(strcat('../data_files/CFB/',int2str(conf(k)),'/',int2str(year),'games.txt'));
        % initalize team and score arrays
        teami = [];
        scorei = [];
        teamj = [];
        scorej = [];
        % get first line
        games = fgetl(fid);
        % proceed to get all remaining lines and data
        while(games>0)
            % split string
            games = strsplit(games,',');
            % record team and game data
            teami = [teami, str2num(games{3})];
            teamj = [teamj, str2num(games{6})];
            scorei = [scorei, str2num(games{5})];
            scorej = [scorej, str2num(games{8})];
            % get next line
            games = fgetl(fid);
        end
        % close file
        fclose(fid);
        % number of teams and games
        numGames = length(teami);
        numTeams = max(max(teami),max(teamj));
        % create games matrix
        games = zeros(numTeams);
        for k=1:numGames
            i = teami(k);
            j = teamj(k);
            if(scorei(k)>scorej(k))
                games(i,j) = games(i,j) + 1;
            else
                games(j,i) = games(j,i) + 1;
            end
        end
        % create adjacency matrix
        adj = zeros(numTeams);
        for i=1:numTeams
            for j=1:numTeams
                total = games(i,j)+games(j,i);
                if(total~=0)
                    adj(i,j) = games(i,j)/total;
                    adj(j,i) = games(j,i)/total;
                end
            end
        end
        % compute SIMOD rankability
        [k,p,P,stats] = rankability_exhaustive(adj);
        kmax = (numTeams*numTeams-numTeams)/2;
        pmax = factorial(numTeams);
        r(year-1994,k) = 1 - (k*p)/(kmax*pmax);
    end
end
csvwrite('CSV/CFB_Simod_Rankability.csv',r)