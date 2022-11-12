# Ji4ka Coworkimg Space RFID visits tracker, logger and customer receipt printing service.
![USB card reader](https://raw.githubusercontent.com/Irdroid/jrfid/main/hardware/51yL27kO7eL.jpg)

## Motivation:
As prepaid visits packages are offered in our coworking space
we needed a way to track down the user visits as initially it
was very inconvenient for the user to write down their visits
on a paper in a notepad that we have there.

## The solution:
The solution was to use one of the computers in the office to
interface with a cheap chineese USB rfid reader , when the user taps their tag
to the rfid reader their prepaid visits counter gets decremented,
a receipt with the date of the visit and the remaining days  gets
printed on the thermal receipt printer. In addition, the visits
counter are stored locally in a text file, for easier modification of
the available days variables and also not to loose any data if the system is rebooted or the program crash.

The rfid tag ids are hardcoded in the program but they can be easily changed
as if you tap a new rfid tag its id gets printed in the conaole.

by default the utility should run in the background so when starting from
the console/terminal type : nohup ji4ka_rfid.py &
the visit counters are stored in a text file called visits1.txt
