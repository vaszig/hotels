from django import forms
from django.contrib import admin

from app.models import Hotel, City
from managers.models import Manager


class ManagerAdminArea(admin.AdminSite):
    site_header = 'Manager database'


class ManagerPermissions(admin.ModelAdmin):      
    
    list_display = ('name', 'city')
    
    def get_queryset(self, request):
        if request.user.groups.filter(name='managers').exists():
            qs = super().get_queryset(request)
            cities = []
            for manager in request.user.manager_set.all():
                cities.append(manager.city)
            return qs.filter(city__in=cities)
        return Hotel.objects.none()

    def get_form(self, request, obj=None, *args, **kwargs):
        if obj:
            kwargs['exclude'] = ['id', 'city']
        else:
            kwargs['fields'] = ['id', 'name', 'city']
        return super().get_form(request, obj, *args, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "city":
            kwargs["queryset"] = City.objects.filter(id=request.user.manager.city.id)
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def has_add_permission(self, request):
        if request.user.groups.filter(name='managers').exists():
            return True            
        
    def has_delete_permission(self, request, obj=None):
        if obj is None and request.user.groups.filter(name='managers').exists():
            return True
        elif obj is not None:
            return obj.city==request.user.manager.city

    def has_change_permission(self, request, obj=None):
        if obj is None and request.user.groups.filter(name='managers').exists():
            return True
        elif obj is not None:
            return obj.city==request.user.manager.city
        

manager_site = ManagerAdminArea(name='ManagerAdmin')
manager_site.register(Hotel, ManagerPermissions)
admin.site.register(Manager)