from django.db import models

class Target(models.Model):
    TYPE_CHOICES = [
        ('PL',  'Planet'),
        ('NEO', 'Near-Earth Object'),
        ('RS',  'Radio Source'),
        ('DSO', 'Deep-Sky Object')
    ]
    title =     models.CharField(max_length=100)
    type =      models.CharField(max_length=100,choices=TYPE_CHOICES)
    ra =        models.DecimalField(max_digits=10, decimal_places=8)
    dec =       models.DecimalField(max_digits=10, decimal_places=8)
    img =       models.ImageField(upload_to ='uploads/', null=True, blank=True)

    def __str__(self):
        return self.title

