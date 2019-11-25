<template>
  <div>
    <button @click="clickButton" class="button">Send 'hoi'</button>
  </div>
</template>

<script>
export default {
  name: "WebsocketButton",
  methods: {
    clickButton: function(val) {
        // verstuur hoi (Alleen 'hoi' als string)
      // $socket is [WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket) instance
      this.$socket.send("hoi");
      // or with {format: 'json'} enabled (<- wat hij in het engels zei) -< 't kan zijn dat dit niet werkt
      this.$socket.sendObj({ awesome: "data" });
    }
  },
  created () {
    //   Luister naar websocket (ik heb dit niet kunnen testen want heb geen ws :P)
    this.$options.sockets.onmessage = (data) => this.messageReceived(data)
  },
};
</script>

<style lang="scss" scoped>
</style>