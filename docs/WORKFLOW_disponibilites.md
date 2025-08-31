# Workflow disponibilites (Jalon 16)

Etat: PENDING -> APPROVED/REJECTED
Acteurs: user (demande), manager (approve/reject).
Contrainte: chevauchement interdit entre slots APPROVED du meme user.
Stockage: UTC naive en DB, affichage local en FE.
Sequence:

1. User PUT /users/{id}/profile
2. User POST /availabilities
3. Manager POST /availabilities/{id}:approve ou :reject
4. FE affiche GET /users/{id}/calendar
