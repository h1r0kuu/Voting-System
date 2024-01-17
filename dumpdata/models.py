from django.db import models

# Create your models here.
class Dumpdata(models.Model):
    archive_password = models.CharField(max_length = 50)

    def save(self, *args, **kwargs):
        self.full_clean()

    class Meta:
        managed = False
