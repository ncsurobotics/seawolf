#include <complex.h>
#include <math.h>
#include <stdlib.h>
#include <stdio.h>
#include <fftw3.h>

void flip(float* data, int ending)
{
	float tmp;
	for(int i = 0; i < (int)(floor(ending / 2)); i++) {
		tmp = data[i];
		data[i] = data[ending - i - 1];
		data[ending - i - 1] = tmp;
	//	printf("data = %f, enddata = %f, ending = %d, i = %d \n", data[i], data[ending - i - 1], (int)(floor(ending/2)), i);
	}

	return;
}

void fft (float* data, complex* imag, int ending)
{
	//control variables
	int i;

	//fft stuff
	complex *in, *out;
	fftw_plan plan;
	
	//generate array
	in  = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * ending);
	out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * ending);
	
	//generate plan
	plan = fftw_plan_dft_1d((ending), in, out, FFTW_FORWARD, FFTW_ESTIMATE); //use FFTW_estimate for speed
	
	//generate input variables
	for (i=0; i < ending; i++)
	{
		in[i] = data[i]; // + (0 * I);
	}
	
	//execute fft
	fftw_execute(plan);
	
	//unzip complex array
	for (i=0; i < ending; i++)
	{
		imag[i] = out[i];
	}
	
	//free memory
	fftw_destroy_plan(plan);
	fftw_free(in);
	fftw_free(out);
	
	return;
}

void ifft (complex* cmplx, float* data, int ending)
{
	//control variables
	int i;

	//fft stuff
	complex *in, *out;
	fftw_plan plan;
	
	//generate array
	in  = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * ending);
	out = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * ending);
	
	//generate plan
	plan = fftw_plan_dft_1d((ending), in, out, FFTW_BACKWARD, FFTW_ESTIMATE); //use FFTW_estimate for speed
	
	//generate input variables
	for (i=0; i < ending; i++)
	{
		in[i] = cmplx[i]; // + (0 * I);
	}
	
	//execute fft
	fftw_execute(plan);
	
	//unzip complex array
	for (i=0; i < ending; i++)
	{
		data[i] = creal(out[i]);
	}
	
	//free memory
	fftw_destroy_plan(plan);
	fftw_free(in);
	fftw_free(out);
	
	return;
}

void multiply(complex* in1, complex* in2, complex* out, int size)
{
	for(int i = 0; i < size; i++) {
		out[i] = in1[i] * in2[i];
	}

	return;	
}

void convolve(float* f, float* g, float* out, int size)
{
	//Implements fast convolution
	complex f_fft[size];
	complex g_fft[size];
	complex out_fft[size];
	
	fft(f, f_fft, size);
	fft(g, g_fft, size);
	multiply(f_fft, g_fft, out_fft, size);
	ifft(out_fft, out, size);

	return;	
}

void correlate(float* f, float* g, float* out, int size)
{
	//Cross Correlation = Convolution(f(-t), g(t))
	flip(f, size);
	convolve(f, g, out, size);

	return;	
}
