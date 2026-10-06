---
description: Recharge la mémoire persistante (vault Obsidian) du projet courant — derniers logs de session, décisions en vigueur, prochaines étapes.
argument-hint: "[projet] (défaut : nom du dossier du dépôt courant)"
---

# /vault-resume — reprendre là où on s'était arrêté

Ne modifie aucun fichier pendant cette commande.

## 1. Localiser le vault

Prends le premier chemin qui existe :

1. `$VAULT_DIR`
2. `<racine du dépôt courant>/vault` (dépôt LegacyFX-Ultra-)
3. `<racine du dépôt courant>/../LegacyFX-Ultra-/vault` (dépôts clonés côte à côte)
4. `/home/user/LegacyFX-Ultra-/vault` (sessions cloud multi-dépôts)

Aucun trouvé : dis-le en une ligne et propose de cloner `Tahititrader/LegacyFX-Ultra-` à côté
du dépôt courant. Ne crée pas de vault ailleurs.

## 2. Choisir le projet

`$ARGUMENTS` s'il est fourni, sinon le nom du dossier du dépôt courant
(`LegacyFX-Ultra-`, `LegacyFX-Ultra-Trading-App-`, `music-player-pwa`). Le dossier du projet
dans le vault porte exactement ce nom. Session multi-dépôts sans argument : demande lequel,
ou résume les trois en une ligne chacun.

## 3. Lire, dans cet ordre, sans tout relire

1. La section « Règles pour Claude » de `<vault>/README.md` (si pas déjà lue dans la session)
2. `<vault>/<projet>/index.md`
3. `<vault>/<projet>/architecture/decisions.md` (les 5 entrées les plus récentes suffisent)
4. Les 3 logs les plus récents de `<vault>/<projet>/logs/` (tri par nom `YYYY-MM-DD-...`),
   puis le plus récent de `<vault>/logs/` s'il est plus récent qu'eux
5. Si `graphify-out/GRAPH_REPORT.md` existe dans le dépôt : uniquement la section « God Nodes »
6. `git log --oneline -10` du dépôt, pour repérer le travail fait depuis le dernier log

## 4. Restituer, en français et court

- **État actuel** : ce qui est fait, ce qui est en cours
- **Décisions en vigueur** : avec le wikilink de la note source
- **Prochaines étapes** : la liste « À faire » du dernier log, priorisée et actionnable
- **Points de vigilance** : risques, dettes, questions ouvertes, commits non consignés
