import tkinter as tk
from Wallascrap import Wallascrap

Walla = Wallascrap()
def on_button_click():
    entradanombre = text_box.get()
    Walla.SetEntradaNombre(entradanombre)
    url = text_box2.get()

    Walla.pull_wallapop(url,text_box3.get())


root = tk.Tk()
root.geometry("400x300")
root.title("Selecciona un nombre para el csv")

label = tk.Label(root, text="Nombre del csv: ")
label.pack()

text_box = tk.Entry(root, width=20)
text_box.pack()

label2 = tk.Label(root, text="Url del produto: ")
label2.pack()

text_box2 = tk.Entry(root, width=20)
text_box2.pack()

label3 = tk.Label(root, text="Profundidad: ")
label3.pack()

text_box3 = tk.Entry(root, width=20)
text_box3.pack()


button = tk.Button(root, text="Generar CSV", command=on_button_click)
button.pack()


root.mainloop()






