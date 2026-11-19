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
- `cp env.example .env` (à faire une seule fois, voir [Variables d'environnement](#variables-denvironnement))
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

| Variable | Rôle | Valeur par défaut   |
|----------|------|---------------------|
| `DJANGO_DEBUG` | Mode debug (`True` en local uniquement, jamais en production) | `False`             |
| `DJANGO_SECRET_KEY` | Clé secrète Django. Facultative si `DJANGO_DEBUG=True`, obligatoire sinon | (vide)  |
| `DJANGO_ALLOWED_HOSTS` | Noms de domaine autorisés, séparés par des virgules | `localhost,127.0.0.1` |
| `SENTRY_DSN` | Clé (DSN) du projet Sentry. Vide : Sentry désactivé | (vide)              |
| `SENTRY_ENVIRONMENT` | Nom de l'environnement affiché dans Sentry | `development`       |
| `SENTRY_TRACES_SAMPLE_RATE` | Part des requêtes suivies en performance (0 à 1) | `0`                 |
| `LOG_LEVEL` | Niveau de log des applications du projet | `INFO`              |

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

Vérifier l'intégration (uniquement avec `DJANGO_DEBUG=True`) :

- Aller sur `http://localhost:8000/sentry-debug/` : la page provoque volontairement une erreur (division par zéro)
- Une issue `ZeroDivisionError` et un log `Sentry test` apparaissent dans Sentry après quelques secondes

### Windows

Utilisation de PowerShell, comme ci-dessus sauf :

- Pour activer l'environnement virtuel, `.\venv\Scripts\Activate.ps1` 
- Remplacer `which <my-command>` par `(Get-Command <my-command>).Path`

## Déploiement

### Fonctionnement général

Le déploiement est automatisé par un pipeline CI/CD GitHub Actions (`.github/workflows/ci-cd.yml`), lancé à chaque `git push` :

1. **Lint et tests** (toutes les branches) : installation de Python 3.11 et des dépendances, `flake8`, puis `pytest --cov` (échec si la couverture est inférieure à 80 %).
2. **Conteneurisation** (branche `master` uniquement, si l'étape 1 a réussi) : construction de l'image Docker (`Dockerfile`) et envoi sur Docker Hub avec deux tags : le hash du commit et `latest`.
3. **Déploiement** (branche `master` uniquement, si l'étape 2 a réussi) : appel du *deploy hook* de Render, qui récupère l'image du commit sur Docker Hub et la met en service.

Sur les autres branches, seule l'étape 1 est exécutée.

Dans l'image, le site est servi par **Gunicorn** et les fichiers statiques (CSS, images, admin) par **WhiteNoise**, après un `collectstatic` exécuté à la construction de l'image.

### Configuration requise

- Un compte **Docker Hub** et un *access token* (Account settings > Personal access tokens, droits *Read & Write*)
- Un compte **Render**
- Les **secrets GitHub** suivants (Settings > Secrets and variables > Actions > New repository secret) :

| Secret | Contenu |
|--------|---------|
| `DOCKERHUB_USERNAME` | Nom d'utilisateur Docker Hub |
| `DOCKERHUB_TOKEN` | *Access token* Docker Hub |
| `RENDER_DEPLOY_HOOK_URL` | URL du *deploy hook* du service Render |

- Les **variables d'environnement du service Render** (onglet Environment) :

| Variable | Valeur |
|----------|--------|
| `DJANGO_SECRET_KEY` | Clé longue et aléatoire (voir la commande dans `env.example`) |
| `DJANGO_DEBUG` | `False` |
| `SENTRY_DSN` | DSN du projet Sentry |
| `SENTRY_ENVIRONMENT` | `production` |

`DJANGO_ALLOWED_HOSTS` n'est pas nécessaire sur Render : le nom de domaine public (`RENDER_EXTERNAL_HOSTNAME`) est ajouté automatiquement.

### Étapes de déploiement

Mise en place (une seule fois) :

1. Ajouter les secrets `DOCKERHUB_USERNAME` et `DOCKERHUB_TOKEN` dans GitHub.
2. Pousser sur `master` : les jobs de tests et de conteneurisation créent l'image `<utilisateur>/oc-lettings` sur Docker Hub (le job de déploiement échoue tant que le *deploy hook* n'existe pas, c'est normal).
3. Sur Render : **New > Web Service > Existing image**, image `docker.io/<utilisateur>/oc-lettings:latest`, offre *Free*, puis renseigner les variables d'environnement ci-dessus.
4. Dans le service Render, **Settings** : copier l'URL du **Deploy Hook** et l'ajouter dans le secret GitHub `RENDER_DEPLOY_HOOK_URL`. Vérifier que le déploiement automatique (*Auto-Deploy*) est désactivé : seul le pipeline déclenche les déploiements.

Déploiements suivants : fusionner ou pousser sur `master`, le pipeline fait le reste. Suivre l'avancement dans l'onglet **Actions** de GitHub, puis dans l'onglet **Events** du service Render.

### Lancer l'image en local avec Docker

Une seule commande récupère l'image sur Docker Hub et lance le site sur `http://localhost:8000` :

```bash
docker run --rm -p 8000:8000 -e DJANGO_SECRET_KEY=change-me <utilisateur>/oc-lettings:latest
```

Remplacer <utilisateur> par le nom d'utilisateur Docker Hub (le même que le secret `DOCKER_USERNAME`).

> **Mac avec puce Apple (M1, M2, M3...)** : le pipeline construit l'image pour des processeurs amd64.
> Ajouter `--platform linux/amd64` après `--rm` :
>
> ```bash
> docker run --rm --platform linux/amd64 -p 8000:8000 -e DJANGO_SECRET_KEY=change-me <utilisateur>/oc-lettings:latest
> ```

Pour une version précise, remplacer `latest` par le hash du commit. Pour activer Sentry, ajouter `-e SENTRY_DSN=<dsn>`.
