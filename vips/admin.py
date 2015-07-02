from django.contrib import admin

# Register your models here.
from vips.models import Login, Vip, Member

admin.site.register(Login)
admin.site.register(Vip)
admin.site.register(Member)