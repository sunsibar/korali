N1 = 20; N2 = 20;

f = @(x) sin(x).*cos(3*x) + cos(x/2);

xTrain = unifrnd( 0, 4*pi, N1, 1 );
xTest  = unifrnd( 0, 4*pi, N2, 1 );
xNew   = linspace( 0, 4*pi, 1e3 )';

dlmwrite('sincos1d_train.dat',[xTrain f(xTrain)],' ');
dlmwrite('sincos1d_test.dat',[xTest  f(xTest)],' ');
dlmwrite('sincos1d_new.dat', [xNew f(xNew)],' ');

%%
N1 = 40; N2 = 40;

f = @(x) sin(x(:,1)).*cos(3*x(:,2)) + cos(0.5*x(:,3)).*x(:,1);

xTrain = unifrnd( 0, 4*pi, N1, 3 );
xTest  = unifrnd( 0, 4*pi, N2, 3 );
[X,Y,Z] = meshgrid(linspace(0,4*pi,10));
xNew   = [ X(:) Y(:) Z(:)];


dlmwrite('sincos3d_train.dat',[xTrain f(xTrain)],' ');
dlmwrite('sincos3d_test.dat',[xTest  f(xTest)],' ');
dlmwrite('sincos3d_new.dat', [xNew f(xNew)],' ');
