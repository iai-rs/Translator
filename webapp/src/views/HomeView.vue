<template>
    <div class="container">
      <a href="https://www.ivi.ac.rs"><img class="logo" src="../assets/logo2.png"/></a>
    <h1>Translator</h1>
  </div>
    <translation-form></translation-form>
    <div class="container">
      This is a demo of a project. More info  <a href="https://github.com/iai-rs/Translator">here</a>
  </div>

</template>

<script>
import TranslationForm from '../components/TranslationForm.vue';

export default {
  components: {
    TranslationForm
  },
  created(){
        document.title = "Translator"
    }
};
</script>

<style>
@import '../styles/styles.css';
@import 'sweetalert2/dist/sweetalert2.min.css';
</style>
