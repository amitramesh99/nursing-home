// Vue.http.headers.common['X-CSRFToken'] = "{{ csrf_token }}";

var app2 = new Vue({
  el: '#app-2',
  delimiters: ['[[', ']]'],
  data: {
    message: 'You loaded this page on ' + new Date().toLocaleString(),
    notes: [],
    description: '',
    category: '',
    severity: '',
    created_at: '',
    new_note: ''

  },
  methods: {
    moment: function(){
      return moment();
    },
    getNotes: function() {
      console.log('Started')
      let api_url = '/api/patients/notes/1';
      axios.get(api_url)
        .then((response) => {
          this.notes = response.data;
        })
        .catch((err) => {
          console.log(err);
        })
    },
    postNote: function() {
      console.log('Reached')
      let api_url = '/api/patients/notes/1';
      const category = document.getElementById('category').value;
      const severity = document.getElementById('severity').value;
      console.log(category);
      console.log(severity);
    }
  },
  mounted() {
    this.getNotes()
  },
  filters: {
    timeFromNow: function(date) {
      return moment(date).fromNow();
    }
  },
})

var app = new Vue({
  el: '#add-note',
  delimiters: ['[[', ']]'],
  data: {
    description: '',
    category: 'default',
    severity: 'default',
  },
  methods: {
    postNote: function() {
      console.log('Reached')
      let api_url = '/api/patients/notes/1';
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFToken';

      axios.post(api_url, {
        patient: 1,
        notes: this.description,
        category: this.category,
        severity: this.severity
      }).then((response) => {
        console.log('Note added');
        this.description = ''
        this.category = 'default'
        this.severity = 'default'
        app2.getNotes()
      })
      .catch((err) => {
        console.log('FAILED');
        console.log(err);
      })
    }
  }
})

var app3 = new Vue({
  el: '#activities-section',
  delimiters: ['[[', ']]'],
  data: {
    activities: [],
    activityName: '',
    description: '',
    intensity: 'default'
  },
  methods: {
    moment: function(){
      return moment();
    },
    getActivities: function () {
      console.log('Readched app3');
      let api_url = '/api/patients/activities/1';
      axios.get(api_url)
        .then((response) => {
          this.activities = response.data;
        })
        .catch((err) => {
          console.log(err);
        })
    },
    postActivity: function() {
      let api_url = '/api/patients/activities/1';
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFToken';

      axios.post(api_url, {
        patient: 1,
        name: this.activityName,
        description: this.description,
        intensity: this.intensity
      }).then((response) => {
        this.activityName = '',
        this.description = '',
        this.intensity = 'default'
        app3.getActivities()
      })
      .catch((err) => {
        console.log('FAILED');
        console.log(err);
      })
    }
  },
  mounted() {
    this.getActivities()
  },
  filters: {
    timeFromNow: function(date) {
      return moment(date).fromNow();
    }
  },
})


var app4 = new Vue({
  el: '#list-home',
  delimiters: ['[[', ']]'],
  data: {
    metrics: []
  },
  methods: {
    moment: function(){
      return moment();
    },
    getMetrics: function () {
      console.log('REACHED THIS ONE');
      var metrics = ['blood-sugar', 'pulse', 'temp', 'weight']
      for (metric of metrics) {
        let api_url = '/api/patients/' + metric + '/1';
        console.log(api_url)
        axios.get(api_url)
          .then((response) => {
            this.metrics.push(response.data);
          })
          .catch((err) => {
            console.log(err);
          })
      }
    },
    postBloodSugar: function() {
      let api_url = '/api/patients/blood-sugar/1';
      axios.defaults.xsrfCookieName = 'csrftoken';
      axios.defaults.xsrfHeaderName = 'X-CSRFToken';

      axios.post(api_url, {
        patient: 1,
        entry: this.bloodSugar
      }).then((response) => {
      })
      .catch((err) => {
        console.log('FAILED');
        console.log(err);
      })
    }
  },
  mounted() {
    this.getMetrics()
  },
  filters: {
    timeFromNow: function(date) {
      return moment(date).fromNow();
    }
  },
})
