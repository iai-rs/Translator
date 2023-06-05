<template>
  <div class="container">
    <div class="container1">
      <div class="language-select box">
        <select @click="change_input_lang" v-model="input_lang">
          <option value="sr">Serbian</option>
          <option value="en">English</option>
          <option value="zh">Chinise</option>
          <option value="es">Spanish</option>
          <option value="de">German</option>
          <option value="fr">French</option>
          <option value="el">Greek</option>
          <option value="he">Hebrew</option>
          <option value="hr">Croatian</option>
          <option value="bs">Bosinian</option>
          <option value="sl">Slovenian</option>
          <option value="mk">Macedonian</option>
          <option value="hu">Hungarian</option>
        </select>
      </div>
      <div class="button-container box">
        <button @click="swith" id="btnSwitchLang">
          ↔
        </button>
      </div>
      <div class="language-select box">
        <select @click="change_output_lang" v-model="output_lang">
          <option value="sr">Serbian</option>
          <option value="en">English</option>
          <option value="zh">Chinise</option>
          <option value="es">Spanish</option>
          <option value="de">German</option>
          <option value="fr">French</option>
          <option value="el">Greek</option>
          <option value="he">Hebrew</option>
          <option value="hr">Croatian</option>
          <option value="bs">Bosinian</option>
          <option value="sl">Slovenian</option>
          <option value="mk">Macedonian</option>
          <option value="hu">Hungarian</option>
        </select>
      </div>
    </div>
    <div class="textareas-container">
      <textarea v-model="input_text" placeholder="Enter text"></textarea>
      <textarea v-model="output_text" placeholder="Translated text" disabled></textarea>
    </div>

    <div class="button-container">
      <button @click="translate" id="btnTranslate">Translate</button>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      input_text: '',
      output_lang: 'en',
      input_lang: 'sr',
      output_text: ''
    };
  },
  methods: {
    translate() {
      fetch(process.env.VUE_APP_API_ENDPOINT+'/translate', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          input_text: this.input_text,
          output_lang: this.output_lang,
          input_lang: this.input_lang
        })
      })
        .then(response => {
          if (response.status === 500) {
            throw response;
          } else if (response.status !== 200) {
            throw response.json();
          }
          return response.json();
        })
        .then(data => {
          this.output_text = data.message
        })
        .catch(error => {
          if (typeof error.then === 'function') {
            error.then(error => {
              this.$swal(error.error);
            })
          } else {
            this.$swal(error.statusText);
          }
        });
    },

    swith() {
      let output_lang = this.output_lang;
      let input_lang = this.input_lang;
      let output_text = this.output_text;
      let input_text = this.input_text;
      this.input_lang = output_lang;
      this.output_lang = input_lang;
      this.output_text = input_text;
      this.input_text = output_text;
    },
    change_input_lang() {
    },
    change_output_lang() {

    }
  }
};
</script>

<style>
@import '../styles/styles.css';
</style>
