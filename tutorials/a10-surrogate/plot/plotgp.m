clc; clear;

addpath('./shplot')

k = 1; 

data = jsondecode(fileread('../_korali_result_new/final.json'));

x = data.Problem.XData;
y = data.Problem.YData;
yGP = data.Problem.Internal.GaussianProcessEvaluation;
vGP = data.Problem.Internal.GaussianProcessVariance;

[~,ind] = sort( x(:,k) );
x = x(ind,k);
y = y(ind);
yGP = yGP(ind);
vGP = vGP(ind);


fig = figure(1); clf
grid on; hold on; axis tight

opt = {'Color', [0.9290    0.6940    0.1250] };
H = shplot( x, yGP, sqrt(vGP), opt{:});
H.line.LineWidth = 3;
plot( x, yGP ); grid on


p4 = plot( x, y,'k');
p4.LineWidth = 3;

%% load train data set

data = jsondecode(fileread('../_korali_result_train/final.json'));
x = data.Problem.XData;
y = data.Problem.YData;

p1 = plot( x(:,k), y(:),'kx');
p1.MarkerFaceColor = [0.9290    0.6940    0.1250];
p1.LineWidth = 3;
p1.MarkerSize = 15;



lg = legend([p1,H.line,H.patch,p4],'  data','  GP mean','  GP one std','  exact');
lg.Location = 'best';

xlabel('x'); ylabel('y');

set(gca,'FontSize',20)

