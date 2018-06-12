#!/usr/bin/python3
import RPi.GPIO as GPIO
import time
import serial

port = serial.Serial("/dev/ttyS0", baudrate=115200, timeout=3.0)

LED_PIN = 7
BTN_PIN_1 = 12
BTN_PIN_2 = 16
BTN_PIN_3 = 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(LED_PIN,GPIO.OUT)
GPIO.setup(BTN_PIN_1,GPIO.IN)
GPIO.setup(BTN_PIN_2,GPIO.IN)
GPIO.setup(BTN_PIN_3,GPIO.IN)

bed_dict = {12:"B01", 16:"B02", 18:"B03"}
logic_dict = {True:"S1", False:"S0"}

counter = 0

while True:
	btn_state_1 = GPIO.input(BTN_PIN_1)
	btn_state_2 = GPIO.input(BTN_PIN_2)
	btn_state_3 = GPIO.input(BTN_PIN_3)

	msg = bed_dict[BTN_PIN_1] + logic_dict[btn_state_1] + " " + bed_dict[BTN_PIN_2] + logic_dict[btn_state_2] + " " + bed_dict[BTN_PIN_3] + logic_dict[btn_state_3]
#	msg = bed_dict[BTN_PIN_1] + logic_dict[btn_state_1]
	print("Write: " + msg)
	port.write(msg.encode())

	if btn_state_1 == True or btn_state_2 == True or btn_state_3 == True:
		GPIO.output(LED_PIN,True)
		if counter == 5:
			GPIO.output(LED_PIN,False)
		elif counter == 7:
			GPIO.output(LED_PIN,True)
		elif counter == 9:
			GPIO.output(LED_PIN,False)
		elif counter == 10:
			counter = 5
		counter += 1
	else:
		GPIO.output(LED_PIN,False)
		counter = 0

	time.sleep(0.1)

