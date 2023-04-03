from graphviz import Digraph
import textwrap
import json

# Abriendo archivo json
with open(
    'codigo/jsons/asignaturasEmilio.json'
    #'codigo/jsons/asignaturasNel.json'
    ) as json_file:
    datos = json.load(json_file)


asignaturas = datos["asignaturas"]
asignaturas.sort(key= lambda asig: (
                                    #-len(asig['prerrequisitos']) if asig['prerrequisitos'] != None else 0, 
                                    asig['semestre'] ))


# Inicializando el grafo
dot = Digraph(comment='Historia academica', format='png',graph_attr={'compound':'true', 
                                                                     'splines':'ortho',
                                                                     })


# Definimos los esquemas de colores
colores_por_tipologia = {
    # Morado para Fundamentación
    'fundamentacion_optativa': "#9f86c0", 
    'fundamentacion_obligatoria': "#9f86c0",
    # Verde para disciplinares
    'disciplinar_obligatoria': "#52b788",
    'disciplinar_optativa': "#52b788",  
    # Amarillo para libre elección
    'libre_eleccion': "#ffca3a", 
    # Gris para nivelación
    'nivelacion': "#EBEBEB", 
}

#Encontramos el último semestre cursado por el alumno

maxsem = 0


for asignatura in asignaturas:
     if asignatura['semestre'] > maxsem:
         maxsem = asignatura['semestre']


#Se crea una lista para llevar control del PAPA. El primer valor
#guardará el peso de la nota y la segunda los créditos
PAPA = [0,0]
# Agregamos un nodo por cada asignatura
for i in range(1,maxsem+1):

    with dot.subgraph(name=f'cluster_{i}',
                      graph_attr={'margin':'25','nodesep':'0.02'}) as sem:

        sem.attr(fontname="Arial",
                 style='filled',
                 fillcolor='lightGray',
                 color='darkgray'
        )

        sem.attr(label=f"Semestre {i}")

        #Nodo para hacer invisible
        dot.node(name=f'sem_{i}',
                width='0.02',
                height='0.02',
                style='invis')
        
        
        sem.node_attr['style'] = 'filled'
        sem.node_attr['shape'] = 'box'
        # sem.node_attr['fixedsize'] = 'true'
        sem.node_attr['width'] = '3'
        
        asignatura_prev = f'sem_{i}'
        asignatura_por_semestre = list()


        for asignatura in asignaturas:
            if asignatura['semestre'] == i:
                asignatura_por_semestre.append(asignatura)
                

                if asignatura['estado'] == 'cancelada':
                    identificador = f'{asignatura["codigo"]}_c{i}'
                    color = '#e36414'
                    nota = "CANCELADA"
                    penwidth = '2'

                elif asignatura['estado'] == 'no_aprobada':
                    identificador = f'{asignatura["codigo"]}_na{i}'
                    color = '#ff0000'
                    nota = asignatura['nota'] if asignatura['nota'] != None else "NO APROBADA"
                    penwidth = '2'

                else:
                    identificador = asignatura["codigo"]
                    color = '#000000'
                    nota = asignatura['nota'] if asignatura['nota'] != None else "APROBADA"
                    penwidth = '1'


                #Primero wrapeamos el texto del nombre

                nombre = asignatura["nombre"]
                wrapper = textwrap.TextWrapper(width = 25)
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
                        group = f'sem{i}',
                        penwidth=penwidth
                    )
            
                #Edges invisibles para las materias queden unas debajo de otras
                sem.edge(tail_name=asignatura_prev, 
                        head_name=identificador, 
                        style='invis')
            
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
         
        PA = 5
        PAPA_semestre = round(PAPA[0]/PAPA[1],1)
        PAPPI = round(PAPPI[0]/PAPPI[1],1)
        node_label=f"PAPA {PAPA_semestre}|PA {PA}|PAPPI {PAPPI}"
            
        sem.node(name=f'Promedio {i}',
        shape='record',
        label=node_label, 
        fillcolor='#EBEBEB'
        )

        sem.edge(asignatura_prev, f'Promedio {i}', style='invis')

        
# Agregamos las flechas de prerequisitos
for asignatura in asignaturas:
    if asignatura["prerrequisitos"] and asignatura['estado'] == 'aprobada':
        for prereq in asignatura["prerrequisitos"]:
            dot.edge(prereq,
                    asignatura["codigo"],
                    constraint='false')

    
for j in range(1,maxsem+1):
     dot.edge('start', f'sem_{j}', lhead=f'cluster_{j}',style='invis')

dot.node('start',shape='Mdiamond', style='invis')


# Render the graph to a file
dot.render(directory='codigo/asignatura_catalog', view=True)
#'doctest-output/round-table.gv.pdf'