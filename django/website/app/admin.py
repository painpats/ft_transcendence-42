from django.contrib import admin
from .models import Friend, Game, Member, Dashboard

admin.site.register(Member)
admin.site.register(Friend)
admin.site.register(Game)
admin.site.register(Dashboard)