hostname > /home/cesar/informe.txt
date >> /home/cesar/informe.txt
cat /home/cesar/estado22.txt >> informe.txt
uuencode /home/cesar/informe.txt informe.txt > /tmp/out.mail
echo "GPIO22 OFF" | mail -s "APAGADO GPIO22" arquicesar230@gmail.com < /tmp/out.mail
