from graphviz import Digraph
import json
# Opening JSON file
with open('codigo/asignaturasEmilio.json') as json_file:
    data = json.load(json_file)


asignaturas = data["asignaturas"]
#print(asignaturas)


# Initialize the graph
dot = Digraph(comment='Course Catalog', format='png',graph_attr={'rankdir':'LR'})

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
for course in courses:
    node_label = f'{course["codigo"]}\n{course["nombre"]}\n{course["creditos"]} créditos\n{course["nota"]}'
    node_shape = 'box'
    node_style = "filled"
    dot.node(course["codigo"], label=node_label, shape=node_shape, style=node_style, fillcolor=color_map[course["tipologia"]])

# Add edges for prerequisite courses
for course in courses:
    if course["prerrequisitos"]:
        for prereq in course["prerrequisitos"]:
            dot.edge(prereq, course["codigo"], arrowhead='vee')

# Add a label for each semester
for i in range(1, 11):
    dot.node(f'sem{i}', label=f'Semestre {i}', shape='plaintext')

# Add edges to group courses by semester
for course in courses:
    dot.edge(f'sem{course["semestre"]}', course["codigo"], style='invis')

# Render the graph to a file
dot.render(directory='codigo/course_catalog', view=True)
#'doctest-output/round-table.gv.pdf'



