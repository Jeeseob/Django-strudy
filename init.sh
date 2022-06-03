#!/bin/sh
echo "------ create default admin user ------"
echo "from django.contrib.auth.models import User; User.objects.create_superuser('jeeseob', 'jeeseob5761@gmail.com', '0000')" | python manage.py shell