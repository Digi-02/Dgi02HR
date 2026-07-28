from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0024_onboardingstage_onboardingparticipant_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='BirthdayMessageLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthday_year', models.PositiveIntegerField()),
                ('recipient_email', models.EmailField(max_length=254)),
                ('sent_at', models.DateTimeField(auto_now_add=True)),
                ('employee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='birthday_message_logs', to='attendance.employee')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='birthday_message_logs', to='attendance.organization')),
            ],
            options={
                'ordering': ['-sent_at'],
                'unique_together': {('organization', 'employee', 'birthday_year')},
            },
        ),
        migrations.AddIndex(
            model_name='birthdaymessagelog',
            index=models.Index(fields=['organization', 'birthday_year'], name='attendance__organiz_169dfd_idx'),
        ),
        migrations.AddIndex(
            model_name='birthdaymessagelog',
            index=models.Index(fields=['employee', 'birthday_year'], name='attendance__employe_1ea066_idx'),
        ),
    ]
