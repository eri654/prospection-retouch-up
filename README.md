# Prospection terrain Retouch'Up

Ce dépôt héberge les feuilles de route consultables sans compte Claude.

## Feuilles disponibles

- [Côte d'Azur — Nice, Cannes, Antibes](cote_azur_2026.html) : **une seule page**, 47 hôtels, 144 personnes nommées et 12 fiches établissement sans personne nommée. Elle réunit les quatre listes : Nice 62, Cannes 47, Antibes 11 et hôtels génériques 99 inscriptions. Les 219 inscriptions correspondent à 156 fiches distinctes, car certaines figurent dans plusieurs listes.
- [Paris · EquipHotel 2026](paris_equiphotel_2026.html) : 21 hôtels et 47 contacts.

Les anciennes adresses Nice, Cannes et Antibes redirigent vers la feuille Côte d'Azur avec le filtre de zone correspondant.

La page Côte d'Azur reprend le modèle terrain Paris. Elle combine la liste de prospection du 16 septembre, les quatre campagnes consultées le 18 septembre 2026 et les fiches du portail HubSpot Retouch'Up. Toutes les fiches des campagnes sont visibles, y compris les rattachements à vérifier et les fiches d'hôtel sans nom de personne. Une présence dans l'inventaire ne vaut pas autorisation de contacter : relire la fiche CRM avant toute action. Aucun état de campagne, email nominatif, mobile ou clé API n'est publié.

Les hôtels vérifiés ont leur adresse, un lien vers le site source et une recherche Google Maps. Les fiches nommées ont un accès LinkedIn et HubSpot, direct quand il est disponible, sinon une recherche de repli signalée par `?`. Les coches, dates et notes sont enregistrées uniquement dans le navigateur utilisé et ne se synchronisent pas entre utilisateurs ou appareils.

Les données publiques structurées sont dans [`data/cote_azur_complete_2026.json`](data/cote_azur_complete_2026.json). Après modification, régénérer la page et les anciennes adresses avec `python render_cote_azur.py`, vérifier le rendu, puis publier.
