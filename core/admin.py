from django.contrib import admin
from .models import *
from django.contrib.auth.models import User, Group
from cities_light.admin import *
from online_users.admin import *
# Register your models here.


# Activate uploaded properties by users

@admin.action(description='Activate Selected Properties',)
def make_active(modeladmin, request, queryset):
    queryset.update(active=True)


# Deactivate uploaded properties by users

@admin.action(description='Deactivate Selected Properties',)
def make_inactive(modeladmin, request, queryset):
    queryset.update(active=False)


class PropertyImageAdmin(admin.TabularInline):
    model = PropertyImage


@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'active', 'date_posted']
    list_filter = ['active', 'date_posted']
    inlines = [PropertyImageAdmin]
    actions = [make_active, make_inactive]


admin.site.register(Category)

# Remove other models from appearing in the admin panel
admin.site.unregister(User)
admin.site.unregister(Group)
admin.site.unregister(City)
admin.site.unregister(Country)
admin.site.unregister(Region)
admin.site.unregister(SubRegion)
admin.site.unregister(OnlineUserActivity)
