<template>
  <div style="text-align: center; display: flex; justify-content: center;">
    <img id="slogan"
      src="@/assets/slogan.png"
      alt="comodo"
    >
  </div>
</template>

<script>

export default {
  name: "Home",
  data () {
    return {};
  },
  async mounted () {
  },
  methods: {}
}
</script>

<style>
  #slogan {
    width: 600px;
    margin-left: auto;
    margin-right: auto;
    margin-top: 100px;
    display: block;
  }
</style>
