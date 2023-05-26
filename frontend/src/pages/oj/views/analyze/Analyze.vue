<template>
  <div class="app">
    <h1>{{ pageTitle }}</h1>
    <img :src="imageSrc" alt="Sample Image" />
    <p>{{ description }}</p>
  </div>
</template>

<script>
export default {
  data () {
    return {
      pageTitle: "Welcome to My Website",
      imageSrc: "https://example.com/sample-image.jpg",
      description: "This is a sample website with text and image."
    };
  }
};
</script>

<style>
.app {
  text-align: center;
  margin-top: 50px;
}
img {
  max-width: 400px;
  margin: 20px auto;
}
</style>
