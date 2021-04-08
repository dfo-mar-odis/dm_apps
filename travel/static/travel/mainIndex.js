var app = new Vue({
  el: '#app',
  delimiters: ["${", "}"],
  data: {
    admHitCount: 0,
    adminWarnings: [],
    admVerificationCount: 0,
    currentUser: {},
    loading_adm_hit_list: false,
    loading_adm_verification_list: false,
    loading_rdg_approval_list: false,
    loading_regional_verification_list: false,
    loading_user: false,
    regionalRDGApprovalCount: 0,
    regionalVerificationCount: 0,
    showNCR: false,
    showOverview: true,
    showRegions: false,
    showReviewer: false,
    showSupport: false,
    showTraveller: false,
    userRequests: [],
    userTripRequestReviews: [],
    userTripReviews: [],
    faqs: [],
    faqSearch: '',

    // vuetify
    alignTop: false,
    avatar: false,
    dense: false,
    fillDot: false,
    hideDot: false,
    icon: false,
    iconColor: false,
    left: false,
    reverse: false,
    right: false,
    small: false,

  },
  methods: {
    changeTabs(tabFlag) {
      this.showOverview = false;
      this.showTraveller = false;
      this.showReviewer = false;
      this.showRegions = false;
      this.showNCR = false;
      this.showSupport = false;
      this[tabFlag] = true;
    },
    getAdminWarnings() {
      let endpoint = `/api/travel/admin-warnings/`;
      apiService(endpoint)
          .then(response => {
            if (response.length) {
              this.adminWarnings = response;
            }
          })
    },
    getFAQs() {
      let endpoint = `/api/travel/faqs/`;
      apiService(endpoint)
          .then(response => {
            if (response.length) {
              this.faqs = response;
            }
          })
    },
    getADMTrips() {
      this.loading_adm_verification_list = true;
      this.loading_adm_hit_list = true;
      apiService(`/api/travel/trips/?adm-verification=true`)
          .then(response => {
            this.loading_adm_verification_list = false;
            this.admVerificationCount = response.count;
          })
      apiService(`/api/travel/trips/?adm-hit-list=true`)
          .then(response => {
            this.loading_adm_hit_list = false;
            this.admHitCount = response.count;
          })
    },
    getCurrentUser() {
      this.loading_user = true;
      let endpoint = `/api/travel/user/`;
      apiService(endpoint)
          .then(response => {
            this.loading_user = false;
            this.currentUser = response;
            this.getAdminWarnings();
            if (this.currentUser.is_ncr_admin) this.getADMTrips();
            if (this.currentUser.is_regional_admin) this.getRegionalAdminStuff();
          })
    },
    getRegionalAdminStuff() {
      this.loading_regional_verification_list = true;
      this.loading_rdg_approval_list = true;
      apiService(`/api/travel/trips/?regional-verification=true`)
          .then(response => {
            this.loading_regional_verification_list = false;
            this.regionalVerificationCount = response.count;
          })
      apiService(`/api/travel/request-reviewers/?rdg=true`)
          .then(response => {
            this.loading_rdg_approval_list = false;
            if (response.length) this.regionalRDGApprovalCount = response.length;
          })
    }
  },

  computed: {
    isAdmin() {
      return this.currentUser.is_regional_admin;
    },
    isNCRAdmin() {
      return this.currentUser.is_ncr_admin;
    },
    foundFAQs() {
      if (this.faqSearch && this.faqSearch !== '') {
        myArray = []
        for (var i = 0; i < this.faqs.length; i++) {
          if (this.faqs[i].tquestion.toLowerCase().search(this.faqSearch.toLowerCase()) > -1 || this.faqs[i].tanswer.toLowerCase().search(this.faqSearch.toLowerCase()) > -1) {
            myArray.push(this.faqs[i])
          }
        }
        return myArray
      }
      return this.faqs
    }
  },
  created() {
    this.getCurrentUser()
    this.getFAQs()
  },
  mounted() {
  },
  vuetify: new Vuetify()

});
