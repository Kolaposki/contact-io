from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Contacts
from import_export.admin import ImportExportModelAdmin


class ContactsAdmin(ImportExportModelAdmin):  # formerly class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'manager', 'name',)
    # list_editable = ('email', 'info')
    list_display_links = ('id', 'manager')
    list_per_page = 20  # show 10 contacts per page
    search_fields = ('name', 'manager__username')  # fields to be able to search for
    list_filter = ('gender', 'manager', 'date_added')  # option to filter by a property


admin.site.register(Contacts, ContactsAdmin)
admin.site.unregister(Group)  # remove Group objects from admin page:  under[Authentication and Authorization]
