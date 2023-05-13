# Generated by Django 4.1.7 on 2023-05-06 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='sub_category',
            field=models.TextField(default='--'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='customer',
            name='state',
            field=models.CharField(choices=[('São Paulo', 'São Paulo'), ('Rio de Janeiro', 'Rio de Janeiro'), ('Minas Gerais', 'Minas Gerais')], max_length=50),
        ),
        migrations.AlterField(
            model_name='product',
            name='category',
            field=models.CharField(choices=[('PC', 'Proteção Cabeça'), ('PA', 'Proteção Auditiva'), ('PR', 'Proteção Respiratória'), ('PM', 'Proteção Mãos'), ('PP', 'Proteção Pés')], max_length=2),
        ),
    ]
