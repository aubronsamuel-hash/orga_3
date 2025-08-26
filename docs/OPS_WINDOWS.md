* Lancer les scripts PowerShell en mode NoProfile.
* En cas de port occupe, fermer les processus node/uvicorn via dev_down.ps1.
* Utiliser `Join-Path` et encodage UTF-8 dans les scripts PS1.
* Python: preferer venv local `backend/.venv`.

## SQLite sur Windows: verrous de fichiers

Sous Windows, SQLite peut garder des verrous de fichiers si des connexions/engines ne sont pas entierement liberes. Mesures appliquees:

* Alembic `env.py`: appel explicite a `connectable.dispose()` apres `run_migrations_online()`.
* Tests migrations: fermeture du `engine` avec `dispose()` et suppression du fichier de test via `_unlink_with_retry()` (retries courts).
  Aucune action necessaire cote developpeur; ces protections sont en place pour la CI.

