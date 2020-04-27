<template>
  <div class="similar">
    <div v-if="is_loading">
      <p>Loading Similar Sentences...</p>
    </div>

    <div v-else>
      <h3>Similar Sentences</h3>
      <table class="table table-condensed table-striped table-hover">
        <thead>
        <tr>
          <th>#</th>
          <th>Score</th>
          <th>Sentence</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="item in similar"
            :key="item.sentence.id"
            >
          <td>
            <router-link :to="`/text/${text_id}/sentence/${item.sentence.id}`">{{item.sentence.number}}</router-link>
          </td>
          <td>{{item.similarity.toFixed(4)}}</td>
          <td>{{item.sentence.content}}</td>
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
  name: 'SimilarSentences',
  mixins: [
    ApiErrorsHandlerMixin
  ],
  props: {
    text_id: String,
    sentence_id: String
  },
  data: () => ({
    is_loading: false,
    similar: []
  }),
  created () {
    this.fetchSimilar()
  },
  methods: {
    fetchSimilar () {
      const url = `/api/text/${this.text_id}/sentence/${this.sentence_id}/similar/`
      this.is_loading = true
      axios
        .get(url)
        .then(resp => {
          this.similar = resp.data
        })
        .catch(this.apiErrorHandler('Fetching similar sentences'))
        .finally(() => {
          this.is_loading = false
        })
    }
  }
}
</script>
