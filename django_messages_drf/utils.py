from django.db import models


class AuditModel(models.Model):

    created_at = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    modified_at = models.DateTimeField(null=False, blank=False, auto_now=True)