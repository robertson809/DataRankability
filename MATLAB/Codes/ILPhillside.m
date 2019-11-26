function [kstar,kworst]=ILPhillside(D)

%Get matrices for MPS file
%function [A,b,Aeq,beq,c]=ILPRatingDiff(D);

% using Yoshi's ILP idea to solve the rating diff. problem

% INPUT:   D = team-by-team data differential matrix, e.g. Markov voting
%               matrix
% OUTPUT:  hillsidek = optimal objective value

% C = matrix of cost coefficients

% SIMODS
%D=[0 1 0 0 0 1;0 0 1 0 0 0;0 1 0 0 0 0;1 0 0 0 0 1;0 0 0 0 0 0;0 1 1 0 0 0]

% completely connected
%D=[0 1 1 1 1 1;1 0 1 1 1 1;1 1 0 1 1 1;1 1 1 0 1 1; 1 1 1 1 0 1; 1 1 1 1 1 0]

% empty
%D=zeros(6,6)

% perfect dominance graph
% D=[0 1 1 1 1 1;0 0 1 1 1 1; 0 0 0 1 1 1; 0 0 0 0 1 1; 0 0 0 0 0 1;0 0 0 0
% 0 0]

% % Cyclic graph
% n=6;
% D=diag(ones(n-1,1),1);D(n,1)=1;

% NCD: 3-dom + 3-dom + 1 to 4
%D=[0 1 1 1 0 0;0 0 1 0 0 0;0 0 0 0 0 0;0 0 0 0 1 1;0 0 0 0 0 1;0 0 0 0 0 0];

n=size(D,1);

%later I'll fill in the code that creates the C matrices from D, for now
%I'm just inputing the Crminus that I built by hand from a 5-by-5 D

% C matrices built from D

%Find C- by definition 2.1
C = zeros(n,n);
for i=1:n
    for j=1:n
        C(i,j)=-nnz(D(:,j)-D(:,i)<0)-nnz(D(i,:)-D(j,:)<0);
    end
end
C
%build W- matrix
% for i=1:n
%     for j=1:n
%         colvec=D(:,j)-D(:,i);
%         rowvec=D(i,:)-D(j,:);
%         col=find(colvec<0);
%         row=find(rowvec<0);
%         W(i,j)=sum(colvec(col))+sum(rowvec(row));
%         clear col row colvec rowvec
%     end
% end
% 
% C=W;

c=reshape(C,n^2,1);
%c=reshape(Cmaxconf,n^2,1);

% create Aeq matrix and beq vector for Yoshi's CONSTRAINT 1
Aeq=spalloc(.5*n*(n-1),n^2,n*(n-1));
ncon1=0;
for j=1:n-1
    for i=j+1:n
        ncon1=ncon1+1;
        Aeq(ncon1,n*(j-1)+i)=1;
        Aeq(ncon1,n*(i-1)+j)=1;
    end
end
beq=ones(.5*n*(n-1),1);
Aeq

% 'Iterative BILP'
%  
% onesinlowertriangular=1;
% A=[];
% b=[];
% sizeA=0;
% while onesinlowertriangular>0
%     [x,fval,exitflag]=bintprog(-c,A,b,Aeq,beq);
%     X=reshape(x,n,n);
%     s=sum(X');
%     [value,perm]=sort(s,'descend');
%     Rank=perm';
%     ReorderedX=X(Rank,Rank);
%     [row,column]=find(ReorderedX);
%     onesinlowertriangular=0;
%     for i=1:length(row)
%         if column(i)<row(i)
%             onesinlowertriangular=onesinlowertriangular+1;
%             hadamardproduct=ReorderedX(column(i),:).*ReorderedX(:,row(i))';
%             findk=find(hadamardproduct);
%             for j=1:length(findk)
%                 newconstraint=zeros(n,n);
%                 newconstraint(row(i),column(i))=1;
%                 newconstraint(column(i),findk(j))=1;
%                 newconstraint(findk(j),row(i))=1;
%                 A(sizeA+1,:)=reshape(newconstraint,1,n^2);
%                 b(sizeA+1,1)=2;
%                 sizeA=sizeA+1;
%             end
%             clear hadamardproduct findk
%         end
%     end
% end
% 
% fval
% X
% Rank

% create A matrix and b vector for Yoshi's CONSTRAINT 2
A=spalloc(n*(n-1)*(n-2),n^2,6*n*(n-1)*(n-2));
ncon2=0;
for i=1:n
    for a=1:n-1
        j=setdiff(1:n,i);
        for b=1:n-2
            ncon2=ncon2+1;
            k=setdiff(1:n,[i j(b)]);
            A(ncon2,n*(j(a)-1)+i)=1;
            A(ncon2,n*(k(b)-1)+j(a))=1;
            A(ncon2,n*(i-1)+k(b))=1;
        end
    end
end
b=2*ones(n*(n-1)*(n-2),1);
A
% all variables must be integer, define lb and ub vectors
%intcon=[1:n*n]';
lb=zeros(n*n,1);
ub=ones(n*n,1);
% force xii=0 for all i by setting lb=0 and ub=0 for these indices
indicesxii=1:n+1:n^2;
lb(indicesxii)=0;
ub(indicesxii)=0;

% % solve BILP
% tic;
% %options = optimoptions(@intlinprog,'OutputFcn',@savemilpsolutions,'PlotFcn',@optimplotmilp);
% options = optimoptions(@intlinprog,'OutputFcn',@savemilpsolutions);
% [x,fval,exitflag,output] = intlinprog(-c,intcon,A,b,Aeq,beq,lb,ub,options);
% BILPtime=toc
% xIntSol=evalin('base','xIntSol');  % xIntSol is a matrix of the integer feasible points found in B&B procedure
% fIntSol=evalin('base','fIntSol') ; % fIntSol is a vector of the objective values associated with xIntSol


% solve LP Relaxation instead
options=optimoptions('linprog','Display','iter','Algorithm','interior-point-legacy','Diagnostics','on');
%options=optimoptions('linprog','Display','iter','Algorithm','dual-simplex','Diagnostics','on');
[x,fval,~,~] = linprog(-c,A,b,Aeq,beq,lb,ub,options);


fval
x
X=reshape(x,n,n)
return
s=sum(X,2);
kstar=fval;
[~,perm]=sort(s,'descend');
revPerm = flip(perm);
kworst = -sum(sum(C(revPerm,revPerm).*triu(ones(n,n))));
return