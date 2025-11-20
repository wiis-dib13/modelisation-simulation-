def mm1(lambd, mu):
    rho = lambd / mu
    if rho >= 1:
        raise ValueError("Système instable : ρ doit être < 1")

    N = rho / (1 - rho)
    NF = rho**2 / (1 - rho)
    W = 1 / (mu - lambd)
    Wq = rho / (mu - lambd)

    return {
        "rho": rho,
        "N": N,
        "NF": NF,
        "W": W,
        "Wq": Wq,
    }

def mm1k(lambd, mu, K):
    rho = lambd / mu

    # Probabilité d'état 0
    P0 = (1 - rho) / (1 - rho**(K+1))

    # Probabilités Pn
    P = [P0 * rho**n for n in range(K+1)]

    # L = somme n * Pn
    L = sum(n * P[n] for n in range(K+1))

    # Probabilité de blocage
    P_block = P[K]

    # Taux effectif d’arrivée
    lambda_eff = lambd * (1 - P_block)

    # Temps moyen dans le système
    W = L / lambda_eff

    return {
        "rho": rho,
        "L": L,
        "P_block": P_block,
        "lambda_eff": lambda_eff,
        "W": W
    }

import numpy as np
mus = 1
rhos = np.arange(0.5, 0.951, 0.05)

results = []
for rho in rhos:
    lambd = rho * mus
    out = mm1(lambd, mus)
    results.append((rho, out["L"], out["W"]))

for r, L, W in results:
    print(f"ρ={r:.2f}  →  L={L:.3f}, W={W:.3f}")


        
#simulation
import  random, statistics

def client(env, mu, serveur, temps_sejour):
    arrivee = env.now
    with serveur.request() as req:
        yield req
        # service
        duree_service = random.expovariate(mu)
        yield env.timeout(duree_service)
        temps_sejour.append(env.now - arrivee)


#simulation
def simulate_mm1(lambd, mu, simulation_time=20000):
    env = simpy.Environment()
    serveur = simpy.Resource(env, capacity=1)
    temps_sejour = []

    def arrival_process(env):
        while True:
            inter_arr = random.expovariate(lambd)
            yield env.timeout(inter_arr)
            env.process(client(env, mu, serveur, temps_sejour))

    env.process(arrival_process(env))
    env.run(until=simulation_time)

    return statistics.mean(temps_sejour)

lambd = 0.8
mu = 1

W_sim = simulate_mm1(lambd, mu)
W_theo = 1 / (mu - lambd)

print("Temps moyen simulé  :", W_sim)
print("Temps moyen théorique :", W_theo)

#question 3 
import random
import math


lam = 4     # taux d'arrivée
mu = 5      # taux de service
N = 100000  # nombre de clients

# simulateur
t = 0
queue = 0
wait_times = []

server_free_at = 0

for _ in range(N):
    # temps entre arrivées
    t += random.expovariate(lam)

    # service
    service_time = random.expovariate(mu)

    # si serveur libre avant l'arrivée → pas d'attente
    if t >= server_free_at:
        start_service = t
    else:
        start_service = server_free_at

    wait_times.append(start_service - t)
    server_free_at = start_service + service_time

# Moyenne simulée
Wq_sim = sum(wait_times) / len(wait_times)
Lq_sim = lam * Wq_sim  # Little

print("Simulation :")
print("Wq (simulé) =", Wq_sim)
print("Lq (simulé) =", Lq_sim)

