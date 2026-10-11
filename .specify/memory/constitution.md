# Constitution du Lecteur de musique PRO

## Core Principles

### I. La musique reste sur l'appareil (NON NÉGOCIABLE)

- Les fichiers audio choisis par l'utilisateur (`showOpenFilePicker`, `<input type="file">`) MUST
  être lus localement ; ils MUST NOT être envoyés à un serveur ou à une API.
- Rien ne quitte l'appareil sans une action explicite de l'utilisateur. Les seules requêtes
  sortantes autorisées sont les appels aux fournisseurs d'IA qu'il a configurés lui-même.
- Aucune télémétrie, aucun traceur, aucune police ou script tiers chargé depuis un CDN.

Raison : un lecteur de musique n'a aucune raison de connaître la bibliothèque de son utilisateur.

### II. Fonctionne hors ligne

- La lecture, l'égaliseur, le visualiseur et les thèmes MUST fonctionner sans réseau une fois
  l'app installée.
- Le service worker MUST mettre en cache tout le shell de l'app (`APP_SHELL`) ; toute modification
  d'un fichier du shell MUST incrémenter `CACHE_NAME`, sinon les utilisateurs gardent l'ancienne
  version.
- Les fonctions d'IA sont facultatives : leur absence ou leur échec MUST NOT bloquer ni ralentir la
  lecture.

Raison : une PWA installée qui ne marche pas hors ligne n'est qu'un favori.

### III. Clés d'IA apportées par l'utilisateur

- Les clés (OpenAI, Perplexity, Gemini, Azure, ElevenLabs) sont fournies par l'utilisateur. Elles
  MUST rester sur son appareil et MUST être envoyées uniquement au fournisseur qu'elles concernent.
- Aucune clé MUST NOT être commitée, codée en dur ou écrite dans les journaux de la console.
- Les champs de clé MUST être de type `password`, et l'utilisateur MUST pouvoir les effacer.
- Comme les clés vivent dans `localStorage`, tout contenu non fiable (noms de fichiers, métadonnées,
  réponses d'IA) MUST être inséré avec `textContent`, jamais avec `innerHTML`.

Raison : une faille XSS dans une page qui stocke des clés d'API revient à les publier.

### IV. Zéro dépendance, zéro build

- L'app MUST rester en HTML, CSS et JavaScript natifs, servie telle quelle, sans bundler, framework
  ni `node_modules`.
- Toute dépendance ou étape de build MUST être justifiée dans une spec et approuvée par un
  amendement MINOR de cette constitution.

Raison : un fichier qui s'ouvre partout ne casse jamais à cause d'une mise à jour de dépendance.

### V. Accessible et pilotable au clavier

- Chaque commande de lecture MUST avoir un nom accessible (`aria-label` ou texte visible) et être
  atteignable au clavier ; les raccourcis clavier MUST NOT intercepter la saisie dans un champ.
- Les contrastes de chaque thème MUST respecter WCAG 2.2 AA.
- Le visualiseur MUST respecter `prefers-reduced-motion`.

Raison : un lecteur de musique sert aussi à qui ne voit pas l'écran ou ne tient pas la souris.

### VI. Fluide sur mobile

- Le thread audio MUST NOT être bloqué : pas de calcul lourd synchrone pendant la lecture.
- Le visualiseur MUST utiliser `requestAnimationFrame` et s'arrêter quand la page est cachée.
- Les réglages et la session (`pwaMusic.settings`, `pwaMusic.session`) MUST se lire sans planter
  si le stockage est vide, corrompu ou bloqué.

Raison : un saut audio ou une batterie vidée font désinstaller l'app plus vite qu'un bug visible.

## Contraintes techniques

- Fichiers servis : `index.html`, `sw.js`, `manifest.webmanifest`, `icons/`. Un nouveau fichier du
  shell MUST être ajouté à `APP_SHELL`.
- L'app MUST être servie en HTTPS (ou `localhost`) : le service worker et la File System Access API
  l'exigent.
- `showOpenFilePicker` n'existe pas partout : le repli `<input type="file">` MUST rester disponible.

## Workflow de développement et quality gates

- Avant tout commit : ouvrir l'app, lire un fichier, recharger hors ligne et vérifier que la console
  ne montre aucune erreur.
- Quand des tests automatisés existent, ils MUST passer avant fusion ; un audit Lighthouse PWA et
  accessibilité SHOULD être lancé sur chaque changement d'interface.
- Une nouvelle fonctionnalité MUST partir d'une spec Spec Kit (`/speckit-specify`) et son plan MUST
  passer le « Constitution Check » contre les principes I à VI ; toute dérogation MUST être justifiée
  dans *Complexity Tracking*.
- Commits au format conventionnel ; l'interface est rédigée en français.

## Governance

- Cette constitution prime sur toute autre pratique du dépôt.
- Amendement : via `/speckit-constitution`, dans un commit dédié qui explique le changement et ses
  raisons.
- Versionnage sémantique : MAJOR pour retirer ou redéfinir un principe, MINOR pour ajouter un
  principe ou une section, PATCH pour une clarification.
- Conformité : chaque revue de code et chaque plan Spec Kit vérifient les principes I à VI. Le
  principe I ne souffre aucune dérogation.

**Version**: 1.0.0 | **Ratified**: 2026-10-11 | **Last Amended**: 2026-10-11
