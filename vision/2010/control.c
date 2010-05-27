/**
 * This file contains functions that make controling headings easier.
 */

#include <seawolf.h>
#include <seawolf3.h>

#include <math.h>

#include "control.h"

static float yaw_control_cache = NAN;

/* Depth */
void set_depth(float depth, float depth_control) {
    if (depth_control == DEPTH_ABSOLUTE) {
        set_depth_absolute(depth);
    } else if (depth_control == DEPTH_RELATIVE) {
        set_depth_relative(depth);
    } else {
        printf("ERROR: depth_control incorrectly set to %f!!!\n", depth_control);
    }
}

void set_depth_relative(float depth) {
    float current_depth = Var_get("Depth");
    Var_set("DepthHeading", current_depth + depth);
}

void set_depth_absolute(float depth) {
    Var_set("DepthHeading", depth);
}

/* Yaw */
void set_yaw(float yaw, float yaw_control) {
    if (yaw_control != yaw_control_cache) {
        Var_set("Rot.Mode", yaw_control);
        yaw_control_cache = yaw_control;
    }
    if (yaw_control == ROT_MODE_ANGULAR) {
        set_yaw_absolute(yaw);
    } else if (yaw_control == ROT_MODE_RELATIVE) {
        set_yaw_relative(yaw);
    } else if (yaw_control == ROT_MODE_RATE) {
        set_yaw_rate(yaw);
    } else {
        printf("ERROR: yaw_control incorrectly set to %f!!!\n", yaw_control);
    }
}

void set_yaw_relative(float yaw) {
    float current_yaw = Var_get("SEA.Yaw");
    Var_set("Rot.Angular.Target", current_yaw + yaw);
}

void set_yaw_absolute(float yaw) {
    Var_set("Rot.Angular.Target", yaw);
}

void set_yaw_rate(float yaw) {
    Var_set("Rot.Rate.Target", yaw);
}
