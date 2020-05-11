from django.contrib import admin
from django.contrib.auth.models import Group
# Register your models here.
from .models import Contacts
from import_export.admin import ImportExportModelAdmin


class ContactsAdmin(ImportExportModelAdmin):  # formerly class ContactsAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'gender', 'email', 'info', 'phone')
    list_editable = ('email', 'info')
    list_display_links = ('id', 'name')  # add a link to access info about the contact [ initially was 'id' ]
    list_per_page = 10  # show 10 contacts per page
    search_fields = ('name', 'email', 'info')  # fields to be able to search for
    list_filter = ('gender',)  # option to filter by a property


admin.site.register(Contacts, ContactsAdmin)
admin.site.unregister(Group)  # remove Group objects from admin page:  under[Authentication and Authorization]
