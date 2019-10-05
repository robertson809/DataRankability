function [hd] = hausdorff(e,s)
hd = max(specV(e,s),specV(s,e));
return