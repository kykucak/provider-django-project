# Generated by Django 3.2 on 2021-05-22 16:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mainapp', '0004_auto_20210522_1818'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='plans',
        ),
        migrations.AlterField(
            model_name='orderedplan',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer'),
        ),
        migrations.CreateModel(
            name='OrderedPlansList',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('final_price', models.DecimalField(decimal_places=2, default=0, max_digits=5)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mainapp.customer')),
                ('plans', models.ManyToManyField(blank=True, related_name='related_plans', to='mainapp.OrderedPlan')),
            ],
        ),
        migrations.AddField(
            model_name='orderedplan',
            name='related_list',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='related_plans_list', to='mainapp.orderedplanslist'),
            preserve_default=False,
        ),
    ]
