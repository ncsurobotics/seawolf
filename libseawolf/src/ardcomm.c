/**
 * \file
 * \brief Arduion communication
 */

#include "seawolf.h"

#include <ctype.h>
#include <termios.h>
#include <unistd.h>

/**
 * Starts a mesage
 * \private
 */
#define START_FRAME  '{'

/**
 * Splits a message
 * \private
 */
#define TYPE_DIVIDER '|'

/**
 * Ends a mesage
 * \private
 */
#define END_FRAME    '}'

/**
 * \defgroup Ard Arduino
 * \ingroup Hardware
 * \brief Provides standardized message passing to Arduino microcontrollers
 * \{
 */

/**
 * \brief Get a raw message
 * \deprecated Raw serial access should be used instead to keep speed acceptible
 *
 * Get a raw message from an Arduino
 *
 * \param sp The serial port to read from
 * \param[out] msgtype Buffer to store the message type into
 * \param[out] buffer Buffer to store the message data into
 * \return Success status, -1 is failure, 1 is success
 */
int ArdComm_getMessage(SerialPort sp, char* msgtype, char* buffer) {
    /* Clear lengths */
    int tmp = 0;
    size_t msgtype_s = 0;
    size_t buffer_s = 0;

    /* Find next frame */
    while(tmp != START_FRAME) {
        tmp = Serial_getByte(sp);
        if(tmp == -1) {
            /* Wasn't able to read, return */
            return -1;
        }
    }

    /* Read type */
    while((msgtype[msgtype_s] = Serial_getByte(sp)) != TYPE_DIVIDER) {
        if(msgtype[msgtype_s] == END_FRAME || msgtype[msgtype_s] == START_FRAME) {
            /* Error. Frame ended or new frame started */
            return -1;
        }
        msgtype_s++;
    }
    msgtype[msgtype_s] = '\0';

    /* Read message */
    while((buffer[buffer_s] = Serial_getByte(sp)) != END_FRAME) {
        if(msgtype[buffer_s] == TYPE_DIVIDER || msgtype[buffer_s] == START_FRAME) {
            /* Error. New frame started or invalid type divider */
            return -1;
        }
        buffer_s++;
    }
    buffer[buffer_s] = '\0';
    
    return 1;
}

/**
 * \brief Send a message
 * \deprecated Raw serial access should be used instead to keep speed acceptible
 *
 * Send a raw message to an Arduino
 *
 * \param sp The serial port to send to
 * \param msgtype The message type
 * \param buffer The message data
 */
void ArdComm_sendMessage(SerialPort sp, char* msgtype, char* buffer) {
    /* Send message in standard format */
    Serial_sendByte(sp, START_FRAME);
    Serial_send(sp, msgtype, strlen(msgtype));
    Serial_sendByte(sp, TYPE_DIVIDER);
    Serial_send(sp, buffer, strlen(buffer));
    Serial_sendByte(sp, END_FRAME);

    /* Newline will be ignored but will make console debugging nice */
    Serial_sendByte(sp, '\n');
}

/**
 * \brief Perform a handshake routine
 *
 * Establish a connection with an Arduino through a handshake process
 *
 * \param sp Serial port arduino is communicted through
 * \return -1 on failure, 0 on success
 */
int ArdComm_handshake(SerialPort sp) {
    /* Send established connection message */
    char name[64];

    if(ArdComm_getId(sp, name) == -1) {
        return -1;
    }

    ArdComm_sendMessage(sp, "ESTABLISHED", "NULL");
    ArdComm_sendMessage(sp, "READY", "NULL");
    Serial_flush(sp);

    return 0;
}

/**
 * \brief Get the Arduino ID
 *
 * Get the identifier from an Arduino before handshaking is performed
 *
 * \param sp Serial port to communicate on
 * \param[out] id Buffer to store identifier into
 * \return Success status; -1 if failure, 1 is success
 */
int ArdComm_getId(SerialPort sp, char* id) {
    char type[16] = {[0] = '\0'};

    /* Get a message */
    if(ArdComm_getMessage(sp, type, id) == -1) {
        return -1;
    }

    /* Log possible error */
    if(strcmp(type, "ID") != 0) {
        id[0] = '\0'; /* Clear ID string */
        Logging_log(ERROR, "Error while attempting to read ID");
        return -1;
    }

    return 0;
}

/** \} */
