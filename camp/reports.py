import statistics
import pandas
import unicodecsv as csv
import xlsxwriter as xlsxwriter
from django.http import HttpResponse
from django.template.defaultfilters import yesno, floatformat
from django.utils import timezone
from math import pi

from bokeh.io import show, export_png, export_svgs
from bokeh.models import SingleIntervalTicker, ColumnDataSource, HoverTool, LabelSet, Label, Title
from bokeh.plotting import figure, output_file, save
from bokeh import palettes
from bokeh.transform import cumsum
from django.db.models import Sum, Q, Avg, Count
from shutil import rmtree
from django.conf import settings

from lib.functions.custom_functions import listrify
from lib.templatetags.custom_filters import nz, zero2val
from . import models
import numpy as np
import os
import pandas as pd


def generate_species_count_report(species_list):
    # start assigning files and by cleaning the temp dir
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(base_dir, 'templates', 'camp', 'temp')
    target_file = os.path.join(target_dir, 'report_temp_{}.html'.format(timezone.now().strftime("%H%M%S")))
    # target_file = os.path.join(target_dir, 'report_temp.html')

    try:
        rmtree(target_dir)
    except:
        print("no such dir.")
    os.mkdir(target_dir)

    # output to static HTML file
    output_file(target_file)

    # create a new plot
    title_eng = "Count of Species Observations by Year"

    p = figure(
        tools="pan,box_zoom,wheel_zoom,reset,save",
        x_axis_label='Year',
        y_axis_label='Count',
        plot_width=1200, plot_height=600,

    )

    p.add_layout(Title(text=title_eng, text_font_size="16pt"), 'above')

    # determine number of species
    # print(species_list)
    my_list = species_list.split(",")

    # prime counter variable
    i = 0

    # generate color palette
    if len(my_list) <= 2:
        colors = palettes.Set1[3][:len(my_list)]
    elif len(my_list) <= 9:
        colors = palettes.Set1[len(my_list)]
    else:
        colors = palettes.Category20[len(my_list)]

    for obj in my_list:
        sp_id = int(obj.replace("'", ""))
        # create a new file containing data
        qs = models.SpeciesObservation.objects.filter(species=sp_id).values(
            'sample__year'
        ).distinct().annotate(dsum=Sum('total_non_sav'))

        years = [i["sample__year"] for i in qs]
        counts = [i["dsum"] for i in qs]
        my_sp = models.Species.objects.get(pk=sp_id)
        legend_title = "Annual observations for {}".format(my_sp.common_name_eng)
        p.line(years, counts, legend=legend_title, line_color=colors[i], line_width=3)
        p.circle(years, counts, legend=legend_title, fill_color=colors[i], line_color=colors[i], size=8)
        i += 1

    save(p)


WIDTH = 1200
HEIGHT = 800
TITLE_FONT_SIZE = '13pt'
SUBTITLE_FONT_SIZE = '12pt'
LEGEND_FONT_SIZE = '10pt'


def generate_annual_watershed_report(site, year):
    # start assigning files and by cleaning the temp dir
    # base_dir = os.path.dirname(os.path.abspath(__file__))
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'camp', 'temp')
    target_file_pie = os.path.join(target_dir, 'pie_chart.png')
    target_file_richness1 = os.path.join(target_dir, 'species_richness1.png')
    target_file_richness2 = os.path.join(target_dir, 'species_richness2.png')
    target_file_do1 = os.path.join(target_dir, 'do1.png')
    target_file_do2 = os.path.join(target_dir, 'do2.png')
    target_file_greeb_crab1 = os.path.join(target_dir, 'green_crab1.png')
    target_file_greeb_crab2 = os.path.join(target_dir, 'green_crab2.png')

    try:
        rmtree(target_dir)
    except:
        print("no such dir.")
    finally:
        os.mkdir(target_dir)

    try:
        generate_sub_pie_chart(site, year, target_file_pie)
    except IndexError:
        pass

    generate_sub_species_richness_1(site, target_file_richness1)
    generate_sub_species_richness_2(site, target_file_richness2)
    generate_sub_do_1(site, target_file_do1)
    generate_sub_do_2(site, target_file_do2)
    generate_sub_green_crab_1(site, target_file_greeb_crab1)
    generate_sub_green_crab_2(site, target_file_greeb_crab2)

    return None


def generate_sub_pie_chart(site, year, target_file):
    # species will be represented by percentages of the total number of species observed at a given site
    species_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 17, 18, 19, ]

    # create a dictionary of species codes by counts
    x = {}
    for s in species_list:
        s_code = "{} / {}".format(models.Species.objects.get(pk=s).common_name_eng, models.Species.objects.get(pk=s).common_name_fre)
        s_sum = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
            sample__year=year).filter(
            species_id=s).order_by("species").values('species').distinct().annotate(
            dsum=Sum('total_non_sav'))
        try:
            x[s_code] = s_sum[0]["dsum"]
        except:
            x[s_code] = 0

    # now we need to add the 'other' category
    cum_mod = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(sample__year=year)
    for s in species_list:
        s_code = 'Other / autres'
        cum_mod = cum_mod.filter(~Q(species_id=s))

    cum_mod = cum_mod.order_by('sample__station__site_id').values('sample__station__site_id').distinct().annotate(
        dsum=Sum('total_non_sav'))
    try:
        x[s_code] = cum_mod[0]["dsum"]
    except:
        x[s_code] = 0

    # prepare the data for the glyph
    data = pd.Series(x).reset_index(name='value').rename(columns={'index': 'species'})
    data['angle'] = data['value'] / data['value'].sum() * 2 * pi
    data['percentage'] = data['value'] / data['value'].sum()
    data['color'] = palettes.Category20[len(x)]
    data['legend_label'] = ["{} - {:.1%}".format(data['species'][i], data['percentage'][i]) for i in range(0, len(x))]

    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)
    # if the year selected is 2018, there is a special case since there was only one sample take
    # in order to make this very clear in the graph, the title should contain the name of the month at which the sample occurred, i.e. June
    if year == 2018:
        title_fre = "Espèces communes capturées à {}, durant l’échantillonnage du PSCA en juin {}".format(site_name_fre, year)
        title_eng = "Most common species captured during CAMP sampling in {} in June {}".format(site_name, year)
    else:
        title_fre = "Espèces communes capturées à {}, durant l’échantillonnage du PSCA en {}".format(site_name_fre, year)
        title_eng = "Most common species captured during CAMP sampling in {} in {}".format(site_name, year)

    p = figure(plot_height=HEIGHT, plot_width=WIDTH, toolbar_location=None,
               x_range=(-0.5, 1.0), )
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.wedge(x=0, y=0, radius=0.4,
            start_angle=cumsum('angle', include_zero=True), end_angle=cumsum('angle'),
            line_color="white", fill_color='color', legend='legend_label', source=data)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    total_mod = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
        sample__year=year).order_by('sample__station__site_id').values('sample__station__site_id').distinct().annotate(
        dsum=Sum('total_non_sav'))
    total_abundance = total_mod[0]["dsum"]
    citation = Label(x=0.45, y=-0.7,
                     text='Total abundance / abondance totale = {:,}'.format(total_abundance), render_mode='css',
                     border_line_color='black', border_line_alpha=1.0,
                     background_fill_color='white', background_fill_alpha=1.0)
    p.add_layout(citation)

    p.axis.axis_label = None
    p.axis.visible = False
    p.grid.grid_line_color = None
    export_png(p, filename=target_file)
    return None


def generate_sub_species_richness_1(site, target_file):
    """
    Species richness plot:  will show all sites sampled in the month of June ONLY
    """
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_fre = "Comparaison annuelle de la diversité des espèces à chaque station d’échantillonnage du PSCA à"
    title_fre1 = "{} pour le mois de juin ou juillet seulement".format(site_name_fre)
    sub_title_fre = "La diversité cumulative des espèces pour toutes les stations et le nombre de stations échantillonnées sont aussi indiqués."
    title_eng = "Annual comparison of species richness at each CAMP sampling station in {} for June or July only".format(site_name)
    sub_title_eng = "Cumulative species richness of all stations and number of stations sampled are also indicated."

    p = figure(
        x_axis_label='Year / année',
        y_axis_label="Species count / nombre d'espèces",
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,

    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    # p.title.text_font_size = TITLE_FONT_SIZE
    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()
        # Only keep a year if there was june sampling
        qs_years = [y for y in qs_years if models.Sample.objects.filter(station=station, year=y['year'], month=6).count() > 0]

        years = []
        counts = []

        for obj in qs_years:
            y = obj['year']
            annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station=station,
                                                                  species__sav=False).filter(Q(sample__month=6)).values(
                'species_id',
            ).distinct()
            species_set = set([i["species_id"] for i in annual_obs])
            years.append(y)
            counts.append(len(species_set))

        legend_title = str(station)

        source = ColumnDataSource(data={
            'year': years,
            'count': counts,
            'station': list(np.repeat(str(station), len(years)))
        })

        p.line("year", "count", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("year", "count", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # Show a line for entire site
    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
        'year',
    ).distinct()
    # Only keep a year if there was june sampling
    qs_years = [y for y in qs_years if models.Sample.objects.filter(station__site_id=site, year=y['year'], month=6).count() > 0]

    years = []
    counts = []
    sample_counts = []

    for obj in qs_years:
        y = obj['year']
        annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                              species__sav=False).filter(Q(sample__month=6)).values(
            'species_id',
        ).distinct()
        species_set = set([i["species_id"] for i in annual_obs])
        years.append(y)
        counts.append(len(species_set))
        # sample_counts.append(models.Sample.objects.filter(year=y, station__site_id=site).count())
        sample_counts.append(models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                                      species__sav=False).filter(
            Q(sample__month=6)).values('sample_id', ).distinct().count())

    legend_title = "Entire site / ensemble du site"

    source = ColumnDataSource(data={
        'year': years,
        'count': counts,
        'station': list(np.repeat("all stations", len(years))),
        'sample_count': sample_counts,
    })

    p.line("year", "count", legend=legend_title, line_width=3, line_color='black', line_dash="4 4", source=source)
    p.circle("year", "count", legend=legend_title, fill_color='black', line_color="black", size=8, source=source)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    p.legend.location = "bottom_left"
    labels = LabelSet(x='year', y='count', text='sample_count', level='glyph',
                      x_offset=-5, y_offset=10, source=source, render_mode='canvas')
    p.add_layout(labels)

    export_png(p, filename=target_file)


def generate_sub_species_richness_2(site, target_file):
    """
    Species richness plot:  will show all sites sampled in the month of June, July and Aug. Months without all three months will be excluded
    """
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_fre = "Comparaison annuelle de la diversité des espèces à chaque station d’échantillonnage du PSCA à"
    title_fre1 = "{} pour les années durant lesquelles l’échantillonnage fut effectué en juin, juillet et août".format(site_name_fre)
    sub_title_fre = "La diversité cumulative des espèces pour toutes les stations et le nombre de stations échantillonnées sont aussi indiqués."
    title_eng = "Annual comparison of species richness at each CAMP sampling station in {} for years in which".format(site_name)
    title_eng1 = "sampling was conducted in June, July and August"
    sub_title_eng = "Cumulative species richness of all stations and number of stations sampled are also indicated."

    p = figure(
        x_axis_label='Year / année',
        y_axis_label="Species count / nombre d'espèces",
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,

    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    # p.title.text_font_size = TITLE_FONT_SIZE
    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()
        # Only keep a year if there is sampling in June, July AND August
        qs_years = [y for y in qs_years if
                    models.Sample.objects.filter(station=station, year=y['year'], month=6).count() > 0 and models.Sample.objects.filter(
                        station=station, year=y['year'], month=7).count() > 0 and models.Sample.objects.filter(station=station,
                                                                                                               year=y['year'],
                                                                                                               month=8).count() > 0]

        years = []
        counts = []

        for obj in qs_years:
            y = obj['year']
            annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station=station,
                                                                  species__sav=False).filter(Q(sample__month=6) | Q(sample__month=7) |
                                                                                             Q(sample__month=8)).values(
                'species_id',
            ).distinct()
            species_set = set([i["species_id"] for i in annual_obs])
            years.append(y)
            counts.append(len(species_set))

        legend_title = str(station)

        source = ColumnDataSource(data={
            'year': years,
            'count': counts,
            'station': list(np.repeat(str(station), len(years)))
        })

        p.line("year", "count", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("year", "count", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # Show a line for entire site
    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
        'year',
    ).distinct()
    # Only keep a year if there is sampling in June, July AND August
    qs_years = [y for y in qs_years if
                models.Sample.objects.filter(station__site_id=site, year=y['year'], month=6).count() > 0 and models.Sample.objects.filter(
                    station__site_id=site, year=y['year'], month=7).count() > 0 and models.Sample.objects.filter(station__site_id=site,
                                                                                                                 year=y['year'],
                                                                                                                 month=8).count() > 0]
    years = []
    counts = []
    sample_counts = []

    for obj in qs_years:
        y = obj['year']
        annual_obs = models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                              species__sav=False).filter(Q(sample__month=6) | Q(sample__month=7) |
                                                                                         Q(sample__month=8)).values(
            'species_id',
        ).distinct()
        species_set = set([i["species_id"] for i in annual_obs])
        years.append(y)
        counts.append(len(species_set))
        # sample_counts.append(models.Sample.objects.filter(year=y, station__site_id=site).count())
        sample_counts.append(models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                                      species__sav=False).filter(
            Q(sample__month=6) | Q(sample__month=7) | Q(sample__month=8)).values(
            'sample_id', ).distinct().count())

    legend_title = "Entire site / ensemble du site"

    source = ColumnDataSource(data={
        'year': years,
        'count': counts,
        'station': list(np.repeat("all stations", len(years))),
        'sample_count': sample_counts,
    })

    p.line("year", "count", legend=legend_title, line_width=3, line_color='black', line_dash="4 4", source=source)
    p.circle("year", "count", legend=legend_title, fill_color='black', line_color="black", size=8, source=source)
    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    p.legend.location = "bottom_left"
    labels = LabelSet(x='year', y='count', text='sample_count', level='glyph',
                      x_offset=-5, y_offset=10, source=source, render_mode='canvas')
    p.add_layout(labels)

    export_png(p, filename=target_file)


def generate_sub_do_1(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_eng = "Annual comparison of dissolved oxygen concentrations at each CAMP sampling station in {}".format(site_name)
    title_eng1 = "for June or July only".format(site_name)
    sub_title_eng = "Number of stations sampled is indicated."
    title_fre = "Comparaison annuelle de la concentration d’oxygène dissous à chaque station du PSCA à {} pour".format(site_name_fre)
    title_fre1 = "le mois de juin ou juillet seulement"
    sub_title_fre = "Le nombre de stations échantillonnées est indiqué."

    p = figure(
        x_axis_label='Year / année',
        y_axis_label='Dissolved oxygen / oxygène dissous (mg/l)',
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,
    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()

        years = []
        # do_max = []
        # do_min = []
        do_avg = []

        for obj in qs_years:
            y = obj['year']
            do_readings = [obj.dissolved_o2 for obj in models.Sample.objects.filter(year=y).filter(station=station).filter(Q(month=6)) if
                           obj.dissolved_o2 is not None]
            try:
                # do_max.append(max(do_readings))
                # do_min.append(min(do_readings))
                do_avg.append(statistics.mean(do_readings))
            except ValueError:
                # do_max.append(None)
                # do_max.append(None)
                pass
            else:
                years.append(y)

        legend_title = str(station)
        source = ColumnDataSource(data={
            'stations': list(np.repeat(str(station), len(years))),
            'years': years,
            # 'do_max': do_max,
            # 'do_min': do_min,
            'do_avg': do_avg,
        })

        # p.segment("years", "do_max", "years", "do_min", color=colors[i], source=source)
        # p.dash(x="years", y="do_max", size=15, color=colors[i], source=source)
        # p.dash(x="years", y="do_min", size=15, color=colors[i], source=source)
        p.line("years", "do_avg", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("years", "do_avg", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # redo the whole process at the site level for total number of samples
    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
        'year',
    ).distinct()

    years = []
    do_max = []
    do_min = []
    do_avg = []
    sample_counts = []

    for obj in qs_years:
        y = obj['year']
        do_readings = [obj.dissolved_o2 for obj in models.Sample.objects.filter(year=y).filter(station__site_id=site).filter(Q(month=6)) if
                       obj.dissolved_o2 is not None]

        try:
            do_max.append(max(do_readings))
            do_min.append(min(do_readings))
            do_avg.append(statistics.mean(do_readings))
        except ValueError:
            pass
        else:
            years.append(y)
            sample_counts.append(models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site,
                                                                          species__sav=False).filter(Q(sample__month=6)).values(
                'sample_id', ).distinct().count())

    source = ColumnDataSource(data={
        'years': years,
        'do_max': do_max,
        'do_min': do_min,
        'do_avg': do_avg,
        'sample_count': sample_counts,
    })

    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    labels = LabelSet(x='years', y='do_max', text='sample_count', level='glyph',
                      x_offset=-10, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)
    export_png(p, filename=target_file)


def generate_sub_do_2(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_eng = "Annual comparison of dissolved oxygen concentrations (mean and range) at each CAMP sampling station in"
    title_eng1 = "{} for years in which sampling was conducted in June, July and August".format(site_name)
    sub_title_eng = "Number of stations sampled is indicated above error bars."
    title_fre = "Comparaison annuelle des concentrations d’oxygène dissous (moyenne et intervalle) à chaque station du PSCA à"
    title_fre1 = "{} pour les années durant lesquelles l’échantillonnage fut effectué en juin, juillet et août".format(site_name_fre)
    sub_title_fre = "Le nombre de stations échantillonnées est indiqué au-dessus des barres d’erreur."

    p = figure(
        x_axis_label='Year / année',
        y_axis_label='Dissolved oxygen / oxygène dissous (mg/l)',
        plot_width=WIDTH, plot_height=HEIGHT,
        x_axis_type="linear",
        toolbar_location=None,
    )
    ticker = SingleIntervalTicker(interval=1)
    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    p.grid.grid_line_alpha = 1
    p.background_fill_color = "white"
    p.xaxis.minor_tick_line_color = None
    p.xaxis.ticker = ticker

    # first we need a list of stations
    stations = models.Station.objects.filter(site_id=site).order_by("name")

    # generate color palette
    if len(stations) <= 10:
        colors = palettes.Category10[len(stations)]
    else:
        colors = palettes.Category20[len(stations)]

    i = 0
    for station in stations:
        qs_years = models.Sample.objects.filter(station=station).order_by("year").values(
            'year',
        ).distinct()
        # Only keep a year if there is sampling in June, July AND August
        qs_years = [y for y in qs_years if
                    models.Sample.objects.filter(station=station, year=y['year'], month=6).count() > 0 and models.Sample.objects.filter(
                        station=station, year=y['year'], month=7).count() > 0 and models.Sample.objects.filter(station=station,
                                                                                                               year=y['year'],
                                                                                                               month=8).count() > 0]

        years = []
        do_max = []
        do_min = []
        do_avg = []

        for obj in qs_years:
            y = obj['year']
            do_readings = [obj.dissolved_o2 for obj in models.Sample.objects.filter(year=y).filter(station=station).filter(
                Q(month=6) | Q(month=7) | Q(month=8)) if obj.dissolved_o2 is not None]

            try:
                do_avg.append(statistics.mean(do_readings))
            except ValueError:
                pass
            else:
                do_max.append(max(do_readings))
                do_min.append(min(do_readings))
                years.append(y)

        legend_title = str(station)

        source = ColumnDataSource(data={
            'stations': list(np.repeat(str(station), len(years))),
            'years': years,
            'do_max': do_max,
            'do_min': do_min,
            'do_avg': do_avg,
        })

        p.segment("years", "do_max", "years", "do_min", color=colors[i], source=source)
        p.dash(x="years", y="do_max", size=15, color=colors[i], source=source)
        p.dash(x="years", y="do_min", size=15, color=colors[i], source=source)
        p.line("years", "do_avg", legend=legend_title, line_width=1, line_color=colors[i], source=source)
        p.circle("years", "do_avg", legend=legend_title, fill_color=colors[i], line_color=colors[i], size=3,
                 source=source)
        i += 1

    # redo the whole process at the site level for total number of samples
    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values(
        'year',
    ).distinct()
    # Only keep a year if there is sampling in June, July AND August
    qs_years = [y for y in qs_years if
                models.Sample.objects.filter(station=station, year=y['year'], month=6).count() > 0 and models.Sample.objects.filter(
                    station=station, year=y['year'], month=7).count() > 0 and models.Sample.objects.filter(station=station,
                                                                                                           year=y['year'],
                                                                                                           month=8).count() > 0]
    years = []
    do_max = []
    do_min = []
    do_avg = []
    sample_counts = []

    for obj in qs_years:
        y = obj['year']
        do_readings = [obj.dissolved_o2 for obj in models.Sample.objects.filter(year=y).filter(station__site_id=site).filter(
            Q(month=6) | Q(month=7) | Q(month=8)) if obj.dissolved_o2 is not None]
        do_max.append(max(do_readings))
        do_min.append(min(do_readings))
        do_avg.append(statistics.mean(do_readings))
        years.append(y)
        sample_counts.append(
            models.SpeciesObservation.objects.filter(sample__year=y, sample__station__site_id=site, species__sav=False).filter(
                Q(sample__month=6) | Q(sample__month=7) | Q(sample__month=8)).values('sample_id', ).distinct().count())

    source = ColumnDataSource(data={
        'years': years,
        'do_max': do_max,
        'do_min': do_min,
        'do_avg': do_avg,
        'sample_count': sample_counts,
    })

    p.legend.label_text_font_size = LEGEND_FONT_SIZE
    labels = LabelSet(x='years', y='do_max', text='sample_count', level='glyph',
                      x_offset=-10, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)
    export_png(p, filename=target_file)


def generate_sub_green_crab_1(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_eng = "Annual comparison of Green Crab abundance observed during CAMP sampling in {} for June or July only".format(site_name)
    sub_title_eng = "Number of stations sampled is indicated above columns."
    title_fre = "Comparaison annuelle de l’abondance de Crabes verts observée durant l’échantillonnage du PSCA à "
    title_fre1 = "{} pour le mois de juin ou juillet seulement".format(site_name_fre)
    sub_title_fre = "Le nombre de stations échantillonnées est indiqué au-dessus des colonnes."

    color = palettes.BuGn[5][2]

    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values('year', ).distinct()
    # Only keep a year if there is sampling in June
    years = [y["year"] for y in qs_years if models.Sample.objects.filter(station__site_id=site, year=y['year'], month=6).count() > 0]
    counts = []
    sample_counts = []

    for year in years:
        green_crab_sum = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(
            sample__year=year).filter(species_id=18).filter(Q(sample__month=6)).order_by("species").values('species').distinct().annotate(
            dsum=Sum('total_non_sav'))
        try:
            counts.append(green_crab_sum[0]["dsum"])
        except:
            counts.append(0)
        sample_counts.append(
            models.SpeciesObservation.objects.filter(sample__year=year, sample__station__site_id=site, species__sav=False).filter(
                Q(sample__month=6)).values('sample_id', ).distinct().count())

    years = [str(y) for y in years]
    source = ColumnDataSource(data={
        'years': years,
        'counts': counts,
        'sample_count': sample_counts,

    })
    p = figure(
        x_range=years,
        toolbar_location=None,
        plot_width=WIDTH,
        plot_height=HEIGHT,
        x_axis_label='Year / année',
        y_axis_label='Abundance / Abondance',
    )
    p.vbar(x='years', top='counts', width=0.9, source=source, line_color='white', fill_color=color)

    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    labels = LabelSet(x='years', y='counts', text='sample_count', level='glyph',
                      x_offset=-10, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)

    # show(p)
    export_png(p, filename=target_file)


def generate_sub_green_crab_2(site, target_file):
    # create a new plot
    site_name = str(models.Site.objects.get(pk=site))
    site_name_fre = "{} ({})".format(models.Site.objects.get(pk=site).site, models.Site.objects.get(pk=site).province.abbrev_fre)

    title_eng = "Annual comparison of Green Crab abundance observed during CAMP sampling in {} for years in ".format(site_name)
    title_eng1 = "which sampling was conducted in June, July and August"
    sub_title_eng = "Number of stations sampled is indicated above columns."
    title_fre = "Comparaison annuelle de l’abondance de Crabes verts observée durant l’échantillonnage du PSCA à"
    title_fre1 = "{} pour les années durant lesquelles l’échantillonnage fut effectué en juin, juillet et août".format(site_name_fre)
    sub_title_fre = "Le nombre de stations échantillonnées est indiqué au-dessus des colonnes."

    color = palettes.BuGn[5][2]

    # years = [obj["year"] for obj in models.Sample.objects.order_by("year").values('year').distinct()]
    # # Only keep a year if there is sampling in June, July AND August
    # years = [y for y in years if models.Sample.objects.filter(year=y, month=6).count() > 0 and models.Sample.objects.filter(year=y, month=7).count() > 0 and models.Sample.objects.filter( year=y, month=8).count() > 0]

    qs_years = models.Sample.objects.filter(station__site_id=site).order_by("year").values('year', ).distinct()
    # Only keep a year if there is sampling in June, July AND August
    years = [y["year"] for y in qs_years if
             models.Sample.objects.filter(station__site_id=site, year=y['year'], month=6).count() > 0 and models.Sample.objects.filter(
                 station__site_id=site, year=y['year'], month=7).count() > 0 and models.Sample.objects.filter(station__site_id=site,
                                                                                                              year=y['year'],
                                                                                                              month=8).count() > 0]
    counts = []
    sample_counts = []

    for year in years:
        green_crab_sum = models.SpeciesObservation.objects.filter(sample__station__site_id=site).filter(sample__year=year).filter(
            species_id=18).filter(Q(sample__month=6) | Q(sample__month=7) | Q(sample__month=8)).order_by("species").values(
            'species').distinct().annotate(dsum=Sum('total_non_sav'))

        try:
            counts.append(green_crab_sum[0]["dsum"])
        except:
            counts.append(0)
        sample_counts.append(
            models.SpeciesObservation.objects.filter(sample__year=year, sample__station__site_id=site, species__sav=False).filter(
                Q(sample__month=6) | Q(sample__month=7) | Q(sample__month=8)).values('sample_id', ).distinct().count())

    years = [str(y) for y in years]
    source = ColumnDataSource(data={
        'years': years,
        'counts': counts,
        'sample_count': sample_counts,

    })
    p = figure(
        x_range=years,
        toolbar_location=None,
        plot_width=WIDTH,
        plot_height=HEIGHT,
        x_axis_label='Year / année',
        y_axis_label='Abundance / Abondance',
    )
    p.vbar(x='years', top='counts', width=0.9, source=source, line_color='white', fill_color=color)

    p.add_layout(Title(text=sub_title_fre, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_fre1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_fre, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=sub_title_eng, text_font_size=SUBTITLE_FONT_SIZE, text_font_style="italic"), 'above')
    p.add_layout(Title(text=title_eng1, text_font_size=TITLE_FONT_SIZE), 'above')
    p.add_layout(Title(text=title_eng, text_font_size=TITLE_FONT_SIZE), 'above')

    labels = LabelSet(x='years', y='counts', text='sample_count', level='glyph',
                      x_offset=-10, y_offset=5, source=source, render_mode='canvas')
    p.add_layout(labels)

    # show(p)
    export_png(p, filename=target_file)


def generate_annual_watershed_spreadsheet(site, year):
    # figure out the filename
    target_dir = os.path.join(settings.BASE_DIR, 'media', 'camp', 'temp')
    target_file = "temp_data_export.xlsx"
    target_file_path = os.path.join(target_dir, target_file)
    target_url = os.path.join(settings.MEDIA_ROOT, 'camp', 'temp', target_file)

    # get a sample list for the site / year
    sample_list = models.Sample.objects.filter(year=year).filter(station__site=site).order_by("station__station_number", "start_date")
    # create workbook and worksheets
    workbook = xlsxwriter.Workbook(target_file_path)
    worksheet1 = workbook.add_worksheet(name="Fauna - Faune")
    worksheet2 = workbook.add_worksheet(name="Sediment - Sédiment")
    worksheet3 = workbook.add_worksheet(name="Vegetation - Végétation")

    # spreadsheet: Fauna #
    ######################

    # get a list of species obs for which sav == false
    species_list = models.Species.objects.filter(sav=False).order_by("code")

    # convert species list into headers (a, yoy, tot)
    species_header_list = []
    for s in species_list:
        species_header_list.append("{}(A)".format(s.code))
        species_header_list.append("{}(YOY)".format(s.code))
        species_header_list.append("{}(TOT)".format(s.code))

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
        "Time start",
        "Time finish",
        "Water Sample #",
        "Rain 24h Y / N",
        "Stage of tide",
        "Samplers name",
        "Water temp",
        "Salinity",
        "Dissolved Oxygen",
        "Water turbidity",
        "SP. RICHNESS",
        "TOTAL",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
        "Heure début",
        "Heure fin",
        "# échantillon d'eau",
        "Pluie 24h O / N",
        "Stade de marée",
        "Nom échantillonneurs",
        "Temp eau",
        "Salinité",
        "Oxygène dissout",
        "Turbidité de l'eau",
        "SP. RICHNESS",
        "TOTAL",
    ]

    # insert species headers 2 from the last item in header_eng / fre
    header_eng[-2:-2] = species_header_list
    header_fre[-2:-2] = species_header_list

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
            s.start_date.strftime("%H:%M"),
            s.end_date.strftime("%H:%M"),
            s.nutrient_sample_id,
            yesno(s.rain_past_24_hours),
            "{} - {}".format(s.get_tide_state_display(), s.get_tide_direction_display(), ),
            s.samplers,
            s.h2o_temperature_c,
            s.salinity,
            s.dissolved_o2,
            s.get_water_turbidity_display(),
        ]

        # now get species data
        species_obs_list = []

        for species in species_list:
            try:
                species_obs = models.SpeciesObservation.objects.get(sample=s, species=species)
            except:
                species_obs_list.append(0)
                species_obs_list.append(0)
                species_obs_list.append(0)
            else:
                nz(species_obs_list.append(species_obs.adults), 0)
                nz(species_obs_list.append(species_obs.yoy), 0)
                species_obs_list.append(species_obs.total_non_sav)

        data_row.extend(species_obs_list)

        # species richness
        annual_obs = models.SpeciesObservation.objects.filter(sample=s, species__sav=False).values(
            'species_id',
        ).distinct()
        species_set = set([i["species_id"] for i in annual_obs])
        data_row.append(len(species_set))

        # total count
        total = models.SpeciesObservation.objects.filter(sample=s, species__sav=False).values(
            'sample_id'
        ).aggregate(dsum=Sum('total_non_sav'))
        data_row.append(total['dsum'])

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    total_format = workbook.add_format({'bg_color': '#D6D1C0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})
    bold_format = workbook.add_format({"align": 'center', 'bold': True})

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet1.write(i, j, my_val, header_format)
            elif "(TOT)" in my_df[j][0]:
                worksheet1.write(i, j, my_val, total_format)
            else:
                worksheet1.write(i, j, my_val, normal_format)

    # add the total at bottom right
    total_sum = 0
    count = 0
    for j in my_df[my_df.shape[1] - 1]:
        if count > 1:
            total_sum = total_sum + nz(j, 0)
        count += 1
    worksheet1.write(my_df.shape[0], my_df.shape[1] - 2, "TOTAL", bold_format)
    worksheet1.write(my_df.shape[0], my_df.shape[1] - 1, total_sum, bold_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet1.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: sediment #
    #########################

    # get a list of species obs for which sav == false
    species_list = models.Species.objects.filter(sav=False).order_by("code")

    for s in species_list:
        species_header_list.append("{}(A)".format(s.code))
        species_header_list.append("{}(YOY)".format(s.code))
        species_header_list.append("{}(TOT)".format(s.code))

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
        "% sand",
        "% gravel",
        "% rocky",
        "% mud",
        "Overall visual sediment observation",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
        "% sable",
        "% gravier",
        "% rocheux",
        "% vase",
        "Observation visuelle du sédiment",
    ]

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
            "{}%".format(nz(s.percent_sand, 0)),
            "{}%".format(nz(s.percent_gravel, 0)),
            "{}%".format(nz(s.percent_rock, 0)),
            "{}%".format(nz(s.percent_mud, 0)),
            "{}%".format(
                sum([nz(s.percent_sand, 0), nz(s.percent_gravel, 0), nz(s.percent_rock, 0), nz(s.percent_mud, 0)])),
        ]

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet2.write(i, j, my_val, header_format)
            else:
                worksheet2.write(i, j, my_val, normal_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet2.set_column(j, j, width=col_max[j] * 1.1)

    # spreadsheet: Veg #
    ####################

    # get a list of species obs for which sav == true
    species_list = models.Species.objects.filter(sav=True).order_by("code")

    # convert sav species list into headers (a, yoy, tot)
    species_header_list_eng = [s.common_name_eng for s in species_list]
    species_header_list_fre = [s.common_name_fre for s in species_list]

    header_eng = [
        "Site location",
        "Station #",
        "Station name",
        "Date",
        "Month",
        "Year",
    ]

    header_fre = [
        "Location Site",
        "# Station",
        "Nom station",
        "(dj/mm/ya)",
        "Mois",
        "Année",
    ]

    # insert species headers 2 from the last item in header_eng / fre
    header_eng.extend(species_header_list_eng)
    header_fre.extend(species_header_list_fre)

    # prime a dataframe obj with the two headers
    my_df = pandas.DataFrame([header_eng, header_fre], columns=[i for i in range(0, len(header_eng))])

    # write some data
    for s in sample_list:
        data_row = [
            s.station.site.site,
            s.station.station_number,
            s.station.name,
            s.start_date.strftime("%d/%m/%Y"),
            s.start_date.month,
            s.start_date.year,
        ]

        # now get species data
        species_obs_list = []

        for species in species_list:
            try:
                species_obs = models.SpeciesObservation.objects.get(sample=s, species=species)
            except:
                species_obs_list.append(0)
            else:
                species_obs_list.append(nz(species_obs.total_sav, 0))

        data_row.extend(species_obs_list)

        # store data_row in a dataframe
        my_df = my_df.append(pandas.DataFrame([data_row, ], columns=[i for i in range(0, len(data_row))]),
                             ignore_index=True)

    # create formatting
    header_format = workbook.add_format(
        {'bold': True, 'border': 1, 'border_color': 'black', 'bg_color': '#8C96A0', "align": 'center'})
    normal_format = workbook.add_format({"align": 'center'})

    # write dataframe to xlsx
    for i in range(0, my_df.shape[0]):
        for j in range(0, my_df.shape[1]):

            # tricky code since j and i are reverses from an intuitive perspective (i.e. not i,j)
            my_val = my_df[j][i]

            if i <= 1:
                worksheet3.write(i, j, my_val, header_format)
            else:
                worksheet3.write(i, j, my_val, normal_format)

    # adjust the width of the columns based on the max string length in each col
    col_max = [max([len(str(s)) for s in my_df[j].values]) for j in my_df.columns]
    for j in my_df.columns:
        worksheet3.set_column(j, j, width=col_max[j] * 1.1)

    workbook.close()
    return target_url


def generate_ais_spreadsheet(species_list):
    # figure out the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="CAMP AIS data export ({}).csv"'.format(timezone.now().strftime("%Y-%m-%d"))
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)
    # write the header
    writer.writerow([
        "Date Observed",
        "Site",
        "Station",
        "Province",
        "Latitude (N)",
        "Longitude (W)",
        "Species (TSN)",
        "Species (Common Name)",
        "Species (Scientific Name)",
        "Count",
    ])

    species_list = [models.Species.objects.get(pk=int(obj)) for obj in species_list.split(",")]
    q_objects = Q()  # Create an empty Q object to start with
    for s in species_list:
        q_objects |= Q(species=s)  # 'or' the Q objects together

    sp_observations = models.SpeciesObservation.objects.filter(q_objects)

    for obs in sp_observations:
        if obs.species.sav:
            count = obs.total_sav
        else:
            count = obs.total_non_sav

        writer.writerow(
            [
                obs.sample.start_date.strftime("%Y-%m-%d"),
                obs.sample.station.site.site,
                obs.sample.station.name,
                obs.sample.station.site.province.abbrev,
                obs.sample.station.latitude_n,
                obs.sample.station.longitude_w,
                obs.species.tsn,
                obs.species.common_name_eng,
                obs.species.scientific_name,
                count,
            ])
    return response


def generate_open_data_wms_report(lang=1):
    """
    Simple report for web mapping service on FGP
    """
    qs = models.SpeciesObservation.objects.all()
    filename = "camp_station_summary_eng.csv" if lang == 1 else "camp_station_summary_fra.csv"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    header_row = [
        'site',
        'province',
        'station',
        'station_latitude' if lang == 1 else "latitude_de_station",
        'station_longitude' if lang == 1 else "longitude_de_station",
        'seasons_in_operation_and_samples_collected' if lang == 1 else "saisons_en_opération_et_nombre_échontillions",
        'list_of_species_caught' if lang == 1 else "liste_des_espèces_capturées",
        'list_of_SAV' if lang == 1 else "list_de_VAS",
        'total_number_of_fish_caught' if lang == 1 else "nombre_total_de_poisson_capturées",
        'mean_annual_number_of_fish_caught' if lang == 1 else "nombre_annuel_moyen_de_poissons_capturés",
    ]

    writer.writerow(header_row)

    # lets start by getting a list of samples and years
    # samples = [models.Sample.objects.get(pk=obj["sample"]) for obj in qs.order_by("sample").values("sample").distinct()]
    stations = [models.Station.objects.get(pk=obj["sample__station"]) for obj in
                qs.order_by("sample__station__site", "sample__station").values("sample__station").distinct()]

    for station in stations:
        years = listrify(
            ["{}({})".format(
                obj["sample__year"],
                models.Sample.objects.filter(station=station, year=obj["sample__year"]).count(),
            ) for obj in qs.filter(sample__station=station).order_by("sample__year").values("sample__year").distinct()])

        if lang == 1:
            spp_list = listrify([models.Species.objects.get(pk=obj["species"]).common_name_eng for obj in
                                 qs.filter(sample__station=station, species__sav=False).order_by("species").values("species").distinct()])
            vas_list = listrify([models.Species.objects.get(pk=obj["species"]).common_name_eng for obj in
                                 qs.filter(sample__station=station, species__sav=True).order_by("species").values("species").distinct()])
        else:
            spp_list = listrify([models.Species.objects.get(pk=obj["species"]).common_name_fre for obj in
                                 qs.filter(sample__station=station, species__sav=False).order_by("species").values("species").distinct()])
            vas_list = listrify([models.Species.objects.get(pk=obj["species"]).common_name_fre for obj in
                                 qs.filter(sample__station=station, species__sav=True).order_by("species").values("species").distinct()])

        total_freq = qs.filter(sample__station=station, ).values("total_non_sav").order_by("total_non_sav").aggregate(
            dsum=Sum("total_non_sav"))["dsum"]
        avg_freq = floatformat(int(total_freq) / len(years.split(",")), 2)

        data_row = [
            station.site.site,
            station.site.province.abbrev_eng if lang == 1 else station.site.province.abbrev_fre,
            station.name,
            station.latitude_n,
            station.longitude_w,
            years,
            spp_list,
            vas_list,
            total_freq,
            avg_freq,
        ]

        writer.writerow(data_row)

    return response


def generate_open_data_species_list():
    """
    Generates the species list for open data
    """

    filename = "camp_species_list.csv"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    # write the header
    header = [
        "code",
        "common_name_en__nom_commun_en",
        "common_name_en__nom_commun_fr",
        "scientific_name__nom_scientifique",
        "ITIS_TSN",
    ]
    writer.writerow(header)

    for sp in models.Species.objects.all():
        writer.writerow([
            sp.code,
            sp.common_name_eng,
            sp.common_name_fre,
            sp.scientific_name,
            sp.tsn,
        ])
    return response


def generate_od1_report():
    """The resulting csv will return a csv with all species obs and related metadata"""

    # figure out the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="camp_species_observations.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)
    # write the header
    writer.writerow([
        "sample_id",
        "year",
        "month",
        "day",
        "site",
        "station",
        "latitude",
        "longitude",
        "species_code",
        "sav",
        "sav_level",
        "adults",
        "yoy",
        "total_ind",
        "total_all",
    ])

    for obs in models.SpeciesObservation.objects.all().order_by("-sample__start_date"):
        if obs.species.sav:
            total_sav = total = obs.total_sav
            adults = None
            yoy = None
            total_non_sav = None
        else:
            total_sav = None
            adults = obs.adults
            yoy = obs.yoy
            total_non_sav = total = obs.total_non_sav

        writer.writerow(
            [
                obs.sample.id,
                obs.sample.year,
                obs.sample.month,
                obs.sample.start_date.day,
                obs.sample.station.site,
                obs.sample.station.name,
                obs.sample.station.latitude_n,
                obs.sample.station.longitude_w,
                obs.species.code,
                obs.species.sav,
                total_sav,
                adults,
                yoy,
                total_non_sav,
                total,
            ])
    return response


def generate_od2_report():
    """The resulting csv will summarize data per station per year"""

    # grab all observations but exclude SAV
    qs = models.SpeciesObservation.objects.filter(species__sav=False)
    filename = "summary_by_station_by_year.csv"

    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)

    # headers are based on csv provided by GD
    species_list = [models.Species.objects.get(pk=obj["species"]) for obj in qs.order_by("species").values("species").distinct()]

    header_row = [
        'year',
        'site',
        'station',
        'latitude',
        'longitude',
        'number_of_samples',
        'avg_water_temp',
        'avg_sal',
        'avg_do',
        'spp_count',
    ]

    for species in species_list:
        addendum = [
            "{}_YOY".format(species.code),
            "{}_adults".format(species.code),
            "{}_total".format(species.code),
            "{}_avg_total".format(species.code),
        ]
        header_row.extend(addendum)

    writer.writerow(header_row)

    # lets start by getting a list of stations and years
    stations = [models.Station.objects.get(pk=obj["sample__station"]) for obj in
                qs.order_by("sample__station__site", "sample__station").values("sample__station").distinct()]
    years = [obj["sample__year"] for obj in qs.order_by("sample__year").values("sample__year").distinct()]
    for year in years:
        for station in stations:
            sample_count = models.Sample.objects.filter(station=station, year=year).count()
            if sample_count > 0:
                data_row = [
                    year,
                    station.site,
                    station.name,
                    station.latitude_n,
                    station.longitude_w,
                    sample_count,
                    floatformat(
                        qs.filter(sample__year=year, sample__station=station, ).values("sample").order_by("sample").distinct().aggregate(
                            davg=Avg("sample__h2o_temperature_c"))["davg"], 3),
                    floatformat(
                        qs.filter(sample__year=year, sample__station=station, ).values("sample").order_by("sample").distinct().aggregate(
                            davg=Avg("sample__salinity"))["davg"], 3),
                    floatformat(
                        qs.filter(sample__year=year, sample__station=station, ).values("sample").order_by("sample").distinct().aggregate(
                            davg=Avg("sample__dissolved_o2"))["davg"], 3),
                    qs.filter(sample__year=year, sample__station=station, ).values("species").order_by("species").distinct().aggregate(
                        dcount=Count("species"))["dcount"]
                ]

                for species in species_list:
                    yoy_sum = qs.filter(sample__year=year, sample__station=station, species=species).values("yoy").order_by(
                        "yoy").distinct().aggregate(dsum=Sum("yoy"))["dsum"]
                    adult_sum = qs.filter(sample__year=year, sample__station=station, species=species).values("adults").order_by(
                        "adults").distinct().aggregate(dsum=Sum("adults"))["dsum"]
                    total = zero2val(nz(yoy_sum, 0) + nz(adult_sum, 0), None)
                    addendum = [
                        yoy_sum,
                        adult_sum,
                        total,
                        total / sample_count if total else None,
                    ]
                    data_row.extend(addendum)
                writer.writerow(data_row)
    return response


def generate_od3_report():
    """camp sample report"""

    # figure out the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="camp_samples.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)
    # write the header
    writer.writerow([
        "sample_id",
        "year",
        "month",
        "day",
        "prov",
        "site",
        "station",
        "latitude",
        "longitude",
        "start_date",
        "end_date",
        "ammonia",
        "do",
        "nitrates",
        "nitrite",
        "phosphate",
        "sal",
        "silicate",
        "water_temp",
        "gravel",
        "mud",
        "rock",
        "sand",
    ])

    for sample in models.Sample.objects.all():
        writer.writerow(
            [
                sample.id,
                sample.year,
                sample.month,
                sample.start_date.day,
                "{} / {}".format(sample.station.site.province.abbrev_eng, sample.station.site.province.abbrev_fre),
                sample.station.site.site,
                sample.station.name,
                sample.station.latitude_n,
                sample.station.longitude_w,
                sample.start_date,
                sample.end_date,
                sample.ammonia,
                sample.dissolved_o2,
                sample.nitrates,
                sample.nitrite,
                sample.phosphate,
                sample.salinity,
                sample.silicate,
                sample.h2o_temperature_c,
                nz(sample.percent_gravel, 0),
                nz(sample.percent_mud, 0),
                nz(sample.percent_rock, 0),
                nz(sample.percent_sand, 0),
            ])
    return response


def generate_od_dict():
    # figure out the filename
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="camp_data_dictionary.csv"'
    response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
    writer = csv.writer(response)
    # write the header

    header = [
        "name_nom",
        "description_en",
        "description_fr",
    ]
    field_names = [
        "sample_id",
        "year",
        "month",
        "day",
        "prov",
        "site",
        "station",
        "latitude",
        "longitude",
        "start_date",
        "end_date",
        "ammonia",
        "do",
        "nitrates",
        "nitrite",
        "phosphate",
        "sal",
        "silicate",
        "water_temp",
        "gravel",
        "mud",
        "rock",
        "sand",
        "species_code",
        "tsn",
        "sav",
        "sav_level",
        "adults",
        "yoy",
        "total_ind",
        "total_all",
        'number_of_samples',
        'avg_water_temp',
        'avg_sal',
        'avg_do',
        'spp_count',
        "[SPECIES_CODE]_YOY",
        "[SPECIES_CODE]_adults",
        "[SPECIES_CODE]_total",
        "[SPECIES_CODE]_avg_total",
    ]

    descr_eng = [
        "unique identifier of sample",
        "year of observation",
        "month of observation",
        "day of observation",
        "province",
        "name of site and province",
        "camp station",
        "station latitude (decimal degrees)",
        "station longitude (decimal degrees)",
        "sample start date/time",
        "sample end date/time",
        "ammonia",
        "dissolved oxygen",
        "nitrates",
        "nitrite",
        "phosphate",
        "salinity",
        "silicate",
        "water temperature (degrees C)",
        "gravel (%)",
        "mud (%)",
        "rock (%)",
        "sand (%)",
        "species code",
        "ITIS taxonomic serial number (TSN)",
        "Is the species submerged aquatic vegetation (SAV)?",
        "SAV level observed",
        "count of adults",
        "count of young-of-the-year",
        "total number of individuals observed",
        "total (SAV and non-SAV)",
        "number of samples collected at the station in that year",
        "average water temperature (degrees C) at station",
        "average salinity at station",
        "average dissolved oxygen (mg/L) at station",
        "number of species observed",
        "count of the young-of-the-year for a given species",
        "count of the adults for a given species",
        "count of all individuals for a given species",
        "average number of individuals (per sample) for a given species",
    ]
    descr_fra = [
        "identifiant unique de l'échantillon",
        "l'année de l’observation",
        "le mois de l’observation",
        "le jour de l’observation",
        "province",
        "site de PSCA",
        "station de PSCA",
        "latitude de la station (degrés décimaux)",
        "longitude de la station (degrés décimaux)",
        "date / heure de début",
        "date / heure de fin",
        "ammoniac",
        "oxygène dissous",
        "nitrates",
        "nitrite",
        "phosphate",
        "salinité",
        "silicate",
        "température de l'eau (degrés C)",
        "gravier (%)",
        "boue (%)",
        "roche (%)",
        "sable (%)",
        "code de l'espèce",
        "numéro de série taxonomique ITIS (TSN)",
        "l'espèce est-elle une végétation aquatique submergée (VAS)?",
        "VAS niveau observé",
        "nombre d’adultes",
        "nombre de jeunes de l'année",
        "nombre total d'individus observés",
        "total (VAS et non-VAS)",
        "nombre d'échantillons recueillis à la station pour cette année",
        "température moyenne de l'eau (degrés C) à la station",
        "salinité moyenne à la station",
        "oxygène dissous (mg / L) à la station",
        "nombre d'espèces observées",
        "nombre de jeunes de l'année pour une espèce donnée",
        "nombre d'adultes pour une espèce donnée",
        "nombre total pour une espèce donnée",
        "nombre moyen d'individus (par échantillon) pour une espèce donnée",
    ]

    writer.writerow(header)

    for i in range(0, len(field_names)):
        writer.writerow([
            field_names[i],
            descr_eng[i],
            descr_fra[i],
        ])

    return response

#
# def generate_open_data_ver_2_dict():
#     """
#     Generates the data dictionary for open data report version 2
#     """
#
#     filename = "open_data_ver2_data_dictionary.csv"
#
#     # Create the HttpResponse object with the appropriate CSV header.
#     response = HttpResponse(content_type='text/csv')
#     response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
#     response.write(u'\ufeff'.encode('utf8'))  # BOM (optional...Excel needs it to open UTF-8 file properly)
#     writer = csv.writer(response)
#
#     # write the header
#     header = [
#         "name__nom",
#         "description_en",
#         "description_fr",
#     ]
#     writer.writerow(header)
#
#     field_names = [
#         'year',
#         'site_name',
#         'station_name',
#         'station_latitude',
#         'station_longitude',
#         'number_of_samples',
#         'avg_water_temp',
#         'avg_sal',
#         'avg_do',
#         "[SPECIES_CODE]_YOY",
#         "[SPECIES_CODE]_adults",
#         "[SPECIES_CODE]_total",
#     ]
#
#     descr_eng = [
#         "sample year",
#         "name of site and province",
#         "name of sampling station",
#         "station latitude (decimal degrees)",
#         "station longitude (decimal degrees)",
#         "number of samples collected at the station in that year",
#         "average water temperature (degrees C) at station",
#         "average salinity at station",
#         "average dissolved oxygen (mg/L) at station",
#         "average count of the young-of-the-year for a given species",
#         "average count of the adults for a given species",
#         "average count of all individuals for a given species",
#     ]
#     descr_fra = [
#         "année-échantillon",
#         "nom du site et de la province",
#         "nom de la station",
#         "latitude de la station (degrés décimaux)",
#         "longitude de la station (degrés décimaux)",
#         "nombre d'échantillons recueillis à la station pour cette année",
#         "température moyenne de l'eau (degrés C) à la station",
#         "salinité moyenne à la station",
#         "oxygène dissous (mg / L) à la station",
#         "nombre moyen de jeunes de l'année pour une espèce donnée",
#         "nombre moyen d'adultes pour une espèce donnée",
#         "nombre moyen d'individus pour une espèce donnée",
#     ]
#
#     for i in range(0, len(field_names)):
#         writer.writerow([
#             field_names[i],
#             descr_eng[i],
#             descr_fra[i],
#         ])
#     return response
