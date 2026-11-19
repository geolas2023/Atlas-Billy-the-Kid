# Atlas géohistorique — Billy the Kid (1859–1881)

Atlas Web interactif (MapLibre GL JS) avec une carte, une timeline et un « dossier » documentaire. Il suit la vie d'Henry McCarty, dit Henry Antrim, dit William H. Bonney, dit Billy the Kid : de New York à Fort Sumner, l'enfance errante, l'Arizona, la guerre du comté de Lincoln, la cavale, la capture, le procès, l'évasion et la mort. La mécanique est celle de l'[Atlas Iberville](https://github.com/geolas2023/Atlas-Iberville), avec un habillage de carte ancienne du Territoire. Une étoile de shérif sert d'emblème, et un cavalier ou une locomotive animent la visite.

> **Sources des données** :
> - Robert M. Utley, *Wanted: The Outlaw Lives of Billy the Kid and Ned Kelly*, New Haven, Yale University Press, 2015 (source principale).
> - Michael Wallis, *Billy the Kid: The Endless Ride*, New York, W. W. Norton, 2007.
> - Pat F. Garrett, *The Authentic Life of Billy, the Kid*, Santa Fe, 1882.
>
> Les renvois donnent la page du PDF de l'édition numérique (champ `sources`). Les descriptions sont des résumés rédigés pour l'atlas. Une `note` critique signale les localisations approximatives ou hypothétiques et les divergences entre auteurs.

## Structure

```
index.html            page principale
css/style.css         mise en page et habillage (carte ancienne, cartouche, dossier)
js/fonds.js           fonds de carte : Parchemin (par défaut), Plan moderne, Satellite
js/app.js             carte, couches, timeline, fiches
js/visite.js          visite animée (le cavalier ou le train suit les routes)
data/lieux.geojson    41 lieux (points)
data/trajets.geojson  12 routes (lignes)
images/               étoile de shérif, cavalier, locomotive, rose des vents, ornements
```

## Modèle d'attributs (compatible QGIS)

| Champ | Type | Exemple | Rôle |
|---|---|---|---|
| `id` | texte | `L16` / `T09` | identifiant stable (L = lieu, T = trajet) |
| `nom` | texte | `Lincoln : le shérif Brady abattu` | libellé |
| `debut`, `fin` | réel | `1878.2466` | dates en année décimale (timeline, visite animée) |
| `date_edtf` | texte | `1878-04-01` | date telle que documentée ([EDTF](https://www.loc.gov/standards/datetime/) : `~` approximatif) |
| `precision` | texte | `jour` / `mois` / `circa` | lieux : précision de la date |
| `certitude` | texte | `certaine` / `approximative` / `hypothetique` | certitude de la localisation ou du tracé |
| `categorie` | texte | `fusillade`, `prison`, `proces`, `refuge`, `naissance`, `vie`, `mort` | lieux : nature de l'événement |
| `mode` | texte | `cheval` / `train` | trajets : moyen de déplacement |
| `description`, `note`, `sources` | texte | | résumé, note critique, référence |

La timeline avance par année de 1859 à 1872, puis par mois de 1873 à 1881.

## Génération des données

Les deux GeoJSON sont produits par `scripts/build_btk.py` (`python3 scripts/build_btk.py .`), où chaque fiche est rédigée d'après les sources ci-dessus. Pour une retouche ponctuelle, on peut éditer directement les GeoJSON (par exemple dans QGIS).

Olivier J. Caron, Département de géographie, UQAM.
