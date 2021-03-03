var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    count: 0,
    currentSort: 'name',
    currentSortDir: 'asc',
    currentUser: {},
    hover: false,
    next: null,
    previous: null,
    requests: [],
    requests_loading: false,
    showSearchLanding: false,

    // filters
    filter_search: "",
    filter_fiscal_year: "",
    filter_status: "",
    filter_region: "",
    filter_division: "",
    filter_section: "",

    // dropdowns
    fiscalYears: [],
    regions: [],
    divisions: [],
    sections: [],

    requestLabels: {},
  },
  methods: {
    clearFilters() {
      this.filter_search = '';
      this.filter_fiscal_year = "";
      this.filter_status = "";
      this.filter_region = "";
      this.filter_division = "";
      this.filter_section = "";
      this.updateResults()
    },
    clearRequests() {
      this.requests = []
      this.next = null
      this.count = 0
    },
    getCurrentUser() {
      let endpoint = `/api/travel/user/`;
      apiService(endpoint)
          .then(response => {
            this.currentUser = response;
          })
    },
    getFilterData() {
      apiService(`/api/travel/fiscal-years/`).then(response => this.fiscalYears = response)
      apiService(`/api/travel/regions/`).then(response => this.regions = response)

      var query = "";
      if (this.filter_region && this.filter_region !== "") query = `?region=${this.filter_region}`
      apiService(`/api/travel/divisions/${query}`).then(response => this.divisions = response)

      if (this.filter_division && this.filter_division !== "") query = `?division=${this.filter_division}`
      apiService(`/api/travel/sections/${query}`).then(response => this.sections = response)

    },
    getRequestMetadata() {
      let endpoint = `/api/travel/meta/models/request/`;
      apiService(endpoint).then(data => {
        this.requestLabels = data.labels;
      });
    },
    getRequests(endpoint) {
      this.showSearchLanding = false;
      this.requests_loading = true;
      if (!endpoint) {
        endpoint = `/api/travel/requests/?`;
        let uri = window.location.search.substring(1);
        let params = new URLSearchParams(uri);
        let typeParam = params.get("all");
        if (typeParam) {
          endpoint += 'all=true;'
        }
        // apply filters
        endpoint += `search=${this.filter_search};` +
            `status=${this.filter_status};` +
            `fiscal_year=${this.filter_fiscal_year};` +
            `section__division__branch__region=${this.filter_region};` +
            `section__division=${this.filter_division};` +
            `section=${this.filter_section};` +
            `status=${this.filter_status};`
      }
      apiService(endpoint)
          .then(response => {
            if (response.results) {
              this.requests_loading = false;
              this.requests.push(...response.results);
              this.next = response.next;
              this.previous = response.previous;
              this.count = response.count;
            }
          })
    },
    goRequestDetail(request) {
      let params = window.location.search.substring(1);
      url = `/travel-plans/requests/${request.id}/view/?${params}`;
      window.location.href = url;
      // var win = window.open(url);
    },
    loadMoreResults() {
      if (this.next) {
        this.getRequests(this.next)
      }
    },
    sort(s) {
      // from https://www.raymondcamden.com/2018/02/08/building-table-sorting-and-pagination-in-vuejs
      //if s == current sort, reverse
      if (s === this.currentSort) {
        this.currentSortDir = this.currentSortDir === 'asc' ? 'desc' : 'asc';
      }
      this.currentSort = s;
    },
    updateResults() {
      this.clearRequests();
      this.getRequests();
      this.getFilterData();
    },
  },
  computed: {
    sortedRequests() {
      return this.requests.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === 'desc') modifier = -1;

        if (this.currentSort && this.currentSort.search("fiscal") > -1) {
          if (a["fiscal_year"] < b["fiscal_year"]) return -1 * modifier;
          if (a["fiscal_year"] > b["fiscal_year"]) return 1 * modifier;
        } else if (this.currentSort && this.currentSort.search("trip") > -1) {
          if (a["trip"]["name"] < b["trip"]["name"]) return -1 * modifier;
          if (a["trip"]["name"] > b["trip"]["name"]) return 1 * modifier;
        } else if (this.currentSort && this.currentSort.search("destination") > -1) {
          if (a["trip"]["location"] < b["trip"]["location"]) return -1 * modifier;
          if (a["trip"]["location"] > b["trip"]["location"]) return 1 * modifier;
        } else {
          if (a[this.currentSort] < b[this.currentSort]) return -1 * modifier;
          if (a[this.currentSort] > b[this.currentSort]) return 1 * modifier;
        }
        return 0;
      });
    },
    pageType() {
      let uri = window.location.search.substring(1);
      let params = new URLSearchParams(uri);
      params.get("all");
      if (params.get("all")) return 'all';
      else return "personal";
    },
    isAdmin() {
      return this.currentUser && this.currentUser.is_admin;
    },
  },
  created() {
    this.getCurrentUser()

    if (this.pageType !== 'all') this.getRequests();
    else this.showSearchLanding = true;

    this.getFilterData()
    this.getRequestMetadata()

  },
  mounted() {
  },
});

