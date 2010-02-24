
#include "seawolf.h"

#include <errno.h>
#include <fcntl.h>
#include <string.h>
#include <stdlib.h>
#include <unistd.h>
#include <termios.h>
#include <stdio.h>
#include <time.h>

static bool initialized = false;
static SerialPort* devices = NULL;
static int open_devices = 0;
static struct termios* default_conf = NULL;

/**
 * Initialize the Serial component of libseawolf 
 */
void Serial_init(void) {
    initialized = true;
}

/**
 * Close the Serial component of libseawolf
 */
void Serial_close(void) {
    if(initialized) {
        /* Close each port that is still open */
        for(int i = 0; i < open_devices; i++) {
            Serial_closePort(devices[i]);
        }
        
        /* Free the list of devices */
        free(devices);
    }
}

/**
 * Set all standard options on the serial port 
 */
static void Serial_setParams(SerialPort sp) {
    struct termios term_conf;

    /* Load attributes */
    tcgetattr(sp, &term_conf);

    /* Set options */
    term_conf.c_iflag &= IGNBRK | IGNCR | IGNPAR | IXANY | ~(IXOFF | IXON | INPCK);
    term_conf.c_oflag &= ~(OPOST);
    term_conf.c_cflag  = CLOCAL;
    term_conf.c_lflag &= ~(ECHO | ECHONL | ICANON | ISIG | IEXTEN);

    /* Set speeds */
    cfsetispeed(&term_conf, B9600);
    cfsetospeed(&term_conf, B9600);
    
    /* Push to device immediately */
    tcsetattr(sp, TCSANOW, &term_conf);
}

/**
 * Open a new "virtual" terminal device
 */
SerialPort Serial_openVTY(void) {
    SerialPort sp = open("/dev/ptmx", O_RDWR | O_NOCTTY | O_NONBLOCK);
    Serial_setParams(sp);
    unlockpt(sp);
    grantpt(sp);

    /* Store device reference */
    open_devices++;
    devices = realloc(devices, open_devices * sizeof(SerialPort));
    devices[open_devices-1] = sp;

    return sp;
}

/**
 * Open a real serial device
 */
SerialPort Serial_open(const char* device_path) {
    SerialPort sp = open(device_path, O_RDWR | O_NOCTTY | O_NONBLOCK);
    if(sp == -1) {
        /* Error opening port */
        return 0;
    }

    /* Store default attribute set */
    if(default_conf == NULL) {
        default_conf = malloc(sizeof(struct termios));
        tcgetattr(sp, default_conf);
    }

    /* Set standard serial port options */
    Serial_setParams(sp);

    /* Store device reference in the local device list */
    open_devices++;
    devices = realloc(devices, open_devices * sizeof(SerialPort));
    devices[open_devices-1] = sp;

    return sp;
}

/**
 * Close an open device
 */
int Serial_closePort(SerialPort sp) {
    int return_value; 

    /* Locate the device in the local device list so it can be removed */
    for(int i = 0; i < open_devices; i++) {
        if(devices[i] == sp) {
            /* Overwrite the device to be closed and move the last item into its
               place in order to shrink the list */
            devices[i] = devices[open_devices-1];
            break;
        }
    }

    /* Shrink the list */
    open_devices--;
    devices = realloc(devices, open_devices * sizeof(SerialPort));

    /* Restore terminal properties */
    tcsetattr(sp, TCSANOW, default_conf);

    /* Actually close the device */
    return_value = close(sp);

    /* Error */
    if(return_value == -1) {
        Logging_log(ERROR, Util_format("Error closing serial port: %s", strerror(errno)));
    }

    return return_value;
}

/**
 * Set the baud rate for a serial device. Initially this is set to 9600 baud.
 */
void Serial_setBaud(SerialPort sp, int baud) {
    struct termios term_conf;

    /* Load current attributes */
    tcgetattr(sp, &term_conf);

    /* Convert from int to a valid baud rate constant  */
    int real_baud = 0;
    switch(baud) {
    case 50:
        real_baud = B50;
        break;
    case 75:
        real_baud = B75;
        break;
    case 110:
        real_baud = B110;
        break;
    case 134:
        real_baud = B134;
        break;
    case 150:
        real_baud = B150;
        break;
    case 200:
        real_baud = B200;
        break;
    case 300:
        real_baud = B300;
        break;
    case 600:
        real_baud = B600;
        break;
    case 1200:
        real_baud = B1200;
        break;
    case 1800:
        real_baud = B1800;
        break;
    case 2400:
        real_baud = B2400;
        break;
    case 4800:
        real_baud = B4800;
        break;
    case 9600:
        real_baud = B9600;
        break;
    case 19200:
        real_baud = B19200;
        break;
    case 38400:
        real_baud = B38400;
        break;
    default:
        Logging_log(ERROR, Util_format("Invalid baud rate %d", baud));
        return;
    }

    /* Set speeds */
    cfsetispeed(&term_conf, real_baud);
    cfsetospeed(&term_conf, real_baud);
    
    /* Push settings changes to device immediately */
    tcsetattr(sp, TCSANOW, &term_conf);

    Serial_flush(sp);
    Util_usleep(0.5);
}

void Serial_flush(SerialPort sp) {
    tcdrain(sp); /* Wait for output to be drained */
    tcflush(sp, TCIOFLUSH); /* Zero input buffers */
}

/**
 * Set the device to be blocking 
 */
void Serial_setBlocking(SerialPort sp) {
    /* Unset non-blocking */
    fcntl(sp, F_SETFL, 0);
}

/**
 * Set the device to be non-blocking
 */
void Serial_setNonBlocking(SerialPort sp) {
    /* Unset non-blocking */
    fcntl(sp, F_SETFL, O_NONBLOCK);
}

/**
 * Check if a serial port is "ready". A serial port is considered "ready" if any
 * data is available within a quarter of a second to read from the port. This is
 * not a very effective test and should not be used in most cases.
 */
bool Serial_isReady(SerialPort sp) {
    int a, n;

#ifdef SEAWOLF_DEBUG
    Logging_log(DEBUG, "Probing ready state");
#endif

    /* Set non-blocking */
    fcntl(sp, F_SETFL, O_NONBLOCK);

    /* Check for available data */
    Util_usleep(0.25);
    n = read(sp, &a, 1);
    
    /* Unset non-blocking */
    fcntl(sp, F_SETFL, 0);

#ifdef SEAWOLF_DEBUG
    if(n == 0) {
        Logging_log(DEBUG, "Probe failed...");
    } else {
        Logging_log(DEBUG, Util_format("Probe returned %d bytes", n));
    }
#endif

    /* We are ready if we read 1 byte rather than 0 */
    return (n == 1);
}

/**
 * Read a single byte from the serial device
 */
int Serial_getByte(SerialPort sp) {
    int n = 0;
    unsigned char b;

    /* Get a byte */
    while(n == 0) {
        n = read(sp, &b, 1);
        if(n == -1) {
            return -1;
        }
    }
    return b;
}

/**
 * Store a "line" of data from the serial port, terminated by a newline (\n) into the buffer
 */
void Serial_getLine(SerialPort sp, char* buffer) {
    while((*buffer = Serial_getByte(sp)) == '\n');
    while(*(buffer++) != '\n') {
        *buffer = Serial_getByte(sp);
    }
    *(buffer-1) = 0;
}

/**
 * Store count bytes of data from the serial port into the buffer
 */
void Serial_get(SerialPort sp, void* buffer, size_t count) {
    unsigned char* buffer_c = (unsigned char*) buffer;
    while(count--) {
        *buffer_c = Serial_getByte(sp);
        buffer_c++;
    }
}

/**
 * Send a single byte out of the serial port
 */
void Serial_sendByte(SerialPort sp, unsigned char b) {
    Serial_send(sp, &b, 1);
}

/**
 * Send size bytes of data from the buffer to the serial port 
 */
void Serial_send(SerialPort sp, void* buffer, size_t count) {
    int sent = 0;
    unsigned char* buffer_c = (unsigned char*) buffer;
    while(sent < count) {
        sent += write(sp, buffer_c + sent, count - sent);
    }        
}
