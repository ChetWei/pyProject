# Generated by Django 2.1 on 2018-08-19 01:32

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('teacher', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('school_number', models.CharField(max_length=16, verbose_name='学号')),
                ('gender', models.CharField(blank=True, choices=[('male', '男'), ('female', '女')], max_length=8, null=True, verbose_name='性别')),
                ('grade', models.CharField(blank=True, choices=[('Freshman', '大一'), ('Sophomore', '大二'), ('Junior', '大三'), ('Senior', '大四'), ('Graduate', '毕业生')], max_length=16, null=True, verbose_name='年级')),
                ('last_login_ip', models.GenericIPAddressField(blank=True, null=True, verbose_name='最后登录ip')),
                ('connect_times', models.IntegerField(blank=True, null=True, verbose_name='连接次数')),
                ('authorization_times', models.IntegerField(blank=True, null=True, verbose_name='授权次数')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Authorized',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expiration_time', models.DateTimeField(verbose_name='授权过期时间')),
                ('privilege', models.BooleanField(default=False, verbose_name='是否特权')),
                ('is_authorized', models.BooleanField(default=False, verbose_name='是否授权')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='teacher.Teacher', verbose_name='教师外键')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户外键')),
            ],
        ),
        migrations.CreateModel(
            name='UserOperation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('connect_time', models.DateTimeField(verbose_name='连接时间')),
                ('discut_time', models.DateTimeField(verbose_name='断开时间')),
                ('connect_ip', models.GenericIPAddressField(verbose_name='连接ip')),
                ('discut_ip', models.GenericIPAddressField(verbose_name='断开ip')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户外键')),
            ],
        ),
    ]
