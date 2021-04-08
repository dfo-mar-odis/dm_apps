Vue.component('v-select', VueSelect.VueSelect);
var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    showSidebar: false,
    showOverview: true,
    collapseOverview: true,
    collapseFinancials: true,
    collapseSubmit: true,
    currentUser: null,
    canModify: false,
    showSubmit: false,
    isACRDP: false,
    isCSRF: false,
    isSARA: false,
    project_loading: false,
    project: {},

    py_loading: false,
    projectYear: {},
    financials: [],
    financials_loading: false,
    project_financials: [],
    project_financials_loading: false,

    // staff
    staff_loading: false,
    staff: [],
    staffToEdit: {},
    showNewStaffModal: false,
    showOldStaffModal: false,

    // om costs
    om_cost_loading: false,
    om_costs: [],
    omCostToEdit: {},
    showNewOMCostModal: false,
    showOldOMCostModal: false,
    omCostLabels: [],
    omCategoryChoices: [],

    // capital costs
    capital_cost_loading: false,
    capital_costs: [],
    capitalCostToEdit: {},
    showNewCapitalCostModal: false,
    showOldCapitalCostModal: false,

    // activities
    activity_loading: false,
    activities: [],
    activityToEdit: {},
    showNewActivityModal: false,
    showOldActivityModal: false,
    activityLabels: [],
    activityTypeChoices: [],
    likelihoodChoices: [],
    impactChoices: [],
    riskRatingChoices: [],

    // collaborations
    collaboration_loading: false,
    collaborations: [],
    collaborationToEdit: {},
    showNewCollaborationModal: false,
    showOldCollaborationModal: false,

    // status reports
    status_report_loading: false,
    status_reports: [],
    statusReportToEdit: {},
    showNewStatusReportModal: false,
    showOldStatusReportModal: false,

    // files
    file_loading: false,
    files: [],
    fileToEdit: {},
    showNewFileModal: false,
    showOldFileModal: false,

  },
  methods: {
    displayOverview() {
      this.collapseOverview = false;
      // this.projectYear = {};
    },
    displaySubmit() {
      this.showSubmit = true
      this.showOverview = false
    },
    displayProjectYear(yearId) {
      // this.showOverview = true;
      // this.getProjectYear(yearId)
      window.location.hash = "#project-year"
      window.location.search = `?project_year=${yearId}`
      // update the query params

    },
    getProjectYear(yearId) {
      this.py_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/`;
      apiService(endpoint)
          .then(response => {
            this.py_loading = false;
            this.projectYear = response;
            // now let's get all the related data
            this.getStaff(yearId)
            this.getOMCosts(yearId)
            this.getCapitalCosts(yearId)
            this.getActivities(yearId)
            this.getCollaborations(yearId)
            this.getStatusReports(yearId)
            this.getFiles(yearId)
            this.getFinancials(yearId)
          })
    },
    getProject(projectId) {
      this.project_loading = true;
      let endpoint = `/api/project-planning/projects/${projectId}/`;
      apiService(endpoint)
          .then(response => {
            this.project_loading = false;
            this.project = response;
            if (response.id && response.default_funding_source && response.default_funding_source.toLowerCase().search("acrdp") > -1) {
              this.isACRDP = true;
            } else if (response.id && response.default_funding_source && response.default_funding_source.toLowerCase().search("csrf") > -1) {
              this.isCSRF = true;
            } else if (response.id && response.default_funding_source && response.default_funding_source.toLowerCase().search("sara") > -1) {
              this.isSARA = true;
            }

            // check to see if we are being asked to open the page to a specific year
            // from https://stackoverflow.com/questions/35914069/how-can-i-get-query-parameters-from-a-url-in-vue-js
            let uri = window.location.search.substring(1);
            let params = new URLSearchParams(uri);
            let projectYearParam = params.get("project_year");
            if (projectYearParam) {
              this.getProjectYear(projectYearParam)
            } else if (!this.projectYear.id && this.project.years.length) {
              this.getProjectYear(this.project.years[0].id)
            }
          })
    },
    submitProjectYear(projectYear, action) {
      if (action === "submit" || action === "unsubmit") {
        if (action === "submit") msg = submitMsg
        else msg = unsubmitMsg
        userInput = confirm(msg + projectYear.display_name)
        if (userInput) {
          this.project_loading = true;
          let endpoint = `/api/project-planning/project-years/${projectYear.id}/${action}/`;
          apiService(endpoint, "POST")
              .then(response => {
                this.project_loading = false;
                this.getProject(projectYear.project)
              })
        }
      }
    },
    getFinancials(yearId) {
      this.financials_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/financials/`;
      apiService(endpoint)
          .then(response => {
            this.financials_loading = false;
            this.financials = response;
          })
    },
    getProjectFinancials(projectId) {
      this.project_financials_loading = true;
      let endpoint = `/api/project-planning/projects/${projectId}/financials/`;
      apiService(endpoint)
          .then(response => {
            this.project_financials_loading = false;
            this.project_financials = response;
          })
    },
    getCurrentUser(projectId) {
      let endpoint = `/api/project-planning/user/?project=${projectId}`;
      apiService(endpoint)
          .then(response => {
            this.currentUser = response;
            this.canModify = this.currentUser.can_modify
          })
    },
    // Staff
    getStaff(yearId) {
      this.staff_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/staff/`;
      apiService(endpoint)
          .then(response => {
            this.staff_loading = false;
            this.staff = response;
          })
    },
    deleteStaffMember(staffMember) {
      userInput1 = confirm(deleteMsg)
      if (userInput1) {
        if (this.currentUser && this.currentUser.id == staffMember.user) userInput2 = confirm(deleteSelfMsg)
        else userInput2 = true
        if (userInput2) {
          let endpoint = `/api/project-planning/staff/${staffMember.id}/`;
          apiService(endpoint, "DELETE")
              .then(response => {
                if (!response.detail) this.$delete(this.staff, this.staff.indexOf(staffMember));
              })
        }
      }
    },
    openStaffModal(staff = null) {
      if (!staff) {
        this.showNewStaffModal = true;
      } else {
        this.staffToEdit = staff;
        this.showOldStaffModal = true;
      }

    },

    // O&M
    getOMCosts(yearId) {
      this.om_cost_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/om-costs/`;
      apiService(endpoint)
          .then(response => {
            this.om_cost_loading = false;
            this.om_costs = response;
          })
    },
    deleteOMCost(OMCost) {
      userInput = confirm(deleteMsg + OMCost.om_category_display)
      if (userInput) {
        let endpoint = `/api/project-planning/om-costs/${OMCost.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.om_costs, this.om_costs.indexOf(OMCost));
            })
      }
    },
    addAllOMCosts() {
      if (this.projectYear.id) {
        this.om_cost_loading = true;
        let endpoint = `/api/project-planning/project-years/${this.projectYear.id}/add-all-costs/`;
        apiService(endpoint, "POST")
            .then(response => {
              this.om_cost_loading = false;
              this.om_costs = response;
            })
      }
    },
    clearEmptyOMCosts() {
      if (this.projectYear.id) {
        this.om_cost_loading = true;
        let endpoint = `/api/project-planning/project-years/${this.projectYear.id}/remove-empty-costs/`;
        apiService(endpoint, "POST")
            .then(response => {
              this.om_cost_loading = false;
              this.om_costs = response;
            })
      }
    },
    openOMCostModal(OMCost) {
      if (!OMCost) {
        this.showNewOMCostModal = true;
      } else {
        this.omCostToEdit = OMCost;
        this.showOldOMCostModal = true;
      }

    },

    // Capital
    getCapitalCosts(yearId) {
      this.capital_cost_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/capital-costs/`;
      apiService(endpoint)
          .then(response => {
            this.capital_cost_loading = false;
            this.capital_costs = response;
          })
    },
    deleteCapitalCost(capitalCost) {
      userInput = confirm(deleteMsg + capitalCost.category_display)
      if (userInput) {
        let endpoint = `/api/project-planning/capital-costs/${capitalCost.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.capital_costs, this.capital_costs.indexOf(capitalCost));
            })
      }
    },

    openCapitalCostModal(capitalCost) {
      if (!capitalCost) {
        this.showNewCapitalCostModal = true;
      } else {
        this.capitalCostToEdit = capitalCost;
        this.showOldCapitalCostModal = true;
      }
    },


    // Activities
    getActivities(yearId) {
      this.activity_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/activities/`;
      apiService(endpoint)
          .then(response => {
            this.activity_loading = false;
            this.activities = response;
          })
    },
    deleteActivity(activity) {
      userInput = confirm(deleteMsg + activity.name)
      if (userInput) {
        let endpoint = `/api/project-planning/activities/${activity.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.activities, this.activities.indexOf(activity))
            })
      }
    },
    cloneActivity(activity) {
      let endpoint = `/api/project-planning/activities/${activity.id}/?clone=true`;
      apiService(endpoint, "POST")
          .then(response => {
            if (!response.detail) this.getActivities(activity.project_year_id);
          })
    },

    openActivityModal(activity) {
      if (!activity) {
        this.showNewActivityModal = true;
      } else {
        this.activityToEdit = activity;
        this.showOldActivityModal = true;
      }
    },


    // Collaboration
    getCollaborations(yearId) {
      this.collaboration_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/collaborations/`;
      apiService(endpoint)
          .then(response => {
            this.collaboration_loading = false;
            this.collaborations = response;
          })
    },
    deleteCollaboration(collaboration) {
      userInput = confirm(deleteMsg + collaboration.name)
      if (userInput) {
        let endpoint = `/api/project-planning/collaborations/${collaboration.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.collaborations, this.collaborations.indexOf(collaboration));
            })
      }
    },

    openCollaborationModal(collaboration) {
      if (!collaboration) {
        this.showNewCollaborationModal = true;
      } else {
        this.collaborationToEdit = collaboration;
        this.showOldCollaborationModal = true;
      }
    },


    // Status Report
    getStatusReports(yearId) {
      this.status_report_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/status-reports/`;
      apiService(endpoint)
          .then(response => {
            this.status_report_loading = false;
            this.status_reports = response;
          })
    },
    deleteStatusReport(statusReport) {
      userInput = confirm(deleteMsg + statusReport.name)
      if (userInput) {
        let endpoint = `/api/project-planning/status-reports/${statusReport.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.status_reports, this.status_reports.indexOf(statusReport));
            })
      }
    },

    openStatusReportModal(statusReport) {
      if (!statusReport) {
        this.showNewStatusReportModal = true;
      } else {
        this.statusReportToEdit = statusReport;
        this.showOldStatusReportModal = true;
      }
    },

    // File
    getFiles(yearId) {
      this.file_loading = true;
      let endpoint = `/api/project-planning/project-years/${yearId}/files/`;
      apiService(endpoint)
          .then(response => {
            this.file_loading = false;
            this.files = response;
          })
    },
    deleteFile(file) {
      userInput = confirm(deleteMsg + file.name)
      if (userInput) {
        let endpoint = `/api/project-planning/files/${file.id}/`;
        apiService(endpoint, "DELETE")
            .then(response => {
              if (!response.detail) this.$delete(this.files, this.files.indexOf(file));
            })
      }
    },

    openFileModal(file) {
      if (!file) {
        this.showNewFileModal = true;
      } else {
        this.fileToEdit = file;
        this.showOldFileModal = true;
      }
    },

    closeModals(projectYear) {
      this.showNewStaffModal = false;
      this.showOldStaffModal = false;

      this.showNewOMCostModal = false;
      this.showOldOMCostModal = false;

      this.showNewCapitalCostModal = false;
      this.showOldCapitalCostModal = false;

      this.showNewActivityModal = false;
      this.showOldActivityModal = false;

      this.showNewCollaborationModal = false;
      this.showOldCollaborationModal = false;

      this.showNewStatusReportModal = false;
      this.showOldStatusReportModal = false;

      this.showNewFileModal = false;
      this.showOldFileModal = false;

      if (projectYear) {
        this.$nextTick(() => {
          this.getProjectYear(projectYear.id)
          // this.getStaff(projectYear.id)
          // this.getOMCosts(projectYear.id)
          // this.getCapitalCosts(projectYear.id)
          // this.getActivities(projectYear.id)
          // this.getStatusReports(projectYear.id)
          // this.getCollaborations(projectYear.id)
          // this.getFiles(projectYear.id)
          // this.getFinancials(projectYear.id)
          this.getProjectFinancials(projectYear.project.id)
          this.getCurrentUser(projectYear.project.id)

        })
      }
    },
    goProjectYearEdit(projectYearId) {
      window.location.href = `/project-planning/project-years/${projectYearId}/edit/`
    },
    goProjectEdit(projectId) {
      window.location.href = `/project-planning/projects/${projectId}/edit/`
    },
    goProjectYearDelete(projectYearId) {
      window.location.href = `/project-planning/project-years/${projectYearId}/delete/`
    },
    goProjectYearClone(projectYearId) {
      window.location.href = `/project-planning/project-years/${projectYearId}/clone/`
    },
    goStatusReportDetail(statusReportId) {
      url = `/project-planning/status-reports/${statusReportId}/view/`;
      win = window.open(url, '_blank');
    },
    isABase(name) {
      if (name && name.length) {
        return name.toLowerCase().search("a-base") > -1
      }
    },
    isBBase(name) {
      if (name && name.length) {
        return name.toLowerCase().search("b-base") > -1
      }
    },
    isCBase(name) {
      if (name && name.length) {
        return name.toLowerCase().search("c-base") > -1
      }
    },
    getActivityMetadata() {
      let endpoint = `/api/project-planning/meta/models/activity/`;
      apiService(endpoint).then(data => {
        this.activityLabels = data.labels;
        this.activityTypeChoices = data.type_choices;
        this.likelihoodChoices = data.likelihood_choices;
        this.impactChoices = data.impact_choices;
        this.riskRatingChoices = data.risk_rating_choices;
      });
    },
    getOMCostMetadata() {
      let endpoint = `/api/project-planning/meta/models/om-cost/`;
      apiService(endpoint).then(data => {
        this.omCostLabels = data.labels;
        this.omCategoryChoices = data.om_category_choices;
      });
    },
    markActivity(activity, action) {
      if (action === "complete" || action === "incomplete") {
        if (action === "complete") msg = markActivityAsComplete;
        else msg = markActivityAsIncomplete;
        let userInput = prompt(msg);
        if (userInput !== null) {
          this.project_loading = true;
          let endpoint = `/api/project-planning/activities/${activity.id}/?action=${action}`;
          apiService(endpoint, "POST", userInput)
              .then(response => {
                this.project_loading = false;
                this.getProjectYear(activity.project_year_id)
              })
        }
      }

    },

  },
  computed: {
    financial_totals() {
      myObj = {
        salary: 0,
        om: 0,
        capital: 0,
        total: 0,
      }
      if (this.financials) {
        for (var i = 0; i < this.financials.length; i++) {
          myObj.salary += this.financials[i].salary
          myObj.om += this.financials[i].om
          myObj.capital += this.financials[i].capital
          myObj.total += this.financials[i].total
        }
      }
      return myObj
    },
    project_financial_totals() {
      myObj = {
        salary: 0,
        om: 0,
        capital: 0,
        total: 0,
      }
      if (this.project_financials) {
        for (var i = 0; i < this.project_financials.length; i++) {
          myObj.salary += this.project_financials[i].salary
          myObj.om += this.project_financials[i].om
          myObj.capital += this.project_financials[i].capital
          myObj.total += this.project_financials[i].total
        }
      }
      return myObj
    }

  },
  created() {
    this.getActivityMetadata();
    this.getOMCostMetadata();
    this.getProjectFinancials(projectId)
    this.getCurrentUser(projectId)
    this.getProject(projectId)
  },
  mounted() {
  },
});

