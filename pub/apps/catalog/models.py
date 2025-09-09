from django.db import models


class Offering(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )

    per = models.CharField(
        max_length=50,
        help_text="e.g., per hour, per project",
        choices=[("hour", "per hour"), ("project", "per project")],
        null=True,
        blank=True,
    )

    marketing_description = models.TextField(
        help_text="A brief description for marketing purposes.",
        null=True,
        blank=True,
    )

    marketing_title = models.CharField(
        max_length=255,
        help_text="A catchy title for marketing purposes.",
        null=True,
        blank=True,
    )

    call_to_action = models.CharField(
        max_length=255,
        help_text="A call to action phrase.",
        null=True,
        blank=True,
    )

    def __str__(self):
        return self.name
