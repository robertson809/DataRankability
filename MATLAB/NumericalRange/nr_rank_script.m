% script for numerical range and rankability examples

% perfect dominance graph Laplacian on 4 vertices
l = [3 -1 -1 -1; 0 2 -1 -1; 0 0 1 -1; 0 0 0 0];
% q matrix
q = [1 1 1; - 1 1 1; 0 -2 1; 0 0 -3];
for j=1:3
    q(:,j) = q(:,j)/norm(q(:,j));
end
% projection transformation
a = transpose(q)*l*q
% numerical range
nr(a)