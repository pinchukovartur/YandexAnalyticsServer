from django.db import models
from django.utils import timezone

SCRIPT_TYPE = (
    ('SINGLE', 'SINGLE'),
    ('MULTI', 'MULTI'),
)


class Post(models.Model):
    author = models.ForeignKey('auth.User', null=False, verbose_name="Автор", )
    title = models.CharField(max_length=200, null=False, verbose_name="Заголовок", )
    type = models.CharField(max_length=10, choices=SCRIPT_TYPE, default='MULTI', null=False, verbose_name="Тип", )
    text = models.TextField(null=True, verbose_name="Описание", )
    published_date = models.DateTimeField(blank=True, null=True, verbose_name="Дата создания", )
    script = models.FileField(null=False, blank=True, upload_to="scripts/", verbose_name="Скрипт", )

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title
