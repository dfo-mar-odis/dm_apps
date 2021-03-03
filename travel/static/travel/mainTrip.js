Vue.component('v-select', VueSelect.VueSelect);
var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    currentUser: {},
    dmAppsUsers: [],
    errorMsgReviewer: null,
    helpText: {},
    isReview: isReview,  // declared in template SCRIPT tag
    loading: true,
    loading_user: false,
    loadingDMAppsUsers: false,
    requestLabels: {},
    reviewerEditMode: false,
    reviewerLabels: {},
    roleChoices: [],
    showAdminNotesForm: false,
    travellerLabels: {},
    trip: {},
    tripLabels: {},
    yesNoChoices: yesNoChoices,

    // these are just being added for the sake of compatibility
    request: null,
    travellerToEdit: null,
    costLabels: {},
    inCostEditMode: false,
    loading_costs: false,
    errorMsgCost: null,

  },
  methods: {
    addReviewer() {
      this.trip.reviewers.push({
        trip: this.trip.id,
        order: this.trip.reviewers.length + 1,
        role: null,
        status: 23,  // this will be updated by the model save method. setting status == 4 just allows to show in list
      })
    },
    addTraveller() {
    }, // being added for the sake of compatibility,
    closeReviewerForm() {
      this.getTrip();
      this.reviewerEditMode = false;
    },
    collapseTravellers() {
      for (var i = 0; i < this.trip.travellers.length; i++) this.trip.travellers[i].show_me = false;
      this.$forceUpdate()
    },
    deleteReviewer(reviewer) {
      if (reviewer.id) {
        userInput = confirm(deleteReviewerMsg);
        if (userInput) {
          let endpoint = `/api/travel/trip-reviewers/${reviewer.id}/`;
          apiService(endpoint, "DELETE")
              .then(response => {
                this.$delete(this.trip.reviewers, this.trip.reviewers.indexOf(reviewer))
              })
        }
      } else {
        this.$delete(this.trip.reviewers, this.trip.reviewers.indexOf(reviewer))
      }
    },
    deleteTraveller(traveller) {
      var userInput = false;
      userInput = prompt(travellerDeleteMsg);
      if (userInput === true || userInput.toLowerCase() === "yes" || userInput.toLowerCase() === "oui") {
        let endpoint = `/api/travel/travellers/${traveller.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              console.log(response);
              this.getTrip();
            })
      }
    },
    cherryPickTraveller(traveller) {
      var userInput = false;
      userInput = prompt(travellerCherryPickMsg);
      if (userInput === true || userInput.toLowerCase() === "yes" || userInput.toLowerCase() === "oui") {
        let endpoint = `/api/travel/travellers/${traveller.id}/?cherry_pick_approval=true`;
        apiService(endpoint, "POST")
            .then(response => {
              console.log(response);
              this.getTrip();
            })
      }
    },
    enablePopovers() {
      $('[data-toggle="popover"]').popover({html: true});
    },
    expandTravellers() {
      for (var i = 0; i < this.trip.travellers.length; i++) this.trip.travellers[i].show_me = true;
      this.$forceUpdate()
    },
    fetchDMAppsUsers() {
      this.loadingDMAppsUsers = true;
      let endpoint = `/api/shared/users/?page_size=50000`;
      apiService(endpoint).then(data => {
        this.dmAppsUsers = data.results;
        this.dmAppsUsers.unshift({full_name: "-----", id: null})
        this.loadingDMAppsUsers = false;
      });
    },
    getCurrentUser(trip) {
      this.loading_user = true;
      let endpoint = `/api/travel/user/?trip=${trip.id}`;
      apiService(endpoint)
          .then(response => {
            this.loading_user = false;
            this.currentUser = response;
          })
    },
    getDeadlineClass(days) {
      let myStr = 'px-1 py-1 ';
      if (days) {
        if (days > 45) myStr += 'bg-success text-light';
        else if (days >= 15) myStr += 'bg-warning';
        else myStr += 'bg-danger text-light';
      }
      return myStr;
    },
    getHelpText() {
      let endpoint = `/api/travel/help-text/`;
      apiService(endpoint).then(data => {
        this.helpText = data;
      });
    },
    getRequestMetadata() {
      let endpoint = `/api/travel/meta/models/request/`;
      apiService(endpoint).then(data => {
        this.requestLabels = data.labels;
      });
    },
    getReviewerMetadata() {
      let endpoint = `/api/travel/meta/models/trip-reviewer/`;
      apiService(endpoint).then(data => {
        this.reviewerLabels = data.labels;
        this.roleChoices = data.role_choices;
      });
    },
    getTravellerMetadata() {
      let endpoint = `/api/travel/meta/models/traveller/`;
      apiService(endpoint).then(data => {
        this.travellerLabels = data.labels;
        this.travellerRoleChoices = data.role_choices;
        this.orgChoices = data.org_choices;
      });
    },
    getTrip() {
      this.loading = true;
      let endpoint = `/api/travel/trips/${tripId}/`;
      apiService(endpoint)
          .then(response => {
            this.loading = false;
            this.trip = response;
            // if there is one traveller, we should have that traveller on display
            if (this.trip.travellers.length === 1) {
              this.trip.travellers[0].show_me = true;
            }
            this.getCurrentUser(response);
            this.$nextTick(() => {
              // enable popovers everywhere
              $('[data-toggle="popover"]').popover({html: true});
            })
          })
    },
    getTripMetadata() {
      let endpoint = `/api/travel/meta/models/trip/`;
      apiService(endpoint).then(data => {
        this.tripLabels = data.labels;
      });
    },
    goRequestDetail(request) {
      let url = `/travel-plans/requests/${request.id}/view/`;
      let win = window.open(url, '_blank');
    },
    groomJSON(json) {
      return JSON.stringify(json).replaceAll("{", "").replaceAll("}", "").replaceAll("[", " ").replaceAll("]", " ").replaceAll('"', "").replaceAll("non_field_errors:", "")
    },
    moveReviewer(reviewer, direction) {
      if (direction === 'up') reviewer.order -= 1.5;
      else if (direction === 'down') reviewer.order += 1.5;
      this.trip.reviewers.sort((a, b) => {
        if (a["order"] < b["order"]) return -1
        if (a["order"] > b["order"]) return 1
      });
      // reset the order numbers based on position in array
      for (var i = 0; i < this.trip.reviewers.length; i++) {
        r = this.trip.reviewers[i]
        if (r.status === 4 || r.status === 20) r.order = i;
        else r.order = i - 1000;
        this.updateReviewer(this.trip.reviewers[i])
      }
    },
    resetReviewers() {
      this.errorMsgReviewer = null
      userInput = confirm(tripReviewerResetMsg)
      if (userInput) {
        let endpoint = `/api/travel/trips/${this.trip.id}/?reset_reviewers=true`;
        apiService(endpoint, "POST", this.trip)
            .then(() => {
              this.getTrip();
            })
      }
    },
    skipReviewer(reviewer) {
      userInput = prompt(skipReviewerMsg);
      if (userInput) {
        reviewer.comments = userInput;
        let endpoint = `/api/travel/trip-reviewers/${reviewer.id}/?skip=true`;
        apiService(endpoint, "PUT", reviewer)
            .then(response => {
              if (response.id) {
                this.getTrip();
              } else {
                console.log(response)
                this.errorMsgReviewer = this.groomJSON(response)
              }
            })
      }
    },
    toggleShowMe(obj) {
      obj.show_me = !obj.show_me;
      this.$forceUpdate();
    },
    updateReviewer(reviewer) {
      this.errorMsgReviewer = null;
      if (reviewer.id) {
        let endpoint = `/api/travel/trip-reviewers/${reviewer.id}/`;
        apiService(endpoint, "PUT", reviewer)
            .then(response => {
              if (response.id) {
                reviewer = response;
                this.errorMsgReviewer = null;
              } else {
                console.log(response)
                this.errorMsgReviewer = this.groomJSON(response)
              }

            })
      } else {
        let endpoint = `/api/travel/trip-reviewers/`;
        apiService(endpoint, "POST", reviewer)
            .then(response => {
              console.log(response)
              if (response.id) {
                this.$delete(this.trip.reviewers, this.trip.reviewers.indexOf(reviewer))
                this.trip.reviewers.push(response)
                this.errorMsgReviewer = null;
              } else {
                this.errorMsgReviewer = this.groomJSON(response)
              }
            })
      }
    },
    updateTripAdminNotes() {
      if (this.canModify) {
        let endpoint = `/api/travel/trips/${tripId}/`;
        apiService(endpoint, "PATCH", {admin_notes: this.trip.admin_notes})
            .then(response => {
              this.getTrip()
              this.showAdminNotesForm = false;
            })
      }
    },
    canCherryPick(traveller) {
      // if their request status is 14 &&  they are ADM && they are the active reviewer
      return this.isADM && this.isCurrentReviewer && traveller.request_obj.status == 14;
    },
    reviewSubmit() {
      let userInput = false;
      if (!this.isADM) userInput = true;
      else userInput = prompt(approveAllTravellersMsg);

      if (userInput === true || userInput.toLowerCase() === "yes" || userInput.toLowerCase() === "oui") {
        $("#my_form").submit()
      }
    }
  },
  computed: {
    canModify() {
      return this.isNCRAdmin || (this.isRegionalAdmin && !this.trip.is_adm_approval_required) || this.isCurrentReviewer
    },
    editableReviewers() {
      myArray = []
      for (var i = 0; i < this.trip.reviewers.length; i++) {
        if (this.trip.reviewers[i].status === 23 || this.request.reviewers[i].status === 24) {
          myArray.push(this.trip.reviewers[i]);
        }
      }
      return myArray
    },
    isAdmin() {
      return this.isNCRAdmin; // being adding in for compatibility with reviewer form
    },
    isNCRAdmin() {
      return this.currentUser && this.currentUser.is_ncr_admin;
    },
    isOwner() {
      return this.currentUser && this.currentUser.is_owner;
    },
    isCurrentReviewer() {
      return this.currentUser && this.currentUser.is_current_reviewer;
    },
    isADM() {
      return this.currentUser && this.currentUser.is_adm;
    },
    isRegionalAdmin() {
      return this.currentUser && this.currentUser.is_regional_admin;
    },
    reviewers() {
      if (this.trip) return this.trip.reviewers;
    },
    travellerColClass() {
      if (this.canModify && !this.isReview && !this.trip) return 'col-4';
      else return 'col';
    },
    travellers() {
      if (this.trip) return this.trip.travellers;
    },
  },
  created() {
    this.getTrip();
    this.fetchDMAppsUsers();
    this.getTripMetadata();
    this.getRequestMetadata();
    this.getReviewerMetadata();
    this.getTravellerMetadata();
    this.getHelpText();
  },
  mounted() {
  },
});
