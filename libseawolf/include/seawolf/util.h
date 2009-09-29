
#ifndef __SEAWOLF_UTIL_INCLUDE_H
#define __SEAWOLF_UTIL_INCLUDE_H

void Util_close(void);

/* Sleep for s seconds */
void Util_usleep(double s);

/* Return a formatted string */
char* Util_format(char* format, ...);

/* Strip spaces from a string */
void Util_strip(char* buffer);

/* Split a buffer by a character and place into the buffers p1 and p2 */
int Util_split(const char* buffer, char split, char* p1, char* p2);

/* Macros */
#define Util_max(a, b) (((a) > (b)) ? (a) : (b))
#define Util_min(a, b) (((a) < (b)) ? (a) : (b))
#define Util_inRange(a, x, b) (((x) < (a)) ? (a) : (((x) > (b)) ? (b) : (x)))

#endif // #ifndef __SEAWOLF_UTIL_INCLUDE_H
