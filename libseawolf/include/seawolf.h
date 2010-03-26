/**
 * \file
 * \brief Top level libseawolf include
 */

/**
 * \mainpage
 *
 * \section intro Introduction
 *
 * Here you will find all documentation for the Seawolf core library
 * (<i>libseawolf</i>) and the Seawolf hub server (<i>hub server</i>). Together
 * these are refered to as the <i>Seawolf Framework</i> (SF). The framework
 * provides a foundation for building distributed software platforms for use in
 * robotics and other sensor/control systems. libseawolf provides numerous
 * utilities to ease development, and in part with the hub server, also provides
 * message passing, shared variables, and centralized configuration and logging
 * to make building distributed systems quick and easy.
 *
 * \section Design
 *
 * When refering to an individual program compiled against libseawolf we will
 * refer to it as an \e application. When referring to multiple applications
 * running together with a single hub server, we refer to this as an
 * <i>application pool</i>. When using the Seawolf Framework the goal is to
 * design multiple applications which can work with one another as an
 * application pool. The primary advantage of this design is that applications
 * can easily be distributed across multiple devices connected via a
 * network. Additionally, this multiple application approach generally improves
 * reliability and fault tolerance, as applications are well isolated from one
 * another. A typical application pool may look as follows,
 *
 * \dot
 *  graph {
 *    node [shape=Mrecord, style="filled", fillcolor="#aaddff", fontname="Sans"];
 *    edge [dir=both, arrowsize=0.9, color="#101020"];
 *    fontname="Sans";
 *    nodesep = 0.6;
 *    pad = 0.5;
 *
 *    application_1:lib:s -- hub;
 *    application_2:lib:s -- hub;
 *    application_3:lib:s -- hub;
 *    application_4:lib:s -- hub;
 *
 *    subgraph cluster_applications {
 *      application_4 [label="{Application 1|<lib> libseawolf}"];
 *      application_3 [label="{Application 2|<lib> libseawolf}"];
 *      application_2 [label="{Application 3|<lib> libseawolf}"];
 *      application_1 [label="{...|<lib> libseawolf}"];
 *      label = "Application Pool";
 *      style = "filled, rounded";
 *      color = "#eeeeee";
 *    }
 *    hub [label="{Hub server|{libseawolf | sqlite}}", fillcolor="#aaaaff"];
 *  }
 * \enddot
 *
 * As can be seen, each application is built on top of libseawolf, and, when
 * running, all applications in the pool connect to a single hub
 * server. libseawolf handles all of the difficult work of communicating with
 * the hub server and provides an easy to use API for application developers
 * providing shared variables, interprocess notifications, and centralized
 * logging.
 *
 * \section writinganapp Writing an Application
 *
 * Writing applications using the Seawolf Framework is made as simple as
 * possible. The following is the outline of a typical Seawolf Framework based
 * application,
 *
 * \code
 * #include "seawolf.h"
 *
 * int main(void) {
 *    Seawolf_loadConfig("../conf/seawolf.conf");
 *    Seawolf_init("My application name");
 *
 *    ...
 *
 *    Seawolf_close();
 *    return 0;
 * }
 * \endcode
 *
 * For most applications this is all the boilerplate code that is
 * neccessary. The first two lines in main() are responsible for loading a
 * configuration file and initializing the library. The configuration file
 * specifies the address and port of the hub server to connect to, as well as
 * the password to use when authenticating with the hub server. No other
 * configuration is done is this file. The argument passed to Seawolf_init()
 * specifies the name of the application. This name is primarily for logging
 * purposes.
 *
 * \section hubserver Hub Server
 *
 * The hub server is responsible for performing logging, variable storage, and
 * notification passing for applications and much of this functionality is
 * configurable. The hub server uses an <a href="http://sqlite.org">SQLite</a>
 * database which stores all configuration, variable definitions, and persistant
 * variable data. The database can be editted with the <tt>sqlite3</tt> command
 * line utility. The hub server uses three tables,
 *  - <tt>variables</tt> - The variables table stores the most recent value of persistent variables
 *  - <tt>variable_definitions</tt> - This table stores definitions of variables which the
 *    hub server makes available. Only variables defined in this table can be
 *    accessed by applications.
 *  - <tt>config</tt> - Configuration options used by the hub server
 *
 * The <tt>variables</tt> table is not meant to be edited by hand and serves only as
 * persistent for the hub server. The valid options for the <tt>config</tt> table are
 *  - log_file - The specifies the log file for the hub to write log messages
 *    to. If this isn't specified the hub will log to its own standard output
 *  - password - The password for the hub server to use when authenticating
 *    clients. This option is required but may be left empty.
 *
 * Each row in the <tt>variable_definitions</tt> table defines a new variable. The colums in this table are,
 *  - name - The name of the variable. This is a what should be passed to Var_get() and Var_set() calls.
 *  - default_value - This is the initial value of the variable after the hub
 *    server starts. If the variable is persistent then an existing value in the
 *    <tt>variables</tt> table will override this.
 *  - persistent - This boolean value specifies whether the variable should be
 *    persistent. Persistent variables retain their value if the hub is
 *    restarted.
 *  - readonly - This boolean value specifies if the variable should be read
 *    only. Read only options values are useful as configuration values shared
 *    between applications as well as defining shared constants.
 *
 * \section components API Organization
 * 
 * The library is organized into \e components such that functions in a component
 * have the form \e Component_someFunction(...). These components can further be
 * grouped according to use or functionality.
 *
 * \subsection core_routines Core
 * These routines include core library initialization and configuration
 *  - \ref Main "Seawolf" - Library initialization and control routines.
 *  - \ref Config "Configuration" - Loading configuration options
 *
 * \subsection comm_routines Communication
 * These components focus on interprocess communication and application -> hub
 * communication.
 *  - \ref Comm "Comm" - Low level routines for communicating with a connected
 *    hub server. Unlikely to be used in applications.
 *  - \ref Logging "Logging" - Facilities for logging, both local and centralized
 *    through the hub server
 *  - \ref Notify "Notify" - Sending and receiving notifications. Notifications
 *    are broadcast messages sent between applications
 *  - \ref Var "Var" - Support for setting and retrieving shared variables
 * 
 * \subsection datastructure_routines Data Structures
 * A number of useful and common data structures are provided for general use.
 *  - \ref Dictionary "Dictionary" - A dictionary, also known as a lookup table
 *    or hash map
 *  - \ref List "List" - A simple list/array with support for many useful routines
 *  - \ref Queue "Queue" - A thread-safe queue implementation
 *  - \ref Stack "Stack" - A simple first-in-last-out stack
 *
 * \subsection hardware_routines Hardware Access
 * Serial access is complicated and error-prone so a easy to use serial API as
 * well as routines for establishing and identify microcontrollers serially
 * attached is provided.
 *  - \ref Serial "Serial" - Routines for opening serial devices and sending and
 *    receive data
 *  - \ref Ard "ArdComm" - Identifying and handshaking with microcontrollers
 *    following the ArdComm protocol
 * 
 * \subsection misc_routines Utilities
 * A number of utilities often useful in robotics and other control systems
 * applications are provided as part of the library
 *  - \ref PID "PID" - Generic implementation of a
 *    Proportional-Integral-Derivative (PID) controller
 *  - \ref Task "Task" - Support for task scheduling and running backgroud tasks
 *  - \ref Timer "Timer" - Timers for easily keeping track of changes in time
 *  - \ref Util "Util" - A number of misc, but useful utilities
 */

/**
 * \defgroup Core Core Routines
 * \defgroup Communications Communications
 * \defgroup DataStructures Data Structures
 * \defgroup Hardware Hardware Access
 * \defgroup Utilities Utilities
 */

#ifndef __SEAWOLF_ROOT_INCLUDE_H
#define __SEAWOLF_ROOT_INCLUDE_H

/**
 * Make available POSIX functions
 */
#define _POSIX_C_SOURCE 199309L

/**
 * Make more functions available
 */
#define _XOPEN_SOURCE 500

/* Make sure some standard includes are available */
#include <assert.h>
#include <errno.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <string.h>
#include <stdint.h>

/* Include all Seawolf III development headers */
#include "seawolf/seawolf_config.h"

#include "seawolf/comm.h"
#include "seawolf/logging.h"
#include "seawolf/var.h"
#include "seawolf/notify.h"

#include "seawolf/serial.h"
#include "seawolf/ardcomm.h"

#include "seawolf/util.h"
#include "seawolf/timer.h"
#include "seawolf/task.h"
#include "seawolf/pid.h"

#include "seawolf/stack.h"
#include "seawolf/list.h"
#include "seawolf/queue.h"
#include "seawolf/dictionary.h"

/* Initialize and close */
void Seawolf_init(const char* name);
void Seawolf_close(void);
void Seawolf_exitError(void);
void Seawolf_exit(void);
bool Seawolf_closing(void);
char* Seawolf_getName(void);

#endif // #ifndef __SEAWOLF_ROOT_INCLUDE_H
