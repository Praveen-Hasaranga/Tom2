# Generated by Django 3.1 on 2020-09-03 11:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Job',
            fields=[
                ('job_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='job id')),
                ('customer_name', models.CharField(max_length=250, verbose_name='customer name')),
                ('description', models.TextField(max_length=1000)),
                ('quantity', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=50)),
                ('category', models.CharField(choices=[('mechanical', 'mechanical'), ('electrical', 'electrical')], max_length=100)),
                ('stage', models.CharField(choices=[('registered', 'registered'), ('production queue', 'production queue'), ('workshop', 'workshop')], default='registered', max_length=100)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='Sales_Person',
            fields=[
                ('sales_person_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='sales person id')),
                ('name', models.CharField(max_length=250)),
                ('contact_no', models.CharField(max_length=15, verbose_name='contact number')),
                ('address', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=500)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date created')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_Workshop',
            fields=[
                ('sub_workshop_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='sub workshop id')),
                ('quantity', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=50)),
                ('status', models.CharField(choices=[('in progress', 'in progress'), ('pending', 'pending')], default='pending', max_length=100)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date created')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tomapp.job', verbose_name='job id')),
            ],
        ),
        migrations.CreateModel(
            name='Sub_WIP',
            fields=[
                ('sub_wip_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='sub WIP id')),
                ('quantity', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=50)),
                ('status', models.CharField(choices=[('complete', 'complete'), ('in progress', 'in progress'), ('pause', 'pause'), ('invoice', 'invoice')], default='in progress', max_length=100)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date created')),
                ('sub_workshop_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tomapp.sub_workshop', verbose_name='sub workshop id')),
            ],
        ),
        migrations.AddField(
            model_name='job',
            name='sales_person',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='tomapp.sales_person'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('invoice_id', models.CharField(max_length=100, primary_key=True, serialize=False, verbose_name='invoice id')),
                ('customer_name', models.CharField(max_length=250, verbose_name='customer name')),
                ('description', models.CharField(max_length=1000)),
                ('quantity', models.IntegerField()),
                ('value', models.DecimalField(decimal_places=2, max_digits=50)),
                ('stage', models.CharField(choices=[('pending invoice', 'pending invoice'), ('invoice', 'invoice')], default='pending invoice', max_length=100)),
                ('date_created', models.DateField(auto_now_add=True, verbose_name='date created')),
                ('sub_wip_id', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='tomapp.sub_wip', verbose_name='sub WIP id')),
            ],
        ),
        migrations.CreateModel(
            name='History',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(max_length=100)),
                ('remark', models.CharField(max_length=1000, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, verbose_name='date created')),
                ('job_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tomapp.job', verbose_name='job id')),
                ('sub_wip_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tomapp.sub_wip', verbose_name='sub WIP id')),
                ('sub_workshop_id', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='tomapp.sub_workshop', verbose_name='sub workshop id')),
            ],
        ),
    ]