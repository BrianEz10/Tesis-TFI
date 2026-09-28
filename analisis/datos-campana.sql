--
-- PostgreSQL database dump
--

\restrict AEw8vsrQvRP3TRlEmHTDggmxd7khDTBn63QCrm6v1EToCBJLjM3LhePyC0i8EM2

-- Dumped from database version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)
-- Dumped by pg_dump version 16.15 (Ubuntu 16.15-0ubuntu0.24.04.1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Data for Name: alerts; Type: TABLE DATA; Schema: public; Owner: n8n_soc
--

COPY public.alerts (id, created_at, executed_at, rule_id, src_ip, target_host, severity, category, abuse_score, event_count, description, raw_log, payload, status, notes, event_timestamp) FROM stdin;
1	2026-07-17 01:46:11.731739	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-07-17 01:45:51
2	2026-08-17 22:05:44.524719	\N	RD-1	192.168.100.20	\N	alto	fuerza_bruta_ssh	0	25	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-17 22:03:58
3	2026-08-17 22:25:44.718915	\N	RD-1	192.168.100.20	\N	alto	fuerza_bruta_ssh	0	25	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-17 22:22:38
4	2026-08-17 22:30:44.423591	\N	RD-1	192.168.100.20	\N	alto	fuerza_bruta_ssh	0	25	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-17 22:28:01
5	2026-08-24 21:40:44.648512	\N	RD-1	192.168.100.20	\N	alto	fuerza_bruta_ssh	0	6	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:36:37
6	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.21	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:30
7	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.22	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:30
8	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.23	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:30
9	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.24	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:30
10	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.25	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:31
11	2026-08-24 21:55:44.587225	\N	RD-1	192.168.100.26	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 21:54:31
12	2026-08-24 22:20:44.692763	\N	RD-1	192.168.100.27	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-24 22:16:31
13	2026-08-25 14:30:44.725793	\N	RD-1	192.168.100.101	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:28:36
14	2026-08-25 14:35:44.537646	\N	RD-1	192.168.100.102	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:31:08
15	2026-08-25 14:40:44.570359	\N	RD-1	192.168.100.103	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:35:59
16	2026-08-25 14:45:44.555797	\N	RD-1	192.168.100.104	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:41:09
17	2026-08-25 14:50:44.607525	\N	RD-1	192.168.100.105	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:46:05
18	2026-08-25 14:55:44.57321	\N	RD-1	192.168.100.106	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:51:12
19	2026-08-25 15:00:44.837733	\N	RD-1	192.168.100.107	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 14:56:47
20	2026-08-25 15:05:44.703065	\N	RD-1	192.168.100.108	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 15:01:06
21	2026-08-25 15:10:44.638005	\N	RD-1	192.168.100.109	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 15:06:03
22	2026-08-25 15:15:44.567204	\N	RD-1	192.168.100.110	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-08-25 15:11:06
23	2026-08-25 22:16:39.886532	\N	RD-2	192.168.100.201	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:08:27
24	2026-08-25 22:25:44.92387	\N	RD-2	192.168.100.201	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:08:27
25	2026-08-25 22:30:44.937008	\N	RD-2	192.168.100.211	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:28:10
26	2026-08-25 22:45:45.53554	\N	RD-2	192.168.100.212	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:40:49
27	2026-08-25 22:50:45.129561	\N	RD-2	192.168.100.213	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:46:47
28	2026-08-25 22:55:45.083532	\N	RD-2	192.168.100.214	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:51:16
29	2026-08-25 23:00:44.865153	\N	RD-2	192.168.100.215	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 22:56:01
30	2026-08-25 23:05:45.024857	\N	RD-2	192.168.100.216	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 23:01:13
31	2026-08-25 23:10:44.935335	\N	RD-2	192.168.100.217	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 23:06:04
32	2026-08-25 23:15:44.928154	\N	RD-2	192.168.100.218	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 23:11:08
33	2026-08-25 23:20:44.874684	\N	RD-2	192.168.100.219	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 23:16:11
34	2026-08-25 23:25:44.961494	\N	RD-2	192.168.100.220	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-08-25 23:21:03
35	2026-08-26 20:20:45.366522	\N	RD-3	192.168.100.41	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.41", "accepted": false, "last_seen": "2026-08-26T20:18:16.000Z", "first_seen": "2026-08-26T20:18:16.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:18:16
36	2026-08-26 20:25:45.436934	\N	RD-3	192.168.100.42	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.42", "accepted": false, "last_seen": "2026-08-26T20:21:45.000Z", "first_seen": "2026-08-26T20:21:45.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:21:45
37	2026-08-26 20:30:45.537592	\N	RD-3	192.168.100.43	\N	crítico	root_login	0	2	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.43", "accepted": false, "last_seen": "2026-08-26T20:26:00.000Z", "first_seen": "2026-08-26T20:25:54.000Z", "ports_used": ["51422", "51422"], "failed_attempts": 2}	pending	\N	2026-08-26 20:25:54
38	2026-08-26 20:35:45.48447	\N	RD-3	192.168.100.44	\N	crítico	root_login	0	2	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.44", "accepted": false, "last_seen": "2026-08-26T20:31:11.000Z", "first_seen": "2026-08-26T20:31:05.000Z", "ports_used": ["51422", "51422"], "failed_attempts": 2}	pending	\N	2026-08-26 20:31:05
39	2026-08-26 20:35:45.48447	\N	RD-3	192.168.100.45	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.45", "accepted": false, "last_seen": "2026-08-26T20:31:45.000Z", "first_seen": "2026-08-26T20:31:45.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:31:45
40	2026-08-26 20:40:45.647094	\N	RD-3	192.168.100.44	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.44", "accepted": false, "last_seen": "2026-08-26T20:36:26.000Z", "first_seen": "2026-08-26T20:36:26.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:36:26
41	2026-08-26 20:40:45.647094	\N	RD-3	192.168.100.46	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.46", "accepted": false, "last_seen": "2026-08-26T20:36:36.000Z", "first_seen": "2026-08-26T20:36:36.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:36:36
42	2026-08-26 20:45:45.792152	\N	RD-3	192.168.100.46	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.46", "accepted": false, "last_seen": "2026-08-26T20:41:20.000Z", "first_seen": "2026-08-26T20:41:20.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:41:20
43	2026-08-26 20:50:45.260063	\N	RD-3	192.168.100.47	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.47", "accepted": false, "last_seen": "2026-08-26T20:46:02.000Z", "first_seen": "2026-08-26T20:46:02.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:46:02
44	2026-08-26 20:55:45.394938	\N	RD-3	192.168.100.48	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.48", "accepted": false, "last_seen": "2026-08-26T20:51:16.000Z", "first_seen": "2026-08-26T20:51:16.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:51:16
45	2026-08-26 21:00:45.383586	\N	RD-3	192.168.100.49	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.49", "accepted": false, "last_seen": "2026-08-26T20:56:12.000Z", "first_seen": "2026-08-26T20:56:12.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 20:56:12
46	2026-08-26 21:05:45.333355	\N	RD-3	192.168.100.50	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.50", "accepted": false, "last_seen": "2026-08-26T21:01:04.000Z", "first_seen": "2026-08-26T21:01:04.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 21:01:04
47	2026-08-26 21:10:45.399078	\N	RD-3	192.168.100.45	\N	crítico	root_login	0	1	Intentos de login root fallidos	\N	{"src_ip": "192.168.100.45", "accepted": false, "last_seen": "2026-08-26T21:09:39.000Z", "first_seen": "2026-08-26T21:09:39.000Z", "ports_used": ["51422"], "failed_attempts": 1}	pending	\N	2026-08-26 21:09:39
48	2026-08-29 20:55:46.004109	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T17:55:27-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:20:55:26 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5500 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T17:55:27-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:20:55:26 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4949 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T17:55:27-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:20:55:26 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15269 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 17:55:27
49	2026-08-29 21:25:46.031419	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:20:53-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:20:53 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5500 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:20:53-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:20:53 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4949 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:20:53-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:20:53 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15269 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:20:53
50	2026-08-29 21:30:45.947121	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:27:19-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:27:19 +0000] \\"GET /vulnerabilities/sqli/?id=2%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5501 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:27:19-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:27:19 +0000] \\"GET /vulnerabilities/sqli/?id=2%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4950 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:27:19-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:27:19 +0000] \\"GET /vulnerabilities/sqli/?id=2%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15270 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:27:19
51	2026-08-29 21:35:45.986064	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:31:34-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:31:34 +0000] \\"GET /vulnerabilities/sqli/?id=3%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5496 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:31:34-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:31:34 +0000] \\"GET /vulnerabilities/sqli/?id=3%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4945 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:31:34-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:31:34 +0000] \\"GET /vulnerabilities/sqli/?id=3%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15265 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:31:34
52	2026-08-29 21:40:45.915723	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:37:16-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:37:15 +0000] \\"GET /vulnerabilities/sqli/?id=4%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5502 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:37:16-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:37:15 +0000] \\"GET /vulnerabilities/sqli/?id=4%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4951 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:37:16-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:37:15 +0000] \\"GET /vulnerabilities/sqli/?id=4%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15271 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:37:16
53	2026-08-29 21:45:46.085455	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:42:00-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:41:59 +0000] \\"GET /vulnerabilities/sqli/?id=5%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5498 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:42:00-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:41:59 +0000] \\"GET /vulnerabilities/sqli/?id=5%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4947 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:42:00-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:41:59 +0000] \\"GET /vulnerabilities/sqli/?id=5%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15267 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:42:00
54	2026-08-29 21:50:45.906147	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:46:49-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:46:49 +0000] \\"GET /vulnerabilities/sqli/?id=6%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5398 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:46:49-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:46:49 +0000] \\"GET /vulnerabilities/sqli/?id=6%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4857 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:46:49-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:46:49 +0000] \\"GET /vulnerabilities/sqli/?id=6%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15145 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:46:49
55	2026-08-29 21:55:46.361277	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:51:59-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:51:58 +0000] \\"GET /vulnerabilities/sqli/?id=7%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5398 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:51:59-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:51:58 +0000] \\"GET /vulnerabilities/sqli/?id=7%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4857 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:51:59-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:51:58 +0000] \\"GET /vulnerabilities/sqli/?id=7%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15145 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:51:59
56	2026-08-29 22:00:46.063316	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T18:56:54-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:56:53 +0000] \\"GET /vulnerabilities/sqli/?id=8%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5398 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:56:54-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:56:53 +0000] \\"GET /vulnerabilities/sqli/?id=8%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4857 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T18:56:54-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:21:56:53 +0000] \\"GET /vulnerabilities/sqli/?id=8%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15145 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 21:56:54
57	2026-08-29 22:05:46.098277	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T19:02:21-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:02:21 +0000] \\"GET /vulnerabilities/sqli/?id=9%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5398 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T19:02:21-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:02:21 +0000] \\"GET /vulnerabilities/sqli/?id=9%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4857 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T19:02:21-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:02:21 +0000] \\"GET /vulnerabilities/sqli/?id=9%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15145 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 22:02:21
58	2026-08-29 22:10:45.945687	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-08-29T19:07:03-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:07:02 +0000] \\"GET /vulnerabilities/sqli/?id=10%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5403 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T19:07:03-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:07:02 +0000] \\"GET /vulnerabilities/sqli/?id=10%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4858 \\"-\\" \\"curl/8.20.0\\"", "2026-08-29T19:07:03-03:00 dvwa-web apache-access 192.168.100.20 - - [29/Aug/2026:22:07:02 +0000] \\"GET /vulnerabilities/sqli/?id=10%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15225 \\"-\\" \\"curl/8.20.0\\""]	pending	\N	2026-08-29 22:07:03
59	2026-08-31 16:00:46.450116	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-08-31 15:59:00
60	2026-08-31 16:05:46.471744	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/hostname"]	pending	\N	2026-08-31 16:02:22
61	2026-08-31 16:10:46.541502	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-08-31 16:06:16
62	2026-08-31 16:15:46.428822	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/hostname"]	pending	\N	2026-08-31 16:11:15
63	2026-08-31 16:20:46.462213	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-08-31 16:16:08
64	2026-08-31 16:25:46.427669	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/hostname"]	pending	\N	2026-08-31 16:21:10
65	2026-08-31 16:30:46.778731	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-08-31 16:26:19
66	2026-08-31 16:35:46.512694	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/hostname"]	pending	\N	2026-08-31 16:31:06
67	2026-08-31 16:40:47.110264	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/passwd"]	pending	\N	2026-08-31 16:36:25
68	2026-08-31 16:45:47.115084	\N	RD-5	192.168.100.20	\N	alto	directory_traversal	\N	\N	\N	\N	["/vulnerabilities/fi/?page=../../../../../etc/hostname"]	pending	\N	2026-08-31 16:41:12
69	2026-08-31 21:30:46.817199	\N	RD-6	labtest1	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest1	[{"command":"/usr/sbin/useradd testuser1","timestamp":"2026-08-31T21:27:57.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser1", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:27:57.000Z"}]	pending	\N	2026-08-31 21:27:57
70	2026-08-31 21:40:46.784737	\N	RD-6	labtest2	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest2	[{"command":"/usr/sbin/useradd testuser2","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser2", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
71	2026-08-31 21:40:46.784737	\N	RD-6	labtest3	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest3	[{"command":"/usr/sbin/useradd testuser3","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser3", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
72	2026-08-31 21:40:46.784737	\N	RD-6	labtest4	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest4	[{"command":"/usr/sbin/useradd testuser4","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser4", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
73	2026-08-31 21:40:46.784737	\N	RD-6	labtest5	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest5	[{"command":"/usr/sbin/useradd testuser5","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser5", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
74	2026-08-31 21:40:46.784737	\N	RD-6	labtest6	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest6	[{"command":"/usr/sbin/useradd testuser6","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser6", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
75	2026-08-31 21:40:46.784737	\N	RD-6	labtest7	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest7	[{"command":"/usr/sbin/useradd testuser7","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser7", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
76	2026-08-31 21:40:46.784737	\N	RD-6	labtest8	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest8	[{"command":"/usr/sbin/useradd testuser8","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser8", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
77	2026-08-31 21:40:46.784737	\N	RD-6	labtest9	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest9	[{"command":"/usr/sbin/useradd testuser9","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser9", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
78	2026-08-31 21:40:46.784737	\N	RD-6	labtest10	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por labtest10	[{"command":"/usr/sbin/useradd testuser10","timestamp":"2026-08-31T21:37:16.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd testuser10", "category": "cuenta_usuario", "timestamp": "2026-08-31T21:37:16.000Z"}]	pending	\N	2026-08-31 21:37:16
79	2026-09-14 19:55:44.913917	\N	RD-1	192.168.100.62	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-09-14 19:54:48
80	2026-09-14 20:15:45.574976	\N	RD-2	192.168.100.72	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-09-14 20:11:59
83	2026-09-19 20:55:45.468583	\N	RD-1	192.168.100.150	\N	alto	fuerza_bruta_ssh	0	5	Fuerza bruta SSH detectada	\N	\N	pending	\N	2026-09-19 20:55:02
81	2026-09-14 20:50:47.389681	\N	RD-4	192.168.100.20	\N	alto	sql_injection	0	3	\N	\N	["2026-09-14T17:42:27-03:00 dvwa-web apache-access 192.168.100.20 - - [14/Sep/2026:20:42:27 +0000] \\"GET /vulnerabilities/sqli/?id=select+all+UNION+members+from+our+database&Submit=Submit HTTP/1.1\\" 200 4751 \\"-\\" \\"curl/8.20.0\\"", "2026-09-14T17:42:27-03:00 dvwa-web apache-access 192.168.100.20 - - [14/Sep/2026:20:42:27 +0000] \\"GET /vulnerabilities/sqli/?id=how+to+select+from+a+UNION+menu&Submit=Submit HTTP/1.1\\" 200 4751 \\"-\\" \\"curl/8.20.0\\"", "2026-09-14T17:46:42-03:00 dvwa-web apache-access 192.168.100.20 - - [14/Sep/2026:20:46:42 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+user%2cpassword+FROM+users--+-&Submit=Submit HTTP/1.1\\" 200 5500 \\"-\\" \\"curl/8.20.0\\"", "2026-09-14T17:47:34-03:00 dvwa-web apache-access 192.168.100.20 - - [14/Sep/2026:20:47:32 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+null%2cversion%28%29--+-&Submit=Submit HTTP/1.1\\" 200 4949 \\"-\\" \\"curl/8.20.0\\"", "2026-09-14T17:48:22-03:00 dvwa-web apache-access 192.168.100.20 - - [14/Sep/2026:20:48:22 +0000] \\"GET /vulnerabilities/sqli/?id=1%27+UNION+SELECT+table_name%2cnull+FROM+information_schema.tables--+-&Submit=Submit HTTP/1.1\\" 200 15269 \\"-\\" \\"curl/8.20.0\\""]	reviewed	\N	2026-09-14 20:48:22
82	2026-09-14 21:20:48.368897	\N	RD-6	admin_real	ubuntu-soc	medio	cuenta_usuario	\N	1	Comandos sudo sensibles ejecutados por admin_real	[{"command":"/usr/sbin/useradd nuevoempleado","timestamp":"2026-09-14T21:20:13.000Z","category":"cuenta_usuario"}]	[{"command": "/usr/sbin/useradd nuevoempleado", "category": "cuenta_usuario", "timestamp": "2026-09-14T21:20:13.000Z"}]	pending	\N	2026-09-14 21:20:13
84	2026-09-23 03:45:46.352782	\N	RD-2	192.168.100.230	\N	alto	port_scan	0	11	Escaneo de puertos detectado: 11 puertos distintos en ventana de 2 min	\N	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080]}	pending	\N	2026-09-23 03:41:34
\.


--
-- Data for Name: playbook_runs; Type: TABLE DATA; Schema: public; Owner: n8n_soc
--

COPY public.playbook_runs (id, alert_id, workflow_name, started_at, executed_at, result, parameters) FROM stdin;
1	1	RD-5	2026-07-17 01:46:11.384	2026-07-17 01:46:14.820273	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
2	2	RD-1	2026-08-17 22:03:58	2026-08-17 22:06:01.340426	banned	{"ip": "192.168.100.20", "bantime": 3600, "approved_by": "manual"}
3	3	RD-1	2026-08-17 22:22:38	2026-08-17 22:25:49.826887	banned	{"ip": "192.168.100.20", "bantime": 3600, "approved_by": "manual"}
4	4	RD-1	2026-08-17 22:28:01	2026-08-17 22:30:48.26595	banned	{"ip": "192.168.100.20", "bantime": 3600, "approved_by": "manual"}
5	5	RD-1	2026-08-24 21:36:37	2026-08-24 21:41:41.968155	banned	{"ip": "192.168.100.20", "bantime": 3600, "approved_by": "manual"}
6	6	RD-1	2026-08-24 21:54:30	2026-08-24 21:55:55.513675	banned	{"ip": "192.168.100.21", "bantime": 3600, "approved_by": "manual"}
7	12	RD-1	2026-08-24 22:16:31	2026-08-24 22:33:29.645231	banned	{"ip": "192.168.100.27", "bantime": 3600, "approved_by": "manual"}
8	13	RD-1	2026-08-25 14:28:36	2026-08-25 14:30:47.907374	banned	{"ip": "192.168.100.101", "bantime": 3600, "approved_by": "manual"}
9	14	RD-1	2026-08-25 14:31:08	2026-08-25 14:35:47.141322	banned	{"ip": "192.168.100.102", "bantime": 3600, "approved_by": "manual"}
10	15	RD-1	2026-08-25 14:35:59	2026-08-25 14:40:47.676457	banned	{"ip": "192.168.100.103", "bantime": 3600, "approved_by": "manual"}
11	16	RD-1	2026-08-25 14:41:09	2026-08-25 14:45:46.88397	banned	{"ip": "192.168.100.104", "bantime": 3600, "approved_by": "manual"}
12	17	RD-1	2026-08-25 14:46:05	2026-08-25 14:50:49.312581	banned	{"ip": "192.168.100.105", "bantime": 3600, "approved_by": "manual"}
13	18	RD-1	2026-08-25 14:51:12	2026-08-25 14:56:15.771041	banned	{"ip": "192.168.100.106", "bantime": 3600, "approved_by": "manual"}
14	19	RD-1	2026-08-25 14:56:47	2026-08-25 15:00:48.032899	banned	{"ip": "192.168.100.107", "bantime": 3600, "approved_by": "manual"}
15	20	RD-1	2026-08-25 15:01:06	2026-08-25 15:05:47.252813	banned	{"ip": "192.168.100.108", "bantime": 3600, "approved_by": "manual"}
16	21	RD-1	2026-08-25 15:06:03	2026-08-25 15:10:47.28624	banned	{"ip": "192.168.100.109", "bantime": 3600, "approved_by": "manual"}
17	22	RD-1	2026-08-25 15:11:06	2026-08-25 15:15:46.852878	banned	{"ip": "192.168.100.110", "bantime": 3600, "approved_by": "manual"}
18	24	RD-2	2026-08-25 22:08:27	2026-08-25 22:25:50.136296	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.201"}
19	25	RD-2	2026-08-25 22:28:10	2026-08-25 22:30:48.235632	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.211"}
20	26	RD-2	2026-08-25 22:40:49	2026-08-25 22:45:48.275114	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.212"}
21	27	RD-2	2026-08-25 22:46:47	2026-08-25 22:50:47.962556	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.213"}
22	28	RD-2	2026-08-25 22:51:16	2026-08-25 22:55:47.620376	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.214"}
23	29	RD-2	2026-08-25 22:56:01	2026-08-25 23:00:52.26349	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.215"}
24	30	RD-2	2026-08-25 23:01:13	2026-08-25 23:05:47.555484	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.216"}
25	31	RD-2	2026-08-25 23:06:04	2026-08-25 23:10:50.971356	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.217"}
26	32	RD-2	2026-08-25 23:11:08	2026-08-25 23:15:53.742477	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.218"}
27	33	RD-2	2026-08-25 23:16:11	2026-08-25 23:20:47.907608	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.219"}
28	34	RD-2	2026-08-25 23:21:03	2026-08-25 23:25:48.062406	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.220"}
29	35	RD-3	2026-08-26 20:18:16	2026-08-26 20:20:50.427635	banned	{"src_ip": "192.168.100.41", "accepted": false, "last_seen": "2026-08-26T20:18:16.000Z", "first_seen": "2026-08-26T20:18:16.000Z", "ports_used": ["51422"], "failed_attempts": 1}
30	36	RD-3	2026-08-26 20:21:45	2026-08-26 20:25:49.591354	banned	{"src_ip": "192.168.100.42", "accepted": false, "last_seen": "2026-08-26T20:21:45.000Z", "first_seen": "2026-08-26T20:21:45.000Z", "ports_used": ["51422"], "failed_attempts": 1}
31	37	RD-3	2026-08-26 20:25:54	2026-08-26 20:30:48.26284	banned	{"src_ip": "192.168.100.43", "accepted": false, "last_seen": "2026-08-26T20:26:00.000Z", "first_seen": "2026-08-26T20:25:54.000Z", "ports_used": ["51422", "51422"], "failed_attempts": 2}
32	38	RD-3	2026-08-26 20:31:05	2026-08-26 20:35:49.058023	banned	{"src_ip": "192.168.100.44", "accepted": false, "last_seen": "2026-08-26T20:31:11.000Z", "first_seen": "2026-08-26T20:31:05.000Z", "ports_used": ["51422", "51422"], "failed_attempts": 2}
33	40	RD-3	2026-08-26 20:36:26	2026-08-26 20:40:48.429561	banned	{"src_ip": "192.168.100.44", "accepted": false, "last_seen": "2026-08-26T20:36:26.000Z", "first_seen": "2026-08-26T20:36:26.000Z", "ports_used": ["51422"], "failed_attempts": 1}
34	42	RD-3	2026-08-26 20:41:20	2026-08-26 20:45:50.673653	banned	{"src_ip": "192.168.100.46", "accepted": false, "last_seen": "2026-08-26T20:41:20.000Z", "first_seen": "2026-08-26T20:41:20.000Z", "ports_used": ["51422"], "failed_attempts": 1}
35	43	RD-3	2026-08-26 20:46:02	2026-08-26 20:50:49.139773	banned	{"src_ip": "192.168.100.47", "accepted": false, "last_seen": "2026-08-26T20:46:02.000Z", "first_seen": "2026-08-26T20:46:02.000Z", "ports_used": ["51422"], "failed_attempts": 1}
36	44	RD-3	2026-08-26 20:51:16	2026-08-26 20:55:51.197247	banned	{"src_ip": "192.168.100.48", "accepted": false, "last_seen": "2026-08-26T20:51:16.000Z", "first_seen": "2026-08-26T20:51:16.000Z", "ports_used": ["51422"], "failed_attempts": 1}
37	45	RD-3	2026-08-26 20:56:12	2026-08-26 21:00:47.961625	banned	{"src_ip": "192.168.100.49", "accepted": false, "last_seen": "2026-08-26T20:56:12.000Z", "first_seen": "2026-08-26T20:56:12.000Z", "ports_used": ["51422"], "failed_attempts": 1}
38	46	RD-3	2026-08-26 21:01:04	2026-08-26 21:06:01.276166	banned	{"src_ip": "192.168.100.50", "accepted": false, "last_seen": "2026-08-26T21:01:04.000Z", "first_seen": "2026-08-26T21:01:04.000Z", "ports_used": ["51422"], "failed_attempts": 1}
39	47	RD-3	2026-08-26 21:09:39	2026-08-26 21:10:53.446534	banned	{"src_ip": "192.168.100.45", "accepted": false, "last_seen": "2026-08-26T21:09:39.000Z", "first_seen": "2026-08-26T21:09:39.000Z", "ports_used": ["51422"], "failed_attempts": 1}
40	48	RD-4	2026-08-29 20:56:40.687586	2026-08-29 20:56:40.687586	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
41	49	RD-4	2026-08-29 21:26:19.863593	2026-08-29 21:26:19.863593	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
42	50	RD-4	2026-08-29 21:30:52.953943	2026-08-29 21:30:52.953943	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
43	51	RD-4	2026-08-29 21:35:49.16829	2026-08-29 21:35:49.16829	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
44	52	RD-4	2026-08-29 21:40:51.325147	2026-08-29 21:40:51.325147	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
45	53	RD-4	2026-08-29 21:46:05.553228	2026-08-29 21:46:05.553228	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
46	54	RD-4	2026-08-29 21:50:51.816262	2026-08-29 21:50:51.816262	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
47	55	RD-4	2026-08-29 21:55:58.508401	2026-08-29 21:55:58.508401	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
48	56	RD-4	2026-08-29 22:01:11.578909	2026-08-29 22:01:11.578909	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
49	57	RD-4	2026-08-29 22:06:22.102737	2026-08-29 22:06:22.102737	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
50	58	RD-4	2026-08-29 22:11:15.743697	2026-08-29 22:11:15.743697	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
51	59	RD-5	2026-08-31 16:00:45.799	2026-08-31 16:00:50.557214	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
52	60	RD-5	2026-08-31 16:05:45.981	2026-08-31 16:05:49.00855	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
53	61	RD-5	2026-08-31 16:10:46.001	2026-08-31 16:10:51.106228	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
54	62	RD-5	2026-08-31 16:15:45.879	2026-08-31 16:15:51.364932	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
55	63	RD-5	2026-08-31 16:20:45.982	2026-08-31 16:20:49.986434	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
56	64	RD-5	2026-08-31 16:25:45.937	2026-08-31 16:25:52.253579	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
57	65	RD-5	2026-08-31 16:30:46.238	2026-08-31 16:30:51.260251	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
58	66	RD-5	2026-08-31 16:35:45.934	2026-08-31 16:35:51.628198	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
59	67	RD-5	2026-08-31 16:40:46.563	2026-08-31 16:40:54.199062	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
60	68	RD-5	2026-08-31 16:45:46.55	2026-08-31 16:45:50.825109	banned	{"src_ip": "192.168.100.20", "attempt_count": 1}
61	79	RD-1	2026-09-14 19:54:48	2026-09-14 19:55:49.820129	banned	{"ip": "192.168.100.62", "bantime": 3600, "approved_by": "manual"}
62	80	RD-2	2026-09-14 20:11:59	2026-09-14 20:15:53.599974	banned	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.72"}
63	81	RD-4	2026-09-14 20:50:59.586088	2026-09-14 20:50:59.586088	banned	{"count": 3, "src_ip": "192.168.100.20", "bantime": 3600}
64	83	RD-1	2026-09-19 20:55:02	2026-09-19 20:55:49.719495	banned	{"ip": "192.168.100.150", "bantime": 3600, "approved_by": "manual"}
65	84	RD-2	2026-09-23 03:41:34	2026-09-23 03:46:04.067727	rejected_by_analyst	{"ports": [21, 22, 23, 25, 53, 80, 110, 143, 443, 3306, 8080], "src_ip": "192.168.100.230"}
\.


--
-- Name: alerts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: n8n_soc
--

SELECT pg_catalog.setval('public.alerts_id_seq', 84, true);


--
-- Name: playbook_runs_id_seq; Type: SEQUENCE SET; Schema: public; Owner: n8n_soc
--

SELECT pg_catalog.setval('public.playbook_runs_id_seq', 65, true);


--
-- PostgreSQL database dump complete
--

\unrestrict AEw8vsrQvRP3TRlEmHTDggmxd7khDTBn63QCrm6v1EToCBJLjM3LhePyC0i8EM2

