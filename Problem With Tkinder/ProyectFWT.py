import tkinter as tk
from tkinter import ttk, messagebox
import json

KEY = "123"

# Se carga el archivo (Libro o Pelicula)
def cargar_datos(nombre_archivo):
    with open(nombre_archivo, "r", encoding="utf-8") as archivo:
        return json.load(archivo)

def recomendar(items, tipo, generos_pref, persona_pref, año_min, año_max):
    recomendaciones = []

    for item in items:
        puntuacion = 0
        generos_item = [gen.lower() for gen in item["genero"]]

        if any(g in generos_item for g in generos_pref):
            puntuacion += 2

        if persona_pref:
            clave = "autor" if tipo == "libro" else "director"
            if persona_pref.lower() in item[clave].lower():
                puntuacion += 2

        if año_min and item["año"] < año_min:
            continue
        if año_max and item["año"] > año_max:
            continue

        if puntuacion > 0:
            recomendaciones.append((item, puntuacion))

    recomendaciones.sort(key=lambda x: x[1], reverse=True)
    return recomendaciones

# Interfaz 
class RecomendadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sistema de Recomendaciones")
        self.root.geometry("700x500")
        self.root.resizable(False, False)
        self.user = ""
        
        self.mostrar_login()

    # Pantalla de Login
    def mostrar_login(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="-------- BIENVENIDO --------", font=("Arial", 16, "bold")).pack(pady=10)
        ttk.Label(frame, text="Usuario:").pack()
        self.usuario_entry = ttk.Entry(frame, width=30)
        self.usuario_entry.pack(pady=5)

        ttk.Label(frame, text="Contraseña:").pack()
        self.password_entry = ttk.Entry(frame, width=30, show="*")
        self.password_entry.pack(pady=5)

        ttk.Button(frame, text="Iniciar sesión", command=self.verificar_login).pack(pady=15)

    def verificar_login(self):
        user = self.usuario_entry.get().strip()
        password = self.password_entry.get().strip()

        if password == KEY and user:
            self.user = user
            messagebox.showinfo("Éxito", f"Bienvenido, {self.user}")
            self.mostrar_tipo()
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Pantalla del Tipo (Libro o Pelicula)
    def mostrar_tipo(self):
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=30)
        frame.pack(expand=True)

        ttk.Label(frame, text="¿Qué recomendaciones desea?", font=("Arial", 14, "bold")).pack(pady=10)
        ttk.Button(frame, text="Libros", width=20, command=lambda: self.mostrar_preferencias("libro")).pack(pady=5)
        ttk.Button(frame, text="Películas", width=20, command=lambda: self.mostrar_preferencias("pelicula")).pack(pady=5)
        ttk.Button(frame, text="Salir", width=20, command=self.root.quit).pack(pady=15)

    # Pantalla de Formulario Preferencias
    def mostrar_preferencias(self, tipo):
        self.tipo_actual = tipo
        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=20)
        frame.pack(expand=True, fill="both")

        ttk.Label(frame, text=f"PREFERENCIAS DE {tipo.upper()}", font=("Arial", 14, "bold")).pack(pady=10)

        ttk.Label(frame, text="Géneros (separados por comas):").pack(anchor="w")
        self.generos_entry = ttk.Entry(frame, width=60)
        self.generos_entry.pack(pady=5)

        ttk.Label(frame, text=f"{'Autor' if tipo=='libro' else 'Director'} favorito (opcional):").pack(anchor="w")
        self.persona_entry = ttk.Entry(frame, width=60)
        self.persona_entry.pack(pady=5)

        ttk.Label(frame, text="Desde qué año (opcional):").pack(anchor="w")
        self.año_min_entry = ttk.Entry(frame, width=20)
        self.año_min_entry.pack(pady=5)

        ttk.Label(frame, text="Hasta qué año (opcional):").pack(anchor="w")
        self.año_max_entry = ttk.Entry(frame, width=20)
        self.año_max_entry.pack(pady=5)

        ttk.Button(frame, text="Mostrar recomendaciones", command=self.mostrar_resultados).pack(pady=15)
        ttk.Button(frame, text="Volver", command=self.mostrar_tipo).pack()

    # Presentación de resultados
    def mostrar_resultados(self):
        generos = [g.strip().lower() for g in self.generos_entry.get().split(",") if g.strip()]
        persona = self.persona_entry.get().strip() or None
        año_min = self.año_min_entry.get().strip()
        año_max = self.año_max_entry.get().strip()

        año_min = int(año_min) if año_min.isdigit() else None
        año_max = int(año_max) if año_max.isdigit() else None

        archivo = "libros.json" if self.tipo_actual == "libro" else "peliculas.json"
        items = cargar_datos(archivo)

        recomendaciones = recomendar(items, self.tipo_actual, generos, persona, año_min, año_max)

        self.limpiar_ventana()
        frame = ttk.Frame(self.root, padding=15)
        frame.pack(expand=True, fill="both")

        # Fondo uniforme blanco
        self.root.configure(bg="white")
        frame.configure(style="White.TFrame")

        ttk.Label(frame, text="RESULTADOS", font=("Segoe UI", 16, "bold"), background="white").pack(pady=10)

        if not recomendaciones:
            ttk.Label(frame, text="No se encontraron coincidencias.", foreground="red", background="white").pack(pady=10)
            ttk.Button(frame, text="Volver", command=self.mostrar_tipo).pack(pady=15)
            return

        # Estilos De la tabla
        style = ttk.Style()
        style.theme_use("clam")

        style.configure("Treeview",
                        background="white",
                        foreground="#222",
                        rowheight=25,
                        fieldbackground="white",
                        font=("Segoe UI", 10))

        style.configure("Treeview.Heading",
                        background="#2C73D2",
                        foreground="white",
                        font=("Segoe UI", 10, "bold"))

        style.map("Treeview",
                background=[("selected", "#A7C7E7")],
                foreground=[("selected", "black")])

        # Forma de la tabla
        tabla_frame = ttk.Frame(frame)
        tabla_frame.pack(fill="both", expand=True, pady=10)

        columnas = ("col1", "col2", "col3", "col4")
        tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10, style="Treeview")

        if self.tipo_actual == "libro":
            tabla.heading("col1", text="Título")
            tabla.heading("col2", text="Autor")
        else:
            tabla.heading("col1", text="Título")
            tabla.heading("col2", text="Director")

        tabla.heading("col3", text="Género")
        tabla.heading("col4", text="Año")

        # Tamaño de columnas
        tabla.column("col1", width=200, anchor="w")
        tabla.column("col2", width=180, anchor="w")
        tabla.column("col3", width=220, anchor="w")
        tabla.column("col4", width=60, anchor="center")

        # Scrollbar vertical
        scrollbar_y = ttk.Scrollbar(tabla_frame, orient="vertical", command=tabla.yview)
        tabla.configure(yscrollcommand=scrollbar_y.set)
        scrollbar_y.pack(side="right", fill="y")

        tabla.pack(fill="both", expand=True, side="left")

        # Filas alternadas (gris muy suave)
        for i, (item, _) in enumerate(recomendaciones):
            genero_str = ", ".join(item["genero"]) if isinstance(item["genero"], list) else item["genero"]
            tag = "evenrow" if i % 2 == 0 else "oddrow"
            tabla.insert("", tk.END, values=(
                item["titulo"],
                item["autor" if self.tipo_actual == "libro" else "director"],
                genero_str,
                item["año"]
            ), tags=(tag,))

        tabla.tag_configure("evenrow", background="#F9F9F9")
        tabla.tag_configure("oddrow", background="#FFFFFF")

        ttk.Button(frame, text="Volver", command=self.mostrar_tipo).pack(pady=15)


    # Utilidad
    def limpiar_ventana(self):
        for widget in self.root.winfo_children():
            widget.destroy()

# Ejecucion del programa
if __name__ == "__main__":
    root = tk.Tk()
    app = RecomendadorApp(root)
    root.mainloop()