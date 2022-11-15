#!/usr/bin/env python
#
# Ji4ka COWORKING space RFID visits tracker, logger
# and customer receipt printing service.
#
# This project uses cheap chineese usb rfid reader adapters
# that enumerate on the host system as a standard HID  input
# devices. When you scan an rfid tag the  rfid tag id and also
# some other information can be access via the device sysfs entry
#
# Motivation:
# as prepaid visits packages are offered in our coworking space
# we needed a way to track down the user visits as initially it
# was very inconvenient for the user to write down their visits 
# on a paper in a notepad that we have there.
# 
# The solution:
# The solution was to use one of the computers in the office to
# interface with the USB rfid reader , when the user taps their tag
# to the rfid reader their prepaid visits counter gets decremented, 
# a receipt with the date of the visit and the remaining days  gets 
# printed on the thermal receipt printer. In addition, the visits 
# counter are stored locally in a text file, for easier modification of
# the available days variables
#
# The rfid tags are hardcoded in the program but they can be easily changed
# as if you tap a new rfid tag its id gets printed in the conaole.
#
# by default the utility should run in the background so when starting from
# the console/terminal type : nohup ji4ka_rfid.py &
# the visit counters are stored in a text file called visits1.txt
#
# when youu plug your USB rfid reader ypu need to identify its file name
# and change it axcordimgly see "dev" below

from evdev import InputDevice, ecodes, list_devices 
from datetime import date
from select import select 
import subprocess
import os
today = date.today()
d1 = today.strftime("%d/%m/%Y")
print("***********\nVisit " \
                +str(d1))
# Open the file  with the visits counter
file = open("visits1.txt", "r")
# Declare visits list
visits = []
# Read the visits counter list from a text file
for line in file.readlines():
    fields = line.split(',')
    visits.append(int(fields[0]))
    visits.append(int(fields[1]))
    visits.append(int(fields[2]))
file.close()

keys = "X^1234567890XXXXqwertzuiopXXXXasdfghjklXXXXXyxcvbnmXXXXXXXXXXXXXXXXXXXXXXX" 
dev = InputDevice("/dev/input/by-id/usb-Sycreader_RFID_Technology_Co.__Ltd_SYC_ID_IC_USB_Reader_08FF20140315-event-kbd") 
barcode = "" 

while True:
    r,w,x = select([dev], [], [])

    for event in dev.read():

        if event.type != 1 or event.value != 1:
            continue
        if event.code == 28:
            if barcode == "0003317244":
                file = open("visits1.txt", "w")
                print(barcode)
                barcode = ""
                today = date.today()
                d1 = today.strftime("%d/%m/%Y")
                header = "*Ji4ka Coworking*\n  visits logger  \n\n"
                message = "*****************\nVisit " \
                + str(d1) + "\nRemaining: " + str(visits[1])
                
                lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
                lpr.stdin.write(header+message)
                lpr.stdin.close()
                visits[0] = visits[0] - 1
                for i in range(len(visits)):
                    file.write(str(visits[i])+", ")
                file.close()
            break
            if barcode == "1003317244":
                file = open("visits1.txt", "w")
                print(barcode)
                barcode = ""
                today = date.today()
                d1 = today.strftime("%d/%m/%Y")
                header = "Ji4ka Coworking\nvisits logger\n"
                message = "****************\nVisit " \
                + str(d1) + "\nRemaining: " + str(visits[1])

                lpr =  subprocess.Popen("/usr/bin/lpr", stdin=subprocess.PIPE)
                lpr.stdin.write(header+message)
                lpr.stdin.close()
                visits[1] = visits[1] - 1
                for i in range(len(visits)):
                    file.write(str(visits[i])+", ")
                file.close()
            break           
        barcode += keys[event.code]
