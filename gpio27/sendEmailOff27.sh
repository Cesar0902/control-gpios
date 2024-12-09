hostname > /home/cesar/informe.txt
date >> /home/cesar/informe.txt
cat /home/cesar/estado27.txt >> informe.txt
uuencode /home/cesar/informe.txt informe.txt > /tmp/out.mail
echo "GPIO27 OFF" | mail -s "APAGADO GPIO27" arquicesar230@gmail.com < /tmp/out.mail
