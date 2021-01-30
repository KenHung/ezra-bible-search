const PAGE_SIZE = 20;
const MAX_SIZE = 100;
const Ezra = {
    data() {
        return {
            loading: true,
            allResults: [],
            pages: 1
        }
    },
    computed: {
        results() {
            return this.allResults.slice(0, this.pages * PAGE_SIZE);
        },
        noMoreResults() {
            return this.results.length >= MAX_SIZE;
        }
    },
    methods: {
        search(query) {
            const vm = this;
            var xhr = new XMLHttpRequest();
            xhr.onload = function (e) {
                if (xhr.status === 200) {
                    var resp = JSON.parse(xhr.responseText)
                    if (resp.status == 'success') {
                        vm.allResults = resp.data;
                    }
                }
                vm.loading = false;
            };
            xhr.open('GET', '/api?' + query + '&top=' + MAX_SIZE);
            xhr.send();
        },
        highlight(result) {
            verse = result.verse;
            for (const kw in result.kw_scores) {
                verse = verse.replace(new RegExp(kw, 'g'), '<em>' + kw + '</em>');
            }
            return verse;
        }
    }
};
const vm = Vue.createApp(Ezra).mount('#ezra');
