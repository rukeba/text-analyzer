import Vue from 'vue'
import VueRouter from 'vue-router'
import TextsList from '../views/TextsList.vue'

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
    component: () => import(/* webpackChunkName: "text" */ '../views/TextSentences.vue')
  },
  {
    path: '/text/:text_id/sentence/:sentence_id',
    name: 'Sentence',
    component: () => import(/* webpackChunkName: "sentence" */ '../views/Sentence.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
