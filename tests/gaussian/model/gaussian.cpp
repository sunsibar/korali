#include "gaussian.h"

#include <gsl/gsl_matrix.h>
#include <gsl/gsl_randist.h>
#include <gsl/gsl_linalg.h>

gsl_vector_view mean_view;
gsl_matrix *L;

double gaussian(double *x)
{
	double work[NDIMS];
	gsl_vector_view work_view	= gsl_vector_view_array(work, NDIMS);
	gsl_vector_view vals_view = gsl_vector_view_array(x, NDIMS);
  double res = 0.0;
  gsl_ran_multivariate_gaussian_log_pdf(&vals_view.vector, &mean_view.vector, L, &res, &work_view.vector);
  printf("res: %f\n", res);
  return res;
}


void gaussian_init()
{
	double mean[NDIMS];
	double sigma[NDIMS*NDIMS];

	for (int i = 0; i < NDIMS; i++) mean[i] = i;
	for (int i = 0; i < NDIMS; i++) sigma[i*NDIMS+i] = i*5.0+1;

	mean_view 	= gsl_vector_view_array(mean, NDIMS);
	gsl_matrix_view sigma_view 	= gsl_matrix_view_array(sigma, NDIMS,NDIMS);
	L = gsl_matrix_alloc(NDIMS,NDIMS);
	gsl_matrix_memcpy(L, &sigma_view.matrix);
	gsl_linalg_cholesky_decomp(L);
}
