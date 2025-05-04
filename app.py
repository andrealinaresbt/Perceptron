import tkinter as tk
from tkinter import filedialog, messagebox

def read_configuration(ruta):
    with open(ruta, 'r') as archivo:
        valores = list(map(float, archivo.readline().strip().split(',')))
        print(f"Valores leídos del archivo: {valores}")  # Depuración
        return valores[0], valores[1:]

def calculate_ponderated_sum(entrada, pesos, bias):
    suma = sum(x * w for x, w in zip(entrada, pesos)) + bias
    print(f"Entrada: {entrada}, Pesos: {pesos}, Bias: {bias} -> Suma ponderada: {suma}")  # Depuración
    return suma

def activation(valor, tipo):
    if tipo == "Escalón":
        resultado = 1 if valor >= 0 else 0
    elif tipo == "Lineal":
        resultado = valor
    print(f"Valor activado ({tipo}): {valor} -> Resultado: {resultado}")  # Depuración
    return resultado

class PerceptronGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Perceptrón Interactivo")
        self.bias = None
        self.pesos = []
        self.activacion_tipo = tk.StringVar(value="Escalón")
        
        self.build_ui()

    def build_ui(self):
        # Frame para la configuración
        config_frame = tk.Frame(self.root)
        config_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(config_frame, text="Archivo de configuración:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.Button(config_frame, text="Cargar Configuración", command=self.cargar_config).pack(side=tk.LEFT, padx=5)

        # Frame para la selección de la función de activación
        activacion_frame = tk.Frame(self.root)
        activacion_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(activacion_frame, text="Función de activación:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        tk.OptionMenu(activacion_frame, self.activacion_tipo, "Escalón", "Lineal").pack(side=tk.LEFT, padx=5)

        # Frame para la entrada manual
        entrada_manual_frame = tk.Frame(self.root)
        entrada_manual_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(entrada_manual_frame, text="Entrada manual (separada por comas):", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.entrada_manual = tk.Entry(entrada_manual_frame, width=50)
        self.entrada_manual.pack(side=tk.LEFT, padx=5)
        tk.Button(entrada_manual_frame, text="Evaluar Entrada Manual", command=self.evaluar_manual).pack(side=tk.LEFT, padx=5)

        # Frame para la carga del archivo de entradas
        archivo_frame = tk.Frame(self.root)
        archivo_frame.pack(padx=20, pady=10, fill="x")

        tk.Button(archivo_frame, text="Cargar Archivo de Entradas", command=self.evaluar_archivo).pack(side=tk.LEFT, padx=5)

        # Frame para la salida
        salida_frame = tk.Frame(self.root)
        salida_frame.pack(padx=20, pady=10, fill="x")

        tk.Label(salida_frame, text="Salidas:", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=5)
        self.salida = tk.Text(salida_frame, height=10, width=60)
        self.salida.pack(side=tk.BOTTOM, padx=5)


    def cargar_config(self):
        ruta = filedialog.askopenfilename(title="Seleccionar archivo de configuración")
        if ruta:
            try:
                self.bias, self.pesos = read_configuration(ruta)
                messagebox.showinfo("Éxito", "Archivo fue cargado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")

    def evaluar_manual(self):
        if self.bias is None:
            messagebox.showwarning("Advertencia!", "Carga un archivo de configuración.")
            return

        try:
            entrada = list(map(float, self.entrada_manual.get().strip().split(',')))
            if len(entrada) != len(self.pesos):
                raise ValueError("Cantidad incorrecta de componentes.")
            suma = calculate_ponderated_sum(entrada, self.pesos, self.bias)
            resultado = activation(suma, self.activacion_tipo.get())
            self.salida.insert(tk.END, f"Entrada: {entrada} -> Resultado {suma} -> Salida: {resultado}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Entrada inválida: {e}")

    def evaluar_archivo(self):
        if self.bias is None:
            messagebox.showwarning("Advertencia!", "Carga un archivo de configuración.")
            return

        ruta = filedialog.askopenfilename(title="Seleccionar archivo de entradas")
        if ruta:
            try:
                with open(ruta, 'r') as archivo:
                    for i, linea in enumerate(archivo):
                        entrada = list(map(float, linea.strip().split(',')))
                        if len(entrada) != len(self.pesos):
                            self.salida.insert(tk.END, f"Línea {i+1} con error (componentes inválidas).\n")
                            continue
                        suma = calculate_ponderated_sum(entrada, self.pesos, self.bias)
                        resultado = activation(suma, self.activacion_tipo.get())
                        resultado = round(resultado, 2)
                        self.salida.insert(tk.END, f"Entrada {i+1}: {entrada} -> Resultado {suma} -> Salida: {resultado}\n")
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo procesar el archivo: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PerceptronGUI(root)
    root.mainloop()
