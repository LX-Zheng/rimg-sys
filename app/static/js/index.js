new Vue({
    el: '#index',
    data: {
        activeIndex: '1',
        index: 1,
        fileList: []
    },
    methods: {
        handleSelect(key, keyPath) {
            this.index = key
        },
      }
}) 