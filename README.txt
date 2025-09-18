# GT Movies Store

Django demo app: browse/search movies, add to cart, checkout (creates orders), write reviews.
- Users: signup/login/logout
- Reviews: create/edit/delete (owner-only)
- Cart: add/remove/clear; checkout updates stock and creates Order+OrderItems
- Orders: "My Orders" page
- Admin: manage movies, users, reviews, orders

## Run locally
```bash
python -m venv .venv
# activate venv
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


Test users (example)

fightclubenjoyer / BradPitt69
userb / Test12345!

Admin

link / HorsePenRainbow

Notes

Bootstrap via CDN, session-based cart, SQLite DB.


## 1.3 Make sure migrations exist
```powershell
python manage.py makemigrations
python manage.py migrate
