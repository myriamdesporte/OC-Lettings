## Résumé

Site web d'Orange County Lettings

## Développement local

### Prérequis

- Compte GitHub avec accès en lecture à ce repository
- Git CLI
- SQLite3 CLI
- Interpréteur Python, version 3.6 ou supérieure

Dans le reste de la documentation sur le développement local, il est supposé que la commande `python` de votre OS shell exécute l'interpréteur Python ci-dessus (à moins qu'un environnement virtuel ne soit activé).

### macOS / Linux

#### Cloner le repository

- `cd /path/to/put/project/in`
- `git clone https://github.com/OpenClassrooms-Student-Center/Python-OC-Lettings-FR.git`

#### Créer l'environnement virtuel

- `cd /path/to/Python-OC-Lettings-FR`
- `python -m venv venv`
- `apt-get install python3-venv` (Si l'étape précédente comporte des erreurs avec un paquet non trouvé sur Ubuntu)
- Activer l'environnement `source venv/bin/activate`
- Confirmer que la commande `python` exécute l'interpréteur Python dans l'environnement virtuel
`which python`
- Confirmer que la version de l'interpréteur Python est la version 3.6 ou supérieure `python --version`
- Confirmer que la commande `pip` exécute l'exécutable pip dans l'environnement virtuel, `which pip`
- Pour désactiver l'environnement, `deactivate`

#### Exécuter le site

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pip install --requirement requirements.txt`
- `python manage.py runserver`
- Aller sur `http://localhost:8000` dans un navigateur.
- Confirmer que le site fonctionne et qu'il est possible de naviguer (vous devriez voir plusieurs profils et locations).

#### Linting

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `flake8`

#### Tests unitaires

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest`

#### Couverture de test

- `cd /path/to/Python-OC-Lettings-FR`
- `source venv/bin/activate`
- `pytest --cov` (la commande échoue si la couverture est inférieure à 80 %)
- Rapport HTML : `pytest --cov --cov-report=html`, puis ouvrir `htmlcov/index.html`

#### Base de données

- `cd /path/to/Python-OC-Lettings-FR`
- Ouvrir une session shell `sqlite3`
- Se connecter à la base de données `.open oc-lettings-site.sqlite3`
- Afficher les tables dans la base de données `.tables`
- Afficher les colonnes dans le tableau des profils, `pragma table_info(profiles_profile);`
- Lancer une requête sur la table des profils, `select user_id, favorite_city from
  profiles_profile where favorite_city like 'B%';`
- `.quit` pour quitter

#### Panel d'administration

- Aller sur `http://localhost:8000/admin`
- Connectez-vous avec l'utilisateur `admin`, mot de passe `Abc1234!`

#### Variables d'environnement

Les données sensibles ne sont pas stockées dans le code : elles sont lues dans des variables d'environnement, chargées depuis un fichier `.env` à la racine du projet (ignoré par git).

- `cp env.example .env`
- Compléter les valeurs dans `.env` :

| Variable | Rôle | Valeur par défaut |
|----------|------|-------------------|
| `SENTRY_DSN` | Clé (DSN) du projet Sentry. Vide : Sentry désactivé | (vide) |
| `SENTRY_ENVIRONMENT` | Nom de l'environnement affiché dans Sentry | `development` |
| `SENTRY_TRACES_SAMPLE_RATE` | Part des requêtes suivies en performance (0 à 1) | `0` |
| `LOG_LEVEL` | Niveau de log des applications du projet | `INFO` |

#### Surveillance avec Sentry et journalisation

Mise en place de Sentry :

- Créer un compte sur https://sentry.io, puis un projet de plateforme **Django**
- Copier le DSN du projet (Settings > Projects > *projet* > Client Keys (DSN)) dans la variable `SENTRY_DSN` du fichier `.env`
- Relancer le serveur : `python manage.py runserver`

Fonctionnement des logs (module `logging`, configuré dans `LOGGING` de `oc_lettings_site/settings.py`) :

- Les logs sont affichés dans la console (niveau `LOG_LEVEL` pour les apps `lettings`, `profiles` et `oc_lettings_site`, `WARNING` pour Django)
- Logs `INFO` et plus : envoyés dans l'onglet **Logs** de Sentry et joints aux erreurs
- Logs `ERROR` et plus, et exceptions non gérées : créent une **issue** dans Sentry
- Sentry n'est jamais activé pendant les tests (`pytest`)

Vérifier l'intégration (uniquement avec `DEBUG = True`) :

- Aller sur `http://localhost:8000/sentry-debug/` : la page provoque volontairement une erreur (division par zéro)
- Une issue `ZeroDivisionError` et un log `Sentry test` apparaissent dans Sentry après quelques secondes

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`
