sudo service gunicorn-montyhall stop
rm instance/montyhall.db
sudo service gunicorn-montyhall start

