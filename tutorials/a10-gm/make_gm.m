clear

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

for i = 1:Ngm
  [~,p] = chol(Sigma(:,:,i));
  if(p~=0), error("Non positive definite (%d)",i); end
end
                            
w = [0.8 0.2];

gm = gmdistribution(Mu,Sigma,w);

x = random(gm,5000);

clf
[ h, ax, BigAx, hhist, pax ] = plotmatrix_hist(x);


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

%% write json file
for i=1:Ngm
  json(i).mu    = Mu(i,:);
  json(i).sigma = Sigma(:,:,i);
  json(i).w     = w(i);
end

if(Ngm==1)
  jsonCode = ['[' jsonencode(json) ']'];
else
  jsonCode = jsonencode(json);
end
fp = fopen('gm.json', 'w');
fprintf(fp, '%s\n', jsonCode );
fclose(fp);

