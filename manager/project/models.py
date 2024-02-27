import datetime

from django.core.exceptions import ValidationError
from django.db import models

import account.models

from account.models import User


def validate_start_date(value):
    if value < datetime.date.today():
        raise ValidationError("La date de début ne peut pas être dans le passé.")


def validate_deadline_date(value):
    if value < datetime.date.today():
        raise ValidationError("La date de début ne peut pas être dans le passé.")


class Project(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    deadline = models.DateField()
    created_by = models.ForeignKey(account.models.User, related_name='projects', on_delete=models.CASCADE, )

    def __str__(self):
        return self.name

    def clean(self):
        if self.deadline < self.start_date:
            raise ValidationError("La date de fin ne peut pas être inférieure à la date de début.")
        super().clean()


class Todolist(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    project = models.ForeignKey(Project, related_name='todolist', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='todolist', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()
    deadline = models.DateField()
    is_done = models.BooleanField(default=False)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    todolist = models.ForeignKey(Todolist, related_name='tasks', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, related_name='tasks', on_delete=models.CASCADE)
    teams = models.ManyToManyField('Team', related_name="teams")
    reunions = models.ManyToManyField('Reunion')
    softwares = models.ManyToManyField('Software', related_name='softwares')
    material_resources = models.ManyToManyField('MaterialResource')

    def __str__(self):
        return self.name

    def clean(self):
        if self.deadline < self.start_date:
            raise ValidationError("La date de fin ne peut pas être inférieure à la date de début.")
        super().clean()

    def can_be_started(self):
        """Returns True if the task can be started based on the start date of other tasks."""
        unfinished_tasks = Task.objects.filter(
            is_done=False, start_date__lt=self.start_date
        )
        return not unfinished_tasks.exists()


class Product(models.Model):
    TYPE_CHOICES = (
        ('Cahier de charges', 'CD'),
        ('Document de conception', 'DC'),
        ('Code source', 'CS'),
        ('Code exécutable', 'CE'),
        ('Rapport de test', 'RT'),
        ('Manuel', 'MA',),
    )
    name = models.CharField(max_length=255, db_index=True)
    description = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=30, choices=TYPE_CHOICES)
    creation_date = models.DateField()
    task_associated = models.ForeignKey(Task, related_name='products', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name


class Reunion(models.Model):
    object = models.CharField(max_length=255, db_index=True)
    date = models.DateField()
    task_associated = models.ForeignKey(Task, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.object


class MeetingReport(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    reunion = models.ForeignKey(Reunion, on_delete=models.CASCADE)
    date = models.DateField()
    content = models.TextField()

    def __str__(self):
        return self.name


class SummaryReport(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    project = models.ForeignKey('Project', on_delete=models.CASCADE, null=True)
    meeting_reports = models.ManyToManyField(MeetingReport)
    date = models.DateField()

    def __str__(self):
        return self.name


class Agent(models.Model):
    matricule = models.CharField(max_length=10, unique=True)
    first_name = models.CharField(max_length=255, db_index=True)
    last_name = models.CharField(max_length=255, db_index=True)
    birth_date = models.DateField()
    recruitment_date = models.DateField()
    qualification = models.CharField(max_length=255)
    expertise_areas = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.first_name} {self.last_name} "


class Team(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    leader = models.OneToOneField(Agent, related_name='teams_leader', on_delete=models.SET_NULL, null=True)
    members = models.ManyToManyField(Agent, related_name='team_memberships')
    tasks = models.ManyToManyField(Task, related_name="tasks_todo")

    def __str__(self):
        return f"{self.name} team, led by {self.leader} "


class MaterialResource(models.Model):
    TYPE_CHOICES = (
        ('Partagée', 'P'),
        ('Exclusif', 'E'),
    )
    name = models.CharField(max_length=255, db_index=True)
    usage_mode = models.CharField(max_length=10, choices=TYPE_CHOICES)

    def __str__(self):
        return self.name


class Software(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
