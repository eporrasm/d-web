from graphviz import Digraph
import textwrap

# Abriendo archivo json
# with open(
#     'codigo/jsons/asignaturasEmilio.json'
#     #'codigo/jsons/asignaturasNel.json'
#     ) as json_file:
#     datos = json.load(json_file)

def generate_graph_pdf(json_data):
    
    datos = json_data
    asignaturas = datos["asignaturas"]
    asignaturas.sort(key= lambda asig: (
                                        asig['semestre'] if asig['semestre'] != None else float('inf'),
                                        asig['tipologia'][9:], #Para que quede ordenado Fundamentación -> Disciplinar -> Libre
                                        asig['codigo']
                                        #-len(asig['prerrequisitos']) if asig['prerrequisitos'] != None else 0 
                                        ))

    # Definimos los esquemas de colores
    colores_por_tipologia = {
        # Morado para Fundamentación
        'fundamentacion_optativa': "#b094c4", 
        'fundamentacion_obligatoria': "#b094c4",
        # Verde para disciplinares
        'disciplinar_obligatoria': "#12a79d",
        'disciplinar_optativa': "#12a79d",  
        # Amarillo para libre elección
        'libre_eleccion': "#fdbe26", 
        # Gris para nivelación
        'nivelacion': "#808285", 
    }


    # Inicializando el grafo
    plan_estudios = Digraph(name='plan_estudios',
                            comment='Historia academica',
                            filename='plan_estudios',
                            format='pdf',
                            graph_attr={'compound':'true', 
                                        'splines':'ortho'
                                        })

    #Encontramos el último semestre cursado por el alumno y si al menos hay una materia en curso
    #para saber si usuario está estudiando en el momento

    max_sem = 0
    en_curso = False
    max_asignaturas_por_semestre = 0
    num_asignaturas_por_semestre = dict()

    #diccionario para llevar control de las materias que se repiten
    dict_materias_cursadas = dict()
    creditos_opt_fund = int(datos["creditos_opt_fund"])
    creditos_opt_disc = int(datos["creditos_opt_disc"])
    cont_creditos_opt_fund = 0
    cont_creditos_opt_disc = 0
    

    #wrapper para label de los nodos asignaturas
    wrapper = textwrap.TextWrapper(width = 25)


    for asignatura in asignaturas:
        semestre_asignatura = asignatura['semestre'] if asignatura['semestre'] != None else -float('inf')
        #max_sem es el último semestre cursado
        if semestre_asignatura > max_sem:
            max_sem = semestre_asignatura
        #si por lo menos una materia es "inscrita", luego hay un semestre en curso
        if asignatura['estado'] == 'inscrita':
            en_curso = True
        #se hace el control de las materias que se han aprobado, perdido o no cursado
        dict_materias_cursadas[asignatura["codigo"]] = "no_cursada"

        #para cada semestre se hace el conteo de los creditos optativos
        #para saber si se deben mostrar entre las materias cursables
        if asignatura['tipologia'] == 'disciplinar_optativa' and asignatura['estado'] == 'aprobada':
            cont_creditos_opt_disc += int(asignatura['creditos'])

        if asignatura['tipologia'] == 'fundamentacion_optativa' and asignatura['estado'] == 'aprobada':
            cont_creditos_opt_fund += int(asignatura['creditos'])
        
        #conteo de asignaturas por cada semestre
        if asignatura['semestre']:
            if asignatura['semestre'] not in num_asignaturas_por_semestre:
                num_asignaturas_por_semestre[asignatura['semestre']] = 1
            else:
                num_asignaturas_por_semestre[asignatura['semestre']] += 1
    
    #Se escoge el mayor numero de asignaturas en algun semestre
    max_asignaturas_por_semestre = max(num_asignaturas_por_semestre.values())


    #Se crea una lista para llevar control del PAPA. El primer valor
    #guardará el peso de la nota y la segunda los créditos
    PAPA = [0,0]
    #hablalomiPA
    hablalomiPA = dict()
    # Agregamos un nodo por cada asignatura
    for i in range(1,max_sem+1):
        contador_asignaturas_creadas_por_semestre = 0

        with plan_estudios.subgraph(name=f'cluster_{i}',
                                    graph_attr={'margin':'25','nodesep':'0.02'}) as sem:

            label_semestre = f'Semestre {i}'

            #en caso de que el semestre sea el último y se esté cursando es el Actual
            if i == max_sem and en_curso:
                label_semestre += ' (Actual)'

            sem.attr(label=label_semestre,
                    fontname="Arial",
                    style='filled',
                    fillcolor='lightGray',
                    color='darkgray',
            )

            
            #Nodo para hacer invisible
            sem.node(name=f'sem_{i}',
                    width='0.02',
                    height='0.02',
                    style='invis')
            
            
            sem.node_attr['style'] = 'rounded,filled'
            sem.node_attr['shape'] = 'box'
            # sem.node_attr['fixedsize'] = 'true'
            sem.node_attr['width'] = '3'
            
            asignatura_prev = f'sem_{i}'
            asignatura_por_semestre = list()

            #Se añaden las asignaturas, controlando su estado y poniéndoles sus datos según corresponda
            for asignatura in asignaturas:
                if asignatura['semestre'] == i:
                    asignatura_por_semestre.append(asignatura)
                    

                    if asignatura['estado'] == 'cancelada':
                        identificador = f'{asignatura["codigo"]}_c{i}'
                        color = '#e36414'
                        nota = 'CANCELADA'
                        penwidth = '2'

                    elif asignatura['estado'] == 'no_aprobada':
                        identificador = f'{asignatura["codigo"]}_na{i}'
                        color = '#ff0000'
                        nota = asignatura['nota'] if asignatura['nota'] != None else 'NO APROBADA'
                        penwidth = '2'
                        dict_materias_cursadas[asignatura["codigo"]] = "no_aprobada" 

                    elif asignatura['estado'] == 'aprobada':
                        identificador = asignatura["codigo"]
                        color = '#000000'
                        nota = asignatura['nota'] if asignatura['nota'] != None else 'APROBADA'
                        penwidth = '1'
                        dict_materias_cursadas[asignatura["codigo"]] = "aprobada"
                    
                    else:
                        identificador = asignatura["codigo"]
                        color = '#000000'
                        nota = 'INSCRITA'
                        penwidth = '1'
                        dict_materias_cursadas[asignatura["codigo"]] = "aprobada"


                    #Primero wrapeamos el texto del nombre

                    nombre = asignatura["nombre"]
                    wrap_list = wrapper.wrap(text=nombre)
                    nombre_wrappeado = "\n".join(wrap_list)

                    #Se crea la label de cada asignatura
                    node_label = '{}\n{}\n{} créditos\n{}'.format(
                                                                asignatura["codigo"],
                                                                nombre_wrappeado,
                                                                asignatura["creditos"],
                                                                nota
                                                                )

                    # Se crea el nodo de cada asignatura dentro de su respectivo cluster (semestre)
                    sem.node(name=identificador, 
                            label=node_label,
                            color=color, 
                            fillcolor=colores_por_tipologia[asignatura["tipologia"]],
                            group=f'sem{i}',
                            penwidth=penwidth
                            )
                    
                    contador_asignaturas_creadas_por_semestre +=1
                
                    #Edges invisibles para las materias queden unas debajo de otras
                    sem.edge(tail_name=asignatura_prev, 
                            head_name=identificador, 
                            style='invis')
                
                     #Se asigna la asignatura previa.
                    asignatura_prev = identificador

                    #Si contador por semestre es llega al numero de asignaturas por semestre y
                    #si el numero de asignaturas por semestre es menor que el max de asignaturas en
                    #cualquier semestre.
                    if contador_asignaturas_creadas_por_semestre == num_asignaturas_por_semestre[i] \
                    and num_asignaturas_por_semestre[i] < max_asignaturas_por_semestre:
                        
                        #Diferencia entre asignaturas semestre actual y max asignaturas en algun semestre. 
                        nodos_faltantes = max_asignaturas_por_semestre - num_asignaturas_por_semestre[i]
                        
                        for k in range(nodos_faltantes):
                            identificador = f'relleno_{i}_{k}'

                            #Nodos relleno invisibles
                            sem.node(name=identificador,
                                    group=f'sem{i}',
                                    style='invis'
                                    )
                            
                            #flechas relleno invisibles
                            sem.edge(tail_name=asignatura_prev, 
                                    head_name=identificador,
                                    style='invis'
                                    )
                            
                            #Se vuelve a asignar la asignatura previa.
                            asignatura_prev = identificador
            
            

            #Se crea una lista para llevar control del PAPPI. El primer valor
            #guardará el peso de la nota y la segunda los créditos
            PAPPI = [0,0]
    
            for asignatura in asignatura_por_semestre:
                # Se revisa que la materia afecte el promedio o si fue cancelada
                if asignatura["nota"] != None or asignatura["estado"] == 'cancelada':
                    #Si se está calculando el PAPPI, se deben de tener en cuenta los créditos cancelados
                    if asignatura["estado"] == 'cancelada':
                        PAPPI[1] += asignatura["creditos"]
                    else:
                        # Se suma el peso ponderado de la nota de la materia y los créditos en su respectiva lista
                        PAPPI[0] += asignatura["nota"] * asignatura["creditos"]
                        PAPPI[1] += asignatura["creditos"]
                        PAPA[0] += asignatura["nota"] * asignatura["creditos"]
                        PAPA[1] += asignatura["creditos"]
                        hablalomiPA[asignatura['codigo']] = (asignatura["nota"], asignatura['creditos'])


            #Chequeamos que el semestre no esté en curso para mostrar los promedios
            if ((not en_curso) or (max_sem != i)):
                credPA = 0
                notPA = 0
                #Guardamos en las variables el total peso de las materias y el número de créditos
                for llave in hablalomiPA.keys():
                    notPA += hablalomiPA[llave][0]*hablalomiPA[llave][1]
                    credPA += hablalomiPA[llave][1]
                PA = None
                if credPA!=0:
                    PA = round(notPA / credPA,1)
                #Calculamos el PAPA que es el peso ponderado de TODAS las materias divido el número de créditos
                PAPA_semestre = round(PAPA[0]/PAPA[1],1)
                PAPPI = round(PAPPI[0]/PAPPI[1],1) 
                #mostramos los 3 valores en un struct
                node_label=f"PAPA {PAPA_semestre}|PAPPI {PAPPI}|PA {PA}"
                    
                sem.node(name=f'Promedio {i}',
                        shape='record',
                        label=node_label, 
                        fillcolor='#EBEBEB'
                        )

                sem.edge(asignatura_prev, f'Promedio {i}', style='invis')

            else:
                #si el semestre está en curso, no tiene promedios aún.
                node_label=f"Semestre en curso"
                sem.node(name=f'Promedio {i}',
                        shape='record',
                        label=node_label, 
                        fillcolor='#EBEBEB'
                        )

            sem.edge(asignatura_prev, f'Promedio {i}', style='invis')

            
    # Agregamos las flechas de prerequisitos
    for asignatura in asignaturas:
        if asignatura["prerrequisitos"] and (asignatura['estado'] == 'aprobada'or asignatura['estado'] == 'inscrita'):
            for prereq in asignatura["prerrequisitos"]:
                plan_estudios.edge(prereq,
                        asignatura["codigo"],
                        constraint='false')


    for j in range(1,max_sem+1):
        plan_estudios.edge('start', f'sem_{j}', lhead=f'cluster_{j}',style='invis')
    plan_estudios.node('start',shape='Mdiamond', style='invis')



    # Render the graph to a file
    plan_estudios.render(directory='output')
    #'asignatur_catalog/Digraph.gv.pdf'

            


            
            
 #------------------------------------PDF2----------------------------------------------#





    # Inicializando el grafo
    asignaturas_cursables = Digraph(name='asignaturas_cursables',
                                    comment='asignaturas cursables',
                                    filename='pendientes',
                                    format='pdf',
                                    graph_attr={'compound':'true'}
                                    )

    #lista mñaterias que se deben mostrar en el segundo pdf
    lista_codigos_por_cursar = list()
    with asignaturas_cursables.subgraph(name=f'cluster_cursables',
                                        graph_attr={'margin':'25','nodesep':'0.02'}) as cluster_cursables:
        
        cluster_cursables.attr(label='Asignaturas cursables el próximo semestre',
                               fontname="Arial",
                               style='filled',
                               fillcolor='lightGray',
                               color='darkgray',
            )
        
        cluster_cursables.node_attr['style'] = 'rounded,filled'
        cluster_cursables.node_attr['shape'] = 'box'
        cluster_cursables.node_attr['width'] = '3'

        grupo_linea = 0
        contador_asignaturas_linea = 0

        for asignatura in asignaturas:

            if dict_materias_cursadas[asignatura['codigo']] != 'aprobada' \
            and asignatura['codigo'] not in lista_codigos_por_cursar:
                
                lista_codigos_por_cursar.append(asignatura['codigo'])
                prerrequisitos_cumplidos = True
                
                

                # Check para comprobar que todos los prerrequisitos estén aprobados
                if asignatura['prerrequisitos'] != None:
                    for cod in asignatura['prerrequisitos']:
                        if dict_materias_cursadas[cod] != 'aprobada':
                            prerrequisitos_cumplidos = False
                            break
                
                #no se muestran las materias cuyos prerrequisitos no se hayan cursado
                #ni aquellas que son optativas y ya se han visto todos los créditos del componente
                if not prerrequisitos_cumplidos:
                    continue
                
                if asignatura['tipologia'] == 'fundamentacion_optativa' \
                    and cont_creditos_opt_fund >= creditos_opt_fund:
                    continue

                if asignatura['tipologia'] == 'disciplinar_optativa' \
                    and cont_creditos_opt_disc >= creditos_opt_disc:
                    continue
        
                wrap_list = wrapper.wrap(text=asignatura['nombre'])
                nombre_wrappeado = "\n".join(wrap_list)

                node_label = '{}\n{}\n{} créditos\n'.format(asignatura['codigo'],
                                                            nombre_wrappeado,
                                                            asignatura['creditos']
                                                        )


                # Se generan los nodos de las materias del segundo pdf
                cluster_cursables.node(name=asignatura['codigo'],
                                    label=node_label,
                                    color='#000000',
                                    group=f'Linea_{grupo_linea}',
                                    fillcolor=colores_por_tipologia[asignatura["tipologia"]],
                                    penwidth='1'
                                    )
                #se forman grupos de a 5 que se unen entre ellas para que queden
                #con una estructura interpretable.
                if contador_asignaturas_linea != 0:
                    cluster_cursables.edge(asignatura_anteriora, asignatura['codigo'], style='invis' )

                contador_asignaturas_linea += 1
                if contador_asignaturas_linea == 5:
                    grupo_linea += 1
                    contador_asignaturas_linea = 0
                
                asignatura_anteriora = asignatura['codigo']

        
    # Render the graph to a file
    return asignaturas_cursables.render(directory='output')
    #'asignatur_catalog/asignaturas_cursables.gv.pdf'       