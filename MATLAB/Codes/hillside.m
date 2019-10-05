function [kstar,kworst] = hillside(sport,conf,year)

dataStr = strcat('../../Python/DataMatrices/',sport,'/',conf,'/',int2str(year),'d4Matrix.csv');
a = csvread(dataStr);
[kstar,kworst]=HillsideHISTbruteforce(a);