
extern "C" {
    #include "seawolf.h"
}

#include <jaus/mobility/sensors/globalposesensor.h>
#include <jaus/mobility/sensors/localposesensor.h>
#include <jaus/mobility/sensors/velocitystatesensor.h>
#include <jaus/mobility/drivers/localwaypointlistdriver.h>
#include <jaus/core/transport/judp.h>
 
#include <jaus/core/component.h>
#include <cxutils/keyboard.h>
#include <cxutils/math/cxmath.h>

#include <iostream>
#include <cstring>
#include <cstdio>
#include <cmath>
 
JAUS::UShort gSubsystemID   = 137;    // ID of our subsystem to use.
JAUS::Byte gNodeID          = 1;      // ID of our node to use.
JAUS::Byte gComponentID     = 1;      // ID of the our component.

/* Calculate the rate of change in the yaw with respect to time */
static float yaw_dt(float yaw) {
    static Timer* timer = NULL;
    static float yaw_last;
    double dt, rate;

    if(timer == NULL) {
        timer = Timer_new();
        yaw_last = yaw;
        rate = 0.0;
    } else {
        dt = Timer_getDelta(timer);
        rate = (yaw - yaw_last) / dt;
        yaw_last = yaw;
    }

    return rate;
}

////////////////////////////////////////////////////////////////////////////////////
///
///   \brief Entry point of jaus_challenge_2010.cpp
///
///   This program demonstrates everything required to complete the JAUS
///   Interoperability Challenge for 2010.  In this program a simulated robot
///   is created which can drive to local waypoints.  This program has
///   run against the JAUS Validation Tool (JVT) and the OCP of the
///   JAUS Interopability Challange during the Autonomous Surface Vehicle
///   Competition, passing all requirements.
///
///   All you have to do is integrate on your own robot, providing real
///   sensor values and generating real control of your bot!
///
////////////////////////////////////////////////////////////////////////////////////
int main(int argc, char* argv[]) {
    Seawolf_loadConfig("../conf/seawolf.conf");
    Seawolf_init("JAUS");

    JAUS::Component component;
 
    component.AccessControlService()->SetTimeoutPeriod(0);
 
    JAUS::LocalPoseSensor* localPoseSensor = new JAUS::LocalPoseSensor();
    localPoseSensor->SetSensorUpdateRate(25);       // Updates at 25 Hz (used for periodic events).
    component.AddService(localPoseSensor);
 
    JAUS::VelocityStateSensor* velocityStateSensor = new JAUS::VelocityStateSensor();
    velocityStateSensor->SetSensorUpdateRate(25);   // Updates at 25 Hz (used for periodic events).
    component.AddService(velocityStateSensor);
 
    component.DiscoveryService()->SetSubsystemIdentification(JAUS::Subsystem::Vehicle, "Seawolf");

    if(component.Initialize(JAUS::Address(gSubsystemID, gNodeID, gComponentID)) == false) {
        std::cout << "Failed to Initialize Component.\n";
        return 0;
    }

    component.ManagementService()->SetStatus(JAUS::Management::Status::Standby);
 
    JAUS::JUDP* transportService = NULL;
    transportService = (JAUS::JUDP*)component.TransportService();

    // Create connection to JAUS Validation Tool (JVT)
    transportService->AddConnection("24.42.140.203", JAUS::Address(90, 1, 1));

    // Create connection to OCP for the JAUS Interoperability Challenge.
    transportService->AddConnection("192.168.1.42", JAUS::Address(42, 1, 1));
 
    // Set an initial global pose.
    JAUS::LocalPose localPose;
    localPose.SetYaw(Var_get("SEA.Yaw"));
    localPose.SetTimeStamp(JAUS::Time::GetUtcTime());
    localPoseSensor->SetLocalPose(localPose);
 
    JAUS::VelocityState velocityState;
    velocityState.SetVelocityX(0.0);
    velocityState.SetYawRate(0.0);
    velocityState.SetTimeStamp(JAUS::Time::GetUtcTime());
    velocityStateSensor->SetVelocityState(velocityState);
 
    JAUS::Time::Stamp printTimeMs = 0;
 
    double yaw, linearDistance, linearVelocity;
 
    while(component.ManagementService()->GetStatus() != JAUS::Management::Status::Shutdown) {
        linearVelocity = (Var_get("PortX") + Var_get("StarX")) / 2;
        yaw = Var_get("SEA.Yaw");
 
        printf("%d\n", localPose.SetYaw(yaw * (3.14 / 180.0)));
        localPose.SetTimeStamp(JAUS::Time(true));
 
        velocityState.SetVelocityX(linearVelocity);
        velocityState.SetYawRate(yaw_dt(yaw));
        velocityState.SetTimeStamp(JAUS::Time(true));

        localPoseSensor->SetLocalPose(localPose);
        velocityStateSensor->SetVelocityState(velocityState);
 
#if 0
        if(JAUS::Time::GetUtcTimeMs() - printTimeMs > 500)
        {
            // Print status of services.
            std::cout << "\n======================================================\n";
            localPoseSensor->PrintStatus(); std::cout << std::endl;
            printTimeMs = JAUS::Time::GetUtcTimeMs();
        }
#endif

        CxUtils::SleepMs(250);
    }
 
    /* Shutdown any components associated with our subsystem */
    component.Shutdown();
    Seawolf_close();
 
    return 0;
}
