from django.contrib import admin
from tapmanager.models import TapType, Tap

class TapTypeAdmin(admin.ModelAdmin):
	list_display = ('name', 'price', 'active')
admin.site.register(TapType, TapTypeAdmin)

class TapAdmin(admin.ModelAdmin):
	list_display = ('taptype_name', 'taptype_price', 'amount', 'user_name', 'maker_name', 'is_active')
admin.site.register(Tap, TapAdmin)

