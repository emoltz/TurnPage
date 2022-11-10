# Generated by Django 4.1.2 on 2022-11-10 16:30

from django.db import migrations, models
import multiselectfield.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ("bookSwiping", "0020_genre_userdemographics_genre"),
    ]

    operations = [
        migrations.AlterField(
            model_name="userdemographics",
            name="ethnicity",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("AIFN", "American Indian/First Nations"),
                    ("BLAD", "Black/African Descent"),
                    ("EA", "East Asian"),
                    ("HL", "Hispanic/Latino"),
                    ("ME", "Middle Eastern"),
                    ("PI", "Pacific Islander"),
                    ("SA", "South Asian"),
                    ("SEA", "Southeast Asian"),
                    ("WC", "White/Caucasian"),
                    ("O", "Other"),
                ],
                max_length=1024,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userdemographics",
            name="gender",
            field=models.CharField(
                choices=[("M", "Male"), ("F", "Female"), ("NB", "Non-Binary")],
                max_length=24,
                null=True,
            ),
        ),
        migrations.AlterField(
            model_name="userdemographics",
            name="lgbtq",
            field=models.BooleanField(default=False, null=True),
        ),
        migrations.AlterField(
            model_name="userdemographics",
            name="religion",
            field=multiselectfield.db.fields.MultiSelectField(
                choices=[
                    ("AG", "Agnostic"),
                    ("A", "Atheist/None"),
                    ("B", "Buddhist"),
                    ("CA", "Catholic"),
                    ("C", "Christian"),
                    ("H", "Hindu"),
                    ("J", "Jewish"),
                    ("M", "Muslim"),
                    ("SK", "Sikh"),
                    ("SP", "Spiritual"),
                    ("O", "Other"),
                ],
                max_length=1024,
                null=True,
            ),
        ),
    ]