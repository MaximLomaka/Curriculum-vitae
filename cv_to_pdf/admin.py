from __future__ import unicode_literals
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from cv_to_pdf.models import *


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['dep_name', 'get_groups_count']
    search_fields = ['dep_name']
    inlines = [
        GroupInline,
    ]


class TechnicalExpertiseInline(admin.TabularInline):
    model = TechnicalExpertise
    extra = 1

    def get_queryset(self, request):
        queryset = super(TechnicalExpertiseInline, self).get_queryset(request)
        return queryset.order_by('index')


class ToolAndFrameworkInline(admin.TabularInline):
    model = ToolAndFramework
    extra = 1

    def get_queryset(self, request):
        queryset = super(ToolAndFrameworkInline, self).get_queryset(request)
        return queryset.order_by('index')


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


class CommunicationInline(admin.TabularInline):
    model = Communication
    extra = 1

    def get_queryset(self, request):
        queryset = super(CommunicationInline, self).get_queryset(request)
        return queryset.order_by('index')


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

    def get_queryset(self, request):
        queryset = super(EducationInline, self).get_queryset(request)
        return queryset.order_by('index')


class ResumeAdmin(admin.ModelAdmin):
    list_display = ['role', 'person_link', 'group_link', 'department_link']
    search_fields = ['role', 'person__first_name', 'person__last_name']
    inlines = [
        TechnicalExpertiseInline,
        ToolAndFrameworkInline,
        ProjectInline,
        CommunicationInline,
        EducationInline,
    ]

    def person_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.person._meta.model_name),
                    args=(obj.person.id,)), obj.person.get_full_name()))
    person_link.short_description = 'person'

    def group_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.person.group._meta.model_name),
                    args=(obj.person.group.id,)), obj.person.group.group_name))
    group_link.short_description = 'group'

    def department_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.person.group.department._meta.model_name),
                    args=(obj.person.group.department.id,)), obj.person.group.department.dep_name))
    department_link.short_description = 'department'


class PersonInline(admin.TabularInline):
    model = Person
    exclude = ('role', )
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    list_display = ('group_name', 'department_link')
    list_filter = ['department']
    search_fields = ['group_name']
    inlines = [
        PersonInline,
    ]

    def department_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.department._meta.model_name),
                    args=(obj.department.id,)), obj.department.dep_name))
    department_link.short_description = 'department'


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    list_display = ('get_full_name', 'get_resume_count', 'group_link', 'department_link')
    list_filter = ['group', 'group__department']
    search_fields = ['first_name', 'last_name']
    exclude = ('role',)
    inlines = [
        ResumeInline,
    ]

    def group_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.group._meta.model_name),
                    args=(obj.group.id,)), obj.group.group_name))
    group_link.short_description = 'group'

    def department_link(self, obj):
        return mark_safe("<a href={}>{}</a>".format(
            reverse('admin:{}_{}_change'.format(obj._meta.app_label, obj.group.department._meta.model_name),
                    args=(obj.group.department.id,)), obj.group.department.dep_name))
    department_link.short_description = 'department'


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(TechnicalExpertise)
admin.site.register(ToolAndFramework)
admin.site.register(Project)
admin.site.register(Communication)
admin.site.register(Education)
