from django.db import models

# Create your models here.
class Dumpdata(models.Model):
    archive_password = models.CharField(max_length = 50, verbose_name = "hasło do archiwum")

    def save(self, *args, **kwargs):
        self.full_clean()

    class Meta:
        managed = False
        verbose_name = "Zrzut danych z bazy"
        verbose_name_plural = "Zrzut danych z bazy"
