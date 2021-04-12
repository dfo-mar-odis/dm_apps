# Generated by Django 3.1.2 on 2021-03-18 10:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import edna.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shared_models', '0006_auto_20210225_1538'),
    ]

    operations = [
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('program_description', models.TextField(blank=True, null=True, verbose_name='program description')),
                ('location_description', models.TextField(blank=True, null=True, verbose_name='area of operation')),
                ('contact_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='contact name')),
                ('contact_email', models.EmailField(blank=True, max_length=255, null=True, verbose_name='contact email')),
                ('start_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='start date')),
                ('end_date', models.DateTimeField(blank=True, editable=False, null=True, verbose_name='end date')),
                ('contact_users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='contact DMApps user(s)')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collection_created_by', to=settings.AUTH_USER_MODEL)),
                ('fiscal_year', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collections', to='shared_models.fiscalyear')),
                ('province', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='edna_collections', to='shared_models.province')),
                ('region', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='edna_collections', to='shared_models.region', verbose_name='DFO region')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DNAExtract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField(verbose_name='start time')),
                ('storage_location', models.CharField(blank=True, max_length=255, null=True, verbose_name='storage location')),
                ('comments', models.CharField(blank=True, max_length=1000, null=True, verbose_name='comments')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dnaextract_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['extraction_batch', 'filter_id'],
            },
        ),
        migrations.CreateModel(
            name='DNAExtractionProtocol',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description (en)')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description (fr)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FiltrationType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Description (en)')),
                ('description_fr', models.TextField(blank=True, null=True, verbose_name='Description (fr)')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Species',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('common_name_en', models.CharField(max_length=255, verbose_name='common name (EN)')),
                ('common_name_fr', models.CharField(blank=True, max_length=255, null=True, verbose_name='common name (FR)')),
                ('scientific_name', models.CharField(blank=True, max_length=255, null=True, verbose_name='scientific name')),
                ('tsn', models.IntegerField(blank=True, null=True, verbose_name='ITIS TSN')),
                ('aphia_id', models.IntegerField(blank=True, null=True, verbose_name='AphiaID')),
            ],
            options={
                'verbose_name_plural': 'Species',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='name (en)')),
                ('nom', models.CharField(blank=True, max_length=255, null=True, verbose_name='name (fr)')),
            ],
            options={
                'ordering': ['name'],
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unique_sample_identifier', models.CharField(max_length=255, unique=True, verbose_name='bottle unique identifier')),
                ('site_identifier', models.CharField(blank=True, max_length=255, null=True, verbose_name='site identifier')),
                ('site_description', models.TextField(blank=True, null=True, verbose_name='site description')),
                ('samplers', models.CharField(blank=True, max_length=255, null=True, verbose_name='sampler(s)')),
                ('datetime', models.DateTimeField(null=True, verbose_name='collection date')),
                ('latitude', models.FloatField(null=True, verbose_name='latitude')),
                ('longitude', models.FloatField(null=True, verbose_name='longitude')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='field comments')),
                ('collection', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.DO_NOTHING, related_name='samples', to='edna.collection', verbose_name='collection')),
            ],
            options={
                'ordering': ['collection', 'unique_sample_identifier'],
            },
        ),
        migrations.CreateModel(
            name='PCRBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('operators', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='operator(s)')),
            ],
            options={
                'verbose_name_plural': 'PCR Batches',
            },
        ),
        migrations.CreateModel(
            name='PCR',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField(verbose_name='start time')),
                ('pcr_number_prefix', models.CharField(blank=True, max_length=25, null=True, verbose_name='PCR number prefix')),
                ('pcr_number_suffix', models.IntegerField(blank=True, null=True, verbose_name='PCR number suffix')),
                ('plate_id', models.CharField(blank=True, max_length=25, null=True, verbose_name='plate Id')),
                ('position', models.CharField(blank=True, max_length=25, null=True, verbose_name='position')),
                ('ipc_added', models.CharField(blank=True, max_length=25, null=True, verbose_name='IPC added')),
                ('qpcr_ipc', models.FloatField(blank=True, null=True, verbose_name='qPCR IPC')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcr_created_by', to=settings.AUTH_USER_MODEL)),
                ('extract', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='pcrs', to='edna.dnaextract', verbose_name='extract Id')),
                ('pcr_batch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcrs', to='edna.pcrbatch', verbose_name='PCR batch')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='pcr_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pcr_batch', 'extract', 'pcr_number_suffix'],
            },
        ),
        migrations.CreateModel(
            name='FiltrationBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('operators', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='operator(s)')),
            ],
            options={
                'verbose_name_plural': 'Filtration Batches',
            },
        ),
        migrations.CreateModel(
            name='Filter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('start_datetime', models.DateTimeField(verbose_name='start time')),
                ('duration_min', models.IntegerField(blank=True, null=True, verbose_name='duration (min)')),
                ('filtration_volume_ml', models.FloatField(blank=True, null=True, verbose_name='volume (ml)')),
                ('storage_location', models.CharField(blank=True, max_length=1000, null=True, verbose_name='storage location')),
                ('comments', models.CharField(blank=True, max_length=1000, null=True, verbose_name='comments')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='filter_created_by', to=settings.AUTH_USER_MODEL)),
                ('filtration_batch', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='filters', to='edna.filtrationbatch', verbose_name='filtration batch')),
                ('filtration_type', models.ForeignKey(default=1, on_delete=django.db.models.deletion.DO_NOTHING, related_name='filters', to='edna.filtrationtype', verbose_name='filtration type')),
                ('sample', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='filters', to='edna.sample', verbose_name='field sample')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='filter_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['filtration_batch', 'sample'],
            },
        ),
        migrations.CreateModel(
            name='File',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('caption', models.CharField(max_length=255)),
                ('file', models.FileField(upload_to=edna.models.file_directory_path)),
                ('date_created', models.DateTimeField(auto_now=True)),
                ('collection', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='files', to='edna.collection')),
            ],
            options={
                'ordering': ['-date_created'],
            },
        ),
        migrations.CreateModel(
            name='ExtractionBatch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(default=django.utils.timezone.now, verbose_name='start date/time')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('operators', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL, verbose_name='operator(s)')),
            ],
            options={
                'verbose_name_plural': 'DNA Extraction Batches',
            },
        ),
        migrations.AddField(
            model_name='dnaextract',
            name='dna_extraction_protocol',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='edna.dnaextractionprotocol', verbose_name='extraction protocol'),
        ),
        migrations.AddField(
            model_name='dnaextract',
            name='extraction_batch',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='extracts', to='edna.extractionbatch', verbose_name='extraction batch'),
        ),
        migrations.AddField(
            model_name='dnaextract',
            name='filter',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='edna.filter'),
        ),
        migrations.AddField(
            model_name='dnaextract',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='dnaextract_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='collection',
            name='tags',
            field=models.ManyToManyField(blank=True, to='edna.Tag', verbose_name='tags'),
        ),
        migrations.AddField(
            model_name='collection',
            name='updated_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='collection_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SpeciesObservation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('ct', models.FloatField(blank=True, null=True, verbose_name='cycle threshold (ct)')),
                ('edna_conc', models.FloatField(blank=True, null=True, verbose_name='eDNA concentration (Pg/L)')),
                ('is_undetermined', models.BooleanField(default=False, verbose_name='undetermined?')),
                ('comments', models.TextField(blank=True, null=True, verbose_name='comments')),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='speciesobservation_created_by', to=settings.AUTH_USER_MODEL)),
                ('pcr', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='observations', to='edna.pcr', verbose_name='PCR')),
                ('species', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='observations', to='edna.species', verbose_name='species')),
                ('updated_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='speciesobservation_updated_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['pcr', 'species'],
                'unique_together': {('pcr', 'species')},
            },
        ),
    ]