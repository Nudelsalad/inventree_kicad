from rest_framework import serializers
from rest_framework.reverse import reverse_lazy

from part.models import Part, PartCategory, PartParameter, PartParameterTemplate


class KicadDetailedPartSerializer(serializers.ModelSerializer):
    """Custom model serializer for a single KiCad part instance"""

    def get_api_url(self):
        """Return the API url associated with this serializer"""
        return reverse_lazy('api-kicad-part-list')

    def __init__(self, *args, **kwargs):
        """Custom initialization for this seriailzer.
        
        As we need to have access to the parent plugin instance,
        we pass it in via the kwargs.
        """

        self.plugin = kwargs.pop('plugin')
        super().__init__(*args, **kwargs)

    class Meta:
        """Metaclass defining serializer fields"""
        model = Part

        fields = [
            'id',
            'name',
            'symbolIdStr',
            'fields',
        ]

    # Custom field definitions
    symbolIdStr = serializers.SerializerMethodField('get_symbolIdStr')
    fields = serializers.SerializerMethodField('get_kicad_fields')

    id = serializers.CharField(source='pk', read_only=True)

    def get_kicad_category(self, part):
        """For the provided part instance, find the associated SelectedCategory instance.
        
        If there are multiple possible associations, return the "deepest" one.
        """

        from .models import SelectedCategory

        # If the selcted part does not have a category, return None
        if not part.category:
            return None

        # Get the category tree for the selected part
        categories = part.category.get_ancestors(include_self=True)

        return SelectedCategory.objects.filter(category__in=categories).order_by('-category__level').first()


    def get_symbol(self, part):
        """Return the symbol associated with this part.
        
        - First, check if the part has a symbol assigned (via parameter)
        - Otherwise, fallback to the default symbol for the KiCad Category
        """

        print("get_symbol for:", part)

        kicad_category = self.get_kicad_category(part)

        print("kicad_category:", kicad_category)

        symbol = ""

        try:
            part_type = part.full_name.split('_')[0]

            if part_type == 'R':
                symbol = "Device:R"

            elif part_type == 'C':
                symbol = "Device:C"

        except:
            pass

        return symbol

    def get_footprint(self, part):
        """Return the footprint associated with this part.
        
        - First, check if the part has a footprint assigned (via parameter)
        - Otherwise, fallback to the default footprint for the KiCad Category
        """

        footprint = ""
        try:
            part_type = part.full_name.split('_')[0]

            if part_type == 'R':
                if part.full_name.split('_')[2] == '0402':
                    footprint = 'Resistor_SMD:R_0402_1005Metric'

                if part.full_name.split('_')[2] == '0603':
                    footprint = "Resistor_SMD:R_0603_1608Metric"

                if part.full_name.split('_')[2] == '0805':
                    footprint = 'Resistor_SMD:R_0805_2012Metric'

            elif part_type == 'C':
                footprint = "Capacitor_SMD:C_0805_2012Metric"

                if part.full_name.split('_')[2] == '0402':
                    footprint = 'Capacitor_SMD:C_0402_1005Metric'

                if part.full_name.split('_')[2] == '0603':
                    footprint = "Capacitor_SMD:C_0603_1608Metric"

                if part.full_name.split('_')[2] == '0805':
                    footprint = 'Capacitor_SMD:C_0805_2012Metric'

        except:
            pass

        return footprint

    def get_datasheet(self, part):
        for p in part.get_parameters():
            if p.name.lower() == 'datasheet':
                return f'{p.data}'
        return ""

    def get_reference(self, part):
        reference = "X"
        try:
            reference = part.full_name.split('_')[0]
            if len(part.full_name.split('_')) <= 1:
                reference = "X"
        except:
            pass

        return reference

    def get_value(self, part):
        value = part.full_name
        try:
            value = f'{part.full_name.split("_")[1]}'
        except:
            pass

        return value

    def get_symbolIdStr(self, part):
        return self.get_symbol(part)

    def get_kicad_fields(self, part):
        """Return a set of fields to be used in the KiCad symbol library"""

        # Default KiCad Fields
        kicad_default_fields = {
            'value': {
                "value": self.get_value(part),
            },
            'footprint': {
                "value": self.get_footprint(part),
                "visible": 'False'
            },
            'datasheet': {
                "value": "www.kicad.org",
                "visible": 'False'
            },
            'reference': {
                "value": "R",
            },
            'description': {
                "value": part.description,
                "visible": 'False'
            },
            'keywords': {
                "value": part.keywords,
                "visible": 'False'
            },
        }

        # Extra fields (to be implemented)
        kicad_custom_fields = {
            'custom1': {
                "value": "MyText1",
                "visible": 'False'
            },
            'custom2': {
                "value": "MyText2",
                "visible": 'False'
            },
            'custom3': {
                "value": "MyText3",
                "visible": 'False'
            },
            'InvenTree': {
                "value": f'{part.id}',
                "visible": 'False'
            },
            'Rating': {
                "value": "",
                "visible": 'False'
            },
        }

        return kicad_default_fields | kicad_custom_fields


class KicadPreviewPartSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = Part

        # fields = [f.name for f in Part._meta.fields]

        fields = [
            'id',
            'name',
        ]

    id = serializers.SerializerMethodField('get_id')
    name = serializers.SerializerMethodField('get_name')

    def get_api_url(self):
        """Return the API url associated with this serializer"""
        return reverse_lazy('api-kicad-part-list')

    def get_name(self, part):
        return part.full_name

    def get_id(self, part):
        return f'{part.pk}'


class KicadCategorySerializer(serializers.ModelSerializer):
    """Custom model serializer for a single KiCad category instance"""

    class Meta:
        """Metaclass defining serializer fields"""
        model = PartCategory
        fields = [
            'id',
            'name',
            'description',
            'pathstring',
        ]

    id = serializers.CharField(source='pk', read_only=True)


class KicadPartParameterTemplateSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = PartParameterTemplate
        fields = [
            'name',
        ]


class KicadFieldsSerializer(serializers.ModelSerializer):
    class Meta:
        """Metaclass defining serializer fields"""
        model = PartParameterTemplate
        fields = [
            'name',
        ]
