from flask import Flask, render_template, request, jsonify, send_file, session
from flask_bootstrap import Bootstrap
from graph_generator_app import generate_graph_pdf
import os.path

from time import sleep

app = Flask(__name__)
Bootstrap(app)

@app.route('/')
def index():
    if os.path.exists("output/plan_estudios.pdf"):
            os.remove("output/plan_estudios.pdf")

    if os.path.exists("output/pendientes.pdf"):
        os.remove("output/pendientes.pdf")
    return render_template('index.html')

@app.route('/api', methods=['POST'])
def api():
    if request.method == 'POST':
        json_input = request.get_json(silent=True)
        #print(json_input)
        if os.path.exists("output/plan_estudios.pdf"):
            os.remove("output/plan_estudios.pdf")

        if os.path.exists("output/pendientes.pdf"):
            os.remove("output/pendientes.pdf")

        pdf_file_path = generate_graph_pdf(json_input)
        # Renderizar una plantilla HTML que muestra un botón para descargar el PDF
        return jsonify(json_input)

@app.route('/output1', methods=['GET'])
def output1():
    if request.method == 'GET':

        while True:
            sleep(0.5)
            if os.path.exists("output/plan_estudios.pdf"):
                break
            

        return send_file('output/plan_estudios.pdf')

@app.route('/output2', methods=['GET'])
def output2():
    if request.method == 'GET':
        
        while True:
            sleep(0.5)
            if os.path.exists("output/pendientes.pdf"):
                break
            

        return send_file('output/pendientes.pdf')

if __name__ == '__main__':
    app.run(port=5000)