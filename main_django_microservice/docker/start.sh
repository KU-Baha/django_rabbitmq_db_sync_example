while ! python manage.py migrate 2>&1; do
  echo "Migration is in progress status"
  sleep 3
done

while ! python manage.py collectstatic --no-input 2>&1; do
  echo "Collecting static files..."
  sleep 3
done

gunicorn config.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 2
