rng default  % For reproducibility

% N = 4;
% Mu = [ 1 0 0 1 ];
% Sigma = [1   1.5 0      0; 
%          1.5  3  0      0; 
%          0    0  1    -0.6;
%          0    0  -0.6   1];
%        
multi = true
  
if(multi)

  Mu = [ 1 0 0 1;
       5 6 7 -5];

  Sigma = zeros(4,4,2);


  Sigma(:,:,1) = [1   1.5 0  0; 
                1.5  3  0  0; 
                0    0  1  -0.6;
                0    0  -0.6  1];
              
  Sigma(:,:,2) = [1   -1.5 0  0.1; 
                -1.5  3  0  0; 
                0    0  1  0;
                0.1    0  0  1];


  Ngm = size(Sigma,3);
  % Ngm = 1;
  N = size(Sigma,1);
  w = [0.8 0.2];
  gm = gmdistribution(Mu,Sigma,w)

else
  Mu = [ 1 0 0 1];

  Sigma = zeros(4,4,1);


  Sigma(:,:,1) = [1   1.5 0  0; 
                1.5  3  0  0; 
                0    0  1  -0.6;
                0    0  -0.6  1];
              
  Ngm = size(Sigma,3);
  % Ngm = 1;
  N = size(Sigma,1);
  w = [1.0];
  gm = gmdistribution(Mu,Sigma,w);
end

       
%pdf = @(x) mvnpdf(x,Mu,Sigma);

tpdf = @(x) pdf(gm,x);


proppdf = @(x,y) mvnpdf(y-x);
proprnd = @(x) mvnrnd(x, eye(N), 1);

nsamples = 10000;
x0 = [1 1 1 1];
x = mhsample( x0 ,nsamples,'pdf',tpdf,'proprnd',proprnd,'symmetric',1,'burnin',500);

%%
fig = figure(1); clf

[ h, ax, BigAx, hhist, pax ] = plotmatrix_hist( x );

%% plot pdf
for i = 1:N
  
  t = linspace( min(x(:,i)), max(x(:,i)), 1000 );
  y = normpdf( t, Mu(i), sqrt(Sigma(i,i)) );
  
  hold( pax(i), 'on' )  
  plot( pax(i), t, y, 'LineWidth', 3)
end


%% plot ellipses
for i = 1:N
  for j = i+1:N 
    Sij = Sigma([i j],[i j]);
    p = 0.99;
    s = -2 * log(1 - p);
    [V, D] = eig( Sij * s);
    t = linspace(0, 2 * pi);
    a = (V * sqrt(D)) * [cos(t(:))'; sin(t(:))'];

    hold( ax(i,j), 'on' )
    plot( ax(i,j), a(2, :) + Mu(j), a(1, :) + Mu(i), 'LineWidth', 4);
  end
end