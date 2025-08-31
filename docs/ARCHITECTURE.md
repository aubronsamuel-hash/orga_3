# Architecture (extrait jalon 3)

## ERD ASCII (simplifie)

orgs (id) 1--* accounts
orgs (id) 1--* users
orgs (id) 1--* projects 1--* missions 1--* mission_roles
missions (id) 1--* assignments *--1 users
users (id) 1--* user_skills
users (id) 1--* user_tags
users (id) 1--* availability
missions (id) 1--* invitations (optionnel user_id)
orgs (id) 1--* audit_log

## Enums

* assignment_status: INVITED, ACCEPTED, DECLINED, CANCELLED
* project_status: DRAFT, ACTIVE, ARCHIVED

## Indexes

* users: ix_users_last_name, ix_users_first_name
* missions: ix_missions_starts_at, ix_missions_ends_at
* assignments: uq_active_assignment_per_mission_user (unique partiel status ACTIVE)

## Flux Conflits

FE -> GET /api/v1/conflicts -> pour chaque id GET /api/v1/conflicts/{id} -> POST /api/v1/conflicts/resolve -> mise a jour UI

