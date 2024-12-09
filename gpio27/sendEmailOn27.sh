hostname > /home/cesar/informe.txt
date >> /home/cesar/informe.txt
cat /home/cesar/estado27.txt >> informe.txt
uuencode /home/cesar/informe.txt informe.txt > /tmp/out.mail
echo "GPIO27 ON" | mail -s "ENCENDIDO GPIO27" arquicesar230@gmail.com < /tmp/out.mail
