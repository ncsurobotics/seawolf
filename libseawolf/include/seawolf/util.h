/**
 * \file
 */

#ifndef __SEAWOLF_UTIL_INCLUDE_H
#define __SEAWOLF_UTIL_INCLUDE_H

/* Sleep for s seconds */
void Util_usleep(double s);

/* Return a formatted string, seperate version for use internal to libseawolf */
char* Util_format(char* format, ...);
char* __Util_format(char* format, ...);

/* Strip spaces from a string */
void Util_strip(char* buffer);

/* Split a buffer by a character and place into the buffers p1 and p2 */
int Util_split(const char* buffer, char split, char* p1, char* p2);

void Util_close(void);


/**
 * \addtogroup Util
 * \{
 */

/**
 * Return the max of a and b
 *
 * \param a first value
 * \param b second value
 * \return The max of a and b
 */
#define Util_max(a, b) (((a) > (b)) ? (a) : (b))

/**
 * Return the min of a and b
 *
 * \param a first value
 * \param b second value
 * \return The min of a and b
 */
#define Util_min(a, b) (((a) < (b)) ? (a) : (b))

/**
 * Bound a value between a maximum and minimum
 *
 * \param a Lower bound
 * \param x The value to bound
 * \param b Upper bound
 * \return x if a <= x <= b, a if x < a, and b if x > b
 */
#define Util_inRange(a, x, b) (((x) < (a)) ? (a) : (((x) > (b)) ? (b) : (x)))

/** \} */

#endif // #ifndef __SEAWOLF_UTIL_INCLUDE_H
