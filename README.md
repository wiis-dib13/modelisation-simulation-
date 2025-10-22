# modelisation-simulation-
solutions des tps du module de modelisation et simulation (graphe de petrie)
## exo1
Développez un programme permettant de modéliser en mémoire la structure d'un système à l'aide des
réseaux de Pétri. Votre implémentation devra représenter :
- L'ensemble des composants du système
- Les interactions entre ces composants
Votre programme devra permettre de répondre aux requêtes suivantes sur les réseaux de Pétri :
a) Pour une place donnée, quelles sont ses transitions de sortie ?
b) Pour une place donnée, quelles sont ses transitions d'entrée ?
c) Pour une transition donnée, quelles sont ses places de sortie ?
d) Pour une transition donnée, quelles sont ses places d'entrée ?

## exo 2
a) Implémenter un algorithme de génération de l'arborescence des états atteignables, afin d'énumérer
exhaustivement tous les états dans lesquels le système peut évoluer via le formalisme des réseaux
de Pétri dans les deux cas suivants :
2/2
- Un réseau borné
- Un réseau non borné
b) Implémenter un algorithme qui permet de générer le graphe de transitions résultant de
l’arborescence des états atteignables ?

## exo3
Dans cette étude de cas il est demandé de modéliser le système de feux de circulation (feux tricolores)
d'un carrefour à deux tronçons à l'aide des réseaux de Pétri.
Travail à réaliser :
a) Modélisation
‑ Représenter les feux de circulation par un réseau de Pétri
‑ Décrire les différents scénarios de fonctionnement
b) Analyse comportementale
‑ Construire l'arborescence des états atteignables
‑ Identifier tous les états possibles du système
c) Vérification des propriétés
‑ Détecter les éventuels problèmes de famine (starvation)
‑ Identifier les risques d'interblocage 
