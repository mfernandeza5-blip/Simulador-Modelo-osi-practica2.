import tkinter as tk
from tkinter import messagebox
import base64
import time


# ==========================================================
# SIMULADOR MODELO OSI - PRÁCTICA 2
# Comunicación de Datos
# ==========================================================


class SimuladorOSI:

    def __init__(self, ventana):

        self.ventana = ventana
        self.ventana.title("Simulador Modelo OSI - Práctica 2")
        self.ventana.geometry("1000x700")
        self.ventana.resizable(False, False)

        self.capas = [
            "7. Aplicación",
            "6. Presentación",
            "5. Sesión",
            "4. Transporte",
            "3. Red",
            "2. Enlace de Datos",
            "1. Física"
        ]

        self.crear_interfaz()

    # ======================================================
    # INTERFAZ
    # ======================================================

    def crear_interfaz(self):

        titulo = tk.Label(
            self.ventana,
            text="SIMULADOR INTERACTIVO DEL MODELO OSI",
            font=("Arial", 20, "bold")
        )
        titulo.pack(pady=15)

        subtitulo = tk.Label(
            self.ventana,
            text="Encapsulamiento y desencapsulamiento de datos",
            font=("Arial", 12)
        )
        subtitulo.pack()

        # --------------------------------------------------
        # PC-A
        # --------------------------------------------------

        marco_entrada = tk.Frame(self.ventana)
        marco_entrada.pack(pady=15)

        tk.Label(
            marco_entrada,
            text="PC-A - Ingrese el mensaje:",
            font=("Arial", 12, "bold")
        ).grid(row=0, column=0, padx=5)

        self.entrada = tk.Entry(
            marco_entrada,
            width=60,
            font=("Arial", 12)
        )
        self.entrada.grid(row=0, column=1, padx=5)

        # --------------------------------------------------
        # BOTONES
        # --------------------------------------------------

        marco_botones = tk.Frame(self.ventana)
        marco_botones.pack(pady=10)

        boton_transmitir = tk.Button(
            marco_botones,
            text="INICIAR TRANSMISIÓN",
            font=("Arial", 11, "bold"),
            command=self.transmitir,
            width=22
        )
        boton_transmitir.grid(row=0, column=0, padx=10)

        boton_limpiar = tk.Button(
            marco_botones,
            text="LIMPIAR",
            font=("Arial", 11, "bold"),
            command=self.limpiar,
            width=15
        )
        boton_limpiar.grid(row=0, column=1, padx=10)

        # --------------------------------------------------
        # ESTADO
        # --------------------------------------------------

        self.estado = tk.Label(
            self.ventana,
            text="Estado: esperando mensaje...",
            font=("Arial", 11, "italic")
        )
        self.estado.pack(pady=5)

        # --------------------------------------------------
        # ÁREA DE RESULTADOS
        # --------------------------------------------------

        marco_resultado = tk.Frame(self.ventana)
        marco_resultado.pack(pady=10)

        tk.Label(
            marco_resultado,
            text="Proceso de comunicación:",
            font=("Arial", 12, "bold")
        ).pack()

        self.resultado = tk.Text(
            marco_resultado,
            width=110,
            height=25,
            font=("Consolas", 10)
        )
        self.resultado.pack()

    # ======================================================
    # FUNCIÓN DE ENCABEZADO
    # ======================================================

    def mostrar(self, texto):

        self.resultado.insert(tk.END, texto + "\n")
        self.resultado.see(tk.END)
        self.ventana.update()

    # ======================================================
    # ENCAPSULAMIENTO
    # ======================================================

    def encapsular_capa(self, datos, capa):

        if capa == 7:
            return datos

        elif capa == 6:
            # Codificación Base64
            datos_codificados = base64.b64encode(
                datos.encode("utf-8")
            ).decode("utf-8")

            return datos_codificados

        elif capa == 5:
            # Identificador de sesión
            return "[SESION-001] " + datos

        elif capa == 4:
            # Información de transporte
            return "[TCP - PUERTO 5000] " + datos

        elif capa == 3:
            # Dirección IP simulada
            return "[IP: 192.168.1.10 -> 192.168.1.20] " + datos

        elif capa == 2:
            # Dirección MAC simulada
            return "[MAC: AA:BB:CC:DD:EE:01 -> AA:BB:CC:DD:EE:02] " + datos

        elif capa == 1:
            # Conversión a bits simulada
            bits = ""

            for caracter in datos:
                bits += format(ord(caracter), "08b")

            return bits

        return datos

    # ======================================================
    # DESENCAPSULAMIENTO
    # ======================================================

    def desencapsular_capa(self, datos, capa):

        if capa == 1:
            # Convertir bits nuevamente a texto
            caracteres = []

            for i in range(0, len(datos), 8):
                bloque = datos[i:i + 8]

                try:
                    caracteres.append(
                        chr(int(bloque, 2))
                    )
                except ValueError:
                    pass

            return "".join(caracteres)

        elif capa == 2:
            return datos.replace(
                "[MAC: AA:BB:CC:DD:EE:01 -> AA:BB:CC:DD:EE:02] ",
                ""
            )

        elif capa == 3:
            return datos.replace(
                "[IP: 192.168.1.10 -> 192.168.1.20] ",
                ""
            )

        elif capa == 4:
            return datos.replace(
                "[TCP - PUERTO 5000] ",
                ""
            )

        elif capa == 5:
            return datos.replace(
                "[SESION-001] ",
                ""
            )

        elif capa == 6:
            try:
                datos_decodificados = base64.b64decode(
                    datos
                ).decode("utf-8")

                return datos_decodificados

            except Exception:
                return datos

        elif capa == 7:
            return datos

        return datos

    # ======================================================
    # TRANSMISIÓN
    # ======================================================

    def transmitir(self):

        mensaje_original = self.entrada.get()

        if mensaje_original.strip() == "":
            messagebox.showwarning(
                "Mensaje vacío",
                "Ingrese un mensaje para iniciar la transmisión."
            )
            return

        self.resultado.delete("1.0", tk.END)

        self.estado.config(
            text="Estado: realizando transmisión..."
        )

        self.mostrar("=" * 80)
        self.mostrar("PC-A: INICIO DE LA TRANSMISIÓN")
        self.mostrar("=" * 80)

        self.mostrar(
            "Mensaje original: " + mensaje_original
        )

        self.mostrar("")
        self.mostrar(">>> ENCAPSULAMIENTO <<<")
        self.mostrar("")

        datos = mensaje_original

        # ----------------------------------------------
        # ENCAPSULAMIENTO 7 -> 1
        # ----------------------------------------------

        for capa in range(7, 0, -1):

            datos = self.encapsular_capa(
                datos,
                capa
            )

            nombre_capa = self.capas[7 - capa]

            self.mostrar(
                f"Capa {capa}: {nombre_capa}"
            )

            self.mostrar(
                "Datos: " + datos
            )

            self.mostrar("-" * 80)

            time.sleep(0.3)

        datos_transmitidos = datos

        self.mostrar("")
        self.mostrar(">>> MEDIO DE TRANSMISIÓN <<<")
        self.mostrar("")
        self.mostrar(
            "Los datos están siendo enviados desde PC-A hacia PC-B..."
        )
        self.mostrar(
            "Datos transmitidos correctamente."
        )

        self.mostrar("")
        self.mostrar(">>> DESENCAPSULAMIENTO <<<")
        self.mostrar("")

        datos = datos_transmitidos

        # ----------------------------------------------
        # DESENCAPSULAMIENTO 1 -> 7
        # ----------------------------------------------

        for capa in range(1, 8):

            datos = self.desencapsular_capa(
                datos,
                capa
            )

            nombre_capa = self.capas[7 - capa]

            self.mostrar(
                f"Capa {capa}: {nombre_capa}"
            )

            self.mostrar(
                "Datos: " + datos
            )

            self.mostrar("-" * 80)

            time.sleep(0.3)

        mensaje_recuperado = datos

        # ----------------------------------------------
        # RESULTADO FINAL
        # ----------------------------------------------

        self.mostrar("")
        self.mostrar("=" * 80)
        self.mostrar("PC-B: RESULTADO FINAL")
        self.mostrar("=" * 80)

        self.mostrar(
            "Mensaje original:    " + mensaje_original
        )

        self.mostrar(
            "Mensaje recuperado:  " + mensaje_recuperado
        )

        self.mostrar("")

        if mensaje_original == mensaje_recuperado:

            self.mostrar(
                "✓ TRANSMISIÓN EXITOSA"
            )

            self.mostrar(
                "✓ El mensaje original fue recuperado correctamente."
            )

            self.estado.config(
                text="Estado: transmisión exitosa ✓"
            )

            messagebox.showinfo(
                "Transmisión exitosa",
                "El mensaje llegó correctamente a PC-B."
            )

        else:

            self.mostrar(
                "✗ ERROR: El mensaje recuperado no coincide."
            )

            self.estado.config(
                text="Estado: error en la transmisión"
            )

    # ======================================================
    # LIMPIAR
    # ======================================================

    def limpiar(self):

        self.entrada.delete(0, tk.END)

        self.resultado.delete(
            "1.0",
            tk.END
        )

        self.estado.config(
            text="Estado: esperando mensaje..."
        )


# ==========================================================
# PROGRAMA PRINCIPAL
# ==========================================================

if __name__ == "__main__":

    ventana = tk.Tk()

    app = SimuladorOSI(ventana)

    ventana.mainloop()