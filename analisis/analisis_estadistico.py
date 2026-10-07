"""
Análisis estadístico — Laboratorio SOC Académico con n8n
Comparación fase de control (calculada) vs. fase experimental (medida) sobre 60 pares reales
(10 repeticiones x 6 reglas de detección: RD-1 a RD-6)

Fuente de los datos (exportados de las tablas `alerts` y `playbook_runs` de PostgreSQL):
  - Sesiones de medición de las 60 repeticiones: 25, 26, 29 y 31 de agosto de 2026
    (RD-1 y RD-2: 25/08; RD-3: 26/08; RD-4: 29/08; RD-5 y RD-6: 31/08).
  - Casos de borde (actividad benigna y evasiones): 14 de septiembre de 2026.
  - Ensayos previos de comprobación con hydra para RD-1 (fuera del dataset de medición): 17 y 24 de agosto de 2026.
RD-6 no genera `executed_at` (regla fire-and-forget, sin bloqueo automático), por lo que se
excluye del análisis de MTTR.

Metodología fase de control: no se ejecutó en vivo. Se calcula matemáticamente a partir
del mismo `event_timestamp` real de cada ataque, asumiendo un analista que revisa la cola
de alertas cada 20 minutos (puntos de revisión en :00, :20, :40 de cada hora) más un tiempo
fijo de respuesta manual de 2.5 minutos (150s) una vez detectado.

RUTAS: todas las salidas se escriben con rutas RELATIVAS, en el directorio desde donde se
ejecuta el script. Este script NO sobrescribe `dataset_pareado.csv` (el volcado pareado con
claves alert_id/playbook_run_id exportado de Postgres, que se versiona aparte); escribe sus
métricas en `metricas_resultados.csv` para no pisar esas claves. Si `dataset_pareado.csv`
está presente en el directorio, el bloque de VALIDACIÓN DE CLAVES lo controla sin modificarlo.
"""

import os
import numpy as np
from scipy import stats
from datetime import datetime, timedelta
import csv

# ---------------------------------------------------------------------------
# 1. DATOS CRUDOS — 60 repeticiones (event_timestamp, created_at, executed_at)
#    Todos los timestamps en UTC tal como quedaron almacenados en Postgres.
# ---------------------------------------------------------------------------

FMT = "%Y-%m-%d %H:%M:%S.%f"

def t(s):
    """Parsea un timestamp con microsegundos opcionales."""
    if "." not in s:
        s = s + ".0"
    return datetime.strptime(s, FMT)

raw = [
    # regla, id, event_timestamp, created_at, executed_at (None si no aplica, como RD-6)
    ("RD-1", "101", "2026-08-25 14:28:36.0", "2026-08-25 14:30:44.725793", "2026-08-25 14:30:47.907374"),
    ("RD-1", "102", "2026-08-25 14:31:08.0", "2026-08-25 14:35:44.537646", "2026-08-25 14:35:47.141322"),
    ("RD-1", "103", "2026-08-25 14:35:59.0", "2026-08-25 14:40:44.570359", "2026-08-25 14:40:47.676457"),
    ("RD-1", "104", "2026-08-25 14:41:09.0", "2026-08-25 14:45:44.555797", "2026-08-25 14:45:46.883970"),
    ("RD-1", "105", "2026-08-25 14:46:05.0", "2026-08-25 14:50:44.607525", "2026-08-25 14:50:49.312581"),
    ("RD-1", "106", "2026-08-25 14:51:12.0", "2026-08-25 14:55:44.573210", "2026-08-25 14:56:15.771041"),
    ("RD-1", "107", "2026-08-25 14:56:47.0", "2026-08-25 15:00:44.837733", "2026-08-25 15:00:48.032899"),
    ("RD-1", "108", "2026-08-25 15:01:06.0", "2026-08-25 15:05:44.703065", "2026-08-25 15:05:47.252813"),
    ("RD-1", "109", "2026-08-25 15:06:03.0", "2026-08-25 15:10:44.638005", "2026-08-25 15:10:47.286240"),
    ("RD-1", "110", "2026-08-25 15:11:06.0", "2026-08-25 15:15:44.567204", "2026-08-25 15:15:46.852878"),

    ("RD-2", "211", "2026-08-25 22:28:10.0", "2026-08-25 22:30:44.937008", "2026-08-25 22:30:48.235632"),
    ("RD-2", "212", "2026-08-25 22:40:49.0", "2026-08-25 22:45:45.535540", "2026-08-25 22:45:48.275114"),
    ("RD-2", "213", "2026-08-25 22:46:47.0", "2026-08-25 22:50:45.129561", "2026-08-25 22:50:47.962556"),
    ("RD-2", "214", "2026-08-25 22:51:16.0", "2026-08-25 22:55:45.083532", "2026-08-25 22:55:47.620376"),
    ("RD-2", "215", "2026-08-25 22:56:01.0", "2026-08-25 23:00:44.865153", "2026-08-25 23:00:52.263490"),
    ("RD-2", "216", "2026-08-25 23:01:13.0", "2026-08-25 23:05:45.024857", "2026-08-25 23:05:47.555484"),
    ("RD-2", "217", "2026-08-25 23:06:04.0", "2026-08-25 23:10:44.935335", "2026-08-25 23:10:50.971356"),
    ("RD-2", "218", "2026-08-25 23:11:08.0", "2026-08-25 23:15:44.928154", "2026-08-25 23:15:53.742477"),
    ("RD-2", "219", "2026-08-25 23:16:11.0", "2026-08-25 23:20:44.874684", "2026-08-25 23:20:47.907608"),
    ("RD-2", "220", "2026-08-25 23:21:03.0", "2026-08-25 23:25:44.961494", "2026-08-25 23:25:48.062406"),

    ("RD-3", "41", "2026-08-26 20:18:16.0", "2026-08-26 20:20:45.366522", "2026-08-26 20:20:50.427635"),
    ("RD-3", "42", "2026-08-26 20:21:45.0", "2026-08-26 20:25:45.436934", "2026-08-26 20:25:49.591354"),
    ("RD-3", "43", "2026-08-26 20:25:54.0", "2026-08-26 20:30:45.537592", "2026-08-26 20:30:48.262840"),
    ("RD-3", "44a", "2026-08-26 20:31:05.0", "2026-08-26 20:35:45.484470", "2026-08-26 20:35:49.058023"),
    ("RD-3", "44b", "2026-08-26 20:36:26.0", "2026-08-26 20:40:45.647094", "2026-08-26 20:40:48.429561"),
    ("RD-3", "46", "2026-08-26 20:41:20.0", "2026-08-26 20:45:45.792152", "2026-08-26 20:45:50.673653"),
    ("RD-3", "47", "2026-08-26 20:46:02.0", "2026-08-26 20:50:45.260063", "2026-08-26 20:50:49.139773"),
    ("RD-3", "48", "2026-08-26 20:51:16.0", "2026-08-26 20:55:45.394938", "2026-08-26 20:55:51.197247"),
    ("RD-3", "49", "2026-08-26 20:56:12.0", "2026-08-26 21:00:45.383586", "2026-08-26 21:00:47.961625"),
    ("RD-3", "45", "2026-08-26 21:09:39.0", "2026-08-26 21:10:45.399078", "2026-08-26 21:10:53.446534"),

    ("RD-4", "sqli1", "2026-08-29 21:20:53.0", "2026-08-29 21:25:46.031419", "2026-08-29 21:26:19.863593"),
    ("RD-4", "sqli2", "2026-08-29 21:27:19.0", "2026-08-29 21:30:45.947121", "2026-08-29 21:30:52.953943"),
    ("RD-4", "sqli3", "2026-08-29 21:31:34.0", "2026-08-29 21:35:45.986064", "2026-08-29 21:35:49.168290"),
    ("RD-4", "sqli4", "2026-08-29 21:37:16.0", "2026-08-29 21:40:45.915723", "2026-08-29 21:40:51.325147"),
    ("RD-4", "sqli5", "2026-08-29 21:42:00.0", "2026-08-29 21:45:46.085455", "2026-08-29 21:46:05.553228"),
    ("RD-4", "sqli6", "2026-08-29 21:46:49.0", "2026-08-29 21:50:45.906147", "2026-08-29 21:50:51.816262"),
    ("RD-4", "sqli7", "2026-08-29 21:51:59.0", "2026-08-29 21:55:46.361277", "2026-08-29 21:55:58.508401"),
    ("RD-4", "sqli8", "2026-08-29 21:56:54.0", "2026-08-29 22:00:46.063316", "2026-08-29 22:01:11.578909"),
    ("RD-4", "sqli9", "2026-08-29 22:02:21.0", "2026-08-29 22:05:46.098277", "2026-08-29 22:06:22.102737"),
    ("RD-4", "sqli10", "2026-08-29 22:07:03.0", "2026-08-29 22:10:45.945687", "2026-08-29 22:11:15.743697"),

    ("RD-5", "trav1", "2026-08-31 15:59:00.0", "2026-08-31 16:00:46.450116", "2026-08-31 16:00:50.557214"),
    ("RD-5", "trav2", "2026-08-31 16:02:22.0", "2026-08-31 16:05:46.471744", "2026-08-31 16:05:49.008550"),
    ("RD-5", "trav3", "2026-08-31 16:06:16.0", "2026-08-31 16:10:46.541502", "2026-08-31 16:10:51.106228"),
    ("RD-5", "trav4", "2026-08-31 16:11:15.0", "2026-08-31 16:15:46.428822", "2026-08-31 16:15:51.364932"),
    ("RD-5", "trav5", "2026-08-31 16:16:08.0", "2026-08-31 16:20:46.462213", "2026-08-31 16:20:49.986434"),
    ("RD-5", "trav6", "2026-08-31 16:21:10.0", "2026-08-31 16:25:46.427669", "2026-08-31 16:25:52.253579"),
    ("RD-5", "trav7", "2026-08-31 16:26:19.0", "2026-08-31 16:30:46.778731", "2026-08-31 16:30:51.260251"),
    ("RD-5", "trav8", "2026-08-31 16:31:06.0", "2026-08-31 16:35:46.512694", "2026-08-31 16:35:51.628198"),
    ("RD-5", "trav9", "2026-08-31 16:36:25.0", "2026-08-31 16:40:47.110264", "2026-08-31 16:40:54.199062"),
    ("RD-5", "trav10", "2026-08-31 16:41:12.0", "2026-08-31 16:45:47.115084", "2026-08-31 16:45:50.825109"),

    ("RD-6", "labtest1", "2026-08-31 21:27:57.0", "2026-08-31 21:30:46.817199", None),
    ("RD-6", "labtest2", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest3", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest4", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest5", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest6", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest7", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest8", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest9", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
    ("RD-6", "labtest10", "2026-08-31 21:37:16.0", "2026-08-31 21:40:46.784737", None),
]

assert len(raw) == 60, f"Se esperaban 60 repeticiones, hay {len(raw)}"

# ---------------------------------------------------------------------------
# 2. PARÁMETROS DE LA FASE DE CONTROL (calculada, decisión de diseño documentada)
# ---------------------------------------------------------------------------
REVIEW_INTERVAL_MIN = 20      # el analista revisa la cola cada 20 minutos
MANUAL_RESPONSE_SEC = 150     # 2.5 min fijos para identificar y ejecutar el bloqueo a mano

def next_checkpoint(event_time):
    """Próximo punto de revisión en :00, :20, :40 de la hora, en o después del evento."""
    minute = event_time.minute
    checkpoints = [0, 20, 40]
    for cp in checkpoints:
        if cp >= minute:
            candidate = event_time.replace(minute=cp, second=0, microsecond=0)
            if candidate >= event_time:
                return candidate
    # ninguno alcanzó dentro de la hora -> próxima hora, minuto 0
    return (event_time.replace(minute=0, second=0, microsecond=0) + timedelta(hours=1))

# ---------------------------------------------------------------------------
# 3. CONSTRUCCIÓN DEL DATASET PAREADO
# ---------------------------------------------------------------------------
rows = []
for regla, id_, ev, created, executed in raw:
    event_time = t(ev)
    created_time = t(created)
    executed_time = t(executed) if executed else None

    mtta_auto = (created_time - event_time).total_seconds()
    mttr_auto = (executed_time - event_time).total_seconds() if executed_time else None

    checkpoint = next_checkpoint(event_time)
    mtta_manual = (checkpoint - event_time).total_seconds()
    mttr_manual = mtta_manual + MANUAL_RESPONSE_SEC

    rows.append({
        "regla": regla, "id": id_,
        "mtta_auto": mtta_auto, "mtta_manual": mtta_manual,
        "mttr_auto": mttr_auto, "mttr_manual": mttr_manual if mttr_auto is not None else None,
    })

# Exportar las MÉTRICAS calculadas (para anexo técnico / verificación del tribunal).
# IMPORTANTE (T8): este archivo NO es el volcado pareado con claves. El dataset con
# claves alert_id/playbook_run_id (dataset_pareado.csv) se exporta de Postgres y se
# versiona aparte; acá solo se escriben las métricas derivadas, en un archivo propio,
# para no sobrescribir esas claves al re-ejecutar el script.
with open("metricas_resultados.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["regla", "id", "mtta_auto", "mtta_manual", "mttr_auto", "mttr_manual"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# 3bis. VALIDACIÓN DE CLAVES DEL VOLCADO PAREADO (hallazgo D2)
#   Controla, sin modificarlo, el dataset con claves exportado de Postgres
#   (dataset_pareado.csv). Falla de forma explícita si:
#     - se repite un alert_id (cada repetición referencia una alerta distinta), o
#     - una fila de RD-6 no tiene un alert_id del rango esperado (69 a 78).
#   RD-6 no ejecuta bloqueo, por lo que sus filas NO deben tener playbook_run_id.
#   Si el archivo no está en el directorio, se omite la validación (el script
#   sigue siendo ejecutable de forma autónoma para el resto del análisis).
# ---------------------------------------------------------------------------
def validar_claves(path="dataset_pareado.csv"):
    if not os.path.exists(path):
        print(f"\n[validación de claves] {path} no está en el directorio: se omite.")
        return True
    with open(path, newline="") as f:
        filas = list(csv.DictReader(f))
    cols = filas[0].keys() if filas else []
    if "alert_id" not in cols:
        print(f"\n[validación de claves] {path} no tiene columna alert_id: se omite.")
        return True

    errores = []
    # 1) alert_id único en todo el dataset
    vistos = {}
    for fila in filas:
        aid = (fila.get("alert_id") or "").strip()
        if aid == "":
            continue
        vistos.setdefault(aid, []).append(fila.get("id", "?"))
    for aid, quienes in vistos.items():
        if len(quienes) > 1:
            errores.append(f"alert_id {aid} repetido en filas: {', '.join(quienes)}")

    # 2) RD-6: alert_id en el rango 69–78 y sin playbook_run_id
    rd6 = [fila for fila in filas if (fila.get("regla") or "").strip() == "RD-6"]
    for fila in rd6:
        aid = (fila.get("alert_id") or "").strip()
        if aid and not (aid.isdigit() and 69 <= int(aid) <= 78):
            errores.append(f"RD-6 fila {fila.get('id','?')}: alert_id {aid} fuera del rango 69–78")
        prid = (fila.get("playbook_run_id") or "").strip()
        if prid not in ("", "NULL", "None", "—", "-"):
            errores.append(f"RD-6 fila {fila.get('id','?')}: no debería tener playbook_run_id ({prid})")

    print("\n" + "=" * 70)
    print("VALIDACIÓN DE CLAVES DEL VOLCADO PAREADO (D2)")
    print("=" * 70)
    if errores:
        print(f"FALLÓ: {len(errores)} inconsistencia(s) en {path}:")
        for e in errores:
            print(f"  - {e}")
        # No abortamos el análisis estadístico (las métricas no dependen de las claves),
        # pero el fallo queda registrado de forma inequívoca para el tribunal.
        return False
    print(f"OK: {len(filas)} filas, alert_id únicos y RD-6 con claves 69–78 sin playbook_run_id.")
    return True

validar_claves()

# ---------------------------------------------------------------------------
# 4. ANÁLISIS ESTADÍSTICO — MTTA (60 pares) y MTTR (50 pares, sin RD-6)
# ---------------------------------------------------------------------------
def wilcoxon_report(name, auto_vals, manual_vals, n_bootstrap=5000, seed=42):
    auto = np.array(auto_vals)
    manual = np.array(manual_vals)
    n = len(auto)
    diff = manual - auto  # positivo = automatizado más rápido

    stat, p = stats.wilcoxon(manual, auto, alternative="greater")

    # Método del p-valor (hallazgo N12): se declara explícitamente si el p reportado
    # proviene de la aproximación normal o del cálculo exacto, y se informan ambos.
    try:
        p_exacto = stats.wilcoxon(manual, auto, alternative="greater", method="exact").pvalue
    except Exception:
        p_exacto = float("nan")
    p_aprox = stats.wilcoxon(manual, auto, alternative="greater", method="approx").pvalue
    # scipy usa 'exact' hasta N≈50 y 'approx' por encima; declaramos cuál aplica aquí.
    metodo = "aproximación normal" if n > 50 else "exacto"

    # Z calculado directamente de la aproximación normal del estadístico de Wilcoxon,
    # NO invirtiendo el p-valor (eso se rompe cuando p redondea a 0.0 por precisión
    # de punto flotante, dando Z=infinito y r>1, que es matemáticamente imposible).
    # Fórmula estándar: mu = n(n+1)/4, sigma = sqrt(n(n+1)(2n+1)/24)
    n_eff = np.sum(diff != 0)  # excluye empates, como hace Wilcoxon internamente
    mu_w = n_eff * (n_eff + 1) / 4
    sigma_w = np.sqrt(n_eff * (n_eff + 1) * (2 * n_eff + 1) / 24)
    z = (stat - mu_w) / sigma_w
    r = z / np.sqrt(n)
    r = min(r, 1.0)  # tope teórico de r, por las dudas ante casos extremos

    rng = np.random.default_rng(seed)
    boot_diffs = []
    idx = np.arange(n)
    for _ in range(n_bootstrap):
        sample = rng.choice(idx, size=n, replace=True)
        # IC bootstrap sobre la DIFERENCIA DE MEDIANAS (coherente con el estimador
        # de reducción usado en la tesis: mediana_manual - mediana_auto)
        boot_diffs.append(np.median(manual[sample]) - np.median(auto[sample]))
    ci_low, ci_high = np.percentile(boot_diffs, [2.5, 97.5])

    # Estimador de reducción: reducción de las medianas (no mediana de reducciones
    # pareadas). Es el criterio declarado en la tesis (§13.3), reconstruible desde
    # la tabla de descriptivos: (mediana_control - mediana_experimental)/mediana_control.
    diff_medianas = np.median(manual) - np.median(auto)
    reduction_pct = (diff_medianas / np.median(manual)) * 100

    print(f"\n--- {name} (N={n}) ---")
    print(f"Mediana automatizado: {np.median(auto):.1f}s ({np.median(auto)/60:.2f} min)")
    print(f"Mediana manual (control): {np.median(manual):.1f}s ({np.median(manual)/60:.2f} min)")
    print(f"Diferencia de medianas (manual - auto): {diff_medianas:.1f}s")
    print(f"Wilcoxon signed-rank: W={stat:.1f}, p={p:.10f}  [método reportado: {metodo}]")
    print(f"   p por aproximación normal: {p_aprox:.3e}  |  p exacto: {p_exacto:.3e}")
    print(f"Z (aprox. normal, calculado directo del estadístico): {z:.3f}")
    print(f"Tamaño del efecto r = Z/sqrt(N): {r:.3f}")
    print(f"IC 95% bootstrap de la diferencia de medianas: [{ci_low:.1f}s, {ci_high:.1f}s]")
    contains = ci_low <= diff_medianas <= ci_high
    print(f"¿El IC contiene la diferencia observada?: {contains}")
    print(f"Reducción de las medianas: {reduction_pct:.1f}%")
    return {
        "n": n, "median_auto": np.median(auto), "median_manual": np.median(manual),
        "median_diff": diff_medianas, "W": stat, "p": p, "z": z, "r": r,
        "ci_low": ci_low, "ci_high": ci_high, "reduction_pct": reduction_pct,
        "metodo_p": metodo, "p_aprox": p_aprox, "p_exacto": p_exacto
    }

print("=" * 70)
print("ANÁLISIS ESTADÍSTICO — MTTA y MTTR, fase experimental vs. control calculada")
print("=" * 70)

mtta_auto_all = [r["mtta_auto"] for r in rows]
mtta_manual_all = [r["mtta_manual"] for r in rows]
res_mtta = wilcoxon_report("MTTA (todas las reglas, N=60)", mtta_auto_all, mtta_manual_all)

rows_mttr = [r for r in rows if r["mttr_auto"] is not None]
mttr_auto_all = [r["mttr_auto"] for r in rows_mttr]
mttr_manual_all = [r["mttr_manual"] for r in rows_mttr]
res_mttr = wilcoxon_report("MTTR (RD-1 a RD-5, N=50 — RD-6 no ejecuta bloqueo)", mttr_auto_all, mttr_manual_all)

# Desagregado por regla (solo MTTA, para no saturar la salida)
print("\n" + "=" * 70)
print("MTTA desagregado por regla")
print("=" * 70)
for regla in ["RD-1", "RD-2", "RD-3", "RD-4", "RD-5", "RD-6"]:
    sub = [r for r in rows if r["regla"] == regla]
    auto = [r["mtta_auto"] for r in sub]
    manual = [r["mtta_manual"] for r in sub]
    print(f"{regla}: auto mediana={np.median(auto):.1f}s | manual mediana={np.median(manual):.1f}s "
          f"| N={len(sub)}")

# ---------------------------------------------------------------------------
# 5. CASOS DE BORDE DE LAS REGLAS (no son métricas de desempeño del sistema)
#    Documentan el comportamiento de cada regla en sus límites. NO se reportan
#    precisión/recall/FPR agregadas, porque estos casos fueron diseñados (una
#    cantidad fija de cada tipo) y cualquier métrica agregada reflejaría esa
#    composición elegida, no un desempeño sobre tráfico representativo.
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("CASOS DE BORDE DE LAS REGLAS (comportamiento en los límites)")
print("=" * 70)

TP = 60  # las 60 repeticiones de detección: ataques reales correctamente detectados
TN = 4   # actividad benigna correctamente ignorada (RD-1, RD-2, RD-4, RD-6)
FP = 4   # actividad legítima que cruza el umbral (RD-1, RD-2, RD-4, RD-6)
FN = 6   # ataques que evaden la detección (uno por regla)

print(f"Ataques detectados (TP): {TP}")
print(f"Casos benignos correctamente ignorados (TN): {TN}")
print(f"Casos benignos que cruzaron el umbral (FP): {FP}")
print(f"Ataques que evadieron la detección (FN): {FN}")
print()
print("NOTA: estos conteos NO se agregan en métricas de precisión/recall/FPR,")
print("porque la cantidad de cada tipo fue elegida por diseño. Su valor es")
print("cualitativo: cada caso documenta un límite concreto de una regla")
print("(ver §13.5 y §14.4 de la tesis). Una estimación de la tasa real de")
print("falsos positivos requeriría un corpus independiente de tráfico legítimo,")
print("planteado como trabajo futuro.")

# ---------------------------------------------------------------------------
# 6. GUARDAR RESUMEN EN CSV
# ---------------------------------------------------------------------------
with open("resumen_resultados.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["metrica", "valor"])
    writer.writerow(["MTTA_mediana_automatizado_s", f"{res_mtta['median_auto']:.1f}"])
    writer.writerow(["MTTA_mediana_manual_s", f"{res_mtta['median_manual']:.1f}"])
    writer.writerow(["MTTA_Wilcoxon_W", f"{res_mtta['W']:.1f}"])
    writer.writerow(["MTTA_p_valor", f"{res_mtta['p']:.6f}"])
    writer.writerow(["MTTA_r_efecto", f"{res_mtta['r']:.3f}"])
    writer.writerow(["MTTA_reduccion_pct", f"{res_mtta['reduction_pct']:.1f}"])
    writer.writerow(["MTTR_mediana_automatizado_s", f"{res_mttr['median_auto']:.1f}"])
    writer.writerow(["MTTR_mediana_manual_s", f"{res_mttr['median_manual']:.1f}"])
    writer.writerow(["MTTR_Wilcoxon_W", f"{res_mttr['W']:.1f}"])
    writer.writerow(["MTTR_p_valor", f"{res_mttr['p']:.6f}"])
    writer.writerow(["MTTR_r_efecto", f"{res_mttr['r']:.3f}"])
    writer.writerow(["MTTR_reduccion_pct", f"{res_mttr['reduction_pct']:.1f}"])
    writer.writerow(["casos_borde_TP", TP]); writer.writerow(["casos_borde_TN", TN])
    writer.writerow(["casos_borde_FP", FP]); writer.writerow(["casos_borde_FN", FN])

print("\n\nArchivos generados: dataset_pareado.csv, resumen_resultados.csv")

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 8. ANÁLISIS DE SENSIBILIDAD DEL BRAZO DE CONTROL
#    Cómo varía la reducción del MTTA según el intervalo de revisión manual asumido
# ---------------------------------------------------------------------------

# 7bis. ROBUSTEZ: Wilcoxon del MTTA excluyendo RD-6 (cuyas 10 repeticiones no son
#       temporalmente independientes; ver §14.2 de la tesis). Confirma que la
#       conclusión no depende de esa regla.
print("\n" + "=" * 70)
print("ROBUSTEZ — MTTA excluyendo RD-6 (N=50)")
print("=" * 70)
sub_sin_rd6 = [r for r in rows if r["regla"] != "RD-6"]
auto_s = np.array([r["mtta_auto"] for r in sub_sin_rd6])
manual_s = np.array([r["mtta_manual"] for r in sub_sin_rd6])
stat_s, p_s = stats.wilcoxon(manual_s, auto_s, alternative="greater")
n_s = len(auto_s); neff_s = np.sum((manual_s - auto_s) != 0)
mu_s = neff_s*(neff_s+1)/4; sigma_s = np.sqrt(neff_s*(neff_s+1)*(2*neff_s+1)/24)
z_s = (stat_s - mu_s)/sigma_s; r_s = min(z_s/np.sqrt(n_s), 1.0)
red_s = (np.median(manual_s) - np.median(auto_s))/np.median(manual_s)*100
print(f"W={stat_s:.0f}, p={p_s:.3e}, z={z_s:.3f}, r={r_s:.3f}, reducción={red_s:.1f}%")
print("(La tesis reporta: W=1197, p=5,96e-10, r=0,764, reducción=61,1%)")

# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("ANÁLISIS DE SENSIBILIDAD — reducción del MTTA por intervalo de revisión")
print("=" * 70)

def next_checkpoint_interval(event_time, interval_min):
    """Próximo punto de revisión manual, para una grilla de revisión cada interval_min
    minutos anclada a la medianoche (0, interval, 2*interval, ...)."""
    minutos_desde_medianoche = event_time.hour * 60 + event_time.minute + event_time.second / 60
    proximo = ((int(minutos_desde_medianoche) // interval_min) + 1) * interval_min
    base = event_time.replace(hour=0, minute=0, second=0, microsecond=0)
    return base + timedelta(minutes=proximo)

mtta_auto_arr = np.array([r["mtta_auto"] for r in rows])
med_a = np.median(mtta_auto_arr)

# Grilla fina de 1 en 1 minuto entre 5 y 25, para identificar el PUNTO DE EQUILIBRIO:
# el intervalo de revisión manual a partir del cual la automatización pasa a ser más rápida.
print(f"{'Intervalo':>10} | {'Med. manual':>12} | {'Reducción':>10} | {'p (una cola, dir. H1)':>22}")
print("-" * 62)
punto_equilibrio = None
for interval in range(5, 31):
    manual = []
    for regla, id_, ev, created, executed in raw:
        e = t(ev)
        cp = next_checkpoint_interval(e, interval)
        manual.append((cp - e).total_seconds())
    manual = np.array(manual)
    med_m = np.median(manual)
    red = (med_m - med_a) / med_m * 100 if med_m > 0 else 0
    try:
        _, p = stats.wilcoxon(manual, mtta_auto_arr, alternative="greater")
        p_str = f"{p:.2e}"
    except Exception:
        p_str = "N/A"
    marca = ""
    if punto_equilibrio is None and red > 0:
        punto_equilibrio = interval
    # imprimir TODAS las filas de la grilla (el tribunal pidió la grilla completa)
    print(f"{interval:>8}min | {med_m/60:>10.2f}min | {red:>+8.1f}% | {p_str:>22}")

print("-" * 62)
print("NOTA: la reducción NO es monótona con el intervalo. Esto refleja el calendario")
print("de generación de los ataques (concentrados en una fase fija del ciclo del Cron),")
print("no una propiedad del sistema. Ver §13.3 de la tesis para la interpretación correcta")
print("y la referencia estructural bajo llegadas uniformes.")

# Referencia estructural bajo LLEGADAS UNIFORMES (hallazgo T1 / §13.3):
#   Si los eventos llegaran uniformemente dentro del ciclo de revisión, la espera
#   hasta el próximo punto de control sería uniforme en [0, T], con mediana T/2.
#   Entonces la mediana del MTTA manual sería T*60/2 s y la reducción teórica es:
#       red(T) = (T*30 - mediana_auto) / (T*30) * 100
#   Esta curva SÍ es monótona creciente; es el contraste que muestra que la forma
#   quebrada de la curva empírica proviene del calendario, no del sistema.
def reduccion_referencia_uniforme(interval_min, mediana_auto_s=med_a):
    med_manual_teorica = interval_min * 60 / 2.0   # = interval*30 s
    return (med_manual_teorica - mediana_auto_s) / med_manual_teorica * 100

print("\nReferencia bajo llegadas uniformes (mediana manual teórica = T/2):")
print(f"{'Intervalo':>10} | {'Red. empírica':>13} | {'Red. referencia':>15}")
print("-" * 46)
for interval in range(5, 31):
    manual = np.array([
        (next_checkpoint_interval(t(ev), interval) - t(ev)).total_seconds()
        for _, _, ev, _, _ in raw
    ])
    red_emp = (np.median(manual) - med_a) / np.median(manual) * 100 if np.median(manual) > 0 else 0
    red_ref = reduccion_referencia_uniforme(interval)
    print(f"{interval:>8}min | {red_emp:>+12.1f}% | {red_ref:>+14.1f}%")
print("-" * 46)

# 8bis. ESTIMADOR DE HODGES-LEHMANN para los intervalos de 10 y 20 minutos.
#   Es el estimador que corresponde a la prueba de Wilcoxon (la pseudomediana:
#   mediana de los promedios de Walsh de las diferencias pareadas). Explica por
#   qué el Wilcoxon puede ser significativo aunque la DIFERENCIA DE MEDIANAS sea
#   negativa: son dos estadísticos distintos. Ver §13.3 de la tesis.
print("\n" + "=" * 70)
print("ESTIMADOR DE HODGES-LEHMANN (pseudomediana de las diferencias pareadas)")
print("=" * 70)

def hodges_lehmann(diffs):
    n = len(diffs)
    walsh = [(diffs[i] + diffs[j]) / 2 for i in range(n) for j in range(i, n)]
    return np.median(walsh)

for iv in [10, 20]:
    manual = np.array([
        (next_checkpoint_interval(t(ev), iv) - t(ev)).total_seconds()
        for _, _, ev, _, _ in raw
    ])
    diff = manual - mtta_auto_arr  # positivo = sistema automatizado más rápido
    hl = hodges_lehmann(diff)
    med_diff = np.median(diff)
    _, p = stats.wilcoxon(manual, mtta_auto_arr, alternative="greater")
    favorables = int(np.sum(diff > 0)); desfav = int(np.sum(diff < 0))
    # IC del estimador de Hodges-Lehmann por el método de Wilcoxon (percentiles de los promedios de Walsh)
    walsh_sorted = np.sort([(diff[i]+diff[j])/2 for i in range(len(diff)) for j in range(i, len(diff))])
    nw = len(walsh_sorted)
    # IC 95% aproximado: percentiles 2.5 y 97.5 de los promedios de Walsh
    hl_low = walsh_sorted[int(0.025*nw)]; hl_high = walsh_sorted[int(0.975*nw)]
    print(f"{iv} min: diferencia de medianas={np.median(manual)-np.median(mtta_auto_arr):+.1f}s | "
          f"mediana de diferencias pareadas={med_diff:+.1f}s | "
          f"Hodges-Lehmann={hl:+.1f}s [IC95%: {hl_low:+.1f}, {hl_high:+.1f}] | "
          f"signos: {favorables} a favor / {desfav} en contra | p(dir H1)={p:.4f}")
print("A los 10 min, pese a una diferencia de medianas negativa, el H-L es positivo")
print("(+103,9 s). ATENCIÓN: esto NO significa que la mayoría de los pares favorezca")
print("al sistema (de hecho, 24 favorables vs 36 desfavorables). Significa que la")
print("mayoría de los PROMEDIOS DE WALSH son positivos: las diferencias favorables son")
print("de mayor magnitud y ocupan los rangos más altos de la prueba de Wilcoxon.")
print()
print("NOTA sobre coherencia IC/p (hallazgo T1): el IC del estimador de Hodges-Lehmann")
print("es BILATERAL al 95 % (percentiles 2,5 y 97,5 de los promedios de Walsh), por eso")
print("a 10 min incluye el cero. El p = 0,0333 es UNILATERAL (dirección de H1: sistema")
print("más rápido). No son contradictorios: miden cosas distintas (un intervalo de dos")
print("colas frente a una prueba de una cola). A 20 min ambos coinciden en el signo.")

# 7. BOXPLOTS — MTTA y MTTR, control (manual) vs. experimental (automatizado)
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

def _boxplot(ax, data, etiquetas, **kw):
    """Boxplot compatible con matplotlib viejo (labels=) y nuevo (tick_labels=)."""
    bp = ax.boxplot(data, patch_artist=True, **kw)
    ax.set_xticks(range(1, len(etiquetas) + 1))
    ax.set_xticklabels(etiquetas)
    return bp

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

_boxplot(axes[0],
    [np.array(mtta_manual_all) / 60, np.array(mtta_auto_all) / 60],
    ["Control\n(calculado)", "Experimental\n(n8n activo)"],
    boxprops=dict(facecolor="#f4a582"),
)
axes[0].set_ylabel("MTTA (minutos)")
axes[0].set_title(f"MTTA — N={res_mtta['n']} pares\np={res_mtta['p']:.2e}")
axes[0].grid(axis="y", alpha=0.3)

_boxplot(axes[1],
    [np.array(mttr_manual_all) / 60, np.array(mttr_auto_all) / 60],
    ["Control\n(calculado)", "Experimental\n(n8n activo)"],
    boxprops=dict(facecolor="#92c5de"),
)
axes[1].set_ylabel("MTTR (minutos)")
axes[1].set_title(f"MTTR — N={res_mttr['n']} pares (RD-1 a RD-5)\np={res_mttr['p']:.2e}")
axes[1].grid(axis="y", alpha=0.3)

fig.suptitle("Comparación fase de control vs. fase experimental — Laboratorio SOC n8n", fontsize=12)
fig.tight_layout()
fig.savefig("boxplot_mtta_mttr.png", dpi=150)
print("Gráfico generado: boxplot_mtta_mttr.png")

# Boxplot adicional: MTTA desagregado por regla, ambas condiciones
fig2, ax2 = plt.subplots(figsize=(11, 5.5))
reglas = ["RD-1", "RD-2", "RD-3", "RD-4", "RD-5", "RD-6"]
positions_auto = np.arange(len(reglas)) * 3
positions_manual = positions_auto + 1

data_auto = [[r["mtta_auto"] / 60 for r in rows if r["regla"] == rg] for rg in reglas]
data_manual = [[r["mtta_manual"] / 60 for r in rows if r["regla"] == rg] for rg in reglas]

bp1 = ax2.boxplot(data_auto, positions=positions_auto, widths=0.8, patch_artist=True,
                   boxprops=dict(facecolor="#f4a582"))
bp2 = ax2.boxplot(data_manual, positions=positions_manual, widths=0.8, patch_artist=True,
                   boxprops=dict(facecolor="#92c5de"))

ax2.set_xticks(positions_auto + 0.5)
ax2.set_xticklabels(reglas)
ax2.set_ylabel("MTTA (minutos)")
ax2.set_title("MTTA por regla — experimental (naranja) vs. control calculado (celeste)")
ax2.legend([bp1["boxes"][0], bp2["boxes"][0]], ["Experimental (n8n)", "Control (calculado)"], loc="upper left")
ax2.grid(axis="y", alpha=0.3)
fig2.tight_layout()
fig2.savefig("boxplot_mtta_por_regla.png", dpi=150)
print("Gráfico generado: boxplot_mtta_por_regla.png")

# ---------------------------------------------------------------------------
# 9. FIGURA 6 — Análisis de sensibilidad del brazo de control (hallazgo T1)
#    Eje x NUMÉRICO y proporcional (5 a 30 min), grilla completa punto a punto,
#    y la CURVA DE REFERENCIA bajo llegadas uniformes superpuesta. El contraste
#    entre la curva empírica (quebrada) y la de referencia (monótona) muestra que
#    la no-monotonía proviene del calendario de generación, no del sistema.
# ---------------------------------------------------------------------------
intervalos = list(range(5, 31))
red_emp = []
for interval in intervalos:
    manual = np.array([
        (next_checkpoint_interval(t(ev), interval) - t(ev)).total_seconds()
        for _, _, ev, _, _ in raw
    ])
    mm = np.median(manual)
    red_emp.append((mm - med_a) / mm * 100 if mm > 0 else 0)
red_ref = [reduccion_referencia_uniforme(iv) for iv in intervalos]

fig6, ax6 = plt.subplots(figsize=(10, 5.5))
# Curva de referencia (monótona) bajo llegadas uniformes
ax6.plot(intervalos, red_ref, color="#2166ac", lw=2, ls="--",
         label="Referencia bajo llegadas uniformes (mediana manual = T/2)")
# Curva empírica, punto a punto, en el eje numérico real
ax6.plot(intervalos, red_emp, color="#b2182b", lw=1.5, marker="o", ms=5,
         label="Reducción empírica observada (calendario real de la campaña)")
# Marcas de referencia: 20 min (configuración declarada) y línea del 0 %
ax6.axhline(0, color="#777777", lw=0.9)
ax6.axvline(20, color="#777777", lw=0.9, ls=":")
ax6.annotate("Intervalo declarado\n(20 min): +50,6 %",
             xy=(20, 50.6), xytext=(21.5, 18),
             fontsize=9, color="#333333",
             arrowprops=dict(arrowstyle="->", color="#333333", lw=0.8))
ax6.set_xlabel("Intervalo de revisión manual asumido (minutos)")
ax6.set_ylabel("Reducción del MTTA mediano (%)")
ax6.set_title("Figura 6 — Sensibilidad de la reducción del MTTA al intervalo de revisión\n"
              "Curva empírica vs. referencia estructural bajo llegadas uniformes")
ax6.set_xticks(intervalos)
ax6.tick_params(axis="x", labelsize=8)
ax6.grid(alpha=0.3)
ax6.legend(loc="lower right", fontsize=9)
fig6.tight_layout()
fig6.savefig("Figura6-Sensibilidad-corregida.png", dpi=150)
print("Gráfico generado: Figura6-Sensibilidad-corregida.png")
