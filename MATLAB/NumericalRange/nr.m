function c=nr(A);

% NR(A) estimates the boundary of the numerical range of
% a square complex matrix A, and its eigenvalues (stars).
%
% (Note that the command tic-toc prints the execution time.)
%
% Author: Panayiotis Psarrakos,
%         Department of Mathematics,
%         National Technical University of Athens.
%
% Let S be the Euclidean unit sphere in C^n and let 
% <.,.> denote the standard inner product in C^n. 
%
% For any A in C^{n times n}, we define the set 
%
%       W(A) = {<Ax,x>:x in S} 
%
% called the "numerical range" of A. The set W(A) is  
% also known as the "field of values" of A.
%
% This procedure uses an algorithm proposed in 
% [R.A. Horn and C.R. Johnson "Topics in Matrix 
% Analysis", Cambridge Univ. Press, New York, 1991].

tic 

nv=120;
n=max(size(A));
i=sqrt(-1);
e=eig(A);

for k=1:nv;
  z=exp(i*(k-1)/nv*2*pi);    % the angular of the rotation
  A1=z*A;                    % the rotation of matrix A   
  A2=(A1+A1')/2;             % the hermitian part of the rotation A1
  [X,D]=eig(A2);             % eigenvectors and eigenvalues of A2  
  [s,w] = sort(real(diag(D)));
  x=X(:,w(n));               % eigenvector of the maximum eigenvalue of A2
  f(k)=x'*A*x/(x'*x);        % boundary point of W(A)
end  % for

toc

f(nv+1)=f(1);               % connection of the last and the first vertices
%plot(real(f),imag(f),'b')   % plot the vertices of the polygon
%hold on
plot(real(e),imag(e),'*r')  % plot the eigenvalues
%xlabel('Real  Axis')
%ylabel('Imaginary  Axis')
%hold off
