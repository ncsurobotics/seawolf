/* Your system includes go here */

#include "seawolf.h"

int main(void) {
  /* Load the Seawolf configuration file */
  Seawolf_loadConfig("../conf/seawolf.conf");

  /* Initialize all libseawolf components and register
     this application with the given name */
  Seawolf_init("Test Application");

  /* your code goes here... */

  /* Clean up and close all libseawolf components */
  Seawolf_close();
  return 0;
}
