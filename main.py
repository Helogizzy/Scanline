import tkinter as tk
from tkinter import messagebox, colorchooser

class Triangulo:
    # Inicializa o triângulo com um número, pontos e cor
    def __init__(self, numero, pontos, cor):
        # Atributo para armazenar o número do triângulo
        self.numero = numero

        # Atributo para armazenar os pontos (coordenadas) do triângulo
        self.pontos = pontos

        # Atributo para armazenar a cor das arestas do triângulo
        self.cor = cor

        # Lista para armazenar as cores dos vértices do triângulo (inicializada com preto)
        self.cores_vertices = ['black'] * 3

class Aplicacao:
    def __init__(self, root):
        # Inicializa a aplicação com a raiz da interface gráfica
        self.root = root # Atribui a janela principal à variável root
        self.root.title("Scanline APP") # Define o título da janela
        self.pontos = [] # Lista para armazenar pontos ao desenhar um triângulo
        self.triangulos = [] # Lista para armazenar os triângulos desenhados
        self.desenho_ativo = True # Estado que controla se o desenho está ativo ou não

        # Barra de menu
        self.menu_bar = tk.Menu(root)
        root.config(menu=self.menu_bar)

        # Menu "Arquivo"
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Arquivo", menu=self.file_menu)
        self.file_menu.add_command(label="Limpar Tela", command=self.limpar_tela)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Sair", command=self.sair)

        # Menu "Cor dos Vértices"
        self.pintar_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="Cor dos Vértices", menu=self.pintar_menu)

        # Submenu "Cor do Vértice 1"
        self.pintar_menu.add_command(label="Cor do Vértice 1", command=lambda: self.escolher_cor_vertice(1))

        # Submenu "Cor do Vértice 2"
        self.pintar_menu.add_command(label="Cor do Vértice 2", command=lambda: self.escolher_cor_vertice(2))

        # Submenu "Cor do Vértice 3"
        self.pintar_menu.add_command(label="Cor do Vértice 3", command=lambda: self.escolher_cor_vertice(3))

        # Barra de ferramentas
        self.toolbar = tk.Frame(root, bd=1, relief=tk.RAISED)
        self.toolbar.pack(side=tk.TOP, fill=tk.X)

        # Botão "Editar Triângulo Selecionado" na barra de ferramentas
        self.botao_editar = tk.Button(self.toolbar, text="Editar Triângulo Selecionado", command=self.editar_triangulo)
        self.botao_editar.pack(side=tk.LEFT)
        self.botao_editar.config(state=tk.DISABLED)

        # Botão "Remover Triângulo Selecionado" na barra de ferramentas
        self.botao_remover = tk.Button(self.toolbar, text="Remover Triângulo Selecionado", command=self.remover_triangulo)
        self.botao_remover.pack(side=tk.LEFT)
        self.botao_remover.config(state=tk.DISABLED)

        # Botão "Cor da Aresta" na barra de ferramentas
        self.botao_cor = tk.Button(self.toolbar, text="Cor da Aresta", command=self.escolher_cor_aresta)
        self.botao_cor.pack(side=tk.LEFT)
        self.botao_cor.config(state=tk.ACTIVE)

        # Botão "Pintar Triângulo Selecionado" na barra de ferramentas
        self.botao_pintar = tk.Button(self.toolbar, text="Pintar Triângulo", command=self.pintar_triangulo_selecionado)
        self.botao_pintar.pack(side=tk.LEFT)
        self.botao_pintar.config(state=tk.DISABLED)

        # Criação de um widget Canvas para desenho, com largura 600, altura 400, e fundo branco
        self.canvas = tk.Canvas(root, width=600, height=400, bg="white")
        self.canvas.pack(expand=tk.YES, fill=tk.BOTH)

        # Criação de um rótulo (Label) para exibir mensagens ao usuário
        self.label = tk.Label(self.root, text="Clique esquerdo para adicionar pontos")
        self.label.pack()

        # Criação de um rótulo para exibir as coordenadas do mouse
        self.coordenadas_label = tk.Label(self.root, text="Coordenadas do Mouse: (0, 0)")
        self.coordenadas_label.pack()

        # Criação de uma lista (Listbox) para exibir os triângulos
        self.lista_triangulos = tk.Listbox(self.root)
        self.lista_triangulos.pack()

        # Vinculação do evento de liberação do botão esquerdo do mouse para a função selecionar_triangulo
        self.lista_triangulos.bind("<ButtonRelease-1>", self.selecionar_triangulo)

        # Vinculação de eventos do Canvas para as funções adicionar_ponto, parar_desenho e atualizar_coordenadas
        self.canvas.bind("<Button-1>", self.adicionar_ponto)
        self.canvas.bind("<Button-3>", self.parar_desenho)
        self.canvas.bind("<Motion>", self.atualizar_coordenadas)

        self.numero_triangulo = 1  # Adicionamos um contador global para os números dos triângulos
        self.triangulo_selecionado = None  # Inicializamos o triângulo selecionado como None

        # Botão "Parar Edição" na barra de ferramentas
        self.botao_parar_edicao = tk.Button(self.toolbar, text="Parar Edição", command=self.parar_edicao)
        self.botao_parar_edicao.pack(side=tk.LEFT)
        self.botao_parar_edicao.config(state=tk.DISABLED)

    # Função para adicionar um ponto ao clicar com o botão esquerdo
    def adicionar_ponto(self, event):
        # Verifica se o desenho está ativo (se o botão de desenho foi pressionado)
        if self.desenho_ativo:
            # Obtém as coordenadas do ponto clicado
            x, y = event.x, event.y

            # Cria uma tupla representando o ponto
            ponto = (x, y)

            # Adiciona o ponto à lista de pontos
            self.pontos.append(ponto)

            # Atualiza o texto na label mostrando os pontos atuais
            self.label.config(text=f"Pontos atuais: {self.pontos}")

            # Verifica se três pontos foram adicionados para formar um triângulo
            if len(self.pontos) == 3:
                # Obtém a cor das arestas selecionada (ou usa preto como padrão)
                cor = self.cor_arestas_selecionada if hasattr(self, 'cor_arestas_selecionada') else 'black'

                # Cria um objeto Triangulo com os pontos e a cor, e o adiciona à lista de triângulos
                triangulo = Triangulo(self.numero_triangulo, self.pontos.copy(), cor)
                self.triangulos.append(triangulo)

                # Insere o triângulo na lista gráfica na interface
                self.lista_triangulos.insert(tk.END, f"Triângulo {triangulo.numero}")

                # Atualiza o contador para o próximo número único de triângulo
                self.numero_triangulo += 1

                # Limpa a lista de pontos e atualiza a label
                self.pontos.clear()
                self.label.config(text="Clique esquerdo para adicionar pontos")

            # Redesenha os triângulos na tela
            self.desenhar_triangules()

            # Habilita os botões de escolher cor e pintar triângulo
            self.botao_cor.config(state=tk.NORMAL)
            self.botao_pintar.config(state=tk.NORMAL)
        
    def escolher_cor_aresta(self):
        # Chama o colorchooser.askcolor() para abrir a janela de escolha de cor e obtém a cor selecionada
        cor = colorchooser.askcolor()[1]

        # Armazena a cor selecionada na variável de instância cor_arestas_selecionada
        self.cor_arestas_selecionada = cor

        # Habilita o botão de escolher cor (caso esteja desabilitado)
        self.botao_cor.config(state=tk.NORMAL)

    def desenhar_triangules(self):
        # Limpa todos os itens desenhados no canvas
        self.canvas.delete("all")

        # Itera sobre a lista de triângulos e desenha cada um no canvas
        for triangulo in self.triangulos:
            # Cria um polígono (triângulo) no canvas usando as coordenadas dos vértices e as cores especificadas
            self.canvas.create_polygon(triangulo.pontos, outline=triangulo.cor, fill='', width=2)
        
    def selecionar_triangulo(self, event):
        # Obtém o índice do triângulo selecionado na lista
        index = self.lista_triangulos.curselection()

        # Verifica se um índice válido foi obtido (a lista não está vazia)
        if index:
            # Obtém o triângulo correspondente ao índice selecionado
            self.triangulo_selecionado = self.triangulos[index[0]]

            # Habilita os botões de edição e remoção do triângulo selecionado
            self.botao_editar.config(state=tk.NORMAL)
            self.botao_remover.config(state=tk.NORMAL)
            
            # Habilita o botão de parar edição
            self.botao_parar_edicao.config(state=tk.NORMAL)

    # Função para iniciar a edição de pontos de um triângulo
    def editar_triangulo(self):
        # Atualiza a etiqueta para indicar a ação durante a edição
        self.label.config(text="Clique esquerdo para editar pontos do triângulo")
        
        # Habilita o botão de parar edição
        self.botao_parar_edicao.config(state=tk.NORMAL)

        # Função interna para editar pontos quando o botão esquerdo do mouse é clicado
        def editar_ponto(event):
            # Obtém as coordenadas do ponto clicado
            x, y = event.x, event.y
            ponto = (x, y)

            # Remove o primeiro ponto da lista e adiciona o novo ponto ao final
            self.triangulo_selecionado.pontos.pop(0)
            self.triangulo_selecionado.pontos.append(ponto)

            # Atualiza a etiqueta com os pontos atuais do triângulo
            self.label.config(text=f"Pontos atuais: {self.triangulo_selecionado.pontos}")

            # Redesenha os triângulos após a edição
            self.desenhar_triangules()

        # Vincula a função de edição de ponto ao evento de clique do botão esquerdo do mouse
        self.canvas.bind("<Button-1>", editar_ponto)

        # Remove a vinculação do botão direito durante a edição
        self.canvas.unbind("<Button-3>")

    def pintar_triangulo_selecionado(self):
        if self.triangulo_selecionado:
            # Verifica se as cores dos vértices estão definidas
            if any(color == 'black' for color in self.triangulo_selecionado.cores_vertices):
                messagebox.showwarning("Aviso", "Selecione as cores dos vértices antes de pintar o triângulo.")
                return
            
            # Obtém as coordenadas dos vértices do triângulo
            x1, y1 = self.triangulo_selecionado.pontos[0]
            x2, y2 = self.triangulo_selecionado.pontos[1]
            x3, y3 = self.triangulo_selecionado.pontos[2]

            # Obtém as cores dos vértices do triângulo
            cor1 = self.triangulo_selecionado.cores_vertices[0]
            cor2 = self.triangulo_selecionado.cores_vertices[1]
            cor3 = self.triangulo_selecionado.cores_vertices[2]

            # Calcula as diferenças entre as coordenadas dos vértices
            dx1 = x2 - x1
            dy1 = y2 - y1
            dx2 = x3 - x1
            dy2 = y3 - y1

            # Loop pelos pontos internos ao triângulo
            for y in range(min(y1, y2, y3), max(y1, y2, y3) + 1):
                # Loop pelos pontos horizontais internos ao triângulo, limitados pelo valor mínimo e máximo das coordenadas x dos vértices
                for x in range(min(x1, x2, x3), max(x1, x2, x3) + 1):
                    # Verifica se o ponto (x, y) está dentro do triângulo usando coordenadas baricêntricas

                    # Calcula o determinante do triângulo (detT) usando as diferenças entre as coordenadas dos vértices
                    detT = dx1 * dy2 - dx2 * dy1

                    # Calcula os determinantes det1 e det2 para o ponto (x, y) em relação ao vértice 1 (x1, y1)
                    det1 = (x - x1) * dy2 - dx2 * (y - y1)
                    det2 = dx1 * (y - y1) - (x - x1) * dy1

                    # Calcula as coordenadas baricêntricas alpha, beta e gamma para o ponto (x, y)
                    alpha = det1 / detT
                    beta = det2 / detT
                    gamma = 1 - alpha - beta

                    if 0 <= alpha <= 1 and 0 <= beta <= 1 and 0 <= gamma <= 1:
                        # O ponto (x, y) está dentro do triângulo
                        # Calcula a cor interpolada para o ponto interno
                        cor_interpolada = (
                            int(alpha * self.hex_para_rgb(cor1)[0] + beta * self.hex_para_rgb(cor2)[0] + gamma * self.hex_para_rgb(cor3)[0]),
                            int(alpha * self.hex_para_rgb(cor1)[1] + beta * self.hex_para_rgb(cor2)[1] + gamma * self.hex_para_rgb(cor3)[1]),
                            int(alpha * self.hex_para_rgb(cor1)[2] + beta * self.hex_para_rgb(cor2)[2] + gamma * self.hex_para_rgb(cor3)[2])
                        )

                        # Converte a cor interpolada de RGB para hexadecimal
                        cor_hex = "#{:02X}{:02X}{:02X}".format(cor_interpolada[0], cor_interpolada[1], cor_interpolada[2])

                        # Preenche o ponto interno com a cor interpolada
                        self.canvas.create_rectangle(x, y, x + 1, y + 1, fill=cor_hex, outline=cor_hex)

    def parar_edicao(self):
        self.label.config(text="Clique esquerdo para adicionar pontos")
        self.botao_parar_edicao.config(state=tk.DISABLED)  # Desabilita o botão de parar edição

        # Limpa a seleção do triângulo
        self.triangulo_selecionado = None

        # Desvincula o evento de clique esquerdo antes de parar a edição
        self.canvas.unbind("<Button-1>")

        # Vincula novamente o evento de clique esquerdo para adicionar pontos
        self.canvas.bind("<Button-1>", self.adicionar_ponto)
        self.canvas.bind("<Button-3>", self.parar_desenho)  # Volta a vinculação do botão direito

        # Desativa os botões de editar e remover triângulo
        self.botao_editar.config(state=tk.DISABLED)
        self.botao_remover.config(state=tk.DISABLED)
        
        # Reseta o estado de desenho ativo
        self.desenho_ativo = True

    def parar_desenho(self, event):
        # Inverte o estado do desenho ativo
        self.desenho_ativo = not self.desenho_ativo

        # Atualiza a mensagem na label com base no estado do desenho
        if self.desenho_ativo:
            self.label.config(text="Clique esquerdo para adicionar pontos")
        else:
            self.label.config(text="Desenho parado (Clique direito para retomar)")

    def atualizar_coordenadas(self, event):
        # Obtém as coordenadas x, y do evento do mouse
        x, y = event.x, event.y

        # Atualiza a label com as coordenadas do mouse
        self.coordenadas_label.config(text=f"Coordenadas do Mouse: ({x}, {y})")

    def remover_triangulo(self):
        index = self.lista_triangulos.curselection()
        if index:
            # Remove o triângulo da lista
            self.remover_triangulo_da_lista(index[0])

            # Desvincula o evento de clique esquerdo antes de remover o triângulo
            self.canvas.unbind("<Button-1>")

            # Remove o triângulo da interface gráfica
            self.lista_triangulos.delete(index)
            self.botao_remover.config(state=tk.DISABLED)
            self.desenhar_triangules()

            # Vincula novamente o evento de clique esquerdo após a remoção
            self.canvas.bind("<Button-1>", self.adicionar_ponto)

    def remover_triangulo_da_lista(self, index):
        # Verifica se o índice está dentro dos limites válidos da lista de triângulos
        if 0 <= index < len(self.triangulos):
            # Remove o triângulo da lista usando o operador 'del'
            del self.triangulos[index]

    def limpar_tela(self):
        # Limpa a lista de pontos e triângulos
        self.pontos.clear()
        self.triangulos.clear()

        # Limpa a lista de triângulos exibida na interface gráfica
        self.lista_triangulos.delete(0, tk.END)

        # Redesenha o canvas sem os triângulos
        self.desenhar_triangules()

        # Atualiza a mensagem na label
        self.label.config(text="Clique esquerdo para adicionar pontos")

        # Desabilita os botões de editar e remover triângulo, parar edição e pintar
        self.botao_editar.config(state=tk.DISABLED)
        self.botao_remover.config(state=tk.DISABLED)
        self.botao_parar_edicao.config(state=tk.DISABLED)
        self.botao_pintar.config(state=tk.DISABLED)

        # Restaura o estado de desenho ativo
        self.desenho_ativo = True

        # Restabelece a vinculação do evento de clique esquerdo para adicionar pontos
        self.canvas.bind("<Button-1>", self.adicionar_ponto)

    def sair(self):
        if messagebox.askokcancel("Sair", "Deseja realmente sair?"):
            self.root.destroy()

    # Função para interpolar uma cor entre cor_inicio e cor_fim com base em uma fração (fracao)
    def interpolar_cor_num(self, cor_inicio, cor_fim, fracao):
        # Converte as cores iniciais e finais de hexadecimal para RGB
        r_inicio, g_inicio, b_inicio = self.hex_para_rgb(cor_inicio)
        r_fim, g_fim, b_fim = self.hex_para_rgb(cor_fim)

        # Interpola os componentes RGB com base na fração
        r_interp = int(r_inicio + fracao * (r_fim - r_inicio))
        g_interp = int(g_inicio + fracao * (g_fim - g_inicio))
        b_interp = int(b_inicio + fracao * (b_fim - b_inicio))

        # Cria a cor interpolada como uma tupla de valores RGB
        cor_interp = (r_interp, g_interp, b_interp)

        # Retorna a cor interpolada
        return cor_interp

    # Função para converter uma cor em formato hexadecimal para uma tupla de valores RGB
    def hex_para_rgb(self, cor_hex):
        # Converte a representação hexadecimal para uma tupla de inteiros RGB
        cor_rgb = tuple(int(cor_hex[i:i+2], 16) for i in (1, 3, 5))
        # Retorna a tupla de valores RGB
        return cor_rgb

    # Função para escolher uma cor usando uma caixa de diálogo e atribuir a cor a um vértice específico do triângulo selecionado
    def escolher_cor_vertice(self, numero_vertice):
        # Verifica se há um triângulo selecionado
        if self.triangulo_selecionado:
            # Abre a caixa de diálogo de escolha de cor e obtém a cor escolhida
            cor = colorchooser.askcolor()[1]
            
            # Atribui a cor escolhida ao vértice correspondente do triângulo selecionado
            self.triangulo_selecionado.cores_vertices[numero_vertice - 1] = cor

            # Redesenha os triângulos após a escolha da cor
            self.desenhar_triangules()

if __name__ == "__main__":
    root = tk.Tk()
    app = Aplicacao(root)
    root.mainloop()