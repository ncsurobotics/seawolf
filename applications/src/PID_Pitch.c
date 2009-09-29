
/*
 *  PID_Pitch.c
 *  Seawolf
 *
 *  PID Controller Code for Pitch
 *
 *  Created by Matthias Welsh on 3/20/09.
 *  Copyright 2009 NCSU Underwater. All rights reserved.
 *
 */

#include "seawolf.h"

#include <stdbool.h>
#include <stdio.h>
#include <time.h>

float getPitchHeading();
float getPitch();
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
    Seawolf_init("PID Pitch");
    char Action[32];
    char Data[32];
    
    // PID vars
    float SP; // setpoint
    float PV; // process variable
    float e_current = 0; // error
    float e_previous;
    float P_out = 0;
    float I_out = 0;
    float D_out = 0;
    float MV;
    
    // Pull PID constants
    K_p = SeaSQL_getPitchPID_p();
    K_i = SeaSQL_getPitchPID_i();
    K_d = SeaSQL_getPitchPID_d();
    
    // Initialize clocks
    IT_previous.tv_sec = 0;
    IT_previous.tv_nsec = 0;

    // Filter messages
    Notify_filter(FILTER_MATCH,"UPDATED IMU");
    Notify_filter(FILTER_MATCH,"UPDATED PitchPID");
    
    // Get desired pitch
    SP = getPitchHeading();
    
    while(true) {
        Notify_get(Action,Data);
        
        if(strcmp(Data, "PitchPID") == 0) {
            // New values of constants
            K_p = SeaSQL_getPitchPID_p();
            K_i = SeaSQL_getPitchPID_i();
            K_d = SeaSQL_getPitchPID_d();
            continue;
        }
        
        // Get actual pitch
        PV = getPitch();
	
        // PID Calculations
        e_current = SP - PV;                      // Error
        P_out = proportional(e_current);          // Proportional
        I_out = integral(e_current,I_out);        // Integral
        D_out = derivative(e_current,e_previous); // Derivative
            
        // P + I + D
        MV = Util_inRange(-63, P_out + (K_i*I_out) + D_out, 63);
	
        // On the first loop through ouput won't make sense (delta_T)
        if(IT_previous.tv_sec) {
            dataOut(MV);
        }
	
        // Var bumps current to previous
        e_previous = e_current;
        IT_previous.tv_sec = IT_current.tv_sec;
        IT_previous.tv_nsec = IT_current.tv_nsec;
        DT_previous.tv_sec = DT_current.tv_sec;
        DT_previous.tv_nsec = DT_current.tv_nsec;
    }
    
    Seawolf_close();
    return 0;
}

// Get the pitch heading
float getPitchHeading(void) {
    // Desired pitch is always 0
    return 0.0;
}

// Get current pitch
float getPitch(void) {
    // Get the stabalized euler angles for pitch
    return SeaSQL_getSEA_Pitch();
}

// Spit out some data
void dataOut(float MV){
    int aft = (int) MV;
    int y = -aft / 2;
    Notify_send("THRUSTER_REQUEST", Util_format("Pitch %d %d %d", y, y, aft));
}

// Calculate Proportion
float proportional(float e_current) {
    return K_p * e_current;
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
    
    I_out += e_current * delta_T;
    return I_out;
}

// Calculate Derivative
float derivative(float e_current, float e_previous){
    // Generate a delta t
    float delta_T;
    clock_gettime(CLOCK_REALTIME, &DT_current);
    delta_T = difftimespec(&DT_current, &DT_previous);
    
    float D_out;
    D_out = K_d*(e_previous-e_current) / delta_T;

    return D_out;
}
