from django import forms
from django.core.exceptions import ValidationError
from app.models import Profile, User, Question, Tag, Answer

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput())

class RegisterForm(forms.ModelForm):
    password_confirm = forms.CharField(max_length=100, widget=forms.PasswordInput(), label="Password confirmation")
    avatar = forms.ImageField(required=False, label="Avatar")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean_username(self):
        username = self.cleaned_data['username'].strip()
        if User.objects.filter(username=username).exists():
            raise ValidationError("A user with the same name already exists!")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].strip()
        if User.objects.filter(email=email).exists():
            raise ValidationError("This email address is already in use!")
        return email

    def clean_password_confirm(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise ValidationError("Passwords do not match!")
        return self.cleaned_data['password_confirm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        Profile.objects.create(user=user, avatar=self.cleaned_data.get('avatar', None))
        return user

class QuestionForm(forms.ModelForm):
    tags = forms.CharField(required=False, max_length=128, label="Tags")

    class Meta:
        model = Question
        fields = ['title', 'text']

    def __get_or_create_tags(self):
        tags_list = self.cleaned_data['tags'].split()
        tags = []

        for tag in tags_list:
            tag_object, created = Tag.objects.get_or_create(name=tag.lower().strip())
            tags.append(tag_object)

        return tags

    def save(self, commit=True):
        question = super().save(commit=False)
        question.author = self.user.profile
        if commit:
            question.save()
            question.tags.set(self.__get_or_create_tags())
        return question

class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['text']

    def save(self, commit=True):
        answer = super().save(commit=False)
        answer.author = self.user.profile
        answer.question = self.question
        if commit:
            answer.save()
        return answer
