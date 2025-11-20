import simpy
import random
import matplotlib.pyplot as plt
import statistics

# -------------------------------
# Données des processus
# -------------------------------
processus = [
    ("P1", 2, 0),
    ("P2", 3, 3),
    ("P3", 2, 5),
    ("P4", 1, 10)
]

# Simulation FIFO M/M/1
def client(env, mu, serveur, temps_sejour, name):
    arrivee = env.now
    with serveur.request() as req:
        yield req
        # service
        duree_service = random.expovariate(1/mu)
        yield env.timeout(duree_service)
        temps_sejour.append((name, arrivee, env.now))

def simulate_mm1(processus, simulation_time=50):
    env = simpy.Environment()
    serveur = simpy.Resource(env, capacity=1)
    temps_sejour = []

    def arrival_process(env):
        for p, duree, arrivee in processus:
            yield env.timeout(max(0, arrivee - env.now))
            env.process(client(env, duree, serveur, temps_sejour, p))

    env.process(arrival_process(env))
    env.run(until=simulation_time)
    return temps_sejour

# -------------------------------
# Lancer la simulation
# -------------------------------
temps_sejour = simulate_mm1(processus, simulation_time=50)

# -------------------------------
# Partie 1b : calcul des indicateurs simulés
# -------------------------------
# Nombre moyen de processus dans le système et en attente
max_time = int(max(finish for _, _, finish in temps_sejour)) + 1
system_counts = []
wait_counts = []

for sec in range(max_time + 1):
    in_system = 0
    in_wait = 0
    for name, arrivee, fin in temps_sejour:
        if arrivee <= sec < fin:
            in_system += 1
            # en attente si pas encore commencé le service
            if sec < arrivee:
                in_wait += 1
    system_counts.append(in_system)
    wait_counts.append(in_wait)

L_system = sum(system_counts)/len(system_counts)
L_wait = sum(wait_counts)/len(wait_counts)

# Temps de réponse et temps d'attente moyen
W = sum(fin - arrivee for _, arrivee, fin in temps_sejour)/len(temps_sejour)
Wq = sum(arrivee - arrivee for _, arrivee, _ in temps_sejour)/len(temps_sejour)  # ici temps d'attente =0 car FIFO sans file

# -------------------------------
# Affichage des résultats simulés
# -------------------------------
print("===== Partie 1 : résultats simulés =====")
print(f"Nombre moyen dans le système : {L_system:.2f}")
print(f"Nombre moyen en attente      : {L_wait:.2f}")
print(f"Temps de réponse moyen       : {W:.2f}")
print(f"Temps d'attente moyen        : {Wq:.2f}")

# -------------------------------
# Partie 2 : calcul théorique M/M/1
# -------------------------------
n_processus = len(processus)
fin_last = max(arrivee + duree for _, duree, arrivee in processus)
lambda_rate = n_processus / fin_last
duree_moyenne = sum(duree for _, duree, _ in processus)/n_processus
mu_rate = 1/duree_moyenne
rho = lambda_rate / mu_rate

L_th = rho / (1 - rho)
Lq_th = rho**2 / (1 - rho)
W_th = 1 / (mu_rate - lambda_rate)
Wq_th = lambda_rate / (mu_rate*(mu_rate - lambda_rate))

print("\n===== Partie 2 : résultats théoriques M/M/1 =====")
print(f"Taux d'arrivée λ             : {lambda_rate:.3f}")
print(f"Taux de service μ            : {mu_rate:.3f}")
print(f"Intensité de trafic ρ        : {rho:.3f}")
print(f"Nombre moyen dans le système : {L_th:.2f}")
print(f"Nombre moyen en attente      : {Lq_th:.2f}")
print(f"Temps de réponse moyen       : {W_th:.2f}")
print(f"Temps d'attente moyen        : {Wq_th:.2f}")

# -------------------------------
# Optionnel : graphique du nombre de processus dans le système
# -------------------------------
plt.figure(figsize=(10,4))
plt.plot(range(max_time + 1), system_counts, drawstyle="steps-post", label="Dans le système")
plt.plot(range(max_time + 1), wait_counts, drawstyle="steps-post", label="En attente")
plt.xlabel("Temps")
plt.ylabel("Nombre de processus")
plt.title("Simulation M/M/1 style JMT")
plt.legend()
plt.grid(True)
plt.show()
