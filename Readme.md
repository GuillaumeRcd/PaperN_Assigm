# Application de Vérification de la Couverture Réseau

Cette application permet de vérifier la couverture réseau pour une adresse donnée en France. Elle affiche les opérateurs mobiles disponibles et indique s'ils proposent une couverture 2G, 3G ou 4G à proximité de l'adresse spécifiée.

## Prérequis

Assurez-vous d'avoir installé les dépendances nécessaires pour exécuter l'application. Vous pouvez les installer en utilisant le fichier `requirements.txt` fourni.

### Installation des dépendances du server

1. Accédez tout d'abord au server:
cd server

2. Puis installez les dépendances:
pip install -r requirements.txt

#### Installation des dépendances du de la partie client (frontend):
1. Accédez tout d'abord à la partie clien:
cd client

2. Puis installez les dépendances:
npm install

##### Utilisation
1. Commencez par démarrer le backend FastAPI :
cd server
uvicorn main:app --reload

Le backend sera accessible à l'adresse http://localhost:8000.

2. Ensuite, démarrez le frontend Vite + React:
cd client
npm run dev

Le frontend sera accessible à l'adresse http://localhost:5173.

3. Utilisez l'interface du frontend pour entrer une adresse et rechercher la couverture réseau.


