# Generated by Django 2.0.9 on 2018-12-26 08:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CustomField',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('field_name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=50, verbose_name='Description')),
                ('field_key', models.CharField(max_length=50)),
                ('field_type', models.CharField(choices=[('5', '字符串'), ('10', '单选框'), ('15', '多选框'), ('20', '日期'), ('25', '日期时间'), ('30', '文本域')], default='5', max_length=5)),
            ],
            options={
                'verbose_name': '工作流自定义字段',
                'verbose_name_plural': '工作流自定义字段',
            },
        ),
        migrations.CreateModel(
            name='State',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='State Name')),
                ('description', models.CharField(max_length=50, verbose_name='Description')),
                ('order_id', models.CharField(max_length=10, verbose_name='State Order')),
                ('state_type', models.CharField(choices=[('1', 'normal'), ('2', 'start'), ('3', 'end')], default='1', max_length=5, verbose_name='State Type')),
                ('participant_type', models.CharField(choices=[('1', 'person'), ('2', 'department')], default='1', max_length=5, verbose_name='Participant Type')),
                ('participant', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='state_user', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '工作流状态',
                'verbose_name_plural': '工作流状态',
            },
        ),
        migrations.CreateModel(
            name='Transition',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='Transition Name')),
                ('description', models.CharField(max_length=50, verbose_name='Description')),
                ('transition_type', models.CharField(choices=[('1', '同意'), ('2', '拒绝'), ('3', '其他')], default='1', max_length=5)),
                ('from_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions_from', to='workflow.State')),
                ('to_state', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions_to', to='workflow.State')),
            ],
            options={
                'verbose_name': '工作流流转',
                'verbose_name_plural': '工作流流转',
            },
        ),
        migrations.CreateModel(
            name='Workflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deleted', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Created At')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Updated At')),
                ('deleted_at', models.DateTimeField(blank=True, null=True)),
                ('name', models.CharField(max_length=50, verbose_name='Workflow Name')),
                ('description', models.CharField(max_length=50, verbose_name='Description')),
                ('flowchart', models.FileField(blank=True, help_text='工作流的流程图', upload_to='flowchart', verbose_name='Flowchart')),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': '工作流',
                'verbose_name_plural': '工作流',
            },
        ),
        migrations.AddField(
            model_name='transition',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transitions', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='state',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='state_workflow', to='workflow.Workflow'),
        ),
        migrations.AddField(
            model_name='customfield',
            name='workflow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='custom_field', to='workflow.Workflow'),
        ),
    ]
