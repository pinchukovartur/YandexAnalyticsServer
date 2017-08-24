from django.db import models
from django.utils import timezone

SCRIPT_TYPE = (
    ('SINGLE', 'SINGLE'),
    ('MULTI', 'MULTI'),
)


class Post(models.Model):
    author = models.ForeignKey('auth.User', null=False, verbose_name="Author", )
    title = models.CharField(max_length=200, null=False, verbose_name="Title", )
    type = models.CharField(max_length=10, choices=SCRIPT_TYPE, default='MULTI', null=False, verbose_name="Type", )
    text = models.TextField(null=True, verbose_name="Description", )
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Published date", )
    script = models.FileField(null=False, blank=True, upload_to="scripts/", verbose_name="File script", )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
