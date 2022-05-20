from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms

from users.models import Profile,Skill,Message

# Create your views here.
class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','username','email','password1','password2']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            match = User.objects.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('This email address is already exist')

    def __init__(self,*args,**kwargs):
        super(UserForm, self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = {"name","email","bio","short_intro","profile_image","location",
                  "social_github","social_twitter","social_linkedln","social_youtube","social_website"}
        labels = {
            "bio":"Bio",
            "short_intro":"Introduction",
            "profile_image":"Image",
            "social_github":"Github",
            "social_website":"Website",
            "social_youtube":"Youtube",
            "social_linkedln":"Linkedln",
            "social_twitter":"Twitter"
        }

    def __init__(self,*args,**kwargs):
        super(ProfileForm, self).__init__(*args,**kwargs)
        for name, field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = {"name","description"}
        exclude = ['owner']

    def __init__(self,*args,**kwargs):
        super(SkillForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})

class MessageForm(ModelForm):
    class Meta:
        model = Message
        fields = {"name","email","subject","body"}

    def __init__(self,*args,**kwargs):
        super(MessageForm, self).__init__(*args,**kwargs)
        for name,field in self.fields.items():
            field.widget.attrs.update({'class':'input'})
