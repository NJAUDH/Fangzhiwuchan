min_supports=[0.05,0.04,0.03,0.02,0.01,0.009,0.008,0.007,0.006];
relations=[454,2035,4829,7853,19074,20798,22120,24688,27421];
frequent_itemsets=[1,4,4,8,148,194,460,1530,1581712];
plot(min_supports,relations,'-*','Linewidth',1);
set(gca,'XDir','reverse')%对X方向反转
xlabel('Minimum Supports');
ylabel('Relations');
ylim([0 30000]);
set(gca,'xtick',0:0.01:0.05)
title('Apriori');
