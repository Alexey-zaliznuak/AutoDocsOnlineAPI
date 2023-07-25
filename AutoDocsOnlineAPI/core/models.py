from django.db import models


class CreatedModel(models.Model):
    """Abstarct model. Add 'created' field."""

    creation_date = models.DateTimeField(
        "Date of creation",
        auto_now_add=True,
    )

    class Meta:
        abstract = True
