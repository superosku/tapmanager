from django.contrib import admin
from tapmanager.models import TapType, Tap

admin.site.register(TapType)

class TapAdmin(admin.ModelAdmin):
	list_display = ('taptype_name', 'taptype_price', 'amount', 'user_name', 'maker_name', 'is_active')
admin.site.register(Tap, TapAdmin)

