# Generated by Django 2.0 on 2017-12-21 07:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Term',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('category', models.CharField(choices=[('Analytics', 'Analytics'), ('Development', 'Development'), ('Finance', 'Finance'), ('General', 'General'), ('Marketing', 'Marketing'), ('Product', 'Product'), ('Supply', 'Supply')], max_length=255)),
                ('description', models.TextField()),
            ],
        ),
    ]
