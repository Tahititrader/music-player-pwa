---
description: Consigne la session dans la mémoire persistante (vault Obsidian) — log, décisions, tâches restantes — puis commit + push du vault.
argument-hint: "[titre court de la session]"
---

# /vault-save — consigner la session

## 1. Localiser le vault et le projet

Même résolution que `/vault-resume` : `$VAULT_DIR`, `<dépôt>/vault`,
`<dépôt>/../LegacyFX-Ultra-/vault`, puis `/home/user/LegacyFX-Ultra-/vault`.
Projet = nom du dossier du dépôt où le travail principal a eu lieu ; travail réparti sur
plusieurs dépôts : un log dans `<vault>/logs/`. Relis la section « Règles pour Claude » de
`<vault>/README.md` avant d'écrire.

## 2. Écrire le log de session

Fichier `<vault>/<projet>/logs/YYYY-MM-DD-<slug>.md` (date du jour, slug kebab-case tiré de
`$ARGUMENTS` ou du sujet principal ; ajoute `-2`, `-3` si le fichier existe). Pars de
`<vault>/templates/session-log.md` :

- frontmatter complet (`title`, `tags: [session-log, <projet>]`, `created`, `updated`,
  `status`, `type: log`, `project`, `branch`)
- **Objectif** de la session
- **Fait** : changements concrets, avec fichiers, commits et PR
- **Décisions** : ce qui a été tranché et pourquoi
- **À faire** : tâches restantes, priorisées, chacune actionnable
- **Liens** : au moins 2 wikilinks qualifiés (`[[<projet>/index|...]]`,
  `[[<projet>/architecture/decisions|...]]`, notes permanentes touchées)

Ne recopie que des faits vérifiés dans la session (sorties de commandes, diff, PR).

## 3. Mettre à jour la mémoire durable

- Décision structurante : nouvelle entrée en haut de `<vault>/<projet>/architecture/decisions.md`
  (gabarit `templates/decision.md`).
- Connaissance réutilisable au-delà de cette session : note atomique dans `<vault>/permanent/`.
- Ajoute le log à la section « Journal » de `<vault>/<projet>/index.md` ; mets à jour `updated`.

## 4. Commit + push

Dans le dépôt qui contient le vault, n'ajoute que `vault/` :

```bash
git add vault
git commit -m "docs(vault): <projet> — <titre>"
git push -u origin "$(git branch --show-current)"
```

Jamais de secret, token ou donnée personnelle dans une note. Si le push échoue, dis-le : le
log reste dans le working tree et doit être poussé avant la fin de la session.
