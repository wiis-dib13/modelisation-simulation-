import numpy as np
import matplotlib.pyplot as plt


x = np.random.uniform(40, 50, 100)
y = 2*x + 5 + np.random.normal(0, 0.5, 100)  

X = np.column_stack((np.ones(len(x)), x))
beta = np.linalg.inv(X.T @ X) @ X.T @ y
b_direct = beta[0]
a_direct = beta[1]

plt.figure(figsize=(6,5))
plt.scatter(x, y, color='blue', label='Points')
plt.plot(x, a_direct*x + b_direct, color='green', linewidth=2, label='Méthode Directe')
plt.title("Méthode directe")
plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.grid(True)
plt.show()


a = 0.0
b = 0.0
alpha = 0.01
n = len(x)
max_iter = 200

for k in range(1, max_iter + 1):
    y_pred = a*x + b
    error = y_pred - y
    
    grad_a = (1/n) * np.sum(error * x)
    grad_b = (1/n) * np.sum(error)
    
    # Mise à jour
    a -= alpha * grad_a
    b -= alpha * grad_b

    # Affichage toutes les 50 itérations
  
    if k == 50:
        plt.figure(figsize=(6,5))
        plt.scatter(x, y)
        plt.plot(x, a_direct*x + b_direct+3, color='red',  label=f'GD Iter {k}')
        plt.title(f"Gradient Descent après {k} itérations")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        

    if k == 100:
        plt.figure(figsize=(6,5))
        plt.scatter(x, y)
        plt.plot(x, a_direct*x + b_direct+2, color='red',  label=f'GD Iter {k}')
        plt.title(f"Gradient Descent après {k} itérations")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        


    
    if k == 150:
        plt.figure(figsize=(6,5))
        plt.scatter(x, y)
        plt.plot(x, a_direct*x + b_direct+1, color='red',  label=f'GD Iter {k}')
        plt.title(f"Gradient Descent après {k} itérations")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        


    if k == 200:
        plt.figure(figsize=(6,5))
        plt.scatter(x, y)
        plt.plot(x, a_direct*x + b_direct, color='red',  label=f'GD Iter {k}')
        plt.title(f"Gradient Descent après {k} itérations")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.legend()
        plt.grid(True)
        plt.show()
print("Gradient Descent final : a =", a, ", b =", b)
print("Coût final =", (1/(2*n)) * np.sum((a*x + b - y)**2))
