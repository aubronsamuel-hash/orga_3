# Roadmap Coulisses Crew (base Codex)

> Source de verite. A LIRE avant toute PR. ASCII uniquement. Windows-first. Zero secret dans le repo et les workflows.

J17: Typing stabilise: `mypy_path=backend`, ajout `backend/tests/__init__.py`, `backend/app/__init__.py`. Runner PowerShell `.\\PS1\\mypy.ps1`.

## Objectifs
- Livrer un MVP fiable (backend + frontend) puis durcir la securite a la fin.
- CI verte a chaque jalon, petites etapes atomiques pour eviter la casse.
- Documentation a jour: mettre a jour les README a CHAQUE jalon (root + backend + frontend + ops).

## Conventions globales
- Langue: francais sans accents (ASCII uniquement).
- OS dev: Windows 10/11 + PowerShell. Scripts dans `PS1/`.
- Branches: `main` (stable), `feat-*` (PR avec CI verte). Pas de commit direct sur `main`.
- Environnements: `local` (Docker Desktop), `staging` (VM Docker + Caddy), `prod` (idem staging).
- Dossiers standards:
  - `backend/` FastAPI + Alembic + tests Pytest
  - `frontend/` React + Vite + Tailwind + shadcn + tests Vitest/Playwright
  - `deploy/` compose files, Caddy, k6, Prometheus, Grafana, Loki, alert rules
  - `docs/` roadmap, runbooks, schemas, READMEs
  - `PS1/` scripts PowerShell Windows-first
- Dependances: lockfiles commit (package-lock.json, etc.), npm ci.
- Terminologie:
  - **user** = personne planifiable (CDI, CDD, intermittent, freelance).
  - **account** = identite de connexion; un account appartient a un user.
  - **org** = organisation/entreprise (multi-tenant) a laquelle appartiennent users + accounts.

## Pile technique cible
- Backend: Python 3.13, FastAPI (async), SQLAlchemy, Alembic, Pydantic, Uvicorn/Gunicorn
- DB: Postgres 16 (+ extensions FTS + pg_trgm), Redis 7
- Cache/Queue: Redis (cache), RQ (background jobs) + APScheduler (taches planifiees)
- Storage: S3-compatible (MinIO en dev) pour documents (contrats, AEM, exports) avec pre-signed URLs
- Antivirus: ClamAV (scan des uploads en arriere-plan)
- Frontend: React + Vite + TypeScript + Tailwind + shadcn/ui, Router, TanStack Query, Zustand, Storybook, Playwright, Vitest, ESLint
- UI calendrier: FullCalendar ou dnd-kit custom (DnD, resize)
- Temps reel: SSE (par defaut) ou WebSocket pour updates planning/notifications
- Obs: OpenTelemetry (traces) + Prometheus + Grafana + Loki
- DAST: OWASP ZAP (baseline)
- Supply chain: syft SBOM, trivy scans, pip-audit, npm audit, cosign (keyless), SLSA provenance
- Connecteurs: ICS export, Google/Microsoft Calendar (optionnel), SMTP, Telegram

## Rituels Codex
- Toujours lire `docs/roadmap.md` avant d agir.
- A CHAQUE JALON: proposer patchs + mise a jour des README concernes.
- Toujours produire: PROMPT_CODEX et MESSAGE_AGENT.
- Si CI echoue: lire logs, pousser correctifs dans la meme PR.

## CI (vue d ensemble)
Jobs standard (les activer par jalon):
- lint-python (ruff) / type-python (mypy)
- test-python (pytest)
- lint-frontend (eslint/tsc) / test-frontend (vitest)
- build-frontend (vite) avec bundle budget
- e2e (playwright) headless
- sbom (syft) / deps-audit (pip-audit, npm audit)
- vuln-scan-fs (trivy fs) / vuln-scan-image (trivy image)
- sign-images (cosign) + provenance (slsa attest)
- dast (zap-baseline) en staging
- perf (k6 smoke + baseline)
- obs-smoke (prometheus scrape ok, loki logs ok, grafana up)

---

# Jalons (etapes atomiques)

Chaque jalon ci-dessous contient: But, Livrables, Fichiers, Commandes, Tests, CI Gates, Docs, Acceptance.

## Jalon 0 - Socle repo et outillage
But: arbo, tooling, scripts PS.
Livrables: .editorconfig, .gitattributes, .gitignore, LICENSE, CODEOWNERS, PS1 de base, .env.example.
Commandes: `pwsh -NoLogo -NoProfile -File PS1/init_repo.ps1`
Tests: n/a
CI Gates: echo pipeline, lint root basique.
Docs: README root initial.
Acceptance: repo clonable, scripts OK.

## Jalon 1 - Backend skeleton + healthz
But: FastAPI minimal, /healthz.
Livrables: app/main.py, pyproject, tests healthz.
Tests: `pytest -q`
CI Gates: ruff, mypy, pytest.
Docs: backend/README.
Acceptance: /healthz 200 JSON.

## Jalon 2 - DB + Alembic
But: Postgres 16, Alembic init.
Livrables: app/db.py, alembic/ + migration head.
Tests: migration up/down.
CI Gates: pytest, mypy.
Docs: Alembic how-to.
Acceptance: `alembic upgrade head` OK.

## Jalon 3 - Modeles metier
But: multi-tenant complet et objets metier centraux, incluant **projects** et workflow d invitation/acceptation.
Livrables: 
- Tables: orgs, accounts, users, user_skills, user_tags, **projects**, missions, mission_roles, assignments, availability, audit_log, **invitations**.
- Relations: `missions.project_id` (nullable au debut, puis obligatoire via migration si decide), `assignments.mission_id`, `assignments.user_id`.
- Enums: `assignment_status` = INVITED | ACCEPTED | DECLINED | CANCELLED ; `project_status` = DRAFT | ACTIVE | ARCHIVED.
- Employment: champs `employment_type` (CDI/CDD/Intermittent/Freelance), `rate_profile`, `legal_ids`, `documents` metas.
- Index: recherche texte sur users, indexes par date pour missions/availability, composite pour assignments (mission_id,user_id,status).
Tests: CRUD unitaires + contraintes + recherches + invariants (unicite assignment par mission/user actifs).
CI Gates: ruff, mypy, pytest.
Docs: ERD ascii + decisions (naming, normalisation, perf, RGPD).
Acceptance: CRUD verts + contraintes appliquees.

## Jalon 4 - Auth reelle (JWT + refresh + cookies httpOnly)
But: auth sans mock, usable direct.
Livrables: OAuth2 password/bearer, tokens access+refresh, cookies httpOnly, password hashing, reset par email.
Tests: login/logout/refresh/reset, CORS et CSRF notes.
CI Gates: pytest auth, coverage >=60%.
Docs: securite (flux, cookies, CSRF), env SMTP.
Acceptance: login fonctionne en dev (MailPit) et staging/prod (SMTP veritable).

## Jalon 5 - RBAC et multi-tenant
But: roles (owner, admin, manager, tech), org isolation.
Livrables: tables org_memberships, policies service-layer, dependences FastAPI.
Tests: access control routes.
CI Gates: pytest.
Docs: matrice roles x actions.
Acceptance: enforcement OK.

## Jalon 6 - Endpoints metier v1
But: API v1 exploitable en prod (sans mock), incluant projets et invitations.
Livrables: routes REST v1 + schemas + services + validations:
- `/v1/projects` (CRUD, archiver, **/projects/{id}/missions:bulk_create** pour creer 10+ missions d un coup)
- `/v1/missions` (CRUD, duplication, publication, recherche)
- `/v1/assignments` (affectations; champs `status` = INVITED/ACCEPTED/DECLINED/CANCELLED; validations de collisions)
- `/v1/invitations` (creer, revoquer, **accept/decline** via token signe; webhooks internes pour MAJ planning)
- `/v1/users` (CRUD, recherche, skills/tags, documents meta)
- `/v1/availability` (CRUD + fenetres recurrentes)
- `/v1/conflicts` (detect service: overlaps, heures max, repos insuffisant)
- `/v1/rates` (profils de remuneration par user/role/mission)
- `/v1/orgs` (membres, roles)
Tests: tests fonctionnels couvrant flux CRUD, **invitation -> accept/decline** et validations assignments.
CI Gates: pytest coverage >=70%.
Docs: API spec minimal (paths, payloads, codes d erreur, etats assignments).
Acceptance: flux API verts bout-en-bout.

## Jalon 7 - Redis cache basique
But: cache listages lourds.
Livrables: client, TTL, invalidation.
Tests: hit/miss.
CI Gates: pytest.
Docs: strategie cache.
Acceptance: perfs locales ameliorees.

## Jalon 8 - Observabilite backend
But: /metrics Prometheus, logs JSON avec trace_id, health probes.
Livrables: middleware, config Loki.
Tests: obs-smoke.
CI Gates: obs-smoke job.
Docs: dashboard ids.
Acceptance: targets UP, logs visibles.

## Jalon 9 - Docker dev stack
But: compose dev (backend, pg, redis, grafana, loki, prom, mailpit).
Livrables: deploy/dev/compose.yaml + volumes.
Tests: PS1/dev_up lance services.
CI Gates: cli-docker build smoke.
Docs: runbook dev.
Acceptance: app up via compose.

## Jalon 10 - Frontend foundation
But: React+Vite+TS+Tailwind+shadcn, Router, ESLint, Vitest, Playwright, Storybook.
Livrables: layout, theming, routes, pre-commit.
Tests: vitest de base, eslint, playwright smoke.
CI Gates: lint-frontend, test-frontend, e2e-smoke.
Docs: frontend/README.
Acceptance: shell UI ok.

## Jalon 11 - Frontend auth complete
But: login/logout, refresh, gardes de routes, profil.
Livrables: react-hook-form + zod, TanStack Query client, intercepteurs 401, stockage cookies httpOnly, CSRF header.
Tests: e2e login, garde, expirations.
CI Gates: e2e auth.
Docs: flux auth cote FE.
Acceptance: session persiste et se renouvelle.

## Jalon 12 - Design system + a11y
But: systeme de design solide et accessible.
Livrables: tokens, composants de base (Button, Input, Table, Modal, Toast), focus rings, shortcuts.
Tests: Storybook CI, axe checks basiques.
CI Gates: build storybook, bundle budget initial.
Docs: guide de style.
Acceptance: composants reutilisables.

## Jalon 13 - Data fetching et etat
But: TanStack Query (cache, retries), Zustand pour etat UI.
Livrables: api client, error boundaries, loaders, optimistic updates patron.
Tests: vitest hooks, e2e erreurs/retry.
CI Gates: test-frontend, e2e.
Docs: patterns data.
Acceptance: UX fluide et resiliente.

## Jalon 14 - Calendrier pro (drag & drop)
But: vues month/week/day + timeline, DnD assign/resize, fuseaux horaires, **etat visuel des assignments**.
Livrables: FullCalendar ou dnd-kit custom, mapping couleurs par status: INVITED (info), ACCEPTED (success), DECLINED (danger), CANCELLED (muted). Legend et filtres par status et par user/org/project.
Tests: e2e DnD, regression visuelle simple, verif couleur/legende.
CI Gates: e2e calendrier, bundle budget strict.
Docs: decisions lib + schema mapping status->style.
Acceptance: planif directe et statut visible en temps reel (polling ou SSE optionnel).

## Jalon 15 - Projects + Missions (table + wizard + batch)
But: gestion **projects** et missions associees, creation en lot, assignations initiales.
Livrables: 
- Pages: liste Projects (status, dates, managers), detail Project avec tableau Missions liees.
- Wizard project->missions: creation d un project puis **batch create** (10+ missions) avec duplication par jours/plages horaires, roles et quotas.
- Actions bulk: assigner users a selection de missions, changement de status, duplication, publication.
Tests: e2e create project, batch missions, assignations bulk, duplication.
CI Gates: e2e missions.
Docs: spec UX et cas d erreurs.
Acceptance: projects et missions operables bout-en-bout.

## Jalon 15.5 - Workflow d acceptation mission (UI + liens securises)
But: inviter, notifier, accepter/decliner depuis le client (connecte) ou via lien (token signe) puis MAJ planning.
Livrables: 
- Backend: endpoints `/v1/invitations` (create, revoke), `/v1/assignments/{id}/accept`, `/v1/assignments/{id}/decline`, validation token et expiration, audit log.
- Frontend: page **My Missions** (status, actions Accept/Decline, message de raison si decline), page publique via lien pour users sans session.
- Planning: MAJ auto des events et du compteur par status, badge sur project/mission.
Tests: e2e accept/decline (avec et sans session), MAJ planning, audit log.
CI Gates: e2e acceptance.
Docs: flux sequence ASCII, securite tokens (duree, revocation).
Acceptance: invitation -> accept/decline -> planning mis a jour et visible.

## Jalon 15.6 - Invitations: endpoint accept
But: corriger l endpoint public d acceptation par token (idempotence).
Livrables:
- POST /api/v1/invitations/{id}/accept?token=...
- Service de validation token et MAJ assignment -> ACCEPTED
Tests: pytest test_invitations_accept.py
Docs: README root + backend
Acceptance: idempotence cote seed OK

## Jalon 16 - Users + disponibilites
But: profils users (skills, tags, employment_type, rate_profile), calendrier individuel, demande/approbation disponibilite.
Livrables: pages profil, workflow appro.
Tests: e2e disponibilites.
CI Gates: e2e.
Docs: schema workflow.
Acceptance: cycle dispo complet.

## Jalon 17 - Conflits (UI resolution)
But: affichage conflits, suggestions auto (remplacements), merge tools.
Livrables: endpoints `/api/v1/conflicts`, page `/conflicts`, CI `e2e-conflits`.
Tests: tests conflits backend + e2e resolution.
CI Gates: e2e conflits.
Docs: algos et limites.
Acceptance: conflit resolu via UI.
Note packaging/typing: ajouter backend/__init__.py ; mypy.ini avec explicit_package_bases ; setuptools limite a 'app'.

## Jalon 18 - Notifications (email + Telegram) fonctionnelles
But: envoi reel + liens d acceptation securises + centre de notifications.
Livrables: 
- Email: MailPit en dev, SMTP en staging/prod. Templates texte (ASCII) pour invitation, rappel, changement d horaire, annulation.
- Telegram: bot avec commandes simples ("mes missions", "accepter <code>", "decliner <code>").
- Liens: URL signée vers page publique d acceptation/decline, ou deep-link vers app connectee.
- Centre de notifications FE: liste, filtre (unread), actions rapides.
Tests: dry-run en dev + e2e reception (dev), verification du lien et changement de status.
CI Gates: pytest + e2e notif.
Docs: runbook SMTP/Telegram (sans secrets), variables env, anti-abuse (rate limit invitation).
Acceptance: notifications efficaces et sures.

## Jalon 19 - Comptabilite et exports
But: cachets, factures, exports CSV/PDF/ICS, **totaux mensuels par user** et par project/org.
Livrables: 
- Backend: `/v1/reports/monthly-users` (par org/project, filtre date, group by user/mois), `/v1/exports/*` pour CSV/PDF/ICS.
- Frontend: ecran Comptabilite -> **Totaux mensuels par user** (table triable, filtres, export CSV), recap par project.
- Calculs: heures prevues vs confirmees (ACCEPTED), taux horaires ou forfaits via `rate_profile`.
Tests: validations montants, regroupements mensuels, conversions horaires->montants, exports.
CI Gates: pytest + e2e.
Docs: formats, conventions de calcul (UTC, arrondis, inclusions jours feries en option).
Acceptance: totaux mensuels par user operationnels et exportables.

## Jalon 20 - Perf baseline
But: k6 smoke + baseline RPS/latence, budgets FE (size-limit), Lighthouse CI (optionnel).
Livrables: deploy/k6/*.js, PS1 wrappers.
Tests: k6-smoke.
CI Gates: perf job (non bloquant d abord), bundle budget FE.
Docs: objectifs perf.
Acceptance: baseline publiee.

## Jalon 21 - Staging infra
But: compose staging, Caddy TLS, volumes persistants.
Livrables: deploy/staging/compose.yaml, Caddyfile, health checks.
Tests: e2e contre staging, zap-baseline.
CI Gates: deploy-staging (manual), zap-baseline.
Docs: runbook staging.
Acceptance: URL publique OK.

## Jalon 22 - Scans securite (phase 1)
But: SBOM, audits deps, Trivy FS et image.
Livrables: workflows syft, pip-audit, npm audit, trivy.
Tests: rapports artefacts, triage exceptions.
CI Gates: sbom, deps-audit, vuln scans (warning puis blocking pour CRITICAL).
Docs: security.md.
Acceptance: scans reguliers et suivis.

## Jalon 23 - Supply chain (cosign + provenance)
But: signature images, attestation SLSA.
Livrables: workflows cosign keyless, provenance attest.
Tests: verification cosign en CI.
CI Gates: sign-images requis avant deploy.
Docs: procedure verify.
Acceptance: images signees.

## Jalon 24 - Hardening backend
But: rate limit, headers securite, validation stricte, limites payload.
Livrables: limiter, headers, pydantic strict.
Tests: abuse tests, zap-baseline amelioration.
CI Gates: e2e + zap sans findings bloquants.
Docs: threat model bref.
Acceptance: endpoints robustes.

## Jalon 25 - Backups et restauration
But: dumps Postgres, plan sauvegarde, rehearsal restore.
Livrables: PS1/backup_db.ps1, PS1/restore_db.ps1, docs cron.
Tests: restore sur copie.
CI Gates: n/a.
Docs: runbook backup.
Acceptance: restore OK.

## Jalon 26 - Deploiement prod
But: compose prod, Caddy, obs, secrets par env host (pas dans git).
Livrables: deploy/prod/compose.yaml, alerts de base.
Tests: smoke post-deploy, e2e critiques.
CI Gates: approval manual, images signees verifiees, zap post-deploy.
Docs: runbook prod.
Acceptance: prod stable.

## Jalon 27 - Post-launch et SLO
But: SLO/SLI, alertes, grooming backlog.
Livrables: dashboards finaux, alert rules, changelog.
Tests: alert smoke.
CI Gates: obs-smoke.
Docs: SLO.md.
Acceptance: on-call pret.

## Jalon 28 - Templates de planification
But: modeliser des templates de shifts et generer des missions rapidement.
Livrables: tables `shift_templates`, `mission_templates`; endpoints `/v1/templates/*`; UI: bibliotheque de templates; generation par recurrence.
Tests: generation batch et collisions.
CI Gates: pytest + e2e wizard avec templates.
Docs: guide templates.
Acceptance: creation rapide de 10+ missions via templates.

## Jalon 29 - Matching et contraintes
But: assignations guidees par skills/tags, preferences, disponibilites, contraintes legales.
Livrables: service matching (score), regles (heures max/jour, repos, incompatibilites), suggestions dans UI.
Tests: cas limites, priorites, performance.
CI Gates: pytest module matching >=75% cov.
Docs: algorithmes et limites.
Acceptance: suggestions pertinentes.

## Jalon 30 - Updates temps reel
But: propagation des changements planning et notifications en live.
Livrables: SSE/WebSocket sur missions/assignments/notifications; reconnection et backoff.
Tests: e2e refresh live.
CI Gates: e2e live basique.
Docs: schema eventing.
Acceptance: DnD ou accept/decline visibles instantanement par tous.

## Jalon 31 - Import/Export en masse
But: on-boarding rapide et interoperabilite.
Livrables: import CSV (users, missions), validation et rapport d erreurs; exports CSV.
Tests: fichiers de test, cas d erreurs.
CI Gates: e2e import.
Docs: gabarits CSV.
Acceptance: import 1000 lignes sans erreur critique.

## Jalon 32 - Sync calendriers externes
But: integrer/partager les plannings.
Livrables: ICS feed par user/project; connecteurs Google/Microsoft (pull/push) optionnels.
Tests: ICS conforme, fuseaux horaires.
CI Gates: tests unitaires; e2e ICS.
Docs: limites des connecteurs.
Acceptance: calendrier perso visible dans Google/Outlook.

## Jalon 33 - Documents et e-sign
But: gerer contrats/AEM/PIECES jointes.
Livrables: upload vers S3 (pre-signed), scan ClamAV, metadonnees; integration e-sign externe optionnelle (placeholders, pas de secret dans repo).
Tests: upload, scan, droits d acces.
CI Gates: pytest + e2e upload.
Docs: runbook stockage.
Acceptance: documents consultables/telechargeables selon RBAC.

## Jalon 34 - Time tracking / Timesheets
But: heures prevues vs faites.
Livrables: timesheet par mission/user (check-in/out manuel), validation manager, ajustements.
Tests: calculs delta/heures de nuit/jours feries.
CI Gates: pytest + e2e timesheets.
Docs: conventions de calcul.
Acceptance: timesheets valides.

## Jalon 35 - Paie / Exports comptables
But: fournir les donnees a la paie/compta.
Livrables: exports CSV standards (par user/mois, par project), mapping `rate_profile` -> lignes; integration cabinet/ERP optionnelle via CSV.
Tests: coherence totaux.
CI Gates: pytest + e2e exports.
Docs: dictionnaire de donnees.
Acceptance: fichiers acceptes par le cabinet.

## Jalon 36 - Reporting avance
But: KPIs et tableaux de bord.
Livrables: pages dashboards (perfs, utilisation, couts, taux d acceptation), filtres par period/user/project.
Tests: exactitude des agregats.
CI Gates: e2e reporting.
Docs: definitions metriques.
Acceptance: KPIs fiables.

## Jalon 37 - i18n/l10n, timezones, feries
But: internationaliser proprement.
Livrables: i18n FE, formats date/nombre, calendrier jours feries par pays, gestion DST.
Tests: snapshots i18n, fuseaux.
CI Gates: lint i18n, e2e fuseaux.
Docs: politique i18n.
Acceptance: UX coherente partout.

## Jalon 38 - PWA et offline basique
But: resilience reseau.
Livrables: manifest, service worker (cache), mode lecture offline pour Planning/My Missions.
Tests: e2e offline simule.
CI Gates: Lighthouse CI perf/PWA (warning d abord).
Docs: limites offline.
Acceptance: consultation offline OK.

## Jalon 39 - API publique + Webhooks
But: ouverture controlee.
Livrables: API keys (scopes), quotas, docs OpenAPI publiques, webhooks (events: mission.created, assignment.accepted...).
Tests: signature HMAC, retries.
CI Gates: tests webhooks.
Docs: guide integrateurs.
Acceptance: integ faciles et sures.

## Jalon 40 - Feature flags
But: livrer en douceur.
Livrables: toggles en DB + middleware FE, bucketing par org.
Tests: flags on/off.
CI Gates: tests unitaires.
Docs: guide flags.
Acceptance: activation controlee.

## Jalon 41 - Deploiement robuste
But: zero-downtime.
Livrables: strategies blue/green, migrations sans coupure (expand/contract), maintenance page.
Tests: rehearsals en staging.
CI Gates: simulateur migration.
Docs: runbook migrations.
Acceptance: deploy sans interruption visible.

## Jalon 42 - Donnees & RGPD
But: confiance et conformite.
Livrables: export de donnees user, effacement, retention policies, pseudonymisation logs, bannettes d acces.
Tests: e2e export/erase.
CI Gates: checks RGPD.
Docs: RGPD.md.
Acceptance: demandes traitees.

## Jalon 43 - SSO + MFA
But: securite compte.
Livrables: OAuth2 Google/Microsoft, MFA TOTP, recovery codes, device management.
Tests: flows, lockout.
CI Gates: e2e auth forte.
Docs: securite.
Acceptance: MFA operationnel.

## Jalon 44 - Isolation multi-tenant
But: etancheite stricte.
Livrables: verrous de scoping dans services/repos, tests "tenant-fuzz".
Tests: tentatives cross-tenant.
CI Gates: suite iso mandatory.
Docs: decisions iso.
Acceptance: aucun leak cross-tenant.

## Jalon 45 - Recherche full-text
But: trouver vite.
Livrables: Postgres FTS + pg_trgm, endpoints recherche (users/missions/projects), surlignage.
Tests: precision/recall basiques.
CI Gates: tests recherche.
Docs: index/strategie.
Acceptance: recherches rapides.

## Jalon 46 - Anti-abuse & rate limit
But: proteger l app.
Livrables: limites par endpoint/user/org/IP, detection login anormal, blocage temporaire.
Tests: scenarios abuse.
CI Gates: tests limites.
Docs: policy anti-abuse.
Acceptance: attaques basiques mitigees.

## Jalon 47 - Workers & scheduler
But: fiabiliser asynchrone.
Livrables: workers RQ dedies, retry exponentiel, DLQ, APScheduler pour taches planifiees.
Tests: idempotence.
CI Gates: tests workers.
Docs: runbook jobs.
Acceptance: jobs fiables.

## Jalon 48 - Backups & DR avances
But: resiliency.
Livrables: WAL archiving, PITR Postgres, restore drill automatisee.
Tests: drill trimestrielle.
CI Gates: rapport drill.
Docs: DR.md.
Acceptance: RTO/RPO documentes.

## Jalon 49 - Budgets & profitabilite
But: suivre couts et marges.
Livrables: budgets par project, couts reels, marge brute, alertes depassement.
Tests: coherence calculs.
CI Gates: e2e budgets.
Docs: definitions couts.
Acceptance: suivi fiable.

## Jalon 50 - A11y & perf gates
But: mettre la barre haute.
Livrables: checks axe, Lighthouse CI budgets, images responsive.
Tests: a11y auto sur composants clefs.
CI Gates: seuils min.
Docs: a11y.md.
Acceptance: acces booste.

## Jalon 51 - Monitoring erreurs & traces
But: troubleshooting rapide.
Livrables: OTel traces, correlation logs/requests, capture erreurs FE (Sentry-compatible via OTel).
Tests: traces dans Grafana Tempo (optionnel) ou Loki + exemplars.
CI Gates: obs-smoke et trace-smoke.
Docs: runbook incident.
Acceptance: MTTD/MTTR reduits.

## Jalon 52 - DX & qualite dev
But: experience dev solide.
Livrables: pre-commit pack (ruff, mypy, eslint, vitest), OpenAPI client codegen FE, make/PS1 helpers, templates PR/issue raffines.
Tests: generation client stable CI.
CI Gates: lint pack.
Docs: CONTRIBUTING.md.
Acceptance: onboard dev rapide.

## Jalon 53 - Donnees de test & Hypothesis
But: fiabilite par la diversite.
Livrables: generateurs de donnees synthetiques, tests property-based (Hypothesis) pour modules sensibles (matching, conflicts).
Tests: campagnes Hypothesis.
CI Gates: job property-tests.
Docs: guide tests.
Acceptance: moins de regressions.

## Jalon 54 - Scalabilite
But: readiness charge.
Livrables: parametrage Caddy, workers horizontaux, DB indexes reviews, read-only replicas (optionnel), strategie cache.
Tests: k6 baseline cible, flamegraphs.
CI Gates: perf threshold.
Docs: capacite.
Acceptance: tient la charge cible.

## Jalon 55 - Multi-region (optionnel)
But: continuites.
Livrables: plan multi-region (stateless FE/BE, DB primaire/replica, CDN), feature flags region.
Tests: plan exercice.
CI Gates: n/a.
Docs: multi-region.md.
Acceptance: plan pret si besoin.

# Scripts PowerShell a fournir au fil des jalons
- `PS1/init_repo.ps1` : init venv, npm, pre-commit, hooks
- `PS1/dev_up.ps1` / `PS1/dev_down.ps1` : compose up/down
- `PS1/test_all.ps1` : ruff, mypy, pytest, eslint, vitest
- `PS1/seed.ps1` : alembic upgrade + seed data
- `PS1/k6_smoke.ps1` : lance les tests k6
- `PS1/backup_db.ps1` / `PS1/restore_db.ps1`

# Politique READMEs (obligatoire)
A chaque jalon, mettre a jour si applicable:
- `README.md` (root): status jalon, commandes, CI gates actifs
- `backend/README.md`: run local, migrations, tests, observabilite
- `frontend/README.md`: run local, build, tests, bundle budget
- `deploy/README.md`: compose files, Caddy, URLs, k6, obs, zap
- `docs/CHANGELOG.md`: resume jalon (Keep a Changelog, date UTC)

# Definition of Done (MVP)
- [ ] Auth reelle (JWT + refresh, cookies httpOnly) sans mock
- [ ] API metier: users, **projects**, missions, assignments (status), invitations, availability, conflicts, rates, orgs
- [ ] Workflow d acceptation: invite -> accept/decline (token) -> MAJ planning
- [ ] DB migrations + seed reproductible
- [ ] Frontend: auth, calendrier DnD avec status, **projects + missions wizard (batch)**, users (profils), disponibilites, conflits, **My Missions (accept/decline)**, notifications, **comptabilite: totaux mensuels par user** + exports
- [ ] Tests: backend >=70% cov, vitest OK, e2e Playwright (login, create project + batch missions, accept/decline, DnD calendrier, resolution conflit, export, reporting)
- [ ] Perf: k6 smoke OK, bundle budget FE respecte
- [ ] Obs: /metrics UP, logs Loki, dashboards de base
- [ ] Staging TLS + zap-baseline sans CRITICAL
- [ ] Supply chain: SBOM, scans, images signees cosign

# Rappels importants
- Zero secret dans git. Toujours `.env.example`.
- Petits PRs, une seule chose a la fois. Toujours CI verte.
- En cas d echec CI: corriger dans la PR avant merge.
- Documenter toute exception securite (justification + date + ticket).

# Gabarits a reutiliser dans les PRs

## PROMPT_CODEX (gabarit)
SYSTEM:
Tu es Codex. Lis `docs/roadmap.md`. Respecte Windows-first, ASCII, zero secret.
USER:
ETAPE <N>: <titre>. Fournis code complet (pas d extraits), scripts PS1, workflows, tests. Mets a jour les READMEs requis.
ACCEPTANCE:
Lister les tests et leurs criteres de reussite.
TESTS:
Commandes exactes (pytest, vitest, playwright, k6...).
GIT:
Branche `feat-<slug>`, commits atomiques, PR avec resume, coche les checkboxes.
NOTES:
Limites connues + next step.

## MESSAGE_AGENT (gabarit)
- branche creee
- generation fichiers
- commandes lancees localement
- resume des tests
- build images
- ouverture PR + labels + assigne


## Jalon 56 - Previsionnel charge (demand forecasting)
But: anticiper besoins en staff par project/date.
Livrables: connecteurs generiques (CSV/API) pour ventes/affluence, courbes prevision, besoin auto de missions.
Tests: scenarios de forecast simples.
CI Gates: tests unitaires forecast.
Docs: mapping sources -> forecast.
Acceptance: besoin propose coherent vs historique.

## Jalon 57 - Moteur droit du travail FR (regles configurables)
But: aides a la conformite (sans avis legal).
Livrables: moteur de regles (repos, amplitudes, heures de nuit, maxi hebdo), profils par type d emploi.
Tests: cas limites reglementaires.
CI Gates: couverture >=75% module regles.
Docs: disclaimer + guide parametres.
Acceptance: avertissements visuels en cas de depassement.

## Jalon 58 - Bourse d echanges et remplacements
But: swaps entre users, remplacements proposes automatiquement.
Livrables: UI echanges (proposer/demander), validation par manager, historique.
Tests: e2e swap.
CI Gates: e2e swaps.
Docs: politique swaps.
Acceptance: swap abouti sans pertes de droits.

## Jalon 59 - Open shifts et candidature
But: publier des shifts ouverts et recevoir des candidatures.
Livrables: page Open Shifts, tri par score matching, auto-close a quota atteint.
Tests: e2e candidature + attribution.
CI Gates: e2e open-shifts.
Docs: guide publication.
Acceptance: attribution rapide et tracee.

## Jalon 60 - Onboarding checklists
But: collecter docs/infos avant mission.
Livrables: checklists par project/role (pieces, IBAN, attestations), rappels auto.
Tests: e2e checklist complete.
CI Gates: e2e onboarding.
Docs: modeles de checklists.
Acceptance: 100% requis OK avant affectation.

## Jalon 61 - Messagerie interne et annonces
But: communication integree.
Livrables: canaux par project/mission, annonces broadcast avec accusé de lecture.
Tests: e2e envoi/lecture.
CI Gates: e2e messaging basique.
Docs: etiquette usage.
Acceptance: messages recus et confirmes.

## Jalon 62 - Pointeuse mobile (geofencing/QR/photo)
But: pointages fiables sur site.
Livrables: check-in/out avec geofencing, scan QR event, photo optionnelle (consentement), anti-fraude basique.
Tests: e2e pointage + deltas temps.
CI Gates: e2e pointeuse.
Docs: RGPD impacts.
Acceptance: temps captes et verifies.

## Jalon 63 - Absences et conges
But: demandes, validations, conflits planning.
Livrables: PTO/absences (types configurables), appro manager, impacts sur planning et matching.
Tests: e2e demande/appro.
CI Gates: e2e absences.
Docs: politique absences.
Acceptance: absences integrees au planning.

## Jalon 64 - Regles paie avancees
But: primes (nuit, dimanche, feries), heures suppl., majorations.
Livrables: moteur de calcul parametre, simulation cout par mission/project.
Tests: cas limites de paie.
CI Gates: pytest paie >=80% module.
Docs: dictionnaire regles.
Acceptance: resultats attendus sur jeux d essai.

## Jalon 65 - Notes de frais et per diem
But: suivi des depenses terrain.
Livrables: capture justificatifs (OCR), per diem, validation et export comptable.
Tests: e2e expenses.
CI Gates: e2e expenses.
Docs: categories depenses.
Acceptance: export pret pour cabinet.

## Jalon 66 - Inventaire materiel et kits plateau
But: eviter conflits materiel.
Livrables: catalogue, reservation par mission, check-in/out, conflits de stock.
Tests: collisions materiel.
CI Gates: tests inventaire.
Docs: modele donnees inventaire.
Acceptance: visibilite stock et alertes conflits.

## Jalon 67 - Voyages et hebergement
But: logistique tournées/deplacements.
Livrables: itineraires, hotels, per diem, partages ICS, budgets et recap couts.
Tests: e2e travel pack.
CI Gates: e2e travel.
Docs: runbook travel.
Acceptance: kit voyage genere et partage.

## Jalon 68 - Vendors, devis, bons de commande
But: achats structures.
Livrables: fournisseurs, demandes de devis, POs, rapprochement factures.
Tests: coherence montants.
CI Gates: e2e achats.
Docs: flux achats.
Acceptance: POs traçables jusqu a facture.

## Jalon 69 - Feedback, incidents, securite
But: boucle qualite.
Livrables: formulaires post-mission, incidents/safety, actions correctives, analytics satisfaction.
Tests: e2e feedback.
CI Gates: tests feedback.
Docs: guide captation incidents.
Acceptance: suivi des plans d actions.

## Jalon 70 - Knowledge base plateau
But: centraliser docs operas.
Livrables: stage plots, input lists, riders, run-of-show; versioning et partage par project.
Tests: acces RBAC.
CI Gates: tests basiques KB.
Docs: arbo KB typee.
Acceptance: docs accessibles et a jour.

## Jalon 71 - Connecteurs ticketing/CA (optionnels)
But: rapprocher couts vs revenus.
Livrables: connecteurs generiques (CSV/API) ticketing/CA, dashboard marge par project.
Tests: rapprochements unitaires.
CI Gates: e2e dashboard CA/couts.
Docs: mapping donnees.
Acceptance: marge calculee.

## Jalon 72 - Data export BI
But: analyse avancee externe.
Livrables: exports programmables (Parquet/CSV) vers DWH/BI, schema stable.
Tests: validation schemas.
CI Gates: tests export.
Docs: contrat de schema.
Acceptance: pipelines BI alimentes.

## Jalon 73 - Score fiabilite user
But: encourager ponctualite et reponses rapides.
Livrables: score base sur acceptation, retard, no-show (pondere), affichage controlle.
Tests: fairness basique.
CI Gates: tests score.
Docs: formule score.
Acceptance: score mis a jour et utile au matching.

## Jalon 74 - Acces invites / guest
But: collaboration ponctuelle sans compte complet.
Livrables: acces limite via liens signes, portees restreintes (lecture/acceptation).
Tests: e2e guest.
CI Gates: e2e guest.
Docs: securite invite.
Acceptance: experience rapide et sure.


## Jalon 75 - Secrets management & rotation
But: gerer secrets proprement.
Livrables: SOPS+age pour non-prod, guide Vault (optionnel), rotation periodique, gitleaks en CI.
Tests: scan secrets CI, rotation dry-run.
CI Gates: gitleaks mandatory.
Docs: SECRETS.md.
Acceptance: aucun secret en clair, rotation documentee.

## Jalon 76 - Email deliverability
But: fiabiliser email.
Livrables: SPF/DKIM/DMARC, suivi bounces/complaints, warm-up plan, reputations.
Tests: envois test, DMARC aggregate parse (basique).
CI Gates: checklist domaine.
Docs: EMAIL.md.
Acceptance: >98% delivrabilite devinee, bounce rate <2% (objectif).

## Jalon 77 - SMS/WhatsApp (optionnel)
But: canal alternatif.
Livrables: provider-agnostic, opt-out, rate limit, templates legaux.
Tests: e2e en sandbox.
CI Gates: e2e sms basique.
Docs: NOTIFS_SMS.md.
Acceptance: envoi OK sans spam.

## Jalon 78 - Web Push (PWA)
But: notifications navigateur.
Livrables: service worker push, preferences user.
Tests: e2e push dev.
CI Gates: lighthouse PWA.
Docs: PUSH.md.
Acceptance: push recu et controlable.

## Jalon 79 - Billing & subscriptions (optionnel)
But: monétiser.
Livrables: Stripe (seats + usage), dunning, coupons, factures PDF, TVA.
Tests: sandbox flows.
CI Gates: e2e billing sandbox.
Docs: PRICING.md.
Acceptance: cycle abonnement complet en sandbox.

## Jalon 80 - Self-serve onboarding org
But: org en autonomie.
Livrables: signup org, invitation par domaine, claim domaine (SSO), guide migration CSV.
Tests: e2e onboarding.
CI Gates: e2e.
Docs: ONBOARDING.md.
Acceptance: org prete en <10 min.

## Jalon 81 - Admin Control Center
But: gouvernance.
Livrables: audit trail et access logs, impersonation sous approbation, export audit.
Tests: RBAC strict.
CI Gates: tests audit.
Docs: ADMIN.md.
Acceptance: controles admin complets.

## Jalon 82 - Data governance & residency
But: confiance donnees.
Livrables: chiffrement par tenant (option), choix region, KMS/keys rotation, champs sensibles chiffrés.
Tests: rotation cle test.
CI Gates: checks chiffrement.
Docs: DATA_GOV.md.
Acceptance: exigences clients couvertes.

## Jalon 83 - Data lifecycle (retention/archival/purge)
But: cycle de vie.
Livrables: politiques retention, archivage froid S3, purge securisee, legal hold.
Tests: e2e purge.
CI Gates: tests lifecycle.
Docs: RETENTION.md.
Acceptance: politique appliquee.

## Jalon 84 - Legal & privacy pack
But: cadre legal.
Livrables: ToS, Privacy, DPA, cookies/consent logs, mentions legales.
Tests: n/a.
CI Gates: checklist legal.
Docs: LEGAL.md.
Acceptance: docs publies.

## Jalon 85 - Support & CX
But: experience complete.
Livrables: centre d aide, in-app help, NPS, integration Zendesk/Intercom (optionnel).
Tests: n/a.
CI Gates: n/a.
Docs: SUPPORT.md.
Acceptance: boucle feedback active.

## Jalon 86 - Product analytics (privacy-first)
But: comprendre usage.
Livrables: telemetry anonyme (events clefs), funnels, consent; opt-out.
Tests: schemas events.
CI Gates: tests schema.
Docs: ANALYTICS.md.
Acceptance: tableaux d usage fiables.

## Jalon 87 - Progressive delivery
But: livrer sans risque.
Livrables: canary, shadow traffic, dark launch via flags, status page publique.
Tests: rehearsal staging.
CI Gates: checks canary.
Docs: RELEASE.md.
Acceptance: releases sans heurts.

## Jalon 88 - Chaos & resiliency drills
But: robustesse prouvee.
Livrables: injections pannes (DB/reseau), runbooks exercises trimestriels.
Tests: drills passes.
CI Gates: rapport drill.
Docs: CHAOS.md.
Acceptance: equipe prete aux incidents.

## Jalon 89 - Cost & FinOps
But: maitrise couts.
Livrables: dashboards couts, budgets/alertes, scenarios scaling, tests budget FE/BE.
Tests: budget checks.
CI Gates: finops gate non-bloquant -> bloquant.
Docs: FINOPS.md.
Acceptance: couts sous controle.

## Jalon 90 - IaC & drift detection
But: infra reproductible.
Livrables: Terraform + Ansible, detection drift, revue PR infra, environnements parite.
Tests: terraform plan en CI.
CI Gates: infra-plan gate.
Docs: IAC.md.
Acceptance: infra versionnee et stable.


## Jalon 91 - Optimiseur IA de planning (ILP/CP-SAT)
But: auto-assign optimal sous contraintes cout/horaires/fairness/preferences.
Livrables: solveur (OR-Tools) avec contraintes (budgets, repos, priorites skills, distances), explications de decisions.
Tests: jeux d essai or, timeouts gardes, tests fairness.
CI Gates: coverage >=80% module optimizer, perf cap.
Docs: guide modelisation.
Acceptance: planning genere <= X s avec cout <= baseline et violations = 0.

## Jalon 92 - Scenarios & what-if (budget guardrails)
But: comparer alternatives avant publication.
Livrables: snapshots de scenarios, simulateur couts/risques, Monte Carlo simple sur absences.
Tests: comparaisons deterministes, variance controlee.
CI Gates: tests scenario.
Docs: SCENARIOS.md.
Acceptance: choix de scenario argumente (cout, risques, fairness).

## Jalon 93 - Automations no-code (IFTTT interne)
But: automatiser sans dev.
Livrables: moteur de regles (triggers + conditions + actions) couvrant invitations, relances, exports, webhooks, flags.
Tests: idempotence, boucle infinie evitee, limites.
CI Gates: tests automations.
Docs: AUTOMATIONS.md.
Acceptance: regles actives, executions tracees.

## Jalon 94 - Integration Hub & Connectors
But: ecosystème ouvert.
Livrables: catalogue connecteurs (CSV/API generic), mapping schemas, replays, OAuth pour providers (optionnel), templates webhooks.
Tests: mapping stable, replays.
CI Gates: tests connectors.
Docs: INTEGRATIONS.md.
Acceptance: flux integres sans code.

## Jalon 95 - Skills Matrix, formations & certifications
But: adequation poste/competences.
Livrables: matrice skills par role, formations, expirations certifs (rappels), pre-requis blocking.
Tests: gating conforme.
CI Gates: tests skills.
Docs: SKILLS.md.
Acceptance: absence d affectation si prerequis manquant.

## Jalon 96 - Sante, securite & bien-etre
But: prevenir fatigue/burnout.
Livrables: indicateurs de charge, DND (do-not-disturb) notifications, limites heures consecutives, alertes.
Tests: seuils et alertes.
CI Gates: tests wellbeing.
Docs: WELLBEING.md.
Acceptance: alertes pertinentes, respect DND.

## Jalon 97 - Marketplace & partenaires
But: capacite elargie via agences.
Livrables: portail vendors (SLAs, rate cards, compliance docs), bids sur open shifts, selection multi-criteres.
Tests: e2e bids.
CI Gates: e2e marketplace.
Docs: VENDORS.md.
Acceptance: attribution via partenaire traçable.

## Jalon 98 - Mobile suite & kiosque
But: usage terrain premium.
Livrables: PWA wrapper mobile, mode kiosque pointage, file d actions offline, stockage securise.
Tests: offline queue, kiosk.
CI Gates: e2e mobile basique.
Docs: MOBILE.md.
Acceptance: check-in/out fiable hors reseau.

## Jalon 99 - Identite & conformite avancees
But: entreprise-ready.
Livrables: SCIM provisioning, campagnes d access review/recertification, audit tamper-evident (hash chain), eIDAS pour signature timesheets.
Tests: recert flows, integrite logs.
CI Gates: tests identite/audit.
Docs: ENTERPRISE.md.
Acceptance: controles passes.

## Jalon 100 - Durabilite & empreinte carbone
But: reporting ESG.
Livrables: calcul CO2 par project/mission (deplacements, hebergement), objectifs et alertes, export ESG.
Tests: verifs facteurs emission basiques.
CI Gates: tests ESG.
Docs: ESG.md.
Acceptance: rapport carbone par project disponible.

---

Fin du document.

