from django.db import models
# from django.utils.translation import ugettext_lazy as _ 

class Url(models.Model):
    long_url = models.URLField()
    short_url = models.URLField()
    access_count = models.PositiveIntegerField(default=0)

    def __str__(self):
        return '%s %s' % (self.long_url, self.short_url)
