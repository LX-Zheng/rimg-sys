new Vue({
    el: '#register',
    data: {
        name: '',
        account: '',
        password: ''
    },
    methods: {
        register() {
            axios.get('/userReg', {
                params: {
                    name: this.name,
                    account: this.account,
                    password: this.password
                }
            }).then((res) => {
                console.log(res);
            }).catch((err) => {
                console.log(err);
            })
        }
    }
})