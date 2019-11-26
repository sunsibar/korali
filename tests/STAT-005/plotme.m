clc; clear



file = get_last_generation('_korali_results002');



data = jsondecode(fileread(file));

N = length(data.Variables);
Ns = data.Solver.PopulationSize;
x = data.Solver.Internal.SampleDatabase;

% x = data.Solver.Internal.SampleDatabase;
% Ns = data.Solver.Internal.DatabaseEntryCount;
% dim = length(data.Solver.Internal.SampleDatabase)/Ns;
%x = reshape(x,dim,Ns)';

min(x(:,2))




%%
fig = figure(); clf
% fig.Position = [539 130 1021 825];

[ h, ax, BigAx, hhist, pax ] = plotmatrix_hist( x );








function f = get_last_generation( folder )

z = dir( [ folder '/gen*.json' ]);

f = [ folder '/' z(end).name ];

end