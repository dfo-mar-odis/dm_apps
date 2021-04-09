from django.db.models import Q
from django.template.defaultfilters import date
from django.urls import reverse
from django.utils.translation import activate

from . import models


def fix_metadata():
    # species
    for obj in models.Species.objects.all():
        obj.created_by = obj.last_modified_by
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # stations
    for obj in models.Station.objects.all():
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # samples
    for obj in models.Sample.objects.all():
        obj.created_at = obj.last_modified
        obj.updated_at = obj.last_modified
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # sample notes
    for obj in models.SampleNote.objects.all():
        obj.created_at = obj.date
        obj.updated_at = obj.date
        obj.created_by = obj.author
        obj.updated_by = obj.author
        obj.save()

    # lines
    for obj in models.Line.objects.all():
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # surfaces
    for obj in models.Surface.objects.all():
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # surfacespp
    for obj in models.SurfaceSpecies.objects.all():
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # incidental reports
    for obj in models.IncidentalReport.objects.all():
        obj.created_at = obj.date_last_modified
        obj.updated_at = obj.date_last_modified
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # gc samples
    for obj in models.GCSample.objects.all():
        obj.created_at = obj.last_modified
        obj.updated_at = obj.last_modified
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()

    # catch
    for obj in models.GCSample.objects.all():
        obj.created_by = obj.last_modified_by
        obj.updated_by = obj.last_modified_by
        obj.save()



def fix_categories():
    '''
    for years 2006 to 2016, the assigned percentages on surfacespecies needs to be fixed.

    .20  -> .125
    .40 -> .375
    .60 -> .625
    .80 -> .875

    '''
    for sample in models.Sample.objects.filter(season__range=[2006, 2016]):
        for line in sample.lines.all():
            for surface in line.surfaces.all():
                for obs in surface.surface_spp.all():
                    obs.notes = obs.notes.replace("20%", "12.5%").replace("40%", "37.5%").replace("60%", "62.5%").replace("80%", "87.5%")
                    if obs.percent_coverage == 0.2:
                        obs.percent_coverage = .125
                    elif obs.percent_coverage == 0.4:
                        obs.percent_coverage = .375
                    elif obs.percent_coverage == 0.6:
                        obs.percent_coverage = .625
                    elif obs.percent_coverage == 0.8:
                        obs.percent_coverage = .875
                    obs.save()


def resave_all():
    for obj in models.GCSample.objects.all():
        obj.save()


def reverse_cond():
    '''
    for seasons 2016, 2014 and 2013 sp_cond_ms and spc_ms are reversed. This function will undo the reversal
    :return: None
    '''
    pass
    # my_probe_qs = models.ProbeMeasurement.objects.filter(Q(sample__season=2016)|Q(sample__season=2014)|Q(sample__season=2013))
    # for probe in my_probe_qs:
    #     # print("sp_cond_ms={}; spc_ms={}".format(
    #     #     probe.sp_cond_ms,
    #     #     probe.spc_ms,
    #     # ))
    #     temp = probe.sp_cond_ms
    #     probe.sp_cond_ms = probe.spc_ms
    #     probe.spc_ms = temp
    #     probe.save()
    #     # print("sp_cond_ms={}; spc_ms={}".format(
    #     #     probe.sp_cond_ms,
    #     #     probe.spc_ms,
    #     # ))


def reconcile_spp():
    '''do not run this twice!!! I am greying out for safe-keeping'''
    # trap_id, number_to_add, species_id
    # crab_list = [
    #     [1501, 3, 26, ],
    #     [1499, 3, 26, ],
    #     [1295, 6, 26, ],
    #     [1278, 16, 26, ],
    #     [1296, 17, 26, ],
    #     [1323, 18, 26, ],
    #     [1283, 23, 26, ],
    #     [1351, 26, 26, ],
    #     [1317, 35, 26, ],
    #     [1294, 36, 26, ],
    #     [1324, 44, 26, ],
    #     [1259, 75, 26, ],
    #     [1190, 2, 27, ],
    #     [985, 1, 98, ],
    #     [1038, 1, 98, ],
    #     [1045, 1, 98, ],
    #     [1058, 1, 98, ],
    #     [1173, 1, 98, ],
    #     [1361, 1, 98, ],
    #     [930, 2, 98, ],
    #     [938, 2, 98, ],
    #     [970, 2, 98, ],
    #     [983, 2, 98, ],
    #     [1094, 2, 98, ],
    #     [1015, 4, 98, ],
    #     [1201, 4, 98, ],
    #     [1221, 4, 98, ],
    #     [1165, 5, 98, ],
    #     [1386, 5, 98, ],
    #     [1054, 6, 98, ],
    #     [1047, 7, 98, ],
    #     [1138, 7, 98, ],
    #     [1043, 8, 98, ],
    #     [1381, 8, 98, ],
    #     [966, 9, 98, ],
    #     [1142, 10, 98, ],
    #     [1213, 10, 98, ],
    #     [1370, 10, 98, ],
    #     [1385, 10, 98, ],
    #     [1025, 11, 98, ],
    #     [1149, 11, 98, ],
    #     [1374, 11, 98, ],
    #     [1011, 12, 98, ],
    #     [1022, 18, 98, ],
    #
    # ]
    # for crab in crab_list:
    #     my_trap = models.Trap.objects.get(pk=crab[0])
    #     number_to_add = crab[1]
    #     for i in range(0, number_to_add):
    #         print("adding species {} to trap {}".format(crab[2], crab[0]))
    #         my_crab = models.Crab.objects.create(trap=my_trap, species_id=crab[2])
    #         my_crab.save()
    pass


def print_list_of_duplicates():
    years = [item["season"] for item in models.Sample.objects.order_by("season").values("season").distinct()]
    stations = models.Station.objects.all()
    for year in years:
        for station in stations:
            sample_qs = models.Sample.objects.filter(season=year, station=station)

            if sample_qs.count() > 1:
                for s in sample_qs:
                    print(f'{s.id};{s.season};{s.station.station_name};{date(s.date_deployed)};{date(s.date_retrieved)}')


def print_notes():
    activate('en')
    print("SAMPLE NOTES")
    print(f'sample_id|note_id|date|author|note|url')
    for n in models.SampleNote.objects.order_by("sample_id"):
        note = n.note.replace("\r\n", "; ")
        print(f'{n.sample_id}|{n.id}|{n.date.strftime("%Y-%m-%d")}|{n.author}|{note}|http://dmapps{reverse("grais:sample_detail", args=[n.sample_id])}')

    print("")
    print("")
    print("LINE NOTES")
    print(f'sample_id|line_id|date|author|notes|url')
    for l in models.Line.objects.filter(notes__isnull=False).filter(~Q(notes="")).order_by("sample_id"):
        note = l.notes.replace("\r\n", "; ")
        print(f'{l.sample.id}|{l.id}|{note}|http://dmapps{reverse("grais:line_detail", args=[l.id])}')

    print("")
    print("")
    print("SURFACE NOTES")
    print(f'sample_id|surface_id|note_id|notes|url')
    for s in models.Surface.objects.filter(notes__isnull=False).filter(~Q(notes="")).order_by("line__sample_id"):
        note = s.notes.replace("\r\n", "; ")
        print(f'{s.line.sample.id}|{s.id}|{note}|http://dmapps{reverse("grais:surface_detail", args=[s.id])}')


def print_bad_surfaces():
    activate('en')
    surfaces = models.Surface.objects.all()
    print(f'surface_id|total_coverage|url')
    for s in surfaces:
        coverage = s.total_coverage
        if coverage and coverage > 1:
            print(f'{s.id}|{coverage}|http://dmapps{reverse("grais:surface_detail", args=[s.id])}')


