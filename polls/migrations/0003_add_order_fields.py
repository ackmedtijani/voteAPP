from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0002_remove_respondents_answers_respondents_answers'),
    ]

    operations = [
        migrations.AddField(
            model_name='questions',
            name='order',
            field = models.IntegerField(null=True, blank=True)
        ),
        migrations.AddField(
            model_name='answers',
            name='order',
            field=models.IntegerField(null = True , blank=True),
        ),
    ]
