from django.db import models

class Record(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, default="Default Title")
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return(f"{self.title}")
