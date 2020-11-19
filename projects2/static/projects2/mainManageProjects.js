var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    currentUser: {},
    isAdminOrMgmt: false,
    hover: false,

    showProjectList: true,
    showStaffList: false,
    showFinancialSummary: false,


    projects_loading: true,
    projectYears: [],
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
    filter_status: "",

    fiscalYears: [],
    tags: [],
    themes: [],
    functionalGroups: [],
    fundingSources: [],
    sections: [],

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
      apiService(`/api/project-planning/sections/${query}`).then(response => this.sections = response)
      if (this.filter_section && this.filter_section !== "") query += `;section=${this.filter_section}`
      apiService(`/api/project-planning/functional-groups/${query}`).then(response => this.functionalGroups = response)

    },
    getProjectYears(endpoint) {
      this.projects_loading = true;
      if (!endpoint) {
        endpoint = `/api/project-planning/project-years/`;
        // apply filters
        endpoint += `?user=true;` +
            `id=${this.filter_id};` +
            `title=${this.filter_title};` +
            `staff=${this.filter_staff};` +
            `fiscal_year=${this.filter_fiscal_year};` +
            `tag=${this.filter_tag};` +
            `theme=${this.filter_theme};` +
            `functional_group=${this.filter_functional_group};` +
            `funding_source=${this.filter_funding_source};` +
            `section=${this.filter_section};` +
            `status=${this.filter_status};`
      }

      apiService(endpoint)
          .then(response => {
            if (response.results) {
              this.projects_loading = false;
              this.projectYears.push(...response.results);
              this.next = response.next;
              this.previous = response.previous;
              this.count = response.count;
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
    comingSoon(){
      alert("this feature is coming soon!")
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
  computed: {},
  created() {
    this.getCurrentUser()
    this.getProjectYears()
    this.getFilterData()
  },
  mounted() {
  },
});

