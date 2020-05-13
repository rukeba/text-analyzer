export const ApiErrorsHandlerMixin = {
  methods: {
    apiErrorHandler (title) {
      return err => {
        title = title || 'Api request'
        const message = `Error occurred during ${title}: ${err.message}`
        console.error(message)
        console.error(err)
        alert(message)
      }
    }
  }
}
