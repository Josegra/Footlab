import pandas as pd
import re
import os
import unidecode

# Lista de enlaces de salarios
links = [
    'https://fbref.com/en/comps/20/wages/Bundesliga-Wages',
    'https://fbref.com/en/comps/9/wages/Premier-League-Wages',
    'https://fbref.com/en/comps/12/wages/La-Liga-Wages',
    'https://fbref.com/en/comps/13/wages/Ligue-1-Wages',
    'https://fbref.com/en/comps/11/wages/Serie-A-Wages'
]

def extract_euro_value(val):
    """Extrae el valor numérico en euros desde una cadena con formato '€ 123,456 (x)'."""
    if isinstance(val, str):
        match = re.search(r'€\s?([\d,]+)', val)
        if match:
            return int(match.group(1).replace(',', ''))
    return None

def process_wage_table(url):
    """Lee y limpia la tabla de salarios desde un enlace de FBref."""
    try:
        df = pd.read_html(url)[1]
        df['Weekly Wages'] = df['Weekly Wages'].apply(extract_euro_value)
        df['Annual Wages'] = df['Annual Wages'].apply(extract_euro_value)

        if 'Player' in df.columns:
            df['Player'] = df['Player'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)
        if 'Squad' in df.columns:
            df['Squad'] = df['Squad'].apply(lambda x: unidecode.unidecode(str(x)) if pd.notnull(x) else x)

        if 'Player' in df.columns and 'Squad' in df.columns:
            df['PlSqu'] = df['Player'].astype(str) + df['Squad'].astype(str)

        return df
    except Exception as e:
        print(f"Error procesando {url}: {e}")
        return None

# Procesamos todos los enlaces y descartamos resultados vacíos
dfs = [process_wage_table(url) for url in links]
dfs = [df for df in dfs if df is not None and not df.empty]



# Si hay datos válidos, los procesamos y guardamos
if dfs:
    df_final = pd.concat(dfs, ignore_index=True)
    nombres_fbref = [
        "Illia Zabarnyi", "Javier Guerra", "Alvaro Garcia", "Nicolas Paz", "Sergi Cardona",
        "Valentin Atangana Edoa", "Yehor Yarmoliuk", "Alexsandro Ribeiro", "Victor Bernth Kristiansen",
        "Dailon Livramento", "Pierre Ekwah Elimby", "Manuel Ugarte Ribeiro", "Johnny Cardoso",
        "Manuel Fuster", "Jon Rowe", "Francisco Perez", "Antoniu", "Peque", "Jean Matteo Bahoya",
        "Orri Steinn Oskarsson", "Hong Hyunseok", "Alejandro Jimenez", "Ngal'Ayel Mukau",
        "Abdoulaye Niakhate Ndiaye", "Lucas Oliveira Rosa", "Juan Herzog", "Keke Maximilian Topp",
        "Jesus Santiago", "Bahereba Guirassy", "Peter Gonzalez", "Urko Gonzalez", "Guimissongui Ouattara",
        "Carlos Gomez", "Alvaro djalo", "Mohamed Haj", "James Mcatee", "Giorgos Masouras",
        "Giorgi Mamardashvili"
    ]
    
    # Nombres con errores (Salarios)
    nombres_salarios = [
        "Ilya Zabarnyi", "Javi Guerra", "Alvaro Garcia", "Nico Paz", "Sergi Cardona",
        "Valentin Atangana", "Yegor Yarmolyuk", "Alexsandro", "Victor Kristiansen",
        "Dailon Rocha Livramento", "Pierre Ekwah", "Manuel Ugarte", "Johnny",
        "Manu Fuster", "Jonathan Rowe", "Fran Perez", "Antoniu Roca", "Peque Fernandez",
        "Jean-Matteo Bahoya", "Orri Oskarsson", "Hyun-seok Hong", "Alex Jimenez", "Ngal'ayel Mukau",
        "Abdoulaye Ndiaye", "Lucas Rosa", "Juanma Herzog", "Keke Topp", "Yellu Santiago",
        "Herba Guirassy", "Peter Federico", "Urko Gonzalez de Zarate", "Abdoul Ouattara",
        "Carlos Andres Gomez", "Alvaro Djalo", "Anas Haj Mohamed", "James McAtee", "Georgios Masouras",
        "Giorgi Mamardashvili"
    ]
    
    # Creamos diccionario de reemplazo
    dicc_reemplazo_nombres = dict(zip(nombres_salarios, nombres_fbref))
    # Reemplazar los nombres en la columna 'Jugador'
    df_final['Player'] = df_final['Player'].replace(dicc_reemplazo_nombres)
    # Ruta de salida
    output_dir = './data'
    output_filename = 'salaries_big5.csv'
    output_path = os.path.join(output_dir, output_filename)

    # Crear el directorio si no existe
    os.makedirs(output_dir, exist_ok=True)

    # Eliminar el archivo si ya existe
    if os.path.exists(output_path):
        os.remove(output_path)

    # Guardar CSV
    df_final.to_csv(output_path, index=False)
    print(f"\n¡Proceso completado! Archivo guardado en: {output_path}")
else:
    print("\nNo se pudo procesar ningún dato.")
