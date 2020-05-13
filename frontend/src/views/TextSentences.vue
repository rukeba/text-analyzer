<template>
  <div class="text">
    <div v-if="is_loading">
      Loading text...
    </div>

    <div v-else>
      <h3 class="clearfix">
        <router-link to="/" class="btn btn-default pull-right">Back to Texts List</router-link>
        <span class="text-muted">Text:</span>
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
          <td>
            <router-link :to="`/text/${text_id}/sentence/${sentence.id}`">
              {{sentence.number}}
            </router-link>
          </td>
          <td>{{sentence.content}}</td>
          <td>
            <router-link :to="`/text/${text_id}/sentence/${sentence.id}`" class="btn btn-default btn-sm">Show Similar</router-link>
          </td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script>
import axios from 'axios'
import { ApiErrorsHandlerMixin } from '@/api/api-errors-handler-mixin'

export default {
  name: 'TextSentences',
  mixins: [
    ApiErrorsHandlerMixin
  ],
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
      this.is_loading = true
      axios
        .get(url)
        .then(resp => {
          this.text = resp.data
        })
        .catch(this.apiErrorHandler('Fetching text with sentences'))
        .finally(() => {
          this.is_loading = false
        })
    }
  }
}
</script>
