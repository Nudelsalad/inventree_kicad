"""Models for Kicad Library Plugin."""

from django.db import models
from django.utils.translation import gettext_lazy as _

from part.models import PartCategory, PartParameterTemplate


class SelectedCategory(models.Model):
    """Categories which are used in Kicad."""

    class Meta:
        app_label = 'inventree_kicad'
        verbose_name = 'KiCad Category'
        verbose_name_plural = 'KiCad Categories'

    category = models.OneToOneField(
        PartCategory,
        on_delete=models.CASCADE,
        related_name='get_enabled_kicad_categories',
        verbose_name=_('Category')
    )

    default_symbol = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Default Symbol'),
        help_text=_('Default symbol for this category, if not specified for an individual part'),
    )

    default_footprint = models.CharField(
        max_length=200,
        blank=True,
        verbose_name=_('Default Footprint'),
        help_text=_('Default footprint for this category, if not specified for an individual part'),
    )

    default_reference = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Default Reference'),
        help_text=_('Default reference for this category, if not specified for an individual part'),
    )

    default_value_parameter_template = models.ForeignKey(
        PartParameterTemplate,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name=_('Default Value Parameter Template'),
        help_text=_('Default value parameter template for this category, if not specified for an individual part'),
    )

    footprint_parameter_template = models.ForeignKey(
        PartParameterTemplate,
        on_delete=models.SET_NULL,
        related_name="footprint_kicad_categories",
        blank=True,
        null=True,
        verbose_name=_('Footprint Parameter Template'),
        help_text=_('Footprint parameter template for this category, will use KICAD_FOOTPRINT_PARAMETER setting if not set'),
    )

    footprint_parameter_mapping = models.JSONField(
        blank=True,
        null=True,
        verbose_name=_('Footprint Parameter Mapping'),
        help_text=_('Mapping from footprint parameter values to actual KiCad footprint names')
    )

    def __str__(self):
        """Default name string which is returned when object is called"""
        return f'{self.category.pathstring}'
