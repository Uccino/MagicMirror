<template>
  <div id="wrapper">
    <section class="section">
      <div class="columns is-multiline">
        <div class="column is-4">
          <time-component/>
        </div>
        <div class="column is-4">
          <message-of-the-day/>
        </div>
        <div class="column is-3">
          <weather/>
        </div>
        <div class="column is-4"></div>
      </div>
    </section>
    <div>
      <websocket-button/>
    </div>
  </div>
</template>

<script>
import weather from "./LandingPage/Weather";
import TimeComponent from "./LandingPage/TimeComponent";
import MessageOfTheDay from "./LandingPage/MessageOfTheDay";
import WebsocketButton from "./LandingPage/WebsocketButton";

export default {
  name: "landing-page",
  components: { weather, TimeComponent, MessageOfTheDay, WebsocketButton },
  methods: {
    open(link) {
      this.$electron.shell.openExternal(link);
    }
  }
};
</script>

<style>
/* @import url("https://fonts.googleapis.com/css?family=Source+Sans+Pro"); */
html{
    overflow:hidden!important;
}

body{    
    background-color:black;
    height: 100vh;    
    color: white!important;   
    font-size: 20px; 
}

</style>
