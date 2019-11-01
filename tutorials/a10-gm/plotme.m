% Add the following to your startup.m:
% addpath(genpath('KORALI_PATH/tools/matlab/'))

clc; clear

addpath("../../tools/matlab/")
addpath("../../tools/matlab/textprogressbar")

file = '_korali_result/final.json';
data = jsondecode(fileread(file));
N = length(data.Variables);
Ns = data.Solver.PopulationSize;
x = data.Solver.Internal.SampleDatabase;

% file = '_korali_result/final.json';
% data = jsondecode(fileread(file));
% x = data.Solver.Internal.SampleDatabase;
% Ns = data.Solver.Internal.DatabaseEntryCount;
% dim = length(data.Solver.Internal.SampleDatabase)/Ns;
% x = reshape(x,dim,Ns)';

%%
fig = figure(1); clf
% fig.Position = [539 130 1021 825];

[ h, ax, BigAx, hhist, pax ] = plotmatrix_hist( x );


%% Plot the GM pdf and error ellipses

gm = jsondecode(fileread('gm.json'));
Ngm = length(gm);
N = length(gm(1).mu);

%% plot pdf
for i = 1:N
  
  y=0;
  t = linspace( min(x(:,i)), max(x(:,i)), 1000 );
  
  for k=1:Ngm
    y = y + gm(k).w * normpdf( t, gm(k).mu(i), sqrt(gm(k).sigma(i,i)) );
  end
  
  hold( pax(i), 'on' )  
  plot( pax(i), t, y, 'LineWidth', 3)
end

%% plot ellipses
for k=1:Ngm
  
  for i = 1:N
    for j = i+1:N 
      Sij = gm(k).sigma([i j],[i j]);
      p = 0.99;
      s = -2 * log(1 - p);
      [V, D] = eig( Sij * s);
      t = linspace(0, 2 * pi);
      a = (V * sqrt(D)) * [cos(t(:))'; sin(t(:))'];

      hold( ax(i,j), 'on' )
      plot( ax(i,j), a(2, :) + gm(k).mu(j), a(1, :) + gm(k).mu(i), 'LineWidth', 4);
    end
  end
  
end

