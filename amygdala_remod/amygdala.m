sholl_basal_length = load('/Users/bozelosp/Dropbox/remod/amygdala_remod/average_sholl_basal_length.txt')
sholl_basal_length = sholl_basal_length(:,[1,2,4])
% Plot using streight lines and * markers.
figure(); plot(sholl_basal_length(:,1),sholl_basal_length(:,[2]),'-^','color','b','linewidth',2); title('BLA: Sholl Analysis Basal - Length'); hold on;
plot(sholl_basal_length(:,1),sholl_basal_length(:,[3]),'-s','color','r','linewidth',2);