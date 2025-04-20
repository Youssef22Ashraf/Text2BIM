from flask import Flask, request, jsonify
from multi_agents_workflow import run_po_coder_agents, export_ifc_and_stuffs, run_agent_checking_loop
import os
import dotenv

app = Flask(__name__)

@app.route('/generate', methods=['POST'])
def generate_model():
    try:
        data = request.json
        prompt = data.get('prompt')
        
        # Run the main workflow
        result = run_po_coder_agents(prompt)
        
        # Export the IFC file
        export_path = export_ifc_and_stuffs()
        
        return jsonify({
            'status': 'success',
            'result': result,
            'export_path': export_path
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

@app.route('/check', methods=['POST'])
def check_model():
    try:
        data = request.json
        model_path = data.get('model_path')
        
        # Run the checking workflow
        result = run_agent_checking_loop(model_path)
        
        return jsonify({
            'status': 'success',
            'result': result
        })
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': str(e)
        }), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)