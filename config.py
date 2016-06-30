XML_EXTENSION = '.xml'

HEADERS = {
    'NAVER' : {
        'cache-control': "no-cache",
        },
    'GITHUB' : {
        'Accept': "application/vnd.github.golden-comet-preview+json",
        'authorization': "token eddd4749028de2cb5617a864c5a65669df29d6be",
        'content-type': "application/json",
        'cache-control': "no-cache",
        'User-Agent': 'postman-test'
        }
}

ENCODING = 'utf-8'
DEBUG = False
XML_OUTPUT = True
TEST = False

GITHUB_URL = "https://oss.navercorp.com/api/v3/repos/maxtortime/open-project-migration-test/import/issues"
