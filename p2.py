import matplotlib.pyplot as plt

# -------------------------------
# Données des processus
# -------------------------------
processus = [
    ("P1", 2, 0),
    ("P2", 3, 3),
    ("P3", 2, 5),
    ("P4", 1, 10)
]

# Tri par date d'arrivée
processus.sort(key=lambda x: x[2])

# -------------------------------
# Partie 1a : Simulation FIFO et diagramme de Gantt
# -------------------------------
t = 0
gantt_data = []
fin_processus = []  # pour chaque processus : (nom, arrivée, début, fin)

for p, duree, arrivee in processus:
    # CPU idle si le processus arrive plus tard
    if t < arrivee:
        gantt_data.append(("IDLE", t, arrivee - t))
        t = arrivee
    debut = t
    fin = t + duree
    gantt_data.append((p, debut, duree))
    fin_processus.append((p, arrivee, debut, fin))
    t = fin

# Tracé du Gantt
fig, ax = plt.subplots(figsize=(10, 3))
y_pos = 0
for p, start, duree in gantt_data:
    color = "purple" if p == "IDLE" else "pink"
    ax.barh(y_pos, duree, left=start, height=0.5, color=color, edgecolor="black")
    ax.text(start + duree/2, y_pos, p, ha="center", va="center", color="black")
    y_pos += 1

ax.set_xlabel("Temps")
ax.set_yticks([])
ax.set_title("Diagramme de Gantt FIFO (FCFS)")
ax.set_xlim(0, t + 1)
plt.show()

# -------------------------------
# Partie 1b : Calcul des indicateurs simulés
# -------------------------------
max_time = fin_processus[-1][3]  # dernière fin
system_counts = []
wait_counts = []

for sec in range(max_time + 1):
    in_system = 0
    in_wait = 0
    for p, arrivee, debut, fin in fin_processus:
        if arrivee <= sec < fin:
            in_system += 1
            if sec < debut:
                in_wait += 1
    system_counts.append(in_system)
    wait_counts.append(in_wait)

L_system = sum(system_counts) / len(system_counts)
L_wait = sum(wait_counts) / len(wait_counts)
W = sum(fin - arrivee for _, arrivee, _, fin in fin_processus) / len(fin_processus)
Wq = sum(debut - arrivee for _, arrivee, debut, _ in fin_processus) / len(fin_processus)

print("\n===== Partie 1 : indicateurs simulés =====")
print(f"Nombre moyen de processus dans le système : {L_system:.2f}")
print(f"Nombre moyen de processus en attente      : {L_wait:.2f}")
print(f"Temps de réponse moyen                     : {W:.2f}")
print(f"Temps d'attente moyen                      : {Wq:.2f}")

# -------------------------------
# Partie 2 : Calcul théorique M/M/1
# -------------------------------
n_processus = len(processus)
fin_last = max(arrivee + duree for _, duree, arrivee in processus)
lambda_rate = n_processus / fin_last  # taux d'arrivée
duree_moyenne = sum(duree for _, duree, _ in processus) / n_processus
mu_rate = 1 / duree_moyenne           # taux de service
rho = lambda_rate / mu_rate           # intensité de trafic

L_th = rho / (1 - rho)
Lq_th = rho**2 / (1 - rho)
W_th = 1 / (mu_rate - lambda_rate)
Wq_th = lambda_rate / (mu_rate * (mu_rate - lambda_rate))

print("\n===== Partie 2 : indicateurs théoriques M/M/1 =====")
print(f"Taux d'arrivée λ       : {lambda_rate:.3f} processus/unité")
print(f"Taux de service μ      : {mu_rate:.3f} processus/unité")
print(f"Intensité de trafic ρ  : {rho:.3f}")
print(f"Nombre moyen dans le système L : {L_th:.2f}")
print(f"Nombre moyen en attente Lq     : {Lq_th:.2f}")
print(f"Temps de réponse moyen W        : {W_th:.2f}")
print(f"Temps d'attente moyen Wq        : {Wq_th:.2f}")
