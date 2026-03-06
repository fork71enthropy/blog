# 📖 Comment étudier un projet open source

> Un guide pratique pour naviguer dans un grand codebase sans se noyer.

---

## Mindset de départ

Lire du code existant est un skill différent d'en écrire. Le but n'est **pas** de tout comprendre — c'est de construire une **carte mentale** suffisante pour naviguer et poser des questions précises. Même les développeurs seniors ne lisent pas un projet en entier avant de contribuer.

---

## Étape 1 — Lire les fichiers de surface (pas le code)

Avant d'ouvrir un seul fichier `.js`, `.py` ou `.cpp`, lis les fichiers de documentation à la racine du projet. Ils sont là pour ça.

| Fichier | Ce qu'il t'apprend |
|---|---|
| `README.md` | La vision, l'objectif, comment installer |
| `CONTRIBUTING.md` | Comment le projet est structuré, les conventions |
| `CHANGELOG.md` | Ce qui a changé récemment → révèle les priorités |
| `ARCHITECTURE.md` | La vue d'ensemble technique (si présent) |
| `SECURITY.md` | Le modèle de sécurité et les choix de design |
| `LICENSE` | Sous quelle licence tu peux utiliser/modifier le code |

**Objectif :** comprendre *pourquoi* ce projet existe et *pour qui*.

---

## Étape 2 — Comprendre la structure des dossiers

Avant de lire une ligne de code, passe 10 minutes à explorer l'arborescence. La structure des dossiers reflète l'architecture mentale du projet.

```bash
# Afficher l'arborescence sur 2 niveaux
tree -L 2

# Ou avec find
find . -maxdepth 2 -type d
```

**Questions à te poser :**
- Où est le code principal ? (`src/`, `lib/`, `core/`...)
- Où sont les tests ? (`test/`, `__tests__/`, `spec/`...)
- Y a-t-il des modules séparés ? (`packages/`, `modules/`...)
- Où sont les configs ? (`config/`, fichiers `.json` à la racine...)

**Exemple avec OpenClaw :**
```
apps/        → apps natives iOS, Android, macOS
src/         → cœur TypeScript du Gateway
packages/    → modules réutilisables partagés
extensions/  → système de plugins
skills/      → compétences injectées dans l'agent
```
Juste cette structure, tu comprends déjà que c'est un projet multi-plateforme avec un cœur central.

---

## Étape 3 — Lire le fichier de dépendances

Le fichier de dépendances (`package.json`, `requirements.txt`, `Cargo.toml`, `CMakeLists.txt`...) est une mine d'or.

**Ce qu'il révèle :**
- Les bibliothèques utilisées → les choix techniques
- Les scripts disponibles (`build`, `test`, `dev`...)
- La version minimale du runtime requis
- Les dépendances de dev vs production

**Exemple :**
```json
{
  "scripts": {
    "build": "tsdown",
    "test": "vitest",
    "gateway:watch": "tsx src/gateway.ts --watch"
  }
}
```
→ Tu sais maintenant comment lancer le projet, le builder et le tester.

---

## Étape 4 — Explorer l'historique Git

L'historique Git raconte l'histoire du projet. C'est souvent plus instructif que le code lui-même.

```bash
# Les 20 derniers commits
git log --oneline -20

# Qui contribue le plus
git shortlog -sn --all

# Quels fichiers changent le plus souvent (= les plus importants)
git log --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20

# Les commits récents sur un fichier spécifique
git log --oneline -- src/gateway.ts
```

**Ce que tu cherches :**
- Les fichiers modifiés le plus souvent → les plus critiques
- Les messages de commit → comprendre les décisions passées
- Les auteurs principaux → savoir qui contacter si tu as une question

---

## Étape 5 — Lire les tests avant le code

Les tests sont la meilleure documentation d'un projet. Ils décrivent **exactement** ce que le code est censé faire, avec des exemples concrets.

```bash
# Trouver tous les fichiers de test
find . -name "*.test.ts" -o -name "*.spec.ts" -o -name "*.test.py"
```

**Méthode :**
1. Trouve les tests du module qui t'intéresse
2. Lis les descriptions (`describe`, `it`, `test`)
3. Regarde les inputs/outputs des cas de test
4. *Ensuite seulement* va lire le code correspondant

---

## Étape 6 — Suivre un flux, pas un fichier

C'est l'étape la plus importante. **Ne lis jamais fichier par fichier** — tu vas te perdre. À la place, pose-toi une question concrète et suis le code qui y répond.

**Exemples de questions à suivre :**
- *"Que se passe-t-il quand un message WhatsApp arrive ?"*
- *"Comment l'agent construit-il sa réponse ?"*
- *"Où sont stockées les sessions ?"*
- *"Comment un plugin est-il chargé ?"*

**Méthode pour suivre un flux :**

```
Point d'entrée → Fonction appelée → Modules impliqués → Données échangées
```

Utilise les outils de ton éditeur :
- **"Go to definition"** (F12 dans VSCode)
- **"Find all references"** (Shift+F12)
- **"Search in files"** pour trouver où une fonction est appelée

---

## Étape 7 — Dessiner ta carte mentale

Au fur et à mesure, note ce que tu comprends. Peu importe le format — texte, schéma, mindmap. L'important c'est d'externaliser ta compréhension pour ne pas devoir tout re-déduire à chaque session.

**Template simple :**
```
## Composant X
- Rôle : ...
- Fichiers principaux : ...
- Entrées : ...
- Sorties : ...
- Dépend de : ...
- Utilisé par : ...
- Questions encore ouvertes : ...
```

---

## Étape 8 — Installer et faire tourner le projet

Rien ne remplace l'exécution du code. Installe le projet dans un environnement isolé (VM, Docker, environnement virtuel...) et observe-le en action.

```bash
# Lancer en mode debug/verbose si disponible
openclaw gateway --verbose

# Regarder les logs en temps réel
tail -f ~/.openclaw/logs/gateway.log
```

**Ce que ça t'apprend :**
- Ce qui se passe réellement vs ce que tu avais imaginé
- Les erreurs concrètes et comment le projet les gère
- Les fichiers créés sur le disque, les ports ouverts...

> ⚠️ Pour un projet comme OpenClaw qui touche à tes messageries et à ton shell, fais-le dans une VM ou sur une machine dédiée la première fois.

---

## Étape 9 — Faire une petite modification

La meilleure façon de comprendre un code est de le casser (dans un environnement de test). Essaie de petites modifications :

- Ajouter un `console.log` pour voir ce qui passe dans une fonction
- Changer une valeur de config et observer l'effet
- Désactiver un module et voir ce qui plante

C'est souvent en cassant quelque chose qu'on comprend vraiment comment ça fonctionne.

---

## Étape 10 — Lire les issues et pull requests ouvertes

Les issues GitHub sont une fenêtre sur les problèmes connus, les décisions en cours, et les zones complexes du code.

**Ce qu'il faut lire :**
- Les issues avec le label `good first issue` → les zones bien documentées
- Les issues `bug` → les parties fragiles du code
- Les grandes PR ouvertes → les changements architecturaux en cours
- Les discussions dans les PR mergées → le raisonnement derrière les choix

---

## Récapitulatif — L'ordre recommandé

```
1. README + CONTRIBUTING + CHANGELOG
         ↓
2. Structure des dossiers
         ↓
3. Fichier de dépendances (package.json, etc.)
         ↓
4. Historique Git (fichiers les plus modifiés)
         ↓
5. Tests (avant le code)
         ↓
6. Suivre un flux concret
         ↓
7. Dessiner ta carte mentale
         ↓
8. Faire tourner le projet
         ↓
9. Petites modifications
         ↓
10. Issues et pull requests
```

---

## Outils utiles

| Outil | Usage |
|---|---|
| `git log --oneline` | Historique rapide |
| `git log --name-only` | Fichiers modifiés par commit |
| `grep -r "nomFonction" src/` | Trouver où une fonction est utilisée |
| `tree -L 2` | Arborescence des dossiers |
| VSCode + extension GitLens | Navigation dans l'historique |
| [DeepWiki](https://deepwiki.com) | Documentation IA générée sur des repos GitHub |
| [sourcegraph.com](https://sourcegraph.com) | Recherche dans des projets open source |

> 💡 **Astuce DeepWiki :** OpenClaw lui-même référence `deepwiki.com/openclaw/openclaw` dans son README — c'est un outil qui génère automatiquement une documentation navigable d'un repo GitHub. Très utile pour les grands projets.

---

## Ce qu'il ne faut pas faire

- ❌ Lire chaque fichier de haut en bas dans l'ordre alphabétique
- ❌ Vouloir tout comprendre avant de toucher au code
- ❌ Ignorer les tests
- ❌ Négliger l'historique Git
- ❌ Travailler directement sur `main` sans branche isolée

---

*Un grand projet open source ne se comprend pas en une session. C'est un processus itératif — chaque passage te donne une carte plus précise.*