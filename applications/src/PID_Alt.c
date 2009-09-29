
/*
 *  PID_Altitude.c
 *  Seawolf
 *
 *  PID Controller Code for Altitude
 *
 *  Created by Matthias Welsh on 3/20/09.
 *  Copyright 2009 NCSU Underwater. All rights reserved.
 *
 */

#include "seawolf.h"

#include <stdbool.h>
#include <stdio.h>
#include <time.h>

float getAltitudeHeading();
float getAltitude();
void dataOut(float MV);
float proportional(float e_current);
float integral(float e_current, float I_out);
float derivative(float e_current, float e_previous);
float difftimespec(struct timespec* current, struct timespec* previous);

// Timer vars
struct timespec IT_current, IT_previous, DT_current, DT_previous;
int K_p, K_i, K_d;

int main(void) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("PID Altitude");
    char Action[32];
    char Data[32];
    
    // PID vars
    float SP; // setpoint
    float SP_tmp;
    float PV; // process variable
    float e_current = 0;  //error
    float e_previous;
    float P_out = 0;
    float I_out = 0;
    float D_out = 0;
    float MV;

    bool do_depth = (SeaSQL_getTrackerDoDepth() == 0.0);
    
    // Pull PID constants
    K_p = SeaSQL_getAltitudePID_p();
    K_i = SeaSQL_getAltitudePID_i();
    K_d = SeaSQL_getAltitudePID_d();
    
    // Initialize clocks
    IT_previous.tv_sec = 0;
    IT_previous.tv_nsec = 0;
    
    // Filter messages
    Notify_filter(FILTER_MATCH, "UPDATED AltitudePID");
    Notify_filter(FILTER_MATCH, "UPDATED AltitudeHeading");
    Notify_filter(FILTER_MATCH, "UPDATED Altitude");
    
    // Get desired altitude
    SP = getAltitudeHeading();
    
    while(true) {
        Notify_get(Action, Data);
        
        if(strcmp(Data, "AltitudePID") == 0) {
            // New values of constants
            K_p = SeaSQL_getAltitudePID_p();
            K_i = SeaSQL_getAltitudePID_i();
            K_d = SeaSQL_getAltitudePID_d();
        } else if(strcmp(Data, "AltitudeHeading") == 0) {
            // New altitude heading
            if((SP_tmp = getAltitudeHeading()) != SP) {
                SP = SP_tmp;
                I_out = 0;
                D_out = 0;
            }
        } else if(strcmp(Data, "TrackerDoDepth") == 0) {
            do_depth = (SeaSQL_getTrackerDoDepth() == 0.0);
        } else {
            // Get new altitude
            PV = getAltitude();

           
            // PID Calculations
            e_current = SP - PV;                      // Error
            P_out = proportional(e_current);          // Proportional
            I_out = integral(e_current,I_out);        // Integral
            D_out = derivative(e_current,e_previous); // Derivative


            
            // P + I + D
            MV = Util_inRange(-63, P_out + (K_i*I_out) + D_out, 63);
            
            // On the first loop through ouput won't make sense (delta_T)
            if(IT_previous.tv_sec && do_depth) {
                dataOut(MV);
            }
            
            // Var bumps current to previous
            e_previous = e_current;
            IT_previous.tv_sec = IT_current.tv_sec;
            IT_previous.tv_nsec = IT_current.tv_nsec;
            DT_previous.tv_sec = DT_current.tv_sec;
            DT_previous.tv_nsec = DT_current.tv_nsec;
        }
    }
    
    Seawolf_close();
    return 0;
}

// Get the altitude heading
float getAltitudeHeading(void) {
    return SeaSQL_getAltitudeHeading();
}

// Get current altitude
float getAltitude(void) {
    return SeaSQL_getAltitude();
}

// Spit out some data
void dataOut(float MV) {
    int aft = (int) MV;
    int y = (int) aft / 1.75;
    Notify_send("THRUSTER_REQUEST", Util_format("Alt %d %d %d", y, y, aft));
}

// Calculate Proportion
float proportional(float e_current) {
    float P_out;
    
    P_out = K_p * e_current;
    return P_out;
}

// Difference between two timestamps
float difftimespec(struct timespec* current, struct timespec* previous) {
    return ((float)current->tv_sec - previous->tv_sec) + (((float)current->tv_nsec - previous->tv_nsec)/1e9);
}

// Calculate Integral
float integral(float e_current, float I_out) {
    // Generate a delta t
    float delta_T;
    clock_gettime(CLOCK_REALTIME, &IT_current);
    delta_T = difftimespec(&IT_current, &IT_previous);
    
    //do a bit of error-checking on the delta_T term
    if(delta_T < 5){
        I_out = e_current * delta_T + I_out;        
    }else{
        printf("we arn't updating I_out because delta_T = %f \n",delta_T);
    }

    return I_out;
}

// Calculate Derivative
float derivative(float e_current, float e_previous) {
    // Generate a delta t
    float delta_T;
    clock_gettime(CLOCK_REALTIME, &DT_current);
    delta_T = difftimespec(&DT_current, &DT_previous);
    
    float D_out;
    D_out = K_d*(e_previous-e_current) / delta_T;
    //Logging_log(DEBUG, UTIL_Format("%.2f", D_out));

    return D_out;
}
