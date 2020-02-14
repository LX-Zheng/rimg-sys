new Vue({
  el: '#reptile',
  data: {
    url: '',
    start: '',
    end: '',
    type: ''
  },
  methods: {
    repImg() {
      axios.post('/reptile_img', {
        url: this.url,
        start: this.start,
        end: this.end,
        type:this.type
      }).then((res) => {
        console.log(res)
      }).catch((err) => {
        console.log(err)
      })
    }
  }
})