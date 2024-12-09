#!/bin/bash
while true
	  do
	     valor1=$(python3 readinbox.py | grep -E "ON|on|On|oN" | cut -d " " -f3 | cut -b 24-25)
	     valor2=$(python3 readinbox.py | grep -E "OFF|off|Off|oFf|ofF|OFf|oFF|OfF" | cut -d " " -f3 | cut -b 24-26)

	     if [[ $valor1 = "ON" || $valor1 = "on" || $valor1 = "On" || $valor1 = "oN" ]]
				  then
				      echo $valor1
	 			      sudo /./home/cesar/on17.sh
	     else
	         if [[ $valor2 = "OFF" || $valor2 = "off" || $valor2 = "Off" || $valor2 = "oFf" || $valor2 = "ofF" || $valor2 = "OFf" || $valor2 = "oFF" || $valor2 = "OfF" ]]
				       then
				 	   echo $valor2
					   sudo /./home/cesar/off17.sh
				       fi
	     fi
	     sleep 1
	  done
