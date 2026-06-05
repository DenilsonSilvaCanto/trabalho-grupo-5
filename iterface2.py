import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

ARQUIVO = "arquivo_alunos.txt"

alunos = []
proximo_id = 1

def centralizar(janela, largura, altura):
    x = (janela.winfo_screenwidth() - largura) // 2
    y = (janela.winfo_screenheight() - altura) // 2
    janela.geometry(f"{largura}x{altura}+{x}+{y}")

def salvar():
    with open(ARQUIVO, "w", newline="", encoding="utf-8") as arq:
        writer = csv.DictWriter(
            arq,
            fieldnames=["id", "nome", "disciplina", "nota"]
        )

        writer.writeheader()

        for aluno in alunos:
            writer.writerow(aluno)

def carregar():
    global proximo_id

    if not os.path.exists(ARQUIVO):
        salvar()
        return

    with open(ARQUIVO, "r", encoding="utf-8") as arq:
        reader = csv.DictReader(arq)

        for linha in reader:
            aluno = {
                "id": int(linha["id"]),
                "nome": linha["nome"],
                "disciplina": linha["disciplina"],
                "nota": float(linha["nota"])
            }

            alunos.append(aluno)

            if aluno["id"] >= proximo_id:
                proximo_id = aluno["id"] + 1

def atualizar_tabela():
    tabela.delete(*tabela.get_children())

    for aluno in sorted(alunos, key=lambda a: a["nome"]):
        tabela.insert(
            "",
            tk.END,
            values=(
                aluno["id"],
                aluno["nome"],
                aluno["disciplina"],
                f"{aluno['nota']:.2f}"
            )
        )

def abrir_cadastro():
    global proximo_id

    topo = tk.Toplevel(janela)
    topo.title("Cadastrar Aluno")

    centralizar(topo, 350, 250)

    topo.resizable(False, False)
    topo.grab_set()

    tk.Label(topo, text="Nome").pack(pady=5)
    nome = tk.Entry(topo, width=30)
    nome.pack()

    tk.Label(topo, text="Disciplina").pack(pady=5)
    disciplina = tk.Entry(topo, width=30)
    disciplina.pack()

    tk.Label(topo, text="Nota").pack(pady=5)
    nota = tk.Entry(topo, width=30)
    nota.pack()

    def salvar_aluno():
        global proximo_id
        try:
            valor_nota = float(nota.get().replace(",", "."))
        except:
            messagebox.showerror("Erro", "Nota inválida")
            return

        if not nome.get() or not disciplina.get():
            messagebox.showerror("Erro", "Preencha todos os campos")
            return

        alunos.append({
            "id": proximo_id,
            "nome": nome.get().title(),
            "disciplina": disciplina.get().title(),
            "nota": valor_nota
        })

        proximo_id += 1

        salvar()
        atualizar_tabela()

        topo.destroy()

    tk.Button(
        topo,
        text="Salvar",
        command=salvar_aluno
    ).pack(pady=20)

def remover():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno")
        return

    id_aluno = int(
        tabela.item(selecionado[0])["values"][0]
    )

    for aluno in alunos:
        if aluno["id"] == id_aluno:
            alunos.remove(aluno)
            break

    salvar()
    atualizar_tabela()

def atualizar_nota():
    selecionado = tabela.selection()
    if not selecionado:
        messagebox.showwarning("Aviso", "Selecione um aluno")
        return

    id_aluno = int(
        tabela.item(selecionado[0])["values"][0]
    )

    topo = tk.Toplevel(janela)
    topo.title("Atualizar Nota")

    centralizar(topo, 300, 150)

    topo.resizable(False, False)
    topo.grab_set()

    tk.Label(topo, text="Nova Nota").pack(pady=10)

    entrada = tk.Entry(topo)
    entrada.pack()

    def salvar_nota():
        try:
            nova_nota = float(
                entrada.get().replace(",", ".")
            )
        except:
            messagebox.showerror("Erro", "Nota inválida")
            return

        for aluno in alunos:
            if aluno["id"] == id_aluno:
                aluno["nota"] = nova_nota
                break

        salvar()
        atualizar_tabela()

        topo.destroy()

    tk.Button(
        topo,
        text="Salvar",
        command=salvar_nota
    ).pack(pady=10)

def buscar():
    termo = busca.get().lower()
    tabela.delete(*tabela.get_children())

    for aluno in alunos:
        if (
            termo in aluno["nome"].lower()
            or termo == str(aluno["id"])
        ):
            tabela.insert(
                "",
                tk.END,
                values=(
                    aluno["id"],
                    aluno["nome"],
                    aluno["disciplina"],
                    f"{aluno['nota']:.2f}"
                )
            )

# JANELA PRINCIPAL

carregar()

janela = tk.Tk()
janela.title("Sistema de Notas")

janela.state("zoomed") 

tk.Button(
    janela,
    text="Novo Aluno",
    command=abrir_cadastro
).pack(pady=10)

frame_busca = tk.Frame(janela)
frame_busca.pack()

tk.Label(frame_busca, text="Buscar").pack(side="left")

busca = tk.Entry(frame_busca, width=30)
busca.pack(side="left", padx=5)

tk.Button(
    frame_busca,
    text="Pesquisar",
    command=buscar
).pack(side="left")

tk.Button(
    frame_busca,
    text="Mostrar Todos",
    command=atualizar_tabela
).pack(side="left", padx=5)

tabela = ttk.Treeview(
    janela,
    columns=("ID", "Nome", "Disciplina", "Nota"),
    show="headings",
    height=18
)

for coluna in ("ID", "Nome", "Disciplina", "Nota"):
    tabela.heading(coluna, text=coluna)

tabela.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

frame = tk.Frame(janela)
frame.pack(pady=10)

tk.Button(
    frame,
    text="Remover Aluno",
    command=remover
).pack(side="left", padx=5)

tk.Button(
    frame,
    text="Atualizar Nota",
    command=atualizar_nota
).pack(side="left", padx=5)

atualizar_tabela()

janela.mainloop()