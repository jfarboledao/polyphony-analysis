import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from conexion import collectionMXML, collectionKERN
from bson import ObjectId

def mostrarTabla(filas, columnas=None):
    # columnas: lista de nombres de columnas (puede venir de analizarKern)
    # Si no se pasan columnas, usar las por defecto
    if columnas is None:
        columnas = ["ID", "Autor", "Título", "Notas", "Formato", "hash"]

    # Mapeo para mostrar nombres bonitos
    col_map = {
        "_id": "ID",
        "autor": "Autor",
        "titulo": "Título",
        "catalogo": "Catálogo",
        "numeroNotas": "Notas",
        "formato": "Formato",
        "hash": "Hash"
    }
    import os
    from music21 import converter

    def abrir_music21():
        if tree is None:
            return
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
            return
        values = tree.item(selected[0])["values"]
        # Buscar el índice real de la columna hash y formato
        col_names = [col for col in columnas if visible_cols[col].get()]
        try:
            idx_hash = col_names.index("hash")
            idx_formato = col_names.index("formato")
        except ValueError:
            messagebox.showerror("Error", "Debes mostrar las columnas Hash y Formato para abrir en MuseScore.")
            return
        hash_val = values[idx_hash]
        formato = values[idx_formato]
        # Buscar archivo por hash en archivosKern y archivosMxml
        def buscar_archivo_por_hash(directorio, hash_val):
            for rootdir, _, files in os.walk(directorio):
                for fname in files:
                    fpath = os.path.join(rootdir, fname)
                    try:
                        with open(fpath, 'rb') as f:
                            import hashlib
                            contenido = f.read()
                            if hashlib.md5(contenido).hexdigest() == hash_val:
                                return fpath
                    except Exception:
                        continue
            return None
        if formato == ".krn":
            carpeta = "archivosKern"
        elif formato == ".musicxml":
            carpeta = "archivosMxml"
        else:
            messagebox.showerror("Error", "Formato de archivo no soportado para abrir en MuseScore.")
            return
        archivo = buscar_archivo_por_hash(carpeta, hash_val)
        if archivo:
            try:
                score = converter.parse(archivo)
                score.show()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo abrir el archivo en MuseScore: {e}")
        else:
            messagebox.showerror("Error", "No se encontró el archivo correspondiente al hash.")


    # Estado de columnas visibles
    visible_cols = {col: tk.BooleanVar(value=True) for col in columnas}

    # Crear ventana Tkinter
    root = tk.Tk()
    root.title("Obras encontradas")

    # Frame para filtros de columnas
    filter_frame = tk.Frame(root)
    filter_frame.pack(side="top", fill="x", padx=10, pady=5)
    tk.Label(filter_frame, text="Filtrar columnas:").pack(side="left")


    # Frame para tabla y scrollbar
    table_frame = tk.Frame(root)
    table_frame.pack(fill="both", expand=True)

    tree = None
    scrollbar = None

    def update_table():
        nonlocal tree, scrollbar
        # Eliminar widgets anteriores
        for widget in table_frame.winfo_children():
            widget.destroy()
        # Obtener columnas visibles
        cols_visibles = [col for col in columnas if visible_cols[col].get()]
        # Crear nuevo Treeview y nuevo Scrollbar
        tree_new = ttk.Treeview(table_frame, columns=[col_map.get(col, col) for col in cols_visibles], show="headings")
        for col in cols_visibles:
            tree_new.heading(col_map.get(col, col), text=col_map.get(col, col))
            tree_new.column(col_map.get(col, col), width=150, anchor="w")
        # Insertar filas filtradas
        col_indices = [i for i, col in enumerate(columnas) if visible_cols[col].get()]
        for fila in filas:
            filtered = [fila[i] for i in col_indices]
            tree_new.insert("", "end", values=filtered)
        tree_new.pack(side="left", fill="both", expand=True)
        # Crear y asociar nuevo scrollbar
        scrollbar_new = ttk.Scrollbar(table_frame, orient="vertical", command=tree_new.yview)
        tree_new.configure(yscrollcommand=scrollbar_new.set)
        scrollbar_new.pack(side="right", fill="y")
        tree_new.update_idletasks()
        tree = tree_new
        scrollbar = scrollbar_new

    def on_col_checkbox():
        update_table()

    # Crear checkboxes después de definir update_table
    for col in columnas:
        cb = tk.Checkbutton(filter_frame, text=col_map.get(col, col), variable=visible_cols[col], command=on_col_checkbox)
        cb.pack(side="left")

    update_table()


    # Botón para eliminar archivo
    def eliminar_archivo():
        if tree is None:
            return
        selected = tree.selection() # Obtener elementos (filas) seleccionadas
        conteoEliminados = 0
        if selected:
            for item in selected:
                values = tree.item(item)["values"]
                # Buscar el índice real de la columna formato e id
                col_names = [col for col in columnas if visible_cols[col].get()]
                try:
                    idx_formato = col_names.index("formato")
                    idx_id = col_names.index("_id")
                except ValueError:
                    messagebox.showerror("Error", "Debes mostrar las columnas ID y Formato para eliminar.")
                    return
                formato = values[idx_formato]
                _id_str = values[idx_id]
                try:
                    # Convertir a ObjectId si es posible
                    try:
                        _id = ObjectId(_id_str)
                    except Exception:
                        _id = _id_str
                    if formato == ".krn":
                        result = collectionKERN.delete_one({"_id": _id})
                    elif formato == ".musicxml" or formato == ".mxl":
                        result = collectionMXML.delete_one({"_id": _id})
                    else:
                        result = None
                    if result and result.deleted_count > 0:
                        tree.delete(item)
                        conteoEliminados += 1
                    else:
                        messagebox.showerror("Error", "No se pudo eliminar el archivo de la base de datos.")
                except Exception as e:
                    messagebox.showerror("Error", f"Ocurrió un error: {e}")

            if conteoEliminados > 0:
                messagebox.showinfo("Información", f"Se eliminaron {conteoEliminados} archivo(s).")
        else:
            messagebox.showwarning("Advertencia", "No se seleccionó ningún archivo.")
    btn_eliminar = tk.Button(root, text="Eliminar archivo", command=eliminar_archivo)
    btn_eliminar.pack(side="bottom", pady=10)

    def mostrar_opciones_insertar():
        from analizarKern import insertarDatos
        # Crear ventana emergente para elegir tipo de datos
        popup = tk.Toplevel(root)
        popup.title("Seleccionar tipo de datos a insertar")
        popup.geometry("300x120")

        def insertar_kern():
            popup.destroy()
            carpeta = "archivosKern"
            if carpeta:
                insertarDatos(carpeta)
                messagebox.showinfo("Éxito", "Datos KERN insertados (ver consola para detalles)")
                update_table()

        def insertar_musicxml():
            popup.destroy()
            carpeta = "archivosMxml"
            if carpeta:
                insertarDatos(carpeta)
                messagebox.showinfo("Éxito", "Datos MusicXML insertados (ver consola para detalles)")
                update_table()

        label = tk.Label(popup, text="¿Qué tipo de datos deseas insertar?")
        label.pack(pady=10)
        btn_kern = tk.Button(popup, text="Insertar datos KERN", command=insertar_kern)
        btn_kern.pack(pady=5)
        btn_mxml = tk.Button(popup, text="Insertar datos MusicXML", command=insertar_musicxml)
        btn_mxml.pack(pady=5)


    btn_abrir = tk.Button(root, text="Abrir MuseScore", command=abrir_music21)
    btn_abrir.pack(side="bottom", pady=5)

    btn_insertar = tk.Button(root, text="Insertar datos", command=mostrar_opciones_insertar)
    btn_insertar.pack(side="bottom", pady=5)

    root.mainloop()
