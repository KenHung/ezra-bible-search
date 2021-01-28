const Ezra = {
    data() {
        return {
            keyword: "",
            results: []
        }
    },
    methods: {
        search(event) {
            event.preventDefault();
            fetch('/api?q=' + this.keyword)
                .then(resp => resp.json())
                .then(data => this.results = data.data)
        }
    }
}

Vue.createApp(Ezra).mount('#ezra')
