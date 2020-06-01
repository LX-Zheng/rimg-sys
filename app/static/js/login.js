new Vue({
    el: '#login',
    data: {
        account: '',
        password: '',
    },
    methods: {
        login() {
            axios.get('/alogin', {
                params: {
                    account: this.account,
                    password: this.password
                }
            }).then((res) => {
                if(res.data.status === 1)
                    window.location.href = "index"
                else
                    alert("失败")
            }).catch((err) => {
                console.log(err);
            })
        }
    }
})