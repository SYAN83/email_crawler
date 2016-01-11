from googlesearch import GoogleSearch
from requests.exceptions import ProxyError
import time

# documentation url: https://pypi.python.org/pypi/googlesearch/0.7.0
# github link: https://github.com/frrmack/googlesearch


def url_search(query, lucky=True):
    gs = GoogleSearch(query)
    try:
        return [gs.top_url()] if lucky else gs.top_urls()
    except ProxyError:
        raise ValueError


def dept_url_search(univs, depts, *args, **kwargs):

    if 'lucky' in kwargs:
        lucky = kwargs['lucky']
    else:
        lucky = True
    if 'pause' in kwargs:
        pause = kwargs['pause']
    else:
        pause = 60
    for univ in univs:
        for dept in depts:
            query = " ".join([univ, dept] + list(args))
            log_w = open('query.log', 'a')
            log_r = open('query.log', 'r')

            if query in map(lambda x: x.strip(), log_r.readlines()):
                log_r.close()
                log_w.close()
                continue
            try:
                yield query, url_search(query, lucky=lucky)
                log_w.write(query + '\n')
                log_w.close()
                log_r.close()
            except ValueError:
                pass
            time.sleep(pause)


if __name__ == "__main__":
    univ_list = ["CMU", "Duke"]
    dept_list = ["computer science", "computer engineering"]
    for url in dept_url_search(univ_list, dept_list, lucky=True, pause=2):
        print url
