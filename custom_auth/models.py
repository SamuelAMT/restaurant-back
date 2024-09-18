from django.db import models
from django.contrib.auth.models import User

class BlacklistedToken(models.Model):
    token = models.CharField(max_length=500)
    blacklisted_at = models.DateTimeField(auto_now_add=True)

class LoginLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)
    ip_address = models.GenericIPAddressField()
    user_agent = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.user.username} logged in at {self.login_time} via {self.method} from {self.ip_address}"
