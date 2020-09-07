Vue.component('video-chat', {
  delimiters: ['[[', ']]'],
  data: function(){
    return{
      token: null,
      params: {},
      VID: '',
      VIDInput: '',
      previewTracks: null,
      activeRoom: null,
    }
  },
  created: function(){
    this.getURLParams();
    if(this.params.vid){
      this.VIDInput = this.params.vid;
    }

    // Check for WebRTC
    if (!navigator.webkitGetUserMedia && !navigator.mozGetUserMedia) {
      alert('WebRTC is not available in your browser.');
    }

    // When we are about to transition away from this page, disconnect
    // from the room, if joined.
    window.addEventListener('beforeunload', this.leaveRoomIfJoined);

    this.refreshToken()
      .then(() => {
        console.log("Got twilio token");
      })
      .catch((error) => {
        console.log("Error fetching Twilio token:");
        console.log(error);
      });
  },
  methods: {
    getURLParams: function(){
      let uri = window.location.href.split("?");
      if (uri.length == 2){
        let vars = uri[1].split('&');
        let getVars = {};
        let tmp = '';
        vars.forEach(function(v){
          tmp = v.split('=');
          if(tmp.length == 2)
          getVars[tmp[0]] = tmp[1];
        });
        this.params = getVars;
      }
    },
    // twilio helper functions
    refreshToken: function() {
      return axios.get('/token/video').then((response) => this.token = response.data);
    },
    attachTracks: function(tracks, container) {
      tracks.forEach(function(track) {
        container.appendChild(track.attach());
      });
    },
    attachParticipantTracks: function(participant, container) {
      console.log(participant.tracks);
      console.log(participant.tracks.values());

      var tracks = Array.from(participant.tracks.values());
      this.attachTracks(tracks, container);
    },
    detachTracks: function(tracks) {
      tracks.forEach(function(track) {
        track.detach().forEach(function(detachedElement) {
          detachedElement.remove();
        });
      });
    },
    detachParticipantTracks: function(participant) {
      var tracks = Array.from(participant.tracks.values());
      detachTracks(tracks);
    },
    // button event handlers
    previewVideoHandler: function(){
      console.log("Called previewVideoHandler");
      var localTracksPromise = this.previewTracks
      ? Promise.resolve(this.previewTracks)
      : Twilio.Video.createLocalTracks();

      localTracksPromise.then((tracks) => {
        this.previewTracks = tracks;
        var previewContainer = this.$refs.preview;
        if (!previewContainer.querySelector('video')) {
          this.attachTracks(tracks, previewContainer);
        }
      }, function(error) {
        console.error('Unable to access local media', error);
        log('Unable to access Camera and Microphone');
      });
    },
    joinCallFormSubmit: function(e){
      e.preventDefault();
      if(this.VIDInput){
        var connectOptions = { name: this.VIDInput, logLevel: 'error' };
        if (this.previewTracks) {
          connectOptions.tracks = this.previewTracks;
        }

        Twilio.Video.connect(this.token, connectOptions).then(this.joinedRoom, function(error) {
          console.log('Could not connect to Twilio: ' + error.message);
        });

      }
      else{
        alert("Enter a call ID");
      }
    },

    joinedRoom: function(room) {
      this.activeRoom = room;

      console.log("Joined room sucessfully");
      // document.getElementById('button-join').style.display = 'none';
      // document.getElementById('button-leave').style.display = 'inline';

      // Draw local video, if not already previewing
      var previewContainer = this.$refs.preview;
      if (!previewContainer.querySelector('video')) {
        this.attachParticipantTracks(room.localParticipant, previewContainer);
      }

      room.participants.forEach((participant) => {
        console.log("Already in Room: '" + participant.identity + "'");
        var previewContainer = this.$refs.remoteMedia;
        this.attachParticipantTracks(participant, previewContainer);
      });

      // When a participant joins, draw their video on screen
      room.on('participantConnected', function(participant) {
        console.log("Joining: '" + participant.identity + "'");
      });

      room.on('trackAdded', (track, participant) => {
        console.log(participant.identity + " added track: " + track.kind);
        var previewContainer = this.$refs.remoteMedia;
        this.attachTracks([track], previewContainer);
      });

      room.on('trackRemoved', (track, participant) => {
        console.log(participant.identity + " removed track: " + track.kind);
        this.detachTracks([track]);
      });

      // When a participant disconnects, note in log
      room.on('participantDisconnected', (participant) => {
        console.log("Participant '" + participant.identity + "' left the room");
        this.detachParticipantTracks(participant);
      });

      // When we are disconnected, stop capturing local video
      // Also remove media for all remote participants
      room.on('disconnected', () => {
        console.log('Left');
        this.detachParticipantTracks(room.localParticipant);
        room.participants.forEach(detachParticipantTracks);
        this.activeRoom = null;
        // document.getElementById('button-join').style.display = 'inline';
        // document.getElementById('button-leave').style.display = 'none';
      });
    },


    leaveRoomIfJoined: function(){
      // todo
      alert("Leaving call");
    },
  },
  template: `
    <div class="container-fluid bg-light">
      <div class="row py-4">
        <div class="col">

          <div class="my-5 mx-auto" style="width:500px;" ref="joinCallForm">
            <h2>Join Video Call</h2>
            <form @submit="joinCallFormSubmit" autocomplete="off" class="form-inline">
              <input v-model="VIDInput" placeholder="Enter your call ID" name="vid" class="form-control form-control-lg mr-2"></input>
              <button class="btn btn-lg btn-primary" type="submit">
                Join Call
              </button>
            </form>
          </div>

        </div>
      </div>

      <div class="row">
        <div class="col">
          <div class="my-5 mx-auto" style="width:500px;" ref="joinCallForm">

            <div ref="preview" id="previewVideoContainer" style="height: 202px; width:270px" class="bg-dark"></div>
            <button @click="previewVideoHandler" class="btn btn-secondary mt-2">Preview Video</button>

          </div>
        </div>
      </div>

      <div class="row">
        <div class="col">
          <div ref="remoteMedia" style="height: 500px; width:1200px"></div>
        </div>
      </div>

    </div>
  `,
});
const videoChatWidget = new Vue({
  el: '#video-chat',
});
