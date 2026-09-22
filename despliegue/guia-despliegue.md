# Guía de Despliegue — Laboratorio SOC n8n

**Objetivo:** desplegar el stack completo (Syslog-ng, PostgreSQL, n8n, Fail2ban, DVWA) sobre una VM Ubuntu ya instalada, con la red del laboratorio ya configurada. Esta guía asume que las VMs (Ubuntu + Kali), la red interna `soc-lab` y las IPs fijas **ya existen** — el tiempo a cronometrar para H2 es el de este documento, no el de instalar el sistema operativo desde cero.

**Antes de empezar (lo prepara el equipo, no la persona que hace la prueba):**
- Exportar los 6 sub-workflows + el orquestador padre desde n8n (menú `...` → Download) y dejarlos en una carpeta `workflows-export/`
- Snapshot limpio de la VM Ubuntu, con el sistema operativo instalado, red configurada, pero **sin ningún componente del stack instalado todavía**
- Cronómetro visible para la persona que hace la prueba

**Para la persona que hace la prueba:** seguí los pasos en orden, sin saltarte ninguno. Si algo no coincide exactamente con lo que ves en pantalla, anotalo — es información valiosa aunque el intento no llegue a los 30 minutos.

---

## Paso 1 — Instalar dependencias base (≈3 min)

```bash
sudo apt update
sudo apt install -y syslog-ng syslog-ng-core postgresql postgresql-contrib fail2ban docker.io docker-compose-plugin openssh-server iptables-persistent netfilter-persistent
```

Cuando `iptables-persistent` pregunte si guardar las reglas actuales de IPv4/IPv6, aceptá ambas.

## Paso 2 — Verificar zona horaria (≈30 seg)

```bash
timedatectl
```

Debe decir `Time zone: America/Argentina/Buenos_Aires`. Si no, corregir:
```bash
sudo timedatectl set-timezone America/Argentina/Buenos_Aires
```

## Paso 3 — Configurar Syslog-ng (≈2 min)

```bash
sudo mkdir -p /var/log/security
sudo tee /etc/syslog-ng/conf.d/soc-lab.conf > /dev/null << 'EOF'
source s_soclab_net {
    network(transport(tcp) port(514));
    network(transport(udp) port(514));
};

destination d_alerts {
    file("/var/log/security/alerts.log"
        template("${ISODATE} ${HOST} ${PROGRAM} ${MESSAGE}\n")
        perm(0644)
    );
};

log { source(s_soclab_net); source(s_src); destination(d_alerts); };
EOF

sudo systemctl restart syslog-ng
sudo systemctl enable syslog-ng
```

**Nota importante ya incorporada:** la fuente local correcta en esta versión de Ubuntu es `s_src`, no `s_local` (un nombre distinto causa el error "Automatic assignment of persist names failed" u otros errores de arranque).

Prueba de humo:
```bash
logger "prueba de despliegue"
grep "prueba de despliegue" /var/log/security/alerts.log
```

## Paso 4 — Configurar PostgreSQL (≈3 min)

```bash
sudo -u postgres psql << 'EOF'
CREATE USER n8n_soc WITH PASSWORD 'CAMBIAR_ESTA_PASSWORD';
CREATE DATABASE soc_lab OWNER n8n_soc;
EOF

sudo sed -i "s/#listen_addresses = 'localhost'/listen_addresses = '*'/" /etc/postgresql/*/main/postgresql.conf

sudo tee -a /etc/postgresql/*/main/pg_hba.conf > /dev/null << 'EOF'
host    all             all             192.168.100.0/24        scram-sha-256
host    all             all             172.16.0.0/12            scram-sha-256
EOF

sudo systemctl restart postgresql
```

**Nota:** la regla para `172.16.0.0/12` es necesaria porque el contenedor de n8n se conecta desde una IP tipo `172.18.x.x` de la red interna de Docker — sin esa regla, n8n no puede conectarse a Postgres aunque las credenciales sean correctas.

Cargar el esquema (usar el archivo `esquema.sql` del repositorio, o crear las tablas manualmente — ver Anexo B de la tesis para el DDL completo, incluidas las 5 tablas: `alerts`, `attack_patterns`, `detection_rules`, `playbook_runs`, `workflow_state`).

## Paso 5 — Levantar n8n con Docker (≈3 min)

```bash
mkdir -p ~/n8n-soc && cd ~/n8n-soc
tee docker-compose.yml > /dev/null << 'EOF'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:latest
    ports:
      - "5678:5678"
    environment:
      - DB_TYPE=postgresdb
      - DB_POSTGRESDB_HOST=192.168.100.10
      - DB_POSTGRESDB_DATABASE=soc_lab
      - DB_POSTGRESDB_USER=n8n_soc
      - DB_POSTGRESDB_PASSWORD=CAMBIAR_ESTA_PASSWORD
      - N8N_HOST=192.168.100.10
      - N8N_SECURE_COOKIE=false
      - NODES_EXCLUDE=[]
    volumes:
      - n8n_data:/home/node/.n8n
      - /var/log/security:/var/log/security:ro
volumes:
  n8n_data:
EOF

sudo docker compose up -d
```

**Nota:** `NODES_EXCLUDE=[]` es necesario para reactivar el nodo **Execute Command**, que viene deshabilitado por defecto en n8n desde la versión 2.0 por seguridad — sin esto, los sub-workflows que ejecutan `fail2ban-client` van a fallar.

## Paso 6 — Configurar Fail2ban (≈3 min)

```bash
sudo tee /etc/fail2ban/jail.local > /dev/null << 'EOF'
[sshd]
enabled = false

[soc-lab-manual]
enabled = true
backend = polling
filter = soc-lab-manual
logpath = /var/log/security/alerts.log
action = iptables-allports[name=soc-lab-manual]
maxretry = 999999
findtime = 1
bantime = 3600
EOF

sudo tee /etc/fail2ban/filter.d/soc-lab-manual.conf > /dev/null << 'EOF'
[Definition]
failregex = ^.*<HOST>.*$
ignoreregex =
EOF

sudo systemctl restart fail2ban
```

**Nota crítica ya incorporada:** la línea `[sshd] enabled = false` es obligatoria — el jail `sshd` que trae Fail2ban por defecto bloquea automáticamente sin pasar por n8n ni por aprobación humana, contradiciendo el requisito de "aprobación humana obligatoria" del diseño. Sin este paso, un ataque real puede quedar bloqueado por Fail2ban antes de que n8n llegue a procesarlo, invalidando las métricas de MTTA/MTTR.

Confirmar que solo hay un jail activo:
```bash
sudo fail2ban-client status
```

## Paso 7 — Configurar la regla de escaneo de puertos (≈1 min)

```bash
sudo iptables -I INPUT 1 -i enp0s3 -m conntrack --ctstate NEW -j LOG --log-prefix "PORTSCAN: " --log-level 4
sudo netfilter-persistent save
```

**Nota:** la posición 1 (antes que la cadena de Fail2ban) es importante para mantener visibilidad de reincidencias incluso sobre IPs ya bloqueadas. Verificar el nombre de la interfaz de red (`enp0s3` puede variar) con `ip addr`.

## Paso 8 — Levantar DVWA (≈2 min)

```bash
mkdir -p ~/dvwa-logs ~/dvwa-sessions
sudo chown :33 ~/dvwa-sessions && chmod 775 ~/dvwa-sessions

sudo docker run -d --name dvwa -p 80:80 \
  --mount type=bind,source=$HOME/dvwa-logs,target=/var/log/apache2 \
  --mount type=bind,source=$HOME/dvwa-sessions,target=/var/lib/php/sessions \
  vulnerables/web-dvwa
```

Configurar la base de datos de DVWA:
```bash
sleep 10  # esperar a que arranque el contenedor
curl -s http://localhost/setup.php > /dev/null
```
Completar el resto del setup (crear la base y fijar seguridad en "Low") desde el navegador en `http://192.168.100.10/setup.php`, o con el script `curl` documentado en el Anexo técnico.

Integrar los logs de DVWA a Syslog-ng:
```bash
sudo tee /etc/syslog-ng/conf.d/dvwa.conf > /dev/null << 'EOF'
source s_dvwa_access {
    file("/home/ubuntu/dvwa-logs/access.log" follow-freq(1));
};

destination d_alerts_dvwa {
    file("/var/log/security/alerts.log"
        template("${ISODATE} dvwa-web apache-access ${MESSAGE}\n")
        persist-name("d_alerts_dvwa")
        perm(0644)
    );
};

log { source(s_dvwa_access); destination(d_alerts_dvwa); };
EOF
sudo systemctl restart syslog-ng
```

**Nota crítica ya incorporada:** el `persist-name("d_alerts_dvwa")` y el `perm(0644)` explícitos son obligatorios — sin ellos, dos destinos de Syslog-ng escribiendo al mismo archivo generan un conflicto de arranque, o el archivo queda con permisos que el contenedor de n8n no puede leer.

## Paso 9 — Importar los workflows de n8n (≈5 min)

1. Abrir `http://192.168.100.10:5678` y crear el usuario owner
2. Importar los 6 sub-workflows desde `workflows-export/` (menú `...` → Import from File)
3. Importar el workflow padre ("Orquestador Central - SOC Lab")
4. **Publicar cada uno de los 6 sub-workflows primero**, y recién después publicar el padre (el padre no puede activarse si algún sub-workflow que referencia no está publicado)
5. Configurar las credenciales necesarias: Postgres (usuario `n8n_soc`), AbuseIPDB (header `Key`), Discord Bot API

## Paso 10 — Verificación final (≈2 min)

```bash
sudo systemctl status syslog-ng postgresql fail2ban --no-pager
sudo docker ps
sudo fail2ban-client status
```

Prueba end-to-end:
```bash
logger -p auth.warning -t sshd "Failed password for labtest from 192.168.100.20 port 51421 ssh2"
```
Esperar el próximo ciclo del Cron (hasta 5 min) y confirmar que llega una notificación a Discord.

---

## Tiempo estimado total: ~25 minutos (sin contar la espera del Cron del paso 10)

Este es el tiempo objetivo de referencia para el intento de H2. Si el paso 10 (validación end-to-end) se cronometra aparte por depender del Cron, el despliegue en sí (pasos 1-9) debería completarse en unos 22-24 minutos siguiendo esta guía al pie de la letra.

---

## Registro del intento (completar durante la prueba)

- Nombre de quien realiza el intento: ___________
- ¿Experiencia previa con n8n/Syslog-ng/Fail2ban/Docker?: ___________
- Hora de inicio: ___________
- Hora de fin (paso 9 completo, antes de la validación end-to-end): ___________
- Tiempo total: ___________
- Pasos donde hubo que pedir ayuda o hubo confusión: ___________
- ¿Se completó dentro de los 30 minutos?: Sí / No
