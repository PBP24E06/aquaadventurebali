# Generated by Django 5.1.2 on 2024-10-27 12:09

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_forum_commenter_name_forum_parent'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='report',
            unique_together={('product', 'user')},
        ),
    ]
