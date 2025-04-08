from django.db import models

class Character(models.Model):
    name = models.CharField(max_length=100)
    race = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=20, blank=True, null=True)
    ki = models.CharField(max_length=20, default="0")  
    max_ki = models.CharField(max_length=20, default="0")
    image = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    affiliation = models.CharField(max_length=100, blank=True, null=True)
    origin_planet = models.CharField(max_length=100, blank=True, null=True) 

    def __str__(self):
        return self.name

    def get_planet_image(self):
        """Devuelve la ruta de la imagen según el planeta de origen"""
        planet_images = {
            "vegeta": "images/vgt.png",
            "namek": "images/namekk.png",
            "tierra": "images/tierr.png",
            "limacity": "images/lima.png"
        }
        return planet_images.get(self.origin_planet, "images/space.png")
    


