<template>
  <div>
    <span class="time">{{ computedTime }}</span>
  </div>
</template>

<script>
import * as moment from "moment";

export default {
  name: "TimeComponent",
  computed: {
    computedTime() {
      return this.this_time;
    }
  },
  data() {
    return {
      timeInterval: "",
      this_time: null
    };
  },
  mounted() {
    this.setTime();
    this.timeInterval = setInterval(() => {
      this.setTime();
    }, 1000);
  },
  methods: {
    setTime() {
      this.this_time = moment().format("LLLL");
    }
  },
  beforeDestroy: function() {
    clearInterval(this.timeInterval);
  }
};
</script>

<style lang="scss" scoped>
.time {
  font-size: 50px;
}
</style>