from django.db import models


class BusinessInquiry(models.Model):
    SERVICE_CHOICES = [
        ("software", "Custom Software"),
        ("cloud", "Cloud & Infrastructure"),
        ("security", "Cybersecurity"),
        ("automation", "Automation"),
        ("other", "Other / Not Sure"),
    ]

    STATUS_CHOICES = [
        ("new", "New"),
        ("reviewing", "Reviewing"),
        ("contacted", "Contacted"),
        ("closed", "Closed"),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    company = models.CharField(max_length=160, blank=True)
    service = models.CharField(
        max_length=30,
        choices=SERVICE_CHOICES,
    )
    message = models.TextField(max_length=5000)

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="new",
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name} — {self.get_service_display()}"
