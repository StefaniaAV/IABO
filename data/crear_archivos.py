import csv
path = 'izquierda'
archivo = path + '/Giro a la izquierda.csv'

lista = []
datosn = []
with open (archivo, 'r', newline = '') as csvfile:
    datos = csv.reader(csvfile, delimiter=';')
    next(datos)
    for row in datos:
        row.pop(0)
        lista.append(row)
print(lista[0:3])
entradas = int(len(lista)/20)
inicio = 0
for i in range(1,21):
    muestra = lista[inicio:entradas*i]
    resultado = f'izquierda_{i}.csv'
    inicio += entradas
    with open (path + '/'+ resultado, 'w', newline = '') as csvfile:
        writer = csv.writer(csvfile, delimiter=';')
        writer.writerows(muestra)