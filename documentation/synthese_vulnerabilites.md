# Synthèse consolidée des vulnérabilités – libXYZ LOAN

**Projet :** BC4SJ2-PYTHON (librairie XYZ – module LOAN)  
**Date :** 28 mai 2026  
**Sources :** Revue de code manuelle · SonarCloud · OWASP PTK (DAST/IAST)  
**URL testée :** https://exam-red.edu-jalm.fr  

---

## 1. Résumé exécutif

| Criticité | Nombre |
|-----------|--------|
| 🔴 HIGH   | 10     |
| 🟡 MEDIUM | 6      |
| 🟢 LOW    | 14     |
| **Total** | **30** |

**7 failles à corriger immédiatement avant tout déploiement en production.**

---

## 2. Tableau consolidé des vulnérabilités

### 🔴 HIGH – Correction obligatoire avant déploiement

| ID | Titre | Source | Fichier concerné | OWASP 2025 | CWE | CVSS 3.1 | Score |
|----|-------|--------|-----------------|------------|-----|----------|-------|
| F-01 | `SECRET_KEY` Django hardcodée en clair dans le code | SonarCloud #33 · Code review | `librairie/settings.py:23` | A02 – Crypto Failures | CWE-321 | AV:N/AC:L/PR:N/UI:N/S:C/C:H/I:H/A:N | **9.1** |
| F-02 | Mot de passe de la base de données en clair dans le code | Code review | `librairie/settings.py:94` | A02 – Crypto Failures | CWE-259 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:H/A:H | **9.8** |
| F-03 | `@csrf_exempt` sur toutes les vues LOAN (loan, new_loan, return_loan) | Code review | `loan/views.py:11,32,70` | A01 – Broken Access Control | CWE-352 | AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:H | **8.8** |
| F-04 | Hash bcrypt d'un utilisateur exposé dans le code source | SonarCloud #37 #38 | `sql/library.sql` | A02 – Crypto Failures | CWE-312 | AV:N/AC:H/PR:N/UI:N/S:U/C:H/I:H/A:N | **7.4** |
| F-05 | `DEBUG = True` en production → stack trace + IP interne exposés | SonarCloud #33 · DAST-0001/0006 | `librairie/settings.py:26` | A05 – Security Misconfiguration | CWE-209 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:N/A:N | **7.5** |
| F-06 | Vue `loan()` accessible sans authentification (`@login_required` absent) | Code review | `loan/views.py:12` | A01 – Broken Access Control | CWE-306 | AV:N/AC:L/PR:N/UI:N/S:U/C:H/I:L/A:N | **7.5** |
| F-07 | DOM XSS via mutation Bootstrap (7 pages : `/books/`, `/loan/`, `/accounts/`) | IAST-0001 à 0007 | Templates + JS Bootstrap | A03 – Injection | CWE-79 | AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:L/A:N | **6.1** |
| F-08 | `ALLOWED_HOSTS = []` → hôte non restreint | Code review | `librairie/settings.py:28` | A05 – Security Misconfiguration | CWE-284 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:L/A:N | **6.5** |
| F-09 | Session d'authentification via `session['user_id']` (contournement `@login_required`) | Code review | `loan/views.py` · `accounts/views.py` | A07 – Identification Failures | CWE-384 | AV:N/AC:L/PR:L/UI:N/S:U/C:H/I:L/A:N | **7.1** |
| F-10 | Erreur `IntegrityError` sur `/books/4/delete/` → 500 non géré | DAST-0001 · Code review | `books/views.py:27` | A05 – Security Misconfiguration | CWE-390 | AV:N/AC:L/PR:L/UI:N/S:U/C:L/I:L/A:L | **6.3** |

---

### 🟡 MEDIUM – À corriger avant déploiement (sous 30 jours)

| ID | Titre | Source | Fichier concerné | OWASP 2025 | CWE | CVSS 3.1 | Score |
|----|-------|--------|-----------------|------------|-----|----------|-------|
| F-11 | Cookie `csrftoken` sans attribut `HttpOnly` → accessible par JS | OWASP PTK · Code review | `librairie/settings.py` (manquant) | A05 – Security Misconfiguration | CWE-1004 | AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:L/A:N | **5.4** |
| F-12 | Caractère illégal (code point 10 = saut de ligne) dans littéraux SQL | SonarCloud #35 #36 | `sql/emprunt.sql` | A03 – Injection | CWE-89 | AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N | **4.8** |
| F-13 | Header `Content-Security-Policy` absent | DAST-0002 · OWASP PTK | Réponses HTTP serveur | A05 – Security Misconfiguration | CWE-693 | AV:N/AC:L/PR:N/UI:R/S:C/C:L/I:N/A:N | **4.7** |
| F-14 | Header `Strict-Transport-Security` (HSTS) absent | OWASP PTK | Réponses HTTP serveur | A05 – Security Misconfiguration | CWE-319 | AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N | **4.8** |
| F-15 | Hints d'environnement "dev" / "testing" dans les réponses HTTP | DAST-0003/4/5/8 | Réponses HTTP (`403`, `500`) | A05 – Security Misconfiguration | CWE-200 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N | **5.3** |
| F-16 | Adresse IP interne `10.250.0.5` leakée dans la stack trace | DAST-0006 | Réponse `500` sur `/books/4/delete/` | A05 – Security Misconfiguration | CWE-200 | AV:N/AC:L/PR:N/UI:N/S:U/C:L/I:N/A:N | **5.3** |

---

### 🟢 LOW – Backlog qualité / accessibilité

| ID | Titre | Source | Fichier concerné | CVSS 3.1 |
|----|-------|--------|-----------------|----------|
| F-17 | Contraste texte/fond insuffisant (×5 occurrences) | SonarCloud #39-41, #46, #48, #52, #56 | `static/css/style.css` | 3.1 |
| F-18 | Sélecteurs CSS dupliqués (`body`, `header`, `h1`, `a`, `table`, `button`, `form`, `#content`) | SonarCloud #42-45, #47, #49-51, #53-55 | `static/css/style.css` | 2.0 |
| F-19 | Attribut `lang` absent sur les balises `<html>` | SonarCloud #57 #58 #60 | Templates HTML | 2.0 |
| F-20 | Utilisation de `window` au lieu de `globalThis` | SonarCloud #59 | JavaScript | 1.5 |
| F-21 | `COOP` défini sans `COEP`/`CORP` (isolation cross-origin incomplète) | OWASP PTK | En-têtes HTTP | 3.1 |
| F-22 | `Referrer-Policy` faible ou absente | OWASP PTK | En-têtes HTTP | 3.1 |
| F-23 | `X-Content-Type-Options` manquant ou invalide | OWASP PTK | En-têtes HTTP | 3.1 |

---

## 3. Ce à quoi l'application résiste

| Test | Résultat | Détail |
|------|----------|--------|
| Requêtes POST non authentifiées (CSRF) | ✅ **Bloqué** → 403 Forbidden | Le middleware CSRF Django est actif et valide le token |
| Accès admin sans session | ✅ **Bloqué** | Vérification du `session['role'] == 'admin'` dans `books/views.py` |
| Injection SQL directe via ORM | ✅ **Résiste** | Les vues utilisant des paramètres `%s` sont protégées contre l'injection SQL classique |
| Stockage de données sensibles côté client | ✅ **OK** | `localStorage` = 0 entrée, `sessionStorage` = 0 entrée |
| Dépendances à risque élevé | ✅ **Aucune détectée** | OWASP PTK : no high-risk dependencies identified |

---

## 4. Correspondance OWASP Top 10 – 2025

| Catégorie OWASP | Failles associées | Gravité max |
|-----------------|-------------------|-------------|
| A01 – Broken Access Control | F-03 (`@csrf_exempt`), F-06 (auth manquante LOAN), F-09 (session bypass) | 🔴 8.8 |
| A02 – Cryptographic Failures | F-01 (SECRET_KEY), F-02 (password DB), F-04 (hash exposé) | 🔴 9.8 |
| A03 – Injection | F-07 (DOM XSS), F-12 (char illégal SQL) | 🔴 6.1 |
| A05 – Security Misconfiguration | F-05 (DEBUG), F-08 (ALLOWED_HOSTS), F-13 (CSP), F-14 (HSTS), F-15 (env hints), F-16 (IP leak), F-10 (500 non géré) | 🔴 7.5 |
| A07 – Identification & Auth Failures | F-09 (session custom), F-11 (cookie HttpOnly) | 🔴 7.1 |

---

## 5. Priorités de remédiation (planning pré-déploiement)

```
Sprint URGENCE (< 7 jours) :
  F-01  Déplacer SECRET_KEY dans variable d'environnement (.env)
  F-02  Déplacer credentials DB dans .env / secret manager
  F-03  Supprimer @csrf_exempt sur loan/, new_loan/, return_loan/
  F-05  Passer DEBUG=False + configurer handler 500 personnalisé
  F-06  Ajouter @login_required sur la vue loan()
  F-08  Définir ALLOWED_HOSTS avec les domaines autorisés uniquement
  F-09  Utiliser request.user.is_authenticated (auth Django natif)

Sprint 2 (7–30 jours) :
  F-04  Supprimer les hashes et credentials des fichiers SQL commités
  F-07  Ajouter CSP strict pour neutraliser le DOM XSS Bootstrap
  F-10  Gérer les erreurs 500 avec pages génériques (DEBUG=False)
  F-11  Ajouter SESSION_COOKIE_HTTPONLY=True + CSRF_COOKIE_HTTPONLY=True
  F-13  Configurer Content-Security-Policy
  F-14  Activer HSTS (SECURE_HSTS_SECONDS)
  F-15  Vérifier et nettoyer les réponses d'erreur

Backlog :
  F-17 à F-23  Qualité CSS, accessibilité HTML, headers mineurs
```
