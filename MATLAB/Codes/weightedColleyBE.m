corrArray = zeros(18,1);
rankArray = zeros(18,1);
for year=1995:2012
    gameStr = strcat('../../data_files/CFB/Big East/',int2str(year),'games.txt');
    teamStr = strcat('../../data_files/CFB/Big East/',int2str(year),'teams.txt');
    dataStr = strcat('../../Python/DataMatrices/CFB/Big East/',int2str(year),'d4Matrix.csv');
    a = csvread(dataStr);
    rankArray(year-1994) = specR(a);
    r1 = rankingColley(gameStr,teamStr,0,[0.5 1],0.5,1,1);
    r2 = rankingColley(gameStr,teamStr,2,[0.5 1],0.5,1,1);
    r3 = rankingColley(gameStr,teamStr,2,[0.25 1 2],0.5,1,1);
    R = [r1,r2,r3];
    [~,pval] = corr(R);
    corrArray(year-1994) = max(max(triu(pval,1)));
end

[rho,pval] = corr([rankArray,corrArray])