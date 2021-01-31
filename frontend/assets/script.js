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
        wdLink(ref) {
            return 'https://wd.bible/' + wdAbbr[ref.book] + '.' + ref.chap + '.' + ref.vers + '.cunpt';
        },
        verseRef(ref) {
            return bookName[ref.book] + ' ' + ref.chap + ':' + ref.vers;
        },
        highlight(result) {
            text = result.text;
            for (const kw in result.kw_scores) {
                text = text.replace(new RegExp(kw, 'g'), '<em>' + kw + '</em>');
            }
            return text;
        }
    }
};
const vm = Vue.createApp(Ezra).mount('#ezra');

const bookName = {
    'Gen': '創世記',
    'Ex': '出埃及記',
    'Lev': '利未記',
    'Num': '民數記',
    'Deut': '申命記',
    'Josh': '約書亞記',
    'Judg': '士師記',
    'Ruth': '路得記',
    '1 Sam': '撒母耳記上',
    '2 Sam': '撒母耳記下',
    '1 Kin': '列王紀上',
    '2 Kin': '列王紀下',
    '1 Chr': '歷代志上',
    '2 Chr': '歷代志下',
    'Ezra': '以斯拉記',
    'Neh': '尼希米記',
    'Esth': '以斯帖記',
    'Job': '約伯記',
    'Ps': '詩篇',
    'Prov': '箴言',
    'Eccl': '傳道書',
    'Song': '雅歌',
    'Is': '以賽亞書',
    'Jer': '耶利米書',
    'Lam': '耶利米哀歌',
    'Ezek': '以西結書',
    'Dan': '但以理書',
    'Hos': '何西阿書',
    'Joel': '約珥書',
    'Amos': '阿摩司書',
    'Obad': '俄巴底亞書',
    'Jon': '約拿書',
    'Mic': '彌迦書',
    'Nah': '那鴻書',
    'Hab': '哈巴谷書',
    'Zeph': '西番雅書',
    'Hag': '哈該書',
    'Zech': '撒迦利亞書',
    'Mal': '瑪拉基書',
    'Matt': '馬太福音',
    'Mark': '馬可福音',
    'Luke': '路加福音',
    'John': '約翰福音',
    'Acts': '使徒行傳',
    'Rom': '羅馬書',
    '1 Cor': '哥林多前書',
    '2 Cor': '哥林多後書',
    'Gal': '加拉太書',
    'Eph': '以弗所書',
    'Phil': '腓立比書',
    'Col': '歌羅西書',
    '1 Thess': '帖撒羅尼迦前書',
    '2 Thess': '帖撒羅尼迦後書',
    '1 Tim': '提摩太前書',
    '2 Tim': '提摩太後書',
    'Titus': '提多書',
    'Philem': '腓利門書',
    'Heb': '希伯來書',
    'James': '雅各書',
    '1 Pet': '彼得前書',
    '2 Pet': '彼得後書',
    '1 John': '約翰一書',
    '2 John': '約翰二書',
    '3 John': '約翰三書',
    'Jude': '猶大書',
    'Rev': '啟示錄'
};

const wdAbbr = {
    "Gen": "gen",
    "Ex": "exo",
    "Lev": "lev",
    "Num": "num",
    "Deut": "deu",
    "Josh": "jos",
    "Judg": "jdg",
    "Ruth": "rut",
    "1 Sam": "1sa",
    "2 Sam": "2sa",
    "1 Kin": "1ki",
    "2 Kin": "2ki",
    "1 Chr": "1ch",
    "2 Chr": "2ch",
    "Ezra": "ezr",
    "Neh": "neh",
    "Esth": "est",
    "Job": "job",
    "Ps": "psa",
    "Prov": "pro",
    "Eccl": "ecc",
    "Song": "sng",
    "Is": "isa",
    "Jer": "jer",
    "Lam": "lam",
    "Ezek": "ezk",
    "Dan": "dan",
    "Hos": "hos",
    "Joel": "jol",
    "Amos": "amo",
    "Obad": "oba",
    "Jon": "jon",
    "Mic": "mic",
    "Nah": "nam",
    "Hab": "hab",
    "Zeph": "zep",
    "Hag": "hag",
    "Zech": "zec",
    "Mal": "mal",
    "Matt": "mat",
    "Mark": "mrk",
    "Luke": "luk",
    "John": "jhn",
    "Acts": "act",
    "Rom": "rom",
    "1 Cor": "1co",
    "2 Cor": "2co",
    "Gal": "gal",
    "Eph": "eph",
    "Phil": "php",
    "Col": "col",
    "1 Thess": "1th",
    "2 Thess": "2th",
    "1 Tim": "1ti",
    "2 Tim": "2ti",
    "Titus": "tit",
    "Philem": "phm",
    "Heb": "heb",
    "James": "jas",
    "1 Pet": "1pe",
    "2 Pet": "2pe",
    "1 John": "1jn",
    "2 John": "2jn",
    "3 John": "3jn",
    "Jude": "jud",
    "Rev": "rev"
};
