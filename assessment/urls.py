
from django.contrib import admin  
from django.urls import path, re_path
from users import views  
from django.conf.urls import  include

urlpatterns = [ 
    #paths for creator (Admin)
    path('', views.login),
    path('logout', views.logout),
    path('profile', views.creator_profile, name="creatorprofile"),
    path('admin/', admin.site.urls),  
    path('addcreator', views.creator_create, name="creatorsignup"),  
    
    # path('showcreator',views.creator_show),  
    re_path(r'^editcreator/(?P<username>.*[^ ].*)', views.creator_edit, name="editcreator"),  
    re_path(r'^updatecreator/(?P<username>.*[^ ].*)', views.creator_update, name="updatecreator" ),  
    re_path(r'^deletecreator/(?P<username>.*[^ ].*)', views.creator_destroy, name="destroycreator"), 
    
    #paths for viewer
    path('addviewer', views.viewer_create, name="viewersignup"),  
    # path('showviewer', views.creator_show),  
    re_path(r'^editviewer/(?P<username>.*[^ ].*)', views.viewer_edit, name="editviewer"),  
    re_path(r'^updateviewer/(?P<username>.*[^ ].*)', views.viewer_update, name="updateviewer"),  
    re_path(r'^deleteviewer/(?P<username>.*[^ ].*)', views.viewer_destroy, name="deleteviewer"),  
    
    #paths for video
    path('addvideo', views.video_create, name="addvideo"),  
    path('showvideo', views.video_show, name="showvideo"),  
    re_path(r'^editvideo/(?P<id>.*[^ ].*)', views.video_edit, name="editvideo"),  
    re_path(r'^updatevideo/(?P<id>.*[^ ].*)', views.video_update, name="updatevideo"),  
    re_path(r'^deletevideo/(?P<id>.*[^ ].*)', views.video_destroy, name="deletevideo"),  
]  