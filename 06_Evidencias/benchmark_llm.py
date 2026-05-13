import json
import time
from langchain_ollama import ChatOllama
from pydantic import ValidationError
import sys
import os

# Add the project directory to sys.path to import from agente_final
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from agente_final import DatosConvenio

def run_benchmark():
    with open('test_cases.json', 'r') as f:
        test_cases = json.load(f)

    models = ["granite4:micro-h", "ibm/granite4:350m-h"]
    results = {}

    for model in models:
        print(f"--- Benchmarking model: {model} ---")
        llm = ChatOllama(model=model)
        model_results = []
        
        for case in test_cases:
            print(f"  Testing case {case['id']}: {case['descripcion']}")
            start_time = time.time()
            
            prompt = f"""
            Extrae la información de los siguientes datos: {case['datos']}
            Esquema JSON solicitado:
            {{
                "nombre_representante_organizacion": "string|null",
                "cedula_representante_organizacion": "string|null",
                "cargo_representante_organizacion": "string|null",
                "nombre_organizacion": "string|null",
                "nit_organizacion": "string|null",
                "nombre_estudiante": "string|null",
                "cedula_estudiante": "string|null",
                "programa_estudiante": "string|null",
                "direccion_organizacion": "string|null",
                "actividades_lista": "string|null",
                "fecha_inicio": "string|null",
                "fecha_fin": "string|null"
            }}
            Si falta un dato, pon 'null'. No incluyas texto extra, solo el JSON.
            """
            
            try:
                response = llm.invoke(prompt)
                json_str = response.content.replace("```json", "").replace("```", "").strip()
                datos_json = json.loads(json_str)
                
                # Validate
                datos_validados = DatosConvenio.model_validate(datos_json)
                success = True
                error = None
            except Exception as e:
                success = False
                error = str(e)
            
            end_time = time.time()
            latency = end_time - start_time
            
            model_results.append({
                "case_id": case['id'],
                "success": success,
                "latency": latency,
                "error": error
            })
            
        results[model] = model_results
        
    # Generate report
    with open('reporte_bench.md', 'w') as f:
        f.write("# Reporte de Benchmarking LLM\n\n")
        for model, res in results.items():
            f.write(f"## Modelo: {model}\n")
            successes = sum(1 for r in res if r['success'])
            avg_latency = sum(r['latency'] for r in res) / len(res)
            f.write(f"- Éxitos: {successes}/{len(res)}\n")
            f.write(f"- Latencia promedio: {avg_latency:.2f}s\n\n")

    print("Benchmark completo. Ver 'reporte_bench.md'.")

if __name__ == "__main__":
    run_benchmark()
