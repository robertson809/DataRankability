m=9;
n=9;
X=rand(n);
for j=1:n
    X(:,j)=X(:,j)/vecnorm(X(:,j),1);
end

R=zeros(m,n);
for j=1:n
    R(:,j)=rankingColley('../../data_files/CFB/Mountain West/2009games.txt','../../data_files/CFB/Mountain West/2009teams.txt',2,X(j,:),0.5,1,1);
end
[rho,pval]=corr(R);
rho
pval