# Generated by Django 3.2.7 on 2023-07-06 17:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('account', '0001_initial'),
        ('route', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bus',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('bus_number', models.CharField(blank=True, max_length=255, unique=True)),
                ('pos_serial_no', models.ImageField(blank=True, max_length=255, upload_to='')),
                ('pos_dsn_number', models.CharField(blank=True, max_length=255)),
                ('gps_sim_image', models.ImageField(blank=True, max_length=255, upload_to='')),
                ('operator', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='account.operator')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='BusRoute',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('start_time', models.TimeField(default='00:00:00')),
                ('arrival_time', models.TimeField(default='00:00:00')),
                ('route', models.JSONField(blank=True, default=list)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('return_id', models.CharField(blank=True, default='', max_length=255)),
                ('bus', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='bus.bus')),
                ('from_town', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_route_from_town_FK', to='route.town')),
                ('to_town', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_route_to_town_FK', to='route.town')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='BusRouteTown',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('days', models.CharField(choices=[('Today', 'Today'), ('Alternate', 'Alternate')], default='', max_length=100)),
                ('another_trip', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=100)),
                ('bus_route', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_routes', to='bus.busroute')),
                ('route', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='route.route')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistoricalBusRouteTownStoppage',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('latitude', models.FloatField(blank=True)),
                ('longitude', models.FloatField(blank=True)),
                ('duration', models.IntegerField(blank=True)),
                ('start_time', models.TimeField(blank=True)),
                ('calculated_duration', models.IntegerField(blank=True)),
                ('calculated_start_time', models.TimeField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('eta_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bus_route_town', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bus.busroutetown')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('route_town_stoppage', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='route.routetownstoppage')),
            ],
            options={
                'verbose_name': 'historical bus route town stoppage',
                'verbose_name_plural': 'historical bus route town stoppages',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBusRouteTown',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('days', models.CharField(choices=[('Today', 'Today'), ('Alternate', 'Alternate')], default='', max_length=100)),
                ('another_trip', models.CharField(choices=[('Yes', 'Yes'), ('No', 'No')], default='', max_length=100)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bus_route', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bus.busroute')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('route', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='route.route')),
            ],
            options={
                'verbose_name': 'historical bus route town',
                'verbose_name_plural': 'historical bus route towns',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBusRoutesTowns',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('duration', models.IntegerField(blank=True)),
                ('calculated_duration', models.IntegerField(blank=True)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('day', models.IntegerField(blank=True, default=0)),
                ('town_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('town_stoppage_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('eta_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('route', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='route.route')),
            ],
            options={
                'verbose_name': 'historical bus routes towns',
                'verbose_name_plural': 'historical bus routes townss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBusRouteMissingTown',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('missing_town', models.CharField(blank=True, default='town', max_length=255)),
                ('duration', models.IntegerField(blank=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bus_route', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bus.busroute')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical bus route missing town',
                'verbose_name_plural': 'historical bus route missing towns',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBusRoute',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('start_time', models.TimeField(default='00:00:00')),
                ('arrival_time', models.TimeField(default='00:00:00')),
                ('route', models.JSONField(blank=True, default=list)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('return_id', models.CharField(blank=True, default='', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('bus', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='bus.bus')),
                ('from_town', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='route.town')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('to_town', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='route.town')),
            ],
            options={
                'verbose_name': 'historical bus route',
                'verbose_name_plural': 'historical bus routes',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalBus',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('bus_number', models.CharField(blank=True, db_index=True, max_length=255)),
                ('pos_serial_no', models.TextField(blank=True, max_length=255)),
                ('pos_dsn_number', models.CharField(blank=True, max_length=255)),
                ('gps_sim_image', models.TextField(blank=True, max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('operator', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='account.operator')),
            ],
            options={
                'verbose_name': 'historical bus',
                'verbose_name_plural': 'historical buss',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='BusRouteTownStoppage',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('latitude', models.FloatField(blank=True)),
                ('longitude', models.FloatField(blank=True)),
                ('duration', models.IntegerField(blank=True)),
                ('start_time', models.TimeField(blank=True)),
                ('calculated_duration', models.IntegerField(blank=True)),
                ('calculated_start_time', models.TimeField(blank=True)),
                ('is_active', models.BooleanField(default=True)),
                ('status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('eta_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('bus_route_town', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='bus_route_town', to='bus.busroutetown')),
                ('route_town_stoppage', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='route.routetownstoppage')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='BusRoutesTowns',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('duration', models.IntegerField(blank=True)),
                ('calculated_duration', models.IntegerField(blank=True)),
                ('towns', models.JSONField(blank=True, default=list)),
                ('day', models.IntegerField(blank=True, default=0)),
                ('town_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('town_stoppage_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('eta_status', models.CharField(choices=[('active', 'active'), ('inactive', 'inactive'), ('request_for_deletion', 'request_for_deletion'), ('deletion_ready', 'deletion_ready')], default='active', max_length=20)),
                ('route', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='route.route')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='BusRouteMissingTown',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('missing_town', models.CharField(blank=True, default='town', max_length=255)),
                ('duration', models.IntegerField(blank=True)),
                ('bus_route', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='bus.busroute')),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
    ]
