# Generated by Django 3.1.3 on 2020-11-15 18:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(editable=False, primary_key=True, serialize=False)),
                ('date', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('REGULAR', 'regular'), ('BUDGET', 'budget'), ('PREMIUM', 'premium'), ('VIP', 'vip')], max_length=16)),
                ('price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('sold_status', models.BooleanField(default=False)),
                ('reserved', models.BooleanField(default=False)),
                ('payment_status', models.CharField(choices=[('NONE', 'none'), ('STARTED', 'started'), ('PAYED', 'payed'), ('ERROR', 'error')], default='none', max_length=16)),
                ('reserved_until', models.DateTimeField()),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='API.event')),
            ],
        ),
    ]