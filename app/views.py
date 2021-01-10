import json

from django.http import HttpResponseRedirect
from s4api.graphdb_api import GraphDBApi
from s4api.swagger import ApiClient
from django.shortcuts import redirect, render
from SPARQLWrapper import SPARQLWrapper, JSON
from django.template.defaulttags import register
from django.http.request import HttpRequest
from random import randint
import random

user = None


def getUser():
    global user
    return user
 

def postUser(usr):
    global user
    user = usr 
 

def index(request):
    if user == None:
        return redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)  
    repo_name = "cars"
  
    query = """
        PREFIX vso: <http://purl.org/vso/ns#>
        PREFIX gr: <http://purl.org/goodrelations/v1#>
        PREFIX uco: <http://purl.org/uco/ns#>
        PREFIX foaf:<http://xmlns.com/foaf/0.1/>
        PREFIX schema: <http://schema.org/>

        SELECT ?idc ?name ?cor ?prev ?pets ?smoke ?val ?loc ?ft ?offer
        WHERE { 
            ?vendor foaf:nick ?person .
    		?person foaf:nick ?name .
    		?vendor gr:offers ?offer .
    		?offer gr:includes ?car .
    		?offer vso:color ?cor .
    		?offer vso:previousOwners ?prev .  
    		?offer uco:pets ?pets .
    		?offer uco:smoking ?smoke .
    		?offer uco:currentLocation [schema:addressRegion ?loc] .
    		?offer gr:hasPriceSpecification [gr:hasCurrencyValue ?val] .
    		?car vso:fuelType ?ft .
    		?car vso:VIN ?idc . 
        } 
    """   

    try:
        payload_query = {"query": query}
        result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
        result = json.loads(result) 
    except ValueError:
        print("error")

    lista = []

    for e in result['results']['bindings']:
        lista.append([e['idc']['value'].split(" ", 2)[1],
                      e['idc']['value'].split(" ", 2)[2],
                      e['cor']['value'],
                      e['ft']['value'].replace("Gasoline", "Gasolina").replace("E85", "Diesel"),
                      e['pets']['value'].replace("Yes", "Sim").replace("No", "Não"),
                      e['smoke']['value'].replace("Yes", "Sim").replace("No", "Não"),
                      e['prev']['value'],
                      e['loc']['value'],
                      e['name']['value'].capitalize(),
                      e['val']['value'] + '€',
                      e['idc']['value'], 
                      e['offer']['value'].replace("http://garagemdosusados.com/vendas/#", "")])     
    
    for l in lista:
        ask_query = ''' PREFIX sell: <http://garagemdosusados.com/vendas/#>
                    PREFIX person: <http://garagemdosusados.com/pessoas/#>
                            ASK
                            WHERE {{
                                person:{} person:wishlist sell:{}
                            }}'''.format( getUser(), l[11] )     
        payload_query = {"query": ask_query} 
        
        result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
        result = json.loads(result)    
        print(result)
        if (result['boolean']):  
            l.append( True ) 
        else: 
            l.append(False)   
        
        #print(lista)

    tparams = {  
        'lista': lista, 
    }

    return render(request, 'index.html', tparams)

def fav(request): 
    #//print("OLA")
    if user == None:
        return redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"
    query = '''   prefix foaf: <http://xmlns.com/foaf/0.1/>
                  prefix person: <http://garagemdosusados.com/pessoas/#>
                  prefix sell: <http://garagemdosusados.com/vendas/#>
                  insert {{
                      ?s person:wishlist sell:{}
                  }} where {{
                      ?s foaf:nick "{}"
                  }}
    '''.format(request.GET['idc'] , getUser()) 
    payload_query = {"update": query}  
    result = acessor.sparql_update(body=payload_query, repo_name=repo_name)
   # print(request.GET['idc'])
    #print("OLA")
    print(result) 
    if request.GET['source'] == "index":
        return redirect('/')
    return redirect('profile')   

def rev(request): 

    if user == None:
        return redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"
    query = '''   prefix foaf: <http://xmlns.com/foaf/0.1/>
                  prefix person: <http://garagemdosusados.com/pessoas/#>
                  prefix sell: <http://garagemdosusados.com/vendas/#> 
                  delete {{
                      ?s person:wishlist sell:{}
                  }} where {{
                      ?s foaf:nick "{}"
                  }}  
    '''.format(request.GET['idc'], getUser())  
    payload_query = {"update": query} 
    result = acessor.sparql_update(body=payload_query, repo_name=repo_name)
    print(result)  
    if request.GET['source'] == "index":
        return redirect('/')  
    if request.GET['source'] == "wishlist":
        return redirect('wishlist')
    return redirect('profile')    
      
def model(request):
    if user == None:
        return redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars" 

    query = '''  
            PREFIX car: <http://garagemdosusados.com/carros/#>
            PREFIX vso: <http://purl.org/vso/ns#>
            PREFIX gr: <http://purl.org/goodrelations/v1#>
            SELECT ?marca ?modelo ?data ?hei ?len ?wi ?dw ?gear ?hp ?trans ?fuel ?vel ?ace ?vin
            WHERE {{
                ?car vso:VIN "{}".
                ?car gr:hasManufacturer ?marca.
                ?car gr:hasMakeAndModel ?modelo.
                ?car vso:modelDate ?data.
                ?car vso:height ?hei.
                ?car vso:length ?len.
                ?car vso:width ?wi.
                ?car vso:DriveWheelConfiguration ?dw.
                ?car vso:gearsTotal ?gear.
                ?car vso:enginePower ?hp.
                ?car vso:TransmissionTypeValue ?trans.
                ?car vso:fuelType ?fuel.
                ?car vso:speed ?vel.
                ?car vso:accelaration ?ace.
                ?car vso:VIN ?vin.
            }}  
        '''.format(request.GET["entity"])

    try: 
        payload_query = {"query": query}
        result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
        result = json.loads(result)
    except ValueError:
        print("error")

    lista = []

    for e in result['results']['bindings']:
        lista.append([e['marca']['value'].split("/")[-1],
                      e['modelo']['value'].split("_")[1],
                      e['data']['value'],
                      e['hei']['value']+"cm",
                      e['len']['value']+"cm",
                      e['wi']['value']+"cm",
                      e['dw']['value'].replace("Rear-wheel drive", "Traseira").replace("Front-wheel drive", "Dianteira").replace("All-wheel drive", "4x4").replace("Four-wheel drive", "4WD"),
                      e['gear']['value'],
                      e['hp']['value']+"cv",
                      e['trans']['value'].replace("Automatic transmission", "Automática").replace("Manual transmission","Manual"),
                      e['fuel']['value'].replace("E85", "Diesel"),
                      e['vel']['value']+"km/h",
                      e['ace']['value']+"s",
                      e['vin']['value']])

    tparams = {
        'lista': lista[0], 
    }
    return render(request, 'model.html', tparams)


def login(request):
    assert isinstance(request, HttpRequest)
    if 'user' in request.POST and request.POST['user'] != '':
            endpoint = "http://localhost:7200"
            client = ApiClient(endpoint=endpoint)
            acessor = GraphDBApi(client)
            repo_name = "cars" 
            query = ''' PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                        ASK
                        WHERE {{
                            ?name foaf:nick "{}" .
                            ?name foaf:nick ?nick .
                        }}'''.format(request.POST['user'])  
            try: 
                payload_query = {"query": query} 
                result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
                result = json.loads(result) 
                if (result['boolean']):
                    postUser(request.POST['user'])
                    return redirect('index')
                else:
                    return render(request, 'login.html', {'bool': False})
            except ValueError:
                print("error")
    return render(request, 'login.html', {'bool': True})


def signup(request): 
    assert isinstance(request, HttpRequest) 
    if ('user' in request.POST and request.POST['user'] != '') \
        and ('firstName' in request.POST and request.POST['firstName'] != '') \
            and ('email' in request.POST and request.POST['email'] != '') \
                and ('idade' in request.POST and request.POST['idade'] != ''): 
        endpoint = "http://localhost:7200"
        client = ApiClient(endpoint=endpoint)
        acessor = GraphDBApi(client)
        repo_name = "cars" 
        query = ''' PREFIX foaf: <http://xmlns.com/foaf/0.1/>
                    ASK
                    WHERE {{
                        ?name foaf:nick "{}" .
                        ?name foaf:nick ?nick . 
                    }}'''.format(request.POST['user'])   
        try: 
            payload_query = {"query": query} 
            result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
            result = json.loads(result)   
            if result['boolean']:
                return render(request, 'signup.html', {'bool1': False, 'bool2': True})
        except ValueError:
            print("error") 

        query2 = '''PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX person: <http://garagemdosusados.com/pessoas/#>
        INSERT DATA {{
            person:{} a foaf:Person;
            foaf:firstName "{}"@pt;
            foaf:nick "{}"^^xsd:string;
            foaf:mbox "{}"^^xsd:string;
            foaf:age "{}"^^xsd:integer . 
            }}'''.format(request.POST['user'], request.POST['firstName'], request.POST['user'], request.POST['email'], request.POST['idade'])
        try:
            payload_query2 = {"update": query2} 
            acessor.sparql_update(body=payload_query2, repo_name=repo_name)
            postUser(request.POST['user'])   
            return redirect(index)
        except ValueError:
            print("error")  
    else:
        return render(request, 'signup.html', {'bool1': True, 'bool2': False})
    return render(request, 'signup.html', {'bool1': True, 'bool2': True})


def profile(request):
    if user == None:
        return redirect('login')
    if request.GET.get("exit_BTN"):
        print("EXIT_BTN")
        postUser(None)
        return redirect("login") 
    endpoint = "http://localhost:7200"
    repo_name = "cars"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)

    query = ''' PREFIX foaf:<http://xmlns.com/foaf/0.1/>
                PREFIX person: <http://garamgemdosusados.com/pessoas/#>
                PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
                SELECT ?name ?first_name ?nick ?email
                WHERE 
                {{
                    ?name foaf:nick "{}" .
                    ?name foaf:firstName ?first_name . 
                    ?name foaf:nick ?nick .
                    ?name foaf:mbox ?email . 
                    }}'''.format(getUser())
    payload_query = {"query": query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)
    name_nick = res['results']['bindings'][0]['nick']['value']
    name_first = res['results']['bindings'][0]['first_name']['value']
    email = res['results']['bindings'][0]['email']['value']
     
    ids = dict()
    query = """
                PREFIX vso: <http://purl.org/vso/ns#>  
                PREFIX schema: <http://schema.org/> 
                SELECT ?id
                WHERE {
                    ?car vso:VIN ?id .
                } 
                ORDER BY ASC(?id)
            """
    payload_query = {"query": query} 
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)

    for e in res['results']['bindings']:
        ids[e['id']['value']] = e['id']['value']
    
    query = ''' PREFIX vso: <http://purl.org/vso/ns#>
        PREFIX gr: <http://purl.org/goodrelations/v1#>
        PREFIX uco: <http://purl.org/uco/ns#>
        PREFIX foaf:<http://xmlns.com/foaf/0.1/>
        PREFIX schema: <http://schema.org/>
        PREFIX person: <http://garagemdosusados.com/pessoas/#>

        SELECT ?idc ?name ?cor ?prevOwners ?pets ?smoke ?val ?looc ?fuelType ?mileage ?offer
        WHERE {{ 
            ?vendor foaf:nick person:{} .
    		?vendor gr:offers ?offer .
    		?offer gr:includes ?car .
    		?offer vso:color ?cor .
    		?offer vso:previousOwners ?prevOwners .  
    		?offer uco:pets ?pets .
    		?offer uco:smoking ?smoke .
    		?offer uco:currentLocation [schema:addressRegion ?looc] .
    		?offer gr:hasPriceSpecification [gr:hasCurrencyValue ?val] .
    		?offer uco:mileageEnd ?mileage .
    		?car vso:fuelType ?fuelType .
    		?car vso:VIN ?idc .  
        }}    
        '''.format(getUser())  

    payload_query = {"query" : query }
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)['results']['bindings']
    
    anuncios = [] 
    for anuncio in res:
        idc_format = anuncio['offer']['value'].replace("http://garagemdosusados.com/vendas/#", "") 
        #//print("idc_format")   
        anuncios.append([anuncio['pets']['value'], anuncio['val']['value'], anuncio['looc']['value'], anuncio['prevOwners']['value'], anuncio['fuelType']['value'], anuncio['cor']['value'], anuncio['smoke']['value'], anuncio['idc']['value'], anuncio['mileage']['value'], idc_format]) 
 
    tparams = {
        'id': ids, 
        'name_first': name_first, 
        'name_nick' : name_nick,
        'email' : email, 
        'anuncios' : anuncios  
    }      

    return render(request, 'profile.html', tparams)


def add_announce(request):
    if user == None:
        return redirect('login') 
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client) 
    repo_name = "cars"

    # Sale specs
    color = request.GET['color'] 
    smoke = "No" 
    pets = "No" 
    if 'smoke' in request.GET:
        smoke = "Yes" 
    if 'pets' in request.GET:
        pets = "Yes" 
    own = request.GET['owners']
    kms = request.GET['km']
    value = request.GET['value']
    local = request.GET['locale']
 
    # Car
    idc = request.GET['id'].replace(" ", "_").replace("+", "Plus").replace("!", "ExclamationPoint").replace("/", "").replace('"', '').replace("''", "").replace("-", "_").replace(".", "_")
    break_Loop = None
    vendor_idc = None
    while break_Loop == None: 
        vendor_idc = idc + str(random.randint(123, 123123123123))
        ask_query = ''' PREFIX sell: <http://garagemdosusados.com/vendas/#>
                    PREFIX gr: <http://purl.org/goodrelations/v1#>
                            ASK
                            WHERE {{ 
                                sell:{} a gr:Offering 
                            }}'''.format(vendor_idc)  
        payload_query = {"query": ask_query} 
        result = acessor.sparql_select(body=payload_query, repo_name=repo_name)
        result = json.loads(result)  
        #//print(vendor_idc) 
        if ( not result['boolean']):
            break_Loop = vendor_idc   
    
    # Insert all
    insert_query = '''PREFIX vendor: <http://garagemdosusados.com/vendors/#>
        PREFIX sell: <http://garagemdosusados.com/vendas/#>
        PREFIX vso:<http://purl.org/vso/ns#>    
        PREFIX uco:<http://purl.org/uco/ns#>
        PREFIX gr:<http://purl.org/goodrelations/v1#>
        PREFIX foaf: <http://xmlns.com/foaf/0.1/>
        PREFIX schema: <http://schema.org/>
        PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix person:  <http://garagemdosusados.com/pessoas/#>
        prefix car:     <http://garagemdosusados.com/carros/#>  
        INSERT DATA {{  
            vendor:{} a gr:Reseller;
                      foaf:nick person:{};
                      gr:offers sell:{} .
            
            sell:{} a gr:Offering; 
            gr:includes car:{};
            gr:hasBunsinessFucntion gr:Sell;
            gr:hasPriceSpecification [ a gr:UnitPriceSpecification ; 
                                       gr:hasCurrency "EUR"^^xsd:string; 
                                       gr:hasCurrencyValue "{}"^^xsd:float ] ; 
            vso:color "{}"@pt ; 
            vso:previousOwners "{}"^^xsd:integer ;  
            uco:pets "{}"@en; 
            uco:smoking "{}"@en; 
            uco:currentLocation [ a schema:PostalAddress;
                                  schema:addressCountry "PT"@pt; 
                                  schema:addressRegion "{}"@pt ];  
            uco:mileageEnd "{}"^^xsd:integer .    
        }}'''.format(getUser(), getUser(), vendor_idc, vendor_idc, idc, value, color, own, pets, smoke, local, kms);  

    payload_query = {"update": insert_query} 
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name) 
    #//print(res)
    return HttpResponseRedirect('/profile')   

def remove_announcement(request):
    if getUser() == None:
        redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"
 
    query = '''
               prefix foaf: <http//xmlns.com/foaf/0.1/>
               delete {{
                    ?s gr:offers {} .              
                   }} where {{
                       vendor:{} ?o ?p .
                   }}'''.format(request.GET['idc'], getUser())  
    payload_query = {"update": query}
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name)
    
    query = '''     
        prefix sell: <http://garagemdosusados.com/vendas/#>   
        delete {{
            sell:{} ?o ?p.
        }}  where {{ 
            sell:{} ?o ?p .
    }}'''.format( request.GET['idc'], request.GET['idc'])  
    payload_query = {"update": query} 
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name) 
    
    #//print("ola {}".format(request.GET['idc']))
    return HttpResponseRedirect('/profile')  
   
def deleteAccount(request):
    if getUser() == None: 
        redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"

    query = ''' prefix foaf: <http://xmlns.com/foaf/0.1/>
                select ?nick ?mbox ?age ?firstName
                    where {{
                        ?person foaf:nick '{}' .
                        ?person foaf:nick ?nick .
                        ?person foaf:mbox ?mbox .
                        ?person foaf:firstName ?firstName .
                        ?person foaf:age ?age .
                        }}'''.format(getUser()) 

    payload_query = {"query": query} 
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name) 
    res = json.loads(res)
    nick = res['results']['bindings'][0]['nick']['value']
    mbox = res['results']['bindings'][0]['mbox']['value']
    age = res['results']['bindings'][0]['age']['value']
    firstName = res['results']['bindings'][0]['age']['value']

    query = '''prefix person: <http://garagemdosusados.com/pessoas/#>
               delete  {{
                   person:{} ?o ?p .
                    }} where {{
                        person:{} ?o ?p .
                            }}'''.format(nick,   nick)
    payload_query = {"update": query}
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name)

    query = ''' PREFIX vso: <http://purl.org/vso/ns#>
        PREFIX gr: <http://purl.org/goodrelations/v1#>
        PREFIX uco: <http://purl.org/uco/ns#>
        PREFIX foaf:<http://xmlns.com/foaf/0.1/>
        PREFIX schema: <http://schema.org/>
        PREFIX person: <http://garagemdosusados.com/pessoas/#>

        SELECT ?offer
        WHERE {{   
            ?vendor foaf:nick person:{} .
    		?vendor gr:offers ?offer .
    		?offer gr:includes ?car .
    		?car vso:VIN ?idc .
        }}  
        '''.format(getUser())

    idcs = [] 
    payload_query = {"query" : query }
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    res = json.loads(res)['results']['bindings']
    for idc in res: 
        idcs.append(idc['offer']['value'].replace("http://garagemdosusados.com/vendas/#", ""))

    query = ''' 
               prefix foaf: <http//xmlns.com/foaf/0.1/>
               delete {{
                    vendor:{} ?o ?p .              
                   }} where {{
                       vendor:{} ?o ?p .
                   }}'''.format(getUser(), getUser())
    payload_query = {"update": query}
    res = acessor.sparql_update(body=payload_query, repo_name=repo_name) 
    
    for n in idcs:
        query = '''     
            prefix sell: <http://garagemdosusados.com/vendas/#>
            delete {{
                sell:{} ?o ?p.
            }}  where {{
                sell:{} ?o ?p .
        }}'''.format( n, n) 
        payload_query = {"update": query}
        res = acessor.sparql_update(body=payload_query, repo_name=repo_name)

    postUser(None);
    return HttpResponseRedirect('/login')   


def wishlist(request):
    if user == None:
        return redirect('login')
    endpoint = "http://localhost:7200"
    client = ApiClient(endpoint=endpoint)
    acessor = GraphDBApi(client)
    repo_name = "cars"
    query = ''' prefix foaf: <http://xmlns.com/foaf/0.1/>
                prefix person: <http://garagemdosusados.com/pessoas/#>
                PREFIX gr: <http://purl.org/goodrelations/v1#>
                PREFIX sell: <http://garagemdosusados.com/vendas/#>
                PREFIX car: <http://garagemdosusados.com/carros/#>
                PREFIX vso: <http://purl.org/vso/ns#>
                PREFIX uco: <http://purl.org/uco/ns#>
                PREFIX schema: <http://schema.org/>
                select ?id ?name ?color ?pets ?smoke ?loc ?val ?fuelType ?prev ?wishes
                where {{
                    ?nck foaf:nick "{}" .
    				?nck person:wishlist ?wishes .
    				?vendor gr:offers ?wishes .
    				?vendor foaf:nick ?nick . 
    				?nick foaf:nick ?name .
    				?wishes gr:includes ?car .
    				?wishes vso:color ?color .
    				?wishes uco:pets ?pets .
    				?wishes uco:smoking ?smoke .
    				?wishes vso:previousOwners ?prev .
    				?wishes uco:currentLocation [schema:addressRegion ?loc] .
   					?wishes gr:hasPriceSpecification [gr:hasCurrencyValue ?val] .
    				?car vso:fuelType ?fuelType .
    				?car vso:VIN ?id .
                    }}'''.format(getUser()) 
    payload_query = {"query" : query}
    res = acessor.sparql_select(body=payload_query, repo_name=repo_name)
    print(res) 
    res = json.loads(res)
    
    lista = []
    for e in res['results']['bindings']:
        lista.append([e['id']['value'].split(" ", 2)[1],
                      e['id']['value'].split(" ", 2)[2],
                      e['color']['value'],
                      e['fuelType']['value'].replace("Gasoline", "Gasolina").replace("E85", "Diesel"),
                      e['pets']['value'].replace("Yes", "Sim").replace("No", "Não"),
                      e['smoke']['value'].replace("Yes", "Sim").replace("No", "Não"),
                      e['prev']['value'],
                      e['loc']['value'],
                      e['name']['value'].capitalize(),
                      e['val']['value'] + '€',
                      e['id']['value'], 
                      e['wishes']['value'].replace("http://garagemdosusados.com/vendas/#", "")])     
    print(lista)
    tparams = {
        'lista': lista,
    }  
    return render(request, 'wishlist.html', tparams)      
  

def about(request):
    if user == None:
        return redirect('login')
    sparql = SPARQLWrapper('https://dbpedia.org/sparql')
    brand = request.GET["entity"] 
    sparql.setQuery(f'''
            SELECT ?name ?abst ?city ?own ?num ?prod ?slo
            WHERE {{ dbr:{brand} rdfs:label ?name.
                    OPTIONAL{{ dbr:{brand} dbo:abstract ?abst.
                        FILTER (lang(?abst) = 'pt') .}}
                    OPTIONAL{{ dbr:{brand} dbo:locationCity ?city.}}
                    OPTIONAL{{ dbr:{brand} dbo:owner ?own. }}
                    OPTIONAL{{ dbr:{brand} dbo:numberOfEmployees ?num. }}
                    OPTIONAL{{ dbr:{brand} dbo:production ?prod. }}
                    OPTIONAL{{ dbr:{brand} dbp:slogan ?slo. }}
            }}
    ''')
    sparql.setReturnFormat(JSON)
    qres = sparql.query().convert()
    result = qres['results']['bindings'][0]

    result.setdefault('abst', {'type': 'literal', 'xml:lang': 'pt', 'value': 'Indisponível'})
    result.setdefault('city', {'type': 'literal', 'xml:lang': 'en', 'value': '-'})
    result.setdefault('own', {'type': 'literal', 'xml:lang': 'en', 'value': '-'})
    result.setdefault('num', {'type': 'literal', 'xml:lang': 'en', 'value': '-'})
    result.setdefault('prod', {'type': 'literal', 'xml:lang': 'en', 'value': '-'})
    result.setdefault('slo', {'type': 'literal', 'xml:lang': 'en', 'value': '-'})

    name, abst, own, city, num, prod, slo = result['name']['value'], result['abst']['value'], result['own']['value'], \
                                            result['city']['value'], result['num']['value'], result['prod']['value'], \
                                            '"'+ result['slo']['value']+'"'

    own = own.replace('_', ' ').split('/')[-1]
    city = city.replace('_', ' ').split('/')[-1]

    tparams = {
        "name": name,
        "abstract": abst, 
        "city": city,
        "owner": own,
        "employees": num,
        "production": prod,
        "slogan": slo
    } 

    return render(request, 'about.html', tparams)
 

