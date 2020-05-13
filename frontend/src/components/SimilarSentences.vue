<template>
  <div class="similar">
    <div v-if="is_loading">
      <p>Loading Similar Sentences...</p>
    </div>

    <div v-else>
      <h3>Similar Texts</h3>

      <div v-for="similar_text in similar_texts"
           :key="similar_text.text.id">
        <h4>
          <span class="text-muted">Text:</span>&nbsp;
          <router-link :to="'/text/' + similar_text.text.id">{{similar_text.text.title}}</router-link>
        </h4>
        <table class="table table-condensed table-striped table-hover">
          <thead>
          <tr>
            <th style="width: 15%">Text</th>
            <th class="text-right">#</th>
            <th>Score</th>
            <th style="width: 75%">Sentence</th>
          </tr>
          </thead>
          <tbody>
          <tr v-for="item in similar_text.similar_sentences"
              :key="item.sentence.id"
              >
            <td>
              <router-link :to="`/text/${item.sentence.text.id}`">{{item.sentence.text.title}}</router-link>
            </td>
            <td class="text-right">
              <router-link :to="`/text/${item.sentence.text.id}/sentence/${item.sentence.id}`">{{item.sentence.number}}</router-link>
            </td>
            <td>{{item.similarity.toFixed(4)}}</td>
            <td>{{item.sentence.content}}</td>
          </tr>
          </tbody>
        </table>
      </div>
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
    similar_texts: []
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
          this.similar_texts = resp.data
        })
        .catch(this.apiErrorHandler('Fetching similar sentences'))
        .finally(() => {
          this.is_loading = false
        })
    }
  }
}
</script>
