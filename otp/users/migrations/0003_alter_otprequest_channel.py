# Generated by Django 4.0.3 on 2022-04-09 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_otprequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otprequest',
            name='channel',
            field=models.CharField(blank=True, choices=[('Phone', 'Phone'), ('E_Mail', 'Email')], default='Phone', max_length=12),
        ),
    ]
