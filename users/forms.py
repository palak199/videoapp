from django import forms  
from users.models import Creator,Viewer,Video

class CreatorForm(forms.ModelForm):  
    class Meta:  
        model = Creator 
        password = forms.CharField(widget=forms.PasswordInput)
        fields = "__all__"  
        
class ViewerForm(forms.ModelForm):  
    class Meta:  
        model = Viewer 
        password = forms.CharField(widget=forms.PasswordInput)
        fields = "__all__" 
         
class VideoForm(forms.ModelForm):  
    class Meta:  
        model = Video 
        fields = "__all__"  
        
class LoginForm(forms.Form):
     username = forms.CharField(label="USER NAME", max_length=100)
     password = forms.CharField(label="PASSWORD", max_length=150)
     User_Type =( 
        ("Creator", "Creator"), 
        ("Viewer", "Viewer"), ) 
     user_type = forms.ChoiceField(label="ARE YOU",choices = User_Type) 