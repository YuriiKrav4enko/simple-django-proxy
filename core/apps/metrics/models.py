from django.contrib.auth import get_user_model

UserModel = get_user_model()


class UserMetrics(UserModel):

    class Meta:
        proxy = True
        verbose_name_plural = "User Metrics"
