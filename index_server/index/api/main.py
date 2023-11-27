"""REST API for index server."""
import flask
import index
import re
import math


@index.app.route('/api/v1/', methods=['GET'])
def services():
    """List of services available."""
    context = {
        "hits": "/api/v1/hits/",
        "url": "/api/v1/"
    }

    return flask.jsonify(**context), 200

@index.app.route('/api/v1/hits/')
def hits():
    query = flask.request.args.get("q", default="", type=str)
    weight = flask.request.args.get("w", default=0.5, type=float)
    query = re.sub(r"[^a-zA-Z0-9 ]+", "", query)
    query = str.casefold(query)
    query = query.split()
    query = [word for word in query if word not in index.api.dic['stopwords']]
    terms = {}
    for term in query:
        if term in terms:
            terms[term][0]+=1
        else:
            terms[term] = [1]
    docs = set()
    init = False
    for term in terms:
        if term not in index.api.dic['index']:
            print(term)
            return flask.jsonify(**{"hits":[]}), 200
        elif float(index.api.dic['index'][term][1]) == 0.0:
            del terms[term]
        else:
            rec = index.api.dic['index'][term]
            terms[term].append((float)(rec[1]))
            temp = set()
            for doc in range((len(rec)-2)//3):
                temp.add(rec[2+doc*3])
            if not init:
                docs = temp
                init = True
            else:
                docs = docs.intersection(temp)
    _docs = {}
    docs = list(docs)
    for doc in docs:
        _docs[doc] = {}
        for term in terms:
            rec = index.api.dic['index'][term]
            for i in range((len(rec)-2)//3):
                if rec[2+i*3] == doc:
                    if 'factor' not in _docs[doc]:
                        _docs[doc]['factor'] = (float(rec[4+i*3]))
                    _docs[doc][term] = (float(rec[3+i*3]))
                    break
        
        _docs[doc]['pagerank'] = (float(index.api.dic['pagerank'][doc]))
        
    scores = {}
    for doc in _docs:
        tf_idf = 0.0
        qlenth = 0.0
        for key in terms:
            tf_idf += terms[key][0] * (terms[key][1]**2) * (_docs[doc][key])
            qlenth += (terms[key][0] * terms[key][1])**2
        tf_idf /= (math.sqrt(qlenth*_docs[doc]['factor']))
        score = weight*_docs[doc]['pagerank'] + (1.0-weight)*tf_idf
        scores[doc] = score
    hits = []
    for key, val in sorted(scores.items(), key=lambda x: x[1],reverse=True):
        hits.append({"docid":int(key), "score":val})
    context = {"hits":hits}
    return flask.jsonify(**context), 200