from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menu', '0002_menuitem_menu_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='menuitem',
            name='url',
            field=models.CharField(max_length=200),
        ),
    ]
