from django import forms

from django.contrib.auth.models import User

class RegisterForm(forms.Form):
	username = forms.CharField(
			label="Username", 
			widget=forms.TextInput(attrs={'class':'form-control'}), )
	firstname = forms.CharField(
			label="First name", 
			widget=forms.TextInput(attrs={'class':'form-control'}), )
	lastname = forms.CharField(
			label="Last name", 
			widget=forms.TextInput(attrs={'class':'form-control'}), )
	email = forms.EmailField(
			label="Email",
			widget=forms.EmailInput(attrs={'class':'form-control'}), )
	pass1 = forms.CharField(
			label="Password",
			widget=forms.PasswordInput(attrs={'class':'form-control'}), )
	pass2 = forms.CharField(
			label="Password again",
			widget=forms.PasswordInput(attrs={'class':'form-control'}), )
	def clean_username(self):
		existing = User.objects.filter(username__iexact=self.cleaned_data['username'])
		if existing.exists():
			raise forms.ValidationError(("Username exists"))
		return self.cleaned_data['username']
	def clean_pass2(self):
		p1 = self.cleaned_data.get('pass1', None)
		p2 = self.cleaned_data.get('pass2', None)
		if p1 != p2:
			raise forms.ValidationError("Passwords didint match")
		return p1

class SettingsForm(forms.Form):
	email = forms.EmailField(
			label="Email",
			widget=forms.EmailInput(attrs={'class':'form-control'}),
			required=False, )
	firstname = forms.CharField(
			label="First name", 
			widget=forms.TextInput(attrs={'class':'form-control'}), )
	lastname = forms.CharField(
			label="Last name", 
			widget=forms.TextInput(attrs={'class':'form-control'}), )
	newpass1 = forms.CharField(
			label="New password",
			widget=forms.PasswordInput(attrs={'class':'form-control'}),
			required=False, )
	newpass2 = forms.CharField(
			label="New password again",
			widget=forms.PasswordInput(attrs={'class':'form-control'}), 
			required=False, )
	oldpass = forms.CharField(
			label="Old password (required)",
			widget=forms.PasswordInput(attrs={'class':'form-control'}), )
	def clean_newpass2(self):
		new1 = self.cleaned_data.get('newpass1', None)
		new2 = self.cleaned_data.get('newpass2', None)
		if new1 != new2:
			raise forms.ValidationError('New passwords didnt match')
		return new2

class CustomUserChoiceField(forms.ModelChoiceField):
	def label_from_instance(self, obj):
		return obj.get_full_name()
class AdminForm(forms.Form):
	users = CustomUserChoiceField(
			queryset=User.objects.filter(groups__name='tapmanager').order_by('username').all(),
			label="User",
			empty_label="--- (Choose) ---",
			widget=forms.Select(attrs={'class':'form-control'}), )
	amount = forms.DecimalField(
			max_digits=7,
			decimal_places=2,
			label="Amount",
			widget=forms.TextInput(attrs={'class':'form-control'}), )


