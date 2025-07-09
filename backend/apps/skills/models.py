from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator


class SkillCategory(models.Model):
    """
    Skill category for grouping skills.
    """
    name = models.CharField(_("Name"), max_length=100)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Skill Category")
        verbose_name_plural = _("Skill Categories")
        ordering = ['order']
    
    def __str__(self):
        return self.name


class Skill(models.Model):
    """
    Technical skill with proficiency level.
    """
    name = models.CharField(_("Name"), max_length=100)
    category = models.ForeignKey(
        SkillCategory, 
        on_delete=models.CASCADE,
        related_name="skills"
    )
    proficiency = models.PositiveSmallIntegerField(
        _("Proficiency"),
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    icon = models.FileField(_("Icon"), upload_to="skills/", blank=True)
    order = models.PositiveIntegerField(_("Order"), default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = _("Skill")
        verbose_name_plural = _("Skills")
        ordering = ['category', 'order']
    
    def __str__(self):
        return self.name
