from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='menuitem',
            name='menu_name',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
