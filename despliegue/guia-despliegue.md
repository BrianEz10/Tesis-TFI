# Guía de Despliegue — Laboratorio SOC n8n

> **Versión de referencia:** esta guía se publicó por primera vez en el commit `209ffb9` del repositorio (22/09/2026) y se revisó y amplió con posterioridad; el tag `v1.4-defensa` incluye esta versión revisada. El intento de despliegue de H2 reportado en la tesis (§13.6) se realizó el **19 de septiembre de 2026** sobre una versión local previa de esta guía, anterior a su primera publicación y no conservada, por lo que su contenido no coincide línea por línea con el de esta versión.

**Objetivo:** desplegar el stack completo (Syslog-ng, PostgreSQL, n8n, Fail2ban, DVWA) sobre una VM Ubuntu ya instalada, con la red del laboratorio ya configurada. Esta guía asume que las VMs (Ubuntu + Kali), la red interna `soc-lab` y las IPs fijas **ya existen** — el tiempo a cronometrar para H2 es el de este documento, no el de instalar el sistema operativo desde cero.

**Versiones del stack (fijadas para reproducibilidad):** Ubuntu 24.04.4 LTS · PostgreSQL 16 · **n8n 2.29.9** (imagen pinneada, no `latest`) · Fail2ban 1.0.2 · Docker 29.x · Syslog-ng 4.x.

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

**Fijar la zona horaria de PostgreSQL en UTC (obligatorio para reproducir las métricas).** El esquema almacena los timestamps con tipo `TIMESTAMP` (sin zona horaria), de modo que `NOW()` debe registrar en UTC de forma consistente (ver §13.7). Aunque el sistema operativo use `America/Argentina/Buenos_Aires`, PostgreSQL debe operar en UTC:
```bash
sudo -u postgres psql -c "ALTER SYSTEM SET timezone = 'UTC';"
sudo -u postgres psql -c "ALTER DATABASE soc_lab SET timezone = 'UTC';"
sudo systemctl restart postgresql
# verificar:
sudo -u postgres psql -d soc_lab -c "SHOW timezone;"   # debe devolver UTC
```

**Nota:** la regla para `172.16.0.0/12` es necesaria porque el contenedor de n8n se conecta desde una IP tipo `172.18.x.x` de la red interna de Docker — sin esa regla, n8n no puede conectarse a Postgres aunque las credenciales sean correctas.

Cargar el esquema (usar el archivo `esquema.sql` del repositorio, o crear las tablas manualmente — ver Anexo B de la tesis para el DDL completo, incluidas las 5 tablas: `alerts`, `attack_patterns`, `detection_rules`, `playbook_runs`, `workflow_state`).

## Paso 5 — Levantar n8n con Docker (≈3 min)

```bash
mkdir -p ~/n8n-soc && cd ~/n8n-soc
tee docker-compose.yml > /dev/null << 'EOF'
services:
  n8n:
    image: docker.n8n.io/n8nio/n8n:2.29.9
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
      - GENERIC_TIMEZONE=UTC
      - EXECUTIONS_DATA_PRUNE=false
    volumes:
      - n8n_data:/home/node/.n8n
      - /var/log/security:/var/log/security:ro
volumes:
  n8n_data:
EOF

sudo docker compose up -d
```

**Nota:** `NODES_EXCLUDE=[]` es necesario para reactivar el nodo **Execute Command**, que viene deshabilitado por defecto en n8n desde la versión 2.0 por seguridad — sin esto, los sub-workflows que ejecutan `fail2ban-client` van a fallar.

**Nota sobre la imagen y la retención:** se fija `n8n:2.29.9` (no `latest`) para que la versión del motor sea reproducible. `EXECUTIONS_DATA_PRUNE=false` desactiva la poda automática de ejecuciones; de lo contrario, los registros internos de ejecución de n8n (tablas `execution_entity`/`execution_data`) se purgan y no pueden aportarse como evidencia posterior (ver §13.7 y la nota de evidencia del repositorio). `GENERIC_TIMEZONE=UTC` alinea la zona horaria del motor con la de PostgreSQL.

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

## Paso 6b — Permisos de actuación por SSH (clave + sudoers) (≈2 min)

Los sub-workflows ejecutan la contención conectándose por SSH a la propia VM y corriendo `fail2ban-client` e `iptables` con `sudo`. Para que eso funcione sin pedir contraseña, hay que (1) habilitar una clave SSH para n8n y (2) autorizar esos dos comandos por sudo sin contraseña.

**1. Clave SSH para n8n:**
```bash
# generar un par de claves dedicado para n8n (sin passphrase)
ssh-keygen -t ed25519 -f ~/n8n_soc_key -N ""
# autorizar la clave pública para el usuario que ejecutará la contención (ej. ubuntu)
cat ~/n8n_soc_key.pub >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
```
La clave privada `~/n8n_soc_key` se cargará como credencial "SSH Private Key account" en n8n (Paso 9).

**2. sudoers sin contraseña para los comandos de contención:**
```bash
sudo tee /etc/sudoers.d/n8n-soc > /dev/null << 'EOF'
ubuntu ALL=(root) NOPASSWD: /usr/bin/fail2ban-client, /usr/sbin/iptables
EOF
sudo chmod 440 /etc/sudoers.d/n8n-soc
sudo visudo -c   # verificar que la sintaxis es válida
```
(Reemplazar `ubuntu` por el usuario real si es otro. Verificar las rutas con `which fail2ban-client` y `which iptables`.)

**Nota:** sin la regla de sudoers, los nodos "Ban IP"/"Execute a command" fallan con un prompt de contraseña que n8n no puede responder, y el bloqueo nunca se ejecuta.

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
Completar el resto del setup (crear la base y fijar seguridad en "Low") desde el navegador en `http://192.168.100.10/setup.php` (o, de forma equivalente, reproduciendo el envío del formulario «Create / Reset Database» de esa misma página con `curl`, pasando el `user_token` que devuelve el `GET` previo).

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
4. **Configurar las credenciales** (los JSON publicados traen los IDs como marcadores `TU_CREDENCIAL_*_AQUI`, hay que crear cada credencial y asignarla en los nodos correspondientes):
   - **Postgres** (usuario `n8n_soc`, base `soc_lab`, host `192.168.100.10`) — en todos los nodos Postgres de los 7 workflows.
   - **AbuseIPDB** (Header Auth, cabecera `Key`) — nodo de enriquecimiento.
   - **Discord Bot API** — nodos de notificación/aprobación; además, reemplazar los marcadores `TU_GUILD_ID_AQUI` y `TU_CHANNEL_ID_AQUI` por el servidor y canal reales.
   - **SSH Private Key account** — cargar la clave privada `~/n8n_soc_key` generada en el Paso 6b; es la que usan los nodos "Ban IP"/"Execute a command".
5. **Reasignar los sub-workflows en el orquestador padre.** El padre publicado referencia a cada hijo por su ID interno de workflow, propio de la instancia de los autores, que no existe en un despliegue nuevo. En cada nodo "Execute Sub-workflow" del padre hay que seleccionar manualmente el sub-workflow RD-1 a RD-6 correspondiente ya importado en esta instancia; al guardar, el ID original queda reemplazado por el de la nueva instancia.
6. **Publicar cada uno de los 6 sub-workflows primero**, y recién después publicar el padre (el padre no puede activarse si algún sub-workflow que referencia no está publicado).

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

## Tiempo estimado total: ~28 minutos (sin contar la espera del Cron del paso 10)

Este es el tiempo objetivo de referencia para el intento de H2. Si el paso 10 (validación end-to-end) se cronometra aparte por depender del Cron, el despliegue en sí (pasos 1-9) debería completarse en unos 25-28 minutos siguiendo esta guía al pie de la letra. El intento real de H2 (19/09/2026) superó el umbral de 30 minutos, lo que la tesis reporta como evidencia preliminar de que la documentación permite el despliegue autónomo pero aún requiere mejoras (§13.6, §15.2).

---

## Registro del intento (completar durante la prueba)

- Nombre de quien realiza el intento: ___________
- ¿Experiencia previa con n8n/Syslog-ng/Fail2ban/Docker?: ___________
- Hora de inicio: ___________
- Hora de fin (paso 9 completo, antes de la validación end-to-end): ___________
- Tiempo total: ___________
- Pasos donde hubo que pedir ayuda o hubo confusión: ___________
- ¿Se completó dentro de los 30 minutos?: Sí / No
