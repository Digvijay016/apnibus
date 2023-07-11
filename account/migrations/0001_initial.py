# Generated by Django 3.2.7 on 2023-07-11 05:25

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import simple_history.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('user_type', models.CharField(choices=[('admin', 'admin'), ('conductor', 'conductor'), ('commuter', 'commuter'), ('internal_user', 'internal_user'), ('operator', 'operator'), ('bus_driver', 'bus_driver'), ('pos_device', 'pos_device'), ('conductor_se', 'conductor_se'), ('operator_sales_lead', 'operator_sales_lead'), ('Sales', 'Sales')], max_length=25)),
                ('preferred_language', models.CharField(choices=[('english', 'english'), ('hindi', 'hindi')], default='english', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='user_groups', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for the user.', related_name='user_permissions_user', to='auth.Permission', verbose_name='user permissions')),
            ],
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='MasterOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=10)),
                ('otp_type', models.CharField(choices=[('commuter', 'commuter'), ('conductor', 'conductor'), ('operator', 'operator'), ('conductor_se', 'conductor_se')], default='commuter', max_length=20)),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='UserAuthenticationOTP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=6)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('mobile', models.CharField(max_length=10)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='SalesTeamUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('type', models.CharField(choices=[('sales', 'sales'), ('marketing', 'marketing')], default='sales', max_length=255)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to.', related_name='sales_team_users', related_query_name='sales_team_user', to='auth.Group', verbose_name='groups')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sales_team_user_FK', to=settings.AUTH_USER_MODEL)),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='sales_team_users', related_query_name='sales_team_user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Operator',
            fields=[
                ('created_on', models.DateTimeField(auto_now_add=True, db_column='created_on')),
                ('updated_on', models.DateTimeField(auto_now=True, db_column='updated_on')),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(default=uuid.uuid1, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('town', models.CharField(blank=True, default='', max_length=255)),
                ('gstin', models.CharField(blank=True, max_length=20)),
                ('pan_number', models.CharField(blank=True, max_length=20)),
                ('pan_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('aadhar_number', models.CharField(blank=True, max_length=20)),
                ('aadhar_front_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('aadhar_back_photo', models.ImageField(blank=True, max_length=255, null=True, upload_to='')),
                ('setup_fee', models.IntegerField(blank=True)),
                ('monthly_subscription_fee', models.IntegerField(blank=True)),
                ('rejection_reason', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('p', 'Verification Pending'), ('v', 'Verified'), ('r', 'Rejected')], default='p', max_length=225)),
                ('pos_given_as', models.CharField(blank=True, choices=[('d', 'Demo'), ('s', 'Sold')], max_length=20)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='operator_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'get_latest_by': 'updated_on',
                'abstract': False,
                'default_permissions': (),
            },
        ),
        migrations.CreateModel(
            name='HistoricalUserAuthenticationOTP',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=6)),
                ('is_verified', models.BooleanField(default=False)),
                ('is_valid', models.BooleanField(default=True)),
                ('mobile', models.CharField(max_length=10)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user authentication otp',
                'verbose_name_plural': 'historical user authentication otps',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('user_type', models.CharField(choices=[('admin', 'admin'), ('conductor', 'conductor'), ('commuter', 'commuter'), ('internal_user', 'internal_user'), ('operator', 'operator'), ('bus_driver', 'bus_driver'), ('pos_device', 'pos_device'), ('conductor_se', 'conductor_se'), ('operator_sales_lead', 'operator_sales_lead'), ('Sales', 'Sales')], max_length=25)),
                ('preferred_language', models.CharField(choices=[('english', 'english'), ('hindi', 'hindi')], default='english', max_length=255)),
                ('is_active', models.BooleanField(default=True)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user',
                'verbose_name_plural': 'historical users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalSalesTeamUser',
            fields=[
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(db_index=True, error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('name', models.CharField(blank=True, max_length=50)),
                ('mobile', models.CharField(max_length=10)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('type', models.CharField(choices=[('sales', 'sales'), ('marketing', 'marketing')], default='sales', max_length=255)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical user',
                'verbose_name_plural': 'historical users',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalOperator',
            fields=[
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('id', models.UUIDField(db_index=True, default=uuid.uuid1, editable=False)),
                ('name', models.CharField(blank=True, max_length=255)),
                ('company_name', models.CharField(blank=True, max_length=255)),
                ('mobile', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=255)),
                ('town', models.CharField(blank=True, default='', max_length=255)),
                ('gstin', models.CharField(blank=True, max_length=20)),
                ('pan_number', models.CharField(blank=True, max_length=20)),
                ('pan_photo', models.TextField(blank=True, max_length=255, null=True)),
                ('aadhar_number', models.CharField(blank=True, max_length=20)),
                ('aadhar_front_photo', models.TextField(blank=True, max_length=255, null=True)),
                ('aadhar_back_photo', models.TextField(blank=True, max_length=255, null=True)),
                ('setup_fee', models.IntegerField(blank=True)),
                ('monthly_subscription_fee', models.IntegerField(blank=True)),
                ('rejection_reason', models.CharField(blank=True, max_length=255)),
                ('status', models.CharField(choices=[('p', 'Verification Pending'), ('v', 'Verified'), ('r', 'Rejected')], default='p', max_length=225)),
                ('pos_given_as', models.CharField(blank=True, choices=[('d', 'Demo'), ('s', 'Sold')], max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('user', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical operator',
                'verbose_name_plural': 'historical operators',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalMasterOTP',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_on', models.DateTimeField(blank=True, db_column='created_on', editable=False)),
                ('updated_on', models.DateTimeField(blank=True, db_column='updated_on', editable=False)),
                ('is_deleted', models.BooleanField(default=False)),
                ('otp', models.CharField(max_length=10)),
                ('otp_type', models.CharField(choices=[('commuter', 'commuter'), ('conductor', 'conductor'), ('operator', 'operator'), ('conductor_se', 'conductor_se')], default='commuter', max_length=20)),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical master otp',
                'verbose_name_plural': 'historical master otps',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
