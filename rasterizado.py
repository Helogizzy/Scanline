import tkinter as tk
from tkinter import colorchooser, messagebox
import math

class Triangulo:
    def __init__(self, pontos):
        self.pontos = pontos
        self.nome = "Triângulo"
        self.cores = ['black'] * 3

    def ordenar_pontos(self):
        self.pontos = sorted(self.pontos, key=lambda ponto: ponto[1])  # Ordena por coordenada y pois começa do y maior até o menor

class Aplicacao:
    def __init__(self, root):
        self.root = root
        self.root.title("Scanline APP")
        self.pontos = []
        self.triangulos = []
        self.triangulo_selecionado = None
        self.ponto_selecionado = None
        self.ponto_selecionado_index = None

        # Barra de ferramentas
        self.toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        self.canvas = tk.Canvas(self.root, width=800, height=600, bg="white")
        self.canvas.pack(side=tk.LEFT) 

        # Botão para limpar a tela
        self.botao_limpar = tk.Button(self.toolbar, text="Limpar Tela", command=self.limpar_tela)
        self.botao_limpar.pack(side=tk.LEFT)

        self.botao_remover = tk.Button(self.toolbar, text="Remover Triângulo", command=self.remover_triangulo)
        self.botao_remover.pack(side=tk.LEFT)
        self.botao_remover.config(state=tk.DISABLED)

        self.cor_arestas = (0, 0, 0)  # Cor padrão das arestas é preto
        self.botao_cor_arestas = tk.Button(self.toolbar, text="Cor da Aresta", command=self.selecionar_cor_arestas)
        self.botao_cor_arestas.pack(side=tk.LEFT)    

        self.botao_pintar = tk.Button(self.toolbar, text="Pintar Triângulo", command=self.pintar_triangulo_selecionado)
        self.botao_pintar.pack(side=tk.LEFT)
        self.botao_pintar.config(state=tk.DISABLED)

        self.buttons_color_picker = []
        for i in range(3):
            button_color_picker = tk.Button(self.toolbar, text=f"Cor do Vértice {i}", command=lambda i=i: self.selecionar_cor(i))
            button_color_picker.pack(side=tk.LEFT)
            self.buttons_color_picker.append(button_color_picker)

        self.desativar_botoes_cores_vertice()

        self.label = tk.Label(self.root, text="Clique esquerdo para adicionar pontos")
        self.label.pack()

        self.coordenadas_label = tk.Label(self.root, text="Coordenadas do Mouse: (0, 0)")
        self.coordenadas_label.pack()

        #menu de seleção de triângulos
        self.lista_triangulos = tk.Listbox(self.root)
        self.lista_triangulos.pack()
        self.lista_triangulos.bind("<ButtonRelease-1>", self.selecionar_triangulo)

        self.canvas.bind("<Button-1>", self.adicionar_ponto)
        self.canvas.bind("<Motion>", self.atualizar_coordenadas)

        self.menu_lateral = tk.Frame(self.root)
        self.menu_lateral.pack()

    def limpar_tela(self):
        # Limpa a tela
        self.canvas.delete("all")
        
        # Limpa a lista de triângulos
        self.triangulos.clear()
        self.lista_triangulos.delete(0, tk.END)

        # Reseta as variáveis
        self.pontos = []
        self.triangulo_selecionado = None
        self.ponto_selecionado = None
        self.ponto_selecionado_index = None

        # Reseta os botões
        self.botao_remover.config(state=tk.DISABLED)
        self.botao_cor_arestas.config(state=tk.NORMAL)
        self.botao_pintar.config(state=tk.DISABLED)
        self.desativar_botoes_cores_vertice()

    def desativar_botoes_cores_vertice(self):
        for button in self.buttons_color_picker:
            button.config(state=tk.DISABLED)
    
    def ativar_botoes_cores_vertice(self):
        for button in self.buttons_color_picker:
            button.config(state=tk.NORMAL)

    def adicionar_ponto(self, event):
        x, y = event.x, event.y # Obtém as coordenadas x e y do evento (posição do mouse quando clicado)
        ponto = (x, y) # Cria uma tupla com as coordenadas x e y, representando o ponto clicado
        self.pontos.append(ponto) # Adiciona o ponto à lista de pontos do aplicativo
        self.label.config(text=f"Pontos atuais: {self.pontos}")

        if len(self.pontos) == 3:
            triangulo = Triangulo(self.pontos.copy()) # Se três pontos foram selecionados, cria um objeto Triangulo com os pontos
            triangulo.ordenar_pontos() 
            self.triangulos.append(triangulo) # Adiciona o triângulo à lista de triângulos do aplicativo
            self.lista_triangulos.insert(tk.END, f"{triangulo.nome} {len(self.triangulos)}")
            self.pontos.clear() # Limpa a lista de pontos para que o usuário possa selecionar um novo conjunto de pontos
            self.label.config(text="Clique esquerdo para adicionar pontos")

        self.desenhar_triangulo()
        self.botao_pintar.config(state=tk.DISABLED)

    def desenhar_triangulo(self):
        self.canvas.delete("all")
        for i, triangulo in enumerate(self.triangulos): # Itera sobre a lista de triângulos
            pontos = triangulo.pontos # Obtém os pontos que definem o triângulo atual
            self.canvas.create_polygon(pontos, outline="black", fill="", width=2)

    def selecionar_triangulo(self, event):
        widget = event.widget # Obtém o componente da GUI que acionou o evento
        selection = widget.curselection() # Obtém a seleção atual na lista de triângulos
        if selection:
            index = selection[0]
            self.triangulo_selecionado = self.triangulos[index] ## Define o triângulo selecionado como o triângulo na posição do índice na lista de triângulos
            self.botao_remover.config(state=tk.NORMAL)
            self.botao_pintar.config(state=tk.NORMAL)
            self.ativar_botoes_cores_vertice()

    def pintar_triangulo_selecionado(self):
        if self.triangulo_selecionado:
            if all(color == 'black' for color in self.triangulo_selecionado.cores):
                tk.messagebox.showerror("Erro", "Por favor, escolha as cores dos vértices antes de pintar o triângulo.")
                return
        
            self.triangulo_selecionado.ordenar_pontos()
            v1, v2, v3 = self.triangulo_selecionado.pontos #vértices de pontos
            c1, c2, c3 = self.triangulo_selecionado.cores #cores
            rasterize_triangle(v1, v2, v3, c1, c2, c3, self.canvas) #passa os dados para a função

    def selecionar_cor_arestas(self):
        cor = colorchooser.askcolor()[0]
        if cor:
            self.cor_arestas = tuple(int(c) for c in cor) # Converte a cor selecionada (RGB) para uma tupla e atualiza a cor das arestas
            self.desenhar_triangulo() # Redesenha o triângulo com a nova cor das arestas

    def desenhar_triangulo(self):
        self.canvas.delete("all")  # Limpa todos os desenhos anteriores no canvas
        for i, triangulo in enumerate(self.triangulos):  # Itera sobre todos os triângulos na lista
            pontos = triangulo.pontos  # Obtém os pontos do triângulo atual
            # Desenha o triângulo como um polígono no canvas, usando os pontos e a cor de arestas definida
            self.canvas.create_polygon(pontos, outline="#%02x%02x%02x" % self.cor_arestas, fill="", width=2)

    def selecionar_cor(self, index):
        cor = colorchooser.askcolor()[0] 
        if cor:  # Verifica se uma cor foi selecionada
            # Converte a cor selecionada para uma tupla de inteiros e atribui ao vértice no índice
            self.triangulo_selecionado.cores[index] = tuple(int(c) for c in cor)
            self.desenhar_triangulo()  # Redesenha o triângulo para refletir a nova cor do vértice

    def remover_triangulo(self):
        if self.triangulo_selecionado:
            index = self.triangulos.index(self.triangulo_selecionado)
            del self.triangulos[index]
            self.lista_triangulos.delete(index)
            self.triangulo_selecionado = None
            self.ponto_selecionado = None
            self.ponto_selecionado_index = None
            self.botao_remover.config(state=tk.DISABLED)
            self.botao_pintar.config(state=tk.DISABLED)
            self.desenhar_triangulo()

    def atualizar_coordenadas(self, event):
        x, y = event.x, event.y
        self.coordenadas_label.config(text=f"Coordenadas do Mouse: ({x}, {y})")

    
def rasterize_triangle(v1, v2, v3, c1, c2, c3, canvas):
    if v1[1] == v2[1] == v3[1] or v1[0] == v2[0] == v3[0]:
        print("Não é um triângulo válido!")
        return

    # Ordena os vértices pelo valor de y
    vertices = sorted([(v1, c1), (v2, c2), (v3, c3)], key=lambda v: v[0][1])
    v1, c1 = vertices[0] # vértice com o menor y
    v2, c2 = vertices[1] # vértice intermediário
    v3, c3 = vertices[2] #vértice com o maior y

    # Calcula a taxa de variação de cor entre os vértices
    taxa_cor_v12 = [(c2[i] - c1[i]) / (v2[1] - v1[1]) for i in range(3)] 
    taxa_cor_v13 = [(c3[i] - c1[i]) / (v3[1] - v1[1]) for i in range(3)]
    taxa_cor_v23 = [(c3[i] - c2[i]) / (v3[1] - v2[1]) for i in range(3)]

    # Calcula a taxa de variação dos vértices para o incremento
    taxa_verticeX_12 = (v2[0] - v1[0]) / (v2[1] - v1[1]) 
    taxa_verticeX_13 = (v3[0] - v1[0]) / (v3[1] - v1[1])
    taxa_verticeX_23 = (v3[0] - v2[0]) / (v3[1] - v2[1])

    # Separa as cores
    cor_v12_R, cor_v12_G, cor_v12_B = c1
    cor_v13_R, cor_v13_G, cor_v13_B = c1
    cor_v23_R, cor_v23_G, cor_v23_B = c2

    # Inicializa as posições x para cada vértice
    cor_v12_para_X = v1[0] 
    cor_v13_para_X = v1[0]
    cor_v23_para_x = v2[0]

    # Para cada linha horizontal do triângulo
    for y in range(v1[1], v3[1] - 1):
        if y < v2[1]: # Se y é menor que o y do vértice 2
            # Desenha uma linha de varredura entre os vértices 1 e 2
            draw_scanline(cor_v12_para_X, cor_v13_para_X, [cor_v12_R, cor_v12_G, cor_v12_B], [cor_v13_R, cor_v13_G, cor_v13_B], y, canvas)
            # Atualiza as cores e as posições x para a próxima linha
            cor_v12_R += taxa_cor_v12[0]
            cor_v12_G += taxa_cor_v12[1]
            cor_v12_B += taxa_cor_v12[2]
            cor_v12_para_X += taxa_verticeX_12
            cor_v13_para_X += taxa_verticeX_13
        else: # Se y é maior ou igual ao y do vértice 2
            # Desenha uma linha de varredura entre os vértices 2 e 3
            draw_scanline(cor_v23_para_x, cor_v13_para_X, [cor_v23_R, cor_v23_G, cor_v23_B], [cor_v13_R, cor_v13_G, cor_v13_B], y, canvas)
            # Atualiza as cores e as posições x para a próxima linha
            cor_v23_R += taxa_cor_v23[0]
            cor_v23_G += taxa_cor_v23[1]
            cor_v23_B += taxa_cor_v23[2]
            cor_v23_para_x += taxa_verticeX_23
            cor_v13_para_X += taxa_verticeX_13
            
        # Atualiza as cores para a próxima linha
        cor_v13_R += taxa_cor_v13[0]
        cor_v13_G += taxa_cor_v13[1]
        cor_v13_B += taxa_cor_v13[2]

def draw_scanline(x1, x2, c1, c2, y, canvas):  
    # Se x1 for maior que x2, troca os valores de x1 e x2 e as cores correspondentes
    if x1 > x2:
        x1, x2 = x2, x1
        c1, c2 = c2, c1

    # Calcula a variação de cor entre os pontos x1 e x2 para cada componente de cor
    taxa_cor_R = (c2[0] - c1[0]) / (x2 - x1) if x2 != x1 else 0
    taxa_cor_G = (c2[1] - c1[1]) / (x2 - x1) if x2 != x1 else 0
    taxa_cor_B = (c2[2] - c1[2]) / (x2 - x1) if x2 != x1 else 0
    
    # Inicializa os componentes de cor com os valores de c1
    cor_R, cor_G, cor_B = c1

    # Para cada pixel na linha horizontal
    for x in range(int(x1), int(x2)):
        color_hex = "#{:02X}{:02X}{:02X}".format(int(cor_R), int(cor_G), int(cor_B))
        # Desenha um pixel na tela com a cor calculada
        canvas.create_rectangle(x, y, x+1, y+1, outline=color_hex, fill=color_hex)
        # Atualiza os componentes de cor para o próximo pixel
        cor_R += taxa_cor_R
        cor_G += taxa_cor_G
        cor_B += taxa_cor_B

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()