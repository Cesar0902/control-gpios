#!/bin/bash

# Cambiar el estado del GPIO
echo 0 > /home/cesar/estado27.txt

# Configuración de la base de datos
DB_HOST="localhost"
DB_USER="developer"
DB_PASS="Developer"
DB_NAME="arquitectura"
DB_TABLE="proyecto_final"

# Insertar registro en la base de datos
mysql -h "$DB_HOST" \
      -u "$DB_USER" \
      -p"$DB_PASS" \
      -D "$DB_NAME" \
      -e "
       INSERT INTO $DB_TABLE (desc_gpios, estado, fecha) 
       VALUES ('GPIO27', '0', NOW());
       "

echo "GPIO 27 APAGADO"