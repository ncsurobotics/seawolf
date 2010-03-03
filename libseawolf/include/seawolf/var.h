/**
 * \file
 */

#ifndef __SEAWOLF_VAR_INCLUDE_H
#define __SEAWOLF_VAR_INCLUDE_H

void Var_init(void);
float Var_get(char* name);
void Var_setAutoNotify(bool autonotify);
void Var_set(char* name, float value);
void Var_close(void);

#endif // #ifndef __SEAWOLF_VAR_INCLUDE_H
