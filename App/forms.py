from django.forms import ModelForm
from .models import A,Q,CustomUser

class AnswerForm(ModelForm):
    class Meta:
        model=A
        fields=('a', )

class QuestionForm(ModelForm):
    class Meta:
        model=Q
        fields=('title','content','tags' )
    def __init__(self, *args, **kwargs):
        super(QuestionForm, self).__init__(*args, **kwargs)
        self.fields['tags'].widget.attrs.update({'placeholder': 'Gym, Python, Cooking'})

class ProfileForm(ModelForm):
    class Meta:
        model=CustomUser
        fields=('first_name','last_name','username','bio','location')