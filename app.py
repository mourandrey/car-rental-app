from tkinter import ttk
from tkinter import *
from tkinter import messagebox
import sqlite3
import csv
from datetime import datetime, date

def conectar():
    return sqlite3.connect("database/projeto_final.db")

#Criação de tabela para gestor da app
def tabela_gestor():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS gestor(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
    )
    """)

    conn.commit()
    conn.close()

#Criando admin para a app
def criar_admin():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gestor WHERE username='admin'")
    existe = cursor.fetchone()

    if not existe:
        cursor.execute("""INSERT INTO gestor(username, password)
        VALUES(?, ?)""", ("admin", "1234"))

    conn.commit()
    conn.close()

#Validação do login
def validar_login(username, password):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM gestor WHERE username=? AND password=?", (username, password))

    user = cursor.fetchone()
    conn.close()

    return user

def abrir_login():
    login = Toplevel()
    login.title("Login - Luxury Wheels")
    login.geometry("600x400")
    login.wm_iconbitmap("recursos/logo.ico")

    Label(login, text = "Usuário").pack()
    user_entry = Entry(login)
    user_entry.pack()

    Label(login, text = "Senha").pack()
    password_entry = Entry(login, show="*")
    password_entry.pack()

    def entrar():
        if validar_login(user_entry.get(), password_entry.get()):
            login.destroy()
            abrir_menu()
        else:
            messagebox.showerror("Erro", "Login inválido")

    Button(login, text = "Login", command=entrar).pack(pady=10)
    login.mainloop()

#Criação da janela seguinte após validar menu
def abrir_menu():
    menu = Toplevel()
    menu.title("Luxury Wheels")
    menu.geometry("600x400")
    menu.wm_iconbitmap("recursos/logo.ico")

    Label(menu, text="Luxury Wheels", font=("Calibri", 14, "bold")).pack(pady=10)

    Button(menu, text = "Usuários", width=20, command=abrir_usuarios).pack(pady=5)
    Button(menu, text = "Carros", width=20, command=abrir_carros).pack(pady=5)
    Button(menu, text = "Reservas", width=20, command=abrir_reservas).pack(pady=5)

    Button(menu, text = "Sair", command=menu.destroy).pack(pady=20)

    menu.mainloop()

#Funções para registar, atualizar, listar e remover usuários
def registar_usuarios(primeiro_nome, ultimo_nome, email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO usuarios (primeiro_nome, ultimo_nome, email)
    VALUES (?, ?, ?)""", (primeiro_nome, ultimo_nome, email))

    conn.commit()
    conn.close()

def atualizar_usuarios(id, primeiro_nome, ultimo_nome, email):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""UPDATE usuarios SET primeiro_nome=?, ultimo_nome=?, email=?
    WHERE id=?""", (primeiro_nome, ultimo_nome, email, id))

    conn.commit()
    conn.close()

def listar_usuarios():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM usuarios")
    dados = cursor.fetchall()

    conn.close()
    return dados

#Função para abrir usuário quando clicar no botão de usuários
def abrir_usuarios():
    janela_usuarios = Toplevel()
    janela_usuarios.title("Usuários")
    janela_usuarios.geometry("600x400")

    #Criar o menu
    tree = ttk.Treeview(janela_usuarios, columns=("ID", "Nome", "Apelido", "Email"), show="headings")

    #Mostra para o utilizador as colunas feitas
    tree.heading("ID", text="ID")
    tree.heading("Nome", text="Nome")
    tree.heading("Apelido", text="Apelido")
    tree.heading("Email", text="Email")

    tree.pack(fill=BOTH, expand=True)

    def carregar():
        tree.delete(*tree.get_children())
        for usuario in listar_usuarios():
            tree.insert("", END, values=usuario)

    Button(janela_usuarios, text="Atualizar", command=carregar).pack()

    carregar()

def remover_usuarios(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM usuarios WHERE id=?", (id,))

    conn.commit()
    conn.close()


# Funções para registar, atualizar, listar e remover carros
def registar_carros(marca, modelo, transmissao, categoria,
                      quantidade, preco_diaria, data_legalizacao, data_proxima_revisao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO carros (marca, modelo, transmissao, categoria, 
    quantidade, preco_diaria, data_legalizacao, data_proxima_revisao)
    VALUES (?, ?, ?, ?, ? ,? ,? ,?)""", (marca, modelo, transmissao, categoria,
                                        quantidade, preco_diaria, data_legalizacao, data_proxima_revisao))
    conn.commit()
    conn.close()

def atualizar_carros(id, marca, modelo, transmissao, categoria,
                      quantidade, preco_diaria, data_legalizacao, data_proxima_revisao):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""UPDATE carros SET marca=?, modelo=?, transmissao=?, categoria=?,
    quantidade=?, preco_diaria=?, data_legalizacao=?, data_proxima_revisao=? 
    WHERE id=?""", (marca, modelo, transmissao, categoria,
                    quantidade, preco_diaria, data_legalizacao, data_proxima_revisao, id))

    conn.commit()
    conn.close()

def listar_carros():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM carros")
    dados = cursor.fetchall()

    conn.close()
    return dados

#Função para abrir carros quando clicar no botão de carros
def abrir_carros():
    janela_carros = Toplevel()
    janela_carros.title("Carros")
    janela_carros.geometry("600x400")

    tree = ttk.Treeview(janela_carros, columns=("ID", "Marca", "Modelo", "Transmissão", "Categoria",
                                               "Quantidade","Preço Diária", "Data de Legalização", "Data de Revisão", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Marca", text="Marca")
    tree.heading("Modelo", text="Modelo")
    tree.heading("Transmissão", text="Transmissão")
    tree.heading("Categoria", text="Categoria")
    tree.heading("Quantidade", text="Quantidade")
    tree.heading("Preço Diária", text="Preço Diária")
    tree.heading("Data de Legalização", text="Data de Legalização")
    tree.heading("Data de Revisão", text="Data de Revisão")
    tree.heading("Status", text="Status")

    tree.pack(fill=BOTH, expand=True)

    def carregar():
        tree.delete(*tree.get_children())
        for carro in listar_carros():
            tree.insert("", END, values=carro)

    Button(janela_carros, text="Atualizar", command=carregar).pack()

    carregar()


def remover_carros(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM carros WHERE id=?", (id,))

    conn.commit()
    conn.close()


#Funções para registar, atualizar, listar e remover reservas
def registar_reservas(carro_id, usuario_id, data_inicio, data_fim, forma_pagamento,
                      valor_total, status, carro_marca, carro_modelo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""INSERT INTO reservas (carro_id, usuario_id, data_inicio, data_fim, forma_pagamento,
    valor_total, status, carro_marca, carro_modelo)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""", (carro_id, usuario_id, data_inicio, data_fim, forma_pagamento,
                                       valor_total, status, carro_marca, carro_modelo))

    conn.commit()
    conn.close()

def atualizar_reservas(id, carro_id, usuario_id, data_inicio, data_fim, forma_pagamento,
                       valor_total, status, carro_marca, carro_modelo):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""UPDATE reservas SET carro_id=?, usuario_id=?, data_inicio=?, data_fim=?, forma_pagamento=?,
    valor_total=?, status=?, carro_marca=?, carro_modelo=?
    WHERE id=?""", (carro_id, usuario_id, data_inicio, data_fim, forma_pagamento,
                    valor_total, status, carro_marca, carro_modelo, id))

    conn.commit()
    conn.close()

def listar_reservas():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM reservas")

    dados = cursor.fetchall()

    conn.close()
    return dados

#Função para abrir reservas quando clicar no botão de reservas
def abrir_reservas():
    janela_reservas = Toplevel()
    janela_reservas.title("Reservas")
    janela_reservas.geometry("600x400")

    tree = ttk.Treeview(janela_reservas, columns=("ID", "Carro ID", "Usuário ID", "Data Inicial", "Data Final", "Forma de Pagamento",
                                                  "Valor Total", "Status", "Carro Marca", "Carro Modelo"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Carro ID", text="Carro ID")
    tree.heading("Usuário ID", text="Usuário ID")
    tree.heading("Data Inicial", text="Data Inicial")
    tree.heading("Data Final", text="Data Final")
    tree.heading("Forma de Pagamento", text="Forma de Pagamento")
    tree.heading("Valor Total", text="Valor Total")
    tree.heading("Status", text="Status")
    tree.heading("Carro Marca", text="Carro Marca")
    tree.heading("Carro Modelo", text="Carro Modelo")

    tree.pack(fill=BOTH, expand=True)

    def carregar():
        tree.delete(*tree.get_children())
        for reserva in listar_reservas():
            tree.insert("", END, values=reserva)

    Button(janela_reservas, text="Atualizar", command=carregar).pack()

    carregar()


def remover_reservas(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM reservas WHERE id=?", (id,))

    conn.commit()
    conn.close()

#Exportar arquivos CSV
def carros_csv():
    dados = listar_carros()

    with open("carros.csv", "w", newline="", encoding="utf-8") as ficheiro:
        writer = csv.writer(ficheiro)

        writer.writerow(["ID", "Marca", "Modelo", "Transmissão", "Categoria",
                         "Quantidade","Preço Diária", "Data Legalização", "Data Revisão"])

        writer.writerows(dados)

def usuarios_csv():
    dados = listar_usuarios()

    with open("usuarios.csv", "w", newline="", encoding="utf-8") as ficheiro:
        writer = csv.writer(ficheiro)

        writer.writerow(["ID", "Primeiro Nome", "Último Nome", "Email"])

        writer.writerows(dados)

def reservas_csv():
    dados = listar_reservas()

    with open("reservas.csv", "w", newline="", encoding="utf-8") as ficheiro:
        writer = csv.writer(ficheiro)

        writer.writerow(["ID", "Carro ID", "Usuário ID", "Data Início", "Data Fim", "Forma de Pagamento",
                         "Valor Total", "Status", "Marca", "Modelo"])

        writer.writerows(dados)

#Mostrar veículos alugados e dias restantes
def veiculos_alugados():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT carro_marca, carro_modelo, data_fim FROM reservas 
    WHERE status = 'ativa'""")

    dados = cursor.fetchall()
    conn.close()

    resultado = []

    for marca, modelo, data_fim in dados:
        data_fim = datetime.strptime( data_fim, "%Y-%m-%d")
        hoje = datetime.now()
        dias_restantes = (data_fim - hoje).days

        resultado.append((marca, modelo, dias_restantes))

    return resultado

#Mostrar os últimos usuários registados
def mostrar_usuarios(limite=10):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT primeiro_nome, ultimo_nome, email FROM usuarios
    ORDER BY id DESC LIMIT ?""", (limite,))

    dados = cursor.fetchall()
    conn.close()

    return dados

#Quantidade de veículos por categoria
def veiculos_por_categoria():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("SELECT categoria, COUNT(*) FROM carros GROUP BY categoria")

    dados = cursor.fetchall()
    conn.close()

    return dados

#Reservas do mês e total financeiro
def reservas_e_total():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT COUNT(*), SUM(valor_total) FROM reservas
    WHERE strftime('%Y-%m', data_inicio) = strftime('%Y-%m', 'now')""")

    dados = cursor.fetchone()
    conn.close()

    return dados

#Revisões com 15 dias a expirar
def revisoes_a_expirar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT marca, modelo, data_proxima_revisao FROM carros
    WHERE date(data_proxima_revisao) <= date('now', '+15 days')""")

    dados = cursor.fetchall()
    conn.close()

    return dados

#Legalizações com 15 dias a expirar
def legalizacoes_a_expirar():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT marca, modelo, data_legalizacao FROM carros
    WHERE date(data_legalizacao) <= date('now', '+15 days')""")

    dados = cursor.fetchall()
    conn.close()

    return dados

#Alertar com 5 dias de revisão
def alertar_revisao_5_dias():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""SELECT id, marca, modelo, data_proxima_revisao FROM carros
    WHERE date(data_proxima_revisao) <= date('now', '+5 days')
    AND date(data_proxima_revisao) >= date('now')""")

    dados = cursor.fetchall()
    conn.close()

    return dados

#Função para colocar carro em manutenção
def carro_em_manutencao(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE carros SET status='manutencao' WHERE id=?", (id,))

    conn.commit()
    conn.close()

#Função para ativar o carro novamente
def ativar_carro(id):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("UPDATE carros SET status='disponivel' WHERE id=?", (id,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    tabela_gestor()
    criar_admin()
    root = Tk()
    root.withdraw()

    abrir_login()
    root.mainloop()