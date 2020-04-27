<template>
  <div class="text">
    <h3 class="clearfix">
      <router-link to="/" class="btn btn-default pull-right">Back to Texts List</router-link>
      <span class="text-muted">Text Title:</span>
      {{text.title}}
    </h3>
    <table class="table table-condensed table-striped table-hover">
      <thead>
      <tr>
        <th>#</th>
        <th>Sentence</th>
        <th></th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="sentence in text.sentences"
          :key="sentence.id"
          >
        <td>{{sentence.number}}</td>
        <td>{{sentence.content}}</td>
        <td>
          <router-link :to="`/text/${text_id}/sentence/${sentence.id}`" class="btn btn-default">Show Similar</router-link>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: 'TextSentences',
  data: () => ({
    text: {},
    is_loading: true
  }),
  computed: {
    text_id () {
      return this.$route.params.text_id
    }
  },
  created () {
    this.fetchText()
  },
  methods: {
    fetchText () {
      const url = '/api/text/' + this.text_id + '/'
      axios
        .get(url)
        .then(resp => {
          this.text = resp.data
        })
        .catch(err => {
          console.log(err)
        })
    }
  }
}
</script>
