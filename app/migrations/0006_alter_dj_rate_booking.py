# Generated by Django 4.2.5 on 2023-10-07 01:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("app", "0005_bankdetails"),
    ]

    operations = [
        migrations.AlterField(
            model_name="dj",
            name="rate",
            field=models.IntegerField(null=True),
        ),
        migrations.CreateModel(
            name="Booking",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                (
                    "stage",
                    models.CharField(
                        choices=[
                            ("requested", "Requested"),
                            ("accepted", "Accepted"),
                            ("declined", "Declined"),
                            ("quote", "Quote given"),
                            ("paid", "Paid"),
                            ("completed", "Completed"),
                            ("cancelled", "Cancelled"),
                            ("refunded", "Refunded"),
                        ],
                        max_length=200,
                    ),
                ),
                ("code", models.CharField(max_length=23)),
                ("contact_name", models.CharField(max_length=200)),
                ("phone_number", models.CharField(max_length=50)),
                ("email", models.EmailField(max_length=254)),
                ("address_line_1", models.CharField(max_length=200)),
                ("address_line_2", models.CharField(max_length=200)),
                ("city", models.CharField(max_length=200)),
                ("state", models.CharField(max_length=200)),
                ("post_code", models.CharField(max_length=20)),
                ("country", models.CharField(max_length=200)),
                ("set_time", models.DateTimeField()),
                ("hours", models.IntegerField()),
                ("equipment_information", models.TextField()),
                ("other_information", models.TextField()),
                ("extra_budget", models.IntegerField(null=True)),
                ("rate", models.IntegerField(null=True)),
                ("quote", models.IntegerField(null=True)),
                ("dj", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to="app.dj")),
            ],
        ),
    ]
