import os
import sqlite3
from os import system
import time
system("cls")

source = open('Covid19_limpio.csv', newline='', encoding='latin-1')
con=sqlite3.connect('C19Casos.db')
cursor=con.cursor()

def crear_tabla(): #Crea Las Tablas necesarias
    cursor.execute('''CREATE TABLE IF NOT EXISTS C19(
        Sexo TEXT NOT NULL,       
        Edad INTEGER NOT NULL,
        Provincia_Res TEXT NOT NULL,
        Fallecido TEXT NOT NULL,
        Confirmados TEXT NOT NULL
    )
    ''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS C22(
        Jurisdiccion TEXT NOT NULL,
        TT_Pob INTEGER NOT NULL,
        PVP INTEGER NOT NULL,
        PVC INTEGER NOT NULL,
        PSC INTEGER NOT NULL,
        TT_Pob_V INTEGER NOT NULL,
        PVPV INTEGER NOT NULL,
        PVCV INTEGER NOT NULL,
        PSCV INTEGER NOT NULL,
        TT_Pob_M INTEGER NOT NULL,
        PVPM INTEGER NOT NULL,
        PVCM INTEGER NOT NULL,
        PSCM INTEGER NOT NULL
    )
    ''')
    print('Tablas creadas con exito')

def cargar_tabla(): #Carga de Tablas de Casos de Covid 19
    lines=source.readlines()
    for line in lines:
        line = line.split(';')
        if(line[0]=='sexo'):
            print('Exito')
        else:
            line[3]=line[3].upper()
            if line[1].strip()!='':
                edades=int(line[1])
                cass_original = line[4].strip().upper()
                if "CASO CONFIRMADO" in cass_original:
                    cass = "CASO CONFIRMADO"
                else:
                    cass = cass_original
                cursor.execute("INSERT OR REPLACE INTO C19 VALUES (?, ?, ?, ?, ?)", (line[0], edades, line[2], line[3], cass))
    con.commit()
    print("Tablas cargadas con Exito")

def cargar_tabla_c22(): #Carga de Tabla de Censos 2022
    source2=open('c2022_tp_c_resumen.csv')
    lines2=source2.readlines()
    for line2 in lines2:
        line2=line2.split(';')
        if line2[0]=="Jurisdiccion":
            print("Exito")
        else:
            cursor.execute("INSERT OR REPLACE INTO C22 VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)", (line2[0],line2[1],line2[2],line2[3],line2[4],line2[5],line2[6],line2[7],line2[8],line2[9],line2[10],line2[11],line2[12]))
    con.commit()
    print("Tabla Cargada Exitosamente")

def PromEdFall():#3 Edad promedio de fallecidos en cada provincia
    Fallecido = "SI"
    cursor.execute(f'''SELECT Provincia_Res, COUNT(Edad) AS TT_Edad, SUM(Edad) AS Ed FROM C19 WHERE Fallecido == '{Fallecido}'  GROUP BY Provincia_Res''')
    prom=cursor.fetchall()
    print("El promedio de Edad de personas fallecidas por provincia es:")
    for provincia, tt_edad, suma_edad in prom:
        promedio=suma_edad/tt_edad
        print(f"Provincia: {provincia}, Promedio de edad: {promedio:.2f}")

def Intervalos(): #4  Intervalos de clases de la variable edad
    cursor.execute('''
        SELECT ROUND(1 + 3.322 * (LOG(COUNT(Edad)) / LOG(10))) AS num_intervalos
        FROM C19;
    ''')
    k = cursor.fetchone()[0]
    print("Número de intervalos (Sturges):", k)
    cursor.execute(f'''
        SELECT 
            MIN(Edad) AS minimo, 
            MAX(Edad) AS maximo, 
            ROUND((MAX(Edad) - MIN(Edad)) / {k}, 2) AS ancho_intervalo 
        FROM C19;
    ''')
    resultado = cursor.fetchone()
    minimo, maximo, ancho = resultado
    print("Mínimo:", minimo)
    print("Máximo:", maximo)
    print("Ancho de intervalo:", ancho)
    caso_Confirmado="CASO CONFIRMADO"
    SI="SI"
    intervalos = []
    inicio = minimo
    for i in range(int(k)):
        fin = inicio + ancho
        intervalos.append((inicio, fin))
        inicio = fin

    print("\nDistribución por intervalos:")
    mayor_confirmados = (None, 0)
    mayor_fallecidos = (None, 0)

    for ini, fin in intervalos:
        cursor.execute(f"""
            SELECT
                COUNT(*) 
            FROM C19 
            WHERE Edad >= {ini} AND Edad < {fin} AND Confirmados = '{caso_Confirmado}'
        """)
        confirmados = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT  
                COUNT(*) 
            FROM C19 
            WHERE Edad >= {ini} AND Edad < {fin} AND Fallecido = '{SI}'
        """)
        fallecidos = cursor.fetchone()[0]
       
        print(f"Intervalo {int(ini)} - {int(fin)}: Confirmados = {confirmados}, Fallecidos = {fallecidos}")

        if confirmados > mayor_confirmados[1]:
            mayor_confirmados = (f"{int(ini)} - {int(fin)}", confirmados)
        if fallecidos > mayor_fallecidos[1]:
            mayor_fallecidos = (f"{int(ini)} - {int(fin)}", fallecidos)
    print(f"Intervalo con más casos confirmados: {mayor_confirmados[0]} ({mayor_confirmados[1]})")
    print(f"Intervalo con más fallecidos: {mayor_fallecidos[0]} ({mayor_fallecidos[1]})")

def Fallecidos(): #5 Intervalo de edad donde se registró el mayor número de mujeres y hombres fallecidos
    cursor.execute('''
        SELECT ROUND(1 + 3.322 * (LOG(COUNT(Edad)) / LOG(10))) AS num_intervalos
        FROM C19;
    ''')
    k = cursor.fetchone()[0]
    print("Número de intervalos (Sturges):", k)
    cursor.execute(f'''
        SELECT 
            MIN(Edad) AS minimo, 
            MAX(Edad) AS maximo, 
            ROUND((MAX(Edad) - MIN(Edad)) / {k}, 2) AS ancho_intervalo 
        FROM C19;
    ''')
    resultado = cursor.fetchone()
    minimo, maximo, ancho = resultado
    print("Mínimo:", minimo)
    print("Máximo:", maximo)
    print("Ancho de intervalo:", ancho)
    M="M"
    F="F"
    SI="SI"
    intervalos = []
    inicio = minimo
    for i in range(int(k)):
        fin = inicio + ancho
        intervalos.append((inicio, fin))
        inicio = fin

    print("\nDistribución por intervalos:")
    Hombre_Fallecido = (None, 0)
    Mujer_Fallecida = (None, 0)

    for ini, fin in intervalos:
        cursor.execute(f"""
            SELECT 
                COUNT(*) 
            FROM C19 
            WHERE Edad >= {ini} AND Edad < {fin} AND Fallecido = '{SI}' AND Sexo = '{M}'
        """)
        HF = cursor.fetchone()[0]

        cursor.execute(f"""
            SELECT 
                COUNT(*) 
            FROM C19 
            WHERE Edad >= {ini} AND Edad < {fin} AND Fallecido = '{SI}' AND Sexo = '{F}'
        """)
        MF = cursor.fetchone()[0]

        print(f"Intervalo {int(ini)} - {int(fin)}: Hombres Fallecidos = {HF}, Mujeres Fallecidas = {MF}")

        if HF > Hombre_Fallecido[1]:
            Hombre_Fallecido = (f"{int(ini)} - {int(fin)}", HF)
        if MF > Mujer_Fallecida[1]:
            Mujer_Fallecida = (f"{int(ini)} - {int(fin)}", MF)

    print(f"Intervalo con más Hombres Fallecidos: {Hombre_Fallecido[0]} ({Hombre_Fallecido[1]})")
    print(f"Intervalo con más Mujeres Fallecidas: {Mujer_Fallecida[0]} ({Mujer_Fallecida[1]})")

def CCPP(): #6 Registró de mayor número de casos confirmados en mujeres y hombres
    caso="CASO CONFIRMADO"
    F="F"
    M="M"
    cursor.execute(f"SELECT Provincia_Res, COUNT(*) AS cantida FROM C19 WHERE Confirmados='{caso}' AND Sexo = '{F}' GROUP BY Provincia_Res ORDER BY cantida DESC LIMIT 1")
    provincia1 = cursor.fetchone()
    print(f"En la provincia { provincia1[0]}. Se registran La mayor cantidad de Mujeres En Caso Confirmado")
    cursor.execute(f"SELECT Provincia_Res, COUNT(*) AS cantida FROM C19 WHERE Confirmados='{caso}' AND Sexo = '{M}' GROUP BY Provincia_Res ORDER BY cantida DESC LIMIT 1")
    provincia2 = cursor.fetchone()
    print(f"En la provincia { provincia2[0]}. Se registran La mayor cantidad de Hombres En Caso Confirmado")

def MenorR():#7 Jurisdicción que registró la menor proporción de casos confirmados
    caso = "CASO CONFIRMADO"
    
    cursor.execute("""
        SELECT Provincia_Res, COUNT(Confirmados) AS cantidad 
        FROM C19 
        WHERE Confirmados = ?
        GROUP BY Provincia_Res
        ORDER BY cantidad ASC
    """, (caso,))
    
    resultados = cursor.fetchall()
    
    menor_proporcion = None
    
    for provincia, cantidad in resultados:
        cursor.execute("SELECT TT_Pob FROM C22 WHERE Jurisdiccion = ?", (provincia,))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            try:
                poblacion = float(resultado[0])
                proporcion = (cantidad / poblacion)
                
                if menor_proporcion is None or proporcion < menor_proporcion:
                    menor_proporcion = proporcion
                    menorprov = provincia
            except:
                continue
    
    if menor_proporcion is not None:
        print(f"La menor proporcion se registro en la provincia de: {menorprov} con un porcentaje de {menor_proporcion:.2}")

def MayorFallecidos(): #8 Registró de mayor porcentaje de fallecidos
    Fallecido="SI"
    cursor.execute(f"""
        SELECT Provincia_Res, COUNT(Fallecido) AS cantidad
        FROM C19
        WHERE Fallecido = '{Fallecido}'
        GROUP BY Provincia_Res
    """)
    resultados = cursor.fetchall()
    cursor.execute(f"""SELECT COUNT(Fallecido) AS cant FROM C19 WHERE Fallecido = '{Fallecido}'""")
    cant=cursor.fetchone()
    mayorpor=0.0
    MayProv=None
    for prov, fall in resultados:
        porcentaje=(float(fall)*100)/float(cant[0])
        if porcentaje>mayorpor:
            mayorpor = porcentaje
            MayProv=prov
    print(f"La Provincia con mayor porcentaje es {MayProv}, con {mayorpor:.2f}%")
    
    mayor_proporcion = 0.0
    provincia_mayor = None

    for provincia, fallecidos in resultados:
        cursor.execute("SELECT TT_Pob FROM C22 WHERE Jurisdiccion = ?", (provincia,))
        resultado = cursor.fetchone()
        
        if resultado is not None:
            try:
                poblacion = float(resultado[0])
                proporcion = fallecidos / poblacion
                
                if proporcion > mayor_proporcion:
                    mayor_proporcion = proporcion
                    provincia_mayor = provincia
            except:
                continue
    
    if provincia_mayor is not None:
        print(f"La provincia con mayor proporción de fallecidos es {provincia_mayor} ({mayor_proporcion:.2})")

def IndicePorSexo(): #9 Mayor índice de casos confirmados en mujeres y en varones
    sexos = {'F': 'Mujeres', 'M': 'Varones'}
    indices = {}

    for s in sexos:
        cursor.execute("""
            SELECT COUNT(*) FROM C19
            WHERE Confirmados = 'CASO CONFIRMADO' AND Sexo = ?
        """, (s,))
        cantidad = cursor.fetchone()[0]
        indices[sexos[s]] = cantidad

    print("Sexo     | Casos Confirmados")
    print("----------------------------")
    for sexo, cant in indices.items():
        print(f"{sexo:<9}| {cant}")

    mayor = max(indices, key=indices.get)
    print(f"Se observa el mayor índice de casos confirmados en: {mayor}")

opc=int(input("\tIngrese\n[1] Menu de Tablas\n[2] Mostrar promedio de fallecidos por provincia\n[3] Intervalos de Confirmados y Fallecidos\n[4] Intervalo de Hombres y Mujeres Fallecidas\n[5] Casos Confirmados Por Provincia\n[6] Menor Proporcion de Casos Confirmados\n[7] Mayor porcentaje de Fallecidos\n[8] Mayor Indices de Casos Confirmados\n[0] Salir: "))
while(opc!=0):
    if(opc==1):
        opc2=int(input("Ingrese\n[1] Para Crear Tablas\n[2] Para Cargar Tabla de Covid\n[3] Para Cargar Tabla de Censo\n"))
        if (opc2==1):
            crear_tabla()
        elif(opc2==2):
            cargar_tabla()
        elif(opc2==3):
            cargar_tabla_c22()
        else:
            print("Opcion Invalida")
    elif(opc==2):
        PromEdFall()
        time.sleep(5)
    elif(opc==3):
        Intervalos()
        time.sleep(5)
    elif(opc==4):
        Fallecidos()
        time.sleep(5)
    elif(opc==5):
        CCPP()
        time.sleep(5)
    elif(opc==6):
        MenorR()
        time.sleep(5)
    elif(opc==7):
        MayorFallecidos()
        time.sleep(5)
    elif(opc==8):
        IndicePorSexo()
        time.sleep(5)
    else:
        print("Elija una de las Opciones:")
    print("---------------------------------")
    opc=int(input("\tIngrese\n[1] Menu de Tablas\n[2] Mostrar promedio de fallecidos por provincia\n[3] Intervalos de Confirmados y Fallecidos\n[4] Intervalo de Hombres y Mujeres Fallecidas\n[5] Casos Confirmados Por Provincia\n[6] Menor Proporcion de Casos Confirmados\n[7] Mayor porcentaje de Fallecidos\n[8] Mayor Indices de Casos Confirmados\n[0] Salir: "))
    system("cls")
con.close()

