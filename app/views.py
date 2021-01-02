import json
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.shortcuts import render
from rdflib import Graph
from SPARQLWrapper import SPARQLWrapper, JSON, N3
from pprint import pprint
from django.template.defaulttags import register


def index(request):
    # aqui aparece lista de carros com os detalhes: id (marca,modelo,versão), wheel drive, horse power, aceleração, consumo, cor e preço

    id = dict()
    cor = dict()
    hp = dict()
    consumo = dict()
    loc = dict()
    preco = dict()
    endpoint = "http://localhost:7200"
    repo_name = "cars"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    query = """
                PREFIX vso: <http://purl.org/vso/ns#>
                PREFIX gr: <http://purl.org/goodrelations/v1#>
                PREFIX uco: <http://purl.org/uco/ns#>
                PREFIX schema: <http://schema.org/>

                SELECT ?id ?cor ?hp ?consumo ?preco ?loc
                WHERE {
                    ?car vso:VIN ?id .
                    ?car vso:color ?cor .
                    ?car vso:enginePower ?hp .
                    ?car vso:fuelType ?consumo .
                    ?car uco:currentLocation [ schema:addressRegion ?loc ] .
                    ?car gr:hasPriceSpecification [ gr:hasCurrencyValue ?preco ] .
                }
                ORDER BY ASC(?id)
            """
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        id[e['id']['value']] = e['id']['value']
        cor[e['cor']['value']] = e['cor']['value'].replace("@pt", "")
        hp[e['hp']['value']] = e['hp']['value'].replace("^^xsd:integer", "") + " CV"
        consumo[e['consumo']['value']] = e['consumo']['value'].replace("@en", "").replace("Gasoline", "Gasolina")
        loc[e['loc']['value']] = e['loc']['value'].replace("@pt", "")
        preco[e['preco']['value']] = e['preco']['value'].replace("xsd:float", "") + "€"

    tparams = {
        'id': id,
        'cor': cor,
        'hp': hp,
        'consumo': consumo,
        'loc': loc,
        'preco': preco
    }
    print(tparams)
    return render(request, 'index.html', tparams)


def login(request):
    # username id = "user"
    # password id = "pass"
    # login id = "login"
    return render(request, 'login.html')


def loginreq(request):
    # Este é só para redireccionar para a página do login caso não tenha login feito
    return render(request, 'loginreq.html')


def signup(request):
    # username id = "user"
    # email id = "email"
    # password id = "pass"
    # register id = "register"
    return render(request, 'signup.html')


def motos(request):
    # Não sei se querem por motos também
    return render(request, 'motos.html')


def profile(request):
    # Aqui aparece nome, email e anúncios feitos pelo próprio

    # ADICIONAR ANUNCIO DE CARRO
    # id do carro id = "id"
    # cor do carro id = "color"
    # preço do carro id = "price"
    # adicionar anuncio id = "announce"
    return render(request, 'profile.html')


def friends(request):
    # Aqui aparece nome, email e anúncios feitos por cada amigo

    # ADICIONAR AMIGO
    # nome do amigo id = "name"
    # email do amigo id = "email"
    # adicionar amigo id = "add"
    # Se não existir dizer que não existe
    return render(request, 'friends.html')


def about(request):
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    # brand = request.GET['brand']
    brand = 'BMW'
    sparql.setQuery(f'''
        SELECT ?name ?abst ?city ?num ?own ?prod
        WHERE {{ dbr:{brand} rdfs:label ?name.
                 dbr:{brand} dbo:abstract ?abst.
                 dbr:{brand} dbo:locationCity ?city.
                 dbr:{brand} dbo:numberOfEmployees ?num.
                 dbr:{brand} dbo:owner ?own.
                 dbr:{brand} dbo:production ?prod.
            FILTER (lang(?abst) = 'pt')
        }}
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()

    result = qres['results']['bindings'][0]
    name, abst, num, own, prod, city = result['name']['value'], result['abst']['value'], result['num']['value'], \
                                       result['own']['value'], result['prod']['value'], result['city']['value']

    own = own.replace('_', ' ').split('/')[-1]
    city = city.replace('_', ' ').split('/')[-1]

    tparams = {
        "name": name,
        "abstract": abst,
        "city": city,
        "employees": num,
        "owner": own,
        "prod": prod,

    }

    return render(request, 'about.html', tparams)


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)