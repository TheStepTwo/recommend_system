<template>
  <v-app>
    <v-content>
      <keep-alive include="Main" >
        <router-view/>
      </keep-alive>
    </v-content>
  </v-app>
</template>

<script>

export default {
  name: 'App',
  data: () => ({
    //
  }),
};
</script>

<style lang="scss">
  @import './assets/css/style.css';
</style>
