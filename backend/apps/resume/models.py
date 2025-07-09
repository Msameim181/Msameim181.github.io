from django.db import models
from django.utils.translation import gettext_lazy as _


class Education(models.Model):
    """
    Educational background information.
    """
    institution = models.CharField(_("Institution"), max_length=200)
    degree = models.CharField(_("Degree"), max_length=200)
    field_of_study = models.CharField(_("Field of Study"), max_length=200)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    description = models.TextField(_("Description"), blank=True)
    location = models.CharField(_("Location"), max_length=200)
    is_current = models.BooleanField(_("Current"), default=False)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Education")
        verbose_name_plural = _("Education")
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.degree} at {self.institution}"
    
    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)


class Experience(models.Model):
    """
    Work experience information.
    """
    company = models.CharField(_("Company"), max_length=200)
    position = models.CharField(_("Position"), max_length=200)
    start_date = models.DateField(_("Start Date"))
    end_date = models.DateField(_("End Date"), null=True, blank=True)
    description = models.TextField(_("Description"))
    location = models.CharField(_("Location"), max_length=200)
    is_current = models.BooleanField(_("Current"), default=False)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Experience")
        verbose_name_plural = _("Experience")
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.position} at {self.company}"
    
    def save(self, *args, **kwargs):
        if self.is_current:
            self.end_date = None
        super().save(*args, **kwargs)
