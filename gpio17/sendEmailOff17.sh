hostname > /home/cesar/informe.txt
date >> /home/cesar/informe.txt
cat /home/cesar/estado17.txt >> informe.txt
uuencode /home/cesar/informe.txt informe.txt > /tmp/out.mail
echo "GPIO17 OFF" | mail -s "APAGADO GPIO17" arquicesar230@gmail.com < /tmp/out.mail
