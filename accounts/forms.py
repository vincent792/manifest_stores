from  django import forms
from accounts.models import Account

class RegistrationForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Enter Password'
		}))
	password2=forms.CharField(widget=forms.PasswordInput(attrs={
		'placeholder': 'Confirm Password'
		}))
	class Meta:
		model= Account
		fields=['first_name', 'last_name', 'phone', 'email', 'password']
	def __init__(self, *args, **kwargs):
		super(RegistrationForm, self). __init__(*args, **kwargs)
		self.fields['first_name'].widget.attrs['placeholder']= 'Enter First Name'
		self.fields['last_name'].widget.attrs['placeholder']= 'Enter Last Name'
		self.fields['phone'].widget.attrs['placeholder']= 'Enter Phone Number'
		self.fields['email'].widget.attrs['placeholder']= 'Enter Email Address'

		for  field in  self.fields:
			self.fields[field].widget.attrs['class']= 'form-control'

	def clean(self):
		cleaned_data= super(RegistrationForm, self).clean()
		password=cleaned_data.get('password')
		password2=cleaned_data.get('password2')

		if password != password2:
			raise forms.ValidationError(
				'Password Missmatch',
				)
		elif len(password)<8:
			raise forms.ValidationError(
				"Password must be at least 8 characters long.",
				)