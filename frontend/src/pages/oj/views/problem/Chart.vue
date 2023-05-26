<template>
  <div>
    <canvas ref="chartCanvas"></canvas>
  </div>
</template>

<script>
import { Bar } from 'vue-chartjs';

export default {
  extends: Bar,
  props: {
    chartData: {
      type: Object,
      required: true
    },
    chartOptions: {
      type: Object,
      default: () => ({})
    }
  },
  mounted () {
    this.renderChart(this.chartData, this.chartOptions);
  }
};
</script>

<style>
/* 스타일링을 추가할 수 있습니다. */
</style>
