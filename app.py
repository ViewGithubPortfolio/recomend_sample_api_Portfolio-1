from flask import Flask,jsonify,request,redirect,url_for,abort
from elasticsearch_model.emodel import QueryBuilder as qb, ElasticSearchDataAccess
from elasticsearch_model.emodel import ElasticConnectionSomthingError,ElasticProcSomthingError
from elasticsearch_model.helper_for_disp import ElasticResultEmptyError,get_elastic_suggest_result

from elasticsearch_model.helper_for_search import gen_random_int_no_dup,get_target_artist_list

from neo4j_model.nmodel import App

import os
import json

app = Flask(__name__)

#########
@app.errorhandler(404)
def error_handler(error):
    return jsonify({ 'id': error.description, 'message': 'resource not fonud', 'result': error.code }), error.code


@app.errorhandler(400)
def error_handler(error):
    return jsonify({ 'id': error.description, 'message': 'id is different', 'result': error.code }), error.code

@app.errorhandler(401)
def error_handler(error):
    return jsonify({ 'id': error.description, 'message': 'id is different', 'result': error.code }), error.code

@app.errorhandler(404)
def error_handler(error):
    return jsonify({ 'id': error.description, 'message': 'id is different', 'result': error.code }), error.code

@app.errorhandler(500)
def error_handler(error):
    return jsonify({ 'id': error.description, 'message': 'id is different', 'result': error.code }), error.code

######
 
@app.route('/hello')
def hello():
    hello = "It is Work"
    return jsonify(hello)

@app.route('/suggest',methods=['get'])
def get_suggest():
    _target_param = request.values.get("suggest", "None")
    if _target_param == None:
        abort(400)
    elif _target_param =="":
        abort(400)
    queryy = qb.suggest_query_dict_none_aggr(_target=_target_param)
    esda=ElasticSearchDataAccess(
        elastic_host=ELASTIC_HOST
    )
    result_proc =None
    try:
        result_proc = esda.search_suggest(queryy)
    except ElasticConnectionSomthingError as ecse:
        abort(500)
    except ElasticProcSomthingError as epse:
        abort(500)

    result_li = None
    try:
        result_li = get_elastic_suggest_result(result_proc)
    except ElasticResultEmptyError as eree:
        abort(500)
    
    res_json_dict = {"result":result_li}
    return jsonify(res_json_dict)

@app.route('/neighborArtists',methods=['get'])
def get_neighbor_artist():
    _get_param = request.values.get("artist_name_trance_remove_kakko", "None")
    if _get_param ==None:
        raise  abort(400)
    
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    
    _nn_neighbor_artist_result =None
    try:

        _nn_neighbor_artist_result = neo4j_app.find_neighbor(_get_param)
    except Exception as e:

        raise abort(500)
    return jsonify({"nn_neighbor_artist_result":_nn_neighbor_artist_result})


@app.route('/main',methods=['get'])
def get_init_disp_artist():
    _init_disp_ids = gen_random_int_no_dup()
    target_atists = get_target_artist_list(_init_disp_ids)
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    _main_disp_result =None
    try:
        _main_disp_result = neo4j_app.get_artist_main_disp(target_atists)
    except Exception as e:
        abort(500)

    res_main_disp = {}
    res_main_disp["result"]=_main_disp_result
    _res_jsonn = jsonify(res_main_disp)
    return _res_jsonn


@app.route('/artistDetail',methods=['get'])
def get_artist_detail_with_releases():
    _get_param = request.values.get("artist_name_trance_remove_kakko", "None")
    if _get_param ==None:
        abort(400)
    
    neo4j_app = App(
        uri=NEO4J_URI,
        user=NEO4J_USER,
        password=NEO4J_PASSWORD
    )
    _artist_detail_result =None
    try:
        
        _artist_detail_result = neo4j_app.get_artist_detail_and_releases(_get_param)
    except Exception as e:
        raise abort(500)
    _res_jsonn = jsonify(_artist_detail_result)
    return _res_jsonn


@app.route('/suggestResult',methods=['get'])
def get_suggestResult():
    _get_param = request.values.get("artist_name_trance_remove_kakko", "None")
    if _get_param is None :
        abort(400)

    return redirect(url_for('get_artist_detail_with_releases', artist_name_trance_remove_kakko=_get_param),code=302)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 3333)))