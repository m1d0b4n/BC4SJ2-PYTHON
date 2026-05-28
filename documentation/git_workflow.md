# Git Workflow — libXYZ LOAN

## Branches

| Branche | Usage |
|---------|-------|
| `main` | Code stable, déployé en production |
| `develop` | Branche d'intégration principale |
| `feature/<slug>` | Nouvelle fonctionnalité |
| `fix/<slug>` | Correction de bug non critique |
| `hotfix/<slug>` | Correction urgente de sécurité (merge direct sur `main`) |

### Nommage des branches

```
feature/loan-csrf-protection
fix/footer-xss
hotfix/settings-debug-disabled
```

---

## Commits

Format **Conventional Commits** :

```
<type>(<scope>): <description courte>

[corps optionnel]

[refs: #<numéro issue>]
```

### Types autorisés

| Type | Usage |
|------|-------|
| `feat` | Nouvelle fonctionnalité |
| `fix` | Correction de bug |
| `sec` | Correctif de sécurité |
| `refactor` | Refactoring sans changement fonctionnel |
| `test` | Ajout ou modification de tests |
| `docs` | Documentation uniquement |
| `chore` | Maintenance (deps, config) |

### Exemples

```
sec(settings): disable DEBUG in production
fix(loan): add login_required decorator on new_loan view
feat(loan): add due date validation on return
refactor(books): replace raw query with ORM
```

---

## Issues GitHub

### Titre

```
[TYPE] Description courte du problème
```

Types : `[SEC]`, `[BUG]`, `[FEAT]`, `[REFACTOR]`, `[DOCS]`

### Corps de l'issue (template)

```markdown
## Description
Explication claire du problème ou de la fonctionnalité.

## Criticité (sécurité)
- Risque : High / Medium / Low
- Probabilité : High / Medium / Low
- Score CVSS estimé : (ex: 8.1)
- Catégorie OWASP : (ex: A01 - Broken Access Control)

## Fichier(s) concerné(s)
- `librairie/settings.py` ligne X
- `loan/views.py` ligne Y

## Reproduction (si bug/vuln)
Étapes pour reproduire le problème.

## Correctif proposé
Description de la solution envisagée.

## Critères d'acceptation
- [ ] Le correctif est en place
- [ ] Un test couvre le cas
- [ ] La PR est reviewée par au moins 1 membre
```

### Labels à appliquer

| Label | Couleur | Usage |
|-------|---------|-------|
| `security:high` | Rouge `#d73a4a` | Vulnérabilité critique |
| `security:medium` | Orange `#e4a11b` | Risque modéré |
| `security:low` | Jaune `#f9d71c` | Risque faible |
| `bug` | Rouge clair | Bug fonctionnel |
| `feat` | Vert | Nouvelle fonctionnalité |
| `refactor` | Bleu | Refactoring |
| `docs` | Gris | Documentation |

---

## Pull Requests

### Titre

```
[TYPE] Description courte — refs #<issue>
```

### Règles

- Toujours cibler `develop` (sauf `hotfix` → `main`)
- Au moins **1 approbation** requise avant merge
- Les tests doivent passer (CI)
- Lier la PR à l'issue correspondante avec `Closes #<numéro>`
- Pas de merge si des conflits non résolus

### Template de description PR

```markdown
## Changements apportés
- ...

## Issue liée
Closes #<numéro>

## Tests effectués
- [ ] Tests unitaires
- [ ] Test manuel sur l'environnement local
- [ ] Pas de régression observée

## Checklist sécurité
- [ ] Pas de secrets en dur dans le code
- [ ] Les inputs utilisateur sont validés/échappés
- [ ] Les vues sensibles sont protégées par authentification
```

---

## Flux de travail type (sprint)

```
1. Issue créée et affectée dans le Kanban (colonne Backlog)
2. Dev prend l'issue → déplace en "In Progress"
3. Création de la branche depuis develop
4. Commits + push
5. PR ouverte → déplace l'issue en "In Review"
6. Review par un autre membre
7. Merge dans develop → issue déplacée en "Done"
8. En fin de sprint : merge develop → main
```
