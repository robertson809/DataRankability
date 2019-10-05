function [kstar,kworst]=HillsideHISTbruteforce(D)

% INPUT: D matrix of weighted dominance relations
% OUTPUT: hillside1 = k* (optimal k value =  minimum number of hillside
% violations)
%         fitness = n! by 1 vector of fitness values for all n! rankings

n=size(D,1);

% C matrices built from D

%Find C- by definition 2.1

for i=1:n
    for j=1:n
        C(i,j)=-nnz(D(:,j)-D(:,i)<0)-nnz(D(i,:)-D(j,:)<0);
    end
end

%%% This code computes the k-histogram using brute force
%%% total enumeration with smart nextperm.m code
i=1;
perm=[1:n]; % first permutation input to nextperm.m function is [1:n]
fitness(i)=sum(sum(C(perm,perm).*triu(ones(length(perm),length(perm)),1))); 

while sum(nextperm(perm,n) == perm)< n
    i=i+1;
    perm=nextperm(perm,n);
    fitness(i)=sum(sum(C(perm,perm).*triu(ones(length(perm),length(perm)),1)));
end 
fitness=-fitness;
kstar=min(fitness);
kworst=max(fitness);
% r_k=(kworst-kstar)/(kworst+kstar);
% nbins=kworst-kstar+1;
% figure(1)
% histogram(fitness,nbins)
% hillside1=kstar;
% sortedfitness=sort(fitness)
% sortedfitness(1:20)
% sortedfitness(length(fitness):-1:length(fitness)-19)