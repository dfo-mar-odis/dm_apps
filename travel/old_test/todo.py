# TODO: warnings should be sent when trip costs mount above 10000 CAD
# TODO: trip requests must always have a fiscal year after saving
# TODO: make sure that the correct permissions are enforced with respect to editing a trip (both for adm and non-adm)

# TODO: can never have two requests for the same trip with the same traveller; taking into account both the individual and group requests
# TODO: should never be able to submit a trip request for a trip that is not "opened"
# TODO: and adm reviewer should have the reviewer tab show up on the main page if a trip is awaiting their approval

# TODO: when a trip is cancelled, associated trips should also be cancelled
# TODO: when a trip is being re-assigned, if should only be able to be reassigned by an adm admin if adm-approval-required
# TODO: ... all trip requests under the trip should be successfully moved.
# TODO: ... should not be able to merge the trips if there is an overlap of travellers.

# TODO: IMPORTANT... check to see that the correct trips are being caught by the ADM filter... one good test would be to ensure that a trip shows up only when it has an associated active tr

# TODO: reset reviewers!!
# TripRequestReviewerADMUpdateView
# Create a test for the closest date function!!