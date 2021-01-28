from elasticsearch import Elasticsearch
from ttpeople.settings import ES_HOST, ES_PORT, ES_PASSWD

__all__ = ['Es', 'singleton']


def singleton(cls):
    instances = {}

    def wrapper(*args, **kwargs):
        if cls not in instances:
            instances[cls] = cls(*args, **kwargs)
        return instances[cls]

    return wrapper


class Es:
    def __init__(self, index_name="tt_people", doc_type="_doc"):
        self.con = get_con()
        self.index_name = index_name
        self.doc_type = doc_type

    def save(self, body):
        self.con.index(index=self.index_name, doc_type=self.doc_type, body=body)

    def delete_idx(self):
        self.con.indices.delete(index=self.index_name, ignore=[400, 404])

    def delete_by_query(self, body):
        self.con.delete_by_query(index=self.index_name, doc_type=self.doc_type, body=body)


@singleton
def get_con():
    if ES_PASSWD:
        hosts = f'http://elastic:{ES_PASSWD}@{ES_HOST}:{ES_PORT}/'
        con = Elasticsearch(hosts=hosts)
    else:
        con = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT}])
    return con


if __name__ == '__main__':
    es = Es()
    query = {
        "query": {
            "bool": {
                "must": [
                    {
                        "term": {
                            "source.keyword": "rand"
                        }
                    }
                ],
            }
        }
    }
    es.delete_by_query(query)
