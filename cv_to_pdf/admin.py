from __future__ import unicode_literals
from django.contrib import admin
from django.urls import reverse
from django.utils.safestring import mark_safe

from cv_to_pdf.models import *


class GroupInline(admin.TabularInline):
    model = Group
    extra = 1


class DepartmentAdmin(admin.ModelAdmin):
    def dep_group_count(self, obj):
        return obj.group_set.count()
    dep_group_count.short_description = "Groups Count"

    list_display = ['dep_name', 'dep_group_count']
    search_fields = ['dep_name']
    inlines = [
        GroupInline,
    ]


class TechnicalExpertiseInline(admin.TabularInline):
    model = TechnicalExpertise
    extra = 1


class ToolAndFrameworkInline(admin.TabularInline):
    model = ToolAndFramework
    extra = 1

    def get_queryset(self, request):
        queryset = super(ToolAndFrameworkInline, self).get_queryset(request)
        queryset = queryset.order_by('index')
        return queryset


class ProjectInline(admin.StackedInline):
    model = Project
    extra = 1


class CommunicationInline(admin.TabularInline):
    model = Communication
    extra = 1

    def get_queryset(self, request):
        queryset = super(CommunicationInline, self).get_queryset(request)
        queryset = queryset.order_by('index')
        return queryset


class EducationInline(admin.TabularInline):
    model = Education
    extra = 1

    def get_queryset(self, request):
        queryset = super(EducationInline, self).get_queryset(request)
        queryset = queryset.order_by('index')
        return queryset


class ResumeAdmin(admin.ModelAdmin):
    def person_link(self, obj):
        person = Person.objects.get(pk=obj.person.id)
        return mark_safe('<a href="/admin/cv_to_pdf/person/{}/change/">{}</a>'.format(
            person.id,
            person.get_full_name()
        ))
    person_link.short_description = 'person'

    def group_link(self, obj):
        group = Group.objects.get(pk=obj.person.group.id)
        return mark_safe('<a href="/admin/cv_to_pdf/group/{}/change/">{}</a>'.format(
            group.id,
            group.group_name
        ))
    group_link.short_description = 'group'

    def department_link(self, obj):
        department = Department.objects.get(pk=obj.person.group.department.id)
        return mark_safe('<a href="/admin/cv_to_pdf/department/{}/change/">{}</a>'.format(
            department.id,
            department.dep_name
        ))
    department_link.short_description = 'department'

    list_display = ['role', 'person_link', 'group_link', 'department_link']
    search_fields = ['role', 'person__first_name', 'person__last_name']
    inlines = [
        TechnicalExpertiseInline,
        ToolAndFrameworkInline,
        ProjectInline,
        CommunicationInline,
        EducationInline,
    ]


class PersonInline(admin.TabularInline):
    model = Person
    exclude = ('role', )
    extra = 1


class GroupAdmin(admin.ModelAdmin):
    def department_link(self, obj):
        department = Department.objects.get(pk=obj.department.id)
        return mark_safe('<a href="/admin/cv_to_pdf/department/{}/change/">{}</a>'.format(
            department.id,
            department.dep_name
        ))
    department_link.short_description = 'department'

    list_display = ('group_name', 'department_link')
    list_filter = ['department']
    search_fields = ['group_name']
    inlines = [
        PersonInline,
    ]


class ResumeInline(admin.TabularInline):
    model = Resume
    extra = 1


class PersonAdmin(admin.ModelAdmin):
    def person_cv_count(self, obj):
        return obj.resume_set.count()
    person_cv_count.short_description = "CV Count"

    def show_full_name(self, obj):
        return ' '.join([obj.first_name, obj.last_name])
    show_full_name.short_description = "Person"

    def group_link(self, obj):
        group = Group.objects.get(pk=obj.group.id)
        return mark_safe('<a href="/admin/cv_to_pdf/group/{}/change/">{}</a>'.format(
            group.id,
            group.group_name
        ))
    group_link.short_description = 'group'

    def department_link(self, obj):
        department = Department.objects.get(pk=obj.group.department.id)
        return mark_safe('<a href="/admin/cv_to_pdf/department/{}/change/">{}</a>'.format(
            department.id,
            department.dep_name
        ))
    department_link.short_description = 'department'

    list_display = ('show_full_name', 'person_cv_count', 'group_link', 'department_link')
    list_filter = ['group', 'group__department']
    search_fields = ['first_name', 'last_name']
    exclude = ('role',)
    inlines = [
        ResumeInline,
    ]


admin.site.register(Department, DepartmentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(Person, PersonAdmin)
admin.site.register(Resume, ResumeAdmin)
admin.site.register(TechnicalExpertise)
admin.site.register(ToolAndFramework)
admin.site.register(Project)
admin.site.register(Communication)
admin.site.register(Education)
