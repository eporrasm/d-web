from flask import Flask, render_template, request, jsonify, send_file
from flask_bootstrap import Bootstrap
from graph_generator_app import generate_graph_pdf

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        json_input = request.get_json(silent=True)
        pdf_file_path = generate_graph_pdf(json_input)
        # Renderizar una plantilla HTML que muestra un botón para descargar el PDF
        #print(pdf_file_path)
        return json_input

@app.route('/output1', methods=['GET'])
def output1():
    if request.method == 'GET':
        return send_file('output/plan_estudios.pdf')

@app.route('/output2', methods=['GET'])
def output2():
    if request.method == 'GET':
        return send_file('output/pendientes.pdf')

if __name__ == '__main__':
    app.run(debug=True)