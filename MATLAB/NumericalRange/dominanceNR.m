q = [[1,-1,0,0,0,0];[1,1,-2,0,0,0];[1,1,1,-3,0,0];[1,1,1,1,-4,0];[1,1,1,1,1,-5]];
for i=1:5
q(:,i) = q(:,i)/norm(q(:,i));
end
a = [[0,1,1,1,1,1];[0,0,1,1,1,1];[0,0,0,1,1,1];[0,0,0,0,1,1];[0,0,0,0,0,1];[0,0,0,0,0,0]];
d = eye(6);
for i = 1:6
d(i,i) = 7 - i;
end
l = d - a;
sym = 1/2*(l + l')