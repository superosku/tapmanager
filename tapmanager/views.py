# -*- coding: utf-8 -*-

from django.contrib import messages

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.template import RequestContext
from django.db.models import Q
from django.contrib.auth.models import User, Group
from django.http import HttpResponse
from django.forms.util import ErrorList

from tapmanager.forms import *#RegisterForm, SettingsForm
from tapmanager.models import TapType, Tap

import decimal

from mycustomsql import my_custom_sql

import datetime
from django.utils import timezone

@login_required
def taps(request):
	#error_list = []
	taptypes = TapType.objects.filter(active=True).all()#.order_by('-price').all()
	taptypes = taptypes.extra(
		select={'price_is_null': 'price IS NULL'},
		order_by=['price_is_null', 'name']
	)
	#users = User.objects.filter(groups__name='tapmanager').order_by('username').all()
	users = my_custom_sql()

	if request.method == 'POST':
		userid = request.POST['userid']
		if Tap.objects.filter(maker=request.user, date__gt=timezone.now()-datetime.timedelta(seconds=10)).count() > 0:
			messages.error(request, "Too frequent, wait 10s")
			return redirect('tapmanager:taps')
		# Checkataan kaikki taptypet, fiksuin tapa mita keksin
		added_funds = False
		for taptype in taptypes:
			amount = request.POST["type-" + str(taptype.id)]
			# Cheking that we can convert amount to decimal
			if amount:
				try:
					amount = decimal.Decimal(float(amount))
				except:
					messages.error(request, 'Invalid value in "' + taptype.name + '", didnt add that.')
					amount = None
			# Jos amountti loyty ja on oikeessa muodossa
			if amount and amount <= 0:
				messages.error(request, 'Amount <= 0 in "' + taptype.name + '", didint add that.')
			elif amount:
				user = get_object_or_404(User, pk=int(request.POST['userid']))
				t = Tap(user=user, maker=request.user, taptype=taptype , amount=amount , active=True)
				t.save()
				added_funds = True
		if added_funds:
			messages.success(request, "Addeds funds succesfully")
		else:
			messages.error(request, "Nothing added")
		return redirect('tapmanager:taps')
	return render(request, "tapmanager/taps.html", {'users': users, 'taptypes': taptypes, 'messages': messages.get_messages(request) })
@login_required
def logout_view(request):
	logout(request)
	return redirect('tapmanager:login')
@login_required
def log(request, filter_log=None):
	if request.method == 'POST':
		tapid = request.POST['tapid']
		tap = get_object_or_404(Tap, pk=int(tapid))
		if tap.is_recent():
			total = tap.amount
			if tap.taptype and tap.taptype.price:
				total *= tap.taptype.price
			if tap.active:
				tap.active = False
			else:
				tap.active = True
			tap.save()
		else:
			messages.error(request, 'Tap not recent enough. You cannot modify it')
	if filter_log=='me':
		sel = 'me'
		taps = Tap.objects.filter(Q(user__id=request.user.id) | Q(maker__id=request.user.id)).order_by('-date')[:50]
	else:
		sel = 'all'
		taps = Tap.objects.order_by('-date')[:50]
	return render(request, "tapmanager/log.html", {'taps': taps, 'sel': sel, 'messages': messages.get_messages(request) })
@login_required
def settings(request):
	form = SettingsForm(request.POST or None)
	if request.POST and form.is_valid():
		oldpass = form.cleaned_data.get('oldpass', None)
		if not request.user.check_password(oldpass):
			errors = form._errors.setdefault('oldpass', ErrorList())
			errors.append(u"Wrong pass")
		else:
			newpass = form.cleaned_data.get('newpass2', None)
			email = form.cleaned_data.get('email', None)
			firstname = form.cleaned_data.get('firstname', None)
			lastname = form.cleaned_data.get('lastname', None)
			if newpass:
				request.user.set_password(newpass)
				request.user.save()
			if email:
				request.user.email = email;
				request.user.save()
			if firstname:
				request.user.first_name = firstname;
				request.user.save()
			if lastname:
				request.user.last_name = lastname
				request.user.save()

			return redirect("tapmanager:settings")
	return render(request, "tapmanager/settings.html", {'form': form,})

@login_required
@user_passes_test(lambda u: u.groups.filter(name='tapadmin').count() != 0)#, login_url='tapmanager:taps')
def tapadmin(request):
	form = AdminForm(request.POST or None)
	#users = User.objects.filter(groups__name='tapmanager').order_by('firstname', 'lastname', 'username').all()
	if request.POST and form.is_valid():
		amount = form.cleaned_data['amount']
		maker = request.user
		user = form.cleaned_data['users']
		t = Tap(taptype=None, user=user, maker=maker, active=True, amount=-amount)
		t.save()
		return redirect("tapmanager:tapadmin")
	return render(request, "tapmanager/admin.html", {'form': form,})

@login_required
def stats(request):
	return render(request, "tapmanager/stats.html", )

def login_view(request):
	form = MyAuthForm(data=request.POST or None)
	if request.POST and form.is_valid():
		username = form.cleaned_data['username']
		password = form.cleaned_data['password']
		user = authenticate(username=username, password=password)
		if user:
			login(request, user)
			return redirect('tapmanager:taps')
		else:
			messages.error(request, "Error in login")
	form.fields['username'].widget.attrs['class'] = 'form-control' 
	form.fields['password'].widget.attrs['class'] = 'form-control' 
	return render(request, "tapmanager/login.html", {'form':form, 'messages': messages.get_messages(request)}, context_instance=RequestContext(request))

def register(request):
	form = RegisterForm(data=request.POST or None)
	if request.POST and form.is_valid():
		username = form.cleaned_data['username']
		email = form.cleaned_data['email']
		pass1 = form.cleaned_data['pass1']
		firstname = form.cleaned_data['firstname']
		lastname = form.cleaned_data['lastname']
		user = User.objects.create_user(username, email, pass1, first_name=firstname, last_name=lastname)
		group, created = Group.objects.get_or_create(name='tapmanager')
		group.user_set.add(user)
		return redirect('tapmanager:login')
	return render(request, "tapmanager/register.html", {'form': form})
