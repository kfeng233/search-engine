import search
import flask
import requests
import threading
import heapq
import queue


def get_results(url, text, slider):
    response = requests.get(url, params={'q': text, 'w': slider})
    return response.json()

@search.app.route('/', methods=['GET'])
def show_index():
    total_results = []
    lock = threading.Lock()
    text = flask.request.args.get('q', '')
    slider = flask.request.args.get('w', 0.5)

    def worker(url, text, slider):
        with search.app.app_context():
            results = get_results(url, text, slider)
            connection = search.model.get_db()
            for res in results['hits']:
                doc_id = res['docid']
                cur = connection.execute(
                    """SELECT docid, title, summary, url FROM Documents WHERE docid = ?""", (doc_id,)
                )
                docs = cur.fetchall()
                if docs:
                    for doc in docs:
                        doc['score'] = res['score']
                        if doc['summary'] == '':
                            doc['summary'] = 'No summary available'
                    with lock:
                        total_results.append(docs)

    threads = []
    for url in search.app.config['SEARCH_INDEX_SEGMENT_API_URLS']:
        t = threading.Thread(target=worker, args=(url, text, slider,))
        threads.append(t)
        t.start()
    for thread in threads:
        thread.join()
    #flat_documents = [doc for sublist in total_results for doc in sublist]
    merged_documents = heapq.merge(*total_results, key=lambda d: d['score'], reverse=True)
    result_list = list(merged_documents)[:10]
    for i in result_list:
        print(i['score'])
    context = {"documents": result_list, "text": text, "range": slider}
    return flask.render_template("index.html", **context)

if __name__ == '__main__':
    search.app.run(debug=True)