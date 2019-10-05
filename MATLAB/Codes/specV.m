function [sv] = specV(e,s)

n = length(e);
m = length(s);
row = zeros(m,1);
col = zeros(n,1);
for i=1:n
    for j=1:m
        row(j) = abs(e(i)-s(j));
    end
    col(i) = min(row);
end
sv = max(col);
return