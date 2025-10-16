import json

key = "123"

print("\n-------- BIENVENIDO-------- ")

def inicio_sesion():
    user = input("Ingrese su usuario: ")

    while True:
        password = input("Ingrese su contraseña: ")
        if password == key:
            print(f"Bienvenido, {user}")
            break
        else:
            input("Contraseña incorrecta. Por favor intente de nuevo.")

def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)
    

def obtener_preferencias(tipo):
    print("\n---------PREFERENCIAS---------")
    generos = input("¿Qué generos le interesan? (separados en comas): ").lower()
    generos = [g.strip().lower() for g in generos.split(",") if g.strip()]

    persona = input(f"¿Hay algún {'autor' if tipo=='libro' else 'director'} que te guste? (opcional): ").strip()
    persona = persona if persona else None

    print("A continuacion te preguntaremos por un periodo de tiempo especifico (opcional)")
    año_min = input("¿Desde qué año te interesa? (opcional): ").strip()
    año_max = input("¿Hasta qué año? (opcional): ").strip()
    
    año_min = int(año_min) if año_min.isdigit() else None
    año_max = int(año_max) if año_max.isdigit() else None

    return generos, persona, año_min, año_max

def recomendar(items, tipo, generos_pref, persona_pref, año_min, año_max):
    recomendaciones = []

    for item in items:
        puntuacion = 0

        generos_item = [gen.lower() for gen in item["genero"]]
        if any(g in generos_item for g in generos_pref):
            puntuacion += 2

        if persona_pref:
            if persona_pref.lower() in item["autor" if tipo=="libro" else "director"].lower():
                puntuacion += 2

        if año_min and item["año"] < año_min:
            continue
        if año_max and item["año"] > año_max:
            continue

        if puntuacion > 0:
            recomendaciones.append((item, puntuacion    ))

    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return recomendaciones

def mostrar_recomendaciones(recomendaciones, tipo):
    print("\n------ RECOMENDACIONES ------")
    if not recomendaciones:
        print(f"No se encontraron {tipo} que coincidan con tus preferencias.")
    else:
        max_titulo = max(len(item[0]['titulo']) for item in recomendaciones)
        max_autor_o_director = max(len(item[0]['autor']) if tipo == "libro" else len(item[0]['director']) for item in recomendaciones)
        max_genero = max(len(", ".join(item[0]['genero'])) for item in recomendaciones)
        max_año = max(len(str(item[0]['año'])) for item in recomendaciones)

        max_titulo += 5
        max_autor_o_director += 5
        max_genero += 5
        max_año += 5

        if tipo == "libro":
            print(f"{'NOMBRE':<{max_titulo}} | {'AUTOR':<{max_autor_o_director}} | {'GÉNERO':<{max_genero}} | {'AÑO':<{max_año}}")
        else:
            print(f"{'NOMBRE':<{max_titulo}} | {'DIRECTOR':<{max_autor_o_director}} | {'GÉNERO':<{max_genero}} | {'AÑO':<{max_año}}")
        print("-" * (max_titulo + max_autor_o_director + max_genero + max_año + 6))  

        for item in recomendaciones:
            if tipo == "libro":
                genero_str = ", ".join(item[0]["genero"]) if isinstance(item[0]["genero"], list) else item[0]["genero"]
                print(f"{item[0]['titulo']:<{max_titulo}} | {item[0]['autor']:<{max_autor_o_director}} | {genero_str:<{max_genero}} | {item[0]['año']:<{max_año}}")
            else:
                genero_str = item[0]['genero'] if isinstance(item[0]['genero'], str) else ", ".join(item[0]['genero'])
                print(f"{item[0]['titulo']:<{max_titulo}} | {item[0]['director']:<{max_autor_o_director}} | {genero_str:<{max_genero}} | {item[0]['año']:<{max_año}}")

def recomendaciones(tipo):
    archivo = "libros.json" if tipo=="libro" else "peliculas.json"
    items = cargar_datos(archivo)
    generos, persona, año_min, año_max = obtener_preferencias(tipo)
    recomendaciones = recomendar(items, tipo, generos, persona, año_min, año_max)
    mostrar_recomendaciones(recomendaciones, tipo)

def tipo():
    while True:
        eleccion = input("\n¿Qué recomendaciones desea? ¿Libro o Película? (escriba 'fin' para salir): ").lower().strip()
        if eleccion in ["libro","pelicula"]:
            recomendaciones(eleccion)
        elif eleccion == "fin":
            print("Gracias por usar el sistema. ¡Hasta luego!")
            break
        else:
            print("Entrada no válida. Por favor escriba 'libro', 'pelicula' o 'fin'.")

inicio_sesion()
tipo()