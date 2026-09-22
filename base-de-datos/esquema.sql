-- =====================================================================
-- Esquema de base de datos — Laboratorio SOC n8n
-- Extraído del pg_dump real de la base `soc_lab` en producción.
-- Contiene únicamente las cinco tablas del sistema SOC (NO las tablas
-- internas de n8n, que n8n crea automáticamente al arrancar).
--
-- Uso: psql -h 127.0.0.1 -U n8n_soc -d soc_lab -f esquema.sql
-- =====================================================================

-- ---------------------------------------------------------------------
-- Tabla: alerts — alertas generadas por las reglas de detección
-- ---------------------------------------------------------------------
CREATE TABLE public.alerts (
    id               integer NOT NULL,
    created_at       timestamp without time zone DEFAULT now(),
    executed_at      timestamp without time zone,
    rule_id          character varying(120) NOT NULL,
    src_ip           character varying(60),
    target_host      character varying(120),
    severity         character varying(20),
    category         character varying(60),
    abuse_score      integer,
    event_count      integer,
    description      text,
    raw_log          text,
    payload          jsonb,
    status           character varying(30) DEFAULT 'pending'::character varying,
    notes            text,
    event_timestamp  timestamp without time zone
);
CREATE SEQUENCE public.alerts_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.alerts_id_seq OWNED BY public.alerts.id;
ALTER TABLE ONLY public.alerts ALTER COLUMN id SET DEFAULT nextval('public.alerts_id_seq'::regclass);
ALTER TABLE ONLY public.alerts ADD CONSTRAINT alerts_pkey PRIMARY KEY (id);

-- ---------------------------------------------------------------------
-- Tabla: playbook_runs — registro de acciones de respuesta ejecutadas
-- ---------------------------------------------------------------------
CREATE TABLE public.playbook_runs (
    id             integer NOT NULL,
    alert_id       integer,
    workflow_name  character varying(120),
    started_at     timestamp without time zone DEFAULT now(),
    executed_at    timestamp without time zone,
    result         character varying(30),
    parameters     jsonb
);
CREATE SEQUENCE public.playbook_runs_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.playbook_runs_id_seq OWNED BY public.playbook_runs.id;
ALTER TABLE ONLY public.playbook_runs ALTER COLUMN id SET DEFAULT nextval('public.playbook_runs_id_seq'::regclass);
ALTER TABLE ONLY public.playbook_runs ADD CONSTRAINT playbook_runs_pkey PRIMARY KEY (id);

-- ---------------------------------------------------------------------
-- Tabla: attack_patterns — seguimiento de reincidencia por IP
-- ---------------------------------------------------------------------
CREATE TABLE public.attack_patterns (
    id                integer NOT NULL,
    pattern_type      character varying(60),
    source_ip         character varying(60),
    first_seen        timestamp without time zone,
    last_seen         timestamp without time zone,
    occurrence_count  integer DEFAULT 1,
    is_blocked        boolean DEFAULT false
);
CREATE SEQUENCE public.attack_patterns_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.attack_patterns_id_seq OWNED BY public.attack_patterns.id;
ALTER TABLE ONLY public.attack_patterns ALTER COLUMN id SET DEFAULT nextval('public.attack_patterns_id_seq'::regclass);
ALTER TABLE ONLY public.attack_patterns ADD CONSTRAINT attack_patterns_pkey PRIMARY KEY (id);
-- Constraint que usan los workflows para el UPSERT de reincidencia (ON CONFLICT):
ALTER TABLE ONLY public.attack_patterns ADD CONSTRAINT uq_source_pattern UNIQUE (source_ip, pattern_type);

-- ---------------------------------------------------------------------
-- Tabla: detection_rules — catálogo de las 6 reglas de detección
-- ---------------------------------------------------------------------
CREATE TABLE public.detection_rules (
    id           integer NOT NULL,
    name         character varying(120) NOT NULL,
    description  text,
    pattern      text,
    severity     character varying(20),
    threshold    integer,
    time_window  integer,
    enabled      boolean DEFAULT true
);
CREATE SEQUENCE public.detection_rules_id_seq AS integer START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER SEQUENCE public.detection_rules_id_seq OWNED BY public.detection_rules.id;
ALTER TABLE ONLY public.detection_rules ALTER COLUMN id SET DEFAULT nextval('public.detection_rules_id_seq'::regclass);
ALTER TABLE ONLY public.detection_rules ADD CONSTRAINT detection_rules_pkey PRIMARY KEY (id);

-- ---------------------------------------------------------------------
-- Tabla: workflow_state — puntero de última corrida por regla
-- ---------------------------------------------------------------------
CREATE TABLE public.workflow_state (
    workflow_name  character varying(50) NOT NULL,
    last_run       timestamp without time zone DEFAULT '2000-01-01 00:00:00'::timestamp without time zone NOT NULL
);
ALTER TABLE ONLY public.workflow_state ADD CONSTRAINT workflow_state_pkey PRIMARY KEY (workflow_name);

-- =====================================================================
-- Datos iniciales
-- =====================================================================
INSERT INTO public.workflow_state (workflow_name, last_run) VALUES
    ('RD-1', '2000-01-01 00:00:00'), ('RD-2', '2000-01-01 00:00:00'),
    ('RD-3', '2000-01-01 00:00:00'), ('RD-4', '2000-01-01 00:00:00'),
    ('RD-5', '2000-01-01 00:00:00'), ('RD-6', '2000-01-01 00:00:00')
ON CONFLICT (workflow_name) DO NOTHING;

INSERT INTO public.detection_rules (name, description, pattern, severity, threshold, time_window, enabled) VALUES
    ('RD-1 - Fuerza Bruta SSH', 'Multiples intentos fallidos de autenticacion SSH', 'Failed password', 'alto', 5, 300, true),
    ('RD-2 - Escaneo de Puertos', 'Conexiones a multiples puertos distintos desde una misma IP', 'PORTSCAN', 'alto', 11, 120, true),
    ('RD-3 - Login como Root', 'Intento de autenticacion directa como root', 'password for root', 'critico', 1, 0, true),
    ('RD-4 - Inyeccion SQL', 'Patrones de inyeccion SQL en peticiones HTTP', 'UNION.*SELECT', 'alto', 3, 120, true),
    ('RD-5 - Directory Traversal', 'Intento de acceso a rutas fuera del directorio web', '../', 'alto', 1, 0, true),
    ('RD-6 - Abuso de Sudo', 'Comandos sudo sensibles', 'COMMAND=', 'medio', 1, 0, true)
ON CONFLICT DO NOTHING;
