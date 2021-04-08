var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    showSidebar: true,
    currentUser: {},
    isAdminOrMgmt: false,
    hover: false,

    currentSort: 'name',
    currentSortDir: 'asc',

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
    filter_region: "",
    filter_division: "",
    filter_section: "",
    filter_status: "",
    filter_is_hidden: false,

    fiscalYears: [],
    tags: [],
    themes: [],
    functionalGroups: [],
    fundingSources: [],
    regions: [],
    divisions: [],
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
      apiService(`/api/project-planning/fiscal-years/`).then(response => this.fiscalYears = response)

      apiService(`/api/project-planning/tags/`).then(response => this.tags = response)

      apiService(`/api/project-planning/themes/`).then(response => this.themes = response)


      apiService(`/api/project-planning/funding-sources/`).then(response => this.fundingSources = response)

      apiService(`/api/project-planning/regions/`).then(response => this.regions = response)

      var query = "";
      if (this.filter_region && this.filter_region !== "") query = `?region=${this.filter_region}`
      apiService(`/api/project-planning/divisions/${query}`).then(response => this.divisions = response)

      if (this.filter_division && this.filter_division !== "") query = `?division=${this.filter_division}`
      apiService(`/api/project-planning/sections/${query}`).then(response => this.sections = response)

      if (this.filter_section && this.filter_section !== "") query = `?section=${this.filter_section}`
      apiService(`/api/project-planning/functional-groups/${query}`).then(response => this.functionalGroups = response)

    },
    getProjectYears(endpoint) {
      this.projects_loading = true;
      if (!endpoint) {
        endpoint = `/api/project-planning/project-years/`;
        // apply filters
        endpoint += `?is_hidden=${this.filter_is_hidden}&` +
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
    sort(s) {
      // from https://www.raymondcamden.com/2018/02/08/building-table-sorting-and-pagination-in-vuejs
      //if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      }
      this.currentSort = s;
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
  },
  created() {
    this.getCurrentUser()
    this.getProjectYears()
    this.getFilterData()
  },
  mounted() {
  },
});

