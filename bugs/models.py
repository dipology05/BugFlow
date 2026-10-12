
from django.db import models


class BugReport(models.Model):

    CATEGORY_CHOICES = [
        ("UI", "UI"),
        ("Database", "Database"),
        ("Security", "Security"),
        ("API", "API"),
    ]

    SEVERITY_CHOICES = [
        ("Low", "Low"),
        ("Medium", "Medium"),
        ("High", "High"),
        ("Critical", "Critical"),
    ]

    STATUS_CHOICES = [
        ("Open", "Open"),
        ("In Progress", "In Progress"),
        ("Resolved", "Resolved"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    stack_trace = models.TextField(blank=True)

    component_label = models.CharField(
        max_length=50,
        choices=CATEGORY_CHOICES,
        blank=True,
    )

    severity_label = models.CharField(
        max_length=20,
        choices=SEVERITY_CHOICES,
        blank=True,
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="Open",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


