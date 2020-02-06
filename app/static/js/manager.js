new Vue({
    el: '#manager',
    data: {
        search: '',
        tableData: [],
        dialogFormVisible: false,
        form: {
            name: '',
            category: '',
            row: '',
        },
        formLabelWidth: '120px',
        imgSrc: '',                     // 图片的src
        multipleSelection: [],          // 删除多选框的数据
        currentPage: 1,                 // 当前页
        total: 0,                       // 分页数据项
    },
    methods: {
        // edit编辑
        handleEdit(index, row) {
            this.dialogFormVisible = true;
            this.form.name = row.id;
            this.form.category = row.type;
            this.form.row = index;
            this.imgSrc = ".." + this.tableData[index].url.split("..")[1]
        },
        handleDelete(index, row) {
            console.log(index, row);
        },
        // dialog修改事件
        changePost() {
            this.dialogFormVisible = false;
            axios.post('/changeInfo', {
                id: this.form.name,
                type: this.form.category
            }).then((res) => {
                console.log(res);
                if(res.data.success === 0) {
                    this.tableData[this.form.row].type = this.form.category;
                }
            }).catch((err) => {
                console.log(err);
            })
        },
        // 多选框的删除事件
        handleSelectionChange(val) {
            this.multipleSelection = val;
        },
        // 取消多选框
        toggleSelection() {
            this.$refs.multipleTable.clearSelection();
        },
        // 删除多选框
        toggleDelete() {
            let obj = []
            for(let i in this.multipleSelection){
                obj.push({id: this.multipleSelection[i].id})
            }
            axios.post('/toggleDelete',obj)
            .then((res) => {
                if(res.data.success === 0) {
                    for(let i in obj){
                        pos = this.index(obj[i].id)
                        if(pos !== -1){
                            this.tableData.splice(pos,1)
                        }
                    }
                }
            }).catch((err) => {
                console.log(err)
            })
        },
        // 返回数组的下标
        index(val) {
            for(let i in this.tableData){
                if(this.tableData[i].id === val)
                    return i
            }
            return -1;
        },
        // 分页
        handleSizeChange(val) {
            console.log(`每页 ${val} 条`);
        },
        handleCurrentChange(val) {
            console.log(`当前页: ${val}`);
        }
    },
    created: function () {
        axios.post('/getInfo')
        .then((res) => {
            this.tableData = []
            for(let d in res.data){
                this.tableData.push({
                    id: res.data[d].wp_id,
                    type: res.data[d].wp_type,
                    url: res.data[d].wp_url
                })
                this.total++
            }
        }).catch((err) => {
            console.log(err);
        })
    }
})