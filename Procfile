web: python DjangoBlog/manage.py run_gunicorn -b "0.0.0.0:$PORT" -w 3
web: python myapp/manage.py collectstatic --noinput; bin/gunicorn_django --workers=4 --bind=0.0.0.0:$PORT myapp/settings.py
