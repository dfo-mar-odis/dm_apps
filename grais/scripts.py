from django.db.models import Q

from .import models


def fix_categories():
    '''
    for years 2006 to 2016, the assigned percentages on surfacespecies needs to be fixed.

    .20  -> .125
    .40 -> .375
    .60 -> .625
    .80 -> .875

    '''
    for sample in models.Sample.objects.filter(season__range=[2006,2016]):
        for line in sample.lines.all():
            for surface in line.surfaces.all():
                for obs in surface.surface_spp.all():
                    obs.notes = obs.notes.replace("20%","12.5%").replace("40%","37.5%").replace("60%","62.5%").replace("80%","87.5%")
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



