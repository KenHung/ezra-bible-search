const PAGE_SIZE = 10;
const MAX_SIZE = 100;
const Ezra = {
    data() {
        return {
            loading: true,
            keyword: '',
            allResults: [],
            pages: 1,
            searchRanges: {
                'all': '全部',
                'nt': '新約',
                'ot': '舊約',
                'gospels': '四福音',
                'letters': '書信',
                'torah': '摩西五經',
                'history': '歷史書',
                'poetry': '詩歌/智慧書',
                'prophecy': '先知書'
            }
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
            xhr.open('GET', '/api' + query + '&top=' + MAX_SIZE);
            xhr.send();
        },
        wdLink(ref) {
            return 'https://wd.bible/' + wdAbbr[ref.book] + '.' + ref.chap + '.' + ref.vers + '.cunpt';
        },
        verseRef(ref) {
            return bookName[ref.book] + ' ' + ref.chap + ':' + ref.vers;
        },
        highlight(result) {
            text = result.text;
            for (const kw in result.kw_scores) {
                if (result.kw_scores[kw] >= 0.5) {
                    text = text.replace(new RegExp(kw, 'g'), '<em>' + kw + '</em>');
                }
            }
            return text;
        },
        clearSearch() {
            this.keyword = '';
            this.$refs.keyword.focus();
        },
        rangeSelected(range) {
            const found = window.location.search.match(/book=([^&]*)/i);
            const selectedRange = found ? found[1] : 'all';
            return range == selectedRange.toLowerCase();
        },
        searchRangeQuery(range) {
            var baseQuery = window.location.search;
            var bookParam = /book=([^&]*)/;
            if (range === 'all') {
                return baseQuery.replace(/&?book=([^&]*)/, '');
            } else if (baseQuery.search(bookParam) > 0) {
                return baseQuery.replace(bookParam, 'book=' + range);
            }
            else {
                return baseQuery + '&book=' + range;
            }
        }
    }
};
const vm = Vue.createApp(Ezra).mount('#ezra');

const bookName = {
    'gen': '創世記',
    'ex': '出埃及記',
    'lev': '利未記',
    'num': '民數記',
    'deut': '申命記',
    'josh': '約書亞記',
    'judg': '士師記',
    'ruth': '路得記',
    '1sam': '撒母耳記上',
    '2sam': '撒母耳記下',
    '1kin': '列王紀上',
    '2kin': '列王紀下',
    '1chr': '歷代志上',
    '2chr': '歷代志下',
    'ezra': '以斯拉記',
    'neh': '尼希米記',
    'esth': '以斯帖記',
    'job': '約伯記',
    'ps': '詩篇',
    'prov': '箴言',
    'eccl': '傳道書',
    'song': '雅歌',
    'is': '以賽亞書',
    'jer': '耶利米書',
    'lam': '耶利米哀歌',
    'ezek': '以西結書',
    'dan': '但以理書',
    'hos': '何西阿書',
    'joel': '約珥書',
    'amos': '阿摩司書',
    'obad': '俄巴底亞書',
    'jon': '約拿書',
    'mic': '彌迦書',
    'nah': '那鴻書',
    'hab': '哈巴谷書',
    'zeph': '西番雅書',
    'hag': '哈該書',
    'zech': '撒迦利亞書',
    'mal': '瑪拉基書',
    'matt': '馬太福音',
    'mark': '馬可福音',
    'luke': '路加福音',
    'john': '約翰福音',
    'acts': '使徒行傳',
    'rom': '羅馬書',
    '1cor': '哥林多前書',
    '2cor': '哥林多後書',
    'gal': '加拉太書',
    'eph': '以弗所書',
    'phil': '腓立比書',
    'col': '歌羅西書',
    '1thess': '帖撒羅尼迦前書',
    '2thess': '帖撒羅尼迦後書',
    '1tim': '提摩太前書',
    '2tim': '提摩太後書',
    'titus': '提多書',
    'philem': '腓利門書',
    'heb': '希伯來書',
    'james': '雅各書',
    '1pet': '彼得前書',
    '2pet': '彼得後書',
    '1john': '約翰一書',
    '2john': '約翰二書',
    '3john': '約翰三書',
    'jude': '猶大書',
    'rev': '啟示錄'
};

const wdAbbr = {
    "gen": "gen",
    "ex": "exo",
    "lev": "lev",
    "num": "num",
    "deut": "deu",
    "josh": "jos",
    "judg": "jdg",
    "ruth": "rut",
    "1sam": "1sa",
    "2sam": "2sa",
    "1kin": "1ki",
    "2kin": "2ki",
    "1chr": "1ch",
    "2chr": "2ch",
    "ezra": "ezr",
    "neh": "neh",
    "esth": "est",
    "job": "job",
    "ps": "psa",
    "prov": "pro",
    "eccl": "ecc",
    "song": "sng",
    "is": "isa",
    "jer": "jer",
    "lam": "lam",
    "ezek": "ezk",
    "dan": "dan",
    "hos": "hos",
    "joel": "jol",
    "amos": "amo",
    "obad": "oba",
    "jon": "jon",
    "mic": "mic",
    "nah": "nam",
    "hab": "hab",
    "zeph": "zep",
    "hag": "hag",
    "zech": "zec",
    "mal": "mal",
    "matt": "mat",
    "mark": "mrk",
    "luke": "luk",
    "john": "jhn",
    "acts": "act",
    "rom": "rom",
    "1cor": "1co",
    "2cor": "2co",
    "gal": "gal",
    "eph": "eph",
    "phil": "php",
    "col": "col",
    "1thess": "1th",
    "2thess": "2th",
    "1tim": "1ti",
    "2tim": "2ti",
    "titus": "tit",
    "philem": "phm",
    "heb": "heb",
    "james": "jas",
    "1pet": "1pe",
    "2pet": "2pe",
    "1john": "1jn",
    "2john": "2jn",
    "3john": "3jn",
    "jude": "jud",
    "rev": "rev"
};
