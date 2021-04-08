var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    currentUser: null,
    sections: [],
    loadingSections: false,
    editMode: false,
    sectionToEdit: null,
    unsavedSectionWork: false,
    sectionFormErrors: null,
    observationFormErrors: null,
    intervalWarning: null,
    new_observation: {
      sex: "",
      egg_status: "",
      carapace_length_mm: null,
      certainty_rating: 1,
      comment: null,
    },
  },
  methods: {
    getCurrentUser() {
      let endpoint = `/api/project-planning/user/`;
      apiService(endpoint)
          .then(response => {
            this.currentUser = response;
            this.isAdminOrMgmt = this.currentUser.is_admin || this.currentUser.is_management
          })
    },
    getSections() {
      this.loadingSections = true;
      let endpoint = `/api/scuba/sections/?dive=${diveId}`;
      apiService(endpoint)
          .then(response => {
            this.sections = response;
            this.loadingSections = false;
          })
    },
    closeEditMode() {
      var userInput = true;
      if (this.unsavedSectionWork) {
        msg = "Are you certain you want to leave with un-saved work?";
        userInput = confirm(msg);
      }
      if (userInput) {
        this.sectionFormErrors = null
        this.unsavedSectionWork = false;
        this.editMode = false;
        this.sectionToEdit = null;
        this.getSections();
      }
    },
    editSection(section) {
      if (section == null) {
        // we should be able to take a good guess at the interval
        var intervalArray = [];
        for (var i = 0; i < this.sections.length; i++) {
          s = this.sections[i];
          intervalArray.push(s.interval);
        }
        intervalArray.sort(function(a, b){return a-b});
        if (!intervalArray.length) interval = null;
        else {
          var interval = intervalArray[intervalArray.length - 1] + 1;
          // question 1: what if there is a number missing?
          if (intervalArray.length !== interval -1) {
            for (var i = 1; i < interval; i++) {
              if(!intervalArray.includes(i)) {
                interval = i;
                break;
              }
            }
          }
          // question 2: what if this is greater than 20?
          else if (interval > 20) {
            alert("Warning! This dive already has all 20 intervals!")
            interval = null
          }
        }

        this.sectionToEdit = {
          comment: "",
          depth_ft: null,
          dive: diveId,
          interval: interval,
          observations: [],
          percent_algae: 0,
          percent_cobble: 0,
          percent_gravel: 0,
          percent_hard: 0,
          percent_mud: 0,
          percent_pebble: 0,
          percent_sand: 0,
        }

      } else {
        this.sectionToEdit = section

      }
      this.editMode = true;

      // focus on the save button
      this.$nextTick(() => {
        if (section && section.id) this.$refs['top_of_form1'].focus()
        else this.$refs['top_of_form'].focus()

      })

    },
    submitSectionForm() {
      this.sectionFormErrors = null
      // this is an update
      if (this.sectionToEdit.id) {
        let endpoint = `/api/scuba/sections/${this.sectionToEdit.id}/`;
        apiService(endpoint, "PUT", this.sectionToEdit)
            .then(response => {
              console.log(response)
              // if the response does not have an id, it means there is an error...
              if (!response.id) {
                this.sectionFormErrors = response[Object.keys(response)[0]][0]
              } else {
                this.unsavedSectionWork = false;

              }
            })

      }
      // this is a new section being added
      else {
        let endpoint = `/api/scuba/sections/`;
        apiService(endpoint, "POST", this.sectionToEdit)
            .then(response => {
              console.log(response)
              // if the response does not have an id, it means there is an error...
              if (!response.id) {
                this.sectionFormErrors = response[Object.keys(response)[0]][0]
              } else {
                this.unsavedSectionWork = false;
                // this.getSections();
                // this.closeEditMode();
                this.sectionToEdit = response;
                this.$nextTick(() => {
                  this.$refs['top_of_form1'].focus();
                })
              }
            })
      }

    },
    updateObservation(observation) {
      this.observationFormErrors = null
      let endpoint = `/api/scuba/observations/${observation.id}/`;
      apiService(endpoint, "PUT", observation)
          .then(response => {
            console.log(response)
            // if the response does not have an id, it means there is an error...
            if (!response.id) {
              this.observationFormErrors = response[Object.keys(response)[0]]
              console.log(this.observationFormErrors)
            }
          })
    },
    deleteObservation(observation) {
      // warning
      var userInput = true;
      msg = "Are you certain you want to delete this observation?";
      userInput = confirm(msg);
      if (userInput) {
        let endpoint = `/api/scuba/observations/${observation.id}`;
        apiService(endpoint, "DELETE")
            .then(response => {
              // if the response does not have an id, it means there is an error...
              if (response.detail) {
                this.sectionFormErrors = response["detail"]
              } else {
                this.$delete(this.sectionToEdit.observations, this.sectionToEdit.observations.indexOf(observation))
              }

            })
      }
    },
    submitObservationForm() {
      this.obserFormErrors = null
      // this is a new section being added
      let endpoint = `/api/scuba/observations/`;
      this.new_observation.section_id = this.sectionToEdit.id
      apiService(endpoint, "POST", this.new_observation)
          .then(response => {
            console.log(response)
            // if the response does not have an id, it means there is an error...
            if (!response.id) {
              this.obserFormErrors = response[Object.keys(response)[0]][0]
            } else {
              this.sectionToEdit.observations.unshift(response)
              this.new_observation = {
                sex: "",
                egg_status: "",
                carapace_length_mm: null,
                certainty_rating: 1,
                comment: null,
              }
              this.$refs["top_of_form1"].focus()
            }
          })

    },
    deleteSection(section) {
      // warning
      var userInput = true;
      msg = "Are you certain you want to delete this section?";
      userInput = confirm(msg);
      if (userInput) {
        let endpoint = `/api/scuba/sections/${section.id}`;
        apiService(endpoint, "DELETE")
            .then(response => {
              // if the response does not have an id, it means there is an error...
              if (response.detail) {
                this.sectionFormErrors = response["detail"]
              } else {

                this.closeEditMode()
              }

            })
      }
    },
    updateEggStatus(){
      if(this.new_observation.sex === 'f') this.new_observation.egg_status = 0
      else this.new_observation.egg_status = ""
    },
    updateLengthCertainty(){
      let length = Number(this.new_observation.carapace_length_mm)
      if(this.new_observation.sex === 'u' && length > 20 ) this.new_observation.certainty_rating = 0
      else this.new_observation.certainty_rating = 1
    },

  },
  filters: {
    floatformat: function (value, precision = 2) {
      if (value == null) return '';
      value = Number(value).toFixed(precision).toLocaleString("en");
      return value
    },
    currencyFormat: function (value, precision = 2) {
      if (value == null) return '';
      value = accounting.formatNumber(value, precision);
      return value
    },
    zero2NullMark: function (value) {
      if (!value || value === "0.00" || value == 0) return '---';
      return value
    },
    nz: function (value, arg = "---") {
      if (value == null || value === "None") return arg;
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
    totalPercentage() {
      myString = ((Number(this.sectionToEdit.percent_sand) +
          Number(this.sectionToEdit.percent_mud) +
          Number(this.sectionToEdit.percent_hard) +
          Number(this.sectionToEdit.percent_algae) +
          Number(this.sectionToEdit.percent_gravel) +
          Number(this.sectionToEdit.percent_cobble) +
          Number(this.sectionToEdit.percent_pebble)) * 100).toFixed() + "%"
      if (myString === "99%") myString = "100%"
      return myString
    },
  },
  created() {
    this.getSections();

  },
  mounted() {
  },
});

