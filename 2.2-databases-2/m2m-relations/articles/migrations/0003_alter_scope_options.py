# Generated by Django 4.1.4 on 2022-12-08 20:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0002_scope_alter_article_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='scope',
            options={'ordering': ['-is_main', 'tag'], 'verbose_name': 'Тег статьи', 'verbose_name_plural': 'Теги статей'},
        ),
    ]
