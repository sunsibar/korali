clear

gm = jsondecode(fileread('gm.json'));
Ngm = length(gm);
for i=1:Ngm
  Mu(i,:) = gm(i).mu(:)';
  Sigma(:,:,i) = gm(i).sigma;
  w(i) = gm(i).w;
end
  
N = size(Mu,2);
%%
gm = gmdistribution(Mu,Sigma,w);

pdf = @(x) gm.pdf(x);
proppdf = @(x,y) mvnpdf(y-x);
proprnd = @(x) mvnrnd(x, 2*eye(N), 1);

nsamples = 100000;
x0 = [5 5 5 5];
x = mhsample( x0 ,nsamples,'pdf',pdf,'proprnd',proprnd,'symmetric',1,'burnin',500);

%%
fig = figure(1); clf

[ h, ax, BigAx, hhist, pax ] = plotmatrix_hist( x );

%% plot pdf
for i = 1:N

  y=0;
  t = linspace( min(x(:,i)), max(x(:,i)), 1000 );

  for k=1:Ngm
    mu = Mu(k,:);
    sigma = Sigma(:,:,k);
    N = length(mu);
    y = y + w(k)*normpdf( t, mu(i), sqrt(sigma(i,i)) );
  end

  hold( pax(i), 'on' )
  plot( pax(i), t, y, 'LineWidth', 3)
end

%% plot ellipses
for k=1:size(Sigma,3)

  mu = Mu(k,:);
  sigma = Sigma(:,:,k);
  N = length(mu);

  for i = 1:N
    for j = i+1:N
      Sij = sigma([i j],[i j]);
      p = 0.99;
      s = -2 * log(1 - p);
      [V, D] = eig( Sij * s);
      t = linspace(0, 2 * pi);
      a = (V * sqrt(D)) * [cos(t(:))'; sin(t(:))'];

      hold( ax(i,j), 'on' )
      plot( ax(i,j), a(2, :) + mu(j), a(1, :) + mu(i), 'LineWidth', 4);
    end
  end

end