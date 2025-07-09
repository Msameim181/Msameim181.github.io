from django.db import models
from django.utils.translation import gettext_lazy as _


class Profile(models.Model):
    """
    Personal profile information.
    """
    first_name = models.CharField(_("First Name"), max_length=100)
    last_name = models.CharField(_("Last Name"), max_length=100)
    title = models.CharField(_("Professional Title"), max_length=200)
    bio = models.TextField(_("Bio"))
    avatar = models.ImageField(_("Avatar"), upload_to="profile/")
    email = models.EmailField(_("Email"))
    phone = models.CharField(_("Phone"), max_length=20, blank=True)
    location = models.CharField(_("Location"), max_length=200)
    
    # Social links
    github = models.URLField(_("GitHub"), blank=True)
    linkedin = models.URLField(_("LinkedIn"), blank=True)
    twitter = models.URLField(_("Twitter"), blank=True)
    website = models.URLField(_("Personal Website"), blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Profile")
        verbose_name_plural = _("Profiles")
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
