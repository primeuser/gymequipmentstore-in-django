from django import forms
from .models import *
from django.contrib.auth.models import User
from django_summernote.widgets import SummernoteWidget, SummernoteInplaceWidget


# -------- CLIENT FORMS ---------
# -------- CLIENT FORMS ---------
# -------- CLIENT FORMS ---------
# -------- CLIENT FORMS ---------


class ClientContactForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['name', 'email', 'phone', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'data-validation': 'required',
                'placeholder': 'Enter Your Name'
            }),
            'email': forms.EmailInput(attrs={
                'data-validation': 'required',
                'placeholder': 'Enter your Email',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
            }),
            'phone': forms.TextInput(attrs={
                'data-validation': 'required',
                'placeholder': 'Enter contact number',
                'pattern': '[0-9]{10}'

            }),
            'message': forms.Textarea(attrs={
                'data-validation': 'required',
                'placeholder': 'Your Message'
            }),
        }


# class ClientAppointmentForm(forms.ModelForm):

#     class Meta:
#         model = Appointment
#         autocomplete_fields = ['doctor']

#         fields = ['patient_name', 'email', 'mobile', 'doctor', 'date',
#                   'details']
#         widgets = {
#             'patient_name': forms.TextInput(attrs={
#                 'data-validation': 'required',
#                 'placeholder': 'Enter your name',
#             }),
#             'email': forms.EmailInput(attrs={
#                 'data-validation': 'required',
#                 'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
#                 'placeholder': 'Enter your email',
#             }),
#             'mobile': forms.NumberInput(attrs={
#                 'data-validation': 'required',
#                 'placeholder': 'Enter phone number',
#             }),
#             'doctor': forms.Select(attrs={
#                 'class': 'form-doctor',
#                 'data-validation': 'required',

#                 # 'placeholder': 'Doctor',
#             }),

#             'date': forms.DateInput(attrs={
#                 'data-validation': 'required',
#                 'placeholder': 'Appointment date',
#                 'id': 'datetimepicker1',


#             }),
#             'details': forms.Textarea(attrs={
#                 'placeholder': 'Details',
#             }),
#             # 'appointed_time': forms.TimeInput(attrs={
#             #     'data-validation': 'required',
#             #     'placeholder': 'Appointment time',
#             #     'id': 'datetimepicker3'
#             # }),

#         }


class ClientSubscriberForm(forms.ModelForm):
    class Meta:
        model = Subscriber
        fields = ['email']
        widget = {
            'email': forms.EmailInput(attrs={
                'data-validation': 'required',
                'placeholder': 'Enter your Email',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
            })
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if Subscriber.objects.filter(email=email).exists():
            print("Email exists")
            raise forms.ValidationError(
                "User already registered.", code="email",)
        else:
            # print("Email doesnot exist.")
        # 
            return email


class ClientLoginForm(forms.Form):

    # class Meta:
    #     model = Appointment
    #     autocomplete_fields = ['doctor']

    #     fields = ['patient_name', 'email', 'mobile', 'doctor', 'date',
    #               'details']
    #     widgets = {
    #         'patient_name': forms.TextInput(attrs={
    #             'data-validation': 'required',
    #             'placeholder': 'Enter your name',
    #         }),
    #         'email': forms.EmailInput(attrs={
    #             'data-validation': 'required',
    #             'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
    #             'placeholder': 'Enter your email',
    #         }),





    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password'
    }))


class ClientRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=30, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Choose Username',
    }),)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Enter Password',
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = Client
        fields = ['username', 'password1', 'password2',
                  'name', 'phone','email','image']
        widgets = {

            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Name',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'data-validation': 'required',
                'pattern': '[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,3}$',
                'placeholder': 'Enter your email',
            }),
            'phone': forms.NumberInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]+',
                'placeholder': 'Enter Phone Number',
            }),
            'image': forms.ClearableFileInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter image',
            }),

        }

    def clean(self):
        cleaned_data = super(ClientRegistrationForm, self).clean()
        username = cleaned_data.get('username')
        print(username)
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("username already exists")
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 != password2:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )

        return cleaned_data

