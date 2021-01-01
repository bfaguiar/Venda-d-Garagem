import random 
import csv

with open('../cars.csv', 'r') as read_csvfile:
    with open('../cars_sells.csv', 'w') as write_csvfile:
        
        reader = csv.reader(read_csvfile, delimiter=',')
        writer = csv.writer(write_csvfile, lineterminator='\n') 
        colors = ["Branco", "Prateado", "Cinzento", "Preto", "Encarnado", "Amarelo", "Azul", "Azul Marinho", "Verde", "Laranja", "Verde Corrida", "Azul Corrida", "Laranja Lava"]
        speedV1 = [170, 171, 175, 180, 185, 190, 200, 210]
        speedV2 = [215, 217, 220, 222, 223, 225, 227, 230, 235, 237, 240]
        speedV3 = [244, 245, 247, 250, 255, 260] 
        speedV4 = [270, 290, 300, 320, 350] 
        
        accelV1 = [12.0, 11.5, 10.5, 9.8, 9.5, 9.2, 9.4, 9.0]
        accelV2 = [8.8, 8.5, 8.4, 8.2, 8.0, 7.8, 7.5, 7.4, 7.2, 7.0, 6.5]
        accelV3 = [ 6.0, 5.5, 5.0, 4.5, 4.0]
        accelV4 = [3.0, 3.5, 2.5, 2.0, 1.9]
        doors = [2, 5, 2, 4, 5, 5]
        valueV1 = [15000, 20000, 25000, 30000, 35000, 40000]
        valueV2 = [45000, 50000, 55000, 60000, 65000]
        valueV3 = [70000, 75000, 80000, 85000, 90000, 95000]
        valueV4 = [100000, 150000, 200000, 250000]
        
        number_of_owners = [1, 1, 1, 2, 2, 3, 4, 5]
        pets = ["Yes", "No"]
        smoking = ["Yes", "No"]
        location = ["Viana do Castelo", "Braga", "Vila Real", "Bragança", "Porto", "Aveiro", "Viseu", "Guarda", "Coimbra", "Castelo Branco", "Santarém", "Lisboa", "Portalegre", "Évora", "Setúbal", "Beja", "Faro", "Açores", "Madeira"]
        number_of_replacements = [0, 1, 2, 3, 4]
        km = [10, 1000, 2000, 5000, 10000, 20000, 30000, 40000, 50000, 60000, 70000, 80000, 90000, 100000, 150000, 120000, 170000, 200000, 250000, 300000]

        line_count = 0
        
        for row in reader:
            if line_count == 0:
                row.append('Speed.Maximum')
                row.append('Speed.Accelaration')
                row.append('Color')
                row.append('Price')
                row.append('number_of_owners')
                row.append('pets')
                row.append('smoking')
                row.append('location')
                row.append('number_of_replacements')
                row.append('km')
                writer.writerow(row)
                line_count = line_count + 1
            
            else:
                if int(row[16]) < 125:
                    row.append(speedV1[random.randrange(0, len(speedV1))])
                    row.append(accelV1[random.randrange(0, len(accelV1))])
                    row.append(colors[random.randrange(0, len(colors))])
                    row.append(valueV1[random.randrange(0, len(valueV1))])
                    row.append(number_of_owners[random.randrange(0, len(number_of_owners))])
                    row.append(pets[random.randrange(0, len(pets))])
                    row.append(smoking[random.randrange(0, len(smoking))])
                    row.append(location[random.randrange(0, len(location))])
                    row.append(number_of_replacements[random.randrange(0, len(number_of_replacements))])
                    row.append(km[random.randrange(0, len(km))])

                elif (int(row[16]) >= 125) and (int(row[16]) < 225):
                    row.append(speedV2[random.randrange(0, len(speedV2))])
                    row.append(accelV2[random.randrange(0, len(accelV2))])
                    row.append(colors[random.randrange(0, len(colors))])
                    row.append(valueV2[random.randrange(0, len(valueV2))])
                    row.append(number_of_owners[random.randrange(0, len(number_of_owners))])
                    row.append(pets[random.randrange(0, len(pets))])
                    row.append(smoking[random.randrange(0, len(smoking))])
                    row.append(location[random.randrange(0, len(location))])
                    row.append(number_of_replacements[random.randrange(0, len(number_of_replacements))])
                    row.append(km[random.randrange(0, len(km))])
                elif (int(row [16]) >= 225) and (int(row[16]) < 335):
                    row.append(speedV3[random.randrange(0, len(speedV3))])
                    row.append(accelV3[random.randrange(0, len(accelV3))])
                    row.append(colors[random.randrange(0, len(colors))])
                    row.append(valueV3[random.randrange(0, len(valueV3))])
                    row.append(number_of_owners[random.randrange(0, len(number_of_owners))])
                    row.append(pets[random.randrange(0, len(pets))])
                    row.append(smoking[random.randrange(0, len(smoking))])
                    row.append(location[random.randrange(0, len(location))])
                    row.append(number_of_replacements[random.randrange(0, len(number_of_replacements))])
                    row.append(km[random.randrange(0, len(km))])
                else:
                    row.append(speedV4[random.randrange(0, len(speedV4))])
                    row.append(accelV4[random.randrange(0, len(accelV4))])
                    row.append(colors[random.randrange(0, len(colors))])
                    row.append(valueV4[random.randrange(0, len(valueV4))])
                    row.append(number_of_owners[random.randrange(0, len(number_of_owners))])
                    row.append(pets[random.randrange(0, len(pets))])
                    row.append(smoking[random.randrange(0, len(smoking))])
                    row.append(location[random.randrange(0, len(location))])
                    row.append(number_of_replacements[random.randrange(0, len(number_of_replacements))])
                    row.append(km[random.randrange(0, len(km))])

                writer.writerow(row)
                line_count = line_count + 1 
