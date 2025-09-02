# Runbook Staging

Objectif: Expliquer le cycle de vie staging: DNS/TLS, deploiement, rollback, sauvegardes, securite, scans.

1. DNS/TLS

* Variable STAGING_DOMAIN pointe sur VM.
* Caddy gere ACME; ports 80/443 requis.
* ACME_EMAIL doit etre valide.

2. Deploiement

* Runner self-hosted sur VM.
* Lancer workflow "deploy-staging".
* Images FRONTEND_IMAGE/BACKEND_IMAGE deja poussees au registry.
* Compose attend les health checks avant d exposer Caddy.

3. Verification

* Smoke:
  $Env:STAGING_DOMAIN="staging.example.com"
  deploy/staging/smoke.ps1 -BaseUrl ("https://{0}" -f $Env:STAGING_DOMAIN)

4. Scans ZAP

* Lancer workflow "zap-baseline" ou attendre CRON hebdomadaire.
* Recuperer artifact zap-baseline (html/xml/md).
* Traiter alertes Medium+.

5. Backups/Restore

* Postgres: volume db_data. Faire dump regulier (pg_dump) via job hors scope present fiche.
* Redis: AOF dans redis_data.

6. Rollback

* Revenir a images N-1 en ajustant BACKEND_IMAGE/FRONTEND_IMAGE dans .env puis redeployer.
* Si schema DB casse, appliquer rollback via Alembic (commande hors scope ici).

7. Journalisation/Observabilite

* Logs docker: docker logs -f cc_staging_backend
* request_id et logs JSON (selon app).
* Ajout Grafana/OTel (optionnel futur jalon).

8. Securite

* npm audit/pip-audit en CI deja en place (global).
* Gitleaks, SBOM CycloneDX recommandes sur images.

9. Incidents

* Fe 502: verifier health backend. docker ps, docker logs.
* ACME echec: verifier ports 80/443 et DNS propagation.
