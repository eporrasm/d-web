from graphviz import Digraph
import textwrap
import json

# Abriendo archivo json
with open('codigo/jsons/asignaturasEmilio.json') as json_file:
    datos = json.load(json_file)


asignaturas = datos["asignaturas"]


# Inicializando el grafo
dot = Digraph(comment='Historia academica', format='png',graph_attr={'compound':'true', 
                                                                     'splines':'ortho', 
                                                                     })


# Definimos los esquemas de colores
colores_por_tipologia = {
    # Rosado para Fundamentación
    'fundamentacion_optativa': "#FFC0CB", 
    'fundamentacion_obligatoria': "#FFC0CB",
    # Azul para disciplinares
    'disciplinar_obligatoria': "#87CEFA",
    'disciplinar_optativa': "#87CEFA",  
    # Verde para libre elección
    'libre_eleccion': "#98FB98", 
    # Gris para nivelación
    'nivelacion': "#EBEBEB", 
}

# Define the node styles
node_styles = {
    'aprobada': 'style="filled", fillcolor="#98FB98"',
    'cancelada': 'style="filled", fillcolor="#FFFFE0"',
    'no_aprobada': 'style="filled", fillcolor="#FFB6C1"'
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

    with dot.subgraph(name=f'cluster_{i}') as sem:

        sem.attr(fontname="Arial",
                 style='filled',
                 color='lightgrey'
        )

        sem.attr(label=f"Semestre {i}")
        
        
        sem.node_attr['style'] = 'filled'
        sem.node_attr['shape'] = 'box'
        # sem.node_attr['fixedsize'] = 'true'
        sem.node_attr['width'] = '3'

        #Nodo para hacer invisible
        sem.node(name=f'sem_{i}',label=f'sem_{i}',style='invis')
        
        asignatura_prev = f'sem_{i}'
        asignatura_por_semestre = list()


        for asignatura in asignaturas:
            if asignatura['semestre'] == i:
                asignatura_por_semestre.append(asignatura)

                

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
                                                              asignatura["nota"]
                                                              )
                
                # Se crea el nodo de cada asignatura dentro de su respectivo cluster (semestre)
                sem.node(name=asignatura["codigo"], 
                         label=node_label, 
                         fillcolor=colores_por_tipologia[asignatura["tipologia"]],
                         group = f'sem{i}'
                        )
                
                #Edges invisibles para las materias queden unas debajo de otras
                sem.edge(asignatura_prev, 
                         asignatura["codigo"], 
                         style='invis')
                
                asignatura_prev = asignatura["codigo"]
        
        

        #Se crea una lista para llevar control del PAPPI. El primer valor
        #guardará el peso de la nota y la segunda los créditos
        PAPPI = [0,0]
 
        for asignatura in asignatura_por_semestre:
            # Se revisa que la materia afecte el promedio o si fue cancelada
            if asignatura["afecta_promedio"] == "si" or asignatura["estado"] == 'cancelada':
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
    if asignatura["prerrequisitos"]:
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