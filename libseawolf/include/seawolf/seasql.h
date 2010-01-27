
#ifndef __SEAWOLF_SEASQL_INCLUDE_H
#define __SEAWOLF_SEASQL_INCLUDE_H

#include <stdbool.h>

#include <mysql/mysql.h>

#include "seawolf/seasql_config.h"

/* Basic methods */
void SeaSQL_init(void);          /* Initialize SeaSQL backend */
void SeaSQL_close(void);         /* Close SeaSQL backend */
void SeaSQL_setAutoNotify(bool do_notify); /* Automatically use notify to send variable update notifications */
int SeaSQL_execute(char* cmd);   /* Execute the given SQL expression */

/* Helpful functions */
bool SeaSQL_table_exists(char* tbl);   /* Does the table exists? */

/* Variable updating methods */
int SeaSQL_updateVariable(char* name, float value);  /* Update the value of variable 'name' to 'value' */
float SeaSQL_getMostRecent(char* name);              /* Store the most recent version of variable 'name' and store it to 'value' */
void SeaSQL_clearVariables(void);                    /* Reset the variables table */

/* Make defining accessors easy */
#define MYSQL_ACCESSOR_HEADER(name) float SeaSQL_get##name(void); \
                                    int SeaSQL_set##name(float value);

/* Define all variables and accessors */
MYSQL_ACCESSOR_HEADER( SEA_Roll )
MYSQL_ACCESSOR_HEADER( SEA_Yaw )
MYSQL_ACCESSOR_HEADER( SEA_Pitch )
MYSQL_ACCESSOR_HEADER( IEA_Roll )
MYSQL_ACCESSOR_HEADER( IEA_Yaw )
MYSQL_ACCESSOR_HEADER( IEA_Pitch )
MYSQL_ACCESSOR_HEADER( IV_MagField_X )
MYSQL_ACCESSOR_HEADER( IV_MagField_Y )
MYSQL_ACCESSOR_HEADER( IV_MagField_Z )
MYSQL_ACCESSOR_HEADER( IV_Accel_X )
MYSQL_ACCESSOR_HEADER( IV_Accel_Y )
MYSQL_ACCESSOR_HEADER( IV_Accel_Z )
MYSQL_ACCESSOR_HEADER( IV_AngRate_X )
MYSQL_ACCESSOR_HEADER( IV_AngRate_Y )
MYSQL_ACCESSOR_HEADER( IV_AngRate_Z )
MYSQL_ACCESSOR_HEADER( IOM_11 )
MYSQL_ACCESSOR_HEADER( IOM_21 )
MYSQL_ACCESSOR_HEADER( IOM_31 )
MYSQL_ACCESSOR_HEADER( IOM_12 )
MYSQL_ACCESSOR_HEADER( IOM_22 )
MYSQL_ACCESSOR_HEADER( IOM_32 )
MYSQL_ACCESSOR_HEADER( IOM_13 )
MYSQL_ACCESSOR_HEADER( IOM_23 )
MYSQL_ACCESSOR_HEADER( IOM_33 )

/* Depth and depth heading */
MYSQL_ACCESSOR_HEADER( Depth )
MYSQL_ACCESSOR_HEADER( DepthHeading )
MYSQL_ACCESSOR_HEADER( Altitude )
MYSQL_ACCESSOR_HEADER( AltitudeHeading )
MYSQL_ACCESSOR_HEADER( YawHeading )

/* Set point tracker heading */
MYSQL_ACCESSOR_HEADER( SetPoint_Theta )
MYSQL_ACCESSOR_HEADER( SetPoint_Phi )
MYSQL_ACCESSOR_HEADER( SetPoint_Rho )

/* Fake set points */
MYSQL_ACCESSOR_HEADER( SetPointSource )
MYSQL_ACCESSOR_HEADER( SetPointVision_Theta )
MYSQL_ACCESSOR_HEADER( SetPointVision_Phi )
MYSQL_ACCESSOR_HEADER( SetPointVision_Rho )
MYSQL_ACCESSOR_HEADER( SetPointAcoustics_Theta )
MYSQL_ACCESSOR_HEADER( SetPointAcoustics_Phi )
MYSQL_ACCESSOR_HEADER( SetPointAcoustics_Rho )
MYSQL_ACCESSOR_HEADER( SetPointOverride_Theta )
MYSQL_ACCESSOR_HEADER( SetPointOverride_Phi )
MYSQL_ACCESSOR_HEADER( SetPointOverride_Rho )

/* PID Tunables */
MYSQL_ACCESSOR_HEADER( DepthPID_p )
MYSQL_ACCESSOR_HEADER( DepthPID_i )
MYSQL_ACCESSOR_HEADER( DepthPID_d )
MYSQL_ACCESSOR_HEADER( AltitudePID_p )
MYSQL_ACCESSOR_HEADER( AltitudePID_i )
MYSQL_ACCESSOR_HEADER( AltitudePID_d )
MYSQL_ACCESSOR_HEADER( RollPID_p )
MYSQL_ACCESSOR_HEADER( RollPID_i )
MYSQL_ACCESSOR_HEADER( RollPID_d )
MYSQL_ACCESSOR_HEADER( PitchPID_p )
MYSQL_ACCESSOR_HEADER( PitchPID_i )
MYSQL_ACCESSOR_HEADER( PitchPID_d )
MYSQL_ACCESSOR_HEADER( YawPID_p )
MYSQL_ACCESSOR_HEADER( YawPID_i )
MYSQL_ACCESSOR_HEADER( YawPID_d )

/* Thrusters */
MYSQL_ACCESSOR_HEADER( Aft )
MYSQL_ACCESSOR_HEADER( PortX )
MYSQL_ACCESSOR_HEADER( PortY )
MYSQL_ACCESSOR_HEADER( StarX )
MYSQL_ACCESSOR_HEADER( StarY )

/* Vision information */
MYSQL_ACCESSOR_HEADER( VisionTarget )
MYSQL_ACCESSOR_HEADER( VisionFound )

/* Status */
MYSQL_ACCESSOR_HEADER( MissionStatus )
MYSQL_ACCESSOR_HEADER( CountDownStatus )

/* Depth controller */
MYSQL_ACCESSOR_HEADER( TrackerDoDepth )
MYSQL_ACCESSOR_HEADER( PIDDoYaw )

/* Pinger delays */
MYSQL_ACCESSOR_HEADER( PingDelay_a )
MYSQL_ACCESSOR_HEADER( PingDelay_b )
MYSQL_ACCESSOR_HEADER( PingDelay_c )

#endif // #ifndef __SEAWOLF_SEASQL_INCLUDE_H
