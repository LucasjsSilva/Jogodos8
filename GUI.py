from tkinter import *
import tkinter as tk
from tkinter import ttk
import time

import main
from main import *
from main import retornarCaminhoSolucao

def delay(segundos):
   time.sleep(segundos)

estado_inicial = []
estados = ''
def geravetor(number):
    global estado_inicial
    global estados
    if number not in estado_inicial:
        if len(estado_inicial) < 9:
            estado_inicial.append(number)
            if len(estado_inicial)==1:
                estados = str(number) + '     '
            else:
                if len(estado_inicial) % 3 == 0 and len(estado_inicial)!=9:
                    estados += str(number) + "     \n\n"
                else:
                    estados += str(number) + "     "

            lbl2.config(text=estados, background="#708090",font=15)
def geraMsg(camin, prof,quantElem,MemAt,pico):
    msg = ''
    for index, c in enumerate(camin):
        msg += "Estado: " + str(index) + "\n" + str(c[0]) + " " + str(c[1]) + " " + str(c[2]) + "\n" + str(c[3]) + " " + str(c[4]) + " " + str(c[5]) + "\n" + str(c[6]) + " " + str(c[7]) + " " + str(c[8]) +"\n\n"
    msg += f"Profundidade: {prof} \n"
    msg += f"Quantidade de Estados na Borda: {quantElem}\n"
    msg += f"Memória atual: {MemAt} bytes, Pico de memória: {pico} bytes"
    return msg

def buscarSolucao(metodo):
    global estado_inicial
    estado_objetivo = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    if len(estado_inicial) == 9:
    
        if metodo == 'Largura':
            tracemalloc.start()  # Inicia a coleta de rastreamento de alocação de memória
            solucao, profundidade, quantidadeDeElementosNaBorda = buscaEmLargura(estado_inicial, estado_objetivo)
            MemoriaAtualmenteAlocada, picoDeMemoria = tracemalloc.get_traced_memory()  # Obtém a quantidade de memória alocada
            tracemalloc.stop()
            caminho = retornarCaminhoSolucao(solucao)
            mostraCaminho(caminho)
            mostraSolucao(geraMsg(caminho, profundidade, quantidadeDeElementosNaBorda, MemoriaAtualmenteAlocada, picoDeMemoria))
        elif metodo == 'Profundidade':
            tracemalloc.start()  # Inicia a coleta de rastreamento de alocação de memória
            solucao, profundidade, quantidadeDeElementosNaBorda = buscaEmProfundidade(estado_inicial, estado_objetivo)
            MemoriaAtualmenteAlocada, picoDeMemoria = tracemalloc.get_traced_memory()  # Obtém a quantidade de memória alocada
            tracemalloc.stop()
            caminho = retornarCaminhoSolucao(solucao)
            mostraCaminho(caminho)
            mostraSolucao(geraMsg(caminho, profundidade, quantidadeDeElementosNaBorda, MemoriaAtualmenteAlocada, picoDeMemoria))
        elif metodo == 'Guloso':
            tracemalloc.start()
            solucao, profundidade, quantidadeDeElementosNaBorda = buscaGulosa_algoritmo(estado_inicial, estado_objetivo)
            MemoriaAtualmenteAlocada, picoDeMemoria = tracemalloc.get_traced_memory()  # Obtém a quantidade de memória alocada
            tracemalloc.stop()
            caminho = retornarCaminhoSolucao(solucao)
            mostraCaminho(caminho)
            mostraSolucao(geraMsg(caminho, profundidade, quantidadeDeElementosNaBorda, MemoriaAtualmenteAlocada,
                                    picoDeMemoria))
        elif metodo == 'A*':
            tracemalloc.start()  # Inicia a coleta de rastreamento de alocação de memória
            solucao, profundidade, quantidadeDeElementosNaBorda = a_estrela(estado_inicial, estado_objetivo)
            MemoriaAtualmenteAlocada, picoDeMemoria = tracemalloc.get_traced_memory()  # Obtém a quantidade de memória alocada
            tracemalloc.stop()
            caminho = retornarCaminhoSolucao(solucao)
            mostraCaminho(caminho)
            mostraSolucao(geraMsg(caminho, profundidade, quantidadeDeElementosNaBorda, MemoriaAtualmenteAlocada, picoDeMemoria))
        else:
            print("Metodo de Busca não Encontrado")

       
def mostraCaminho(caminho):
    for elemento in caminho:
        lbl4.config(text=str(elemento[0]) + "      " + str(elemento[1]) + "      " + str(elemento[2]) + "\n\n" +
                         str(elemento[3]) + "      " + str(elemento[4]) + "      " + str(elemento[5]) + "\n\n" +
                         str(elemento[6]) + "      " + str(elemento[7]) + "      " + str(elemento[8]),
                    background="#B0C4DE", font=15)
        janela.update()
        delay(1)
def mostraSolucao(msg):
    resultados.delete(1.0,'end')

    resultados.insert('end',msg)

janela = tk.Tk()
janela.title("Jogo dos 8")
janela.geometry("510x375")
metodo = ttk.Combobox(janela)
metodo['values'] = ('Largura', 'Profundidade', 'Guloso', 'A*')
metodo.current(0)
metodo.place(x=5, y=5)
tk.Label(janela, text="Digite o estado de inicial:").place(x=5,y=30)
for i in range(9):
    tk.Button(janela, text=str(i), borderwidth=1, width=3,command=lambda i=i: geravetor(i)).place(y=((i+6)//3)*35, x=((i % 3)*45)+5)
ret1 = Canvas(janela)
ret1.create_rectangle(40, 150, 150, 40, fill="#708090")
ret1.pack()
ret1.place(x=150, y=25)

lbl1 = tk.Label(janela, text="Estado inicial: ")
lbl1.pack()
lbl1.place(x=200,y=30)

lbl2 = tk.Label(janela, text="",background="#708090")
lbl2.pack()
lbl2.place(x=205,y=75)

ret2 = Canvas(janela)
ret2.create_rectangle(40, 150, 150, 40, fill="#B0C4DE")
ret2.pack()
ret2.place(x=350, y=25)

lbl3 = tk.Label(janela, text="Estados: ")
lbl3.pack()
lbl3.place(x=420,y=30)

lbl4 = tk.Label(janela, text="",background="#B0C4DE")
lbl4.pack()
lbl4.place(x=405,y=75)

lbl5 = tk.Label(janela, text="Solução: ")
lbl5.pack()
lbl5.place(x=5,y=180)

resultados = tk.Text(janela,width=62,height=10)
resultados.pack()
resultados.place(x=5, y=200)

tk.Button(janela, text='Buscar', command=lambda: buscarSolucao(metodo.get())).place(x=325,y=100)

janela.mainloop()