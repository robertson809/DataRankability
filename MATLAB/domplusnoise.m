%%% DOMGRAPH + NOISE function creates a dominance graph and adds some
%%% amount of noise. The goal is to use these carefully structured graphs
%%% with increasing noise to see if there is a correlation between our
%%% rankability measures and predictability measures. This code only
%%% creates unweighted D matrices.  See HILLSIDE + NOISE for weighted D
%%% matrices.
%%%
%%%    Input: n = number of rows/cols in D matrix
%%%           percentnoise = integer between 1 and n^2 representing the
%%%                          percentage of noise to add to D domgraph, e.g., 
%%%                          if percentnoise = 10, then 10% of the n^2
%%%                          elements will be noise
%%%    Example: 'D = domplusnoise(6,20)' creates a 6 by 6 matrix with 20% noise
%%%                 added to the dominance graph

function [D]=domplusnoise(n,percentnoise);
 
D=triu(ones(n,n),1);  % initialize D as perfect dominance graph
d=reshape(D,n^2,1);   % vector version of D matrix

% randperm(n,k) returns a row vector containing k unique integers selected randomly from 1 to n inclusive.
randlocations=randperm(n^2,floor(percentnoise*.01*n*n));  % these elements in D will be flipped
d(randlocations)=~d(randlocations); % flip the elements
D=reshape(d,n,n);  % D matrix now contains noise

for i=1:n
    D(i,i)=0;  % remove any self-loops that the noise matrix may have added
end