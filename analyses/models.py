from dataclasses import fields
from django.db import models
from django.contrib.postgres.fields import ArrayField
import uuid


class Analysis(models.Model):
    class Status(models.TextChoices):
        FINISHED = "Finished"
        PENDING = "Pending"
        IN_PROGRESS = "In progress"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    sample = models.UUIDField(primary_key=False)
    laborant = models.UUIDField(primary_key=False)
    lab = models.UUIDField(primary_key=False)
    status = models.CharField(max_length=12, choices=Status.choices)
    structure = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True)
    ended_at = models.DateTimeField(null=True)
    tools = ArrayField(models.UUIDField())
