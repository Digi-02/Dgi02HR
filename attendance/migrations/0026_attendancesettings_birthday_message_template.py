from django.db import migrations, models


DEFAULT_BIRTHDAY_BODY = (
    'Dear {display_name},\n\n'
    'Happy birthday from all of us at {organization_name}.\n\n'
    'Today, we celebrate you and the value you bring to the team. We hope your day is filled with joy, '
    'good health, and the kind of moments that remind you how appreciated you are.\n\n'
    'Thank you for being part of {organization_name}. We wish you a wonderful birthday and a year ahead '
    'filled with growth, fulfilment, and success.\n\n'
    'Warm regards,\n'
    'HR Team\n'
    '{organization_name}'
)


class Migration(migrations.Migration):

    dependencies = [
        ('attendance', '0025_birthdaymessagelog'),
    ]

    operations = [
        migrations.AddField(
            model_name='attendancesettings',
            name='birthday_message_body',
            field=models.TextField(default=DEFAULT_BIRTHDAY_BODY),
        ),
        migrations.AddField(
            model_name='attendancesettings',
            name='birthday_message_subject',
            field=models.CharField(default='Happy Birthday, {first_name}! From everyone at {organization_name}', max_length=180),
        ),
    ]
