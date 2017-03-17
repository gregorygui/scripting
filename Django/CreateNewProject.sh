echo -e "Django building new script...\n"

echo "Enter a name : "
read name
echo "Enter a port : "
read port
echo "Enter a name for the 1st app : "
read appname

django-admin startproject $name

cd $name
echo "python3 manage.py runserver $port" > LaunchServer.sh
chmod 755 LaunchServer.sh

python3 manage.py startapp $appname

echo "from django.http import HttpResponse


def index(request):
    return HttpResponse(\"Hello, welcome to your $name Django app\")" > $appname/views.py
    
echo "from django.conf.urls import url

from . import views

app_name= '$appname'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    ]" > $appname/urls.py

echo "from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
        url(r'^admin/', admin.site.urls),
	]" > $name/urls.py

mkdir -p $appname/templates/$appname
mkdir -p $appname/static/$appname

echo "Don't forget to create your superuser. You can now launch your project via the script LaunchServer.sh in the $name directory"
