<template>
  <div>
    <div class="module" id="module" style="width: 100%;">
      <div class="weather">
        <p class="weather-title">Arnhem, the Netherlands.</p>
        <p class="weather-current-forecast">
          <i class="wi wi-day-rain fa-2x"></i> 24°C, Raining
        </p>
        <hr class="weather-hr">
        <table class="weather-table">
          <tr class="weather-table-head">
            <th></th>
            <th></th>
            <th>Max</th>
            <th>Min</th>
          </tr>
          <tr>
            <th>Dinsdag</th>
            <th>
              <i class="wi wi-day-sunny"></i>
            </th>
            <th>25°C</th>
            <th>2°C</th>
          </tr>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: "Weather"
};
</script>

<style lang="scss" scoped>
.weather {
  width: 75%;
  font-size: 20px;
}

.weather-title {
  font-size: 23px;
  margin-bottom: 10px;
}

.weather-hr {
  background: white!important;
}

.weather-table {
  width: 100%;
  color: white!important;
}
</style>