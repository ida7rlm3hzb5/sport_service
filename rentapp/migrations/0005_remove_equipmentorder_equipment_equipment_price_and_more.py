# Generated by Django 5.0.6 on 2024-06-02 11:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rentapp', '0004_alter_equipmentorder_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='equipmentorder',
            name='equipment',
        ),
        migrations.AddField(
            model_name='equipment',
            name='price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='equipmentorder',
            name='total_price',
            field=models.FloatField(default=1),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='equipmentorder',
            name='status',
            field=models.CharField(choices=[('CREATED', 'Создан'), ('RENTED', 'Арендован'), ('RETURNED', 'Возвращено')], default='CREATED', max_length=10),
        ),
        migrations.CreateModel(
            name='OrderedEquipment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.IntegerField(default=1)),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='rentapp.equipment')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ordered_equipment', to='rentapp.equipmentorder')),
            ],
        ),
    ]
