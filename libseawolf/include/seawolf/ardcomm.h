
#ifndef __SEAWOLF_ARDCOMM_INCLUDE_H
#define __SEAWOLF_ARDCOMM_INCLUDE_H

#include "seawolf.h"

/* Message types

   ID := Identify an arduino to the host (pc <- ard)
     identifier := [a-zA-Z0-9]+
     format     := "{ID|" <identifier> "}"

   COMMAND := Execute a function with the given parameters (pc -> ard)
     float  := [1-9][0-9]* ("." [0-9]*)?
     format := "{COMMAND|" <identifier> (" " <float>)* "}"

   REQUESTVAR := Request and update for a variable (pc <-> ard)
     format := "{REQUESTUPDATE|" <identifier> "}"

   UPDATEVAR := Provide a new update value for a variable (pc <-> ard)
     format := "{UPDATEVAR|" <identifier> "=" <float> "}"

   LOG := Provide ability to log to database to devices (pc <- ard)
     message  := [a-zA-Z0-9]*
     severity := "ERROR" | "INFO" | "DEBUG"
     format   := "{LOG|" <severity> " " <message> "}"

   ESTABLISHED := Connection to Arduino established (pc -> ard)
     format := "{ESTABLISHED|NULL}"

   READY := Connection to Arduino ready (pc -> ard)
     format := "{READY|NULL}"

   TERMINATE := Terminate communication with the Arduino (pc -> ard)
     format := "{TERMINATE|NULL}"
*/

/* Message transmission */
void ArdComm_sendMessage(SerialPort sp, char* msgtype, char* buffer);
int ArdComm_getMessage(SerialPort sp, char* msgtype, char* buffer);

/* Connection initialization */
void ArdComm_handshake(SerialPort sp);
int ArdComm_getId(SerialPort sp, char* id);

/* Send commmands */
void ArdComm_sendCommand(SerialPort sp, char* command, float* params, size_t param_n);
void ArdComm_sendRequestVar(SerialPort sp, char* var);
void ArdComm_sendVarUpdate(SerialPort sp, char* var, float value);

/* Parse commands for Serial_get_message */
void ArdComm_parseUpdateVar(char* buffer, char* var, float* value);
void ArdComm_parseCommand(char* buffer, char* command, float* params, size_t* param_n);
void ArdComm_parseLog(char* buffer, int* log_level, char* message);

#endif // #ifndef __SEAWOLF_ARDCOMM_INCLUDE_H
