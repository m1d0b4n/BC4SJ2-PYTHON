# PROMPT GAMMA.APP — AT4 Sujet 2 : Remise en conformité libXYZ LOAN
# VERSION 10 SLIDES — 20 MINUTES (~2 min/slide)

---

Copier-coller ce texte dans Gamma.app > "Generate" > "Paste outline"

---

## PROMPT :

Génère une présentation professionnelle en français de **exactement 10 slides** intitulée :
**"Remise en conformité de l'application libXYZ LOAN — Audit de sécurité"**

Style visuel : sombre, moderne, cybersécurité. Thème dark avec accents rouge/orange pour les vulnérabilités critiques, vert pour les éléments sécurisés. Police sans-serif propre. Icônes tech.

---

### Slide 1 — Page de titre (1 min)

**Titre :** Remise en conformité — libXYZ LOAN
**Sous-titre :** AT4 · Audit de sécurité applicative · 28 mai 2026

Équipe de 4 :
- diegodudn — Scrum Master / Coordination
- kevljn — Pentest & tests manuels
- orAAKLe — Revue de code & sécurité Django
- rudyb — Analyse statique SonarCloud & qualité

Stack auditée : Django 5.0.6 · Python 3.12 · MySQL 8.0 · Apache · Docker
URL cible : https://exam-red.edu-jalm.fr

---

### Slide 2 — Contexte & Organisation Agile (2 min)

**Titre :** Contexte & Méthodologie

**Contexte :**
La librairie XYZ a reçu une première version de son application web (gestion de livres + emprunts). Bien que fonctionnelle, elle contient de nombreuses failles. Notre équipe réalise un audit complet avant déploiement en production.

Périmètre : `settings.py` · module `loan/` · module `books/` · `accounts/` · templates

**Organisation Agile (Scrum adapté — contexte examen 4h) :**
- 1 sprint unique découpé en itérations de 45 min
- Sprint Planning (15 min) → Stand-up toutes les 45 min → Sprint Review → Rétrospective
- **50+ issues** créées sur GitHub Projects (Kanban) : classifiées HIGH / MEDIUM / LOW
- Outils : SonarCloud (analyse statique) · OWASP PTK (DAST/IAST) · Pentest boîte grise

[Insérer screenshot Kanban GitHub]

---

### Slide 3 — Revue de code — Configuration & Authentification (2 min)

**Titre :** Revue de code — `settings.py` & Authentification

Fichier `librairie/settings.py` — **4 failles critiques** :

| Faille | Impact | CVSS |
|--------|--------|------|
| `SECRET_KEY` hardcodée en clair | Compromet toute la crypto Django | **9.1** 🔴 |
| Password MySQL en dur (`'NIEN97BF21OZEFJOZEO'`) | Accès DB si code source exposé | **9.8** 🔴 |
| `DEBUG = True` en production | Expose stack traces, code source, IP interne | **7.5** 🔴 |
| `ALLOWED_HOSTS = []` | Aucun filtre sur les hôtes HTTP | **6.5** 🔴 |

Fichier `accounts/views.py` — **système d'auth custom** :
- Contourne Django Auth natif → gestion manuelle via `session['user_id']`
- Aucun `@login_required` → vérification `session.get('is_authenticated')` non fiable

---

### Slide 4 — Revue de code — Module LOAN (2 min)

**Titre :** Revue de code — Module LOAN & livres

Fichier `loan/views.py` — **failles bloquantes** :
- ❌ `@csrf_exempt` sur **toutes** les vues (`loan`, `new_loan`, `return_loan`) → bypass CSRF total — CVSS **8.8**
- ❌ Vue `loan()` accessible **sans authentification** (pas de `@login_required`) — CVSS **7.5**
- ❌ `return_loan()` — aucune vérification que l'emprunt appartient à l'utilisateur courant

Fichier `books/views.py` :
- ❌ `add_book_view()` — **aucun contrôle de rôle admin** → utilisateur standard peut ajouter des livres — CVSS **8.1**
- ❌ `delete_book_view()` — `IntegrityError` non gérée → HTTP 500 + traceback complet exposé

Fichier `sql/library.sql` :
- ❌ **Hash bcrypt d'utilisateurs committé** dans le dépôt Git — CVSS **7.4**

---

### Slide 5 — SonarCloud — Analyse statique (2 min)

**Titre :** SonarCloud — Résultats sur 1 400 lignes de code

[Insérer screenshot dashboard SonarCloud]

| Catégorie | Issues | Note SonarCloud |
|-----------|--------|-----------------|
| 🔴 Sécurité | 4 issues | **E** — pire note possible |
| 🟠 Fiabilité | 3 issues | **C** |
| 🟢 Maintenabilité | 23 issues | **A** |
| 🔥 Security Hotspots | **18** | À analyser manuellement |
| Duplications | 0.0% | ✅ |

[Insérer screenshot liste issues SonarCloud]

Top issues SonarCloud :
- **Blocker ×3** : SECRET_KEY exposée + bcrypt hash × 2 dans `sql/library.sql`
- **High ×2** : Caractère illégal (code point 10) dans littéraux SQL
- **Medium ×24** : Contraste CSS insuffisant · sélecteurs dupliqués · attribut `lang` absent

→ **28 issues importées et classifiées** sur GitHub Kanban

---

### Slide 6 — Pentest — 3 exploits réussis en production (2 min)

**Titre :** Pentest boîte grise — exam-red.edu-jalm.fr — 28 mai 2026

🔴 **Exploit 1 — Fuite de code source (DEBUG=True)**
`GET /books/999/` → HTTP 500 → Stack trace complète : code source, variables locales, routes Django, version, IP interne `10.250.0.5` — CVSS **7.5**

🔴 **Exploit 2 — CSRF bypass (création d'emprunt sans token)**
`POST /loan/new_loan/` sans `csrfmiddlewaretoken` → HTTP 302 → emprunt créé pour `marc@lord.com`
`@csrf_exempt` désactive toute protection CSRF — CVSS **8.8**

🔴 **Exploit 3 — Élévation de privilèges (utilisateur standard ajoute un livre)**
`POST /books/add/` avec cookie utilisateur standard → HTTP 302 → livre `"USER_HACKED"` visible publiquement
Aucun contrôle de rôle dans `add_book_view()` — CVSS **8.1**

[Insérer screenshot liste des livres montrant XSS et USER_HACKED]
[Insérer screenshot console DevTools : fetch CSRF-free → status 200]

---

### Slide 7 — OWASP PTK + Ce que l'appli bloque (2 min)

**Titre :** Scan OWASP PTK & Résistances

**OWASP PTK — exam-red.edu-jalm.fr :**

| Moteur | Sévérité | Finding |
|--------|----------|---------|
| IAST | 🔴 HIGH ×7 | DOM XSS via Bootstrap sur `/books/`, `/loan/`, `/accounts/` (CWE-79, CVSS 6.1) |
| DAST | 🟡 MEDIUM ×1 | Python traceback + IP `10.250.0.5` sur `/books/4/delete/` |
| DAST | 🟢 LOW ×7 | CSP absent · HSTS absent · hints "dev"/"testing" dans réponses |
| Cookie | ⚠️ | `csrftoken` : HttpOnly = **false** → accessible par JavaScript |

**Ce que l'application bloque correctement :**
- ✅ POST non authentifiés → **403 Forbidden** (middleware CSRF actif)
- ✅ Injection SQL classique → requêtes paramétrées `%s` protègent les vues
- ✅ Données côté client → localStorage = 0 · sessionStorage = 0
- ✅ Dépendances à risque élevé → aucune détectée

---

### Slide 8 — Synthèse CVSS & Mapping OWASP Top 10 (2 min)

**Titre :** Synthèse des vulnérabilités — 30 failles — Mapping OWASP 2025

Tableau consolidé (top 10) :

| ID | Faille | Source | OWASP 2025 | CVSS |
|----|--------|--------|------------|------|
| F-02 | Password DB en clair | Code | A02 | **9.8** 🔴 |
| F-01 | SECRET_KEY hardcodée | Code / Sonar | A02 | **9.1** 🔴 |
| F-03 | @csrf_exempt sur LOAN | Code | A01 | **8.8** 🔴 |
| F-09 | add_book sans contrôle rôle | Pentest | A01 | **8.1** 🔴 |
| F-05 | DEBUG=True + traceback | Sonar / DAST | A05 | **7.5** 🔴 |
| F-06 | loan() sans @login_required | Code | A01 | **7.5** 🔴 |
| F-04 | Hash bcrypt dans SQL commité | Sonar | A02 | **7.4** 🔴 |
| F-07 | DOM XSS Bootstrap (×7) | IAST | A03 | **6.1** 🔴 |
| F-11 | Cookie csrftoken sans HttpOnly | PTK | A05 | **5.4** 🟡 |
| F-13/14 | CSP + HSTS absents | PTK | A05 | **4.8** 🟡 |

Répartition OWASP :
- **A01** Broken Access Control : 4 failles · max 8.8
- **A02** Cryptographic Failures : 3 failles · max **9.8**
- **A03** Injection : 2 failles · max 6.1
- **A05** Misconfiguration : 7 failles · max 7.5

---

### Slide 9 — Specs reformulées & Planning sprint (2 min)

**Titre :** Reformulation des specs & Planning pré-déploiement

**Specs reformulées — Module LOAN (après audit) :**
- Toute vue LOAN exige `@login_required` (Django Auth natif — plus de `session['user_id']` custom)
- CRUD livres réservé au rôle admin → contrôle via `request.user.is_staff`
- Tous les endpoints LOAN protégés par CSRF → supprimer `@csrf_exempt`
- Configuration via variables d'environnement `.env` : SECRET_KEY, DB_PASSWORD, ALLOWED_HOSTS
- `DEBUG = False` + pages d'erreur génériques en production
- Cookies : `Secure` + `HttpOnly` + `SameSite=Lax`

**Planning :**

🔴 **Sprint URGENCE (0–7 jours) — 7 correctifs bloquants :**
Déplacer SECRET_KEY + DB_PASSWORD dans `.env` · `DEBUG=False` · Supprimer `@csrf_exempt` · Ajouter `@login_required` sur LOAN · Définir `ALLOWED_HOSTS` · Contrôle rôle admin `add_book` · Migrer vers `request.user`

🟡 **Sprint 2 (7–30 jours) :**
Supprimer hashes SQL committés · Ajouter CSP · Activer HSTS · `COOKIE_HTTPONLY=True` · Nettoyer données injectées (livres ID 5, 6)

🟢 **Backlog :** Accessibilité HTML · Contraste CSS · Sélecteurs dupliqués

---

### Slide 10 — Conclusion (1 min)

**Titre :** Conclusion — L'application n'est pas déployable en l'état

**Avant remédiation :**
- 🔴 3 exploits réussis en production confirmés
- 🔴 CVSS max = **9.8** (credentials DB en clair)
- 🔴 SonarCloud Security : note **E**
- ❌ **Non déployable en production**

**Après sprint d'urgence (7 jours) :**
- ✅ 7 failles bloquantes corrigées → risque passe de CRITIQUE à **MODÉRÉ**
- ✅ Aucune credential en clair
- ✅ CSRF + authentification correctement gérés
- ✅ **Déployable sous surveillance**

**Message clé :** La version livrée est fonctionnelle mais présente des failles OWASP Top 10 élémentaires non corrigées. Le sprint d'urgence est un **prérequis absolu** avant toute mise en production.

Repo : github.com/m1d0b4n/BC4SJ2-PYTHON · Kanban : GitHub Projects BC4SJ2-PYTHON · SonarCloud : m1d0b4n_BC4SJ2-PYTHON

---

FIN DU PROMPT
