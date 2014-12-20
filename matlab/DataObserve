function [ ] = DataObserve( )

stockPrice = csvread('./HD-2013-2014-d.csv', 1, 1);

[timeLength, ~] = size(stockPrice);

openPrice = flipud(stockPrice(:, 1));
closePrice = flipud(stockPrice(:, 4));


figure;
hold on;
grid on;
title('Daily Stock Price of The Home Depot');
xlabel('Time (day)');
ylabel('Stock Price (Dollar)');
plot(1:timeLength, openPrice,'b');
plot(1:timeLength, closePrice,'r--');
legend('Open Price', 'Close Price','Location','SouthEast');
% set(gca, 'YLim', [0, 100] ,'XTick', 1:250:timeLength, 'XTickLabel',{'2004', ...
%     '2005', '2006', '2007', '2008', '2009', '2010', '2011',...
%     '2012', '2013', '2014'});

end
