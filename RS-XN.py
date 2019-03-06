#Rocksat Norway Payload Code for January 2019 Flight
#UPRRP Team
#Coded by: John G. Wilson Negroni
#jgwilson1997@gmail.com
#---------------------------------------------

#Imports
import serial
import time
import RPi.GPIO as GPIO
import subprocess

#Serial Setup

serialOUT = serial.Serial(port = '/dev/ttyAMA0', baudrate = 230400, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

#Board Pin Mode Setup

GPIO.setmode(GPIO.BCM)

#Variable Definitions
#Components
Proximity_Sensor = 5

#Flags
Launch = 22
Skirt = 23

#Misc
time_to_launch = 30 #225 full sequence(-16 is the marging between actual time and boot up) IE 240 is 225

Count = 0
check = 1

#IO Setup
#Flags
GPIO.setup(Launch, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(Skirt, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Proximity Sensor
GPIO.setup(Proximity_Sensor, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

#Function Definitions
#Flag Check

def FlagCheck(flag):

        InputToCheck = 1
        Count = 0

        if (flag == Launch):
                InputToCheck = 1
        if (flag == Skirt):
                InputToCheck = 1
        if (flag == Proximity_Sensor):
                InputToCheck = 0
		for x in range(0,13):
				if(GPIO.input(flag) == InputToCheck):
						Count += 1
		if (Count > 10):
				return 1     
		else:
				return 0
				
def GetFlagValue():

		Data_Launch = str(FlagCheck(Launch))
		Data_Skirt = str(FlagCheck(Skirt))
		Data_Proximity = str(FlagCheck(Proximity_Sensor))
		
		FlagStatusBit = (Data_Launch + Data_Skirt + Data_Proximity)
		
		return FlagStatusBit
		
def GetSpectroData():

		value = subprocess.Popen('php /home/pi/dek-kit/php/getspectrum.php', shell=True, stdout=subprocess.PIPE)
		
		Data_Spectro = value.stdout.read()
		
		return Data_Spectro
		
def GetLineData():
	
		data = GetSpectroData()
		data2 = GetFlagValue()
		
		final_string = (data + data2)
	
		return final_string
		


#--------------------------------------------------------------------------
#Begin Program
#Starting Print

serialOUT.write('Software RockSat Norway 2019 Revision 7/20/18 \n'.encode())
serialOUT.write('This software is for January Flight \n'.encode())
serialOUT.write('UPR Payload Alive T(sec)= '.encode())
GetTime()

while (1):
		serialOUT.write(GetLineData().encode())
	
#Sequence End
#Payload keeps running until it dies
