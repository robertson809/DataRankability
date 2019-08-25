%% SIMOD Rankability Examples

a1 = [[0.,1,1,1,1,1];[0,0.,1,1,1,1];[0,0,0.,1,1,1];[0,0,0,0.,1,1];[0,0,0,0,0.,1];[0,0,0,0,0,0.]];
a2 = [[0.,1,1,1,1,1];[0,0.,0,1,1,1];[1,0,0.,1,1,1];[0,0,0,0.,1,1];[0,0,0,0,0.,1];[0,0,0,0,0,0.]];
a3 = [[0.,1,1,0,0,1];[0,0.,0,1,1,0];[0,0,0.,0,0,0];[1,1,0,0.,0,1];[1,1,0,0,0.,0];[1,1,1,0,1,0.]];
a4 = [[0.,1,1,1,0,0];[0,0.,1,0,0,0];[0,0,0.,0,0,0];[0,0,0,0.,1,1];[0,0,0,0,0.,1];[0,0,0,0,0,0.]];
a5 = [[0.,1,1,0,0,1];[0,0.,0,1,1,0];[0,0,0.,0,0,0];[1,0,0,0.,0,1];[1,1,0,0,0.,0];[0,1,1,0,1,0.]];
a6 = [[0.,1,0,0,0,0];[0,0.,1,0,0,0];[0,0,0.,1,0,0];[0,0,0,0.,1,0];[0,0,0,0,0.,1];[1,0,0,0,0,0.]];
a7 = [[0.,1,1,1,1,1];[1,0.,1,1,1,1];[1,1,0.,1,1,1];[1,1,1,0.,1,1];[1,1,1,1,0.,1];[1,1,1,1,1,0.]];
a8 = zeros(6);

[k,p] = rankability_exhaustive(a1);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a2);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a3);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a4);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a5);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a6);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a7);
sprintf('%.4f',1 - k*p/10800)
[k,p] = rankability_exhaustive(a8);
sprintf('%.4f',1 - k*p/10800)