function [hill,rank] = hillSQfield()

hill = zeros(1,7);
rank = zeros(1,7);
for year=2013:2015
    dataStr = strcat('../../data_files/SinquefieldCup/SinquefieldCup',int2str(year),'.csv');
    fid = fopen(dataStr);
    info = fgetl(fid);
    info = strsplit(info,',');
    numPlayers = str2num(info{1});
    numRounds = str2num(info{2});
    
    a = zeros(numPlayers,numPlayers);
    for k=1:numRounds
        for n=1:numPlayers/2
            info = fgetl(fid);
            info = strsplit(info,',');
            i = str2num(info{1});
            j = str2num(info{3});
            score = str2num(info{2});
            if(score>0)
                a(i,j) = a(i,j) + 1;
            elseif(score<0)
                a(j,i) = a(j,i) + 1;
            else
                a(i,j) = a(i,j) + 1/2;
                a(j,i) = a(j,i) + 1/2;
            end
        end
        d = zeros(numPlayers,numPlayers);
        for i=1:numPlayers
            for j=i+1:numPlayers
                total = a(i,j) + a(j,i);
                if(total ~= 0)
                    d(i,j) = a(i,j)/total;
                    d(j,i) = a(j,i)/total;
                end
            end
        end
        rank(k,year-2012) = specR(d);
        [kstar,kworst,p]=HillsideHISTbruteforce(d);
        hill(k,year-2012) = 1 - kstar*p/(kworst*factorial(numPlayers));
    end
end

corr(rank(1:6,1),hill(1:6,1))
corr(rank(1:10,2),hill(1:10,2))
corr(rank(1:9,2),hill(1:9,3))