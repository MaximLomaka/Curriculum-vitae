# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models


class Department(models.Model):
    dep_name = models.CharField(max_length=255)

    def __str__(self):
        return self.dep_name

    def get_groups(self):
        return self.group_set.all()

    def get_groups_count(self):
        return self.group_set.count()


class Group(models.Model):
    department = models.ForeignKey(Department, on_delete=models.CASCADE, default=None)
    group_name = models.CharField(max_length=255)

    def __str__(self):
        return self.group_name

    def get_employees(self):
        return self.person_set.all()


class Person(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE, default=None)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    ROLES = (
        ('Junior', 'Junior'),
        ('Middle', 'Middle'),
        ('Senior', 'Senior')
    )
    role = models.CharField(max_length=7, choices=ROLES, null=True)

    def __str__(self):
        return ' '.join([self.first_name, self.last_name])

    def get_full_name(self):
        return ' '.join([self.first_name, self.last_name])

    def get_resume(self):
        return self.resume_set.all()

    def get_resume_count(self):
        return self.resume_set.count()


class Resume(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, default=None)
    role = models.CharField(max_length=255)

    def __str__(self):
        return self.person.get_full_name()

    def get_technical_expertise(self):
        return self.technicalexpertise_set.all()

    def get_tool_and_framework(self):
        return self.toolandframework_set.all()

    def get_project(self):
        return self.project_set.all()

    def get_communication(self):
        return self.communication_set.all()

    def get_education(self):
        return self.education_set.all()


class TechnicalExpertise(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.description[:10] + '...'


class ToolAndFramework(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.name


class Project(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    is_nda = models.BooleanField(default=False)
    project_title = models.CharField(max_length=255)
    nda_title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField()
    team = models.CharField(max_length=255)
    role = models.CharField(max_length=255)
    skills = models.CharField(max_length=255)

    def __str__(self):
        return self.project_title


class Communication(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    description = models.TextField()
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.description[:10] + '...'


class Education(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, default=None)
    place = models.CharField(max_length=255)
    specialization = models.CharField(max_length=255)
    year_of_ending = models.IntegerField(blank=True, null=True)
    index = models.SmallIntegerField(default=0)

    def __str__(self):
        return self.place[:10] + '...'
