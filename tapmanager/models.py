import datetime

from django.db import models

from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.signals import request_started

from django.utils import timezone

class TapType(models.Model):
	name = models.CharField(max_length=30)
	price = models.DecimalField(max_digits=7, decimal_places=2, null=True, blank=True) # if null, price is just the amount
	active = models.BooleanField()
	def __unicode__(self):
		if self.price:
			return "{0} ({1})".format(self.name, self.price)
		return "{0}".format(self.name)

class Tap(models.Model):
	taptype = models.ForeignKey(TapType, null=True)
	user = models.ForeignKey(User)
	maker = models.ForeignKey(User, related_name='maker')
	active = models.BooleanField(default=True)
	amount = models.DecimalField(max_digits=7, decimal_places=2)
	date = models.DateTimeField(auto_now_add=True)
	def is_recent(self):
		return self.date >= timezone.now() - datetime.timedelta(hours=1)
	def taptype_name(self):
		if self.taptype and self.taptype.name: return self.taptype.name
		return "Payback"
	def taptype_price(self):
		if self.taptype and self.taptype.price: return self.taptype.price
		return ""
	def maker_name(self):
		return self.maker.get_full_name()
	def user_name(self):
		return self.user.get_full_name()
	def is_active(self):
		return self.active
	def get_date(self):
		return self.date.strftime("%H:%M | %d.%m.%y")
	def has_type(self):
		if self.taptype: return True
		return False
	is_active.boolean = True

