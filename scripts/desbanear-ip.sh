#!/bin/bash
IP="$1"
if [ -z "$IP" ]; then
  echo "Uso: $0 <ip>"
  exit 1
fi

echo "Desbaneando $IP en Fail2ban..."
sudo fail2ban-client set soc-lab-manual unbanip "$IP"

echo "Limpiando reglas residuales en f2b-soc-lab-manual (INPUT, para SSH/puertos)..."
COUNT1=0
while sudo iptables -C f2b-soc-lab-manual -s "$IP" -j REJECT --reject-with icmp-port-unreachable 2>/dev/null; do
  sudo iptables -D f2b-soc-lab-manual -s "$IP" -j REJECT --reject-with icmp-port-unreachable
  COUNT1=$((COUNT1+1))
done
echo "Reglas residuales eliminadas en f2b-soc-lab-manual: $COUNT1"

echo "Limpiando reglas residuales en DOCKER-USER (para tráfico hacia contenedores)..."
COUNT2=0
while sudo iptables -C DOCKER-USER -s "$IP" -j REJECT --reject-with icmp-port-unreachable 2>/dev/null; do
  sudo iptables -D DOCKER-USER -s "$IP" -j REJECT --reject-with icmp-port-unreachable
  COUNT2=$((COUNT2+1))
done
echo "Reglas residuales eliminadas en DOCKER-USER: $COUNT2"

echo "Estado final:"
sudo iptables -L f2b-soc-lab-manual -n -v --line-numbers
sudo iptables -L DOCKER-USER -n -v --line-numbers