#!/bin/bash
# Regla de iptables que alimenta la detección de escaneo de puertos (RD-2).
# Registra las conexiones NUEVAS con el prefijo PORTSCAN:, que Syslog-ng
# reenvía al archivo de eventos. Se inserta en la posición 1 (antes de la
# cadena de Fail2ban) para mantener visibilidad incluso sobre IPs ya bloqueadas.
# Ajustar 'enp0s3' al nombre real de la interfaz (verificar con: ip addr).

sudo iptables -I INPUT 1 -i enp0s3 -m conntrack --ctstate NEW \
    -j LOG --log-prefix "PORTSCAN: " --log-level 4

# Persistir la regla para que sobreviva reinicios:
sudo netfilter-persistent save
