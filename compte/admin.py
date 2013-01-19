from compte.models import Compte, Categorie, User
from django.contrib import admin

class CompteAdmin(admin.ModelAdmin):
    fields = ('date', 'date_sup', 'user','mntTotal','mnt','remb','motif','categorie',)
    list_display = ('date', 'date_sup', 'user','remb',)
    list_filter = ['date']
    search_fields = ['motif']
    date_hierarchy = 'date'
    
admin.site.register(Compte, CompteAdmin)
admin.site.register(Categorie)
admin.site.register(User)