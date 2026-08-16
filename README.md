# Railoo — prototype

*Swachh Safar, Surakshit Bharat.* A working, runnable slice of the Railoo platform:
PNR-based railway restroom booking, highway restroom discovery, women's safety
(Pink Help Points + period care), and a real emergency SOS flow — built on
Django + Django REST Framework, styled with Tailwind, with a premium-feeling
landing page and dashboard.

This is a **prototype**, not the full 12-module enterprise spec — see
"What was intentionally scoped down" below for exactly what's stubbed and why.

---

## Stack

- **Backend:** Django 5, Django REST Framework, SimpleJWT, django-filter
- **DB:** SQLite by default (zero setup) — one env flag away from Postgres
- **Frontend:** Django templates + Tailwind (CDN) + vanilla JS (fetch calls to the API)
- **Maps:** Google Maps JS API (optional — the page works without a key, just without the live map)
- **Deploy:** Dockerfile + docker-compose (gunicorn + Postgres)

## Run it locally

```bash
cd railoo
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python manage.py makemigrations accounts core restrooms bookings sos women_safety
python manage.py migrate
python manage.py createsuperuser   # for /admin/

python manage.py seed_demo_data    # populates demo restrooms, Pink Help Points, period care spots

python manage.py runserver
```

Then open:
- `http://127.0.0.1:8000/` — landing page + PNR booking widget
- `http://127.0.0.1:8000/highway/` — highway restroom finder
- `http://127.0.0.1:8000/womens-safety/` — Women's Safety dashboard
- `http://127.0.0.1:8000/sos/` — SOS trigger (requires login)
- `http://127.0.0.1:8000/admin/` — admin panel
- `http://127.0.0.1:8000/api/v1/...` — the JSON API (see below)

No `.env` file is required to run locally — `config/settings.py` has sane
dev defaults. Copy `.env.example` to `.env` when you want to override anything
(Postgres, Google Maps key, Twilio, Razorpay).

### Try the PNR flow without a real PNR

The PNR lookup is a deterministic mock (see `restrooms/services.py`) — type
**any** 10-digit string and you'll get a stable, believable train route with
restrooms attached to whichever seeded stations match. Swap in a licensed PNR
provider later without touching any other file — the service returns the same
shape either way.

## API surface (DRF, JWT-authenticated)

| Endpoint | Notes |
|---|---|
| `POST /api/v1/auth/register/` | Returns `{user, access, refresh}` |
| `POST /api/v1/auth/token/` | Login → JWT pair |
| `GET/PATCH /api/v1/auth/profile/` | Current user |
| `GET /api/v1/restrooms/` | Filter by `restroom_type`, `is_women_only`, `is_wheelchair_accessible`, `has_baby_care`, `has_ev_charging`, `min_cleanliness`, `station_code`, search, ordering |
| `GET /api/v1/restrooms/pnr/<pnr>/` | Train route + restrooms per upcoming station |
| `POST /api/v1/restrooms/<id>/rate/` | Rate a restroom (auth required) |
| `GET/POST /api/v1/bookings/` | User-scoped bookings; `POST .../cancel/` |
| `GET/POST /api/v1/sos/incidents/` | Trigger SOS; `POST .../resolve/` |
| `GET/POST /api/v1/sos/contacts/` | Emergency contacts CRUD |
| `GET /api/v1/women-safety/help-points/` | Pink Help Points (read-only) |
| `GET /api/v1/women-safety/period-care/` | Period care locations (read-only) |

All list endpoints are paginated (20/page) and support `?search=` and `?ordering=`.

## Project layout

```
railoo/
├── config/                # settings, root urls, wsgi/asgi
├── accounts/               # custom User, JWT + session auth, register/login/profile
├── restrooms/               # Restroom + RestroomRating models, PNR lookup service
├── bookings/               # user-scoped Booking model + API
├── sos/                     # SOSIncident + EmergencyContact, notification stub
├── women_safety/            # PinkHelpPoint + PeriodCareLocation
├── core/                    # landing/dashboard/highway/SOS/women's-safety pages,
│                             seed_demo_data management command, base.html
├── Dockerfile / docker-compose.yml
└── requirements.txt
```

## What was intentionally scoped down (and why)

The original spec asked for the full enterprise stack: Postgres, Redis, Celery,
Twilio SMS, Razorpay payments, Swagger docs, and 12 fully-built modules. For a
**runnable prototype** I deliberately did not wire up the pieces that need
external accounts/services to even boot, so this zip runs with `pip install`
and nothing else:

- **Postgres → SQLite by default.** Flip `USE_POSTGRES=True` in `.env` (or use
  `docker-compose up`, which runs Postgres for you) — the Django ORM code is
  identical either way.
- **Celery/Redis are not included.** SOS notifications and booking confirmations
  run synchronously for now. `sos/services.py` is written as a plain function
  specifically so it can become a `.delay()` Celery task later without changing
  any view code.
- **Twilio/Razorpay are stubbed.** `sos/services.py` logs what it *would* text
  your emergency contacts; `Booking.is_paid` exists but there's no real payment
  flow yet. Both are structured so credentials are the only thing missing.
- **Real PNR data isn't available** without a paid provider — `restrooms/services.py`
  documents exactly where to swap in a real one.
- **Payments, analytics, and adminpanel modules** from the original 12-app list
  aren't separate apps yet — analytics live directly in Django admin for now,
  and there's no separate `payments` app since there's no live payment gateway
  to back it.

## What to extend first

1. **Real PNR provider** — swap `PNRLookupService.get_train_route` in
   `restrooms/services.py` for a licensed API call. Everything downstream
   (the widget, the API response shape) stays the same.
2. **Celery for SOS + notifications** — move `sos/services.py` and booking
   confirmation emails into `tasks.py` per app, add Redis + a Celery worker
   service to `docker-compose.yml`. This is the highest-value reliability
   improvement (an SOS alert shouldn't wait on a slow SMS API call).
3. **A real emergency-contacts UI** — right now they're managed via the API
   only (`/api/v1/sos/contacts/`); the SOS page just displays them. A small
   Alpine.js or HTMX form on `core/templates/core/sos.html` closes that gap fast.
4. **Payments** — add a `payments` app wrapping Razorpay's order/verify flow,
   hang it off `Booking.is_paid`.
5. **Swagger/OpenAPI docs** — `drf-spectacular` is commented out in
   `requirements.txt`; uncomment it, add it to `INSTALLED_APPS`, and wire
   `/api/schema/` + `/api/docs/` in `config/urls.py`.
6. **Distance-based "near me" search** — restroom lookups currently don't
   filter by radius. Add `GeoDjango` + PostGIS (once you're on Postgres) or a
   simple haversine `annotate()` for "restrooms within 5km".
