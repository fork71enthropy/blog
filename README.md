# blog

## Prochains projets
```
-Scraper les offres d'emploi d'un secteur chaque matin et filtrer selon tes critères
-Lire tes emails, identifier ceux qui nécessitent une réponse urgente et les trier
```

### I- Scraper d'offres d'emploi d'un secteur et filtre selon les critères
```
1- On commence par une version minimaliste histoire d'avoir quelque chose de pésentable ce soir. Le site cible 
est welcome to the jungle car ses CGU nous sont plus favorables (scrappers). Welcome to the jungle change 
régulièrement la structure de ses pages donc il faut maintenir le scrapper à jours. Le site charge ses offres
via javascript, ce qui signifie que beautifullsoup et requests ne seront pas suffisants ! Il faudra ajouter
playwright pour piloter un vrai navigateur !
-- Stack de base : 
Playwright — pour piloter le navigateur et récupérer le HTML rendu
BeautifulSoup — pour parser ce HTML et extraire les offres
Python — pour filtrer et afficher les résultats
```