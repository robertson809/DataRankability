function [pval] = WColleyRCorr(conf,startYear,endYear)

n = endYear-startYear+1;
corrArray = zeros(n,1);
rankArray = zeros(n,1);

for year=startYear:endYear
    gameStr = strcat('../../data_files/CFB/',conf,'/',int2str(year),'games.txt');
    teamStr = strcat('../../data_files/CFB/',conf,'/',int2str(year),'teams.txt');
    dataStr = strcat('../../Python/DataMatrices/CFB/',conf,'/',int2str(year),'d4Matrix.csv');
    
    a = csvread(dataStr);
    rankArray(year-startYear+1) = specR(a);
    
    r1 = rankingColley(gameStr,teamStr,0,[0.5 1],1,1,1);
    r2 = rankingColley(gameStr,teamStr,2,[0.5 1],1,1,1);
    r3 = rankingColley(gameStr,teamStr,2,[1/3 1/3 1/3],1,1,1);
    r4 = rankingColley(gameStr,teamStr,2,[0.25 0.5 1 2],1,1,1);
    r5 = rankingColley(gameStr,teamStr,0,[0.5 1],0.5,1,1);
    r6 = rankingColley(gameStr,teamStr,2,[0.5 1],0.5,1,1);
    r7 = rankingColley(gameStr,teamStr,2,[1/3 1/3 1/3],0.5,1,1);
    r8 = rankingColley(gameStr,teamStr,2,[0.25 0.5 1 2],0.5,1,1);
    R = [r1,r2,r3,r4,r5,r6,r7,r8];
    [~,pval] = corr(R);
    corrArray(year-startYear+1) = max(max(triu(pval,1)));
end

[~,pval] = corr([rankArray,corrArray]);
pval = pval(1,2);