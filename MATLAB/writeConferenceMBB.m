function writeConferenceMBB()
    % store conferences
    conferences = {'America East';'Atlantic 10';'Atlantic Coast';'Atlantic Sun';'Big 10';'Big 12';'Big East';'Big Sky';
                    'Big South';'Big West';'Colonial';'Conference USA';'Horizon';
                    'Ivy League';'Metro Atlantic';'Mid-American';'Mid-Eastern AC';'Missouri Val';
                    'Mountain West';'Northeast';'OH Valley';'Patriot League';'Southeastern';
                    'Southern';'Southland';'Southwestern AC';'Sun Belt';'West Coast'};
    % Colley Predictability
    A = zeros(18,length(conferences));
    for i = 2002:2019
        for j = 1:length(conferences)
            gamefilename = strcat('../data_files/ALLMBB-Verbos/conference/', conferences{j}, '/', int2str(i),...
                'games.txt');
            teamfilename = strcat('../data_files/ALLMBB-Verbos/conference/', conferences{j}, '/', int2str(i),...
                'teams.txt');
            A(i-2001,j)=ColleySeasonPercentageCorrect(gamefilename,teamfilename,0);
        end
    end
    csvwrite('ColleyConferencePredictability.csv',A)
    % Massey Predictability
    A = zeros(18,length(conferences));
    for i = 2002:2019
        for j = 1:length(conferences)
            gamefilename = strcat('../data_files/ALLMBB-Verbos/conference/', conferences{j}, '/', int2str(i),...
                'games.txt');
            teamfilename = strcat('../data_files/ALLMBB-Verbos/conference/', conferences{j}, '/', int2str(i),...
                'teams.txt');
            A(i-2001,j)=MasseySeasonPercentageCorrect(gamefilename,teamfilename,0);
        end
    end
    csvwrite('MasseyConferencePredictability.csv',A)