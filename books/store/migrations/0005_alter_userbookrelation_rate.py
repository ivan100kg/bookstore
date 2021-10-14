# Generated by Django 3.2.8 on 2021-10-14 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_auto_20211014_0934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userbookrelation',
            name='rate',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Horrible'), (2, 'Bad'), (3, 'Normal'), (4, 'Good'), (5, 'Amazing')], null=True),
        ),
    ]