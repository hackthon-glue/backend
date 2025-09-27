# Hackthon Backend

## Neon Database

The project now connects to the shared Neon Postgres instance provisioned for the hackathon.

1. Copy `.env.example` to `.env` and keep it out of source control:

   ```bash
   cp .env.example .env
   ```

2. Update `SECRET_KEY` if necessary and confirm the Neon credentials. The current demo connection string is:

   ```text
   postgresql://neondb_owner:npg_lJQ43sKDLExk@ep-rapid-hat-a1tnh9eg-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require
   ```

   `.env.example` already contains each piece of this URL.

3. Apply migrations and seed demo data:

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   pip install -r requirements/dev.txt
   python manage.py migrate
   python manage.py seed_mock_data
   ```

   These commands will run against the Neon database (development and production share the same instance during the demo).

4. Start the API locally:

   ```bash
   python manage.py runserver 0.0.0.0:8000
   ```

## Notes

- `seed_mock_data` is safe to re-run; it upserts the base countries and replaces dependent rows.
- Ensure outbound access to Neon (`ep-rapid-hat-a1tnh9eg-pooler.ap-southeast-1.aws.neon.tech:5432`). If DNS resolution or connectivity is blocked locally, run the migrations from a host with network access or through Neon’s SQL editor.
- Avoid committing `.env`; secrets must remain local.
