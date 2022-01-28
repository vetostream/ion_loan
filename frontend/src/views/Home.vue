<template>
  <div class="home">
  </div>
</template>

<script>

export default {
  name: 'Home',
  filters: {
    longDate (date) {
      return date.toDateString();
    }
  },
  data() {
    return {
    }
  },
}
</script>

<style>
</style>