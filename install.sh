sudo apt-get install python-pygame
sudo apt-get install xbacklight
mkdir ~/.autobrightness
cp autobrightness.py ~/.autobrightness
echo "
[Desktop Entry]
Type=Application
Exec=/home/$USER/.autobrightness/autobrightness.py
Hidden=false
NoDisplay=false
X-GNOME-Autostart-enabled=true
Name[en_US]=Auto Brightness
Name=Auto Brightness
Comment[en_US]=
Comment=
" >> autobrightness.py.desktop
mv autobrightness.py.desktop ~/.config/autostart
