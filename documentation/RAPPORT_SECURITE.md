# Rapport d'Audit de Sécurité - Librairie XYZ

**Date:** 28 Mai 2026  
**Projet:** BC4SJ2-PYTHON (Django 5.0.6)  
**Périmètre:** Code source complet (backend, frontend, base de données, configuration, dépendances)

---

## État des dépendances

| Package | Version installée | Dernière version stable | Statut |
|---------|-------------------|------------------------|--------|
| Django | 5.0.6 | **6.0.5** / 5.2.14 LTS | 🔴 CRITIQUE - 10+ versions de retard |
| cryptography | 42.0.8 | **48.0.0** | 🔴 CRITIQUE - 39 vulnérabilités connues |
| bcrypt | 4.1.3 | **5.0.0** | 🟠 MODÉRÉ |
| asgiref | 3.8.1 | **3.11.1** | 🟠 MODÉRÉ - CVE-2025-14550 (DoS) |
| cffi | 1.16.0 | **2.0.0** | 🟡 FAIBLE |
| PyMySQL | 1.1.1 | **1.2.0** | 🟠 MODÉRÉ - CVE SQL injection (1.1.3) |
| pycparser | 2.22 | **3.0** | 🟡 FAIBLE |
| sqlparse | 0.5.0 | **0.5.5** | 🟡 FAIBLE |

---

## Synthèse des failles

| # | Catégorie | Gravité | Titre |
|---|-----------|---------|-------|
| V01 | Configuration | 🔴 CRITIQUE | DEBUG=True en production |
| V02 | Configuration | 🔴 CRITIQUE | SECRET_KEY hardcodée dans le code source |
| V03 | Base de données | 🔴 CRITIQUE | Identifiants DB en clair dans le code source |
| V04 | Dépendances | 🔴 CRITIQUE | cryptography 42.0.8 : 39 vulnérabilités connues |
| V05 | Backend/Auth | 🔴 CRITIQUE | @csrf_exempt sur endpoints sensibles (emprunts) |
| V06 | Backend/Auth | 🔴 CRITIQUE | Système d'authentification custom contournant Django Auth |
| V07 | Backend | 🟠 MODÉRÉ | Absence de contrôle d'accès sur endpoints sensibles |
| V08 | Backend | 🟠 MODÉRÉ | Pas de rate limiting (login/register) |
| V09 | Dépendances | 🟠 MODÉRÉ | Django 5.0.6 : multiples CVE corrigées depuis |
| V10 | Base de données | 🟠 MODÉRÉ | SQL raw sans ORM sur l'ensemble du projet |
| V11 | Configuration | 🟠 MODÉRÉ | ALLOWED_HOSTS = [] et absence de headers de sécurité |
| V12 | Frontend | 🟠 MODÉRÉ | XSS : injection possible via photo_url dans les templates |
| V13 | Frontend | 🟠 MODÉRÉ | CSRF token manquant dans new_loan.html |
| V14 | Dépendances | 🟠 MODÉRÉ | PyMySQL 1.1.1 : vulnérabilité SQL injection corrigée en 1.1.3 |
| V15 | Backend | 🟠 MODÉRÉ | Gestion manuelle des mots de passe (bypass Django) |
| V16 | Backend | 🟠 MODÉRÉ | Messages d'erreur exposant des détails DB |
| V17 | Dépendances | 🟡 FAIBLE | bcrypt 4.1.3 obsolète |
| V18 | Dépendances | 🟡 FAIBLE | asgiref 3.8.1 : CVE-2025-14550 DoS |
| V19 | Code Quality | 🟡 FAIBLE | Modèle Book non hérité de models.Model |
| V20 | Code Quality | 🟡 FAIBLE | Logging via print() au lieu du logger Django |
| V21 | Configuration | 🟡 FAIBLE | Session cookies non sécurisés (pas de HTTPOnly/Secure) |
| V22 | Base de données | 🟡 FAIBLE | Utilisateur DB avec GRANT OPTION et accès depuis % |

---

## Détail des failles

---

### V01 — DEBUG=True en production — 🔴 CRITIQUE

**Fichier:** `librairie/settings.py:26`  
**Description:** Le mode DEBUG est activé (`DEBUG = True`). Le projet est déployé en production (README mentionne un lien HTTPS distant). En mode DEBUG, Django expose les stack traces complètes, les variables locales, les settings (incluant la SECRET_KEY et les mots de passe DB) en cas d'erreur 500.

**Impact:** 
- Fuite de la SECRET_KEY
- Fuite des identifiants de base de données
- Exposition de la structure interne du code
- Attaques par déni de service facilitées

**Correction proposée:**
```python
DEBUG = os.environ.get('DJANGO_DEBUG', 'False').lower() in ('true', '1', 't')
```

---

### V02 — SECRET_KEY hardcodée — 🔴 CRITIQUE

**Fichier:** `librairie/settings.py:24`  
**Description:** `SECRET_KEY = 'django-insecure-@hls)o^6*(#*n0-nhq!k*me@(@tfk@b)2&m^q2(#)lfds-fsrm'` est en clair dans le code source, commitée sur GitHub. Cette clé est utilisée pour signer les sessions, les tokens CSRF, et le chiffrement des cookies.

**Impact:**
- Forgery de session (usurpation d'identité admin)
- Contournement de la protection CSRF
- Déchiffrement des cookies signés

**Correction proposée:**
```python
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
# En dev uniquement:
# if not SECRET_KEY:
#     raise ImproperlyConfigured("DJANGO_SECRET_KEY must be set")
```

---

### V03 — Identifiants DB en clair — 🔴 CRITIQUE

**Fichiers:** `librairie/settings.py:89-96`, `sql/library.sql:41-43`  
**Description:** Les credentials MySQL sont hardcodés :
```
USER: 'libr'
PASSWORD: 'NIEN97BF21OZEFJOZEO'
```
L'utilisateur est créé avec `GRANT ALL PRIVILEGES` et `WITH GRANT OPTION`, accessible depuis n'importe quel hôte (`'libr'@'%'`).

**Impact:**
- Accès complet à la base de données si le code fuit
- Escalade de privilèges possible (GRANT OPTION)
- Déjà exposé sur GitHub

**Correction proposée:**
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '3306'),
    }
}
```
Restreindre l'utilisateur DB à `'libr'@'localhost'` et révoquer `GRANT OPTION`.

---

### V04 — cryptography 42.0.8 : 39 vulnérabilités — 🔴 CRITIQUE

**Fichier:** `requirements.txt:4`  
**Description:** `cryptography==42.0.8` date de juin 2024. La version actuelle est **48.0.0** (mai 2026). 39 vulnérabilités connues affectent la version 42.0.8, dont des failles critiques de type buffer overflow, null pointer dereference, et contournement de validation.

**Impact:**
- Exécution de code à distance potentielle
- Corruption de mémoire
- Contournement de vérifications cryptographiques

**Correction proposée:**
```txt
cryptography>=48.0.0,<49.0.0
```

---

### V05 — @csrf_exempt sur endpoints sensibles — 🔴 CRITIQUE

**Fichier:** `loan/views.py:12,34,82`  
**Description:** Les vues `loan()`, `new_loan()`, et `return_loan()` sont décorées avec `@csrf_exempt`, désactivant la protection CSRF sur des endpoints qui modifient l'état (emprunts/retours de livres).

**Impact:**
- Attaques CSRF permettant d'emprunter/retourner des livres à l'insu de l'utilisateur
- Modification non autorisée de l'état des livres

**Correction proposée:**
Supprimer les décorateurs `@csrf_exempt` et s'assurer que tous les formulaires incluent `{% csrf_token %}`.

---

### V06 — Auth custom contournant Django Auth — 🔴 CRITIQUE

**Fichier:** `accounts/views.py:13-31`  
**Description:** L'authentification est gérée manuellement via les sessions Django (`request.session['is_authenticated'] = True`) au lieu d'utiliser `django.contrib.auth`. Aucune intégration avec le middleware d'authentification, pas de protection contre la fixation de session, pas de rotation de session après login.

**Impact:**
- Session fixation possible
- Contournement de toutes les protections de Django Auth
- Pas de `@login_required` utilisable nativement
- Pas de gestion des permissions par groupe

**Correction proposée:**
Implémenter un backend d'authentification custom qui s'intègre avec `django.contrib.auth`, ou migrer vers le modèle User standard de Django.

---

### V07 — Absence de contrôle d'accès — 🟠 MODÉRÉ

**Fichiers:** `books/views.py`, `home/views.py`  
**Description:**
- `books_view()` : pas d'authentification requise
- `book_detail_view()` : pas d'authentification requise
- `home_view()` : pas d'authentification requise
- `add_book_view()` : **aucune vérification de rôle admin**

**Impact:**
- N'importe quel utilisateur peut ajouter des livres
- Accès non restreint aux données

**Correction proposée:**
Utiliser le système d'authentification Django avec `@login_required` et `@user_passes_test` pour les rôles admin.

---

### V08 — Pas de rate limiting — 🟠 MODÉRÉ

**Fichiers:** `accounts/views.py`, endpoints login/register  
**Description:** Aucune limitation du nombre de tentatives de connexion ou d'inscription. Aucune protection contre le brute-force.

**Impact:**
- Attaques par dictionnaire sur les comptes
- Dénis de service sur l'inscription

**Correction proposée:**
Utiliser `django-ratelimit` ou `django-axes` pour limiter les tentatives.

---

### V09 — Django 5.0.6 obsolète — 🟠 MODÉRÉ

**Fichier:** `requirements.txt:5`  
**Description:** Django 5.0.6 est dépassé de 10+ versions. Les versions 5.0.7+ corrigent des CVE. La version LTS actuelle est **5.2.14** et la dernière stable est **6.0.5**.

**Impact:**
- Vulnérabilités de session fixation (CVE-2026-35192)
- Exposure de données privées (CVE-2026-6907)
- DoS via upload (CVE-2026-5766)

**Correction proposée:**
```txt
Django>=5.2.14,<6.0.0   # LTS recommandée
# ou
Django>=6.0.5,<6.1.0
```

---

### V10 — SQL raw sans ORM — 🟠 MODÉRÉ

**Fichiers:** `accounts/views.py`, `books/views.py`, `loan/views.py`, `home/views.py`  
**Description:** L'intégralité des requêtes DB utilise `connection.cursor()` avec du SQL brut, au lieu de l'ORM Django. Bien que les paramètres soient passés de manière sécurisée (`%s`), le risque d'erreur humaine est maximal et aucune validation de schéma n'est faite.

**Impact:**
- Risque accru d'injection SQL en cas d'oubli de paramétrage
- Aucune validation des données (types, longueurs)
- Code non maintenable et sujet aux erreurs

**Correction proposée:**
Migrer vers les modèles Django ORM pour toutes les opérations CRUD.

---

### V11 — ALLOWED_HOSTS vide et headers de sécurité absents — 🟠 MODÉRÉ

**Fichier:** `librairie/settings.py:27`  
**Description:**
- `ALLOWED_HOSTS = []` — en production avec DEBUG=True, cela expose le serveur aux attaques Host header injection
- Aucun header de sécurité : pas de `SECURE_HSTS_SECONDS`, `SECURE_SSL_REDIRECT`, `SECURE_BROWSER_XSS_FILTER`, `SECURE_CONTENT_TYPE_NOSNIFF`

**Impact:**
- Host header injection
- Man-in-the-middle (pas de HSTS)
- Clickjacking (X-Frame-Options présent mais insuffisant sans CSP)

**Correction proposée:**
```python
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(',')
SECURE_SSL_REDIRECT = True
SECURE_HSTS_SECONDS = 31536000
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
```

---

### V12 — XSS potentiel via photo_url — 🟠 MODÉRÉ

**Fichiers:** `templates/books.html:17`, `templates/book_detail.html:23`  
**Description:** Le champ `photo_url` (provenant de la base de données ou saisi par l'utilisateur) est injecté directement dans l'attribut `src` d'une balise `<img>` sans validation. Un attaquant pourrait insérer `javascript:alert(1)` comme URL.

**Impact:**
- Exécution de JavaScript dans le navigateur de la victime
- Vol de cookies de session

**Correction proposée:**
Valider que `photo_url` commence par `https://` avant affichage, ou utiliser une whitelist de domaines autorisés.

---

### V13 — CSRF token manquant dans new_loan.html — 🟠 MODÉRÉ

**Fichier:** `templates/new_loan.html`  
**Description:** Le template `new_loan.html` affiche le formulaire avec `{{ form.as_p }}` mais n'inclut pas `{% csrf_token %}`. Combiné avec `@csrf_exempt` sur la vue, cela rend l'endpoint vulnérable.

**Correction proposée:**
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Emprunter</button>
</form>
```

---

### V14 — PyMySQL 1.1.1 : SQL injection — 🟠 MODÉRÉ

**Fichier:** `requirements.txt:7`  
**Description:** PyMySQL 1.1.1 est vulnérable à une injection SQL via `Cursor.callproc()` (corrigé en 1.1.3). La version actuelle est 1.2.0.

**Correction proposée:**
```txt
PyMySQL>=1.2.0,<2.0.0
```

---

### V15 — Gestion manuelle des mots de passe — 🟠 MODÉRÉ

**Fichiers:** `accounts/views.py:49-56`, `sql/library.sql`  
**Description:** Les mots de passe sont hashés avec `make_password()` dans la vue `register_view()`, mais le système d'authentification custom les vérifie avec `check_password()`. Aucun validateur de complexité n'est appliqué (bien que Django les ait configurés dans `AUTH_PASSWORD_VALIDATORS`, ils ne sont pas utilisés car `register_view` ne crée pas un `User` Django).

**Impact:**
- Validation de mot de passe absente
- Hash stocké via un mécanisme non standard (bcrypt_sha256$)

**Correction proposée:**
Utiliser `django.contrib.auth.models.User` pour la création d'utilisateurs, ce qui appliquera automatiquement les validateurs de mot de passe.

---

### V16 — Messages d'erreur exposant des détails DB — 🟠 MODÉRÉ

**Fichiers:** `books/views.py:52`, `books/views.py:78`  
**Description:** Les erreurs de base de données sont exposées à l'utilisateur :
```python
form.add_error(None, "An error occurred while updating the book: {}".format(e))
```
Cela peut fuiter des noms de tables, de colonnes, ou des contraintes.

**Correction proposée:**
```python
import logging
logger = logging.getLogger(__name__)
# ...
logger.error("Book update failed: %s", e)
form.add_error(None, "Une erreur est survenue. Veuillez réessayer.")
```

---

### V17 — bcrypt 4.1.3 obsolète — 🟡 FAIBLE

**Fichier:** `requirements.txt:2`  
**Description:** bcrypt 4.1.3 est 2 versions majeures derrière (5.0.0). La version 5.0.0 corrige des problèmes de sécurité (truncation silencieuse des mots de passe > 72 octets).

**Correction proposée:**
```txt
bcrypt>=5.0.0,<6.0.0
```

---

### V18 — asgiref 3.8.1 : CVE-2025-14550 — 🟡 FAIBLE

**Fichier:** `requirements.txt:1`  
**Description:** asgiref 3.8.1 est vulnérable au CVE-2025-14550 (DoS via WsgiToAsgi). La version corrigée minimale est 3.11.1.

**Correction proposée:**
```txt
asgiref>=3.11.1,<4.0.0
```

---

### V19 — Modèle Book non conforme — 🟡 FAIBLE

**Fichier:** `books/models.py`  
**Description:** La classe `Book` n'hérite pas de `django.db.models.Model`. C'est une classe Python standard, ce qui empêche d'utiliser l'ORM et les migrations Django. Le `__init__` écrase le constructeur du modèle.

**Correction proposée:**
```python
class Book(models.Model):
    titre = models.CharField(max_length=255)
    auteur = models.CharField(max_length=255)
    date_publication = models.DateField()
    isbn = models.CharField(max_length=13)
    description = models.TextField()
    statut = models.CharField(max_length=20, default='disponible')
    photo_url = models.URLField(max_length=255)
```

---

### V20 — Logging via print() — 🟡 FAIBLE

**Fichiers:** `loan/views.py:30,53,72,91`, `books/views.py`, etc.  
**Description:** Les erreurs sont loggées via `print()` au lieu du système de logging Django. Cela empêche toute traçabilité, monitoring, et agrégation des erreurs en production.

**Correction proposée:**
Remplacer tous les `print()` par `logger.error()` avec le système de logging configuré dans `settings.py`.

---

### V21 — Cookies de session non sécurisés — 🟡 FAIBLE

**Fichier:** `librairie/settings.py` (absence de configuration)  
**Description:** `SESSION_COOKIE_SECURE`, `SESSION_COOKIE_HTTPONLY`, et `CSRF_COOKIE_SECURE` ne sont pas configurés. En production, les cookies de session peuvent être transmis en clair.

**Correction proposée:**
```python
SESSION_COOKIE_SECURE = True
SESSION_COOKIE_HTTPONLY = True
CSRF_COOKIE_SECURE = True
```

---

### V22 — Utilisateur DB sur-privilégié — 🟡 FAIBLE

**Fichier:** `sql/library.sql:41-43`  
**Description:** `CREATE USER 'libr'@'%' IDENTIFIED BY 'NIEN97BF21OZEFJOZEO'; GRANT ALL PRIVILEGES ON library.* TO 'libr'@'%' WITH GRANT OPTION;` — L'utilisateur a tous les privilèges incluant DROP, ALTER, GRANT, et est accessible depuis n'importe quelle adresse IP.

**Correction proposée:**
```sql
CREATE USER 'libr'@'localhost' IDENTIFIED BY '<password>';
GRANT SELECT, INSERT, UPDATE, DELETE ON library.* TO 'libr'@'localhost';
FLUSH PRIVILEGES;
```

---

## Plan de remédiation Agile

### Sprint 1 — Correctifs critiques (Urgence — Semaine 1)

| Issue | Priorité | Effort |
|-------|----------|--------|
| V01 — DEBUG=False | Blocker | 0.5 j |
| V02 — SECRET_KEY via env | Blocker | 0.5 j |
| V03 — DB credentials via env | Blocker | 0.5 j |
| V04 — Upgrade cryptography | Blocker | 1 j |
| V05 — Supprimer @csrf_exempt | Blocker | 1 j |
| V11 — ALLOWED_HOSTS + headers | Blocker | 0.5 j |

**Total Sprint 1:** ~4 jours

### Sprint 2 — Auth & Accès (Semaine 2)

| Issue | Priorité | Effort |
|-------|----------|--------|
| V06 — Auth Django native | Haute | 3 j |
| V07 — Contrôle d'accès endpoints | Haute | 1.5 j |
| V08 — Rate limiting | Haute | 1 j |
| V15 — Gestion password Django | Haute | 1 j |
| V21 — Cookies sécurisés | Haute | 0.5 j |

**Total Sprint 2:** ~7 jours

### Sprint 3 — Dépendances & ORM (Semaine 3)

| Issue | Priorité | Effort |
|-------|----------|--------|
| V09 — Upgrade Django LTS | Haute | 2 j |
| V10 — Migration SQL → ORM | Haute | 4 j |
| V19 — Modèle Book conforme | Haute | 1 j |
| V14 — Upgrade PyMySQL | Moyenne | 0.5 j |
| V17 — Upgrade bcrypt | Faible | 0.5 j |
| V18 — Upgrade asgiref | Faible | 0.5 j |

**Total Sprint 3:** ~8.5 jours

### Sprint 4 — Frontend & Qualité (Semaine 4)

| Issue | Priorité | Effort |
|-------|----------|--------|
| V12 — XSS photo_url | Haute | 1 j |
| V13 — CSRF token new_loan | Haute | 0.5 j |
| V16 — Messages d'erreur | Moyenne | 0.5 j |
| V20 — Logging standard | Faible | 0.5 j |
| V22 — Restreindre privilèges DB | Faible | 0.5 j |

**Total Sprint 4:** ~3 jours

---

**Total estimé du plan:** ~22.5 jours/homme sur 4 sprints d'une semaine.
