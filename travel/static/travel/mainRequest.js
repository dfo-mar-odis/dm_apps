Vue.component('v-select', VueSelect.VueSelect);
var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    clean: true,
    cloningTraveller: false,
    costChoices: [],
    costLabels: {},
    currentUser: {},
    dmAppsUsers: [],
    errorMsgCost: null,
    errorMsgReviewer: null,
    errorMsgTraveller: null,
    fileLabels: {},
    fileToUpload: null,
    firstTravellerMsg: null,
    helpText: {},
    inCostEditMode: false,
    inFileEditMode: false,
    isReview: isReview,  // declared in template SCRIPT tag
    loading: true,
    loading_costs: false,
    loading_reviewers: false,
    loading_user: false,
    loadingDMAppsUsers: false,
    orgChoices: [],
    request: {},
    requestLabels: {},
    reviewerEditMode: false,
    reviewerLabels: {},
    roleChoices: [],
    showAdminNotesForm: false,
    travellerLabels: {},
    travellerRoleChoices: [],
    travellerToEdit: null,
    yesNoChoices: yesNoChoices,

    // these are just being added for the sake of compatibility
    trip: null,
  },
  methods: {
    addAllCosts(traveller) {
      let endpoint = `/api/travel/travellers/${traveller.id}/?populate_all_costs=true`;
      apiService(endpoint, "POST")
          .then(response => {
            this.refreshCosts(traveller);
          })
    },
    addAttachment() {
      this.inFileEditMode = true;
      this.request.files.push({
        request: this.request.id,
        name: null,
        file: null,
        editMode: true,
      })
    },
    addCost(traveller) {
      this.inCostEditMode = true;
      traveller.costs.push({
        traveller: traveller.id,
        rate_cad: null,
        number_of_days: null,
        amount_cad: 0,
        editMode: true,
      })
    },
    addReviewer() {
      this.request.reviewers.push({
        request: this.request.id,
        order: this.request.reviewers.length + 1,
        role: null,
        status: 4,  // this will be updated by the model save method. setting status == 4 just allows to show in list
      })
    },
    addTraveller(clonedtraveller) {
      let newTraveller;
      if (!clonedtraveller.id) {
        newTraveller = {
          request: this.request.id,
          start_date: this.request.trip.start_date,
          end_date: this.request.trip.end_date,
          user: '',
          name: null,
          file: null,
          editMode: true,
          non_dfo_costs: 0,
          is_public_servant: true,
          is_research_scientist: false,
          learning_plan: false,
        };
      } else {
        this.cloningTraveller = true;
        newTraveller = JSON.parse(JSON.stringify(clonedtraveller));
        newTraveller.start_date = newTraveller.start_date.split("T")[0];
        newTraveller.end_date = newTraveller.end_date.split("T")[0];
        newTraveller.old_name = clonedtraveller.smart_name;
        newTraveller.old_id = newTraveller.id;
        delete newTraveller.id
      }
      this.request.travellers.push(newTraveller);
      this.travellerToEdit = this.request.travellers[this.request.travellers.length - 1];
      this.$nextTick(() => {
        this.$refs.traveller_form_starting_point.focus()
      })
    },
    cancelTravellerEdit() {
      this.getRequest();
      this.travellerToEdit = null;
      this.cloningTraveller = false;
      this.firstTravellerMsg = null;
    },

    clearEmptyCosts(traveller) {
      let endpoint = `/api/travel/travellers/${traveller.id}/?clear_empty_costs=true`;
      apiService(endpoint, "POST")
          .then(response => {
            console.log(response);
            this.refreshCosts(traveller);
          })
    },
    closeReviewerForm() {
      this.getRequest();
      this.reviewerEditMode = false;
    },
    collapseTravellers() {
      for (var i = 0; i < this.request.travellers.length; i++) this.request.travellers[i].show_me = false;
      this.$forceUpdate()
    },
    costCloseEditMode(traveller, cost) {
      this.inCostEditMode = false;
      if (!cost.id) {
        // remove from array
        this.$delete(traveller.costs, traveller.costs.indexOf(cost))
      } else {
        cost.editMode = false;
        this.refreshCosts(traveller)
      }
    },
    deleteCost(traveller, cost) {
      userInput = confirm(deleteCostMsg);
      if (userInput) {
        let endpoint = `/api/travel/costs/${cost.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              this.$delete(traveller.costs, traveller.costs.indexOf(cost));
              this.updateTotalCost(traveller);
            })
      }
    },
    deleteFile(file) {
      userInput = confirm(deleteFileMsg);
      if (userInput) {
        let endpoint = `/api/travel/request-files/${file.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              this.$delete(this.request.files, this.request.files.indexOf(file))
            })
      }
    },
    deleteReviewer(reviewer) {
      if (reviewer.id) {
        userInput = confirm(deleteReviewerMsg);
        if (userInput) {
          let endpoint = `/api/travel/request-reviewers/${reviewer.id}/`;
          apiService(endpoint, "DELETE")
              .then(response => {
                this.$delete(this.request.reviewers, this.request.reviewers.indexOf(reviewer))
              })
        }
      } else {
        this.$delete(this.request.reviewers, this.request.reviewers.indexOf(reviewer))
      }
    },
    deleteTraveller(traveller) {
      var userInput = false;
      if (this.request.status === 8) userInput = confirm(travellerDeleteMsgLITE);
      else userInput = prompt(travellerDeleteMsg);
      if (userInput === true || userInput.toLowerCase() === "yes" || userInput.toLowerCase() === "oui") {
        let endpoint = `/api/travel/travellers/${traveller.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              console.log(response);
              this.getRequest();
            })
      }
    },
    editTraveller(traveller) {
      this.errorMsgTraveller = null;
      this.travellerToEdit = traveller;
      this.travellerToEdit.start_date = this.travellerToEdit.start_date.split("T")[0]
      this.travellerToEdit.end_date = this.travellerToEdit.end_date.split("T")[0]
      this.$nextTick(() => {
        this.$refs.traveller_form_starting_point.focus()
      })
    },
    enablePopovers() {
      $('[data-toggle="popover"]').popover({html: true});
    },
    expandTravellers() {
      for (var i = 0; i < this.request.travellers.length; i++) this.request.travellers[i].show_me = true;
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
    fileCloseEditMode(file) {
      this.inFileEditMode = false;
      if (!file.id) {
        // remove from array
        this.$delete(this.request.files, this.request.files.indexOf(file))
      } else {
        file.editMode = false;
        this.$forceUpdate()
      }
    },
    getCostMetadata() {
      let endpoint = `/api/travel/meta/models/cost/`;
      apiService(endpoint).then(data => {
        this.costLabels = data.labels;
        this.costChoices = data.cost_choices;
      });
    },
    getCurrentUser(request) {
      this.loading_user = true;
      let endpoint = `/api/travel/user/?request=${request.id}`;
      apiService(endpoint)
          .then(response => {
            this.loading_user = false;
            this.currentUser = response;
          })
    },
    getFileMetadata() {
      let endpoint = `/api/travel/meta/models/file/`;
      apiService(endpoint).then(data => {
        this.fileLabels = data.labels;
      });
    },
    getHelpText() {
      let endpoint = `/api/travel/help-text/`;
      apiService(endpoint).then(data => {
        this.helpText = data;
      });
    },
    getRequest() {
      this.loading = true;
      let endpoint = `/api/travel/requests/${tripRequestId}/`;
      apiService(endpoint)
          .then(response => {
            this.loading = false;
            this.request = response;
            // if there is one traveller, we should have that traveller on display
            if (this.request.travellers.length === 1) {
              this.request.travellers[0].show_me = true;
            } else if (this.request.status === 8) {
              for (var i = 0; i < this.request.travellers.length; i++) {
                this.request.travellers[i].show_me = true;
              }
            }
            this.getCurrentUser(response);

            // if this is being opened from the create form, AND there is a SINGLE traveller, we should be helpful and open up in edit mode
            // this will be singaled by there being a hash in the window location called "travellers_head"
            if (this.clean && window.location.hash === "#travellers_head" && this.request.travellers.length === 1) {
              this.travellerToEdit = this.request.travellers[0];
              this.firstTravellerMsg = firstTravellerMsg;
              this.clean = false;
              this.$nextTick(()=>{this.$refs["travellers_head"].focus()})
            }

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
    getReviewerMetadata() {
      let endpoint = `/api/travel/meta/models/request-reviewer/`;
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
    goTripDetail(trip) {
      let url = `/travel-plans/trips/${trip.id}/view/`;
      let win = window.open(url, '_blank');
    },
    groomJSON(json) {
      return JSON.stringify(json).replaceAll("{", "").replaceAll("}", "").replaceAll("[", " ").replaceAll("]", " ").replaceAll('"', "").replaceAll("non_field_errors:", "")
    },
    moveReviewer(reviewer, direction) {
      if (direction === 'up') reviewer.order -= 1.5;
      else if (direction === 'down') reviewer.order += 1.5;
      this.request.reviewers.sort((a, b) => {
        if (a["order"] < b["order"]) return -1
        if (a["order"] > b["order"]) return 1
      });
      // reset the order numbers based on position in array
      for (var i = 0; i < this.request.reviewers.length; i++) {
        r = this.request.reviewers[i]
        if (r.status === 4 || r.status === 20) r.order = i;
        else r.order = i - 1000;
        this.updateReviewer(this.request.reviewers[i])
      }
    },
    onFileChange(fileRef) {
      this.fileToUpload = this.$refs[fileRef][0].files[0];
    },
    refreshCosts(traveller) {
      this.loading_costs = true;
      let endpoint = `/api/travel/costs/?traveller=${traveller.id}`;
      apiService(endpoint)
          .then(response => {
            traveller.costs = response;
            this.loading_costs = false;
          })
    },
    resetReviewers() {
      this.errorMsgReviewer = null
      userInput = confirm(requestReviewerResetMsg)
      if (userInput) {
        let endpoint = `/api/travel/requests/${this.request.id}/?reset_reviewers=true`;
        apiService(endpoint, "POST", this.request)
            .then(() => {
              this.getRequest();
            })
      }
    },
    skipReviewer(reviewer) {
      userInput = prompt(skipReviewerMsg);
      if (userInput) {
        reviewer.comments = userInput;
        let endpoint = `/api/travel/request-reviewers/${reviewer.id}/?skip=true`;
        apiService(endpoint, "PUT", reviewer)
            .then(response => {
              if (response.id) {
                this.getRequest();
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
    updateCost(traveller, cost) {
      this.errorMsgCost = null;
      let endpoint;
      let method;
      if (cost.rate_cad === "") cost.rate_cad = null;
      if (cost.number_of_days === "") cost.number_of_days = null;
      if (!cost.id) {
        endpoint = `/api/travel/costs/`;
        method = "POST";
      } else {
        endpoint = `/api/travel/costs/${cost.id}/`;
        method = "PATCH";
      }
      apiService(endpoint, method, cost).then(response => {
        if (response.id) {
          if (traveller) {
            this.refreshCosts(traveller);
            this.updateTotalCost(traveller)
          }
          this.inCostEditMode = false;
        } else {
          this.errorMsgCost = this.groomJSON(response)
        }
      })
    },
    updateCostRowTotal(cost) {
      cost.amount_cad = Number(cost.number_of_days) * Number(cost.rate_cad);
    },
    updateFile(file) {
      // if there is a file attribute, delete it since we send back the file through a separate request
      if (file.file) delete file.file
      let endpoint1;
      let method1;
      if (!file.id) {
        endpoint1 = `/api/travel/request-files/`;
        method1 = "POST";
      } else {
        endpoint1 = `/api/travel/request-files/${file.id}/`;
        method1 = "PATCH";
      }
      apiService(endpoint1, method1, file).then(response => {
        if (response.id) {
          let endpoint2 = `/api/travel/request-files/${response.id}/`;
          fileApiService(endpoint2, "PATCH", "file", this.fileToUpload).then(response => {
            this.fileToUpload = null
          })
        } else console.log(response)
        // regardless, refresh everything!!
        this.getRequest();
        this.inFileEditMode = false;
      })
    },
    updateRequestAdminNotes() {
      if (this.currentUser.is_admin) {
        let endpoint = `/api/travel/requests/${tripRequestId}/`;
        apiService(endpoint, "PATCH", {admin_notes: this.request.admin_notes})
            .then(response => {
              this.getRequest()
              this.showAdminNotesForm = false;
            })
      }
    },
    updateReviewer(reviewer) {
      this.errorMsgReviewer = null;
      if (reviewer.id) {
        let endpoint = `/api/travel/request-reviewers/${reviewer.id}/`;
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
        let endpoint = `/api/travel/request-reviewers/`;
        apiService(endpoint, "POST", reviewer)
            .then(response => {
              console.log(response)
              if (response.id) {
                this.$delete(this.request.reviewers, this.request.reviewers.indexOf(reviewer))
                this.request.reviewers.push(response)
                this.errorMsgReviewer = null;
              } else {
                this.errorMsgReviewer = this.groomJSON(response)
              }
            })
      }
    },
    updateTotalCost(traveller) {
      let cost = 0;
      for (var i = 0; i < traveller.costs.length; i++) {
        cost += Number(traveller.costs[i].amount_cad);
      }
      traveller.total_cost = cost;
    },
    updateTraveller() {
      this.errorMsgTraveller = null;
      if (this.travellerToEdit.start_date) this.travellerToEdit.start_date += "T00:00:00.421977Z"
      if (this.travellerToEdit.end_date) this.travellerToEdit.end_date += "T00:00:00.421977Z"
      let endpoint;
      let method;
      if (!this.travellerToEdit.id) {
        endpoint = `/api/travel/travellers/`;
        method = "POST";
      } else {
        endpoint = `/api/travel/travellers/${this.travellerToEdit.id}/`;
        method = "PATCH";
      }
      apiService(endpoint, method, this.travellerToEdit).then(response => {
        if (response.id) {
          this.firstTravellerMsg = null;
          this.getRequest();
          if (this.cloningTraveller) {
            // start by removing all costs
            costs = this.travellerToEdit.costs // before this gets erased
            endpoint = `/api/travel/travellers/${response.id}/?clear_empty_costs=true`;
            apiService(endpoint, method, response).then(response1 => {
              let newCost;
              for (var i = 0; i < costs.length; i++) {
                newCost = JSON.parse(JSON.stringify(costs[i]));
                delete newCost.id;
                newCost.traveller = response.id;
                this.updateCost(null, newCost);
              }
            })
            // sorry, I am not proud about this...
            setTimeout(function () {
              this.getRequest()
            }.bind(this), 3000);
          }
          this.travellerToEdit = null;
        } else {
          if (this.travellerToEdit.start_date) this.travellerToEdit.start_date = this.travellerToEdit.start_date.split("T")[0]
          if (this.travellerToEdit.end_date) this.travellerToEdit.end_date = this.travellerToEdit.end_date.split("T")[0]
          console.log(response)
          this.errorMsgTraveller = this.groomJSON(response)
        }
      })
    },
    cherryPickTraveller() {
    }, // for compatibility
    canCherryPick() {
      return false;
    }
  },
  computed: {
    canModify() {
      return this.currentUser && this.currentUser.can_modify;
    },
    editableReviewers() {
      myArray = []
      for (var i = 0; i < this.request.reviewers.length; i++) {
        if (this.request.reviewers[i].status === 4 || this.request.reviewers[i].status === 20) {
          myArray.push(this.request.reviewers[i]);
        }
      }
      return myArray
    },
    isAdmin() {
      return this.currentUser && this.currentUser.is_admin;
    },
    isOwner() {
      return this.currentUser && this.currentUser.is_owner;
    },
    isTraveller() {
      return this.currentUser && this.currentUser.is_traveller;
    },
    reviewers() {
      if (this.request) return this.request.reviewers;
    },
    submitTip() {
      if (this.request.id) {
        if (this.request.is_late_request && !this.request.late_justification) return lateJustificationTip;
        else if (!this.request.submitted && !this.request.travellers.length) return noTravellersTip;
      }
    },
    travellerColClass() {
      if (this.canModify && !this.isReview && !this.trip) return 'col-4';
      else return 'col';
    },
    travellers() {
      if (this.request) return this.request.travellers;
    },
  },
  created() {
    this.getRequest();
    this.fetchDMAppsUsers();
    this.getRequestMetadata();
    this.getReviewerMetadata();
    this.getFileMetadata();
    this.getTravellerMetadata();
    this.getCostMetadata();
    this.getHelpText();
  },
  mounted() {
  },
});
