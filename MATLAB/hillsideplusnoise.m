%%% HILLSIDE + NOISE function starts with a perfect hillside graph and adds some
%%% amount of noise. The goal is to use these carefully structured graphs
%%% with increasing noise to see if there is a correlation between our
%%% rankability measures and predictability measures. This code only
%%% creates weighted hillside D matrices.  See DOMGRAPH + NOISE for unweighted D
%%% matrices.
%%%
%%%    Input: n = number of rows/cols in D matrix
%%%           percentnoise = integer between 1 and n^2 representing the
%%%                          percentage of noise to add to D hillside, e.g., 
%%%                          if percentnoise = 10, then 10% of the n^2
%%%                          elements will be noise
%%%    Example: 'D = hillsideplusnoise(6,20)' creates a 6 by 6 matrix with 20% noise
%%%                 added to the hillside graph

function [D]=hillsideplusnoise(n,percentnoise);
 
v=[0:1:n-1];
D=triu(toeplitz(v));  % initialize D as a graph in hillside form. Other options are: D=(fliplr(pascal(n)))'; 
N=floor(n*sprand(n,n,.01*percentnoise))  % add random integers between 1 and n in random locations
D=D+N;   % D now has noise added, meaning that it now has violations from hillside form

for i=1:n
    D(i,i)=0;  % remove any self-loops that the noise matrix may have added
end