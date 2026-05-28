# Organisation Agile — libXYZ LOAN

## Équipe

| Membre GitHub | Rôle |
|---------------|------|
| `diegodudn` | Scrum Master / Coordination & rédaction rapport |
| `kevljn` | Dev / Tests manuels (pentest, injection, XSS) |
| `orAAKLe` | Dev / Revue de code & sécurité Django |
| `rudyb` | Dev / Analyse statique SonarQube & qualité |

---

## Méthodologie : Scrum adapté (sprints courts)

Durée de sprint : **1 jour** (contexte examen 4h → 1 sprint unique découpé en itérations de ~45min)

### Cérémonies

| Cérémonie | Durée | Moment |
|-----------|-------|--------|
| Sprint Planning | 15 min | Début de séance |
| Stand-up | 5 min | Toutes les 45 min |
| Sprint Review | 10 min | Fin de séance |
| Rétrospective | 5 min | Avant la soutenance |

---

## Kanban GitHub Projects

### Colonnes du tableau

| Colonne | Description |
|---------|-------------|
| **Backlog** | Toutes les issues identifiées, non encore traitées |
| **In Progress** | Issue en cours de traitement (1 par personne max) |
| **In Review** | PR ouverte, en attente de validation |
| **Done** | Issue terminée, mergée, vérifiée |

### Colonnes de criticité sécurité (matrice risque)

Ces 3 colonnes servent à **classifier les issues de sécurité** avant de les traiter. Chaque issue de sécurité est d'abord posée ici, puis déplacée dans le Backlog avec sa priorité.

| Colonne | Risque × Probabilité | Exemples |
|---------|----------------------|----------|
| 🔴 **HIGH** | Risque élevé ET/OU probabilité élevée | `DEBUG=True` en prod, pas d'auth sur vues sensibles, injection SQL |
| 🟡 **MEDIUM** | Risque modéré OU probabilité modérée | CSRF mal configuré, exposition de données non critique |
| 🟢 **LOW** | Risque faible ET probabilité faible | Mauvaise gestion d'erreur mineure, info-disclosure dans les messages |

### Matrice risque / probabilité

```
         │ Probabilité LOW │ Probabilité MEDIUM │ Probabilité HIGH
─────────┼─────────────────┼────────────────────┼──────────────────
Risque   │                 │                    │
HIGH     │    MEDIUM       │       HIGH         │      HIGH
         │                 │                    │
MEDIUM   │    LOW          │       MEDIUM       │      HIGH
         │                 │                    │
LOW      │    LOW          │       LOW          │      MEDIUM
```

---

## Workflow d'une issue de sécurité

```
1. Faille identifiée (revue de code / SonarQube / test)
2. Issue créée avec template → placée dans colonne criticité (HIGH/MEDIUM/LOW)
3. Issue déplacée en BACKLOG avec label correspondant
4. Affectée à un membre → In Progress
5. Correctif développé + PR ouverte → In Review
6. Review + merge → Done
```

---

## Priorités du sprint (ordre de traitement)

1. 🔴 Issues **HIGH** — bloquants avant tout déploiement
2. 🟡 Issues **MEDIUM** — à corriger dans le sprint
3. 🟢 Issues **LOW** — si le temps le permet

---

## Périmètre des fichiers à analyser en priorité

Selon le sujet, les fichiers prioritaires sont :

| Fichier | Responsable suggéré |
|---------|---------------------|
| `librairie/settings.py` | `rudyb` |
| `librairie/urls.py` | `orAAKLe` |
| `loan/views.py` | `kevljn` |
| `loan/forms.py` | `kevljn` |
| `loan/models.py` | `orAAKLe` |
| `templates/loan.html` | `rudyb` |
| `templates/new_loan.html` | `rudyb` |
| `templates/return_loan.html` | `rudyb` |
| `templates/base.html` | `diegodudn` |
| `templates/footer.html` | `diegodudn` |
| `home/views.py` | `orAAKLe` |

---

## Définition of Done (DoD)

Une issue est considérée **Done** uniquement si :

- [ ] Le correctif est implémenté et testé
- [ ] La PR a été reviewée par au moins 1 autre membre
- [ ] Aucune régression introduite
- [ ] La faille est documentée dans le rapport (description, CVSS, correctif)
- [ ] Le code est mergé dans `develop`
