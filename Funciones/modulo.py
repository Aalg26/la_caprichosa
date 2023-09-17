import pandas as pd
import requests
from bs4 import BeautifulSoup
import time
import re

#codigos ligas:
#inglesas=9,10
#españolas=12,17
#italianas=11,18
#francesa=13,60
#alemanas=20,33

def get_teams(res):#obtiene los equipos y los codigos.
    
    #url=f'https://fbref.com/es/comps/9' url de ejemplo para el res

    soup= BeautifulSoup(res.text, 'html.parser')
    #de la sopa obtengo todos los tbody
    tbodys=soup.find_all("tbody")
    #entre los tbodys elijo el 11 y extraigo los tr
    trs=tbodys[11].find_all('tr')
    ths=[]
    codigos=[]
    equipos=[]
    #a la lista llamada ths le agrego cada th de la clase left en forma de texto
    for tr in trs:
        ths.append(str(tr.find('th', class_='left')))
    #parto cada th en 2 y luego lo vuelvo a dividir y me quedo solo con elemento que
    #contiene el codigo y lo agrego a la lista codigos y lo mismo para obtener los equipos
    
    for th in ths: 
        texto_split=th.split('href="/es/equipos/')
        codigos.append(texto_split[1].split('/Estadisticas')[0].strip())
        equipos.append(texto_split[1].split('>vs.')[1].split('</a>')[0].strip())
        
    
    return [equipos,codigos ]

def get_players_code(res):#devuelve el codigo de los jugadores de un equipo

    #url1='https://fbref.com/es/equipos/53a2f082/' url de ejemplo para el res

    soup=BeautifulSoup(res.text, 'html.parser')
    jugadoreshtml=soup.find_all('tbody')[11].find_all('tr')
    codigo_jugadores=[]
    for i in range(len(jugadoreshtml)):
        codigo_jugadores.append(str(jugadoreshtml[i]).split('csv="')[1].split('" data-stat="player"')[0])
    
    return codigo_jugadores

def get_player_stats_last365(codigosJ):#devuelve las estadisticas de los jugadores de la lista en los ultimos 365 dias
    

    columnas=['Goles sin penalización','Goles esperados (xG) sin contar penaltis','Total de disparos','Asistencias',
              'xAG','npxG + xAG','Acciones para la creación de tiros','Pases intentados','% de pase completo',
              'Pases progresivos','Acarreos progresivos','Tomas exitosas','Toques (Ataq. pen.)','Pases progresivos Rec',
              'Derribos','Intercepciones','Bloqueos','Despeje','Aéreos ganados']
    tabla=pd.DataFrame(columns=columnas)
    for codigo in codigosJ:
        url2=f'https://fbref.com/es/jugadores/{codigo}/'
        pagina=pd.read_html(url2)
        numeritos=pagina[0]['Por 90'].dropna()
        columnas_estadisticas=pagina[0]['Estadísticas'].dropna()
        tablajr=pd.DataFrame([list(numeritos)], columns=list(columnas_estadisticas))
        tabla=pd.concat([tablajr, tabla], ignore_index=True)
        time.sleep(2)

    return tabla

def year():#devuelve el año en el que se corre el codigo
    # Obtiene el tiempo actual en segundos desde el epoch (1 de enero de 1970 hasta el momento actual).
    tiempo_actual = time.time()

    # Convierte el tiempo en una estructura de tiempo local
    estructura_tiempo = time.localtime(tiempo_actual)

    # Obtiene el año de la estructura de tiempo
    año_actual = estructura_tiempo.tm_year

    return año_actual

def listnEditions(nEditions, current_year):#devuelve una lista con los años de las ligas debes introducir
                                           # la cantidad de años y el año actual
    Editions=[]
    for i in range(nEditions):
        last_year=current_year-1
        Editions.append(f'{last_year}-{current_year}')
        current_year-=1

    return Editions

def drop_duplicates_columns(tabla,col,pos):#elimina una columna si una tabla tiene 2, requiere como parametro la tabla, el nombre de la columna y la posicion
                                            #respecto a la otra columna es decir si tienes: tabla.columns=[A1 , B , C, A2](los numeros son para distinguirlas)  
                                            #como columnas, la funcion crea un dataframe solo con las dos columnas [A1, A2] en el mismo orden que tenian en la
                                            #tabla y tu debes decirle cual de las 2 es la que te importa por ejemplo drop_duplicates_columns(tabla, 'A',1) te 
                                            # devuelve la segunda A(A2)


    for columna, i in zip(tabla.columns, range(len(tabla.columns))):
    
        if columna == col:
            #creo un df con las dos columnas pero con iloc[:,[1]] muestro todas las filas pero solo la columna 1
            columnasave=tabla[f'{tabla.columns[i]}'].iloc[:,[pos]]
            #dropeo las columnas 
            tabla=tabla.drop(tabla.columns[i], axis=1)
            break
    tabla=pd.concat([tabla, columnasave], axis=1)

    return tabla

def get_players_mean(res,url): # ejemplo url https://fbref.com/es/equipos/b8fd03ef/2022-2023/all_comps/Estadisticas-de-Manchester-City-Todas-las-competencias

    codigoE=url.split('equipos/')[1].split('/20')[0]
    soup=BeautifulSoup(res.text, 'html.parser')
    pagina=pd.read_html(url)
    tamaño=len(soup.find('div', class_='filter switcher'))
    tablas=[]
    tablas.append(pagina[0])

    ##BLOQUE 1 

    #defino que tablas voy a usar
    for i in range(1,5):
        tablas.append(pagina[(i*tamaño-(i-1))])
    for i in range(6,9):
        tablas.append(pagina[(i*tamaño-(i-1))])
    tablas.append(pagina[10*tamaño-9])

    #elimino los encabezados de las tablas y filtro a los jugadores con mas de 5 min jugados en promedio en la temporada
    for i in range(9):
        tablas[i].columns=tablas[i].columns.droplevel(level=0)
        tablas[i]=tablas[i][tablas[i]['90 s']>=5]

    
    ## BLOQUE 2
    
    dfs_arreglados=[]
    for i, df in enumerate(tablas):

        if i == 0:
            #elimino las columnas duplicadas
            duplicates=['G-TP','npxG','xAG','npxG+xAG']
            for duplicate in duplicates:
                df=drop_duplicates_columns(df,duplicate,1)
            #me quedo con las columnas que necesito
            df = df.loc[:,['Jugador', 'Posc', 'Edad', '90 s', 'PrgC', 'PrgP', 'PrgR', 'Ast','G-TP', 'npxG', 'xAG', 'npxG+xAG']]
            # como los apartados de Prg estan en total y no por 90min los pasare a 90 min
            Prgs=['PrgC','PrgP','PrgR']   
            for Prg in Prgs:
                df[f'{Prg}']=round(df[f'{Prg}']/df['90 s'], 2)
            #agrego el dataframe nuevo a la lista de dfs 
            dfs_arreglados.append(df)

        if i ==1:
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','GC90','% Salvadas','PaC%',]]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

        if i ==2:    
            
            df=drop_duplicates_columns(df,'Long. prom.',1)
            df=drop_duplicates_columns(df,'Int.',2)
            df=drop_duplicates_columns(df,'%deLanzamientos',0)
            df['Int.']=round(df['Int.']/df['90 s'],2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador', 'PSxG/SoT', '/90','%deLanzamientos','Int.','% de Stp', 'Núm. de OPA/90', 'DistProm.', 'Long. prom.']]
            #agrego el dataframe nuevo a la lista de dfs 
            dfs_arreglados.append(df)
        if i == 3:
            #cambio el apartado de Dis a Dis por 90min
            df.loc[:, 'Dis'] = round(df['Dis'] / df['90 s'], 2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','Dis']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)
        if i == 4:
            #elimino las columnas duplicadas
            duplicates=['Int.','% Cmp']
            for duplicado in duplicates:
                df=drop_duplicates_columns(df,duplicado,0)
            df['Int.']=round(df['Int.']/df['90 s'],2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','Int.','% Cmp']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

        if i == 5:

            df.loc[:,'ACT']=round(df['ACT']/df['90 s'],2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','ACT']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

        if i == 6:

            df=drop_duplicates_columns(df,'Tkl',0)
            df['Tkl']=round(df['Tkl']/df['90 s'], 2)
            df['Bloqueos']=round(df['Bloqueos']/df['90 s'], 2)
            df['Int']=round(df['Int']/df['90 s'], 2)
            df['Desp.']=round(df['Desp.']/df['90 s'], 2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','Desp.','Int','Bloqueos','Tkl']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

        if i == 7:
            df.loc[:,'Ataq. pen.']=round(df['Ataq. pen.']/df['90 s'], 2)
            df.loc[:,'Toques']=round(df['Toques']/df['90 s'], 2)
            df.loc[:,'Succ']=round(df['Succ']/df['90 s'], 2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','Ataq. pen.','Toques','Succ']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

        if i == 8:

            df.loc[:,'Ganados']=round(df['Ganados']/df['90 s'], 2)
            #me quedo con las columnas que necesito
            df = df.loc[:, ['Jugador','Ganados']]
            #agrego el dataframe nuevo a la lista de dfs
            dfs_arreglados.append(df)

    ## BLOQUE 3
    temp=dfs_arreglados[0]
    i=0
    while i < 8:
        resultado = pd.merge(temp,dfs_arreglados[i+1], on='Jugador', how='outer')
        temp=resultado
        i+=1
    ## BLOQUE 4
    allteams=pd.read_csv(r'C:\Users\ARTUROS\Desktop\Archivos Adrian\personal\proyectos personales\lacaprichosa\dataset\All_teams.csv')
    resultado['Jugador']=int(allteams[allteams['id Web']==f'{codigoE}']['id_ml'].iloc[0])
    resultado.rename(columns={'Jugador':'Equipo'})

    ## BLOQUE 5
    resultado=resultado.drop('Posc', axis=1)
    resultado=resultado.groupby('Jugador').mean().reset_index()
    resultado=resultado.rename(columns={'Jugador':'Equipo id'})

    return resultado

def get_numbers(cadena):
    # Utiliza expresiones regulares para encontrar todos los números en la cadena.
    # El patrón \d+\.\d+|\d+ busca números enteros o decimales en la cadena.
    numeros_encontrados = re.findall(r'\d+\.\d+|\d+', str(cadena))
    
    # Si se encuentran números en la cadena:
    if numeros_encontrados:
        # Une los números encontrados utilizando comas y devuelve la cadena resultante.
        return ''.join(numeros_encontrados)
    
    # Si no se encuentran números en la cadena, devuelve 0.
    return 0