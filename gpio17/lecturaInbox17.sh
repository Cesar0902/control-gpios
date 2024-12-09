#!/bin/bash
last_processed=""

while true
do
    # Leer el correo solo una vez
    correo=$(python3 readinbox.py)

    # Filtrar "ON" y "OFF" del correo
    valor1=$(echo "$correo" | grep -E "ON|on|On|oN" | cut -d " " -f3 | cut -b 24-25)
    valor2=$(echo "$correo" | grep -E "OFF|off|Off|oFf|ofF|OFf|oFF|OfF" | cut -d " " -f3 | cut -b 24-26)

    # Si el valor del correo es "ON" y no ha sido procesado antes
    if [[ -n "$valor1" && ( "$valor1" == "ON" || "$valor1" == "on" || "$valor1" == "On" || "$valor1" == "oN" ) && "$correo" != "$last_processed" ]]
    then
        echo "Encendiendo GPIO17"
        sudo /./home/cesar/on17.sh
        last_processed="$correo"  # Marcar correo como procesado
    elif [[ -n "$valor2" && ( "$valor2" == "OFF" || "$valor2" == "off" || "$valor2" == "Off" || "$valor2" == "oFf" || "$valor2" == "ofF" || "$valor2" == "OFf" || "$valor2" == "oFF" || "$valor2" == "OfF" ) && "$correo" != "$last_processed" ]]
    then
        echo "Apagando GPIO17"
        sudo /./home/cesar/off17.sh
        last_processed="$correo"  # Marcar correo como procesado
    fi
    
    sleep 1
done