function [ h, ax, BigAx, hhist, pax ] = plotmatrix_hist( theta, varargin )

% Start parser
p = inputParser;

checkTheta = @(x) isnumeric(x) && ismatrix(x);
addRequired(p,'theta', checkTheta);

defaultThetaValues = [];
checkThetaValues = @(x) isnumeric(x) && ismatrix(x);
addOptional(p,'Evaluation', defaultThetaValues, checkThetaValues);

defaultPlot = 'surf';
validPlot   = {'surf','contour'};
checkPlot   = @(x) any(validatestring(x,validPlot));
addOptional(p,'PlotFunction',defaultPlot,checkPlot);

defaultScatterSym      = '.';
validdefaultScatterSym = {'.','o','*','x'};
checkScatterSym        = @(x) any(validatestring(x,validdefaultScatterSym));
addOptional(p,'ScatterSymbol',defaultScatterSym,checkScatterSym);

defaultVariableName = '\vartheta';
checkVariableName   = @(x) ischar(x);
addOptional(p,'VariableName',defaultVariableName,checkVariableName);

parse(p,theta,varargin{:})
% End of parser

plotFunction  = p.Results.PlotFunction;
scatterSymbol = p.Results.ScatterSymbol;
variableName  = p.Results.VariableName;
Evaluation    = p.Results.Evaluation;

N = size(theta,2);

% Don't plot anything if either theta or theta is empty
hhist = gobjects(0);
pax   = gobjects(0);
if isempty(N) || isempty(N)
  if nargout>0, h = gobjects(0); ax = gobjects(0); BigAx = gobjects(0); end
  return
end


% Create/find BigAx and make it invisible
cax   = axes;
BigAx = newplot(cax);
fig   = ancestor(BigAx,'figure');
hold_state = ishold(BigAx);
set(BigAx,'Visible','off','color','none')

if any( scatterSymbol=='.' )
  units = get(BigAx,'units');     set(BigAx,'units','pixels');
  pos   = get(BigAx,'Position');  set(BigAx,'units',units);
  markersize = max(1,min(15,round(15*min(pos(3:4))/max(1,size(theta,1))/max(N,N))));
else
  markersize = get(0,'DefaultLineMarkerSize');
end

% Create and plot into axes
ax        = gobjects(N,N);
pos       = get(BigAx,'Position');
width     = pos(3)/N;
height    = pos(4)/N;
space     = .1; % 2 percent space between axes
pos(1:2)  = pos(1:2) + space*[width height];
xlim = zeros([N N 2]);
ylim = zeros([N N 2]);
BigAxHV     = get(BigAx,'HandleVisibility');
BigAxParent = get(BigAx,'Parent');
paxes       = findobj(fig,'Type','axes','tag','PlotMatrixScatterAx');


n = N*N;
% Initialize progress bar
upd = textprogressbar(n, 'barlength', 30, ...
                         'updatestep', 10, ...
                         'startmsg', 'Loading data... ',...
                         'endmsg', ' Done!', ...
                         'showbar', true, ...
                         'showremtime', true, ...
                         'showactualnum', true, ...
                         'barsymbol', '+', ...
                         'emptybarsymbol', '-');


for i = N:-1:1
  for j = N:-1:1
    
    axPos = [ pos(1)+(j-1)*width, pos(2)+(N-i)*height, width*(1-space), height*(1-space) ];
    findax = findaxpos(paxes, axPos);
    if isempty( findax )
      ax(i,j) = axes('Position',axPos,'HandleVisibility',BigAxHV,'parent',BigAxParent);
      set(ax(i,j),'visible','on');
    else
      ax(i,j) = findax(1);
    end
    
    xData = theta(:,j);
    yData = theta(:,i);

    if(i<j) % Upper right
      if( ~isempty( Evaluation ) )
          hh(i,j) = scatter( xData, yData, [], Evaluation );
      else
          hh(i,j) = plot( xData, yData, scatterSymbol );
      end

      ax(i,j).XLim = ax(j,i).YLim;
      ax(i,j).YLim = ax(j,i).XLim;

    elseif(i>j)% Lower left
      [Z,Xe,Ye] = histcounts2( yData, xData, 20, 'Normalization','pdf' );

      X = Xe(1:end-1) + diff(Xe)/2; 
      Y = Ye(1:end-1) + diff(Ye)/2;

      [X,Y] = meshgrid( X, Y );  

      Z = smoothn(Z,1);
      
      nn = 100;
      xi = linspace(X(1), X(end), nn);
      yi = linspace(Y(1), Y(end), nn);
      [xi, yi] = meshgrid(xi, yi);
      zi = interp2(X, Y, Z', xi, yi, 'spline');

      if( strcmp( plotFunction, 'contour' ) )
        [~,hh(i,j)] = contour(yi, xi, zi, 30 ,'parent',ax(i,j));
      end
      if( strcmp( plotFunction, 'surf' ) )
        hh(i,j) = surf(yi, xi, zi, 'parent',ax(i,j));
        hh(i,j).FaceColor = 'interp';
        hh(i,j).EdgeColor = 'none';
      end
      view(ax(i,j), [0,90]) 

      ax(i,j).XLim = [ Y(1), Y(end) ];
      ax(i,j).YLim = [ X(1), X(end) ];
           
    end
    
    upd( n - (i-1)*N - j + 1 );
    
    set(ax(i,j),'xgrid','off','ygrid','off')

    xlim(i,j,:) = get(ax(i,j),'xlim');
    ylim(i,j,:) = get(ax(i,j),'ylim');        

  end


end

xlimmin = min(xlim(:,:,1),[],1);
xlimmax = max(xlim(:,:,2),[],1);
ylimmin = min(ylim(:,:,1),[],2);
ylimmax = max(ylim(:,:,2),[],2);


% Try to be smart about axes limits and labels.  Set all the limits of a
% row or column to be the same and inset the tick marks by 10 percent.
inset = 0;
for i=1:N
  set(ax(i,1),'ylim',[ylimmin(i,1) ylimmax(i,1)])
  dy = diff(get(ax(i,1),'ylim'))*inset;
  set(ax(i,:),'ylim',[ylimmin(i,1)-dy ylimmax(i,1)+dy])
end

dx = zeros(1,N);
for j=1:N
  set(ax(1,j),'xlim',[xlimmin(1,j) xlimmax(1,j)])
  dx(j) = diff(get(ax(1,j),'xlim'))*inset;
  set(ax(:,j),'xlim',[xlimmin(1,j)-dx(j) xlimmax(1,j)+dx(j)])
end

set(ax(1:N-1,:),'xticklabel','')
set(ax(:,2:N),'yticklabel','')

set( BigAx, 'XTick',get(ax(N,1),'xtick'), 'YTick',get(ax(N,1),'ytick'), 'userdata',ax, 'tag','PlotMatrixBigAx')
set(ax,'tag','PlotMatrixScatterAx');


% Plot histogram in the diagonal
paxes = findobj(fig,'Type','axes','tag','PlotMatrixHistAx');
pax = gobjects(1, N);
for i = N:-1:1
  axPos = get(ax(i,i),'Position');
  findax = findaxpos(paxes, axPos);
  if isempty(findax)
    histax = axes('Position',axPos,'HandleVisibility',BigAxHV,'parent',BigAxParent);
    set(histax,'visible','on');
  else
    histax = findax(1);
  end

  hhist(i) = histogram(histax,theta(:,i,:),50);
  hhist(i).Normalization = 'pdf';
  hhist(i).FaceColor = [51,255,51]/255;

  set(histax,'xtick',[],'ytick',[],'xgrid','off','ygrid','off');
  set(histax,'xlim',[xlimmin(1,i)-dx(i) xlimmax(1,i)+dx(i)])
  set(histax,'tag','PlotMatrixHistAx');
  pax(i) = histax;  % ax handles for histograms
end

% Make BigAx the CurrentAxes
set(fig,'CurrentAx',BigAx)
if ~hold_state
  set(fig,'NextPlot','replacechildren')
end

% Also set Title and X/YLabel visibility to on and strings to empty
set([get(BigAx,'Title'); get(BigAx,'XLabel'); get(BigAx,'YLabel')], 'String','','Visible','on')

if nargout~=0
    h = hh;
end


for i=1:N
  varNameStr = [ '$' variableName '_{' num2str(i) '} $'];
  ax(i,1).YLabel.String= varNameStr; 
  ax(i,1).YLabel.FontSize = 20; 
  ax(i,1).YLabel.Interpreter='Latex';

  ax(N,i).XLabel.String= varNameStr; 
  ax(N,i).XLabel.FontSize = 20; 
  ax(N,i).XLabel.Interpreter='Latex';
end


end





function findax = findaxpos(ax, axpos)
tol = eps;
findax = [];
for i = 1:length(ax)
    axipos = get(ax(i),'Position');
    diffpos = axipos - axpos;
    if (max(max(abs(diffpos))) < tol)
        findax = ax(i);
        break;
    end
end

end
