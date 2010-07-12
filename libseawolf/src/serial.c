/**
 * \file
 * \brief Serial port access
 */

#include "seawolf.h"

#include <asm/ioctls.h>
#include <fcntl.h>
#include <poll.h>
#include <unistd.h>
#include <sys/ioctl.h>
#include <termios.h>

/** True if the serial component has been initialized */
static bool initialized = false;

/** List of open devices */
static SerialPort* devices = NULL;

/** Number of open devices */
static int open_devices = 0;

/** A copy of the default parameters on a port so that they may be returned on
    exit */
static struct termios* default_conf = NULL;

/**
 * \defgroup Serial Serial access
 * \ingroup Hardware
 * \brief Functions for accessing and using serial ports
 * \{
 */

/**
 * \brief Initialize the Serial component of libseawolf 
 * \private
 */
void Serial_init(void) {
    initialized = true;
}

/**
 * \brief Set all standard options on the serial port 
 *
 * Called by Serial_open* to initialize a serial port and set all default
 * options on it. The port is placed into a mode equivalent to 8 data bits, one
 * stop bit, no parity bits, and 9600 baud
 *
 * \param sp Handler for the serial port to set defaults on
 * \return 0 if successful, -1 in case of error
 */
static int Serial_setParams(SerialPort sp) {
    struct termios term_conf;

    /* Load attributes */
    tcgetattr(sp, &term_conf);

    /* Set options */
    term_conf.c_cflag &= ~PARENB;
    term_conf.c_cflag &= ~CSTOPB;
    term_conf.c_cflag &= ~CSIZE;
    term_conf.c_cflag |= CS8 | CLOCAL | CREAD;

    term_conf.c_iflag = IGNPAR;
    term_conf.c_oflag = 0;
    term_conf.c_lflag = 0;

    /* Set speeds */
    cfsetispeed(&term_conf, B9600);
    cfsetospeed(&term_conf, B9600);
    
    Serial_flush(sp);

    /* Push to device immediately */
    if(tcsetattr(sp, TCSANOW, &term_conf) != 0) {
        return -1;
    }

    /* Flush once more for good measure */
    Serial_flush(sp);
    return 0;
}

/**
 * \brief Open a virtual terminal device
 * \deprecated The use of virtual terminal devices is unsupported and has limited functionality
 *
 * Open a new virtual terminal (VTY) device
 *
 * \return A handler for the opened device
 */
SerialPort Serial_openVTY(void) {
    SerialPort sp = open("/dev/ptmx", O_RDWR | O_NOCTTY);
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
 * \brief Open a serial port
 *
 * Open and return a handler for the given serial device
 *
 * \param device_path The device path
 * \return The serial port handler or -1 in the case of failure to open
 */
SerialPort Serial_open(const char* device_path) {
    SerialPort sp = open(device_path, O_RDWR | O_NOCTTY | O_NONBLOCK);
    if(sp == -1) {
        /* Error opening port */
        return -1;
    }

    /* Store default attribute set */
    if(default_conf == NULL) {
        default_conf = malloc(sizeof(struct termios));
        tcgetattr(sp, default_conf);
    }

    /* Set standard serial port options */
    if(Serial_setParams(sp) == -1) {
        return -1;
    }

    /* Store device reference in the local device list */
    open_devices++;
    devices = realloc(devices, open_devices * sizeof(SerialPort));
    devices[open_devices-1] = sp;

    return sp;
}

/**
 * \brief Close a serial device
 *
 * Close a previously open serial device
 *
 * \param sp The handler for the serial port to close
 * \return -1 on failure
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
        Logging_log(ERROR, __Util_format("Error closing serial port: %s", strerror(errno)));
    }

    return return_value;
}

/**
 * \brief Set the baud rate
 * 
 * Set the baud rate for a serial device. Default is 9600 baud
 *
 * \param sp A handler for the serial port to set the buad rate for
 * \param baud The baud rate to set
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
        Logging_log(ERROR, __Util_format("Invalid baud rate %d", baud));
        return;
    }

    /* Set speeds */
    cfsetispeed(&term_conf, real_baud);
    cfsetospeed(&term_conf, real_baud);
    
    /* Push settings changes to device immediately */
    Serial_flush(sp);
    tcsetattr(sp, TCSANOW, &term_conf);

    /* Is this necessary? */
    Serial_flush(sp);
}

/**
 * \brief Flush input buffers
 *
 * Flush the input buffers for the given port
 *
 * \param sp A handler for a serial port to flush
 */
void Serial_flush(SerialPort sp) {
    tcflush(sp, TCIOFLUSH); /* Zero input buffers */
}

/**
 * \brief Set blocking
 *
 * Set the given port to be blocking
 *
 * \param sp A handler for a serial port
 */
void Serial_setBlocking(SerialPort sp) {
    /* Unset non-blocking */
    fcntl(sp, F_SETFL, fcntl(sp, F_GETFL) & (~O_NONBLOCK));
}

/**
 * \brief Set non-blocking
 *
 * Set the given port to be non-blocking
 *
 * \param sp A handler for a serial port
 */
void Serial_setNonBlocking(SerialPort sp) {
    /* Set non-blocking */
    fcntl(sp, F_SETFL, fcntl(sp, F_GETFL) | O_NONBLOCK);
}

/**
 * \brief Check if a serial port is "ready"
 * \deprecated This function is completely useless and ineffective. It should
 * not be used; determining if a serial port is "ready" is high application
 * particular
 * 
 * Determine if a serial port is "ready" by probing it and attempting to receive
 * data.
 *
 * \param sp Handler for a serial port to test
 * \return true if the port is ready, false otherwise
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
        Logging_log(DEBUG, __Util_format("Probe returned %d bytes", n));
    }
#endif

    /* We are ready if we read 1 byte rather than 0 */
    return (n == 1);
}

/**
 * \brief Get a byte
 *
 * Read a single byte from the serial device
 *
 * \param sp Handler for device to read from
 * \return -1 in case of failure, otherwise the byte read
 */
int Serial_getByte(SerialPort sp) {
    unsigned char b;

    /* Get a byte */
    if(Serial_get(sp, &b, 1)) {
        return -1;
    }

    return b;
}

/**
 * \brief Read a line from a serial device
 *
 * Return a newline terminated line from the given serial device
 *
 * \param sp Handler for the device to read from
 * \param[out] buffer The buffer to write the line into
 * \return -1 if an error occurs, 0 otherwise
 */
int Serial_getLine(SerialPort sp, char* buffer) {
    int n = 0;
    int i = 0;

    while(n == 0 || n == -1 || n == '\n') {
        n = Serial_getByte(sp);
    }

    buffer[0] = n;
    do {
        n = Serial_getByte(sp);
        if (n == -1) { return -1; }
        buffer[++i] = n;
    } while(n != '\n');
    buffer[i] = '\0';
    return 0;
}

/**
 * \brief Read data from a serial device
 *
 * Store count bytes of data from the serial port into the buffer
 *
 * \param sp Handler for the device to read from
 * \param[out] buffer The buffer to read into
 * \param count The number of bytes to read
 * \return -1 if an error occurs, 0 otherwise
 */
int Serial_get(SerialPort sp, void* buffer, size_t count) {
    struct pollfd fd = {.fd = sp, .events = POLLRDNORM};
    int blocking = (~fcntl(sp, F_GETFL)) & O_NONBLOCK;
    unsigned char* buffer_c = (unsigned char*) buffer;
    size_t n; 

    while(count > 0) {
        if(blocking) {
            poll(&fd, 1, -1);
        }

        n = read(sp, buffer_c, count);
        if(n == -1) {
            return -1;
        }

        count -= n;
        buffer_c += n;
    }
    
    return 0;
}

/**
 * \brief Send a byte
 *
 * Send a single byte out of the serial port
 *
 * \param sp Handler for the port to write to
 * \param b The byte to write
 * \return -1 if a write errors occurs, 0 otherwise
 */
int Serial_sendByte(SerialPort sp, unsigned char b) {
    return Serial_send(sp, &b, 1);
}

/**
 * \brief Send data
 *
 * Send multiple bytes via the given serial device
 *
 * \param sp Handler for the device to send data on
 * \param buffer The buffer to read from
 * \param count Number of bytes to write
 * \return -1 if a write error occurs, 0 otherwise
 */
int Serial_send(SerialPort sp, void* buffer, size_t count) {
    unsigned char* buffer_c = (unsigned char*) buffer;
    size_t n;

    while(count) {
        n = write(sp, buffer_c, count);
        if(n == -1) {
            return -1;
        }

        count -= n;
        buffer_c += n;
    }

    return 0;
}

/**
 * \brief Control the DTR line
 *
 * Set the DTR line on the given serial port
 *
 * \param sp Handler for the devices to toggle DTR on
 * \param value 0 to clear DTR. 1 to assert
 */
void Serial_setDTR(SerialPort sp, int value) {
    unsigned int base;

    /* Copy out ioctl settings */
    ioctl(sp, TIOCMGET, &base);

    if(value) {
        /* Assert DTR */
        base |= TIOCM_DTR;
    } else {
        /* Clear DTR */
        base &= ~TIOCM_DTR;
    }
    
    ioctl(sp, TIOCMSET, &base);
}

/**
 * \brief Checks for data
 *
 * Returns the number of bytes available in the serial buffer
 *
 * \param sp Handler for the device to check
 * \return The number of bytes available to be read or -1 if an error occured
 */
int Serial_available(SerialPort sp) {
    int available;

    if(ioctl(sp, FIONREAD, &available)) {
        return -1;
    }

    return available;
}

/**
 * \brief Close the Serial component of libseawolf
 * \private
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

/** \} */
