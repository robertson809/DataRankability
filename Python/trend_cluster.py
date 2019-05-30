# Trend and Cluster Analytics
# Thomas R. Cameron
# 4/12/2018
from numpy import random
from numpy import linspace
from scipy import linalg
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# create data
m = 3                                               # number of rows
n = 100                                             # number of columns
# data mimics ellipsoid with a=4.5, b=6, and c=3
a = 4.5; b=6.0; c=3.0
A = [[j for j in range(n)] for i in range(m)]
A[1][:] = -1.0*random.rand(n)+2.0*random.rand(n)
A[2][:] = [c**2*(1-A[1][j]**2/b**2-A[0][j]**2/a**2) for j in range(n)]

# mean and variance
e = [1.0 for j in range(n)]                                     # ones vector
u = linalg.blas.dgemv(1.0/n,A,e)                                # mean
C = [[A[i][j] - u[i]*e[j] for j in range(n)] for i in range(m)] # centered matrix
var = linalg.norm(C,'fro')**2/n                                 # variance

# Minimum Deviation Trend Line:
# line L for which the total sum of squares of orthogonal deviations between the data and L is minimal
# along all lines in R^m. This line is given by L={au1(C)+u | a is in R}, where u1(C) is the principal
# left-hand singular vector of the centered matrix C=A-ue^T=A(I-ee^T/n). You may also think of this
# line as the maximum variance trend line. The first left-hand singular vector u1(C) is called the principal
# component of the column data in A. 
U, s, V = linalg.svd(C)     # SVD of centered matrix C
u1 = U[:][0]
print u1
print linalg.norm(u1)

# Plot
fig = plt.figure()
ax = fig.add_subplot(111,projection='3d')
ax.scatter(A[0][:],A[1][:],A[2][:])
t = linspace(-1,1,1000)
x = u1[0]*t+u[0]
y = u1[1]*t+u[1]
z = u1[2]*t+u[2]
ax.plot(x,y,z,label='trend line',color='red')
plt.show()