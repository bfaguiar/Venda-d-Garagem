import csv
import random

lista_carrosIDs = []
lista_pessoasIDS = ['chico', 'santi', 'jonni', 'fonsi', 'rodri', 'martin','tomas', 'duarte',  'migas', 'gabi', 'mari', 'leo', 'mat',  'bea', 'carol', 'marian', 'ana', 'sofi', 'fran', 'ines' ]




#####################################################GENERATE CARROS SPECS#############################################################################

str_header_carros = '''@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .  
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> . 
@prefix gr:      <http://purl.org/goodrelations/v1#> . 
@prefix dbpedia: <http://dbpedia.org/resource/> . 
@prefix vso:     <http://purl.org/vso/ns#> . 
@prefix car:     <http://garagemdosusados.com/carros/#> . 
@prefix uco:     <http://purl.org/uco/ns#> . 
@prefix schema:  <http://schema.org/> . \n '''  

str_body_carros = '''
                car:{} a vso:Automobile, gr:ActualProductOrServiceInstance; 
                                gr:hasManufacturer dbpedia:{}; 
                                gr:hasBusinessFunction gr:Sell ; 
                                gr:hasMakeAndModel dbpedia:{}; 
                                vso:modelDate "{}"^^xsd:integer ;
                                vso:VIN "{}"^^xsd:string; 
                                vso:height "{}"^^xsd:integer ; 
                                vso:length "{}"^^xsd:integer ; 
                                vso:width "{}"^^xsd:integer ; 
                                vso:DriveWheelConfiguration "{}"@en ; 
                                vso:engineType "{}"^^xsd:string ; 
                                vso:gearsTotal "{}"^^xsd:integer ; 
                                vso:enginePower "{}"^^xsd:integer ; 
                                vso:TransmissionTypeValue "{}"@en; 
                                vso:FuelQuantity "{}"^^xsd:integer; 
                                vso:fuelType "{}"@en; 
                                vso:speed "{}"^^xsd:integer ; 
                                vso:accelaration "{}"^^xsd:integer .\n'''

with open('../cars_sells.csv', 'r') as read_csvfile:
    with open('../cars_specs.n3', 'w') as write_n3file:
        reader = csv.reader(read_csvfile, delimiter=',')
        #//writer = csv.writer(write_n3file, lineterminator='\n')
        line_count = 0
        for row in reader:
            if line_count == 0:
                write_n3file.write(str_header_carros)   
                line_count = line_count + 1
            else:
                row14 = row[14].split(" ")
                row13 = row[13].split(" ")
                row12 = row[12].replace(" ", "_").replace("+", "Plus").replace("!", "ExclamationPoint").replace("/", "").replace('"', '').replace("''", "").replace("-", "_").replace(".", "_")
                write_n3file.write(str_body_carros.format(row12, row13[0], row14[1] + "_"  + row14[2], row[15], row[12], 
                    row[0], row[1], row[2], row[3], row[4], row[6], row[16], row[11], int(row[10])*2.352,  row[9],
                    row[18], row[19],
                )) #i
                lista_carrosIDs.append(row12);
                line_count = line_count + 1 
 
#####################################################################################################################################

###################################################### GENERATE CAR VENDORS ##########################################################################

str_header = '''@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .  
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> . 
@prefix gr:      <http://purl.org/goodrelations/v1#> .  
@prefix vendor:  <http://garagemdosusados.com/vendors/#> .
@prefix person:  <http://garagemdosusados.com/pessoas/#> .   
@prefix sell:    <http://garagemdosusados.com/vendas/#> .
@prefix foaf:    <http://xmlns.com/foaf/0.1/> .
@prefix vso:     <http://purl.org/vso/ns#> .    
@prefix uco:     <http://purl.org/uco/ns#> .
@prefix schema:  <http://schema.org/> . \n
@prefix car:     <http://garagemdosusados.com/carros/#> .
'''

str_schema = '''
    vendor:{} a gr:Reseller;
              foaf:nick person:{};
              gr:offers sell:{} .
'''

price = [2000, 4000, 5000, 7000, 6000, 8000, 90000, 10000, 15000, 20000, 25000, 30000, 35000, 40000, 45000, 50000, 55000, 60000, 65000, 70000, 75000, 80000, 85000, 90000, 95000, 100000, 150000, 200000, 250000]
number_of_owners = [1, 1, 1, 2, 2, 3, 4, 5]

pets = ["Yes", "No"]
colors = ["Branco", "Prateado", "Cinzento", "Preto", "Encarnado", "Amarelo", "Azul", "Azul Marinho", "Verde", "Laranja", "Verde Corrida", "Azul Corrida", "Laranja Lava"]
smoking = ["Yes", "No"]
location = ["Viana do Castelo", "Braga", "Vila Real", "Bragança", "Porto", "Aveiro", "Viseu", "Guarda", "Coimbra", "Castelo Branco", "Santarém", "Lisboa", "Portalegre", "Évora", "Setúbal", "Beja", "Faro", "Açores", "Madeira"]
km = [10, 1000, 2000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 150000, 120000, 170000, 200000, 250000, 300000]

str_schema2 = '''
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
'''

with open('../vendors.n3', 'w') as wr:
    line_count = 0
    for row in lista_pessoasIDS: 
            if line_count == 0:
                wr.write(str_header) 
                line_count = line_count + 1 
            else:  
                str_aux = lista_carrosIDs.pop(random.randrange(0, len(lista_carrosIDs)))
                wr.write(str_schema.format(row, row, str_aux))
                wr.write(str_schema2.format(str_aux, str_aux, price[random.randrange(0, len(price))], colors[random.randrange(0, len(colors))], number_of_owners[random.randrange(0, len(number_of_owners))], pets[random.randrange(0, len(pets))],
                smoking[random.randrange(0, len(smoking))], location[random.randrange(0, len(location))],  km[random.randrange(0, len(km))]))
                line_count = line_count + 1

##############################################################################################################################################################

###################################### GENERATE CAR SELLS ##########################################################################################################




#################################################GENERATE PESSOAS CAARACTERISTICAS####################################################################################

# str_header_pessoas = '''@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .  
# @prefix xsd:     <http://www.w3.org/2001/XMLSchema#> .
# @prefix foaf:   <http://xmlns.com/foaf/0.1/> .
# @prefix person:  <http://garagemdosusados.com/pessoas/#> .  

# '''

# str_pessoas = '''
#             person:{} a foaf:Person;
#                       foaf:firstName "{}"@pt ;
#                       foaf:nick "{}"^^xsd:string; 
#                       foaf:mbox "{}"^^xsd:string;
#                       foaf:age "{}"^^xsd:integer;
#                       foaf:knows '''    


# line = 0 
# with open('../people.n3', 'w') as wr:
#     pessoas = [['Santiago', 'Coimbra', 48, 'santi', 'santi@gmail.com'], ['Francisco', 'Porto', 25, 'chico', 'chico@hotmail.com'], ['João', 'Beja', 50, 'jonni', 'jonni@gmail.com'], 
#             ['Afonso', 'Aveiro', 39, 'fonsi', 'fonsi@outlook.pt'], ['Rodrigo', 'Castelo Branco', 37, 'rodri', 'rodri@gmail.com'], ['Martim', 'Braga', 59, 'martin', 'mar@hotmail.com'], 
#             ['Tomás', 'Bragança', 43, 'tomas', 'tomas@up.pt'], ['Duarte', 'Viseu', 50, 'duarte', 'duarte@gmail.com'], ['Miguel', 'Castelo Branco', 57, 'migas', 'migas@outlook.pt'], 
#             ['Gabriel', 'Madeira', 20, 'gabi', 'gabi@gmail.com'], ['Maria', 'Bragança', 51, 'mari', 'mari@gmail.com'], ['Leonor', 'Vila Real', 40, 'leo', 'leo@yahoo.com'], 
#             ['Matilde', 'Faro', 46, 'mat', 'matilde@gmail.com'], ['Beatriz', 'Faro', 64, 'bea', 'bia@gmail.com'], ['Carolina', 'Guarda', 55, 'carol', 'carol79@gmail.com'], 
#             ['Mariana', 'Portalegre', 30, 'marian', 'amarian@gmail.com'], ['Ana', 'Lisboa', 63, 'ana', 'nan@outlook.pt'], ['Sofia', 'Santarém', 53, 'sofi', 'sof@ua.pt'], 
#             ['Francisca', 'Bragança', 53, 'fran', 'franxica@gmail.com'], ['Inês', 'Açores', 45, 'ines', 'in@gmail.com']]  
    
#     for row in pessoas:
#         pessoas.remove(row)
#         if line == 0:
#             wr.write( str_header_pessoas)
#             line = line + 1
#         else:
#             str1 = str_pessoas.format(row[3], row[0], row[3], row[4], row[2]);
#             n = random.randrange(2, 10);
#             for i in range(n):
#                 str1 = str1 + '''person:{} '''.format(pessoas[random.randrange(0, len(pessoas))][3]) 
#             wr.write(str1 + '.\n')
#             line = line + 1
#         pessoas.insert(line-1, row)
# print(lista_carrosIDs) 

###################################################################################################################################################



# ## GENERATE RDF CARS


## GENERATE RDF PEOPLE uncomment.







 