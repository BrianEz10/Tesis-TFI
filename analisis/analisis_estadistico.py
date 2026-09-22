"""
Análisis estadístico — Laboratorio SOC Académico con n8n
Comparación fase de control (calculada) vs. fase experimental (medida) sobre 60 pares reales
(10 repeticiones x 6 reglas de detección: RD-1 a RD-6)

Datos crudos: exportados de las tablas `alerts` y `playbook_runs` de PostgreSQL durante
la sesión de medición del 25/8 al 14/9 de 2026. RD-6 no genera `executed_at` (regla
fire-and-forget, sin bloqueo automático), por lo que se excluye del análisis de MTTR.

Metodología fase de control: no se ejecutó en vivo. Se calcula matemáticamente a partir
del mismo `event_timestamp` real de cada ataque, asumiendo un analista que revisa la cola
de alertas cada 20 minutos (puntos de revisión en :00, :20, :40 de cada hora) más un tiempo
fijo de respuesta manual de 2.5 minutos (150s) una vez detectado.
"""

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

# Exportar CSV crudo (para anexo técnico / verificación del tribunal)
with open("/home/claude/dataset_pareado.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["regla", "id", "mtta_auto", "mtta_manual", "mttr_auto", "mttr_manual"])
    writer.writeheader()
    for r in rows:
        writer.writerow(r)

# ---------------------------------------------------------------------------
# 4. ANÁLISIS ESTADÍSTICO — MTTA (60 pares) y MTTR (50 pares, sin RD-6)
# ---------------------------------------------------------------------------
def wilcoxon_report(name, auto_vals, manual_vals, n_bootstrap=5000, seed=42):
    auto = np.array(auto_vals)
    manual = np.array(manual_vals)
    n = len(auto)
    diff = manual - auto  # positivo = automatizado más rápido

    stat, p = stats.wilcoxon(manual, auto, alternative="greater")

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
    print(f"Wilcoxon signed-rank: W={stat:.1f}, p={p:.10f}")
    print(f"Z (aprox. normal, calculado directo del estadístico): {z:.3f}")
    print(f"Tamaño del efecto r = Z/sqrt(N): {r:.3f}")
    print(f"IC 95% bootstrap de la diferencia de medianas: [{ci_low:.1f}s, {ci_high:.1f}s]")
    contains = ci_low <= diff_medianas <= ci_high
    print(f"¿El IC contiene la diferencia observada?: {contains}")
    print(f"Reducción de las medianas: {reduction_pct:.1f}%")
    return {
        "n": n, "median_auto": np.median(auto), "median_manual": np.median(manual),
        "median_diff": diff_medianas, "W": stat, "p": p, "z": z, "r": r,
        "ci_low": ci_low, "ci_high": ci_high, "reduction_pct": reduction_pct
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
# 5. MATRIZ DE CONFUSIÓN Y MÉTRICAS DE CLASIFICACIÓN
#    A partir de la ronda TN/FP/FN documentada (18 casos adicionales + 60 TP)
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("MATRIZ DE CONFUSIÓN Y MÉTRICAS DE CLASIFICACIÓN")
print("=" * 70)

TP = 60  # las 60 repeticiones originales, todas detectadas correctamente

# Solo RD-1, RD-2, RD-4, RD-6 tienen TN/FP definidos (RD-3 y RD-5 no aplican por diseño)
TN = 4   # 1 por regla en RD-1, RD-2, RD-4, RD-6
FP = 4   # 1 por regla en RD-1, RD-2, RD-4, RD-6
FN = 6   # 1 por regla en las 6 reglas (todas tienen caso FN)

precision = TP / (TP + FP)
recall = TP / (TP + FN)
f1 = 2 * precision * recall / (precision + recall)
fpr = FP / (FP + TN)

print(f"TP={TP}, TN={TN}, FP={FP}, FN={FN}")
print(f"Precisión: {precision:.4f}")
print(f"Recall (sensibilidad): {recall:.4f}")
print(f"F1-score: {f1:.4f}")
print(f"FPR (tasa de falsos positivos): {fpr:.4f}")
print("\n⚠️  ADVERTENCIA METODOLÓGICA IMPORTANTE:")
print("TN y FP se estiman sobre una muestra muy pequeña (4 casos cada uno, 1 por regla")
print("en las 4 reglas donde aplica). Cualquier intervalo de confianza calculado sobre")
print("n=8 (FP+TN) va a ser extremadamente ancho y poco informativo. Esto debe declararse")
print("como limitación explícita en la tesis, NO ocultarse ni maquillarse con IC angostos")
print("artificiales (el error exacto que cometió la versión anterior del trabajo).")

# Intervalo de Wilson para la FPR, honesto sobre lo ancho que va a salir
def wilson_ci(successes, n, z=1.96):
    if n == 0:
        return (None, None)
    p_hat = successes / n
    denom = 1 + z**2 / n
    center = (p_hat + z**2 / (2*n)) / denom
    margin = (z * np.sqrt(p_hat*(1-p_hat)/n + z**2/(4*n**2))) / denom
    return (max(0, center - margin), min(1, center + margin))

fpr_ci = wilson_ci(FP, FP + TN)
precision_ci = wilson_ci(TP, TP + FP)
recall_ci = wilson_ci(TP, TP + FN)
print(f"\nIC 95% Wilson FPR: [{fpr_ci[0]:.3f}, {fpr_ci[1]:.3f}]  <- MUY ancho, n=8")
print(f"IC 95% Wilson Precisión: [{precision_ci[0]:.3f}, {precision_ci[1]:.3f}]")
print(f"IC 95% Wilson Recall: [{recall_ci[0]:.3f}, {recall_ci[1]:.3f}]")

# ---------------------------------------------------------------------------
# 6. GUARDAR RESUMEN EN CSV
# ---------------------------------------------------------------------------
with open("/home/claude/resumen_resultados.csv", "w", newline="") as f:
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
    writer.writerow(["TP", TP]); writer.writerow(["TN", TN])
    writer.writerow(["FP", FP]); writer.writerow(["FN", FN])
    writer.writerow(["precision", f"{precision:.4f}"])
    writer.writerow(["recall", f"{recall:.4f}"])
    writer.writerow(["f1", f"{f1:.4f}"])
    writer.writerow(["fpr", f"{fpr:.4f}"])

print("\n\nArchivos generados: dataset_pareado.csv, resumen_resultados.csv")

# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# 8. ANÁLISIS DE SENSIBILIDAD DEL BRAZO DE CONTROL
#    Cómo varía la reducción del MTTA según el intervalo de revisión manual asumido
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
for interval in range(5, 26):
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
        marca = "  <- punto de equilibrio (el sistema pasa a ser más rápido)"
    # imprimir solo algunos para no saturar, pero marcar el equilibrio
    if interval in (5, 10, 15, 20, 25) or marca:
        print(f"{interval:>8}min | {med_m/60:>10.2f}min | {red:>+8.1f}% | {p_str:>22}{marca}")

print("-" * 62)
if punto_equilibrio:
    print(f"PUNTO DE EQUILIBRIO: con revisión manual cada >= {punto_equilibrio} min, la automatización es más rápida.")
    print(f"Por debajo de ese intervalo, el sistema no aporta ventaja de tiempo (comparte el piso del cron de 5 min).")

# 7. BOXPLOTS — MTTA y MTTR, control (manual) vs. experimental (automatizado)
# ---------------------------------------------------------------------------
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 2, figsize=(11, 5))

axes[0].boxplot(
    [np.array(mtta_manual_all) / 60, np.array(mtta_auto_all) / 60],
    labels=["Control\n(calculado)", "Experimental\n(n8n activo)"],
    patch_artist=True,
    boxprops=dict(facecolor="#f4a582"),
)
axes[0].set_ylabel("MTTA (minutos)")
axes[0].set_title(f"MTTA — N={res_mtta['n']} pares\np={res_mtta['p']:.2e}")
axes[0].grid(axis="y", alpha=0.3)

axes[1].boxplot(
    [np.array(mttr_manual_all) / 60, np.array(mttr_auto_all) / 60],
    labels=["Control\n(calculado)", "Experimental\n(n8n activo)"],
    patch_artist=True,
    boxprops=dict(facecolor="#92c5de"),
)
axes[1].set_ylabel("MTTR (minutos)")
axes[1].set_title(f"MTTR — N={res_mttr['n']} pares (RD-1 a RD-5)\np={res_mttr['p']:.2e}")
axes[1].grid(axis="y", alpha=0.3)

fig.suptitle("Comparación fase de control vs. fase experimental — Laboratorio SOC n8n", fontsize=12)
fig.tight_layout()
fig.savefig("/home/claude/boxplot_mtta_mttr.png", dpi=150)
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
fig2.savefig("/home/claude/boxplot_mtta_por_regla.png", dpi=150)
print("Gráfico generado: boxplot_mtta_por_regla.png")
