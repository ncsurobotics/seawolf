
#include <math.h>
#include <math_bf.h>
#include <complex_bf.h>
#include <filter.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>

#include "acoustics_math.h"
//#include "csv_io.h"

void flip(fract16* data, int size)
{
	fract16* data_end = data + size - 1;
	fract16 tmp;
	
	while(data_end > data)
	{
		tmp = *data; // Swap
		*data++ = *data_end;
		*data_end-- = tmp;
	}
}

void multiply(complex_fract16* in1, complex_fract16* in2, complex_fract16* out, int size)
{
	while(size--)
	{
		*out++ = cmlt_fr16(*in1++, *in2++);
	}
}

void fft(fract16* data, complex_fract16* cmplx, int ending)
{
	//control variables
	//int twiddleSize = ending;
	int wst = ending;
	int scale=0;
	int *blockExp = 0;
	
	
	//fft stuff
	complex_fract16 w[ending];
	

	//set up twiddle tables
	twidfftrad2_fr16(w,ending);
	

	//execute fft
	rfft_fr16(data, cmplx, w, 1, ending, 0 , 0);
}

void ifft(complex_fract16* cmplx, fract16* data, int ending)
{
	//control variables
	int twiddleSize = ending / 2;
	int wst = 2 * twiddleSize / ending;
	int scale;
	
	//fft stuff
	//complex_fract16 temp[ending];
	complex_fract16 w[ending];
	complex_fract16 o[ending];
	
	//set up twiddle tables
	twidfftrad2_fr16(w,ending/2);
	
	//execute fft
	ifft_fr16(cmplx, /*(complex_fract16*)temp,*/ o, (complex_fract16*)w, wst, ending, &scale, 2);

	//convert back to real data
	
	//Resolve Pointers (for high speed)
	complex_fract16* o_ptr	  = &o[0];
	
	//Convert complex to real
	for(int i = 0; i < ending; i++)
	{
		*(data++) = (o_ptr++)->re; //This works, data is a local copy of the data pointer being passed to it 
	}
}


//FIR filter (send it down the zipline)
void firfly(fract16* data, int size, fir_state_fr16* firState)
{
	//Create Temporary Data array
	fract16* tempData;

	tempData = calloc(sizeof(fract16), size);

	
	//execute fir
	fir_fr16 ( data, tempData, size, firState);

	//overwrite input data
	memcpy( data, tempData, sizeof(fract16)*size );	
}


void convolve(fract16* f, fract16*g, fract16* out, int size)  
{
	convolve_fr16(f, size, g, size, out);
}

void fast_convolve(fract16* f, fract16* g, fract16* out, int size)
{
	//Implements fast convolution
	complex_fract16 f_fft[size];
	complex_fract16 g_fft[size];
	complex_fract16 out_fft[size];
	
	fft(f, f_fft, size);
	fft(g, g_fft, size);
	multiply(f_fft, g_fft, out_fft, size);
	ifft(out_fft, out, size);
}

void correlate(fract16* f, fract16* g, fract16* out, int size)
{
	//Cross Correlation = Convolution(f(-t), g(t))
	flip(f, size);
	convolve(f, g, out, size);
}

void fast_correlate(fract16* f, fract16* g, fract16* out, int size)
{
	//Cross Correlation = Convolution(f(-t), g(t))
	flip(f, size);
	fast_convolve(f, g, out, size);
}

int findMax(fract16* f, int size)
{
	fract16 maxY = 0;
	int maxX = 0;
	int i;

	for(i = 0; i < size; i++)
	{
		if ( f[i] > maxY )
		{
			maxY = f[i];
			maxX = i; 
		} //if
	} //for
	
	return maxX;
}//findMax
