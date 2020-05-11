# Generated by Django 2.0.6 on 2019-01-13 23:25
from django.contrib.contenttypes.models import ContentType
from django.db import migrations

from outputs.mixins import FilterExporterMixin
from outputs.models import Export
from swida.migration_helpers import RunPython


def set_export_fields(*args, **kwargs):
    exporters = FilterExporterMixin.__subclasses__()

    # necessary to match formats of Export model with exporters names
    formats = {format[0].replace('_', ''): format[0] for format in Export.FORMATS}

    for exporter in exporters:
        model = exporter.queryset.model
        format = exporter.__name__.replace(model._meta.object_name, '').replace('Exporter', '').upper()

        # remove context from format
        for context in dict(Export.CONTEXTS).keys():
            format = format.replace(context, '')

        # if exporter name format doesn't match Export model's formats try remove underscores from second one
        if format not in formats.values():
            if format in formats.keys():
                format = formats[format]
            else:
                raise ValueError(f'Format {format} not valid')

        content_type = ContentType.objects.get_for_model(model, for_concrete_model=False)

        try:
            selectable_fields = exporter.selectable_fields()
        except AttributeError:
            selectable_fields = None

        try:
            for set in exporter.selectable_iterative_sets().values():
                selectable_fields.update(set)
        except AttributeError:
            pass

        if selectable_fields:
            fields = []
            for field_group in selectable_fields.values():
                fields.extend([field[0] for field in field_group])

            exports = Export.objects.filter(content_type=content_type, format=format).defer('context')

            print(f'Updating export fields of {exports.count()} {content_type} {format} exports')

            exports.update(fields=fields)


class Migration(migrations.Migration):

    dependencies = [
        ('outputs', '0005_export_fields'),
    ]

    operations = [
        RunPython(set_export_fields)
    ]