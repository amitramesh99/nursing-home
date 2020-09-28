Vue.component('video-chat', {
  delimiters: ['[[', ']]'],
  data: function(){
    return{
      token: null,
      params: {},
      VID: '',
      VIDInput: '',
      previewTracks: null,
      isMuted: false,
      isVideoOff: false,
      activeRoom: {
        participants: {},
        state: '',
        localParticipant: {},
      },
      activeRoomChangeTracker: 0,
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
        // container.appendChild(track.attach());
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
      this.detachTracks(tracks);
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
      // var previewContainer = this.$refs.preview;
      // if (!previewContainer.querySelector('video')) {
      //   this.attachParticipantTracks(room.localParticipant, previewContainer);
      // }

      room.participants.forEach((participant) => {
        console.log("Already in Room: '" + participant.identity + "'");
        var previewContainer = this.$refs.remoteMedia;
        this.attachParticipantTracks(participant, previewContainer);
      });

      // When a participant joins, draw their video on screen
      room.on('participantConnected', function(participant) {
        this.activeRoomChangeTracker += 1;
        console.log("Joining: '" + participant.identity + "'");        
      });
      
      room.on('trackAdded', (track, participant) => {
        this.activeRoomChangeTracker += 1;
        console.log(participant.identity + " added track: " + track.kind);
        var previewContainer = this.$refs.remoteMedia;
        this.attachTracks([track], previewContainer);
      });

      room.on('trackRemoved', (track, participant) => {
        this.activeRoomChangeTracker += 1;
        console.log(participant.identity + " removed track: " + track.kind);
        this.detachTracks([track]);
      });

      // When a participant disconnects, note in log
      room.on('participantDisconnected', (participant) => {
        this.activeRoomChangeTracker += 1;
        console.log("Participant '" + participant.identity + "' left the room");
        this.detachParticipantTracks(participant);
      });

      // When we are disconnected, stop capturing local video
      // Also remove media for all remote participants
      room.on('disconnected', () => {
        this.activeRoomChangeTracker += 1;
        console.log('Left');
        this.detachParticipantTracks(room.localParticipant);
        room.participants.forEach(this.detachParticipantTracks);
        Object.assign(this.$data, this.$options.data.apply(this));
        this.refreshToken();
        // document.getElementById('button-join').style.display = 'inline';
        // document.getElementById('button-leave').style.display = 'none';
      });
    },

    leaveRoomIfJoined: function(){
      // todo
      alert("Leaving call");
    },

    //Controls:
    getButtonClass: function(isActive){
      return isActive ? 'btn-danger': 'btn-success';
    },

    toggleMute: function(){
      let audioTracks = this.activeRoom.localParticipant.audioTracks;

      if(this.isMuted){
        audioTracks.forEach(function(track, trackId) {
          track.enable();
        });
      }
      else{
        audioTracks.forEach(function(track, trackId) {
          track.disable();
        });
      }

      this.isMuted = !this.isMuted;
    },

    toggleVideo: function(){
      let videoTracks = this.activeRoom.localParticipant.videoTracks;

      if(this.isVideoOff){
        videoTracks.forEach(function(track, trackId) {
          track.enable();
        });
      }
      else{
        videoTracks.forEach(function(track, trackId) {
          track.disable();
        });
      }

      this.isVideoOff = !this.isVideoOff;
    },

    leaveCall: function(){
      console.log("Leaving call...");
      this.activeRoom.disconnect();
    },
  },
  computed: {
    participants: function(){
      console.log("Re-computing participantTracks");
      // if(!this.activeRoom || this.activeRoom.participants.size <= 0){
      //   return null;
      // }
      console.log(this.activeRoom.localParticipant);
      return this.activeRoomChangeTracker && Array.from(this.activeRoom.participants.values());
    }
  },
  mounted: function(){
    console.log(this.activeRoom);
  },
  template: `
    <div class="container-fluid h-100">
      <div v-if="!activeRoom.state" class="row h-100 align-items-center">
        <div class="col">

          <div class="my-2 mx-auto" style="width:500px;" ref="joinCallForm">
            <h1 class="mb-4">Join an Acrusis Video Call</h1>
            <form @submit.prevent="joinCallFormSubmit" alutocomplete="off" class="form-inline justify-content-center">
              <input v-model="VIDInput" placeholder="Enter your call ID" name="vid" class="form-control form-control-lg mr-2"></input>
              <button class="btn btn-lg btn-primary" type="submit">
                Join Call
              </button>
            </form>
          </div>

        </div>
      </div>

      <div v-else class="row h-100">
        <div class="col h-100 px-0">
          <div ref="remoteMedia" class="h-100 bg-dark">
            <video-grid
              v-bind:participants="participants"
            ></video-grid>
            <div id="previewVideoContainer">
              <video-stream v-bind:participant="activeRoom.localParticipant"></video-stream>
            </div>
            <div id="videoControlsContainer" class="justify-content-between">
              <button class="btn btn-lg" @click="toggleMute" :class="getButtonClass(isMuted)">
                <span class="fa fa-microphone-slash"></span>
              </button>
              <button class="btn btn-lg" @click="toggleVideo" :class="getButtonClass(isVideoOff)">
                <span class="fa fa-video-camera"></span>
              </button>
              <button class="btn btn-lg btn-secondary" @click="leaveCall">
                <span class="fa fa-times"></span>
              </button>

              </div>
          </div>
        </div>
      </div>
    </div>
  `,
});

Vue.component('video-grid', {
  delimiters: ['[[', ']]'],
  props: ['participants'],
  computed: {
    participantMatrix: function(){
      let n = this.participants.length;
      let numRows = Math.round(Math.sqrt(n));
      let numCols = Math.ceil(Math.sqrt(n));

      var matrix = [];
      for(i=0; i<numRows; i++){
        let startIndex = i * numCols;
        let endIndex = (startIndex + numCols);
        matrix.push(this.participants.slice(startIndex, endIndex));
      }
      return matrix;

    },
    displayWaitingMessage: function(){
      console.log("partcipant change fired");
      return !(this.participants && this.participants.length > 0);
    },

  },
  beforeMount: function(){
    // alert("Before mount");
  },
  //TODO: 
  // * Rows not working as expected inside flex container
  // * Video keeps resizing during call
  // * Video not taking up full size of container
  template: `
    <div class="d-flex h-100 align-items-center justify-content-center">
      <div class="row" v-for="row in participantMatrix">
        <div class="col" v-for="participant in row">
          <video-stream v-bind:participant="participant"></video-stream>
        </div>
      </div>
      <div v-if="displayWaitingMessage" class="mx-auto">
        <h3 class="text-light">Waiting for participants to join...</h3>
      </div>
    </div>
  `,
});

Vue.component('video-stream', {
  delimiters: ['[[', ']]'],
  props: ['participant'],
  methods: {
    attachTracks: function(tracks, container) {
      tracks.forEach(function(track) {
        container.appendChild(track.attach());
      });
    },
  },
  mounted: function(){
    if(this.participant){
      let container = this.$refs[this.participant.identity];
      let tracks = Array.from(this.participant.tracks.values());
      this.attachTracks(tracks, container);
    }
    else{
      console.log("No participant");
    }

  },
  template: `
    <div v-if="participant" :ref="participant.identity" class="video-container"></div>
  `,
});

const videoChatWidget = new Vue({
  el: '#video-chat',
});
