from django.db import models

class Target(models.Model):
    class Meta:
        abstract = True
 
    """
    a = semimajor axis
    e = ecenttricity
    i = inclination
    w = arg perih
    omega = ecliptic longitude
    M = mean anomaly
    Initial Date (datetime type)

    TargetName (CharField)
    CentreBody (CharField)
    Type (TYPE_CHOICE - custom imported)

    (optional)
    mass
    radius
    solar day
    
    """

    TYPE_CHOICES = [
        ('PL',  'Planet'),
        ('NEO', 'Near-Earth Object'),
        ('RS',  'Radio Source'),
        ('DSO', 'Deep-Sky Object')
    ]

    title =        models.CharField(max_length=100)
    type =         models.CharField(max_length=100,choices=TYPE_CHOICES)
    img =          models.ImageField(upload_to ='uploads/', null=True, blank=True)

    def __str__(self):
        return self.title


class SolarTarget(Target):
    semimajor_axis  =    models.DecimalField(max_digits=10, decimal_places=5)
    eccentricity    =    models.DecimalField(max_digits=10, decimal_places=5)
    inclination     =    models.DecimalField(max_digits=10, decimal_places=5)
    perihelion      =    models.DecimalField(max_digits=10, decimal_places=5)
    longitude       =    models.DecimalField(max_digits=10, decimal_places=5)
    mean_anomaly    =    models.DecimalField(max_digits=10, decimal_places=5)
    init_date       =    models.DateTimeField()
    
class DeepSpaceTarget(Target):
    right_ascension     =    models.DecimalField(max_digits=10, decimal_places=5)
    declination         =    models.DecimalField(max_digits=10, decimal_places=5)
    magnitude           =    models.DecimalField(max_digits=10, decimal_places=5)
    bayer               =    models.CharField(max_length=100)


