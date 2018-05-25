#if (ARDUINO >= 100)
    #include <Arduino.h>
#else
    #include <WProgram.h>
#endif

#include "lino_base_config.h"
#include "Motor.h"
#include "Kinematics.h"
#include "PID.h"

#define ENCODER_OPTIMIZE_INTERRUPTS
#include "Encoder.h"

#define COMMAND_RATE 15 //hz

Encoder motor1_encoder(MOTOR1_ENCODER_A, MOTOR1_ENCODER_B);
Encoder motor2_encoder(MOTOR2_ENCODER_A, MOTOR2_ENCODER_B); 
Encoder motor3_encoder(MOTOR3_ENCODER_A, MOTOR3_ENCODER_B); 
Encoder motor4_encoder(MOTOR4_ENCODER_A, MOTOR4_ENCODER_B); 

Motor motor1(Motor::MOTOR_DRIVER, COUNTS_PER_REV, MOTOR1_PWM, MOTOR1_IN_A, MOTOR1_IN_B);
Motor motor2(Motor::MOTOR_DRIVER, COUNTS_PER_REV, MOTOR2_PWM, MOTOR2_IN_A, MOTOR2_IN_B); 
Motor motor3(Motor::MOTOR_DRIVER, COUNTS_PER_REV, MOTOR3_PWM, MOTOR3_IN_A, MOTOR3_IN_B);
Motor motor4(Motor::MOTOR_DRIVER, COUNTS_PER_REV, MOTOR4_PWM, MOTOR4_IN_A, MOTOR4_IN_B);

PID motor1_pid(PWM_MIN, PWM_MAX, K_P, K_I, K_D);
PID motor2_pid(PWM_MIN, PWM_MAX, K_P, K_I, K_D);
PID motor3_pid(PWM_MIN, PWM_MAX, K_P, K_I, K_D);
PID motor4_pid(PWM_MIN, PWM_MAX, K_P, K_I, K_D);

Kinematics kinematics(Kinematics::LINO_BASE, MAX_RPM, WHEEL_DIAMETER, FR_WHEELS_DISTANCE, LR_WHEELS_DISTANCE, PWM_BITS);

float g_req_linear_vel_x = 0;
float g_req_linear_vel_y = 0;
float g_req_angular_vel_z = 0;

unsigned long g_prev_command_time = 0;

/* ----- MAIN ----- */
void setup()
{
    delay(1);
}

/* ----- LOOP ----- */
void loop()
{
    static unsigned long prev_control_time = 0;

    //this block drives the robot based on defined rate
    if ((millis() - prev_control_time) >= (1000 / COMMAND_RATE))
    {
        moveBase();
        prev_control_time = millis();
    }

    //this block stops the motor when no command is received
    if ((millis() - g_prev_command_time) >= 400)
    {
        stopBase();
    }

    //parse here - cmd_msg.linear is the message
    g_req_angular_vel_z = 0;

    g_prev_command_time = millis();
}

void moveBase()
{
    Kinematics::rpm req_rpm;

    //get the required rpm for each motor based on required velocities, and base used
    req_rpm = kinematics.getRPM(g_req_linear_vel_x, g_req_linear_vel_y, g_req_angular_vel_z);

    //the required rpm is capped at -/+ MAX_RPM to prevent the PID from having too much error
    //the PWM value sent to the motor driver is the calculated PID based on required RPM vs measured RPM
    motor1.spin(motor1_pid.compute(req_rpm.motor1, motor1.getRPM()));
    motor2.spin(motor2_pid.compute(req_rpm.motor2, motor2.getRPM()));
    motor3.spin(motor3_pid.compute(req_rpm.motor3, motor3.getRPM()));  
    motor4.spin(motor4_pid.compute(req_rpm.motor4, motor4.getRPM()));    
}

void stopBase()
{
    g_req_linear_vel_x = 0;
    g_req_linear_vel_y = 0;
    g_req_angular_vel_z = 0;
}
