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
    trips: [],
    trips_loading: true,

    // filters
    filter_search: "",
    filter_fiscal_year: "",
    filter_regional_lead: "",
    filter_adm_approval: "",
    filter_status: "",
    filter_subcategory: "",

    // dropdowns
    fiscalYears: [],
    regions: [],
    divisions: [],
    sections: [],

    tripLabels: {},

  },
  methods: {
    clearFilters() {
      this.filter_search = null;
      this.filter_fiscal_year = "";
      this.filter_regional_lead = null;
      this.filter_adm_approval = "";
      this.filter_status = "";
      this.filter_subcategory = "";
      this.updateResults()
    },
    clearTrips() {
      this.trips = []
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
    getDeadlineClass(days) {
      let myStr = 'px-1 py-1 ';
      if (days) {
        if (days > 45) myStr += 'bg-success text-light';
        else if (days >= 15) myStr += 'bg-warning';
        else myStr += 'bg-danger text-light';
      }
      return myStr;
    },
    getFilterData() {
      apiService(`/api/travel/fiscal-years/`).then(response => this.fiscalYears = response)
      apiService(`/api/travel/regions/`).then(response => this.regions = response)
    },
    getTripMetadata() {
      let endpoint = `/api/travel/meta/models/trip/`;
      apiService(endpoint).then(data => {
        this.tripLabels = data.labels;
      });
    },
    getTrips(endpoint) {
      this.trips_loading = true;
      if (!endpoint) {
        endpoint = `/api/travel/trips/?`;
        if (this.pageType === 'all') endpoint += 'all=true;'
        else if (this.pageType === 'adm-hit-list') endpoint += 'adm-hit-list=true;'
        else if (this.pageType === 'adm-verification') endpoint += 'adm-verification=true;'
        else if (this.pageType === 'regional-verification') endpoint += 'regional-verification=true;'
      }

      // apply filters
      endpoint += `search=${this.filter_search}&` +
          `lead=${this.filter_regional_lead}&` +
          `status=${this.filter_status}&` +
          `fiscal_year=${this.filter_fiscal_year}&` +
          `is_adm_approval_required=${this.filter_adm_approval}&` +
          `trip_subcategory=${this.filter_subcategory}&`

      apiService(endpoint)
          .then(response => {
            if (response.results) {
              this.trips_loading = false;
              this.trips.push(...response.results);
              this.next = response.next;
              this.previous = response.previous;
              this.count = response.count;
            }
          })
    },
    goRow(trip) {
      let win;
      if (this.pageType.search("verification") > -1) {
        url = `/travel-plans/trips/${trip.id}/verify/?${this.pageType}=true`;
        win = window.open(url, '_blank');
      } else if (this.pageType.search("all") > -1) {
        url = `/travel-plans/trips/${trip.id}/view/?${window.location.search.substring(1)}`;
        win = window.open(url, '_blank');
      } else {
        url = `/travel-plans/trips/${trip.id}/view/?${window.location.search.substring(1)}`;
        window.location.href = url;
      }
    },
    loadMoreResults() {
      if (this.next) {
        this.getTrips(this.next)
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
      this.clearTrips();
      this.getTrips();
      this.getFilterData();
    },
  },
  computed: {
    sortedTrips() {
      return this.trips.sort((a, b) => {
        let modifier = 1;
        if (this.currentSortDir === 'desc') modifier = -1;

        if (this.currentSort && this.currentSort.search("fiscal") > -1) {
          if (a["fiscal_year"] < b["fiscal_year"]) return -1 * modifier;
          if (a["fiscal_year"] > b["fiscal_year"]) return 1 * modifier;
        } else if (this.currentSort && this.currentSort.search("title") > -1) {
          if (a["name"] < b["name"]) return -1 * modifier;
          if (a["name"] > b["name"]) return 1 * modifier;
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
      else if (params.get("regional-verification")) return 'regional-verification';
      else if (params.get("adm-verification")) return 'adm-verification';
      else if (params.get("adm-hit-list")) return 'adm-hit-list';
      else return "upcoming";
    }

  },
  created() {
    this.getCurrentUser()
    this.getTrips()
    this.getFilterData()
    this.getTripMetadata()
  },
  mounted() {
  },
});

