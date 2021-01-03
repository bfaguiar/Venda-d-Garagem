import json

from django.http import HttpResponseRedirect
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.shortcuts import render
from SPARQLWrapper import SPARQLWrapper, JSON
from django.template.defaulttags import register
import pprint


def index(request):
    # aqui aparece lista de carros com os detalhes: id (marca,modelo,versão), wheel drive, horse power, aceleração, consumo, cor e preço
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"

    idc = dict()
    name = dict()
    cor = dict()

    query = """
        PREFIX vso: <http://purl.org/vso/ns#>
        PREFIX gr: <http://purl.org/goodrelations/v1#>
        PREFIX uco: <http://purl.org/uco/ns#>
        PREFIX foaf:<http://xmlns.com/foaf/0.1/>
        PREFIX schema: <http://schema.org/>

        SELECT ?idc ?name ?cor ?hp ?comb ?loc ?preco
        WHERE {
            ?vendor ?sell [?car [vso:VIN ?idc]].
            ?vendor ?person [foaf:nick ?name].
            ?vendor ?sell [vso:color ?cor].
            ?vendor ?sell [?car [vso:enginePower ?hp]].
    		?vendor ?sell [?car [vso:fuelType ?comb]].
    		?vendor ?sell [?car [ uco:currentLocation [ schema:addressRegion ?loc ]]].
    		?vendor ?sell [?car [ gr:hasPriceSpecification [ gr:hasCurrencyValue ?preco ]]].
        }
        ORDER BY ASC(?idc)
    """
    try:
        payload_query = {"query": query}
        result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
        result = json.loads(result)
    except ValueError:
        print("erro")
    
    lista = []
    return_template = {}
    for e in result['results']['bindings']:
        lista.append([e['idc']['value'], e['name']['value'], e['cor']['value'], e['hp']['value']+" CV", e['comb']['value'].replace("Gasoline","Gasolina"), e['loc']['value'], e['preco']['value']+"€"])

    pprint.pprint(lista)
    #return_template["caracteristicas"] = lista
    tparams = {
                'lista': lista,
    }

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
    endpoint = "http://localhost:7200"
    repo_name = "cars"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    ids = dict()
    carid_query = """
                PREFIX vso: <http://purl.org/vso/ns#>
                PREFIX schema: <http://schema.org/>
                SELECT ?id
                WHERE {
                    ?car vso:VIN ?id .
                }
                ORDER BY ASC(?id)
            """
    payload_query = {"query": carid_query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        ids[e['id']['value']] = e['id']['value']

    tparams = {
        'id': ids,
    }

    return render(request, 'profile.html', tparams)


def add_announce(request):
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"

    # Sale specs
    color = request.POST.get('color')
    smoke = request.POST.get('smoke')
    pet = request.POST.get('pets')
    own = request.POST.get('owners')
    kms = request.POST.get('km')
    value = request.POST.get('value')
    local = request.POST.get('local')

    # Car
    idc = request.POST.get('id')

    # User
    person_query = """
        PREFIX person: <http://garagemdosusados.com/pessoas/#>
        SELECT ?name
        WHERE {
            ?person foaf:firstName ?name .
        }
    """
    payload_query = {"query": person_query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    name = res['name']['value']

    # Insert all
    insert_query = f"""
        PREFIX vendor:<http://garagemdosusados.com/vendors/#>.
        PREFIX sell:<http://garagemdosusados.com/vendas/#>.
        PREFIX vso:<http://purl.org/vso/ns#>.    
        PREFIX uco:<http://purl.org/uco/ns#>.
        PREFIX gr:<http://purl.org/goodrelations/v1#> .  
        INSERT DATA {{



            #### ??????



        }}
    """

    payload_query = {"update": insert_query}
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name)

    return HttpResponseRedirect('/profile')


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
