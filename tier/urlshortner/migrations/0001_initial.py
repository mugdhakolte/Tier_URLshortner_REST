# Generated by Django 4.0.5 on 2022-06-08 17:45

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TierURL',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('main_url', models.URLField()),
                ('short_url', models.URLField(max_length=100, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='URLVisit',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('visits', models.IntegerField()),
                ('tier_url', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='urlvisits', to='urlshortner.tierurl')),
            ],
        ),
    ]
