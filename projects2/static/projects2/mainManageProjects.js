Vue.component('v-select', VueSelect.VueSelect);
var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    showSidebar: true,
    currentUser: {},
    isAdminOrMgmt: false,
    hover: false,

    errorNoFiscalYear: false,


    showProjectList: true,
    showStaffList: false,
    showFinancialSummary: false,

    currentSort: 'name',
    currentSortDir: 'asc',

    projects_loading: true,
    staff_loading: true,
    errorTooBigStaff: false,
    errorTooSmallStaff: false,
    financial_loading: true,
    errorTooBigFinancial: false,
    errorTooSmallFinancial: false,
    projectYears: [],
    staff: [],
    financials: [],
    next: null,
    previous: null,
    count: 0,

    // filters
    filter_id: null,
    filter_title: null,
    filter_staff: null,
    filter_fiscal_year: "",
    filter_tag: "",
    filter_theme: "",
    filter_functional_group: "",
    filter_funding_source: "",
    filter_section: "",
    filter_region: "",
    filter_division: "",
    filter_status: "",

    showColumnAllocation: false,
    showColumnLeads: true,
    showColumnHidden: true,
    showColumnScore: false,
    showColumnLastModified: true,

    fiscalYears: [],
    tags: [],
    themes: [],
    functionalGroups: [],
    fundingSources: [],
    sections: [],
    regions: [],
    divisions: [],

    // modal
    projectYear2Review: {},
    showReviewModal: false,
    approvalModal: false,
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
    goProjectDetail(projectYear) {
      url = `/project-planning/projects/${projectYear.project.id}/view/?project_year=${projectYear.id}`;
      var win = window.open(url, '_blank');
    },
    getFilterData() {
      var query = `?user=true`;
      apiService(`/api/project-planning/themes/${query}`).then(response => this.themes = response)
      apiService(`/api/project-planning/fiscal-years/${query}`).then(response => this.fiscalYears = response)
      apiService(`/api/project-planning/tags/${query}`).then(response => this.tags = response)
      apiService(`/api/project-planning/funding-sources/${query}`).then(response => this.fundingSources = response)

      apiService(`/api/project-planning/regions/${query}`).then(response => this.regions = response)

      if (this.filter_region && this.filter_region !== "") query += `&region=${this.filter_region}`
      apiService(`/api/project-planning/divisions/${query}`).then(response => this.divisions = response)

      if (this.filter_division && this.filter_division !== "") query += `&division=${this.filter_division}`
      apiService(`/api/project-planning/sections/${query}`).then(response => this.sections = response)

      if (this.filter_section && this.filter_section !== "") query += `&section=${this.filter_section}`
      apiService(`/api/project-planning/functional-groups/${query}`).then(response => this.functionalGroups = response)

    },

    getProjectYearsEndpoint(pageSize = 45) {
      endpoint = `/api/project-planning/project-years/`;
      // apply filters
      endpoint += `?page_size=${pageSize}&user=true&` +
          `id=${this.filter_id}&` +
          `title=${this.filter_title}&` +
          `staff=${this.filter_staff}&` +
          `fiscal_year=${this.filter_fiscal_year}&` +
          `tag=${this.filter_tag}&` +
          `theme=${this.filter_theme}&` +
          `functional_group=${this.filter_functional_group}&` +
          `funding_source=${this.filter_funding_source}&` +
          `region=${this.filter_region}&` +
          `division=${this.filter_division}&` +
          `section=${this.filter_section}&` +
          `status=${this.filter_status}&`
      return endpoint

    },

    getProjectYears(endpoint, pageSize = 45) {
      this.projects_loading = true;
      if (!endpoint) endpoint = this.getProjectYearsEndpoint(pageSize)
      apiService(endpoint)
          .then(response => {
            if (response.results) {
              this.projects_loading = false;
              this.projectYears.push(...response.results);
              this.next = response.next;
              this.previous = response.previous;
              this.count = response.count;
              this.getStaff()
              this.getFinancials()
            }
          })
    },
    changeTabs(name) {
      this.showProjectList = false
      this.showStaffList = false
      this.showFinancialSummary = false
      if (name === "project") this.showProjectList = true
      else if (name === "staff") this.showStaffList = true
      else if (name === "financial") this.showFinancialSummary = true
    },


    getStaff() {
      this.staff_loading = true;
      this.errorTooBigStaff = false
      this.errorTooSmallStaff = false
      this.errorNoFiscalYear = false
      if (!this.filter_fiscal_year) {
        this.staff_loading = false;
        this.errorNoFiscalYear = true;
      } else if (!this.projectYears.length) {
        this.staff_loading = false;
        this.errorTooSmallStaff = true;
      } else if (this.count > 150) {
        this.staff_loading = false;
        this.errorTooBigStaff = true;
      } else {
        // first get the full list of project years
        let endpoint1 = this.getProjectYearsEndpoint(pageSize = 150)
        apiService(endpoint1)
            .then(response => {
              if (response.results) {
                if (response.next) {
                  this.errorTooBigStaff = true
                } else {

                  // need a list of projectYears
                  pyIds = []
                  for (var i = 0; i < response.results.length; i++) {
                    pyIds.push(response.results[i].id)
                  }

                  let endpoint2 = `/api/project-planning/fte-breakdown/?year=${this.filter_fiscal_year}&ids=${pyIds}`;
                  apiService(endpoint2)
                      .then(response => {
                        this.staff_loading = false;
                        this.staff = response;
                      })
                }
              }

            })
      }
    },
    getFinancials() {
      this.financial_loading = true;
      this.errorTooBigFinancial = false
      this.errorTooSmallFinancial = false

      if (!this.projectYears.length) {
        this.financial_loading = false;
        this.errorTooSmallFinancial = true;
      } else if (this.count > 200) {
        this.financial_loading = false;
        this.errorTooBigFinancial = true;
      } else {
        // first get the full list of project years
        let endpoint1 = this.getProjectYearsEndpoint(pageSize = 200)
        apiService(endpoint1)
            .then(response => {
              if (response.results) {

                if (response.next) {
                  this.errorTooBigFinancial = true
                } else {
                  // need a list of projectYears
                  pyIds = []
                  for (var i = 0; i < response.results.length; i++) {
                    pyIds.push(response.results[i].id)
                  }
                  let endpoint2 = `/api/project-planning/financials/?ids=${pyIds}`;
                  apiService(endpoint2)
                      .then(response => {
                        this.financial_loading = false;
                        this.financials = response;
                      })
                }
              }

            })
      }
    },
    submitProjectYear(projectYear, action) {
      if (action === "submit" || action === "unsubmit") {
        if (action === "submit") msg = submitMsg
        else msg = unsubmitMsg
        userInput = confirm(msg + projectYear.display_name)
        if (userInput) {
          let endpoint = `/api/project-planning/project-years/${projectYear.id}/${action}/`;
          apiService(endpoint, "POST")
              .then(response => {
                this.$set(this.projectYears, this.projectYears.indexOf(projectYear), response);
              })
        }
      }
    },
    comingSoon() {
      alert("this feature is coming soon!")
    },
    sort(s) {
      // from https://www.raymondcamden.com/2018/02/08/building-table-sorting-and-pagination-in-vuejs
      //if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      }
      this.currentSort = s;
    },
    clearProjectYears() {
      this.projectYears = []
      this.next = null
      this.count = 0
    },
    loadMoreResults() {
      if (this.next) {
        this.getProjectYears(this.next)
      }
    },
    clearFilters() {
      this.filter_id = null;
      this.filter_title = null;
      this.filter_staff = null;
      this.filter_fiscal_year = "";
      this.filter_tag = "";
      this.filter_theme = "";
      this.filter_functional_group = "";
      this.filter_funding_source = "";
      this.filter_region = "";
      this.filter_division = "";
      this.filter_section = "";
      this.filter_status = "";
      this.filter_is_hidden = false;

      this.updateResults()
    },
    updateResults() {
      this.clearProjectYears();
      this.getProjectYears();
      this.getFilterData();

    },
    openReviewModal(projectYear, which = "review") {
      this.projectYear2Review = projectYear;
      if (!this.projectYear2Review.review) {
        this.projectYear2Review.review = {}
      }
      this.showReviewModal = true;
      if (which === "approval") {
        this.approvalModal = true;
        this.projectYear2Review.review.approval_email_update = true
      }
    },

    closeModal(updatedProjectYear) {
      if (updatedProjectYear) {

        let endpoint = `/api/project-planning/project-years/${updatedProjectYear.id}/`;
        apiService(endpoint, "GET")
            .then(response => {
              this.$set(this.projectYears, this.projectYears.indexOf(updatedProjectYear), response);
            })
      }
      this.showReviewModal = false;
      this.approvalModal = false;

    },
    toggleShowProjects(staff) {
      staff.showRelatedProjects = !staff.showRelatedProjects
      this.$forceUpdate()
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

    sortedProjectYears() {
      return this.projectYears.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === 'desc') modifier = -1;

        if (this.currentSort && this.currentSort.search("fiscal") > -1) {
          if (a["fiscal_year"] < b["fiscal_year"]) return -1 * modifier;
          if (a["fiscal_year"] > b["fiscal_year"]) return 1 * modifier;
        } else if (this.currentSort === "id") {
          if (a["project"]["id"] < b["project"]["id"]) return -1 * modifier;
          if (a["project"]["id"] > b["project"]["id"]) return 1 * modifier;
        } else if (this.projectYears[0][this.currentSort] == null) {
          if (a["project"][this.currentSort] < b["project"][this.currentSort]) return -1 * modifier;
          if (a["project"][this.currentSort] > b["project"][this.currentSort]) return 1 * modifier;
        } else {
          if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        }
        return 0;
      });
    },

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
  },
  created() {
    this.getCurrentUser()
    this.getProjectYears()
    this.getFilterData()
  },
  mounted() {
  },
});

