<template>
  <div class="home">
    <div class="text-form">
      <h2>New Text</h2>
      <form @submit="submitText" onsubmit="return false;">
        <div class="form-group">
          <input v-model="new_text.title"
                 :disabled="form_loading"
                 class="form-control" type="text" maxlength="200" placeholder="Title" autofocus>
        </div>
        <div class="form-group">
          <textarea v-model="new_text.content"
                    :disabled="form_loading"
                    class="form-control" placeholder="Text here..." rows="6"></textarea>
        </div>
        <button type="submit" class="btn btn-default" :disabled="!allow_form_submit">
          <span v-if="form_loading">Submitting...</span>
          <span v-else>Submit</span>
        </button>
      </form>
    </div>

    <hr/>

    <h2>Texts</h2>

    <div v-if="text_loading" class="loading">
      Loading Texts...
    </div>

    <div v-else>
      <table class="table table-condensed table-hover table-striped">
        <thead>
        <tr>
          <th>#</th>
          <th style="width: 50%">Title</th>
          <th>Created At</th>
          <th></th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="text in text_list"
            :key="text.id"
            >
          <td>{{text.id}}</td>
          <td><router-link :to="'/text/' + text.id">{{ text.title }}</router-link></td>
          <td>{{ new Date(text.created_at).toLocaleString() }}</td>
          <td><button v-on:click="removeText(text.id)" class="btn btn-default btn-sm">Remove</button></td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TextsList',
  data: () => ({
    new_text: {
      title: '',
      content: ''
    },
    form_loading: false,
    text_loading: false,
    text_list: []
  }),
  computed: {
    allow_form_submit () {
      return this.new_text.title.length && this.new_text.content.length && !this.form_loading
    }
  },
  created () {
    this.fetchTexts()
  },
  methods: {
    fetchTexts () {
      this.text_loading = true
      this.text_list = []
      axios
        .get('/api/text/')
        .then(resp => {
          this.text_list = resp.data
        })
        .catch(err => {
          console.log(err)
        })
        .finally(() => {
          this.text_loading = false
        })
    },
    submitText () {
      this.form_loading = true
      axios
        .post('/api/text/', this.new_text)
        .then(resp => {
          this.fetchTexts()
        })
        .catch(err => {
          console.log(err)
        })
        .finally(() => {
          this.form_loading = false
          this.resetForm()
        })
      return false
    },
    resetForm () {
      this.new_text.title = ''
      this.new_text.content = ''
    },
    removeText (textId) {
      if (confirm('Are you sure to delete this text?')) {
        axios
          .delete(`/api/text/${textId}/`)
          .then(resp => {
            this.fetchTexts()
          })
          .catch(err => {
            console.log(err)
          })
      }
    }
  }
}
</script>
