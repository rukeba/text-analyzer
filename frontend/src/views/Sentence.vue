<template>
  <div v-if="is_loading">
    Loading...
  </div>

  <div v-else>
    <h3>
      <router-link :to="`/text/${text_id}/`" class="btn btn-default pull-right">Back to Text</router-link>
      Source Sentence <span class="text-muted small">#{{sentence.number}}</span>
    </h3>
    <p class="alert alert-info">{{sentence.content}}</p>

    <SimilarSentences v-if="sentence" v-bind:text_id="text_id" v-bind:sentence_id="sentence_id">
    </SimilarSentences>
  </div>
</template>

<script>
import axios from 'axios'
import { ApiErrorsHandlerMixin } from '@/api/api-errors-handler-mixin'
import SimilarSentences from '@/components/SimilarSentences'

export default {
  name: 'Sentence',
  mixins: [
    ApiErrorsHandlerMixin
  ],
  components: {
    SimilarSentences
  },
  data: () => ({
    sentence: {},
    is_loading: true
  }),
  computed: {
    text_id () {
      return this.$route.params.text_id
    },
    sentence_id () {
      return this.$route.params.sentence_id
    }
  },
  created () {
    this.fetchSentence()
  },
  methods: {
    fetchSentence () {
      const url = `/api/text/${this.text_id}/sentence/${this.sentence_id}/`
      this.is_loading = true
      axios
        .get(url)
        .then(resp => {
          this.sentence = resp.data
        })
        .catch(this.apiErrorHandler('Fetching sentence'))
        .finally(() => {
          this.is_loading = false
        })
    }
  }
}
</script>
