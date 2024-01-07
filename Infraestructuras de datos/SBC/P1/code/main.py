import requests
import os
import json
import argparse
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter

#Declaración de clases
class Usuario:

    #Atributos de la clase
    nombre: str
    apellido: str
    genero: int
    pais: str
    edad: int
    telf: str
    pasw: str

    #Constructor de la clase
    def __init__(self, nombre, apellido, genero, pais, edad, telf, pasw):
        self.nombre = nombre
        self.apellido = apellido
        if genero == "male" or genero == '1': 
            self.genero = '1' 
        else: 
            self.genero = '0'
        self.pais = pais
        self.edad = edad
        self.telf = telf
        self.pasw = pasw
    
    def obtener_atributo(self, nombre_atributo):
        if hasattr(self, nombre_atributo):  # Verifica si el atributo existe en la clase
            valor = getattr(self, nombre_atributo)  # Obtiene el valor del atributo usando getattr()
            return valor
        else:
            return f"El atributo {nombre_atributo} no existe en la clase."


 
class Pais:

    #Atributos de la clase
    pais: str
    usuarios: list

    #Atributos constantes de la clase
    edad_min = 20
    edad_max = 35

    #Constructor de la clase
    ### Función que obtiene de la carpeta de "countries" el pais que se le pasa como parametro
    ### Y analiza linea a linea el archivo txt y obtiene los usuarios para guardarlos en una lista
    ### Esta lista será una lista de variables tipo Usuario.

    # self Pais parametro propio de la clase
    # pais str pais del cual se quiere crear un objeto
    def __init__(self, pais):
        self.pais = pais
        self.usuarios = []
        with open(os.path.dirname(os.getcwd())+"/countries/"+pais+'/'+pais+'.txt','r',encoding='utf-8') as archivo:
            for obj in archivo:
                self.usuarios.append(Usuario(**json.loads(obj)))
                
    #Método ejemplo de la clase
    ### Función que devuelve los usuarios comprendidos entre la edad_min y la edad_max

    # self Pais parametro propio de la clase
    # return res list lista de usuarios
    def getEncuestaUsuarios(self):
        res = []
        for i in self.usuarios:
            if i.edad >= self.edad_min and i.edad <= self.edad_max:
                res.append(i)
        return res
    

#Declaración de las funciones (métodos) públicas que se van a usar

### Función que descarga los datos de la url proporcionada, y los guarda en un dict
def descargar_datos(url,numero_personas):
    return requests.get(url+'/?results='+str(numero_personas)).json()['results']

### Función que transforma todos los datos a tipo clase Usuario y los carga en los ficheros locales
def cargar_datos(data):
    def crear_carpeta(lista_paises,actual):
        if not actual in lista_paises and not os.path.exists(os.path.dirname(os.getcwd())+"/countries/"+actual):
            os.mkdir(os.path.dirname(os.getcwd())+"/countries/"+actual)
            lista_paises.add(actual)
    ################################################################################
    
    lista_paises = set()
    for i in data:
        newU = Usuario(i['name']['first'],i['name']['last'],i['gender'],i['location']['country'],
                    i['dob']['age'],i['phone'], i['login']['password'])
        pais_actual = i['location']['country']
        crear_carpeta(lista_paises,pais_actual)
        with open(os.path.dirname(os.getcwd())+"/countries/" + pais_actual+ "/"+ pais_actual+ '.txt', 
                  'a',encoding='utf-8') as archivo:
            archivo.write(json.dumps(newU.__dict__)+"\n")

### Función que obtiene una lista con todos los paises distintos
def getListaPaises():
    return os.listdir(os.path.dirname(os.getcwd())+"/countries")

### Función que obtiene todos los usuarios de todos los paises y los guarda almacenados 
### en una lista de objetos tipo Pais, donde cada Pais tendrá su propio atributo
### usuarios que contendre la lista de todos los usuarios del pais
def getTodo():
    toda_data = []
    for c in getListaPaises():
        toda_data.append(Pais(c))
    return toda_data


### Función principal del codigo. Es lo que se ejecuta cuando se lanza el archivo.py
### En esta función se encontrará todo el proceso de carga realizado 4 veces para un total
### de 5000 usuarios por vez y después se procesaran los datos hasta obtenerlo todo.
### Una vez todo, ya se podrá volver a procesar y sacar las estadisticas que hagan falta 
   
def estadistica_genero(nombre_pais):
    
    
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    total_hombres = sum(1 for usuario in pais.usuarios if usuario.genero == '1')
    total_mujeres = total_usuarios - total_hombres

    porcentaje_hombres = (total_hombres / total_usuarios) * 100
    porcentaje_mujeres = (total_mujeres / total_usuarios) * 100
    
    print(f"Estadísticas de sexo para {nombre_pais}:")
    print(f"Total de usuarios: {total_usuarios}")
    print(f"Porcentaje de hombres: {porcentaje_hombres:.2f}%")
    print(f"Porcentaje de mujeres: {porcentaje_mujeres:.2f}%\n")


def estadistica_edades(nombre_pais,flag):
     
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    menores_de_edad = 0
    juventud = 0
    adultez = 0
    personas_mayores = 0

    for usuario in pais.usuarios:
        edad = usuario.edad
        if edad < 18:
            menores_de_edad += 1
        elif 18 <= edad <= 26:
            juventud += 1
        elif 27 <= edad <= 59:
            adultez += 1
        else:
            personas_mayores += 1

    

    porcentaje_menores_de_edad = (menores_de_edad / total_usuarios) * 100
    porcentaje_juventud = (juventud / total_usuarios) * 100
    porcentaje_adultez = (adultez / total_usuarios) * 100
    porcentaje_personas_mayores = (personas_mayores / total_usuarios) * 100

    mi_diccionario = {
        'menores':menores_de_edad,
        'juventud': juventud,
        'adultez': adultez,
        'mayores': personas_mayores,
        'total_u': total_usuarios
    }
    if flag:
        return mi_diccionario
    else:
        print(f"Estadísticas de edades para {nombre_pais}:")
        print(f"Porcentaje de menores de edad: {porcentaje_menores_de_edad:.2f}%")
        print(f"Porcentaje de juventud: {porcentaje_juventud:.2f}%")
        print(f"Porcentaje de adultez: {porcentaje_adultez:.2f}%")
        print(f"Porcentaje de personas mayores: {porcentaje_personas_mayores:.2f}%\n") 
    
def contiene_letras_numeros(contraseña):
    tiene_letras = False
    tiene_numeros = False

    for caracter in contraseña:
        if caracter.isalpha():
            tiene_letras = True
        elif caracter.isdigit():
            tiene_numeros = True

    return tiene_letras and tiene_numeros
    
def estadistica_contraseñas(nombre_pais):
    pais = Pais(nombre_pais)  

    total_usuarios = len(pais.usuarios)
    seguridad_baja = 0
    seguridad_media = 0
    seguridad_alta = 0
    seguridad_extrema = 0

    for usuario in pais.usuarios:
        contraseña = usuario.pasw
        longitud_contraseña = len(contraseña)

        if longitud_contraseña < 5:
            seguridad_baja += 1
        elif 5 <= longitud_contraseña <= 8:
            if contiene_letras_numeros(contraseña):
                seguridad_alta += 1
            else:
                seguridad_media += 1
        elif 8 <= longitud_contraseña <= 12:
            if contiene_letras_numeros(contraseña):
                seguridad_extrema += 1
            else:
                seguridad_alta += 1
        else:
            seguridad_extrema += 1

    porcentaje_seguridad_baja = (seguridad_baja / total_usuarios) * 100
    porcentaje_seguridad_media = (seguridad_media / total_usuarios) * 100
    porcentaje_seguridad_alta = (seguridad_alta / total_usuarios) * 100
    porcentaje_seguridad_extrema = (seguridad_extrema / total_usuarios) * 100

    print(f"Estadísticas de contraseñas para {nombre_pais}:")
    print(f"Porcentaje contraseñas débiles: {porcentaje_seguridad_baja:.2f}%")
    print(f"Porcentaje de contraseñas medianamente seguras: {porcentaje_seguridad_media:.2f}%")
    print(f"Porcentaje de contraseñas seguras: {porcentaje_seguridad_alta:.2f}%")
    print(f"Porcentaje de contraseñas extremadamente seguras: {porcentaje_seguridad_extrema:.2f}%\n")

def distribucion_normal():
    data = getTodo()
    edades = np.array([])
    total_usuarios = 0
    for pais in data:
        total_usuarios = total_usuarios + len(pais.usuarios)
        for usuario in pais.usuarios:
            edades = np.append(edades,usuario.edad)
    media = np.mean(edades)
    desviacion_estandar = np.std(edades)

    
    x = np.linspace(0, 120, 1000)
    y = (1/(desviacion_estandar * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - media) / desviacion_estandar) ** 2)
    print(f"Para un total de: "+str(total_usuarios))
    print(f"La desviación estandard es de: "+str(desviacion_estandar))
    print(f"La media es de: "+str(media))

    # Graficar la distribución normal teórica
    plt.plot(x, y, label='Distribución Normal')
    plt.title('Distribución normal de edades en todos los paises ('+ str(total_usuarios)+')')
    plt.xlabel('Valores')
    plt.ylabel('Densidad de Probabilidad')
    plt.legend()
    plt.show()

    

if __name__ == "__main__":

    #Gestion de los argumentos de entrada
    parser = argparse.ArgumentParser(description="Ejecutar funciones desde la linea de comandos")
    parser.add_argument('--opcion', choices=['etl','estadistica_pais','encuesta', 'frecuencias'], help='Elige la funcion a ejecutar')
    args = parser.parse_args()

    #ETL
    if args.opcion == 'etl':
        numero_personas = 5000
        url = "https://randomuser.me/api"
        for _ in range(4): 
            cargar_datos(descargar_datos(url,numero_personas))

    #Estadistica especifica del pais
    elif args.opcion == 'estadistica_pais':
            nombre_pais = input("Ingrese el nombre del país: ")
            print("\n")
            estadistica_genero(nombre_pais)
            estadistica_edades(nombre_pais, False)
            estadistica_contraseñas(nombre_pais)

    # Obtencion de usuarios para hacer encuesta
    elif args.opcion == 'encuesta':

        pais = input("Ingrese el pais al que quiere hacer la encuesta: ")
        edad_min = input("Ingrese edad mínima: ")
        edad_max = input("Ingrese edad máxima: ")
        act_pais = Pais(pais)
        res = act_pais.getEncuestaUsuarios()
        with open(os.path.dirname(os.getcwd())+"/resultados/" + "/"+ act_pais.pais + "_"+edad_min+"_"+edad_max+ '.csv', 'w',encoding='utf-8') as archivo:
            archivo.write("Nombre;Apellido;Telefono;Edad \n")
            for usuario in res:
                archivo.write(usuario.nombre + ";" + usuario.apellido + ";" + usuario.telf + ";" + str(usuario.edad)+"\n")

    #Suma total de las coincidencias de atributo por archivo 
    elif args.opcion == 'frecuencias':
        attr = input("Ingrese atributo a comparar: ")
        lista_valores = []
        data = getTodo()
        total_usuarios = 0
        for pais in data:
            total_usuarios = total_usuarios + len(pais.usuarios)
            for usuario in pais.usuarios:
                lista_valores.append(usuario.obtener_atributo(attr))
        valores_frecuencias = Counter(lista_valores)
        print("Las frecuencias genericas de todo el dataset en cuanto a: "+attr+ "son: \n")
        print(valores_frecuencias)
        print("Con un total de "+str(len(valores_frecuencias))+" valores distintos.")

    # Estadistica general de las edades
    else:
        print("Calculando estadistica general de las edades...\n")
        total = getTodo()
        mi_diccionario_total = {
            'menores': 0,
            'juventud': 0,
            'adultez': 0,
            'mayores': 0,
            'total_u': 0
        }
        
        for p in total:
            diccionario_actual = estadistica_edades(p.pais, True)
            mi_diccionario_total['menores'] = mi_diccionario_total['menores'] + diccionario_actual['menores']
            mi_diccionario_total['juventud'] = mi_diccionario_total['juventud'] + diccionario_actual['juventud']
            mi_diccionario_total['adultez'] = mi_diccionario_total['adultez'] + diccionario_actual['adultez']
            mi_diccionario_total['mayores'] = mi_diccionario_total['mayores'] + diccionario_actual['mayores']
            mi_diccionario_total['total_u'] = mi_diccionario_total['total_u'] + diccionario_actual['total_u']
            
        porcentaje_menores_de_edad = (mi_diccionario_total["menores"] / mi_diccionario_total["total_u"]) * 100
        porcentaje_juventud = (mi_diccionario_total["juventud"] / mi_diccionario_total["total_u"] )* 100
        porcentaje_adultez = (mi_diccionario_total["adultez"] / mi_diccionario_total["total_u"]) * 100
        porcentaje_personas_mayores = (mi_diccionario_total["mayores"] / mi_diccionario_total["total_u"]) * 100
        
        
        print(f"Porcentaje total de menores de edad: {porcentaje_menores_de_edad:.2f}%")
        print(f"Porcentaje total de juventud: {porcentaje_juventud:.2f}%")
        print(f"Porcentaje total de adultez: {porcentaje_adultez:.2f}%")
        print(f"Porcentaje total de personas mayores: {porcentaje_personas_mayores:.2f}%")