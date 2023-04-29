from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Sheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    sheet_id = models.CharField(max_length=100)
    sheet_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sheet_name} - {self.user.username}"
    
    def serialize(self):
        return {
            "sheet_id": self.sheet_id,
            "sheet_name": self.sheet_name,
            "created_at": self.created_at,
            "user": self.user.username
        }

