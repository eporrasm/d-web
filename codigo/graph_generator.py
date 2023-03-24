from graphviz import Digraph
import json
# Opening JSON file
with open('codigo/asignaturasEmilio.json') as json_file:
    data = json.load(json_file)


asignaturas = data["asignaturas"]
#print(asignaturas)


# Initialize the graph
dot = Digraph(comment='Course Catalog', format='png',graph_attr={'compound':'true'})

# Define the color schemes
color_map = {
    'fundamentacion_optativa': "#FFC0CB",  # Pink for Teóricas
    'fundamentacion_obligatoria': "#FFC0CB",
    'disciplinar_obligatoria': "#87CEFA",
    'disciplinar_optativa': "#87CEFA",  # Blue for Prácticas
    'libre_eleccion': "#98FB98", 
    'nivelacion': "#EBEBEB", # Green for Laboratorios
}

# Define the node styles
node_styles = {
    'aprobada': 'style="filled", fillcolor="#98FB98"',
    'cancelada': 'style="filled", fillcolor="#FFFFE0"',
    'no_aprobada': 'style="filled", fillcolor="#FFB6C1"'
}

courses = asignaturas

# Add nodes for each course
maxsem = 0
for course in courses:
     if course['semestre'] > maxsem:
         maxsem = course['semestre']

#dot.node('start',shape='Mdiamond')

for i in range(1,maxsem+1):

    with dot.subgraph(name=f'cluster_{i}') as sem:

        sem.attr(style='filled', color='lightgrey', rank='same')
        sem.attr(label=f"Semestre {i}")

        sem.node_attr['style'] = 'filled'
        sem.node_attr['shape'] = 'box'
        
        for course in courses:
            if course['semestre'] == i:

                node_label = '{}\n{}\n{} créditos\n{}'.format(
                                                              course["codigo"],
                                                              course["nombre"],
                                                              course["creditos"],
                                                              course["nota"]
                                                              )
                    
                sem.node(name=course["codigo"], 
                         label=node_label, 
                         fillcolor=color_map[course["tipologia"]]
                        )

# Add edges for prerequisite courses
for course in courses:
    if course["prerrequisitos"]:
        for prereq in course["prerrequisitos"]:
            dot.edge(prereq, course["codigo"], arrowhead='vee')

# for j in range(1,maxsem+1):
#     dot.edge('start', f'cluster_{j}', lhead=f'cluster_{j}')

# Render the graph to a file
dot.render(directory='codigo/course_catalog', view=True)
#'doctest-output/round-table.gv.pdf'