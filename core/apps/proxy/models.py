from django.contrib.auth import get_user_model
from django.db import models
from django.utils.text import slugify

UserModel = get_user_model()


class UserSite(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    title = models.CharField(
        verbose_name='Site title',
        max_length=200
    )
    slug = models.SlugField(max_length=255)
    url = models.URLField()

    class Meta:
        unique_together = [['user', 'title']]

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs) -> None:
        # TODO separate logic
        self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


class SiteVisit(models.Model):
    user_site = models.ForeignKey(UserSite, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    page_url = models.CharField(max_length=255)
    request_size = models.BigIntegerField(default=0)  # Розмір запиту в байтах
    response_size = models.BigIntegerField(default=0)  # Розмір відповіді в байтах

    def __str__(self):
        return f"{self.user_site.title} - {self.page_url} - {self.timestamp}"
