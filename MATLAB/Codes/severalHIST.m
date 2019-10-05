%% script for displaying several histograms on one plot

nbins=length(fitness1);



map = brewermap(4,'Set1'); 
newplot
figure(1)
histogram(Patriot2005rankable,nbins,'FaceColor',map(1,:),'FaceAlpha',.5,'EdgeColor',map(1,:),'EdgeAlpha',.5)
hold on
histogram(Patriot2008unrankable,nbins,'FaceColor',map(2,:),'FaceAlpha',.5,'EdgeColor',map(2,:),'EdgeAlpha',.5)
hold on
histogram(perfectrankableplus5noise,nbins,'FaceColor',map(3,:),'FaceAlpha',.5,'EdgeColor',map(3,:),'EdgeAlpha',.5)
%hold on
%histogram(perfectrankableplus5noise,nbins,'FaceColor',map(4,:),'FaceAlpha',.2,'EdgeColor',map(4,:),'EdgeAlpha',.2)
%histf(emptyunrankableplus10noise,nbins,'FaceColor',map(4,:),'Alpha',.2,'EdgeColor',map(4,:))
%legend('Patriot2005rankable','Patriot2008unrankable','emptyunrankable+10%noise','perfectrankable+10%noise')
%legend('Patriot2005rankable','Patriot2008unrankable','perfectrankable+10%noise','perfectrankable+5%noise')
legend('Patriot2005rankable','Patriot2008unrankable','perfectrankable+5%noise')



