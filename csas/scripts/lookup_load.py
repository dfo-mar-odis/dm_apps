from csas import models


def load_lookup(src_file, model):
    print("{} : {}".format(src_file, model))

    print(model.objects.all())
    file = open(src_file)

    # skip the header line
    file.readline()

    # format:
    # old_id    new_id  english french
    for l in file:
        vals = l.strip('\n').split("\t")
        # load the table using the new_id, if it already exists then it's already in the table
        # later, when the data is loaded, the old_id is matched to the new_id and values in the data will be
        # replaced with the proper lookup reference
        print(vals)

        # check if id already exists
        if not model.objects.filter(pk=vals[0]) and not model.objects.filter(name=vals[1]):
            model(pk=vals[0], name=vals[2], nom=vals[3]).save()


print(models.SecSector.objects.all())

load_lookup(r"csas\scripts\data\main_csas_sectors.tsv", models.SecSector)
load_lookup(r"csas\scripts\data\main_csas_contact_types.tsv", models.ConContact)