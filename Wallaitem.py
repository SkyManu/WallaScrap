

from bs4 import BeautifulSoup
import requests
class Wallaitem:


    def __init__(self,nombre,descripcion,precio):
        self.nombre = nombre
        self.descripcion = descripcion
        self.precio = precio
def SepararEnTuplas(lista):
    lista1 = lista[0]
    lista2 = (" ").join(lista[1:])
    res = (lista1, lista2)
    return res
 # f = results[12].text
 #                arr = f.split()
 #
 #                for elem in arr:
 #                    try:
 #
 #                        if elem == "AnteriorSiguiente":
 #                            lalista = arr[arr.index(elem) + 1:]
 #
 #                    except:
 #                        print("No se esta tratando la string correctamente")
 #
 #                print(lalista)

lista=["7","Cinco","mas","cinco"]
print(SepararEnTuplas(lista))





'''
Creacion de 1 item de prueba
w1= Wallaitem("Ps4","Es muy cara",500)

print(w1.nombre)
print(w1.precio)
'''