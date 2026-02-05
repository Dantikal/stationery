web: python -m gunicorn constr_store.wsgi:application --bind 0.0.0.0:$PORT
release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
