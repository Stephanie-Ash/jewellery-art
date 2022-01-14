""" Models for the designers app. """
from django.db import models


class Designer(models.Model):
    """
    Designer model to store information about the
    jewellery designers used by the store.
    """
    name = models.CharField(max_length=50)
    introduction = models.TextField()
    image = models.ImageField(null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.EmailField(max_length=254, null=True, blank=True)
    facebook_link = models.URLField(max_length=1024, null=True, blank=True)
    instagram_link = models.URLField(max_length=1024, null=True, blank=True)
    website_link = models.URLField(max_length=1024, null=True, blank=True)

    def __str__(self):
        return self.name


class Collection(models.Model):
    """
    Collection model for information about collections
    of a designers jewellery sold on the site.
    """
    designer = models.ForeignKey(
        Designer, on_delete=models.CASCADE, related_name='collections')
    name = models.CharField(max_length=254)
    programmatic_name = models.CharField(
        max_length=254, null=False, editable=False)

    def save(self, *args, **kwargs):
        """
        Override the original save method to set the programmatic
        name if it hasn't been set already.
        """
        if not self.programmatic_name:
            self.programmatic_name = self.name.lower().replace(" ", "_")
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
