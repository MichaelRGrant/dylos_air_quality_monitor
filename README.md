# dylos_air_quality_monitor

This reads the dylos air quality monitor output and saves the data to a csv file. 

This python script is meant to be run at boot on the raspberry pi with the serial output of the dylos air monitor connected to the USB port of the pi. 

### Running a program at boot on pi
First make your script executable by adding `#!/usr/bin/python3` to the top the script. If you are using python 2.7 then `python3 -> python`. 

Edit the `rc.local` file by running the command `sudo vim /etc/rc.local` and add the following code to the end of the `rc.local` file but leaving the `exit 0`

`sudo python <absolute/path/to/script.py> &`

Note: I set an alias in my bash script so that calling python from the console boots up python3. 
**The ampersand (&) is required if the program runs in a loop. It forks the bootup process to allow it to run in that loop while other programs boot.**

