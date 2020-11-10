from django.shortcuts import render, redirect  
from users.forms import VideoForm, ViewerForm, CreatorForm , LoginForm
from users.models import Creator,Viewer,Video 
from django.shortcuts import get_object_or_404 
import json
from django.http import HttpResponse

def login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
             if(form.cleaned_data['user_type']=="Creator"):
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user = get_object_or_404(Creator,username=username,password=password)
                if(user):
                    request.session['user'] = user.id
                    return redirect('/profile')  # takes the admin to profile where he/she can see the video analytics
                    
             else:
                username=form.cleaned_data['username']
                password=form.cleaned_data['password']
                user= get_object_or_404(Viewer,username=username,password=password)
                if(user):
                    request.session['user'] = user.id
                    return redirect('/showvideo') #if the user is only a viewer then he/she can see videos and like them
    else:
        form = LoginForm()
    return render(request,"login.html",{"form":form})
def logout(request):
    del request.session['user']  
    return redirect('/')      
def creator_profile(request):
    try:
        videos = Video.objects.filter(creator=request.session['user'])
        user = Creator.objects.get(id=request.session['user'])
        labels = []
        data = []
        for video in videos:
            labels.append(video.name)
            data.append(video.total_likes)
        ctx={
        "username": user.username,
        "videos": videos,
        'labels': labels,
        'data': data,
        }
        return render(request,"profile.html",ctx)
    except KeyError:
        user = Creator.objects.get(id=request.session['user'])
        ctx={
        "username": user.username,
        
        }
        return render(request, "profile.html", ctx)
       
# creator views here.  
def creator_create(request):  
    if request.method == "POST":  
        form = CreatorForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                newuser=Creator.objects.get(username= form.cleaned_data['username']) 
                request.session['user']=newuser.id
                return redirect('/profile')  
            except:  
                pass  
    else:  
        form = CreatorForm()  
    return render(request,'signupcreator.html',{'form':form})  

# def creator_show(request):  
#     creators = Creator.objects.all()  
#     return render(request,"show.html",{'creators':creators})  

def creator_edit(request, username):  
    creator = Creator.objects.get(username=username)  
    return render(request,'editcreator.html', {'creator':creator})  

def creator_update(request, username):  
    creator = Creator.objects.get(username=username)  
    form = CreatorForm(request.POST, instance = creator)  
    if form.is_valid():  
        form.save()  
        try:  
            form.save()  
            return redirect('/showcreator')  
        except:  
            pass  
    else:  
       
        form = CreatorForm()  
    return render(request, 'editcreator.html', {'creator': creator})  

def creator_destroy(request, username):  
    creator = Creator.objects.get(username=username)  
    creator.delete()  
    return redirect("/showcreator") 
 
# viewer views here
def viewer_create(request):  
    if request.method == "POST":  
        form = ViewerForm(request.POST)  
        if form.is_valid():  
            try:  
                form.save()  
                newuser=Creator.objects.get(username= form.cleaned_data['username']) 
                request.session['user']=newuser.id
                return redirect('/showvideo')  
            except:  
                pass  
        
    else:  
        form = ViewerForm()  
    return render(request,'signupviewer.html',{'form':form})  

# def viewer_show(request):  
#     viewers = Viewer.objects.all()  
#     return render(request,"show.html",{'viewers':viewers})  

def viewer_edit(request, username):  
    viewer = Viewer.objects.get(username=username)  
    return render(request,'editviewer.html', {'viewer':viewer})  

def viewer_update(request, username):  
    viewer = Viewer.objects.get(username=username)  
    form = ViewerForm(request.POST, instance = viewer)  
    if form.is_valid():  
        form.save()  
        try:  
            form.save()  
            return redirect('/showvideo')  
        except:  
            pass  
    else:  
       
        form = ViewerForm()  
    return render(request, 'editviewer.html', {'viewer': viewer})  

def viewer_destroy(request, username):  
    viewer = Creator.objects.get(username=username)  
    viewer.delete()  
    return redirect("") 
 

# video views here 
def video_create(request): 
    user=Creator.objects.get(id=request.session['user'])
    
    if request.method == "POST":  
        form = VideoForm(request.POST)  
        if form.is_valid():  
            try:  
                print('valid')
                form.save()  
                return redirect('/profile')  
            except:  
                pass  
        else:
            print(form.errors)
    else:  
        form = VideoForm()  
    return render(request,'videocreate.html',{'form':form, "user":user.username}) 

def video_show(request):
    if request.method =="POST":
        if request.POST.get("operation") == "like_submit" and request.is_ajax():
            video_id=request.POST.get("video_id",None)
            video=get_object_or_404(Video,id=video_id)
            if video.likes.filter(id=request.session['user']): #already liked the video
                video.likes.remove(request.session['user']) #remove user from likes 
                liked=False
            else:
                video.likes.add(request.session['user'])
                liked=True
        ctx={"likes_count":video.total_likes,"liked":liked,"video_id":video_id}
        return HttpResponse(json.dumps(ctx), content_type='application/json')
    videos = Video.objects.all() 
    already_liked=[]
    id=request.session['user']
    user=Viewer.objects.get(id=id)
    for video in videos:
        if(video.likes.filter(id=id).exists()):
            already_liked.append(video.id)
    context={"videos":videos,"already_liked":already_liked,"user":user}
    return render(request,"showvideos.html",context)  

        
def video_edit(request, id):  
    video = Video.objects.get(id=id)  
    return render(request,'editvideo.html', {'video':video})  

def video_update(request, id):  
    video= Video.objects.get(id=id)
    form = VideoForm(request.POST, instance = video)  
    if form.is_valid():  
        form.save()  
        try:  
            form.save()  
            return redirect('/showvideo')  
        except:  
            pass  
    else:  
        print(form.errors)
        form = VideoForm()  
    return render(request, 'editvideo.html', {'video': video})  

def video_destroy(request, id):  
    video = Video.objects.get(id=id)  
    video.delete()  
    return redirect("/profile")  