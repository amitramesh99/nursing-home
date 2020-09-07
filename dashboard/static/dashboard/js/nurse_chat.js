Vue.component('chat', {
  delimiters: ['[[', ']]'],
  data: function(){
    return{
      token: '',
      chatClient: null,
      channel: {
        'friendlyName': 'Loading Chat...',
      },
      messageInput: '',
      messages: [],
    }
  },
  created: function(){
    this.refreshToken()
      .then(() => {
        Twilio.Chat.Client.create(this.token).then(client => {
          this.chatClient = client;
          this.chatClient.getSubscribedChannels().then(this.createOrJoinChannel);

          // when the access token is about to expire, refresh it
          this.chatClient.on('tokenAboutToExpire', () => {
            this.refreshToken();
          });

          // if the access token already expired, refresh it
          this.chatClient.on('tokenExpired', () => {
            this.refreshToken();
          });

        }).catch(error => {
          console.log('There was an error creating the chat client:');
          console.log(error);
        });
      })
      .catch((error) => {
        console.log("Error fetching Twilio token:");
        console.log(error);
      });
  },
  updated: function(){
    this.$refs.messageContainer.scrollTop = this.$refs.messageContainer.scrollHeight;
  },
  methods: {
    moment: function(){
      return moment();
    },
    refreshToken: function() {
      return axios.get('/token').then((response) => this.token = response.data);
    },
    createOrJoinChannel: function() {
      console.log('Attempting to join chat channel...', );
      this.chatClient.getChannelByUniqueName(chatId)
      .then((channel) => {
        this.channel = channel;
        console.log('Found patient channel:');

        this.setupChannel();
      }).catch((error) => {
        console.log(error);
        // If it doesn't exist, let's create it
        console.log('Creating patient channel');
        this.chatClient.createChannel({
          uniqueName: chatId,
          friendlyName: patient.name + ' Chat Channel'
        }).then((channel) => {
          console.log('Created channel:');
          console.log(channel);
          this.channel = channel;
          this.setupChannel();
        }).catch((channel) => {
          console.log('Channel could not be created:');
          console.log(channel);
        });
      });
    },
    setupChannel: function(){
      // Set up channel after it has been found
      if(this.channel.channelState.status !== "joined"){
        console.log("User has not joined channel");
        this.channel.join().then((channel) => {
          console.log('Joined channel');
        });
      }
      else{
        console.log("User already joined");
      }
      // Get Messages for a previously created channel
      console.log("Retrieving previous messages...");
      this.channel.getMessages().then((messages) => {
        const totalMessages = messages.items.length;
        this.messages.push(...messages.items);
      })
      .catch((err) => console.log(err));

      // Listen for new messages sent to the channel
      this.channel.on('messageAdded', (message) => this.messages.push(message));
      console.log("Listening for new messages");
    },
    messageFormSubmit: function(e){
      e.preventDefault();
      if(this.messageInput){
        this.channel.sendMessage(this.messageInput);
        this.messageInput = "";
      }
    }
  },
  filters: {
    timeFromNow: function(date) {
      return moment(date).fromNow();
    }
  },
  template: `
    <div class="pt-2">
      <div ref="messageContainer" style="max-height: 500px; overflow:auto">
        <div class="card mb-2 mx-2" v-for="message in messages">
          <div class="card-body">
            <h6 class="card-subtitle mb-2">
              [[message.author]]
              <small class="text-muted">[[ message.dateCreated | timeFromNow ]]</small></h6>
            <p class="card-text">[[ message.body ]]</p>
          </div>
        </div>
      </div>
      <form @submit="messageFormSubmit" class="">
        <div class="input-group">
          <input v-model=messageInput placeholder="Send a message" class="form-control form-control-lg rounded-0 border-top"></input>
          <div class="input-group-append">
            <button class="btn btn-primary rounded-0" type="button">
              <span class="fa fa-paper-plane"></span>
            </button>
          </div>
        </div>
      </form>
    </div>
  `,
});
const chatWidget = new Vue({
  el: '#chat',
});
