"""
Coordina las funciones a ejecutar
Interfaz gráfica con Tkinter
"""

import tkinter as tk
from tkinter import messagebox
import analizarKern
from conteoIntervalos import case_1, inicializar, case_2, case_3, voiceLeadingConteo
from pathlib import Path

inicializar()

# TODO: Hacer interfaz y reemplazar el main de consola
# TODO: Poner información de los archivos en la base de datos para que quede en la nube
# TODO: Terminar de implementar conteo de intervalos
# TODO: Revisar filtrado de columnas en visualizar datos

def insertar_datos():
    analizarKern.llamarTabla()

def visualizar_datos():
    analizarKern.visualizarDatos()

def eliminar_datos():
    # Ventana para elegir tipo de archivo a eliminar
    win = tk.Toplevel(root)
    win.title("Eliminar datos")
    tk.Label(win, text="Seleccione el tipo de archivo que desea eliminar:").pack(pady=10)
    def eliminar_kern():
        analizarKern.eliminarDatos(1)
        win.destroy()
    def eliminar_mxml():
        analizarKern.eliminarDatos(2)
        win.destroy()
    tk.Button(win, text="Archivos KERN", command=eliminar_kern).pack(pady=5)
    tk.Button(win, text="Archivos MXML", command=eliminar_mxml).pack(pady=5)

def contar_intervalos_casos():
    # Ventana para ingresar notas
    win = tk.Toplevel(root)
    win.title("Contar intervalos (casos)")
    tk.Label(win, text="Ingrese las notas para el análisis de intervalos:").pack(pady=10)
    entries = []
    for i in range(1, 5):
        frame = tk.Frame(win)
        frame.pack(pady=2)
        tk.Label(frame, text=f"Nota {i}:").pack(side="left")
        entry = tk.Entry(frame)
        entry.pack(side="left")
        entries.append(entry)
    def analizar():
        nota1 = entries[0].get()
        nota2 = entries[1].get()
        nota3 = entries[2].get()
        nota4 = entries[3].get()
        """
        # Ejemplos de casos:
        # Case 1
        # nota1 = 'G4'
        # nota2 = 'F-4'
        # nota3 = 'E5'
        # nota4 = 'F-5'
        #
        # Case 2
        # nota1 = 'G4'
        # nota2 = 'F-4'
        # nota3 = 'B4'
        # nota4 = 'C-5'
        #
        # Case 3
        # nota1 = 'E4'
        # nota2 = 'F-4'
        # nota3 = 'G4'
        # nota4 = 'F-4'
        """
        try:
            resultado = case_1(nota1, nota2, nota3, nota4)
            messagebox.showinfo("Resultado", f"Resultado: {resultado}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
    tk.Button(win, text="Analizar", command=analizar).pack(pady=10)

def contar_intervalos_bigdata():
    # Utiliza archivos KERN
    file_path = Path("archivosKern")
    resultados = []
    for archivo in file_path.iterdir():
        if archivo.is_file() and archivo.suffix.lower() in [".krn", ".musicxml"]:
            try:
                resultado = voiceLeadingConteo(archivo)
                resultados.append(f"{archivo.name}: {resultado}")
            except Exception as e:
                resultados.append(f"{archivo.name}: Error: {e}")
    # Mostrar resultados en ventana
    win = tk.Toplevel(root)
    win.title("Resultados Big Data")
    text = tk.Text(win, width=80, height=20)
    text.pack()
    for r in resultados:
        text.insert(tk.END, r + "\n")
    text.config(state="disabled")

def salir():
    root.destroy()

# Crear ventana principal
root = tk.Tk()
root.title("Base de datos de análisis de Kern")

tk.Label(root, text="Bienvenido a la base de datos de análisis de Kern", font=("Arial", 14)).pack(pady=15)

tk.Button(root, text="Insertar datos", width=40, command=insertar_datos).pack(pady=5)
tk.Button(root, text="Visualizar datos", width=40, command=visualizar_datos).pack(pady=5)
tk.Button(root, text="Eliminar datos", width=40, command=eliminar_datos).pack(pady=5)
tk.Button(root, text="Contar intervalos (casos)", width=40, command=contar_intervalos_casos).pack(pady=5)
tk.Button(root, text="Contar intervalos (Big data)", width=40, command=contar_intervalos_bigdata).pack(pady=5)
tk.Button(root, text="Salir", width=40, command=salir).pack(pady=15)

root.mainloop()
