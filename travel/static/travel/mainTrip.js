Vue.component('v-select', VueSelect.VueSelect);
var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    currentUser: {},
    dmAppsUsers: [],
    errorMsgReviewer: null,
    isReview: isReview,  // declared in template SCRIPT tag
    loading: true,
    loading_user: false,
    loadingDMAppsUsers: false,
    trip: {},
    reviewerEditMode: false,
    tripLabels: {},
    reviewerLabels: {},
    helpText: {},
    roleChoices: [],
    showAdminNotesForm: false,
    travellerLabels: {},
    requestLabels: {},
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
    getDeadlineClass(days) {
      let myStr = 'px-1 py-1 ';
      if (days) {
        if (days > 45) myStr += 'bg-success text-light';
        else if (days >= 15) myStr +=  'bg-warning';
        else myStr += 'bg-danger text-light';
      }
      return myStr;
    },
    addTraveller() {
    }, // being added for the sake of compatibility,
    addReviewer() {
      this.trip.reviewers.push({
        trip: this.trip.id,
        order: this.trip.reviewers.length + 1,
        role: null,
        status: 23,  // this will be updated by the model save method. setting status == 4 just allows to show in list
      })
    },
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
    getHelpText() {
      let endpoint = `/api/travel/help-text/`;
      apiService(endpoint).then(data => {
        this.helpText = data;
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
    getRequestMetadata() {
      let endpoint = `/api/travel/meta/models/request/`;
      apiService(endpoint).then(data => {
        this.requestLabels = data.labels;
      });
    },
    getTripMetadata() {
      let endpoint = `/api/travel/meta/models/trip/`;
      apiService(endpoint).then(data => {
        this.tripLabels = data.labels;
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
        console.log(reviewer)
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
  },
  filters: {
    floatformat: function (value, precision = 2) {
      if (!value) return '---';
      value = value.toLocaleString(undefined, {
        minimumFractionDigits: precision,
        maximumFractionDigits: precision
      });
      return value
    },
    zero2NullMark: function (value) {
      if (!value || value === "0.00" || value == 0) return '---';
      return value
    },
    nz: function (value, arg = "---") {
      if (value === null || value === "") return arg;
      return value
    },
    yesNo: function (value) {
      if (value == null || value == false || value == 0) return 'No';
      return "Yes"
    },
    percentage: function (value, decimals) {
      // https://gist.github.com/belsrc/672b75d1f89a9a5c192c
      if (!value) {
        value = 0;
      }

      if (!decimals) {
        decimals = 0;
      }
      value = value * 100;
      value = Math.round(value * Math.pow(10, decimals)) / Math.pow(10, decimals);
      value = value + '%';
      return value;
    }
  },
  computed: {
    travellers() {
      if (this.trip) return this.trip.travellers;
    },
    reviewers() {
      if (this.trip) return this.trip.reviewers;
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

    canModify() {
      if (this.currentUser && this.currentUser.can_modify) {
        return this.currentUser.can_modify;
      }
      return false;
    },
    isOwner() {
      if (this.currentUser && this.currentUser.is_owner) {
        return this.currentUser.is_owner;
      }
      return false;
    },
    isRegionalAdmin() {
      if (this.currentUser) {
        return this.currentUser.is_regional_admin;
      }
      return false;
    },
    isNCRAdmin() {
      if (this.currentUser) {
        return this.currentUser.is_ncr_admin;
      }
      return false;
    },
    isAdmin() {
      return this.isNCRAdmin; // being adding in for compatibility with reviewer form
    },
    canModify() {
      return this.isNCRAdmin || (this.isRegionalAdmin && !this.trip.is_adm_approval_required)
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