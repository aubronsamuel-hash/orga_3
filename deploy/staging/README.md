# Staging (compose + Caddy)

Prerequis:

* DNS A/AAAA -> VM publique (ports 80/443 ouverts)
* Docker/Compose installs
* Fichier .env base sur .env.example, stocke sur la VM (non commit)

Commandes:

* Demarrer: PowerShell
  cd deploy/staging
  ./deploy_up.ps1 -EnvFile ".env"
* Arreter:
  ./deploy_down.ps1
* Smoke:
  $Env:STAGING_DOMAIN="staging.example.com"
  ./smoke.ps1 -BaseUrl ("https://{0}" -f $Env:STAGING_DOMAIN)

Health:

* FE: GET /
* Static: GET /healthz
* API: GET /api/v1/health

Volumes:

* db_data, redis_data, caddy_data, caddy_config

TLS:

* Lets Encrypt via Caddy (email ACME_EMAIL)
