# Generated by Django 2.2.16 on 2020-11-02 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0006_profile_can_order_physical'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='expire_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='profile',
            name='can_order_physical',
            field=models.BooleanField(default=False),
        ),
    ]
