from django.contrib import admin
from users.models import Creator,Viewer,Video

models=[Creator,Viewer,Video]
admin.site.register(models)