from travel import models as travel_models
from shared_models import models as shared_models
from django.contrib.auth import models as auth_models

update_trips = [173]

# Flag each trip in update_trips as is_adm_approval_required = true
trips = travel_models.Conference.objects.filter(pk__in=update_trips)
print(trips.count())
for trip in trips:
    trip.is_adm_approval_required = 1
    trip.save()

# only make adjustments to travel requests in the maritime region. Let Other regions do their own thing.
mar_region = shared_models.Region(pk=2)

# Get travel request related to update_trips
travels = travel_models.TripRequest.objects.filter(trip_id__in=trips, region=mar_region)
print(travels.count())

adm_approver = auth_models.User.objects.get(pk=626)
adm_role = travel_models.ReviewerRole.objects.get(name='ADM')
adm_status = travel_models.Status.objects.get(pk=20) # 20 is currently 'Queued'

rdg_approver = auth_models.User.objects.get(pk=801)

# Check each travel requests' review list
for t in travels:
    # If user 626 (Arran McPherson) isn't present,
    if not t.reviewers.filter(user=adm_approver):
        print("\nNo ADM approver - {}".format(t))
        print("\nOld Approver list:")
        for r in t.reviewers.order_by('order'):
            print("{} - {}".format(r.order, r.user))
        #   Add one to the order for user 801  (Mary-Ellen Valkenier)
        #   Add user 626 before user 801 (Mary-Ellen Valkenier)

        if t.reviewers.filter(user=rdg_approver):
            rdg = t.reviewers.get(user=rdg_approver)
            pos = rdg.order
            rdg.order = pos + 1
            rdg.save()

            rev = travel_models.Reviewer(order=pos, role=adm_role, status=adm_status, user=adm_approver, trip_request=t)
            rev.save()

            print("\nNew Approver list:")
            for r in t.reviewers.order_by('order'):
                print("{} - {}".format(r.order, r.user))
            #   Add one to the order for user 801  (Mary-Ellen Valkenier)
            #   Add user 626 before user 801 (Mary-Ellen Valkenier)
        else:
            print("No RDG approver for {}".format(t.id))

