n = 9; % number of teams
R = zeros(9,6); % memory for rankings

% compute rankings
R(:,1) = rankingColley('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',0,[0.5 1],0.5,1,1);
R(:,2) = rankingColley('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',1,[0.5 1],0.5,1,1);
R(:,3) = rankingColley('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',2,[0.5 1],0.5,1,1);
R(:,4) = rankingMassey('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',0,[0.5 1],0.5,1,1,20);
R(:,5) = rankingMassey('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',1,[0.5 1],0.5,1,1,20);
R(:,6) = rankingMassey('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',2,[0.5 1],0.5,1,1,20);

% compute correlation
[rho,pval]=corr(R);
rho
pval