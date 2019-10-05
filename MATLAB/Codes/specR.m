function [r] = specR(a)
n = length(a);
x = sum(a,2);
l = diag(x) - a;
e = eig(l);
s = zeros(n,1);
for i=1:n
    s(i) = n-i;
end
r = 1 - ((hausdorff(e,s) + hausdorff(x,s))/(2*(n-1)));
return