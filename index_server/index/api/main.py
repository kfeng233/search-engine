"""REST API for index server."""
import re
import math
import flask
import index

@index.app.route('/api/v1/', methods=['GET'])
def services():
    """List of services available."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }

    return flask.jsonify(**context), 200


def get_term(query):
    """Get item."""
    terms = {}
    for term in query:
        if term in terms:
            terms[term][0] += 1
        else:
            terms[term] = [1]
    return terms


def get_docs(docs, terms):
    """Get docs."""
    _docs = {}
    docs = list(docs)
    for doc in docs:
        _docs[doc] = {}
        for term in terms:
            for i in range((len(index.api.dic['index'][term])-2)//3):
                if index.api.dic['index'][term][2+i*3] == doc:
                    if 'factor' not in _docs[doc]:
                        _docs[doc]['factor'] = float(
                            index.api.dic['index'][term][4+i*3]
                        )
                    _docs[doc][term] = float(
                        index.api.dic['index'][term][3+i*3]
                    )
                    break

        _docs[doc]['pagerank'] = float(index.api.dic['pagerank'][doc])
    return _docs


def helper(_docs, terms, weight):
    """Help me."""
    scores = {}
    for doc in _docs:
        tf_idf = 0.0
        qlenth = 0.0
        for key in terms:
            tf_idf += terms[key][0] * (terms[key][1]**2) * (_docs[doc][key])
            qlenth += (terms[key][0] * terms[key][1])**2
        tf_idf /= (math.sqrt(qlenth*_docs[doc]['factor']))
        scores[doc] = weight*_docs[doc]['pagerank'] + (1.0-weight)*tf_idf
    return scores


@index.app.route('/api/v1/hits/')
def hits():
    """Hits."""
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = str.casefold(query)
    query = query.split()
    query = [word for word in query if word not in index.api.dic['stopwords']]
    terms = get_term(query)
    docs = set()
    init = False
    for term, _ in terms.items():
        if term not in index.api.dic['index']:
            return flask.jsonify(**{"hits": []}), 200
        if float(index.api.dic['index'][term][1]) == 0.0:
            del terms[term]
        else:
            terms[term].append((float)(index.api.dic['index'][term][1]))
            temp = set()
            for doc in range((len(index.api.dic['index'][term])-2)//3):
                temp.add(index.api.dic['index'][term][2+doc*3])
            if not init:
                docs = temp
                init = True
            else:
                docs = docs.intersection(temp)
    _docs = get_docs(docs, terms)

    scores = helper(_docs, terms, weight)
    context = []
    for key, val in sorted(scores.items(), key=lambda x: x[1], reverse=True):
        context.append({"docid": int(key), "score": val})
    context = {"hits": context}
    return flask.jsonify(**context), 200
