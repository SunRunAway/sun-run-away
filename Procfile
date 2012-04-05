web: python DjangoBlog/manage.py collectstatic --noinput ; python DjangoBlog/manage.py run_gunicorn -b 0.0.0.0:$PORT -w 3
worker: python DjangoBlog/manage.py celeryd -E -B --loglevel=INFO
