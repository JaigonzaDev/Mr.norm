import os
from pathlib import Path
from google import genai
from google.genai.errors import APIError


def refactor_file_content(file_path: Path, prompt: str) -> str:
    """
    Lee el contenido del archivo, llama a la API de Gemini para editarlo,
    y devuelve el contenido editado.
    """
    print(f"  -> Procesando archivo: {file_path.name}")
    
    try:
        content = file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"  ❌ ERROR al leer {file_path.name}: {e}")
        return None

    system_instruction = (
        "ERES UN REFORMATEADOR DE CÓDIGO EXTREMADAMENTE ESTRICTO. Tu tarea es reescribir "
        "el código fuente proporcionado para que cumpla "
        "con *todas y cada una* de las siguientes reglas de formato y estilo, que son obligatorias.\n"
        
        "REGLAS DE FORMATO Y ESTILO (OBLIGATORIAS):\n"
        "1. Indentación: Tabulaciones de 4 espacios (el carácter TAB, no 4 espacios).\n"
        "2. Longitud de Función: Máximo 25 líneas por función (excluyendo llaves).\n"
        "3. Ancho de Línea: Máximo 80 columnas (incluyendo comentarios). Advertencia: una tabulación no cuenta como una columna.\n"
        "4. Separación de Funciones: Una línea vacía entre funciones. Comentarios/instrucciones de preprocesador pueden ir justo encima.\n"
        "5. Instrucciones: Una instrucción por línea.\n"
        "6. Líneas Vacías: Deben estar vacías (sin espacios/tabulaciones).\n"
        "7. Espacios Finales: Una línea no puede terminar con espacios o tabulaciones.\n"
        "8. Espacios Consecutivos: No se permiten dos espacios consecutivos.\n"
        "9. Línea Nueva con Llaves: Comenzar una nueva línea después de cada llave de apertura '{' o cierre '}' o después de una estructura de control.\n"
        "10. Comas/Punto y Coma: Cada ',' o ';' debe ser seguido por un espacio, salvo que sea el final de una línea.\n"
        "11. Operadores/Operandos: Cada operador u operando debe estar separado por un (y solo un) espacio.\n"
        "12. Palabras Clave de C: Cada palabra clave de C debe ir seguida de un espacio, excepto tipos (`int`, `char`, etc.) y `sizeof`.\n"
        "13. Declaración de Variables: Indentada en la misma columna dentro de su scope.\n"
        "14. Punteros: Asteriscos '*' pegados a los nombres de las variables.\n"
        "15. Una Declaración por Línea: Una sola declaración de variable por línea.\n"
        "16. Inicialización: Declaración e inicialización no pueden estar en la misma línea (excepto globales/estáticas/constantes).\n"
        "17. Ubicación de Declaraciones: Al principio de una función.\n"
        "18. Línea Vacía en Función: Una línea vacía entre declaraciones de variables y el resto de la función. No se permiten otras líneas vacías dentro de la función.\n"
        "19. Asignaciones Múltiples: Completamente prohibidas.\n"
        "20. Salto de Línea en Instrucción: Si se añade una línea nueva después de una instrucción, se debe agregar una indentación con llaves o un operador de asignación. Los operadores deben estar al principio de una línea.\n"
        "21. Estructuras de Control: Deben tener llaves, salvo que contengan una sola línea.\n"
        "22. Llaves de Función/Estructura: Las llaves que siguen a funciones, declaradores o estructuras de control deben estar **precedidas y seguidas por una nueva línea**.\n"
        
        "REGLAS DE FUNCIONES Y COMENTARIOS:\n"
        "23. Parámetros: Máximo 4 parámetros por función.\n"
        "24. Funciones sin Argumentos: Prototipadas con la palabra 'void' como argumento.\n"
        "25. Nombres de Parámetros: Los parámetros en los prototipos deben tener nombre.\n"
        "26. Declaración de Variables: Máximo 5 variables por función.\n"
        "27. Retorno: El retorno de una función debe estar entre paréntesis.\n"
        "28. Separación de Tipo/Nombre: Una sola tabulación entre el tipo de retorno de la función y su nombre.\n"
        "29. Comentarios en Funciones: Los comentarios no son permitidos en el cuerpo de las funciones, solo en el encabezado antes de la propia funcion.\n"
        "30. Idioma de Comentarios: **Tus comentarios deben estar en inglés** y deben ser útiles.\n"
        
        "El código que devuelvas debe ser SOLAMENTE el código fuente completo y refactorizado. "
        "NO incluyas explicaciones, encabezados, comentarios o bloques de markdown (```).\n\n"
    )
    
    try:
        client = genai.Client()
        
        full_prompt = (
            system_instruction +
            f"REGLA ADICIONAL O ÉNFASIS: {prompt}\n\nAquí está el código fuente a refactorizar. Asegúrate de que **todos los comentarios estén en inglés** y que se utilice el **carácter de tabulación** para la indentación:\n\n{content}"
        )

        response = client.models.generate_content(
            model='gemini-2.5-flash', 
            contents=[
                full_prompt
            ]
        )
        
        edited_code = response.text.strip()
        if edited_code.startswith("```") and edited_code.endswith("```"):
            lines = edited_code.split('\n')
            if len(lines) > 2:
                edited_code = '\n'.join(lines[1:-1]).strip()
        
        return edited_code

    except APIError as e:
        print(f"  ❌ ERROR de API para {file_path.name}: {e}")
        return None
    except Exception as e:
        print(f"  ❌ ERROR inesperado para {file_path.name}: {e}")
        return None

# --------------------------------------------------------------------------------

def process_directory(directory_path: str, file_extension: str, refactor_prompt: str):
    """
    Recorre el directorio y aplica la refactorización a todos los archivos que coincidan con la extensión.
    """
    
    target_dir = Path(directory_path)
    if not target_dir.is_dir():
        print(f"❌ Error: La ruta '{directory_path}' no es un directorio válido.")
        return

    print(f"🚀 Iniciando refactorización en: {target_dir}")
    print(f"🔍 Buscando archivos con extensión: *.{file_extension}\n")
    
    for file_path in target_dir.rglob(f"*.{file_extension}"):
        
        if file_path.is_file():
            
            edited_content = refactor_file_content(file_path, refactor_prompt)
            
            if edited_content and edited_content != file_path.read_text(encoding='utf-8'):
                
                try:
                    file_path.write_text(edited_content, encoding='utf-8')
                    print(f"  ✅ Sobrescrito con éxito.")
                except Exception as e:
                    print(f"  ❌ ERROR al escribir en {file_path.name}: {e}")
            elif edited_content:
                print(f"  ℹ️ Sin cambios significativos detectados.")
            else:
                print(f"  ⚠️ Archivo omitido debido a un error de procesamiento.")
    
    print("\n🏁 Proceso de refactorización completado.")


# --------------------------------------------------------------------------------

# --- CONFIGURACIÓN PRINCIPAL ---
if __name__ == "__main__":
    
    TARGET_DIRECTORY = "./refactorizar" 
    FILE_EXTENSION = "c" 
    REFACTOR_PROMPT = (
        "Enfócate estrictamente en las reglas de las llaves, la indentación por tabulación "
        "y la longitud máxima de 25 líneas por función. Asegúrate de que el retorno esté entre paréntesis."
    )
    
    if 'GEMINI_API_KEY' not in os.environ:
        print("❌ Por favor, establece la variable de entorno GEMINI_API_KEY antes de ejecutar el script.")
    else:
        process_directory(TARGET_DIRECTORY, FILE_EXTENSION, REFACTOR_PROMPT)