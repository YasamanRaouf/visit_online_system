# Generated by Django 5.1.1 on 2024-09-12 18:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('doctor', '0002_rename_speciality_doctor_specialty_and_more'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Speciality',
            new_name='Specialty',
        ),
    ]
