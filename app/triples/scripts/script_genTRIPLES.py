import csv

with open('../cars_sells.csv', 'r') as read_csvfile:
    with open('../cars_sells.n3', 'w') as write_n3file:
        reader = csv.reader(read_csvfile, delimiter=',')
        #//writer = csv.writer(write_n3file, lineterminator='\n')
        line_count = 0
        for row in reader:
            if line_count == 0:
                write_n3file.write('''@prefix rdfs:    <http://www.w3.org/2000/01/rdf-schema#> .  
@prefix xsd:     <http://www.w3.org/2001/XMLSchema#> . 
@prefix gr:      <http://purl.org/goodrelations/v1#> . 
@prefix dbpedia: <http://dbpedia.org/resource/> . 
@prefix vso:     <http://purl.org/vso/ns#> . 
@prefix car:     <http://garagemdosusados.com/carros/#> . 
@prefix uco:     <http://purl.org/uco/ns#> . 
@prefix schema:  <http://schema.org/> . \n ''')   
                line_count = line_count + 1
            else:
                row14 = row[14].split(" ")
                row13 = row[13].split(" ")
                
                write_n3file.write('''
                car:{} a vso:Automobile, gr:ActualProductOrServiceInstance; 
                                gr:hasManufacturer dbpedia:{}; 
                                gr:hasBusinessFunction gr:Sell ; 
                                gr:hasMakeAndModel dbpedia:{}; 
                                gr:hasPriceSpecification [ a gr:UnitPriceSpecification ; 
                                                           gr:hasCurrency "EUR"^^xsd:string; 
                                                           gr:hasCurrencyValue "{}"^^xsd:float ] ; 
                                vso:modelDate "{}"^^xsd:integer ;
                                vso:VIN "{}"^^xsd:string; 
                                vso:color "{}"@pt ; 
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
                                vso:accelaration "{}"^^xsd:integer ; 
                                vso:previousOwners "{}"^^xsd:integer ; 
                                uco:pets "{}"@en; 
                                uco:smoking "{}"@en;
                                uco:currentLocation [ a schema:PostalAddress;
                                                        schema:addressCountry "PT"@pt; 
                                                        schema:addressRegion "{}"@pt ]; 
                                uco:ModificationOrMaintenance "{}"^^xsd:integer; 
                                uco:mileageEnd "{}"^^xsd:integer . \n'''.format(row[12].replace(" ", "_").replace("+", "Plus").replace("!", "ExclamationPoint").replace("/", "").replace('"', '').replace("''", "").replace("-", "_").replace(".", "_"),
             row13[0], 
             row14[1] + "_"  + row14[2],
             row[21],
             row[15],
             row[12],
             row[20],
             row[0],
             row[1],
             row[2],
             row[3],
             row[4],
             row[6],
             row[16],
             row[11],
             int(row[10])*2.352, 
             row[9],
             row[18],
             row[19],
             row[22],
             row[23],
             row[24],
             row[25],
             row[26],
             row[27]
             )) #i
                line_count = line_count + 1

