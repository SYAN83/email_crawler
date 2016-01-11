import threading
import logging
import random
import time
import url_searcher as us
import temp_fun


logging.basicConfig(level=logging.DEBUG, \
                    format='(%(threadName)-10s) %(message)s',)


class Crawler(threading.Thread):

    def __init__(self, target, name=None, args=(), kwargs={}):
        threading.Thread.__init__(self, target=target, name=name, \
                                  args=args, kwargs=kwargs)

    def run(self):
        # logging.debug('running with %s', self.getName())
        time.sleep(random.random())
        super(Crawler, self).run()
        # logging.debug('Exiting %s', self.getName())


if __name__ == '__main__':


    univ_list = ["http://www.eng.auburn.edu/"]
    dept_list = ["computer science"]
    # for univ in univ_list:
    #     for dept in dept_list:
    #         query = univ + dept, [univ + dept] * 4
    #         w = Crawler(target=temp_fun.crawl, name=query[0], args=('temp', query[1]))
    #         w.start()
    for job in us.dept_url_search(univ_list, dept_list, lucky=False, pause=10):
        w = Crawler(target=temp_fun.crawl, name=job[0], \
                    args=(job[1], job[0]), \
                    kwargs={"limit": 50})
        w.start()
