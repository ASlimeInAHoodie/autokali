#!/usr/bin/env bash
chsh -s /usr/bin/zsh # Set default shell

## PURPLE THEME
xfconf-query -c xsettings -p /Net/IconThemeName -s Flat-Remix-Purple-Dark
xfconf-query -c xsettings -p /Net/ThemeName -s Kali-Purple-Dark
xfconf-query -c xfwm4 -p /general/theme -s Kali-Purple-Dark
gsettings set org.xfce.mousepad.preferences.view color-scheme Kali-Purple-Dark