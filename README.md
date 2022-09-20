# Final Year Project Raspberry Pi Script
python version 3.9.2

## Raspberry pi zero w
```ssh
user = pi
pass = password0
```


## Connect to Wifi
Add wpa_supplicant.conf file to the boot directory.

### To configure wifi connection from raspberry pi
```sudo nano /etc/wpa_supplicant/wpa_supplicant.conf``` 

wpa_supplicant.conf
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1

network={
 ssid="Xiaomi"
 psk="ikbr2932"
 id_str="home"
}

network={
 ssid="ikbal.webx"
 psk="12345678"
 id_str="laptop"
}

network={
 ssid="CSE LAB 1"
 psk="12345678"
 id_str="laptop"
}
```