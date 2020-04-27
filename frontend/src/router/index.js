import Vue from 'vue'
import VueRouter from 'vue-router'
import TextsList from '@/views/TextsList.vue'
import TextSentences from '@/views/TextSentences'
import Sentence from '@/views/Sentence'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'TextsList',
    component: TextsList
  },
  {
    path: '/text/:text_id',
    name: 'TextSentences',
    component: TextSentences
  },
  {
    path: '/text/:text_id/sentence/:sentence_id',
    name: 'Sentence',
    component: Sentence
  }
]

const router = new VueRouter({
  routes
})

export default router
