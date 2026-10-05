# Composants Claude Code tiers installés

Inventaire de ce qui est vendorisé dans `.claude/` (et ailleurs) pour les trois dépôts
`LegacyFX-Ultra-`, `LegacyFX-Ultra-Trading-App-` et `music-player-pwa`. Installation du
2026-10-04. Les sessions cloud Claude Code n'installent pas les plugins de marketplace :
tout est donc copié dans le dépôt, versions épinglées ci-dessous.

| Composant | Version (commit) | Licence | Installé dans |
|---|---|---|---|
| [ECC](https://github.com/affaan-m/ECC) | 2.2.3 (`ef648e0`), profil `developer`, **sans hooks** | MIT | agents, commandes, règles `rules/ecc/`, 126 skills ; état : `ecc/install-state.json` |
| [superpowers](https://github.com/obra/superpowers) | 6.4.2 (`8ca22db`) | MIT | 15 skills (`brainstorming`, `test-driven-development`, `systematic-debugging`, `writing-plans`…) |
| [ponytail](https://github.com/DietrichGebert/ponytail) | 4.11.0 (`2b0ea88`) | MIT | 6 skills `ponytail*` |
| [mattpocock/skills](https://github.com/mattpocock/skills) | plugin 1.3.1 (`24fe0ef`) | MIT | les 27 skills du plugin officiel (`grill-me`, `tdd`, `to-spec`, `implement`, `code-review`, `pr`…) |
| [anthropics/skills](https://github.com/anthropics/skills) | `8a1541c` | Apache-2.0 (par skill) | 14 skills : `frontend-design`, `mcp-builder`, `skill-creator`, `webapp-testing`, `canvas-design`, `doc-coauthoring`… ; LegacyFX-Ultra- n'en garde que 9 (`canvas-design`, `algorithmic-art`, `slack-gif-creator`, `theme-factory` et `internal-comms` retirés le 2026-10-05) |
| [graphify](https://github.com/Graphify-Labs/graphify) | 0.9.76 (`graphifyy` sur PyPI) | Apache-2.0 / MIT | skill `graphify` ; graphe dans `graphify-out/` (LegacyFX-Ultra-, Trading-App) ; périmètre : `.graphifyignore` |
| [claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup) | `a89c275` (méthode) | MIT | vault Obsidian `vault/` (LegacyFX-Ultra-) + commandes `/vault-resume`, `/vault-save` (3 dépôts) |
| [OmniRoute](https://github.com/diegosouzapw/OmniRoute) | image Docker `3.8.51` | MIT | service `omniroute` du `docker-compose.yml` (profil `omniroute`, hors démarrage par défaut), guides `omniroute/skills/`, skill `omniroute` (LegacyFX-Ultra- seulement) |
| [ComfyUI](https://github.com/Comfy-Org/ComfyUI) | release `v0.38.2`, code non vendorisé | GPL-3.0 | doc `comfyui/README.md` et skill `comfyui` (client `comfy_run.py`, workflow SDXL) (LegacyFX-Ultra- seulement) |

Licences des ensembles de skills : `vendor/licenses/` ; celles des skills Anthropic sont dans
leur dossier respectif.

## Adaptations locales

- **superpowers** : références `superpowers:<skill>` réécrites en `<skill>` (les skills
  vendorisés ne sont pas préfixés par un namespace de plugin).
- **ECC** : les skills de `code-review` et `pr` de Matt Pocock ont priorité sur les commandes
  ECC du même nom ; les versions ECC restent disponibles sous `/ecc-code-review` et `/ecc-pr`.
  Les agents ECC s'invoquent sans préfixe dans cette installation projet (`planner`, pas
  `ecc:planner` comme l'indique `rules/ecc/common/agents.md`, écrit pour le plugin).
- **ECC** : l'installateur ajoute `"includeCoAuthoredBy": false` aux réglages ; cette
  modification a été annulée (l'attribution des commits n'était pas dans la demande).

## Volontairement non installé

| Élément | Raison | Pour l'activer |
|---|---|---|
| Skills Anthropic `docx`, `pdf`, `pptx`, `xlsx` | licence propriétaire : copie et redistribution interdites | déjà disponibles via claude.ai (`anthropic-skills:*`) |
| Skill Anthropic `claude-api` | déjà intégré à Claude Code, tenu à jour par Anthropic | rien à faire |
| Skills Matt Pocock `misc/` et `in-progress/` | hors du plugin officiel (bêta, rarement utiles) | copier depuis le dépôt amont |
| Hooks superpowers, ponytail, graphify, ECC, autosauvegarde mémoire | un hook modifie le comportement de l'agent à chaque session : à décider par toi | voir ci-dessous |
| Scripts mémoire (`session_autosave.py`, import des chats) | code tiers exécuté par hook ou cron | copier depuis le dépôt amont après relecture |
| OmniRoute dans la session cloud | paquet npm de 546 Mo avec scripts d'installation | setup script de l'environnement : `npm install -g omniroute` |

### Activer les hooks (optionnel)

À faire en local, avec Claude Code et node/python installés :

- **ponytail** (mode « lazy senior dev » permanent) : `/plugin marketplace add DietrichGebert/ponytail`
  puis `/plugin install ponytail@ponytail`. Sans hook : `/ponytail` active le mode pour la session.
- **superpowers** (rappel des skills à chaque session) : `/plugin install superpowers@claude-plugins-official`.
- **graphify** (oriente les recherches vers le graphe) : `graphify claude install --project`
  dans le dépôt, puis commiter `.claude/settings.json` et `CLAUDE.md`.
- **ECC** (24 hooks qualité, dont des blocages d'édition) : relancer l'installateur ECC avec
  `--enable-hooks`.
- **Autosauvegarde mémoire** : hook `SessionEnd` décrit dans le README amont de
  claude-code-memory-setup, avec `VAULT_DIR` pointant sur `vault/`.

Un plugin installé en plus des copies vendorisées fait apparaître chaque skill deux fois :
supprime alors les dossiers correspondants de `.claude/skills/`.

## Mettre à jour

Recloner l'amont à la version voulue et recopier les dossiers de skills (même chemin). Pour
ECC : `node <ECC>/scripts/install-apply.js --target claude-project --profile developer --no-hooks`
depuis la racine du dépôt, puis retirer `includeCoAuthoredBy` de `.claude/settings.json` si
l'installateur l'a ajouté.
