<template>
  <div v-if="is_loading">
    Loading...
  </div>

  <div v-else>
    <h3 class="clearfix">
      <router-link :to="`/text/${text_id}/`" class="btn btn-default pull-right">Back to Text</router-link>
      <span class="text-muted">Text:</span>
      {{sentence.text.title}}
    </h3>

    <h3>
      <span class="text-muted">Sentence:</span> #{{sentence.number}}
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
