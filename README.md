# 🤖 AI-Powered Code Refactor Tool

Este es un script de Python que utiliza la **API de Gemini de Google** para refactorizar automáticamente archivos de código fuente en un directorio específico. El script está diseñado para aplicar un conjunto de reglas de estilo y formato muy estrictas, ideal para estandarizar bases de código, especialmente en lenguajes como C.



## 📜 Descripción

El programa recorre de forma recursiva un directorio, busca archivos con una extensión determinada (por ejemplo, `.c`) y, para cada uno, envía su contenido a la API de Gemini con un *prompt* detallado que contiene 30 reglas de formato y estilo.

Posteriormente, recibe el código refactorizado y lo utiliza para sobrescribir el archivo original, guardando únicamente si se detectan cambios.

---

## ✨ Características Principales

-   **Refactorización Automática**: Utiliza el modelo `gemini-1.5-flash` para reescribir el código.
-   **Reglas Estrictas**: Aplica un conjunto de 30 reglas predefinidas que cubren indentación, longitud de líneas, espaciado, estilo de comentarios y más.
-   **Personalizable**: Puedes ajustar el directorio de destino, la extensión de los archivos y añadir un *prompt* adicional para dar énfasis a ciertas reglas.
-   **Procesamiento por Lotes**: Recorre y procesa automáticamente todos los archivos de un directorio y sus subcarpetas.
-   **Seguridad**: Requiere una clave de API de Gemini configurada como variable de entorno para funcionar.

---

## 🛠️ Requisitos

Antes de ejecutar el script, asegúrate de tener lo siguiente:

1.  **Python 3.6+** instalado.
2.  La biblioteca de `google-generativeai`.
3.  Una **clave de API de Gemini**. Puedes obtenerla en [Google AI Studio](https://aistudio.google.com/app/apikey).

---

## 🚀 Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-DE-TU-REPOSITORIO>
    cd <NOMBRE-DEL-REPOSITORIO>
    ```

2.  **Instala las dependencias necesarias:**
    ```bash
    pip install google-generativeai
    ```

3.  **Configura tu clave de API:**
    Debes establecer tu clave de API de Gemini como una variable de entorno.

    -   En **Linux/macOS**:
        ```bash
        export GEMINI_API_KEY='TU_API_KEY_AQUI'
        ```
    -   En **Windows (CMD)**:
        ```bash
        set GEMINI_API_KEY=TU_API_KEY_AQUI
        ```
    -   En **Windows (PowerShell)**:
        ```powershell
        $env:GEMINI_API_KEY="TU_API_KEY_AQUI"
        ```

    > ⚠️ **Importante**: No escribas tu clave de API directamente en el código. Usar variables de entorno es una práctica de seguridad recomendada.

---

## ⚙️ Uso y Configuración

Toda la configuración se encuentra en el bloque `if __name__ == "__main__":` al final del script.

```python
if __name__ == "__main__":
    # 1. Directorio donde se encuentran los archivos a refactorizar.
    TARGET_DIRECTORY = "./refactorizar"

    # 2. Extensión de los archivos que quieres procesar (sin el punto).
    FILE_EXTENSION = "c"

    # 3. Prompt adicional para dar énfasis a ciertas reglas.
    REFACTOR_PROMPT = (
        "Enfócate estrictamente en las reglas de las llaves, la indentación por tabulación "
        "y la longitud máxima de 25 líneas por función. Asegúrate de que el retorno esté entre paréntesis."
    )

    # ... el resto del código de ejecución
```

1.  **`TARGET_DIRECTORY`**: Modifica esta variable con la ruta al directorio que contiene los archivos que deseas refactorizar.
2.  **`FILE_EXTENSION`**: Especifica la extensión de los archivos a procesar (ej. `"c"`, `"cpp"`, `"java"`).
3.  **`REFACTOR_PROMPT`**: Añade aquí instrucciones adicionales o resalta las reglas más importantes que quieres que el modelo tenga en cuenta con mayor prioridad.

Una vez configurado, simplemente ejecuta el script desde tu terminal:

```bash
python nombre_del_script.py
