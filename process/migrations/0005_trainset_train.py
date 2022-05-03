# Generated by Django 4.0.4 on 2022-05-03 17:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('process', '0004_trainset'),
    ]

    operations = [
        migrations.AddField(
            model_name='trainset',
            name='train',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='process_train_set_for_train', to='process.train', verbose_name='归属火车'),
        ),
    ]
