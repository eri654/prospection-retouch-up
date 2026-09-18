# Prospection terrain Retouch'Up

Ce dépôt héberge les feuilles de route consultables sans compte Claude.

## Feuilles disponibles

- [Côte d'Azur — Nice, Cannes, Antibes](cote_azur_2026.html) : **une seule page**, 68 hôtels, 122 personnes nommées et 34 fiches établissement sans personne nommée. Elle réunit les quatre listes : Nice 62, Cannes 47, Antibes 11 et hôtels génériques 99 inscriptions. Les 219 inscriptions correspondent à 156 fiches distinctes, car certaines figurent dans plusieurs listes.
- [Paris · EquipHotel 2026](paris_equiphotel_2026.html) : 21 hôtels et 47 contacts.

Les anciennes adresses Nice, Cannes et Antibes redirigent vers la feuille Côte d'Azur avec le filtre de zone correspondant.

La page Côte d'Azur reprend l'en-tête, les filtres, les étapes, les liens par hôtel et contact, les cases et les champs de visite de la feuille Paris. Elle combine la liste de prospection, les quatre campagnes consultées le 18 septembre 2026, les fiches du portail HubSpot Retouch'Up et les rattachements recherchés sur LinkedIn. Les personnes sans hôtel local vérifiable restent dans l'annexe de la même page. Une présence dans l'inventaire ne vaut pas autorisation de contacter : relire la fiche CRM avant toute action. Aucun état de campagne, email nominatif, mobile ou clé API n'est publié.

Les hôtels vérifiés ont leur adresse, un lien vers le site source et une recherche Google Maps. Les fiches nommées ont un accès LinkedIn et HubSpot, direct quand il est disponible, sinon une recherche de repli signalée par `?`. Les coches, dates et notes sont enregistrées uniquement dans le navigateur utilisé et ne se synchronisent pas entre utilisateurs ou appareils.

Chaque hôtel dispose aussi d'une case « Avis Tripadvisor & signal Retouch’Up ». Sept hôtels ont un résumé d'avis datés et sourcés avec un angle de visite ; les autres ont un lien de recherche et un statut explicite « Pas de signal sourcé ». Ces résumés sont sélectifs : ils ne prouvent ni l'état actuel de l'hôtel ni un besoin confirmé. Les avis anciens sont signalés comme tels.

Les données publiques structurées sont dans [`data/cote_azur_complete_2026.json`](data/cote_azur_complete_2026.json) et les résumés d'avis dans [`data/cote_azur_tripadvisor_2026.json`](data/cote_azur_tripadvisor_2026.json). Après modification, régénérer la page et les anciennes adresses avec `python render_cote_azur.py`, vérifier le rendu, puis publier.
