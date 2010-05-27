#ifndef _CONTROL_INCLUDE_H
#define _CONTROL_INCLUDE_H

/* Depth */
void set_depth(float depth, float depth_control);
void set_depth_relative(float depth);
void set_depth_absolute(float depth);

/* Yaw */
void set_yaw(float yaw, float yaw_control);
void set_yaw_relative(float yaw);
void set_yaw_absolute(float yaw);
void set_yaw_rate(float yaw);

#endif
