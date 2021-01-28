const Ezra = {
    data() {
        return {
            results: []
        }
    },
    methods: {
        search(e) {
            e.preventDefault();
            searchData = new FormData(document.querySelector('#search-form'))
            searchQuery = new URLSearchParams(searchData)
            fetch('/api?' + searchQuery)
                .then(resp => resp.json())
                .then(data => this.results = data.data)
        }
    }
}

Vue.createApp(Ezra).mount('#ezra')
