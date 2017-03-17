echo -e "Django building new App...\n"

echo "Enter the project name : "
read name
echo "Enter a name for the app : "
read appname

cd $name
python manage.py startapp $appname

echo "from django.http import HttpResponse


def index(request):
    return HttpResponse(\"Hello, welcome to your $appname Django app (Project $name)\")" > $appname/views.py
    
echo "from django.conf.urls import url

from . import views

app_name= '$appname'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    ]" > $appname/urls.py

mkdir -p $appname/templates/$appname
mkdir -p $appname/static/$appname

echo "Don't forget to reference your new app $appname in the urls project file"

