/**
 * util.c contains miscelanious utilites for vision code run on seawolf. 
 */

#include <stdio.h>
#include <stdbool.h>
#include <stdlib.h>
#include <math.h>

#include "util.h"
#include <seawolf3.h>

//convert pixels from center into degrees from center
float PixToDeg(int p){
    float degrees;
    //degrees = floor( 6.49606e-10*pow(p,5) - 2.47052e-7*pow(p,4) + 0.0000336612*pow(p,3) - 0.00205154*p*p + 0.190667*p );
    degrees = p;
    return degrees;
}
