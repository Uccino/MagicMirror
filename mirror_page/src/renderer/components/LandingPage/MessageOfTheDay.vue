<template>
  <div>
    <p id="messageoftheday">Message of the day!</p>
  </div>
</template>

<script>
export default {
  name: "MessageOfTheDay"
};
</script>

<style lang="scss" scoped>
#messageoftheday{
    position: absolute;
    bottom: 20px;
    left: auto;
    right: auto;
}
</style>