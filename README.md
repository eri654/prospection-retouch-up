# Prospection terrain Retouch'Up

Ce dépôt héberge les feuilles de route consultables sans compte Claude.

## Feuilles disponibles

- [Nice et aéroport](nice_2026.html) : 25 hôtels et 5 placements de contacts.
- [Cannes et Mandelieu](cannes_2026.html) : 12 hôtels et 11 placements de contacts.
- [Antibes et Sophia Antipolis](antibes_2026.html) : 10 hôtels et 10 placements de contacts.
- [Paris · EquipHotel 2026](paris_equiphotel_2026.html) : 21 hôtels et 47 contacts.

Les pages Côte d'Azur reprennent le modèle terrain Paris. Elles combinent la liste de prospection Côte d'Azur du 16 septembre, les campagnes géographiques consultées le 18 septembre 2026 et les fiches du portail HubSpot Retouch'Up. Les hôtels au nom ambigu, les rattachements incertains et les personnes désinscrites sont exclus des contacts affichés. Un hôtel sans contact confirmé reste visible avec le repère « À qualifier ». Le repère « Contact identifié » signale une association trouvée dans les sources ; ce n'est pas un score commercial. Les dates restent à planifier.

Chaque contact affiché a un lien LinkedIn et un bouton HubSpot. Un point d'interrogation signale une recherche de repli quand le profil ou la fiche n'est pas confirmé. Chaque hôtel a une recherche Google Maps avec son adresse, un lien LinkedIn vers une personne associée ou une recherche clairement signalée, et une source d'adresse. La page publique n'inclut ni adresse email nominative, ni mobile, ni commande de campagne, ni clé API.

Les coches, dates et notes sont enregistrées uniquement dans le navigateur utilisé. Elles ne se synchronisent pas entre utilisateurs ou appareils.

Les données publiques structurées sont dans [`data/cote_azur_2026.json`](data/cote_azur_2026.json). Après modification de ce fichier, régénérer les trois pages avec `python render_cote_azur.py`, vérifier leur rendu, puis publier.
