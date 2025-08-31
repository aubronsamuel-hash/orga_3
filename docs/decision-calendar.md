# Decision: Calendrier (Jalon 14)

Lib: FullCalendar (OSS) pour month/week/day, timeline simple maison (CSS Grid) pour eviter licence premium.
DnD & Resize: FullCalendar interaction.
Polling: 30s. SSE optionnel a activer au Jalon 30 (updates live).
Mapping status -> style:

- INVITED: info (bleu)
- ACCEPTED: success (vert)
- DECLINED: danger (rouge)
- CANCELLED: muted (gris)
  Filtres: status + user/org/project. Timezone select utilisateur.

CI Gates (J14):

- e2e calendrier (Playwright)
- bundle budget strict (size-limit)
