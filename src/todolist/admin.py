from django.contrib import admin
from .models import Work, Card


class CardInline(admin.TabularInline):
    model = Card
    extra = 0


class WorkAdmin(admin.ModelAdmin):
    inlines = [CardInline]
    search_fields = ['name']
    list_filter = ['create_date']
    list_display = ('name', 'owner', 'create_date', 'modify_date', 'done')


class CardAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_filter = ['create_date']
    list_display = ('name', 'owner', 'create_date', 'modify_date', 'done')


# Register your models here.
admin.site.register(Work, WorkAdmin)
admin.site.register(Card, CardAdmin)
