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
    degrees = floor( p*p*-0.0001+p*0.1488+0.1381 );
    return degrees;
}
