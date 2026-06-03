
"""
Sistema: Juliano Automecânica
Versão: 1.0
Desenvolvido por: Wagnerdev
Ano: 2026
Descrição: Sistema de gestão de oficina mecânica desenvolvido em Python com Tkinter e SQLite.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
import webbrowser
import urllib.parse
from datetime import datetime
import os
import tempfile
import shutil
import json

from config import APP_TITLE, LOGO_PATH
from database import db, init_db
from PIL import Image, ImageTk, ImageDraw, ImageFont

class SplashScreen(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent 
        self.logo_img = None
        self.logo_small = None

        self.overrideredirect(True)
        self.configure(bg="#111827")

        width = 520
        height = 320
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (width // 2)
        y = (sh // 2) - (height // 2)
        self.geometry(f"{width}x{height}+{x}+{y}")

        box = tk.Frame(self, bg="#111827")
        box.pack(fill="both", expand=True)

        try:
            self.logo_img = tk.PhotoImage(file=LOGO_PATH)
            w = self.logo_img.width()
            h = self.logo_img.height()
            factor = max(1, int(max(w / 180, h / 180)))
            self.logo_small = self.logo_img.subsample(factor, factor)
            tk.Label(box, image=self.logo_small, bg="#111827").pack(pady=(30, 18))
        except Exception:
            tk.Label(
                box,
                text="🔧",
                font=("Segoe UI", 42, "bold"),
                fg="#ef4444",
                bg="#111827",
            ).pack(pady=(30, 18))

        tk.Label(
            box,
            text="Juliano Automecânica",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg="#111827",
        ).pack()

        tk.Label(
            box,
            text="Sistema de gestão da oficina",
            font=("Segoe UI", 11),
            fg="#cbd5e1",
            bg="#111827",
        ).pack(pady=(8, 18))

        tk.Label(
            box,
            text="Carregando sistema...",
            font=("Segoe UI", 11, "italic"),
            fg="#f59e0b",
            bg="#111827",
        ).pack()

        self.after(4300, self.finish)

    def finish(self):
        self.destroy()
        self.parent.state("zoomed")
        self.parent.deiconify()

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.withdraw()
        self.title(APP_TITLE)
        self.geometry("1100x650")
        self.minsize(980, 580)
        self.configure(bg="#f5f6f8")

        self.sidebar = tk.Frame(self, bg="#243246", width=270)
        self.sidebar.pack(side="left", fill="y")
        data_atual = datetime.now().strftime("%d/%m/%Y")

        tk.Label(
            self.sidebar,
            text=data_atual,
            bg="#243246",
            fg="white",
            font=("Segoe UI", 16, "bold")
        ).pack(side="bottom", pady=30)

        self.total_clientes_var = tk.StringVar(value="0")

        total_clientes_card = tk.Frame(
            self.sidebar,
            bg="#243246",
            highlightthickness=0,
            bd=0,
            width=220,
            height=88,
        )
        total_clientes_card.pack(side="bottom", fill="x", padx=18, pady=(0, 6))
        total_clientes_card.pack_propagate(False)

        tk.Label(
            total_clientes_card,
            text="Total de Clientes",
            bg="#243246",
            fg="white",
            font=("Segoe UI", 11),
        ).pack(pady=(10, 0))

        tk.Label(
            total_clientes_card,
            text="cadastrados",
            bg="#243246",
            fg="white",
            font=("Segoe UI", 11),
        ).pack()

        tk.Label(
            total_clientes_card,
            textvariable=self.total_clientes_var,
            bg="#243246",
            fg="#3b82f6",
            font=("Segoe UI", 22, "bold"),
        ).pack(pady=(0, 6))

        self.main = tk.Frame(self, bg="#f5f6f8")
        self.main.pack(side="right", fill="both", expand=True)

        self._build_sidebar_header()
        self._build_sidebar_buttons()

        self.content = tk.Frame(self.main, bg="#f5f6f8")
        self.content.pack(fill="both", expand=True, padx=18, pady=18)

        # Logo WagnerDev no canto inferior da janela
        try:
            logo_path = os.path.join(os.path.dirname(__file__), "assets", "logo_wagnerdev.png")
            img = Image.open(logo_path)
            img = img.resize((200, 120))  # largura, altura

            self.logo_wagner = ImageTk.PhotoImage(img)

            self.logo_label = tk.Label(self, image=self.logo_wagner, bg="#f5f6f8")
            self.logo_label.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-10)

        except Exception as e:
            print("Erro ao carregar logo:", e)

        self.frames = {}
        for F in (DashboardFrame, ClientsFrame, ServicesFrame, OrdemServicoFrame, NotasFiscaisFrame, OrdersFrame, FinanceFrame):
            frame = F(self.content, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show("ServicesFrame")
        self.after(100, lambda: SplashScreen(self))


    def _build_sidebar_header(self):
        header = tk.Frame(self.sidebar, bg="#1c283a")
        header.pack(fill="x")

        try:
            self.logo_img = tk.PhotoImage(file=LOGO_PATH)
        except Exception:
            self.logo_img = None

        logo_box = tk.Label(header, bg="#1c283a")
        if self.logo_img:
            w = self.logo_img.width()
            h = self.logo_img.height()
            factor = max(1, int(max(w / 90, h / 90)))
            self.logo_small = self.logo_img.subsample(factor, factor)
            logo_box.configure(image=self.logo_small)
        else:
            logo_box.configure(text="LOGO", fg="white")
        logo_box.pack(side="left", padx=10, pady=10)

        title_box = tk.Frame(header, bg="#1c283a")
        title_box.pack(side="left", pady=10, padx=(0, 18))
        tk.Label(
            title_box,
            text="JULIANO",
            fg="white",
            bg="#1c283a",
            font=("Segoe UI", 16, "bold"),
        ).pack(anchor="w")
        tk.Label(
            title_box,
            text="AUTOMECÂNICA",
            fg="white",
            bg="#1c283a",
            font=("Segoe UI", 12),
        ).pack(anchor="w")

    def _nav_btn(self, text, frame_name):
        def on_click():
            self.show(frame_name)

        b = tk.Button(
            self.sidebar,
            text=text,
            command=on_click,
            bg="#243246",
            fg="white",
            activebackground="#2e415e",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=12,
            font=("Segoe UI", 11),
            anchor="w",
        )
        b.pack(fill="x")
        return b

    def _build_sidebar_buttons(self):
        tk.Frame(self.sidebar, height=10, bg="#243246").pack(fill="x")
        self._nav_btn("🏠  Orçamento", "ServicesFrame")
        self._nav_btn("👤  Clientes", "ClientsFrame")
        self._nav_btn("🔧  Ordem de Serviço", "OrdemServicoFrame")
        self._nav_btn("🧾  Notas Fiscais", "NotasFiscaisFrame")
        self._nav_btn("💰  Financeiro", "FinanceFrame")

        tk.Frame(self.sidebar, bg="#243246").pack(fill="both", expand=True)

        cfg = tk.Button(
            self.sidebar,
           # text="⚙  Configurações (em breve)",  
            bg="#243246",
            fg="#cfd6df",
            activebackground="#2e415e",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=12,
            font=("Segoe UI", 10),
            anchor="w",
            command=lambda: messagebox.showinfo(
                "Configurações", "Ainda vamos criar essa parte 🙂"
            ),
        )
        cfg.pack(fill="x", pady=8)

    def show(self, frame_name):
        frame = self.frames[frame_name]
        frame.tkraise()
        self.atualizar_total_clientes()
        if hasattr(frame, "refresh"):
            frame.refresh()

    def atualizar_total_clientes(self):
        try:
            con = db()
            cur = con.cursor()
            cur.execute("SELECT COUNT(*) FROM clients")
            total = cur.fetchone()[0] or 0
            con.close()
            self.total_clientes_var.set(str(total))
        except Exception:
            self.total_clientes_var.set("0")


    def _maiusculo_placa(self, *args):
        texto = self.placa_var.get()
        texto_maiusculo = texto.upper()

        if texto != texto_maiusculo:
            self.placa_var.set(texto_maiusculo)

class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        tk.Label(
            self,
            text="ORÇAMENTO",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")
        self.recent_box = tk.LabelFrame(
            self,
            text="Ordens recentes (últimas 10)",
            bg="#f5f6f8",
            fg="#374151",
            font=("Segoe UI", 10, "bold"),
        )
        self.recent_box.pack(fill="both", expand=True, pady=16)

        cols = ("id", "cliente", "data", "status", "total")
        self.tree = ttk.Treeview(self.recent_box, columns=cols, show="headings", height=10)
        for c, t, w in [
            ("id", "OS", 80),
            ("cliente", "Cliente", 240),
            ("data", "Data", 120),
            ("status", "Status", 140),
            ("total", "Total", 120),
        ]:
            
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        btns = tk.Frame(self.recent_box, bg="#f5f6f8")
        btns.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(btns, text="Ver todas", command=lambda: app.show("OrdersFrame")).pack(
            side="right"
        )


    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT o.id, COALESCE(c.name,'(sem cliente)'), o.date, o.status, o.total
            FROM orders o
            LEFT JOIN clients c ON c.id = o.client_id
            ORDER BY o.id DESC
            LIMIT 10
            """
        )
        for row in cur.fetchall():
            self.tree.insert(
                "",
                "end",
                values=(row[0], row[1], row[2], row[3], f"R$ {row[4]:.2f}".replace(".", ",")),
            )
        con.close()

class ClientsFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app
        self.cliente_carregado_id = None
        self.dados_originais_cliente = None
        self.veiculos_originais = []
        self._editor_veiculo = None
        self.veiculos_ids = {}

        main_card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            width=900,
            height=520,
        )
        main_card.pack(anchor="w", padx=10, pady=(0, 14))
        main_card.pack_propagate(False)

        # =========================
        # DADOS DO CLIENTE
        # =========================
        tk.Label(
            main_card,
            text="👤  DADOS DO CLIENTE",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=22, pady=(16, 10))

        form = tk.Frame(main_card, bg="white")
        form.pack(fill="x", padx=22)

        self.cpf_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.telefone_var = tk.StringVar()
        self.cidade_var = tk.StringVar()
        self.endereco_var = tk.StringVar()
        self.bairro_var = tk.StringVar()
        self.cep_var = tk.StringVar()
        self.numero_var = tk.StringVar()

        self.cpf_var.trace_add("write", self._limitar_cpf)
        self.telefone_var.trace_add("write", self._limitar_telefone)
        self.cep_var.trace_add("write", self._limitar_cep)

        for var in (
            self.nome_var,
            self.cidade_var,
            self.endereco_var,
            self.bairro_var,
            self.numero_var,
        ):
            var.trace_add("write", lambda *args, v=var: self._maiusculo_var(v))

        self._campo(form, "CPF:", self.cpf_var, 0, 0, width=27)
        self._campo(form, "Nome:", self.nome_var, 0, 1, width=38)
        self._campo(form, "Telefone:", self.telefone_var, 0, 2, width=27)
        self._campo(form, "CEP:", self.cep_var, 0, 3, width=14)

        self._campo(form, "Cidade:", self.cidade_var, 1, 0, width=27)
        self._campo(form, "Endereço:", self.endereco_var, 1, 1, width=38)
        self._campo(form, "Bairro:", self.bairro_var, 1, 2, width=27)
        self._campo(form, "Número:", self.numero_var, 1, 3, width=14)

        separador = tk.Frame(main_card, bg="#e5e7eb", height=1)
        separador.pack(fill="x", padx=22, pady=(0, 7))

        # =========================
        # VEÍCULOS DO CLIENTE
        # =========================
        tk.Label(
            main_card,
            text="🚗  VEÍCULOS DO CLIENTE",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=22, pady=(0, 10))

        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "ClientesVeiculos.Treeview",
            background="white",
            foreground="#111827",
            fieldbackground="white",
            rowheight=32,
            bordercolor="#9ca3af",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        style.configure(
            "ClientesVeiculos.Treeview.Heading",
            background="#f3f4f6",
            foreground="#111827",
            bordercolor="#9ca3af",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "ClientesVeiculos.Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#111827")],
        )

        tabela_frame = tk.Frame(
            main_card,
            bg="white",
            highlightbackground="#9ca3af",
            highlightthickness=1,
        )
        tabela_frame.pack(fill="x", padx=22)

        cols = ("placa", "veiculo", "cor", "ano", "km", "acao")
        self.veiculos_tree = ttk.Treeview(
            tabela_frame,
            columns=cols,
            show="headings",
            height=4,
            style="ClientesVeiculos.Treeview",
        )

        colunas = [
            ("placa", "Placa", 130),
            ("veiculo", "Veículo", 190),
            ("cor", "Cor", 120),
            ("ano", "Ano", 100),
            ("km", "Quilometragem", 160),
            ("acao", "", 55),
        ]

        for col, titulo, largura in colunas:
            self.veiculos_tree.heading(col, text=titulo, anchor="center" if col == "acao" else "w")
            self.veiculos_tree.column(col, width=largura, anchor="center" if col == "acao" else "w", stretch=False if col == "acao" else True)

        scrollbar_veiculos = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.veiculos_tree.yview,
        )
        self.veiculos_tree.configure(yscrollcommand=scrollbar_veiculos.set)

        self.veiculos_tree.pack(side="left", fill="x", expand=True)
        scrollbar_veiculos.pack(side="right", fill="y")

        self.veiculos_tree.tag_configure("linha_par", background="#ffffff")
        self.veiculos_tree.tag_configure("linha_impar", background="#f3f4f6")
        self.veiculos_tree.tag_configure("linha_vazia", background="#ffffff")

        self._limpar_tabela_veiculos()
        self.veiculos_tree.bind("<Double-1>", self.editar_celula_veiculo)
        self.veiculos_tree.bind("<ButtonRelease-1>", self.excluir_veiculo_da_tabela)

        botoes_veiculo = tk.Frame(main_card, bg="white")
        botoes_veiculo.pack(anchor="w", padx=22, pady=(12, 0))

        tk.Button(
            botoes_veiculo,
            text="▣  Adicionar Cliente",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.add_client,
        ).pack(side="left", padx=(0, 22))

        tk.Button(
            botoes_veiculo,
            text="🔎  Buscar Cliente",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.open_search_client_dialog,
        ).pack(side="left", padx=(0, 22))

        tk.Button(
            botoes_veiculo,
            text="🗑  Excluir Cliente",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.open_delete_client_search,
        ).pack(side="left", padx=(0, 22))

        tk.Button(
            botoes_veiculo,
            text="🧹  Limpar Cliente",
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.limpar_tela_cliente,
        ).pack(side="left")

    def _limpar_tabela_veiculos(self):
        self.veiculos_ids = {}

        for item in self.veiculos_tree.get_children():
            self.veiculos_tree.delete(item)

        self._preencher_linhas_vazias_veiculo()
        self._atualizar_linhas_tabela_veiculos()

    def _preencher_linhas_vazias_veiculo(self, minimo_linhas=4):
        while len(self.veiculos_tree.get_children()) < minimo_linhas:
            self.veiculos_tree.insert("", "end", values=("", "", "", "", "", ""), tags=("linha_vazia",))

    def _atualizar_linhas_tabela_veiculos(self):
        indice_dados = 0

        for item in self.veiculos_tree.get_children():
            valores = list(self.veiculos_tree.item(item, "values"))

            while len(valores) < 6:
                valores.append("")

            if self._linha_veiculo_tem_dados(valores):
                tag = "linha_par" if indice_dados % 2 == 0 else "linha_impar"
                indice_dados += 1
            else:
                tag = "linha_vazia"

            self.veiculos_tree.item(item, tags=(tag,))

    def _linha_veiculo_tem_dados(self, valores):
        valores = list(valores)
        dados = valores[:5]
        return any(str(valor).strip() for valor in dados)

    def _garantir_linha_vazia_veiculo(self):
        tem_linha_vazia = False

        for item in self.veiculos_tree.get_children():
            valores = list(self.veiculos_tree.item(item, "values"))

            while len(valores) < 6:
                valores.append("")

            if not self._linha_veiculo_tem_dados(valores):
                tem_linha_vazia = True
                break

        if not tem_linha_vazia:
            self.veiculos_tree.insert("", "end", values=("", "", "", "", "", ""), tags=("linha_vazia",))

        self._preencher_linhas_vazias_veiculo()
        self._atualizar_linhas_tabela_veiculos()

    def excluir_veiculo_da_tabela(self, event):
        item = self.veiculos_tree.identify_row(event.y)
        coluna = self.veiculos_tree.identify_column(event.x)

        # A coluna #6 é a coluna da lixeira.
        if not item or coluna != "#6":
            return

        valores = list(self.veiculos_tree.item(item, "values"))

        if not self._linha_veiculo_tem_dados(valores):
            return

        placa = str(valores[0]).strip() if len(valores) > 0 else ""
        veiculo = str(valores[1]).strip() if len(valores) > 1 else ""
        veiculo_id = self.veiculos_ids.get(item)

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este veículo?\n\n"
            f"Placa: {placa or '-'}\n"
            f"Veículo: {veiculo or '-'}"
        )

        if not confirmar:
            return

        # Se o veículo já existe no banco, exclui definitivamente.
        # Se for uma linha nova ainda não salva, remove apenas da tela.
        if veiculo_id:
            try:
                con = db()
                cur = con.cursor()
                cur.execute(
                    "DELETE FROM vehicles WHERE id = ? AND client_id = ?",
                    (veiculo_id, self.cliente_carregado_id),
                )
                con.commit()
                con.close()
            except Exception as e:
                messagebox.showerror(
                    "Erro",
                    f"Não foi possível excluir o veículo do banco de dados:\n{e}"
                )
                return

        self.veiculos_ids.pop(item, None)
        self.veiculos_tree.delete(item)
        self._garantir_linha_vazia_veiculo()

    def editar_celula_veiculo(self, event):
        item = self.veiculos_tree.identify_row(event.y)
        coluna = self.veiculos_tree.identify_column(event.x)

        if not item or not coluna:
            return

        # Se já existir uma edição aberta, salva antes de abrir outra.
        self._finalizar_edicao_veiculo()

        bbox = self.veiculos_tree.bbox(item, coluna)
        if not bbox:
            return

        x, y, largura, altura = bbox
        valores = list(self.veiculos_tree.item(item, "values"))

        indice_coluna = int(coluna.replace("#", "")) - 1

        # A última coluna é apenas a ação de excluir, não deve ser editada.
        if indice_coluna == 5:
            return

        if indice_coluna < 0 or indice_coluna >= len(valores):
            return

        valor_atual = valores[indice_coluna]

        # Na coluna da placa, durante a digitação deixamos apenas letras/números
        # em maiúsculo. O formato com traço é aplicado somente ao finalizar
        # a edição, evitando que o cursor fique antes do traço.
        if indice_coluna == 0:
            valor_atual = self._normalizar_placa_digitacao(valor_atual)

        entrada_var = tk.StringVar(value=valor_atual)

        entrada = tk.Entry(self.veiculos_tree, textvariable=entrada_var)

        if indice_coluna == 0:
            ajustando_placa = {"ativo": False}

            def normalizar_placa_ao_digitar(*args):
                if ajustando_placa["ativo"]:
                    return

                texto_normalizado = self._normalizar_placa_digitacao(entrada_var.get())

                if entrada_var.get() != texto_normalizado:
                    ajustando_placa["ativo"] = True
                    entrada_var.set(texto_normalizado)
                    ajustando_placa["ativo"] = False
                    entrada.icursor(tk.END)

            entrada_var.trace_add("write", normalizar_placa_ao_digitar)

        elif indice_coluna in (1, 2):
            ajustando_texto = {"ativo": False}

            def deixar_maiusculo_ao_digitar(*args):
                if ajustando_texto["ativo"]:
                    return

                texto_atual = entrada_var.get()
                texto_maiusculo = texto_atual.upper()

                if texto_atual != texto_maiusculo:
                    posicao_cursor = entrada.index(tk.INSERT)
                    ajustando_texto["ativo"] = True
                    entrada_var.set(texto_maiusculo)
                    ajustando_texto["ativo"] = False
                    entrada.icursor(posicao_cursor)

            entrada_var.trace_add("write", deixar_maiusculo_ao_digitar)

            # Coluna 2 = Veículo
            # Ao apertar espaço pela primeira vez, troca por " - "
            if indice_coluna == 1:
                def substituir_espaco_por_traco(event=None):
                    texto_atual = entrada_var.get().strip().upper()

                    if texto_atual and " - " not in texto_atual:
                        entrada_var.set(texto_atual + " - ")
                        entrada.icursor(tk.END)
                        return "break"

                    return None

                entrada.bind("<space>", substituir_espaco_por_traco)

        entrada.place(x=x, y=y, width=largura, height=altura)
        entrada.focus_set()
        entrada.select_range(0, tk.END)

        self._editor_veiculo = {
            "entry": entrada,
            "entry_var": entrada_var,
            "item": item,
            "indice_coluna": indice_coluna,
        }

        entrada.bind("<Return>", lambda event: self._finalizar_edicao_veiculo())
        entrada.bind("<FocusOut>", lambda event: self._finalizar_edicao_veiculo())

    def _finalizar_edicao_veiculo(self):
        if not self._editor_veiculo:
            return

        entrada = self._editor_veiculo.get("entry")
        item = self._editor_veiculo.get("item")
        indice_coluna = self._editor_veiculo.get("indice_coluna")

        if not entrada or not entrada.winfo_exists():
            self._editor_veiculo = None
            return

        valores = list(self.veiculos_tree.item(item, "values"))

        while len(valores) < 6:
            valores.append("")

        novo_valor = entrada.get().strip().upper()

        if indice_coluna == 0:
            novo_valor = self._formatar_placa(novo_valor)

        if indice_coluna is not None and 0 <= indice_coluna < 5:
            valores[indice_coluna] = novo_valor

            if self._linha_veiculo_tem_dados(valores):
                valores[5] = "🗑"
            else:
                valores[5] = ""

            self.veiculos_tree.item(item, values=valores)

        self._garantir_linha_vazia_veiculo()
        self._atualizar_linhas_tabela_veiculos()

        entrada.destroy()
        self._editor_veiculo = None

    def _campo(self, parent, label, var, row, col, width=30):
        box = tk.Frame(parent, bg="white")
        box.grid(row=row, column=col, sticky="w", padx=(0, 28), pady=(0, 14))

        tk.Label(
            box,
            text=label,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 10),
        ).pack(anchor="w")

        entry = tk.Entry(
            box,
            textvariable=var,
            width=width,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        entry.pack(fill="x", pady=(4, 0), ipady=4)

        if label == "CPF:":
            self.cpf_entry = entry

    def _normalizar_cpf(self, valor):
        return "".join(ch for ch in str(valor or "") if ch.isdigit())

    def _normalizar_placa_digitacao(self, valor):
        return "".join(ch for ch in str(valor or "").upper() if ch.isalnum())[:7]

    def _formatar_placa(self, valor):
        texto = self._normalizar_placa_digitacao(valor)

        if len(texto) > 3:
            return f"{texto[:3]} - {texto[3:]}"

        return texto

    def _coletar_dados_cliente(self):
        return {
            "cpf": self._normalizar_cpf(self.cpf_var.get().strip()),
            "name": self.nome_var.get().strip(),
            "phone": self.telefone_var.get().strip(),
            "city": self.cidade_var.get().strip(),
            "address": self.endereco_var.get().strip(),
            "district": self.bairro_var.get().strip(),
            "cep": self.cep_var.get().strip(),
            "number": self.numero_var.get().strip(),
        }

    def _coletar_veiculos_tela(self):
        self._finalizar_edicao_veiculo()
        veiculos = []

        for item in self.veiculos_tree.get_children():
            valores = self.veiculos_tree.item(item, "values")

            placa = self._formatar_placa(valores[0]) if len(valores) > 0 else ""
            veiculo = str(valores[1]).strip().upper() if len(valores) > 1 else ""
            cor = str(valores[2]).strip().upper() if len(valores) > 2 else ""
            ano = str(valores[3]).strip() if len(valores) > 3 else ""
            km = str(valores[4]).strip() if len(valores) > 4 else ""

            if placa or veiculo or cor or ano or km:
                veiculos.append((placa, veiculo, cor, ano, km))

        return veiculos

    def _normalizar_placa_comparacao(self, valor):
        return "".join(ch for ch in str(valor or "").upper() if ch.isalnum())

    def _validar_placas_duplicadas(self, veiculos, cliente_id_ignorar=None):
        placas_digitadas = {}

        for placa, veiculo, cor, ano, km in veiculos:
            placa_normalizada = self._normalizar_placa_comparacao(placa)

            if not placa_normalizada:
                continue

            if placa_normalizada in placas_digitadas:
                messagebox.showwarning(
                    "Atenção",
                    f"A placa {self._formatar_placa(placa_normalizada)} foi digitada mais de uma vez na tabela."
                )
                return False

            placas_digitadas[placa_normalizada] = placa

        if not placas_digitadas:
            return True

        try:
            con = db()
            cur = con.cursor()

            for placa_normalizada in placas_digitadas:
                if cliente_id_ignorar:
                    cur.execute(
                        """
                        SELECT c.name
                        FROM vehicles v
                        LEFT JOIN clients c ON c.id = v.client_id
                        WHERE UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) = ?
                          AND v.client_id <> ?
                        LIMIT 1
                        """,
                        (placa_normalizada, cliente_id_ignorar),
                    )
                else:
                    cur.execute(
                        """
                        SELECT c.name
                        FROM vehicles v
                        LEFT JOIN clients c ON c.id = v.client_id
                        WHERE UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) = ?
                        LIMIT 1
                        """,
                        (placa_normalizada,),
                    )

                cliente = cur.fetchone()

                if cliente:
                    nome_cliente = cliente[0] or "outro cliente"
                    con.close()
                    messagebox.showwarning(
                        "Atenção",
                        f"A placa {self._formatar_placa(placa_normalizada)} já está cadastrada para {nome_cliente}."
                    )
                    return False

            con.close()
            return True

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível verificar placa duplicada:\n{e}"
            )
            return False

    def _limpar_campos_cliente(self):
        if hasattr(self, "cpf_entry"):
            self.cpf_entry.config(state="normal")

        self.cpf_var.set("")
        self.nome_var.set("")
        self.telefone_var.set("")
        self.cidade_var.set("")
        self.endereco_var.set("")
        self.bairro_var.set("")
        self.cep_var.set("")
        self.numero_var.set("")
        self.cliente_carregado_id = None
        self.dados_originais_cliente = None
        self.veiculos_originais = []

    def limpar_tela_cliente(self):
        self._limpar_campos_cliente()
        self._limpar_tabela_veiculos()

    def _limitar_cpf(self, *args):
        texto = "".join(ch for ch in self.cpf_var.get() if ch.isdigit())[:11]
        if self.cpf_var.get() != texto:
            self.cpf_var.set(texto)

    def _limitar_telefone(self, *args):
        texto = "".join(ch for ch in self.telefone_var.get() if ch.isdigit())[:11]
        if self.telefone_var.get() != texto:
            self.telefone_var.set(texto)

    def _limitar_cep(self, *args):
        texto = "".join(ch for ch in self.cep_var.get() if ch.isdigit())[:8]
        if self.cep_var.get() != texto:
            self.cep_var.set(texto)


    def _maiusculo_var(self, var):

        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def add_client(self):
        if self.cliente_carregado_id:
            self.atualizar_cliente_carregado()
            return

        dados = self._coletar_dados_cliente()

        if not dados["cpf"]:
            messagebox.showwarning("Atenção", "Informe o CPF do cliente.")
            return

        if len(dados["cpf"]) != 11:
            messagebox.showwarning("Atenção", "CPF deve conter 11 dígitos.")
            return

        if not dados["name"]:
            messagebox.showwarning("Atenção", "Informe o nome do cliente.")
            return

        veiculos_para_salvar = self._coletar_veiculos_tela()

        if not veiculos_para_salvar:
            messagebox.showwarning(
                "Atenção",
                "Informe pelo menos um veículo na tabela antes de adicionar o cliente."
            )
            return

        if not self._validar_placas_duplicadas(veiculos_para_salvar):
            return

        con = db()
        cur = con.cursor()

        cur.execute("SELECT name FROM clients WHERE cpf = ? LIMIT 1", (dados["cpf"],))
        cliente_cpf = cur.fetchone()
        if cliente_cpf:
            con.close()
            nome_cliente = cliente_cpf[0] or "outro cliente"
            messagebox.showwarning(
                "Atenção",
                f"Este CPF já está cadastrado para {nome_cliente}."
            )
            return

        if dados["phone"]:
            cur.execute("SELECT id FROM clients WHERE phone = ?", (dados["phone"],))
            if cur.fetchone():
                con.close()
                messagebox.showwarning("Atenção", "Este telefone já está cadastrado.")
                return

        try:
            cur.execute(
                """
                INSERT INTO clients (
                    cpf, name, phone, city, address, district, cep, number, created_at
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    dados["cpf"],
                    dados["name"],
                    dados["phone"],
                    dados["city"],
                    dados["address"],
                    dados["district"],
                    dados["cep"],
                    dados["number"],
                    datetime.now().isoformat(timespec="seconds"),
                ),
            )

            cliente_id = cur.lastrowid

            for placa, veiculo, cor, ano, km in veiculos_para_salvar:
                cur.execute(
                    """
                    INSERT INTO vehicles (
                        client_id, plate, vehicle, color, year, mileage, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        cliente_id,
                        placa,
                        veiculo,
                        cor,
                        ano,
                        km,
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )

            con.commit()

        except Exception as e:
            con.rollback()
            messagebox.showerror("Erro", f"Não foi possível salvar o cliente e veículo:\n{e}")
            return

        finally:
            con.close()

        self._limpar_campos_cliente()
        self._limpar_tabela_veiculos()
        self.app.atualizar_total_clientes()
        messagebox.showinfo("Sucesso", "Cliente e veículo cadastrados com sucesso.")

    def atualizar_cliente_carregado(self):
        dados = self._coletar_dados_cliente()
        veiculos_atuais = self._coletar_veiculos_tela()

        if not dados["cpf"]:
            messagebox.showwarning("Atenção", "Informe o CPF do cliente.")
            return

        if len(dados["cpf"]) != 11:
            messagebox.showwarning("Atenção", "CPF deve conter 11 dígitos.")
            return

        if not dados["name"]:
            messagebox.showwarning("Atenção", "Informe o nome do cliente.")
            return

        if not veiculos_atuais:
            messagebox.showwarning("Atenção", "Informe pelo menos um veículo na tabela.")
            return

        if not self._validar_placas_duplicadas(
            veiculos_atuais,
            cliente_id_ignorar=self.cliente_carregado_id
        ):
            return

        dados_comparacao = {
            "cpf": dados["cpf"],
            "name": dados["name"],
            "phone": dados["phone"],
            "city": dados["city"],
            "address": dados["address"],
            "district": dados["district"],
            "cep": dados["cep"],
            "number": dados["number"],
        }

        if (
            dados_comparacao == self.dados_originais_cliente
            and veiculos_atuais == self.veiculos_originais
        ):
            messagebox.showwarning("Atenção", "Cliente já cadastrado.")
            return

        con = db()
        cur = con.cursor()

        cur.execute(
            "SELECT name FROM clients WHERE cpf = ? AND id <> ? LIMIT 1",
            (dados["cpf"], self.cliente_carregado_id),
        )
        cliente_cpf = cur.fetchone()
        if cliente_cpf:
            con.close()
            nome_cliente = cliente_cpf[0] or "outro cliente"
            messagebox.showwarning(
                "Atenção",
                f"Este CPF já pertence a {nome_cliente}."
            )
            return

        if dados["phone"]:
            cur.execute(
                "SELECT id FROM clients WHERE phone = ? AND id <> ?",
                (dados["phone"], self.cliente_carregado_id),
            )
            if cur.fetchone():
                con.close()
                messagebox.showwarning("Atenção", "Este telefone já pertence a outro cliente.")
                return

        try:
            cur.execute(
                """
                UPDATE clients
                SET cpf = ?, name = ?, phone = ?, city = ?, address = ?, district = ?, cep = ?, number = ?
                WHERE id = ?
                """,
                (
                    dados["cpf"],
                    dados["name"],
                    dados["phone"],
                    dados["city"],
                    dados["address"],
                    dados["district"],
                    dados["cep"],
                    dados["number"],
                    self.cliente_carregado_id,
                ),
            )

            cur.execute(
                "DELETE FROM vehicles WHERE client_id = ?",
                (self.cliente_carregado_id,),
            )

            for placa, veiculo, cor, ano, km in veiculos_atuais:
                cur.execute(
                    """
                    INSERT INTO vehicles (
                        client_id, plate, vehicle, color, year, mileage, created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                    """,
                    (
                        self.cliente_carregado_id,
                        placa,
                        veiculo,
                        cor,
                        ano,
                        km,
                        datetime.now().isoformat(timespec="seconds"),
                    ),
                )

            con.commit()

        except Exception as e:
            con.rollback()
            messagebox.showerror("Erro", f"Não foi possível atualizar o cliente:\n{e}")
            return

        finally:
            con.close()

        self.dados_originais_cliente = dados_comparacao.copy()
        self.veiculos_originais = list(veiculos_atuais)
        messagebox.showinfo("Sucesso", "Dados do cliente atualizados com sucesso.")

    def open_edit_client_search(self):
        EditClientSearchDialog(self)

    def open_delete_client_search(self):
        DeleteClientSearchDialog(self)

    def open_search_client_dialog(self):
        SearchClientDialog(self)

    def carregar_cliente_na_tela(self, cliente_id):
        con = db()
        cur = con.cursor()

        cur.execute(
            """
            SELECT cpf, name, phone, city, address, district, cep, number
            FROM clients
            WHERE id = ?
            """,
            (cliente_id,),
        )
        cliente = cur.fetchone()

        cur.execute(
            """
            SELECT id, plate, vehicle, color, year, mileage
            FROM vehicles
            WHERE client_id = ?
            ORDER BY id
            """,
            (cliente_id,),
        )
        veiculos = cur.fetchall()

        con.close()

        if not cliente:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
            return

        if hasattr(self, "cpf_entry"):
            self.cpf_entry.config(state="normal")

        self.cpf_var.set(cliente[0] or "")
        self.nome_var.set(cliente[1] or "")
        self.telefone_var.set(cliente[2] or "")
        self.cidade_var.set(cliente[3] or "")
        self.endereco_var.set(cliente[4] or "")
        self.bairro_var.set(cliente[5] or "")
        self.cep_var.set(cliente[6] or "")
        self.numero_var.set(cliente[7] or "")

        self.veiculos_ids = {}

        for item in self.veiculos_tree.get_children():
            self.veiculos_tree.delete(item)

        for veiculo in veiculos:
            veiculo_id = veiculo[0]
            dados_veiculo = (
                self._formatar_placa(veiculo[1]),
                str(veiculo[2] or "").strip().upper(),
                str(veiculo[3] or "").strip().upper(),
                str(veiculo[4] or "").strip(),
                str(veiculo[5] or "").strip(),
            )
            item = self.veiculos_tree.insert("", "end", values=(*dados_veiculo, "🗑"), tags=("linha_par",))
            self.veiculos_ids[item] = veiculo_id

        self._garantir_linha_vazia_veiculo()
        self._atualizar_linhas_tabela_veiculos()

        self.cliente_carregado_id = cliente_id
        self.dados_originais_cliente = {
            "cpf": str(cliente[0] or "").strip(),
            "name": str(cliente[1] or "").strip(),
            "phone": str(cliente[2] or "").strip(),
            "city": str(cliente[3] or "").strip(),
            "address": str(cliente[4] or "").strip(),
            "district": str(cliente[5] or "").strip(),
            "cep": str(cliente[6] or "").strip(),
            "number": str(cliente[7] or "").strip(),
        }
        self.veiculos_originais = [
            (
                self._formatar_placa(v[1]),
                str(v[2] or "").strip().upper(),
                str(v[3] or "").strip().upper(),
                str(v[4] or "").strip(),
                str(v[5] or "").strip(),
            )
            for v in veiculos
        ]

        if hasattr(self, "cpf_entry"):
            self.cpf_entry.config(state="normal")

    def _acao_visual(self):
        messagebox.showinfo("Em breve", "Por enquanto esta tela é apenas visual.")

    def refresh(self):
        pass

class SearchClientDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Buscar Cliente")
        self.geometry("380x190")
        self.resizable(False, False)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        frame = tk.Frame(self, bg="#f5f6f8", padx=22, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Buscar Cliente por CPF, Placa ou Telefone:",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", lambda *args: self._maiusculo_busca())

        self.search_entry = tk.Entry(
            frame,
            textvariable=self.search_var,
            width=30,
            font=("Segoe UI", 10),
            justify="center"
        )
        self.search_entry.pack(pady=(0, 7), ipady=3)
        self.search_entry.focus_set()

        tk.Button(
            frame,
            text="Buscar",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.buscar_cliente
        ).pack()

        self.bind("<Return>", lambda event: self.buscar_cliente())

        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"+{x}+{y}")

    def _maiusculo_busca(self):
        texto = self.search_var.get()
        texto_formatado = []
        total_numeros = 0

        for caractere in texto.upper():
            if caractere.isdigit():
                if total_numeros < 11:
                    texto_formatado.append(caractere)
                    total_numeros += 1
            else:
                texto_formatado.append(caractere)

        texto_final = "".join(texto_formatado)

        if texto != texto_final:
            self.search_var.set(texto_final)
            self.search_entry.icursor(tk.END)

    def buscar_cliente(self):
        valor_original = self.search_var.get().strip()
        valor_numerico = "".join(ch for ch in valor_original if ch.isdigit())
        valor_placa = "".join(ch for ch in valor_original.upper() if ch.isalnum())

        if not valor_original:
            messagebox.showwarning("Atenção", "Digite o CPF, placa ou telefone do cliente.")
            return

        con = db()
        cur = con.cursor()

        cur.execute(
            """
            SELECT DISTINCT c.id
            FROM clients c
            LEFT JOIN vehicles v ON v.client_id = c.id
            WHERE c.cpf = ?
               OR c.phone = ?
               OR UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) LIKE ?
            ORDER BY c.name
            LIMIT 1
            """,
            (
                valor_numerico,
                valor_numerico,
                valor_placa,
            )
        )

        cliente = cur.fetchone()
        con.close()

        if not cliente:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
            return

        self.parent.carregar_cliente_na_tela(cliente[0])
        messagebox.showinfo("Sucesso", "Cliente carregado na tela.")
        self.destroy()    

class EditClientSearchDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Buscar Cliente")
        self.geometry("380x190")
        self.resizable(False, False)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        frame = tk.Frame(self, bg="#f5f6f8", padx=22, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Digite CPF, Placa ou Telefone do Cliente:",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._limitar_busca)

        self.search_entry = tk.Entry(
            frame,
            textvariable=self.search_var,
            width=30,
            font=("Segoe UI", 10),
            justify="center"
        )
        self.search_entry.pack(pady=(0, 7), ipady=3)
        self.search_entry.focus_set()

        tk.Button(
            frame,
            text="Buscar",
            command=self.buscar_cliente
        ).pack()

        self.bind("<Return>", lambda event: self.buscar_cliente())

        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"+{x}+{y}")

    def _limitar_busca(self, *args):
        texto = "".join(ch for ch in self.search_var.get() if ch.isdigit())[:11]
        if self.search_var.get() != texto:
            self.search_var.set(texto)

    def buscar_cliente(self):
        valor = "".join(ch for ch in self.search_var.get().strip() if ch.isdigit())

        if not valor:
            messagebox.showwarning("Atenção", "Digite CPF ou Telefone.")
            return

        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, cpf, name, phone, city, address, district, cep, number
            FROM clients
            WHERE cpf = ? OR phone = ?
            """,
            (valor, valor)
        )
        cliente = cur.fetchone()
        con.close()

        if not cliente:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
            return

        self.destroy()
        EditClientDataDialog(self.parent, cliente)


class EditClientDataDialog(tk.Toplevel):
    def __init__(self, parent, cliente):
        super().__init__(parent)
        self.parent = parent
        self.cliente_id = cliente[0]

        self.title("Editar Cliente")
        self.geometry("480x430")
        self.resizable(False, False)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        self.cpf_var = tk.StringVar(value=cliente[1] or "")
        self.nome_var = tk.StringVar(value=cliente[2] or "")
        self.telefone_var = tk.StringVar(value=cliente[3] or "")
        self.cidade_var = tk.StringVar(value=cliente[4] or "")
        self.endereco_var = tk.StringVar(value=cliente[5] or "")
        self.bairro_var = tk.StringVar(value=cliente[6] or "")
        self.cep_var = tk.StringVar(value=cliente[7] or "")
        self.numero_var = tk.StringVar(value=cliente[8] or "")

        self.cpf_var.trace_add("write", self._limitar_cpf)
        self.telefone_var.trace_add("write", self._limitar_telefone)
        self.cep_var.trace_add("write", self._limitar_cep)

        for var in (
            self.nome_var,
            self.cidade_var,
            self.endereco_var,
            self.bairro_var,
            self.numero_var,
        ):
            var.trace_add("write", lambda *args, v=var: self._maiusculo_var(v))

        frame = tk.Frame(self, bg="#f5f6f8", padx=20, pady=18)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Editar dados do cliente",
            bg="#f5f6f8",
            fg="#0f172a",
            font=("Segoe UI", 13, "bold")
        ).grid(row=0, column=0, columnspan=2, pady=(0, 7))

        campos = [
            ("CPF:", self.cpf_var),
            ("Nome:", self.nome_var),
            ("Telefone:", self.telefone_var),
            ("Cidade:", self.cidade_var),
            ("Endereço:", self.endereco_var),
            ("Bairro:", self.bairro_var),
            ("CEP:", self.cep_var),
            ("Número:", self.numero_var),
        ]

        for i, (label, var) in enumerate(campos, start=1):
            tk.Label(
                frame,
                text=label,
                bg="#f5f6f8",
                font=("Segoe UI", 10, "bold")
            ).grid(row=i, column=0, sticky="w", pady=6)

            tk.Entry(
                frame,
                textvariable=var,
                width=34,
                font=("Segoe UI", 10)
            ).grid(row=i, column=1, padx=(12, 0), pady=6, ipady=3)

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.grid(row=len(campos) + 1, column=0, columnspan=2, pady=(18, 0))

        tk.Button(
            botoes,
            text="Salvar Alterações",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=5,
            bd=0,
            command=self.salvar_alteracoes
        ).pack(side="left", padx=6)

        tk.Button(
            botoes,
            text="Cancelar",
            command=self.destroy
        ).pack(side="left", padx=6)

        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"+{x}+{y}")

    def _limitar_cpf(self, *args):
        texto = "".join(ch for ch in self.cpf_var.get() if ch.isdigit())[:11]
        if self.cpf_var.get() != texto:
            self.cpf_var.set(texto)

    def _limitar_telefone(self, *args):
        texto = "".join(ch for ch in self.telefone_var.get() if ch.isdigit())[:11]
        if self.telefone_var.get() != texto:
            self.telefone_var.set(texto)

    def _limitar_cep(self, *args):
        texto = "".join(ch for ch in self.cep_var.get() if ch.isdigit())[:8]
        if self.cep_var.get() != texto:
            self.cep_var.set(texto)

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def salvar_alteracoes(self):
        cpf = "".join(ch for ch in self.cpf_var.get().strip() if ch.isdigit())
        nome = self.nome_var.get().strip()
        telefone = "".join(ch for ch in self.telefone_var.get().strip() if ch.isdigit())
        cidade = self.cidade_var.get().strip()
        endereco = self.endereco_var.get().strip()
        bairro = self.bairro_var.get().strip()
        cep = "".join(ch for ch in self.cep_var.get().strip() if ch.isdigit())
        numero = self.numero_var.get().strip()

        if not cpf:
            messagebox.showwarning("Atenção", "Informe o CPF.")
            return

        if len(cpf) != 11:
            messagebox.showwarning("Atenção", "CPF deve conter 11 dígitos.")
            return

        if telefone and len(telefone) != 11:
            messagebox.showwarning("Atenção", "Telefone deve conter 11 dígitos.")
            return

        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome.")
            return

        con = db()
        cur = con.cursor()

        cur.execute(
            "SELECT id FROM clients WHERE cpf = ? AND id <> ?",
            (cpf, self.cliente_id)
        )
        if cur.fetchone():
            con.close()
            messagebox.showwarning("Atenção", "Este CPF já pertence a outro cliente.")
            return

        if telefone:
            cur.execute(
                "SELECT id FROM clients WHERE phone = ? AND id <> ?",
                (telefone, self.cliente_id)
            )
            if cur.fetchone():
                con.close()
                messagebox.showwarning("Atenção", "Este telefone já pertence a outro cliente.")
                return

        cur.execute(
            """
            UPDATE clients
            SET cpf = ?, name = ?, phone = ?, city = ?, address = ?, district = ?, cep = ?, number = ?
            WHERE id = ?
            """,
            (
                cpf,
                nome,
                telefone,
                cidade,
                endereco,
                bairro,
                cep,
                numero,
                self.cliente_id,
            )
        )

        con.commit()
        con.close()

        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
        self.destroy()


class DeleteClientSearchDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Excluir Cliente")
        self.geometry("380x200")
        self.resizable(False, False)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        frame = tk.Frame(self, bg="#f5f6f8", padx=22, pady=20)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Digite CPF, Placa ou Telefone do Cliente:",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 10, "bold")
        ).pack(pady=(0, 10))

        self.search_var = tk.StringVar()
        self.search_var.trace_add("write", self._limitar_busca)

        self.search_entry = tk.Entry(
            frame,
            textvariable=self.search_var,
            width=30,
            font=("Segoe UI", 10),
            justify="center"
        )
        self.search_entry.pack(pady=(0, 7), ipady=3)
        self.search_entry.focus_set()

        tk.Button(
            frame,
            text="Buscar",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=5,
            font=("Segoe UI", 10, "bold"),
            command=self.buscar_cliente
        ).pack()

        self.bind("<Return>", lambda event: self.buscar_cliente())

        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"+{x}+{y}")

    def _limitar_busca(self, *args):
        texto = "".join(ch for ch in self.search_var.get().upper() if ch.isalnum())[:11]

        if self.search_var.get() != texto:
            self.search_var.set(texto)

    def buscar_cliente(self):
        valor_original = self.search_var.get().strip().upper()
        valor_numerico = "".join(ch for ch in valor_original if ch.isdigit())
        valor_placa = "".join(ch for ch in valor_original if ch.isalnum())

        if not valor_original:
            messagebox.showwarning("Atenção", "Digite CPF, placa ou telefone do cliente.")
            return

        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT DISTINCT c.id, c.cpf, c.name, c.phone, c.city, c.address, c.district
            FROM clients c
            LEFT JOIN vehicles v ON v.client_id = c.id
            WHERE c.cpf = ?
               OR c.phone = ?
               OR UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) LIKE ?
            ORDER BY c.name
            LIMIT 1
            """,
            (valor_numerico, valor_numerico, valor_placa + '%')
        )
        cliente = cur.fetchone()
        con.close()

        if not cliente:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
            return

        cliente_id, cpf, nome, telefone, cidade, endereco, bairro = cliente

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir este cliente?\n\n"
            f"Nome: {nome or '-'}\n"
            f"CPF: {cpf or '-'}\n"
            f"Telefone: {telefone or '-'}"
        )

        if not confirmar:
            return

        con = db()
        cur = con.cursor()

        # Primeiro exclui os veículos vinculados ao cliente.
        # Isso evita que placas antigas fiquem "órfãs" no banco
        # e continuem bloqueando novos cadastros.
        cur.execute("DELETE FROM vehicles WHERE client_id = ?", (cliente_id,))

        # Depois exclui o cliente.
        cur.execute("DELETE FROM clients WHERE id = ?", (cliente_id,))

        con.commit()
        con.close()

        self.parent.app.atualizar_total_clientes()
        messagebox.showinfo("Sucesso", "Cliente excluído com sucesso.")
        self.destroy()


class AddClientDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent

        self.title("Adicionar Cliente")
        self.configure(bg="#f5f6f8")
        self.resizable(False, False)
        self.grab_set()

        self.cpf_var = tk.StringVar()
        self.nome_var = tk.StringVar()
        self.cidade_var = tk.StringVar()
        self.endereco_var = tk.StringVar()
        self.placa_var = tk.StringVar()
        self.placa_var.trace_add("write", self._maiusculo_placa)
        self.veiculo_var = tk.StringVar()
        self.telefone_var = tk.StringVar()
        self.cor_var = tk.StringVar()
        self.bairro_var = tk.StringVar()
        self.ano_var = tk.StringVar()
        self.km_var = tk.StringVar()

        self.cpf_var.trace_add("write", self._limitar_cpf)
        self.telefone_var.trace_add("write", self._limitar_telefone)
        self.placa_var.trace_add("write", self._limitar_placa)

        self.nome_var.trace_add("write", lambda *args: self._maiusculo_var(self.nome_var))
        self.cidade_var.trace_add("write", lambda *args: self._maiusculo_var(self.cidade_var))
        self.endereco_var.trace_add("write", lambda *args: self._maiusculo_var(self.endereco_var))
        self.placa_var.trace_add("write", lambda *args: self._maiusculo_var(self.placa_var))
        self.veiculo_var.trace_add("write", lambda *args: self._maiusculo_var(self.veiculo_var))
        self.cor_var.trace_add("write", lambda *args: self._maiusculo_var(self.cor_var))
        self.bairro_var.trace_add("write", lambda *args: self._maiusculo_var(self.bairro_var))

        frame = tk.Frame(self, bg="#f5f6f8", padx=15, pady=15)
        frame.pack(fill="both", expand=True)

        campos = [
            ("CPF:", self.cpf_var),
            ("Nome:", self.nome_var),
            ("Cidade:", self.cidade_var),
            ("Endereço:", self.endereco_var),
            ("Placa:", self.placa_var),
            ("Veículo:", self.veiculo_var),
            ("Telefone:", self.telefone_var),
            ("Cor:", self.cor_var),
            ("Bairro:", self.bairro_var),
            ("Ano:", self.ano_var),
            ("Quilometragem:", self.km_var),
        ]

        for i, (label, var) in enumerate(campos):
            tk.Label(frame, text=label, bg="#f5f6f8").grid(row=i, column=0, sticky="w", pady=4)

            if label == "Placa:":
                self.placa_entry = tk.Entry(frame, textvariable=var, width=35)
                self.placa_entry.grid(row=i, column=1, pady=4, padx=(10, 0))
            else:
                tk.Entry(frame, textvariable=var, width=35).grid(row=i, column=1, pady=4, padx=(10, 0))

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.grid(row=len(campos), column=0, columnspan=2, pady=(15, 0))

        tk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        tk.Button(botoes, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

    def _limitar_placa(self, *args):
        texto = self.placa_var.get().upper()
        texto_limpo = "".join(ch for ch in texto if ch.isalnum())[:7]

        if self.placa_var.get() != texto_limpo:
            self.placa_var.set(texto_limpo)
            self.after(1, lambda: self.placa_entry.icursor(tk.END))

    def _limitar_cpf(self, *args):
        texto = "".join(ch for ch in self.cpf_var.get() if ch.isdigit())[:11]
        if self.cpf_var.get() != texto:
            self.cpf_var.set(texto)

    def _limitar_telefone(self, *args):
        texto = "".join(ch for ch in self.telefone_var.get() if ch.isdigit())[:11]
        if self.telefone_var.get() != texto:
            self.telefone_var.set(texto)

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def salvar(self):
        dados = {
            "cpf": self.cpf_var.get().strip(),
            "name": self.nome_var.get().strip(),
            "city": self.cidade_var.get().strip(),
            "address": self.endereco_var.get().strip(),
            "plate": self.placa_var.get().strip().upper(),
            "vehicle": self.veiculo_var.get().strip(),
            "phone": self.telefone_var.get().strip(),
            "color": self.cor_var.get().strip(),
            "district": self.bairro_var.get().strip(),
            "year": self.ano_var.get().strip(),
            "mileage": self.km_var.get().strip(),
        }

        if not dados["cpf"] or not dados["name"]:
            messagebox.showwarning("Atenção", "CPF e Nome são obrigatórios!")
            return
        
          # validação de tamanho do CPF
        if len(dados["cpf"]) < 11:
            messagebox.showwarning("Atenção", "CPF deve conter 11 dígitos.")
            return

        cpf_normalizado = self.parent._normalizar_cpf(dados["cpf"])
        placa_normalizada = self.parent._normalizar_placa(dados["plate"])

        con = db()
        cur = con.cursor()

        if cpf_normalizado:
            cur.execute("SELECT cpf FROM clients")
            for (cpf_existente,) in cur.fetchall():
                if self.parent._normalizar_cpf(cpf_existente) == cpf_normalizado:
                    con.close()
                    messagebox.showwarning("Atenção", "Este CPF já está cadastrado.")
                    return

        if placa_normalizada:
            cur.execute("SELECT plate FROM clients")
            for (placa_existente,) in cur.fetchall():
                if self.parent._normalizar_placa(placa_existente) == placa_normalizada:
                    con.close()
                    messagebox.showwarning("Atenção", "Esta PLACA já está cadastrada.")
                    return

        cur.execute(
            """
            INSERT INTO clients (
                cpf, name, city, address, plate, vehicle,
                phone, color, district, year, mileage, created_at
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cpf_normalizado or dados["cpf"],
                dados["name"],
                dados["city"],
                dados["address"],
                placa_normalizada or dados["plate"],
                dados["vehicle"],
                dados["phone"],
                dados["color"],
                dados["district"],
                dados["year"],
                dados["mileage"],
                datetime.now().isoformat(timespec="seconds"),
            ),
        )

        con.commit()
        new_id = cur.lastrowid
        con.close()

        self.parent._carregar_cliente_por_id(new_id)
        self.parent.q_var.set("")
        self.parent.sugestoes.delete(0, tk.END)
        self.parent.sugestoes.pack_forget()

        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")
        self.destroy()            
 
class EditClientDialog(tk.Toplevel):
    def __init__(self, parent, client_id, row):
        super().__init__(parent)
        self.parent = parent
        self.client_id = client_id
        self.title("Editar Cliente")
        self.configure(bg="#f5f6f8")
        self.resizable(False, False)
        self.grab_set()

        self.cpf_var = tk.StringVar(value=row[0] or "")
        self.nome_var = tk.StringVar(value=row[1] or "")
        self.cidade_var = tk.StringVar(value=row[2] or "")
        self.endereco_var = tk.StringVar(value=row[3] or "")
        self.placa_var = tk.StringVar(value=row[4] or "")
        self.veiculo_var = tk.StringVar(value=row[5] or "")
        self.telefone_var = tk.StringVar(value=row[6] or "")
        self.cor_var = tk.StringVar(value=row[7] or "")
        self.bairro_var = tk.StringVar(value=row[8] or "")
        self.ano_var = tk.StringVar(value=row[9] or "")
        self.km_var = tk.StringVar(value=row[10] or "")

        self.cpf_var.trace_add("write", self._limitar_cpf)
        self.telefone_var.trace_add("write", self._limitar_telefone)
        self.placa_var.trace_add("write", self._limitar_placa)
        self.nome_var.trace_add("write", lambda *args: self._maiusculo_var(self.nome_var))
        self.cidade_var.trace_add("write", lambda *args: self._maiusculo_var(self.cidade_var))
        self.endereco_var.trace_add("write", lambda *args: self._maiusculo_var(self.endereco_var))
        self.placa_var.trace_add("write", lambda *args: self._maiusculo_var(self.placa_var))
        self.veiculo_var.trace_add("write", lambda *args: self._maiusculo_var(self.veiculo_var))
        self.cor_var.trace_add("write", lambda *args: self._maiusculo_var(self.cor_var))
        self.bairro_var.trace_add("write", lambda *args: self._maiusculo_var(self.bairro_var))

        frame = tk.Frame(self, bg="#f5f6f8", padx=15, pady=15)
        frame.pack(fill="both", expand=True)

        campos = [
            ("CPF:", self.cpf_var),
            ("Nome:", self.nome_var),
            ("Cidade:", self.cidade_var),
            ("Endereço:", self.endereco_var),
            ("Placa:", self.placa_var),
            ("Veículo:", self.veiculo_var),
            ("Telefone:", self.telefone_var),
            ("Cor:", self.cor_var),
            ("Bairro:", self.bairro_var),
            ("Ano:", self.ano_var),
            ("Quilometragem:", self.km_var),
        ]

        for i, (label, var) in enumerate(campos):
            tk.Label(frame, text=label, bg="#f5f6f8").grid(row=i, column=0, sticky="w", pady=4)

            if label == "Placa:":
                self.placa_entry = tk.Entry(frame, textvariable=var, width=35)
                self.placa_entry.grid(row=i, column=1, pady=4, padx=(10, 0))
            else:
                tk.Entry(frame, textvariable=var, width=35).grid(row=i, column=1, pady=4, padx=(10, 0))

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.grid(row=len(campos), column=0, columnspan=2, pady=(15, 0))

        tk.Button(botoes, text="Salvar", command=self.salvar).pack(side="left", padx=5)
        tk.Button(botoes, text="Cancelar", command=self.destroy).pack(side="left", padx=5)

    def _limitar_cpf(self, *args):
        texto = "".join(ch for ch in self.cpf_var.get() if ch.isdigit())[:11]
        if self.cpf_var.get() != texto:
            self.cpf_var.set(texto)

    def _limitar_telefone(self, *args):
        texto = "".join(ch for ch in self.telefone_var.get() if ch.isdigit())[:11]
        if self.telefone_var.get() != texto:
            self.telefone_var.set(texto)

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def _limitar_placa(self, *args):
        texto = self.placa_var.get().upper()
        texto_limpo = "".join(ch for ch in texto if ch.isalnum())[:7]

        if self.placa_var.get() != texto_limpo:
            self.placa_var.set(texto_limpo)
            self.after(1, lambda: self.placa_entry.icursor(tk.END))

    def salvar(self):
        dados = {
            "cpf": self.cpf_var.get().strip(),
            "name": self.nome_var.get().strip(),
            "city": self.cidade_var.get().strip(),
            "address": self.endereco_var.get().strip(),
            "plate": self.placa_var.get().strip().upper(),
            "vehicle": self.veiculo_var.get().strip(),
            "phone": self.telefone_var.get().strip(),
            "color": self.cor_var.get().strip(),
            "district": self.bairro_var.get().strip(),
            "year": self.ano_var.get().strip(),
            "mileage": self.km_var.get().strip(),
        }

        if not dados["cpf"] or not dados["name"]:
            messagebox.showwarning("Atenção", "CPF e Nome são obrigatórios!")
            return

        cpf_normalizado = self.parent._normalizar_cpf(dados["cpf"])
        placa_normalizada = self.parent._normalizar_placa(dados["plate"])

        con = db()
        cur = con.cursor()

        if cpf_normalizado:
            cur.execute("SELECT id, cpf FROM clients WHERE id <> ?", (self.client_id,))
            for client_id, cpf_existente in cur.fetchall():
                if self.parent._normalizar_cpf(cpf_existente) == cpf_normalizado:
                    con.close()
                    messagebox.showwarning("Atenção", "Este CPF já está cadastrado em outro cliente.")
                    return

        if placa_normalizada:
            cur.execute("SELECT id, plate FROM clients WHERE id <> ?", (self.client_id,))
            for client_id, placa_existente in cur.fetchall():
                if self.parent._normalizar_placa(placa_existente) == placa_normalizada:
                    con.close()
                    messagebox.showwarning("Atenção", "Esta PLACA já está cadastrada em outro cliente.")
                    return

        cur.execute(
            """
            UPDATE clients
            SET cpf=?, name=?, city=?, address=?, plate=?, vehicle=?,
                phone=?, color=?, district=?, year=?, mileage=?
            WHERE id=?
            """,
            (
                cpf_normalizado or dados["cpf"],
                dados["name"],
                dados["city"],
                dados["address"],
                placa_normalizada or dados["plate"],
                dados["vehicle"],
                dados["phone"],
                dados["color"],
                dados["district"],
                dados["year"],
                dados["mileage"],
                self.client_id,
            ),
        )

        con.commit()
        con.close()

        self.parent._carregar_cliente_por_id(self.client_id)
        self.parent.q_var.set("")
        self.parent.sugestoes.delete(0, tk.END)
        self.parent.sugestoes.pack_forget()

        messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso.")
        self.destroy()

class OrcamentoPreview(tk.Toplevel):
    def __init__(
        self,
        parent,
        caminho_imagem,
        nome_cliente="",
        telefone="",
        veiculo="",
        placa="",
        mao_de_obra="R$ 0,00",
        total_pecas="R$ 0,00",
        total_servicos="R$ 0,00",
        itens=None,
    ):
        super().__init__(parent)

        self.title("Pré-visualização do Orçamento")
        self.geometry("900x700")
        self.configure(bg="#f5f6f8")
        self.transient(parent)
        self.grab_set()

        self.caminho_imagem = caminho_imagem
        self.nome_cliente = nome_cliente
        self.telefone = telefone
        self.img_tk = None
        self.veiculo = veiculo
        self.placa = placa
        self.mao_de_obra = mao_de_obra
        self.total_pecas = total_pecas
        self.total_servicos = total_servicos
        self.itens = itens or []

        self.update_idletasks()
        largura = 900
        altura = 700
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")

        topo = tk.Frame(self, bg="#f5f6f8")
        topo.pack(fill="x", padx=15, pady=(15, 10))

        tk.Label(
            topo,
            text="Pré-visualização do Orçamento",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left")

        botoes = tk.Frame(self, bg="#f5f6f8")
        botoes.pack(fill="x", padx=15, pady=(0, 10))

        tk.Button(
            botoes,
            text="Enviar para Cliente",
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=5,
            bd=0,
            command=self.enviar_para_cliente
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            botoes,
            text="Imprimir",
            bg="#2563eb",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=5,
            bd=0,
            command=self.imprimir_orcamento
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            botoes,
            text="Fechar",
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            padx=14,
            pady=5,
            bd=0,
            command=self.destroy
        ).pack(side="left")

        frame_preview = tk.Frame(self, bg="#dbe1e8")
        frame_preview.pack(fill="both", expand=True, padx=15, pady=(0, 15))

        self.canvas = tk.Canvas(frame_preview, bg="#cfd6df", highlightthickness=0)
        scrollbar_y = ttk.Scrollbar(frame_preview, orient="vertical", command=self.canvas.yview)

        self.area_interna = tk.Frame(self.canvas, bg="#cfd6df")
        self.area_interna.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")),
        )

        self.canvas.create_window((0, 0), window=self.area_interna, anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar_y.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")

        self.mostrar_imagem()

    def salvar_orcamento_enviado(self):
        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO orcamentos_enviados (
                    cliente_nome,
                    telefone,
                    veiculo,
                    caminho_imagem,
                    mao_de_obra,
                    total_pecas,
                    total_servicos,
                    data_criacao,
                    status_envio
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.nome_cliente,
                    self.telefone,
                    self.veiculo,
                    self.caminho_imagem,
                    self.mao_de_obra,
                    self.total_pecas,
                    self.total_servicos,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "ENVIADO",
                ),
            )

            con.commit()
            con.close()
            return True

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o orçamento:\n{e}")
            return False


    def salvar_orcamento_impresso(self):
        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                """
                INSERT INTO orcamentos_enviados (
                    cliente_nome,
                    telefone,
                    veiculo,
                    caminho_imagem,
                    mao_de_obra,
                    total_pecas,
                    total_servicos,
                    data_criacao,
                    status_envio
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    self.nome_cliente,
                    self.telefone,
                    self.veiculo,
                    self.caminho_imagem,
                    self.mao_de_obra,
                    self.total_pecas,
                    self.total_servicos,
                    datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                    "IMPRESSO",
                ),
            )

            con.commit()
            con.close()
            return True

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível salvar o orçamento impresso:\n{e}")
            return False

    def mostrar_imagem(self):
        if not os.path.exists(self.caminho_imagem):
            messagebox.showerror("Erro", "Imagem do orçamento não encontrada.")
            return

        img = Image.open(self.caminho_imagem)

        largura_max = 760
        proporcao = largura_max / img.width
        nova_altura = int(img.height * proporcao)

        img = img.resize((largura_max, nova_altura), Image.LANCZOS)

        self.img_tk = ImageTk.PhotoImage(img)

        lbl = tk.Label(self.area_interna, image=self.img_tk, bg="#cfd6df")
        lbl.pack(pady=20)

    def salvar_imagem_na_pasta_orcamentos(self):
        try:
            if not os.path.exists(self.caminho_imagem):
                messagebox.showerror("Erro", "Imagem do orçamento não encontrada.")
                return None

            pasta_base = os.path.dirname(os.path.abspath(__file__))
            pasta_orcamentos = os.path.join(pasta_base, "orcamentos")
            os.makedirs(pasta_orcamentos, exist_ok=True)

            placa_nome = "".join(
                ch for ch in str(getattr(self, "placa", "") or "").upper()
                if ch.isalnum()
            )

            if placa_nome:
                nome_arquivo = f"{placa_nome}.jpg"
            else:
                nome_arquivo = f"ORCAMENTO_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"

            caminho_destino = os.path.join(pasta_orcamentos, nome_arquivo)

            # Primeiro arquivo: EOU3D73.jpg
            # Segundo: EOU3D73_02.jpg
            # Terceiro: EOU3D73_03.jpg
            if os.path.exists(caminho_destino) and placa_nome:
                contador = 2

                while True:
                    nome_incremental = f"{placa_nome}_{contador:02d}.jpg"
                    caminho_incremental = os.path.join(pasta_orcamentos, nome_incremental)

                    if not os.path.exists(caminho_incremental):
                        caminho_destino = caminho_incremental
                        break

                    contador += 1

            elif os.path.exists(caminho_destino):
                contador = 2
                nome_base, extensao = os.path.splitext(nome_arquivo)

                while True:
                    caminho_incremental = os.path.join(
                        pasta_orcamentos,
                        f"{nome_base}_{contador:02d}{extensao}"
                    )

                    if not os.path.exists(caminho_incremental):
                        caminho_destino = caminho_incremental
                        break

                    contador += 1

            if os.path.abspath(self.caminho_imagem) != os.path.abspath(caminho_destino):
                shutil.copy(self.caminho_imagem, caminho_destino)

            self.caminho_imagem = caminho_destino
            self.salvar_dados_orcamento_json(caminho_destino)
            return caminho_destino

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar o orçamento na pasta orçamentos:\n{e}"
            )
            return None


    def salvar_dados_orcamento_json(self, caminho_imagem_salvo):
        try:
            pasta_base = os.path.dirname(os.path.abspath(__file__))
            pasta_dados = os.path.join(pasta_base, "dados_orcamentos")
            os.makedirs(pasta_dados, exist_ok=True)

            nome_base = os.path.splitext(os.path.basename(caminho_imagem_salvo))[0]
            caminho_json = os.path.join(pasta_dados, f"{nome_base}.json")

            dados_orcamento = {
                "cliente": self.nome_cliente,
                "telefone": self.telefone,
                "veiculo": self.veiculo,
                "placa": self.placa,
                "mao_de_obra": self.mao_de_obra,
                "total_pecas": self.total_pecas,
                "total_servicos": self.total_servicos,
                "caminho_imagem": caminho_imagem_salvo,
                "data_criacao": datetime.now().strftime("%d/%m/%Y %H:%M:%S"),
                "itens": [
                    {
                        "quantidade": str(item[0]),
                        "descricao": str(item[1]).upper(),
                        "valor_unitario": str(item[2]).replace("R$", "").strip(),
                    }
                    for item in self.itens
                ],
            }

            with open(caminho_json, "w", encoding="utf-8") as arquivo:
                json.dump(dados_orcamento, arquivo, ensure_ascii=False, indent=4)

            return caminho_json

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível salvar os dados do orçamento:\\n{e}"
            )
            return None


    def enviar_para_cliente(self):
        telefone_cliente = self.telefone or ""

        if not telefone_cliente:
            telefone_cliente = self._pedir_telefone_whatsapp()

            if telefone_cliente is None:
                return

        telefone_limpo = "".join(ch for ch in str(telefone_cliente) if ch.isdigit())[:11]

        if len(telefone_limpo) != 11:
            messagebox.showwarning(
                "Atenção",
                "Informe um telefone válido com 11 dígitos.\nExemplo: 11999999999"
            )
            return

        telefone_envio = "55" + telefone_limpo

        caminho_salvo = self.salvar_imagem_na_pasta_orcamentos()

        if not caminho_salvo:
            return

        mensagem = (
            f"Olá {self.nome_cliente}!\n\n"
            f"Segue seu orçamento da *Juliano Automecânica* 🔧\n\n"
            f"Qualquer dúvida estou à disposição."
        )

        texto_url = urllib.parse.quote(mensagem)
        url = f"whatsapp://send?phone={telefone_envio}&text={texto_url}"

        if self.salvar_orcamento_enviado():
            webbrowser.open(url)

    def _pedir_telefone_whatsapp(self):
        janela = tk.Toplevel(self)
        janela.title("Telefone do Cliente")
        janela.configure(bg="#f5f6f8")
        janela.resizable(False, False)
        janela.transient(self)
        janela.grab_set()

        telefone_var = tk.StringVar()

        box = tk.Frame(janela, bg="#f5f6f8", padx=18, pady=14)
        box.pack(fill="both", expand=True)

        tk.Label(
            box,
            text="Digite o telefone com WhatsApp (com DDD):",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(0, 6))

        entrada = tk.Entry(
            box,
            textvariable=telefone_var,
            width=28,
            font=("Segoe UI", 10),
            justify="center",
        )
        entrada.pack(ipady=3)
        entrada.focus_set()

        def limitar_telefone(*args):
            texto = "".join(ch for ch in telefone_var.get() if ch.isdigit())[:11]

            if telefone_var.get() != texto:
                telefone_var.set(texto)
                entrada.icursor(tk.END)

        telefone_var.trace_add("write", limitar_telefone)

        resultado = {"telefone": None}

        def confirmar():
            telefone = telefone_var.get().strip()

            if len(telefone) != 11:
                messagebox.showwarning(
                    "Atenção",
                    "Informe um telefone válido com 11 dígitos.\nExemplo: 11999999999",
                    parent=janela,
                )
                return

            resultado["telefone"] = telefone
            janela.destroy()

        def cancelar():
            resultado["telefone"] = None
            janela.destroy()

        botoes = tk.Frame(box, bg="#f5f6f8")
        botoes.pack(pady=(10, 0))

        tk.Button(
            botoes,
            text="OK",
            width=9,
            command=confirmar,
        ).pack(side="left", padx=(0, 8))

        tk.Button(
            botoes,
            text="Cancelar",
            width=9,
            command=cancelar,
        ).pack(side="left")

        janela.bind("<Return>", lambda event: confirmar())
        janela.bind("<Escape>", lambda event: cancelar())
        janela.protocol("WM_DELETE_WINDOW", cancelar)

        janela.update_idletasks()
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        sw = janela.winfo_screenwidth()
        sh = janela.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        janela.geometry(f"+{x}+{y}")

        self.wait_window(janela)
        return resultado["telefone"]

    def imprimir_orcamento(self):
        if not os.path.exists(self.caminho_imagem):
            messagebox.showerror("Erro", "Imagem do orçamento não encontrada.")
            return

        caminho_salvo = self.salvar_imagem_na_pasta_orcamentos()

        if not caminho_salvo:
            return

        if not self.salvar_orcamento_impresso():
            return

        try:
            img = Image.open(self.caminho_imagem).convert("RGB")

            # A4 em retrato com boa qualidade
            a4_largura = 2480
            a4_altura = 3508

            # Página branca
            pagina = Image.new("RGB", (a4_largura, a4_altura), "white")

            # Margem menor para ocupar mais a folha
            margem_lateral = 80
            margem_superior = 80
            margem_inferior = 80

            area_largura = a4_largura - (margem_lateral * 2)
            area_altura = a4_altura - margem_superior - margem_inferior

            # Faz a imagem ocupar o máximo possível da área útil
            proporcao_img = img.width / img.height
            proporcao_area = area_largura / area_altura

            if proporcao_img > proporcao_area:
                nova_largura = area_largura
                nova_altura = int(nova_largura / proporcao_img)
            else:
                nova_altura = area_altura
                nova_largura = int(nova_altura * proporcao_img)

            img = img.resize((nova_largura, nova_altura), Image.LANCZOS)

            # Centraliza a imagem
            x = (a4_largura - nova_largura) // 2
            y = (a4_altura - nova_altura) // 2

            pagina.paste(img, (x, y))

            # PDF temporário
            pasta_temp = tempfile.gettempdir()
            caminho_pdf = os.path.join(pasta_temp, "orcamento_impressao_temp.pdf")
            pagina.save(caminho_pdf, "PDF", resolution=300.0)

            try:
                os.startfile(caminho_pdf, "print")
            except Exception:
                os.startfile(caminho_pdf)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível preparar a impressão:\n{e}")

class ServicesFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f3f4f6")
        self.app = app

        # =========================
        # VARIÁVEIS DA NOVA TELA
        # =========================
        self.nome_orcamento_var = tk.StringVar()
        self.veiculo_orcamento_var = tk.StringVar()
        self.placa_orcamento_var = tk.StringVar()
        self._formatando_placa_orcamento = False
        self.cliente_vinculado_var = tk.StringVar(value="nenhum")
        self.busca_placa_var = tk.StringVar()
        self.cliente_orcamento_id = None
        self.sugestoes_placa_clientes = []
        self.mao_obra_var = tk.StringVar()
        self.mao_obra_var.trace_add("write", self.atualizar_total_servicos)
        self.total_pecas_var = tk.StringVar(value="R$ 0,00")
        self.total_servicos_var = tk.StringVar(value="R$ 0,00")

        self.nome_orcamento_var.trace_add(
            "write", lambda *args: self._maiusculo_var(self.nome_orcamento_var)
        )
        self.veiculo_orcamento_var.trace_add(
            "write", lambda *args: self._maiusculo_var(self.veiculo_orcamento_var)
        )
        self.placa_orcamento_var.trace_add(
            "write", self._formatar_placa_visual
        )
        self.busca_placa_var.trace_add(
            "write", lambda *args: self._maiusculo_var(self.busca_placa_var)
        )

        # =========================
        # ESTILO DA TABELA
        # =========================
        style = ttk.Style()
        try:
            style.theme_use("clam")
        except Exception:
            pass

        style.configure(
            "Orcamento.Treeview",
            background="white",
            foreground="#111827",
            fieldbackground="white",
            rowheight=26,
            bordercolor="#cbd5e1",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10),
        )
        style.configure(
            "Orcamento.Treeview.Heading",
            background="#f3f4f6",
            foreground="#111827",
            bordercolor="#cbd5e1",
            borderwidth=1,
            relief="solid",
            font=("Segoe UI", 10, "bold"),
        )
        style.map(
            "Orcamento.Treeview",
            background=[("selected", "#dbeafe")],
            foreground=[("selected", "#111827")],
        )

        # =========================
        # CONTAINER PRINCIPAL
        # =========================
        container = tk.Frame(self, bg="#f3f4f6")
        container.pack(fill="both", expand=True, padx=12, pady=6)

        tk.Label(
            container,
            text="📄  ORÇAMENTO",
            bg="#f3f4f6",
            fg="#0b63ce",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w", pady=(0, 5))

        # =========================
        # CARD DADOS DO CLIENTE
        # =========================
        cliente_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            height=155,
        )
        cliente_card.pack(fill="x", pady=(0, 8))
        cliente_card.pack_propagate(False)

        tk.Label(
            cliente_card,
            text="👤  DADOS DO CLIENTE",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(7, 4))

        cliente_body = tk.Frame(cliente_card, bg="white")
        cliente_body.pack(fill="both", expand=True, padx=16, pady=(0, 8))

        form_cliente = tk.Frame(cliente_body, bg="white")
        form_cliente.pack(side="left", anchor="n")

        tk.Label(
            form_cliente,
            text="Nome:",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 4))

        tk.Entry(
            form_cliente,
            textvariable=self.nome_orcamento_var,
            width=34,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        ).grid(row=0, column=1, padx=(10, 0), pady=(0, 4), ipady=3)

        tk.Label(
            form_cliente,
            text="Veículo:",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))

        tk.Entry(
            form_cliente,
            textvariable=self.veiculo_orcamento_var,
            width=34,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        ).grid(row=1, column=1, padx=(10, 0), pady=(8, 0), ipady=3)

        tk.Label(
            form_cliente,
            text="Placa:",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", pady=(8, 0))

        self.placa_orcamento_entry = tk.Entry(
            form_cliente,
            textvariable=self.placa_orcamento_var,
            width=34,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        self.placa_orcamento_entry.grid(row=2, column=1, padx=(10, 0), pady=(8, 0), ipady=3)

        botoes_cliente = tk.Frame(cliente_body, bg="white")
        botoes_cliente.pack(side="left", padx=(22, 0), anchor="n")

        tk.Button(
            botoes_cliente,
            text="🔗  Vincular Cliente Novo",
            command=self.vincular_cliente_visual,
            bg="white",
            fg="#2563eb",
            activebackground="#dbeafe",
            activeforeground="#2563eb",
            relief="solid",
            bd=1,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
        ).pack(fill="x", pady=(0, 10))

        tk.Button(
            botoes_cliente,
            text="🧹  Limpar Cliente",
            command=self.limpar_cliente,
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=5,
            font=("Segoe UI", 10, "bold"),
        ).pack(fill="x")

        cliente_info = tk.Frame(
            cliente_body,
            bg="#f8fafc",
            highlightbackground="#e5e7eb",
            highlightthickness=1,
            width=255,
            height=92,
        )
        cliente_info.pack(side="left", padx=(22, 0), anchor="n")
        cliente_info.pack_propagate(False)

        tk.Label(
            cliente_info,
            text="👥  Cliente vinculado:",
            bg="#f8fafc",
            fg="#2563eb",
            font=("Segoe UI", 11, "bold"),
        ).pack(pady=(10, 1))

        tk.Label(
            cliente_info,
            textvariable=self.cliente_vinculado_var,
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 11, "bold"),
            wraplength=235,
        ).pack()

        # =========================
        # CARD ITENS
        # =========================
        itens_card = tk.Frame(
            container,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
        )
        itens_card.pack(fill="both", expand=True, pady=(0, 8))

        tk.Label(
            itens_card,
            text="🛒  ITENS DO ORÇAMENTO",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(7, 5))

        tabela_frame = tk.Frame(
            itens_card,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
        )
        tabela_frame.pack(fill="both", expand=True, padx=14, pady=(0, 5))

        cols = ("quantidade", "descricao", "valor")
        self.tree = ttk.Treeview(
            tabela_frame,
            columns=cols,
            show="headings",
            style="Orcamento.Treeview",
            height=5,
        )

        colunas = [
            ("quantidade", "QUANTIDADE", 150),
            ("descricao", "DESCRIÇÃO", 560),
            ("valor", "VALOR R$", 190),
        ]

        for coluna, titulo, largura in colunas:
            self.tree.heading(coluna, text=titulo, anchor="center")
            self.tree.column(coluna, width=largura, minwidth=110, anchor="center", stretch=True)

        scrollbar = ttk.Scrollbar(
            tabela_frame,
            orient="vertical",
            command=self.tree.yview,
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)

        # cores alternadas para deixar a tabela de orçamento mais bonita
        self.tree.tag_configure("linha_par_orcamento", background="#f8fafc")
        self.tree.tag_configure("linha_impar_orcamento", background="#eef2f7")
        scrollbar.pack(side="right", fill="y")

        # =========================
        # BOTÕES DE AÇÃO
        # =========================
        botoes = tk.Frame(container, bg="#f3f4f6")
        botoes.pack(fill="x", padx=14, pady=(0, 5))

        def criar_botao(texto, cor, comando, largura):
            return tk.Button(
                botoes,
                text=texto,
                command=comando,
                bg=cor,
                fg="white",
                activeforeground="white",
                bd=0,
                width=largura,
                padx=8,
                pady=5,
                font=("Segoe UI", 10, "bold"),
            )

        criar_botao(
            "➕  Adicionar",
            "#08803a",
            self.validar_cliente_antes_adicionar,
            13,
        ).pack(side="left", padx=(0, 14))

        criar_botao(
            "✏  Editar",
            "#0b63ce",
            self.editar_item_selecionado,
            12,
        ).pack(side="left", padx=(0, 14))

        criar_botao(
            "🗑  Excluir",
            "#ef233c",
            self.excluir_item_selecionado,
            12,
        ).pack(side="left", padx=(0, 14))

        criar_botao(
            "📄  Criar Orçamento",
            "#7b2cbf",
            self.criar_orcamento_visual,
            16,
        ).pack(side="left")

        # =========================
        # RODAPÉ
        # =========================
        rodape = tk.Frame(
            container,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            height=86,
        )
        rodape.pack(fill="x")
        rodape.pack_propagate(False)

        busca_box = tk.Frame(rodape, bg="white")
        busca_box.pack(side="left", padx=16, pady=8)

        tk.Label(
            busca_box,
            text="Buscar por Placa:",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 7))

        self.busca_placa_entry = tk.Entry(
            busca_box,
            textvariable=self.busca_placa_var,
            font=("Segoe UI", 10),
            width=16,
            relief="solid",
            bd=1,
        )
        self.busca_placa_entry.grid(row=0, column=1, padx=(10, 0), pady=(0, 7), ipady=2)
        self.busca_placa_entry.bind("<KeyRelease>", self.atualizar_sugestoes_placa)
        self.busca_placa_entry.bind("<Return>", self.selecionar_primeira_sugestao_placa)
        
        self.popup_sugestoes_placa = None
        self.sugestoes_placa = None

        self.winfo_toplevel().bind("<Unmap>", self._ao_minimizar_janela, add="+")

        tk.Label(
            busca_box,
            text="Mão de Obra:",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=0, sticky="w")

        tk.Entry(
            busca_box,
            textvariable=self.mao_obra_var,
            width=16,
            justify="center",
            relief="solid",
            bd=1,
        ).grid(row=1, column=1, padx=(10, 0), ipady=2)

        totais_box = tk.Frame(rodape, bg="white")
        totais_box.pack(side="left", padx=(55, 0), pady=14)

        tk.Label(
            totais_box,
            text="Total de Peças:",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, padx=(0, 55))

        tk.Label(
            totais_box,
            textvariable=self.total_pecas_var,
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 12, "bold"),
        ).grid(row=1, column=0, padx=(0, 55))

        tk.Label(
            totais_box,
            text="|",
            bg="white",
            fg="#9ca3af",
            font=("Segoe UI", 18),
        ).grid(row=0, column=1, rowspan=2, padx=(0, 55))

        tk.Label(
            totais_box,
            text="Total de Serviços:",
            bg="white",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=2)

        tk.Label(
            totais_box,
            textvariable=self.total_servicos_var,
            bg="white",
            fg="green",
            font=("Segoe UI", 12, "bold"),
        ).grid(row=1, column=2)

    def _normalizar_placa_busca(self, valor):
        return "".join(ch for ch in str(valor or "").upper() if ch.isalnum())

    def _ao_minimizar_janela(self, event=None):
        try:
            if self.winfo_toplevel().state() == "iconic":
                self.esconder_sugestoes_placa()
        except Exception:
            pass

    def esconder_sugestoes_placa(self):
        if hasattr(self, "popup_sugestoes_placa") and self.popup_sugestoes_placa:
            try:
                self.popup_sugestoes_placa.destroy()
            except Exception:
                pass

        self.popup_sugestoes_placa = None
        self.sugestoes_placa = None
        self.sugestoes_placa_clientes = []

    def mostrar_popup_sugestoes_placa(self):
        self.esconder_sugestoes_placa()

        self.popup_sugestoes_placa = tk.Toplevel(self)
        self.popup_sugestoes_placa.overrideredirect(True)
        self.popup_sugestoes_placa.configure(bg="white")
        self.popup_sugestoes_placa.transient(self.winfo_toplevel())
        self.popup_sugestoes_placa.attributes("-topmost", True)
        self.popup_sugestoes_placa.lift(self.winfo_toplevel())

        self.sugestoes_placa = tk.Listbox(
            self.popup_sugestoes_placa,
            width=46,
            height=4,
            font=("Segoe UI", 9),
            relief="solid",
            bd=1,
            activestyle="none",
        )
        self.sugestoes_placa.pack(fill="both", expand=True)

        self.sugestoes_placa.bind("<<ListboxSelect>>", self.selecionar_sugestao_placa)
        self.sugestoes_placa.bind("<Return>", self.selecionar_sugestao_placa)
        self.sugestoes_placa.bind("<Escape>", lambda event: self.esconder_sugestoes_placa())

        self.busca_placa_entry.update_idletasks()
        x = self.busca_placa_entry.winfo_rootx()
        y = self.busca_placa_entry.winfo_rooty() + self.busca_placa_entry.winfo_height()

        largura = 430
        altura = 82
        self.popup_sugestoes_placa.geometry(f"{largura}x{altura}+{x}+{y}")

    def atualizar_sugestoes_placa(self, event=None):
        placa_digitada = self._normalizar_placa_busca(self.busca_placa_var.get())

        teclas_ignorar = {"Up", "Down", "Left", "Right", "Return", "Escape", "Tab"}
        if event is not None and getattr(event, "keysym", "") in teclas_ignorar:
            if event.keysym == "Escape":
                self.esconder_sugestoes_placa()
            return

        if not placa_digitada:
            self.esconder_sugestoes_placa()
            return

        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                """
                SELECT c.id, c.name, v.vehicle, v.plate
                FROM vehicles v
                INNER JOIN clients c ON c.id = v.client_id
                WHERE UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) LIKE ?
                ORDER BY c.name
                LIMIT 5
                """,
                (placa_digitada + "%",),
            )

            resultados = cur.fetchall()
            con.close()

            if not resultados:
                self.esconder_sugestoes_placa()
                return

            self.mostrar_popup_sugestoes_placa()

            for cliente_id, nome, veiculo, placa in resultados:
                texto_sugestao = f"{placa or placa_digitada} - {nome or ''} - {veiculo or ''}".strip().upper()
                self.sugestoes_placa.insert(tk.END, texto_sugestao)
                self.sugestoes_placa_clientes.append((cliente_id, nome, veiculo, placa))

        except Exception as e:
            self.esconder_sugestoes_placa()
            messagebox.showerror("Erro", f"Não foi possível buscar sugestões de placa:\n{e}")

    def selecionar_primeira_sugestao_placa(self, event=None):
        if hasattr(self, "sugestoes_placa") and self.sugestoes_placa and self.sugestoes_placa.size() > 0:
            self.sugestoes_placa.selection_clear(0, tk.END)
            self.sugestoes_placa.selection_set(0)
            self.sugestoes_placa.activate(0)
            self.selecionar_sugestao_placa()
            return "break"

        self.buscar_cliente_por_placa()
        return "break"

    def selecionar_sugestao_placa(self, event=None):
        if not hasattr(self, "sugestoes_placa_clientes"):
            return

        if not self.sugestoes_placa:
            return

        selecao = self.sugestoes_placa.curselection()
        if not selecao:
            return

        indice = selecao[0]

        if indice < 0 or indice >= len(self.sugestoes_placa_clientes):
            return

        cliente_id, nome, veiculo, placa = self.sugestoes_placa_clientes[indice]

        self.cliente_orcamento_id = cliente_id
        self.nome_orcamento_var.set(str(nome or "").strip().upper())
        self.veiculo_orcamento_var.set(str(veiculo or "").strip().upper())
        self.busca_placa_var.set(str(placa or "").strip().upper())
        self.placa_orcamento_var.set(str(placa or "").strip().upper())
        self.cliente_vinculado_var.set(f"{nome or ''} - {veiculo or ''}".strip().upper())

        self.esconder_sugestoes_placa()
        return "break"

    def buscar_cliente_por_placa(self, event=None):
        placa_digitada = self._normalizar_placa_busca(self.busca_placa_var.get())

        if not placa_digitada:
            return

        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                """
                SELECT c.id, c.name, v.vehicle, v.plate
                FROM vehicles v
                INNER JOIN clients c ON c.id = v.client_id
                WHERE UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) LIKE ?
                ORDER BY c.name
                LIMIT 1
                """,
                (placa_digitada + "%",),
            )

            cliente = cur.fetchone()
            con.close()

            if not cliente:
                self.cliente_orcamento_id = None
                self.nome_orcamento_var.set("")
                self.veiculo_orcamento_var.set("")
                self.placa_orcamento_var.set("")
                self.cliente_vinculado_var.set("nenhum")
                messagebox.showwarning("Atenção", "Cliente não encontrado para esta placa.")
                return

            cliente_id, nome, veiculo, placa_banco = cliente

            self.cliente_orcamento_id = cliente_id
            self.nome_orcamento_var.set(str(nome or "").strip().upper())
            self.veiculo_orcamento_var.set(str(veiculo or "").strip().upper())
            self.busca_placa_var.set(str(placa_banco or placa_digitada).strip().upper())
            self.placa_orcamento_var.set(str(placa_banco or placa_digitada).strip().upper())
            self.cliente_vinculado_var.set(f"{nome or ''} - {veiculo or ''}".strip().upper())

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível buscar o cliente pela placa:\n{e}")

    def _formatar_placa_visual(self, *args):
        if getattr(self, "_formatando_placa_orcamento", False):
            return

        self._formatando_placa_orcamento = True

        try:
            texto_atual = self.placa_orcamento_var.get()

            # Mantém apenas letras e números, tudo em maiúsculo, limitado a 7 caracteres.
            texto_limpo = "".join(
                ch for ch in texto_atual.upper()
                if ch.isalnum()
            )[:7]

            if len(texto_limpo) > 3:
                texto_formatado = f"{texto_limpo[:3]}-{texto_limpo[3:]}"
            else:
                texto_formatado = texto_limpo

            if texto_atual != texto_formatado:
                self.placa_orcamento_var.set(texto_formatado)

                if hasattr(self, "placa_orcamento_entry"):
                    self.placa_orcamento_entry.after(
                        1,
                        lambda: self.placa_orcamento_entry.icursor(tk.END)
                    )

        finally:
            self._formatando_placa_orcamento = False


    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def vincular_cliente_visual(self):
        nome = self.nome_orcamento_var.get().strip().upper()
        veiculo = self.veiculo_orcamento_var.get().strip().upper()
        placa = self.placa_orcamento_var.get().strip().upper()

        if not nome:
            messagebox.showwarning("Atenção", "Informe o nome do cliente.")
            return

        if not veiculo:
            messagebox.showwarning("Atenção", "Informe o veículo do cliente.")
            return

        if not placa:
            messagebox.showwarning("Atenção", "Informe a placa do veículo.")
            return

        # Cliente novo/manual não vem do banco.
        self.cliente_orcamento_id = None

        # O campo "Buscar por Placa" é usado apenas para buscar cliente já cadastrado.
        # Por isso, quando o cliente é novo/manual, ele deve ficar vazio.
        self.busca_placa_var.set("")
        self.esconder_sugestoes_placa()

        self.cliente_vinculado_var.set(f"{nome} - {veiculo} - {placa}")

    def limpar_cliente(self):
        self.nome_orcamento_var.set("")
        self.veiculo_orcamento_var.set("")
        self.placa_orcamento_var.set("")
        self.cliente_vinculado_var.set("nenhum")
        self.cliente_orcamento_id = None
        self.busca_placa_var.set("")
        self.esconder_sugestoes_placa()

        # limpa todos os itens do orçamento
        for item in self.tree.get_children():
            self.tree.delete(item)

        # limpa campos do rodapé
        if hasattr(self, "mao_obra_var"):
            self.mao_obra_var.set("")

        if hasattr(self, "busca_placa_var"):
            self.busca_placa_var.set("")

        # zera totais
        if hasattr(self, "total_pecas_var"):
            self.total_pecas_var.set("R$ 0,00")

        if hasattr(self, "total_servicos_var"):
            self.total_servicos_var.set("R$ 0,00")
            self.atualizar_cores_tabela_orcamento()

    def validar_cliente_antes_adicionar(self):
        self.abrir_janela_adicionar_item()

    def abrir_janela_adicionar_item(self):
        cliente_vinculado = self.cliente_vinculado_var.get().strip()

        if not cliente_vinculado or cliente_vinculado.lower() == "nenhum":
            messagebox.showwarning(
                "Atenção",
                "Vincule um cliente antes de adicionar itens ao orçamento."
            )
            return

        janela = tk.Toplevel(self)
        janela.title("Adicionar Item")
        janela.configure(bg="#f5f6f8")
        janela.resizable(False, False)
        janela.grab_set()

        frame = tk.Frame(janela, bg="#f5f6f8", padx=22, pady=18)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Adicionar item ao orçamento",
            bg="#f5f6f8",
            fg="#0b63ce",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 14))

        quantidade_var = tk.StringVar()
        descricao_var = tk.StringVar()
        valor_var = tk.StringVar()

        descricao_var.trace_add("write", lambda *args: self._maiusculo_var(descricao_var))

        validar_quantidade_cmd = janela.register(self._validar_quantidade_item)
        validar_valor_cmd = janela.register(self._validar_valor_item)

        campos = [
            ("Quantidade:", quantidade_var),
            ("Descrição:", descricao_var),
            ("Valor R$:", valor_var),
        ]

        quantidade_entry = None

        for i, (label, var) in enumerate(campos, start=1):
            tk.Label(
                frame,
                text=label,
                bg="#f5f6f8",
                fg="#111827",
                font=("Segoe UI", 10, "bold"),
            ).grid(row=i, column=0, sticky="w", pady=6)

            entry_opcoes = {
                "textvariable": var,
                "width": 34,
                "font": ("Segoe UI", 10),
                "relief": "solid",
                "bd": 1,
            }

            if label == "Quantidade:":
                entry_opcoes["validate"] = "key"
                entry_opcoes["validatecommand"] = (validar_quantidade_cmd, "%P")

            if label == "Valor R$:":
                entry_opcoes["validate"] = "key"
                entry_opcoes["validatecommand"] = (validar_valor_cmd, "%P")

            entrada = tk.Entry(frame, **entry_opcoes)
            entrada.grid(row=i, column=1, padx=(12, 0), pady=6, ipady=3)

            if label == "Quantidade:":
                quantidade_entry = entrada

            if label == "Valor R$:":
                entrada.bind("<FocusOut>", lambda event: valor_var.set(self._formatar_valor_item(valor_var.get())))
                entrada.bind("<Return>", lambda event: valor_var.set(self._formatar_valor_item(valor_var.get())))

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.grid(row=4, column=0, columnspan=2, pady=(16, 0))

        tk.Button(
            botoes,
            text="OK",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=22,
            pady=7,
            font=("Segoe UI", 10, "bold"),
            command=lambda: self.adicionar_item_tabela(
                janela,
                quantidade_var.get(),
                descricao_var.get(),
                valor_var.get(),
            ),
        ).pack(side="left", padx=6)

        tk.Button(
            botoes,
            text="Cancelar",
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=7,
            font=("Segoe UI", 10, "bold"),
            command=janela.destroy,
        ).pack(side="left", padx=6)

        janela.update_idletasks()
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        sw = janela.winfo_screenwidth()
        sh = janela.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        janela.geometry(f"+{x}+{y}")

        if quantidade_entry:
            janela.after(150, lambda: (quantidade_entry.focus_force(), quantidade_entry.icursor(tk.END)))

    def _validar_quantidade_item(self, novo_valor):
        return novo_valor == "" or novo_valor.isdigit()

    def _validar_valor_item(self, novo_valor):
        if novo_valor == "":
            return True

        caracteres_validos = "0123456789,"
        if any(ch not in caracteres_validos for ch in novo_valor):
            return False

        if novo_valor.count(",") > 1:
            return False

        if "," in novo_valor:
            parte_decimal = novo_valor.split(",", 1)[1]
            if len(parte_decimal) > 2:
                return False

        return True

    def _formatar_valor_item(self, valor):
        texto = str(valor).strip()

        if not texto:
            return ""

        texto = texto.replace(".", "").replace(",", ".")

        try:
            numero = float(texto)
        except ValueError:
            return ""

        formatado = f"{numero:,.2f}"
        return formatado.replace(",", "X").replace(".", ",").replace("X", ".")

    def _converter_valor_brasileiro_para_float(self, valor):
        valor = str(valor or "").strip()
        valor = valor.replace("R$", "").strip()

        if not valor:
            return 0.0

        # Exemplo: 1.500,00 -> 1500.00
        valor = valor.replace(".", "").replace(",", ".")

        try:
            return float(valor)
        except ValueError:
            return 0.0

    def atualizar_total_servicos(self, *args):
        total_pecas = self._converter_valor_brasileiro_para_float(self.total_pecas_var.get())

        valor_mao_obra = "0"
        if hasattr(self, "mao_obra_var"):
            valor_mao_obra = self.mao_obra_var.get()

        mao_obra = self._converter_valor_brasileiro_para_float(valor_mao_obra)
        total_servicos = total_pecas + mao_obra

        total_formatado = f"R$ {total_servicos:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.total_servicos_var.set(total_formatado)

    def atualizar_total_pecas(self):
        total = 0.0

        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")

            if len(valores) >= 3:
                total += self._converter_valor_brasileiro_para_float(valores[2])

        total_formatado = f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
        self.total_pecas_var.set(total_formatado)
        self.atualizar_total_servicos()

    def editar_item_selecionado(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um item da tabela para editar.")
            return

        item_id = selecionado[0]
        valores = self.tree.item(item_id, "values")

        if len(valores) < 3:
            messagebox.showwarning("Atenção", "Item inválido para edição.")
            return

        janela = tk.Toplevel(self)
        janela.title("Editar Item")
        janela.geometry("420x260")
        janela.resizable(False, False)
        janela.configure(bg="#f5f6f8")
        janela.grab_set()

        quantidade_var = tk.StringVar(value=str(valores[0]))
        descricao_var = tk.StringVar(value=str(valores[1]))
        valor_var = tk.StringVar(value=str(valores[2]))

        validar_quantidade_cmd = (janela.register(self._validar_quantidade_item), "%P")
        validar_valor_cmd = (janela.register(self._validar_valor_item), "%P")

        frame = tk.Frame(janela, bg="#f5f6f8", padx=24, pady=22)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text="Editar item do orçamento",
            bg="#f5f6f8",
            fg="#0b63ce",
            font=("Segoe UI", 13, "bold"),
        ).grid(row=0, column=0, columnspan=2, pady=(0, 18))

        campos = [
            ("Quantidade:", quantidade_var),
            ("Descrição:", descricao_var),
            ("Valor R$:", valor_var),
        ]

        quantidade_entry = None

        for i, (label, var) in enumerate(campos, start=1):
            tk.Label(
                frame,
                text=label,
                bg="#f5f6f8",
                fg="#111827",
                font=("Segoe UI", 10, "bold"),
            ).grid(row=i, column=0, sticky="w", pady=6)

            opcoes = {
                "textvariable": var,
                "width": 30,
                "font": ("Segoe UI", 10),
                "relief": "solid",
                "bd": 1,
            }

            if label == "Quantidade:":
                opcoes["validate"] = "key"
                opcoes["validatecommand"] = validar_quantidade_cmd

            if label == "Valor R$:":
                opcoes["validate"] = "key"
                opcoes["validatecommand"] = validar_valor_cmd

            entrada = tk.Entry(frame, **opcoes)
            entrada.grid(row=i, column=1, padx=(12, 0), pady=6, ipady=3)

            if label == "Quantidade:":
                quantidade_entry = entrada

            if label == "Descrição:":
                var.trace_add("write", lambda *args, v=var: self._maiusculo_var(v))

            if label == "Valor R$:":
                entrada.bind("<FocusOut>", lambda event: valor_var.set(self._formatar_valor_item(valor_var.get())))
                entrada.bind("<Return>", lambda event: valor_var.set(self._formatar_valor_item(valor_var.get())))

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.grid(row=4, column=0, columnspan=2, pady=(20, 0))

        tk.Button(
            botoes,
            text="Salvar",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=22,
            pady=7,
            font=("Segoe UI", 10, "bold"),
            command=lambda: self.salvar_edicao_item(
                janela,
                item_id,
                quantidade_var.get(),
                descricao_var.get(),
                valor_var.get()
            ),
        ).pack(side="left", padx=8)

        tk.Button(
            botoes,
            text="Cancelar",
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=22,
            pady=7,
            font=("Segoe UI", 10, "bold"),
            command=janela.destroy,
        ).pack(side="left", padx=8)

        janela.update_idletasks()
        largura = janela.winfo_width()
        altura = janela.winfo_height()
        sw = janela.winfo_screenwidth()
        sh = janela.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        janela.geometry(f"+{x}+{y}")

        if quantidade_entry:
            janela.after(150, lambda: (quantidade_entry.focus_force(), quantidade_entry.select_range(0, tk.END)))

    def salvar_edicao_item(self, janela, item_id, quantidade, descricao, valor):
        quantidade = str(quantidade or "").strip()
        descricao = str(descricao or "").strip().upper()
        valor = str(valor or "").strip()

        if not quantidade:
            messagebox.showwarning("Atenção", "Informe a quantidade.")
            return

        if not descricao:
            messagebox.showwarning("Atenção", "Informe a descrição.")
            return

        if not valor:
            messagebox.showwarning("Atenção", "Informe o valor.")
            return

        valor_formatado = self._formatar_valor_item(valor)

        self.tree.item(item_id, values=(quantidade, descricao, valor_formatado))
        self.atualizar_cores_tabela_orcamento()
        self.atualizar_total_pecas()
        self.atualizar_total_servicos()
        janela.destroy()

    def atualizar_cores_tabela_orcamento(self):
        for indice, item in enumerate(self.tree.get_children()):
            tag = "linha_par_orcamento" if indice % 2 == 0 else "linha_impar_orcamento"
            self.tree.item(item, tags=(tag,))

    def excluir_item_selecionado(self):
        selecionado = self.tree.selection()

        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um item da tabela para excluir.")
            return

        confirmar = messagebox.askyesno(
            "Confirmar exclusão",
            "Deseja realmente excluir o item selecionado?"
        )

        if not confirmar:
            return

        for item in selecionado:
            self.tree.delete(item)

        self.atualizar_cores_tabela_orcamento()
        self.atualizar_total_pecas()
        self.atualizar_total_servicos()

    def criar_orcamento_visual(self):
        nome_cliente = self.nome_orcamento_var.get().strip()
        veiculo = self.veiculo_orcamento_var.get().strip()
        placa = self.placa_orcamento_var.get().strip().upper()

        if not nome_cliente:
            messagebox.showwarning("Atenção", "Informe ou vincule um cliente antes de criar o orçamento.")
            return

        if not veiculo:
            messagebox.showwarning("Atenção", "Informe o veículo antes de criar o orçamento.")
            return

        if not placa:
            messagebox.showwarning("Atenção", "Informe a placa antes de criar o orçamento.")
            return

        self.busca_placa_var.set(placa)

        itens = []
        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            if len(valores) >= 3:
                quantidade = str(valores[0]).strip()
                descricao = str(valores[1]).strip()
                valor = str(valores[2]).strip()

                if quantidade or descricao or valor:
                    itens.append((quantidade, descricao, valor))

        if not itens:
            messagebox.showwarning("Atenção", "Adicione pelo menos um item ao orçamento.")
            return

        caminho_imagem = self.gerar_imagem_orcamento(nome_cliente, veiculo, itens)

        if not caminho_imagem:
            return

        telefone = ""
        if hasattr(self, "telefone_orcamento_var"):
            telefone = self.telefone_orcamento_var.get().strip()

        mao_de_obra = "R$ 0,00"
        if hasattr(self, "mao_obra_var"):
            mao_de_obra = self.mao_obra_var.get().strip() or "0,00"
            if not mao_de_obra.startswith("R$"):
                mao_de_obra = f"R$ {mao_de_obra}"

        OrcamentoPreview(
            self,
            caminho_imagem,
            nome_cliente=nome_cliente,
            telefone=telefone,
            veiculo=veiculo,
            placa=placa,
            mao_de_obra=mao_de_obra,
            total_pecas=self.total_pecas_var.get(),
            total_servicos=self.total_servicos_var.get(),
            itens=itens,
        )

    def gerar_imagem_orcamento(self, nome_cliente, veiculo, itens):
        try:
            # Mantém a folha no mesmo tamanho para a pré-visualização não reduzir automaticamente.
            # O conteúdo interno foi aumentado.
            largura = 900
            altura_linha = 48
            altura = 1200 + max(0, len(itens) - 4) * altura_linha

            img = Image.new("RGB", (largura, altura), "white")
            draw = ImageDraw.Draw(img)

            def carregar_fonte(tamanho, negrito=False):
                fontes = [
                    "C:/Windows/Fonts/arialbd.ttf" if negrito else "C:/Windows/Fonts/arial.ttf",
                    "C:/Windows/Fonts/segoeuib.ttf" if negrito else "C:/Windows/Fonts/segoeui.ttf",
                ]

                for fonte in fontes:
                    try:
                        return ImageFont.truetype(fonte, tamanho)
                    except Exception:
                        pass

                return ImageFont.load_default()

            # Fontes maiores dentro do mesmo JPG
            fonte_titulo = carregar_fonte(43)
            fonte_subtitulo = carregar_fonte(31)
            fonte_normal = carregar_fonte(25)
            fonte_negrito = carregar_fonte(25, True)
            fonte_menor = carregar_fonte(21)

            preto = (0, 0, 0)

            # LOGO maior dentro do mesmo JPG
            try:
                logo = Image.open(LOGO_PATH).convert("RGBA")
                logo = logo.resize((155, 155), Image.LANCZOS)
                img.paste(logo, (60, 35), logo)
            except Exception:
                draw.rectangle((60, 35, 215, 190), outline=preto, width=3)
                draw.text((105, 95), "LOGO", fill=preto, font=fonte_menor)

            # Cabeçalho ajustado
            draw.text((245, 58), "Juliano Automecânica", fill=preto, font=fonte_titulo)
            draw.text((245, 122), "ORÇAMENTO", fill=preto, font=fonte_subtitulo)

            y = 230
            draw.line((60, y, largura - 60, y), fill=preto, width=3)

            y += 45
            data_atual = datetime.now().strftime("%d/%m/%Y")
            draw.text((60, y), f"Data: {data_atual}", fill=preto, font=fonte_negrito)

            y += 55
            draw.text((60, y), f"Cliente: {nome_cliente}", fill=preto, font=fonte_normal)

            y += 48
            draw.text((60, y), f"Veículo: {veiculo}", fill=preto, font=fonte_normal)

            placa_visual = ""
            if hasattr(self, "placa_orcamento_var"):
                placa_visual = self.placa_orcamento_var.get().strip().upper()
            elif hasattr(self, "busca_placa_var"):
                placa_visual = self.busca_placa_var.get().strip().upper()

            y += 48
            draw.text((60, y), f"Placa: {placa_visual}", fill=preto, font=fonte_normal)

            y += 62
            draw.line((60, y, largura - 60, y), fill=preto, width=3)

            y += 36
            draw.text((60, y), "QUANTIDADE", fill=preto, font=fonte_negrito)
            draw.text((430, y + 15), "DESCRIÇÃO", fill=preto, font=fonte_negrito, anchor="mm")
            draw.text((800, y), "VALOR", fill=preto, font=fonte_negrito, anchor="ra")

            y += 40
            draw.line((60, y, largura - 60, y), fill=preto, width=3)

            y += 34

            for quantidade, descricao, valor in itens:
                valor_limpo = str(valor).replace("R$", "").strip()
                draw.text((85, y), str(quantidade), fill=preto, font=fonte_normal)
                draw.text((430, y), str(descricao), fill=preto, font=fonte_normal, anchor="ma")
                draw.text((800, y), f"R$ {valor_limpo}", fill=preto, font=fonte_normal, anchor="ra")
                y += altura_linha

            y += 16
            draw.line((60, y, largura - 60, y), fill=preto, width=3)

            y += 45
            mao_obra = "0,00"
            if hasattr(self, "mao_obra_var"):
                mao_obra = self.mao_obra_var.get().strip() or "0,00"

            total_pecas = self.total_pecas_var.get().replace("R$", "").strip()
            total_servicos = self.total_servicos_var.get().replace("R$", "").strip()

            draw.text((60, y), f"Mão de Obra: R$ {mao_obra}", fill=preto, font=fonte_normal)
            y += 48
            draw.text((60, y), f"Total de Peças: R$ {total_pecas}", fill=preto, font=fonte_normal)
            y += 52
            draw.text((60, y), f"Total de Serviços: R$ {total_servicos}", fill=preto, font=fonte_negrito)

            y += 78
            draw.line((60, y, largura - 60, y), fill=preto, width=3)

            y += 45
            draw.text((60, y), "Obrigado pela preferência!", fill=preto, font=fonte_menor)

            # A pré-visualização usa apenas um arquivo temporário.
            # O orçamento definitivo só é salvo ao clicar em Imprimir
            # ou ao confirmar o envio para o cliente.
            pasta_temp = tempfile.gettempdir()
            nome_arquivo = f"preview_orcamento_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            caminho = os.path.join(pasta_temp, nome_arquivo)

            img.save(caminho, "JPEG", quality=95)
            return caminho

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível gerar a imagem do orçamento:\n{e}")
            return None


    def adicionar_item_tabela(self, janela, quantidade, descricao, valor):
        quantidade = str(quantidade).strip()
        descricao = str(descricao).strip().upper()
        valor = str(valor).strip()

        if not quantidade:
            messagebox.showwarning("Atenção", "Informe a quantidade.")
            return

        if not quantidade.isdigit():
            messagebox.showwarning("Atenção", "A quantidade deve conter apenas números.")
            return

        if not descricao:
            messagebox.showwarning("Atenção", "Informe a descrição.")
            return

        if not valor:
            messagebox.showwarning("Atenção", "Informe o valor.")
            return

        valor_formatado = self._formatar_valor_item(valor)

        if not valor_formatado:
            messagebox.showwarning("Atenção", "O valor deve conter apenas números.")
            return

        self.tree.insert("", "end", values=(quantidade, descricao, valor_formatado))
        self.atualizar_cores_tabela_orcamento()
        self.atualizar_total_pecas()
        self.atualizar_total_servicos()

        # limpa os campos para permitir adicionar outro item sem fechar a janela
        for widget in janela.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry):
                    child.delete(0, tk.END)

        # volta o foco para o primeiro campo da janela
        for widget in janela.winfo_children():
            for child in widget.winfo_children():
                if isinstance(child, tk.Entry):
                    janela.after(100, lambda campo=child: (campo.focus_force(), campo.icursor(tk.END)))
                    return

    def _em_desenvolvimento(self, nome_funcao):
        messagebox.showinfo(
            "Função em desenvolvimento",
            f"A função '{nome_funcao}' será criada na próxima etapa."
        )

    def refresh(self):
        pass



class OrdemServicoFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        self.cliente_os_id = None

        self.busca_cliente_os_var = tk.StringVar()
        self.busca_cliente_os_var.trace_add("write", self._maiusculo_busca_placa_os)
        self.orcamento_os_var = tk.StringVar(value="Selecione um orçamento...")
        self.orcamento_arquivo_path = None
        self.mao_obra_os_var = tk.StringVar(value="0,00")

        self.os_nome_var = tk.StringVar(value="-")
        self.os_cpf_var = tk.StringVar(value="-")
        self.os_telefone_var = tk.StringVar(value="-")
        self.os_veiculo_var = tk.StringVar(value="-")
        self.os_placa_var = tk.StringVar(value="-")
        self.os_cidade_var = tk.StringVar(value="-")

        self.os_total_pecas_var = tk.StringVar(value="R$ 0,00")
        self.os_total_servicos_var = tk.StringVar(value="R$ 0,00")
        self.os_total_geral_var = tk.StringVar(value="R$ 0,00")

        self._montar_ordem_servico()

    def _maiusculo_busca_placa_os(self, *args):
        texto = self.busca_cliente_os_var.get()
        texto_maiusculo = texto.upper()

        if texto != texto_maiusculo:
            self.busca_cliente_os_var.set(texto_maiusculo)


    def _botao_os(self, parent, texto, cor, comando, padx=12, pady=5, largura=None):
        return tk.Button(
            parent,
            text=texto,
            command=comando,
            bg=cor,
            fg="white",
            activebackground=cor,
            activeforeground="white",
            bd=0,
            padx=padx,
            pady=pady,
            width=largura if largura else 0,
            font=("Segoe UI", 9, "bold"),
            cursor="hand2",
        )

    def _montar_ordem_servico(self):
        tk.Label(
            self,
            text="Ordem de Serviço",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=10, pady=(0, 8))

        # Mesmo limite visual da tela de Orçamento.
        # Não usa expand=True para não esticar o container principal.
        self.os_card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            width=900,
            height=520,
        )
        self.os_card.pack(anchor="w", padx=10, pady=(0, 14))
        self.os_card.pack_propagate(False)

        self._montar_topo_busca_os()
        self._montar_itens_os()
        self._montar_botoes_finais_os()

    def _montar_topo_busca_os(self):
        topo = tk.Frame(
            self.os_card,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            height=102,
        )
        topo.pack(fill="x", padx=16, pady=(12, 8))
        topo.pack_propagate(False)

        esquerda = tk.Frame(topo, bg="white")
        esquerda.pack(side="left", fill="both", expand=True, padx=(14, 10), pady=10)

        direita = tk.Frame(topo, bg="white")
        direita.pack(side="right", fill="both", expand=True, padx=(10, 14), pady=10)

        tk.Label(
            esquerda,
            text="🔵  1 - BUSCAR CLIENTE",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            esquerda,
            text="Informe a placa do veículo",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(3, 6))

        linha_cliente = tk.Frame(esquerda, bg="white")
        linha_cliente.pack(fill="x")

        self.busca_cliente_os_entry = tk.Entry(
            linha_cliente,
            textvariable=self.busca_cliente_os_var,
            font=("Segoe UI", 9),
            relief="solid",
            bd=1,
        )
        self.busca_cliente_os_entry.pack(side="left", fill="x", expand=True, ipady=5)
        self.busca_cliente_os_entry.bind("<Return>", lambda event: self.buscar_cliente_os())

        self._botao_os(
            linha_cliente,
            "🔍 Buscar Cliente",
            "#0b63ce",
            self.buscar_cliente_os,
            padx=10,
            pady=6,
        ).pack(side="left", padx=(8, 0))

        tk.Label(
            direita,
            text="📄  2 - BUSCAR ORÇAMENTO",
            bg="white",
            fg="#08803a",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w")

        tk.Label(
            direita,
            text="Após selecionar o cliente",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 8),
        ).pack(anchor="w", pady=(3, 6))

        linha_orcamento = tk.Frame(direita, bg="white")
        linha_orcamento.pack(fill="x")

        self.combo_orcamentos_os = ttk.Combobox(
            linha_orcamento,
            textvariable=self.orcamento_os_var,
            values=["Selecione um orçamento..."],
            state="readonly",
            font=("Segoe UI", 9),
        )
        self.combo_orcamentos_os.pack(side="left", fill="x", expand=True, ipady=4)
        self.combo_orcamentos_os.bind("<Button-1>", self.abrir_pasta_orcamentos)

    def abrir_pasta_orcamentos(self, event=None):
        placa_base = self.os_placa_var.get().strip()

        if not placa_base or placa_base == "-":
            placa_base = self.busca_cliente_os_var.get().strip()

        placa = "".join(ch for ch in placa_base.upper() if ch.isalnum())

        if not placa:
            messagebox.showwarning(
                "Atenção",
                "Busque um cliente/veículo antes de buscar o orçamento."
            )
            return "break"

        pasta_orcamentos = os.path.join(os.path.dirname(__file__), "orcamentos")

        if not os.path.exists(pasta_orcamentos):
            messagebox.showwarning(
                "Atenção",
                "A pasta de orçamentos ainda não existe."
            )
            return "break"

        arquivos_encontrados = []

        try:
            for nome_arquivo in os.listdir(pasta_orcamentos):
                nome_maiusculo = nome_arquivo.upper()

                if not nome_maiusculo.lower().endswith((".jpg", ".jpeg")):
                    continue

                nome_sem_extensao = os.path.splitext(nome_maiusculo)[0]
                nome_limpo = "".join(ch for ch in nome_sem_extensao if ch.isalnum())

                if nome_limpo.startswith(placa):
                    caminho_completo = os.path.join(pasta_orcamentos, nome_arquivo)
                    arquivos_encontrados.append(caminho_completo)

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível buscar orçamento na pasta:\n{e}"
            )
            return "break"

        if not arquivos_encontrados:
            messagebox.showwarning(
                "Atenção",
                "Nenhum orçamento encontrado para esta placa."
            )
            return "break"

        caminho_orcamento = max(
            arquivos_encontrados,
            key=lambda caminho: os.path.getmtime(caminho)
        )

        self.orcamento_arquivo_path = caminho_orcamento
        nome_arquivo = os.path.basename(caminho_orcamento)
        self.orcamento_os_var.set(nome_arquivo)

        self.carregar_itens_orcamento_json(caminho_orcamento)

        messagebox.showinfo(
            "Orçamento encontrado",
            "O último orçamento desta placa foi selecionado automaticamente:\n\n"
            f"{nome_arquivo}"
        )

        return "break"


    def _montar_itens_os(self):
        itens = tk.Frame(
            self.os_card,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            height=360,
        )
        itens.pack(fill="x", padx=16, pady=(0, 8))
        itens.pack_propagate(False)

        tk.Label(
            itens,
            text="🔧  ITENS DA ORDEM DE SERVIÇO",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 11, "bold"),
        ).pack(anchor="w", padx=14, pady=(8, 6))

        tabela_frame = tk.Frame(
            itens,
            bg="white",
            highlightbackground="#cbd5e1",
            highlightthickness=1,
            height=265,
        )
        tabela_frame.pack(fill="x", padx=14, pady=(0, 6))
        tabela_frame.pack_propagate(False)

        cols = ("quantidade", "descricao", "valor_unitario")
        self.os_tree = ttk.Treeview(
            tabela_frame,
            columns=cols,
            show="headings",
            height=10,
        )

        self.os_tree.heading("quantidade", text="QUANTIDADE", anchor="center")
        self.os_tree.heading("descricao", text="DESCRIÇÃO", anchor="center")
        self.os_tree.heading("valor_unitario", text="VALOR R$", anchor="center")

        self.os_tree.column("quantidade", width=150, minwidth=130, anchor="center", stretch=False)
        self.os_tree.column("descricao", width=520, minwidth=380, anchor="center", stretch=True)
        self.os_tree.column("valor_unitario", width=170, minwidth=180, anchor="center", stretch=False)

        self.os_tree.pack(side="left", fill="both", expand=True)

        scrollbar = ttk.Scrollbar(tabela_frame, orient="vertical", command=self.os_tree.yview)
        self.os_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        self.os_empty_label = tk.Label(
            self.os_tree,
            text="Nenhum item adicionado",
            bg="white",
            fg="#6b7280",
            font=("Segoe UI", 10),
        )
        self.os_tree.bind("<Configure>", lambda event: self._atualizar_mensagem_vazia_os())
        self._atualizar_mensagem_vazia_os()

        botoes = tk.Frame(itens, bg="white")
        botoes.pack(fill="x", padx=14, pady=(0, 0))

        self._botao_os(botoes, "+  Adicionar Item", "#08803a", self.adicionar_item_os, largura=15).pack(side="left", padx=(0, 8))
        self._botao_os(botoes, "✎  Editar Item", "#0b63ce", self.editar_item_os, largura=13).pack(side="left", padx=(0, 8))
        self._botao_os(botoes, "🗑  Excluir Item", "#ef233c", self.excluir_item_os, largura=13).pack(side="left", padx=(0, 8))
        self._botao_os(botoes, "🖨  Imprimir OS", "#6b7280", self.imprimir_os, largura=14).pack(side="left", padx=(0, 8))

    def _total_os_label(self, parent, titulo, var, cor):
        tk.Label(parent, text=titulo, bg="#f8fafc", fg="#111827", font=("Segoe UI", 9, "bold")).pack(side="left", padx=(0, 6))
        tk.Label(parent, textvariable=var, bg="#f8fafc", fg=cor, font=("Segoe UI", 10, "bold")).pack(side="left", padx=(0, 20))


    def _montar_botoes_finais_os(self):
        botoes = tk.Frame(self.os_card, bg="white")
        botoes.pack(fill="x", padx=16, pady=(0, 0))

        self._botao_os(
            botoes,
            "💾  Salvar OS",
            "#08803a",
            self.salvar_os,
            padx=20,
            pady=7,
        ).pack(side="right")

    def _normalizar_busca_os(self, valor):
        return "".join(ch for ch in str(valor or "").upper() if ch.isalnum())

    def buscar_cliente_os(self):
        placa_digitada = self.busca_cliente_os_var.get().strip()
        placa_normalizada = self._normalizar_busca_os(placa_digitada)

        if not placa_normalizada:
            messagebox.showwarning("Atenção", "Digite a placa do veículo.")
            return

        try:
            con = db()
            cur = con.cursor()

            cur.execute(
                """
                SELECT
                    c.id,
                    c.cpf,
                    c.name,
                    c.phone,
                    c.city,
                    v.plate,
                    v.vehicle
                FROM vehicles v
                INNER JOIN clients c ON c.id = v.client_id
                WHERE UPPER(REPLACE(REPLACE(v.plate, '-', ''), ' ', '')) LIKE ?
                ORDER BY c.name
                LIMIT 1
                """,
                (f"{placa_normalizada}%",),
            )

            cliente = cur.fetchone()
            con.close()

            if not cliente:
                messagebox.showwarning(
                    "Placa não encontrada",
                    "Nenhum cliente cadastrado foi encontrado com essa placa."
                )
                return

            self.carregar_cliente_na_os(cliente)

        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível buscar a placa:\n{e}")

    def carregar_cliente_na_os(self, cliente):
        cliente_id, cpf, nome, telefone, cidade, placa, veiculo = cliente

        self.cliente_os_id = cliente_id

        # Mantém os dados salvos internamente para usar depois ao salvar/imprimir a OS.
        self.os_nome_var.set(str(nome or "-").strip().upper())
        self.os_cpf_var.set(str(cpf or "-").strip())
        self.os_telefone_var.set(str(telefone or "-").strip())
        self.os_cidade_var.set(str(cidade or "-").strip().upper())
        self.os_placa_var.set(str(placa or "-").strip().upper())
        self.os_veiculo_var.set(str(veiculo or "-").strip().upper())

        nome_txt = str(nome or "").strip().upper()
        placa_txt = str(placa or "").strip().upper()
        veiculo_txt = str(veiculo or "").strip().upper()

        if placa_txt and veiculo_txt:
            self.busca_cliente_os_var.set(f"{veiculo_txt} - {placa_txt}")
        elif placa_txt:
            self.busca_cliente_os_var.set(placa_txt)
        elif veiculo_txt:
            self.busca_cliente_os_var.set(veiculo_txt)
        else:
            self.busca_cliente_os_var.set(nome_txt)

        self.combo_orcamentos_os.configure(
            values=[
                "Selecione um orçamento...",
                f"Cliente selecionado: {nome_txt} - {veiculo_txt} - {placa_txt}",
            ]
        )
        self.orcamento_os_var.set("Selecione um orçamento...")

        if hasattr(self, "busca_cliente_os_entry"):
            self.busca_cliente_os_entry.focus_set()
            self.busca_cliente_os_entry.icursor(tk.END)



    def carregar_itens_orcamento_json(self, caminho_orcamento):
        try:
            nome_base = os.path.splitext(os.path.basename(caminho_orcamento))[0]
            pasta_dados = os.path.join(os.path.dirname(__file__), "dados_orcamentos")
            caminho_json = os.path.join(pasta_dados, f"{nome_base}.json")

            if not os.path.exists(caminho_json):
                messagebox.showwarning(
                    "Atenção",
                    "O orçamento foi encontrado, mas os dados dos itens não foram localizados.\\n\\n"
                    "Esse orçamento provavelmente foi criado antes da integração com JSON."
                )
                return

            with open(caminho_json, "r", encoding="utf-8") as arquivo:
                dados_orcamento = json.load(arquivo)

            itens = dados_orcamento.get("itens", [])

            for item in self.os_tree.get_children():
                self.os_tree.delete(item)

            for item in itens:
                quantidade = str(item.get("quantidade", "")).strip()
                descricao = str(item.get("descricao", "")).strip().upper()
                valor_unitario = str(item.get("valor_unitario", "")).strip()

                if not quantidade or not descricao:
                    continue

                valor_unitario_fmt = self._formatar_valor_digitado_os(valor_unitario)

                self.os_tree.insert(
                    "",
                    "end",
                    values=(quantidade, descricao, valor_unitario_fmt)
                )

            mao_obra = str(dados_orcamento.get("mao_de_obra", "")).replace("R$", "").strip()
            if mao_obra:
                self.mao_obra_os_var.set(mao_obra)

            self.atualizar_totais_os()
            self._atualizar_mensagem_vazia_os()

        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Não foi possível carregar os itens do orçamento:\\n{e}"
            )


    def buscar_orcamento_os(self):
        if not self.cliente_os_id:
            messagebox.showwarning("Atenção", "Busque e selecione um cliente primeiro.")
            return

        messagebox.showinfo("Orçamento", "Busca de orçamento será integrada na próxima etapa.")

    def limpar_cliente_os(self):
        self.cliente_os_id = None
        self.busca_cliente_os_var.set("")
        self.orcamento_os_var.set("Selecione um orçamento...")
        self.combo_orcamentos_os.configure(values=["Selecione um orçamento..."])

        for var in (
            self.os_nome_var,
            self.os_cpf_var,
            self.os_telefone_var,
            self.os_veiculo_var,
            self.os_placa_var,
            self.os_cidade_var,
        ):
            var.set("-")

    def _valor_para_float_os(self, valor):
        texto = str(valor or "").replace("R$", "").replace(".", "").replace(",", ".").strip()
        try:
            return float(texto) if texto else 0.0
        except Exception:
            return 0.0

    def _formatar_moeda_os(self, valor):
        return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _formatar_valor_digitado_os(self, valor):
        texto = "".join(ch for ch in str(valor or "") if ch.isdigit())
        if not texto:
            return "0,00"
        numero = int(texto) / 100
        return f"{numero:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

    def _formatar_mao_obra_os(self):
        self.mao_obra_os_var.set(self._formatar_valor_digitado_os(self.mao_obra_os_var.get()))
        self.atualizar_totais_os()

    def adicionar_item_os(self):
        ItemOSDialog(self, titulo="Adicionar Item")

    def editar_item_os(self):
        selecionado = self.os_tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um item para editar.")
            return

        valores = self.os_tree.item(selecionado[0], "values")
        ItemOSDialog(self, titulo="Editar Item", item_id=selecionado[0], valores=valores)

    def excluir_item_os(self):
        selecionado = self.os_tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um item para excluir.")
            return

        if not messagebox.askyesno("Confirmar exclusão", "Deseja realmente excluir este item?"):
            return

        self.os_tree.delete(selecionado[0])
        self.atualizar_totais_os()
        self._atualizar_mensagem_vazia_os()

    def limpar_itens_os(self):
        if not self.os_tree.get_children():
            return

        if not messagebox.askyesno("Confirmar limpeza", "Deseja remover todos os itens da ordem de serviço?"):
            return

        for item in self.os_tree.get_children():
            self.os_tree.delete(item)

        self.atualizar_totais_os()
        self._atualizar_mensagem_vazia_os()

    def salvar_item_os(self, quantidade, descricao, valor_unitario, item_id=None):
        quantidade = str(quantidade).strip()
        descricao = str(descricao).strip().upper()
        valor_unitario = str(valor_unitario).strip()

        if not quantidade or not quantidade.isdigit():
            messagebox.showwarning("Atenção", "Informe uma quantidade válida.")
            return False

        if not descricao:
            messagebox.showwarning("Atenção", "Informe a descrição.")
            return False

        valor_unitario_fmt = self._formatar_valor_digitado_os(valor_unitario)

        valores = (quantidade, descricao, valor_unitario_fmt)

        if item_id:
            self.os_tree.item(item_id, values=valores)
        else:
            self.os_tree.insert("", "end", values=valores)

        self.atualizar_totais_os()
        self._atualizar_mensagem_vazia_os()
        return True

    def atualizar_totais_os(self):
        total_pecas = 0.0

        for item in self.os_tree.get_children():
            valores = self.os_tree.item(item, "values")
            if len(valores) >= 3:
                try:
                    quantidade = int(str(valores[0]).strip() or "0")
                except Exception:
                    quantidade = 0

                valor_unitario = self._valor_para_float_os(valores[2])
                total_pecas += quantidade * valor_unitario

        mao_obra = self._valor_para_float_os(self.mao_obra_os_var.get())
        total_servicos = mao_obra
        total_geral = total_pecas + total_servicos

        self.os_total_pecas_var.set(self._formatar_moeda_os(total_pecas))
        self.os_total_servicos_var.set(self._formatar_moeda_os(total_servicos))
        self.os_total_geral_var.set(self._formatar_moeda_os(total_geral))

    def _atualizar_mensagem_vazia_os(self):
        if self.os_tree.get_children():
            self.os_empty_label.place_forget()
        else:
            self.os_empty_label.place(relx=0.5, rely=0.5, anchor="center")

    def imprimir_os(self):
        messagebox.showinfo("Em desenvolvimento", "A impressão da OS será criada na próxima etapa.")

    def salvar_os(self):
        if not self.cliente_os_id:
            messagebox.showwarning("Atenção", "Selecione um cliente antes de salvar a OS.")
            return

        messagebox.showinfo("Sucesso", "Ordem de Serviço pronta para salvar no banco na próxima etapa.")

    def refresh(self):
        pass


class ItemOSDialog(tk.Toplevel):
    def __init__(self, parent, titulo="Adicionar Item", item_id=None, valores=None):
        super().__init__(parent)
        self.parent = parent
        self.item_id = item_id

        self.title(titulo)
        largura_janela = 400
        altura_janela = 360
        self.geometry(f"{largura_janela}x{altura_janela}")
        self.resizable(False, False)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        self.quantidade_var = tk.StringVar(value=valores[0] if valores else "")
        self.descricao_var = tk.StringVar(value=valores[1] if valores else "")
        self.valor_var = tk.StringVar(value=valores[2] if valores else "")

        self.descricao_var.trace_add("write", lambda *args: self._maiusculo_var(self.descricao_var))

        frame = tk.Frame(self, bg="#f5f6f8", padx=20, pady=18)
        frame.pack(fill="both", expand=True)

        tk.Label(
            frame,
            text=titulo,
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", pady=(0, 12))

        self._campo(frame, "Quantidade:", self.quantidade_var)
        self._campo(frame, "Descrição do Serviço / Peça:", self.descricao_var)
        self._campo(frame, "Valor:", self.valor_var)

        botoes = tk.Frame(frame, bg="#f5f6f8")
        botoes.pack(fill="x", pady=(12, 0))

        tk.Button(
            botoes,
            text="Salvar",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            command=self.salvar,
        ).pack(side="left", padx=(0, 10))

        tk.Button(
            botoes,
            text="Cancelar",
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=16,
            pady=6,
            font=("Segoe UI", 10, "bold"),
            command=self.destroy,
        ).pack(side="left")

        self.update_idletasks()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura_janela // 2)
        y = (sh // 2) - (altura_janela // 2)
        self.geometry(f"{largura_janela}x{altura_janela}+{x}+{y}")

    def _campo(self, parent, label, var):
        tk.Label(
            parent,
            text=label,
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 10, "bold"),
        ).pack(anchor="w")

        entrada = tk.Entry(
            parent,
            textvariable=var,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        entrada.pack(fill="x", pady=(4, 8), ipady=4)
        return entrada

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def salvar(self):
        ok = self.parent.salvar_item_os(
            self.quantidade_var.get(),
            self.descricao_var.get(),
            self.valor_var.get(),
            self.item_id,
        )

        if ok:
            self.destroy()



class NotasFiscaisFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        tk.Label(
            self,
            text="Notas Fiscais",
            bg="#f5f6f8",
            fg="#111827",
            font=("Segoe UI", 20, "bold"),
        ).pack(anchor="w", padx=10, pady=(0, 10))

        main_card = tk.Frame(
            self,
            bg="white",
            highlightbackground="#d7dce2",
            highlightthickness=1,
            width=900,
            height=520,
        )
        main_card.pack(anchor="w", padx=10, pady=(0, 14))
        main_card.pack_propagate(False)

        tk.Label(
            main_card,
            text="🧾  EMISSÃO DE NOTAS FISCAIS",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 13, "bold"),
        ).pack(anchor="w", padx=22, pady=(18, 8))

        tk.Label(
            main_card,
            text="Área preparada para emissão e controle de NF-e de produtos e NFS-e de serviços.",
            bg="white",
            fg="#374151",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=22, pady=(0, 14))

        cards = tk.Frame(main_card, bg="white")
        cards.pack(fill="x", padx=22, pady=(0, 16))

        self._card_nota(
            cards,
            "📦  NF-e de Produtos",
            "Venda de peças/produtos com certificado digital.",
            "#0b63ce",
        ).pack(side="left", fill="both", expand=True, padx=(0, 12))

        self._card_nota(
            cards,
            "🔧  NFS-e de Serviços",
            "Serviços emitidos pelo site da prefeitura com login e senha.",
            "#08803a",
        ).pack(side="left", fill="both", expand=True, padx=(12, 0))

        resumo = tk.Frame(
            main_card,
            bg="#f8fafc",
            highlightbackground="#e5e7eb",
            highlightthickness=1,
            height=170,
        )
        resumo.pack(fill="x", padx=22, pady=(0, 16))
        resumo.pack_propagate(False)

        tk.Label(
            resumo,
            text="📋  Informações pendentes da contadora",
            bg="#f8fafc",
            fg="#111827",
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=18, pady=(14, 6))

        pendencias = (
            "• Dados fiscais obrigatórios para NF-e\n"
            "• Regras de CFOP, NCM, CST/CSOSN e impostos\n"
            "• Dados da empresa emitente\n"
            "• Forma de integração com SEFAZ e prefeitura\n"
            "• Tipo do certificado digital utilizado"
        )

        tk.Label(
            resumo,
            text=pendencias,
            bg="#f8fafc",
            fg="#374151",
            justify="left",
            font=("Segoe UI", 10),
        ).pack(anchor="w", padx=18)

        botoes = tk.Frame(main_card, bg="white")
        botoes.pack(fill="x", padx=22)

        tk.Button(
            botoes,
            text="📦  Emitir NF-e Produto",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            command=self.abrir_cadastro_nfe_produto,
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            botoes,
            text="🔧  Preparar NFS-e Serviço",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            command=lambda: messagebox.showinfo(
                "Em desenvolvimento",
                "A preparação da NFS-e será implementada após definirmos os dados exigidos pela prefeitura."
            ),
        ).pack(side="left")

    def _card_nota(self, parent, titulo, descricao, cor):
        card = tk.Frame(
            parent,
            bg="#f8fafc",
            highlightbackground="#e5e7eb",
            highlightthickness=1,
            height=105,
        )
        card.pack_propagate(False)

        tk.Label(
            card,
            text=titulo,
            bg="#f8fafc",
            fg=cor,
            font=("Segoe UI", 12, "bold"),
        ).pack(anchor="w", padx=16, pady=(14, 6))

        tk.Label(
            card,
            text=descricao,
            bg="#f8fafc",
            fg="#374151",
            font=("Segoe UI", 10),
            wraplength=360,
            justify="left",
        ).pack(anchor="w", padx=16)

        return card

    def abrir_cadastro_nfe_produto(self):
        CadastroNFeProdutoDialog(self)

    def refresh(self):
        pass


class CadastroNFeProdutoDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.produtos = []

        self.title("Cadastro de NF-e de Produto")
        self.geometry("980x680")
        self.minsize(900, 620)
        self.configure(bg="#f5f6f8")
        self.grab_set()

        self._criar_variaveis()
        self._montar_tela()
        self._centralizar()

    def _criar_variaveis(self):
        agora = datetime.now()

        self.modelo_var = tk.StringVar(value="55 - NF-e")
        self.serie_var = tk.StringVar()
        self.numero_var = tk.StringVar()
        self.data_emissao_var = tk.StringVar(value=agora.strftime("%d/%m/%Y"))
        self.hora_emissao_var = tk.StringVar(value=agora.strftime("%H:%M"))
        self.tipo_documento_var = tk.StringVar(value="Saída")
        self.finalidade_var = tk.StringVar(value="Normal")
        self.consumidor_final_var = tk.StringVar(value="Sim")
        self.destino_operacao_var = tk.StringVar(value="Operação interna")
        self.natureza_operacao_var = tk.StringVar()

        self.emitente_doc_var = tk.StringVar()
        self.emitente_nome_var = tk.StringVar()
        self.emitente_ie_var = tk.StringVar()
        self.emitente_endereco_var = tk.StringVar()
        self.emitente_cep_var = tk.StringVar()

        self.destinatario_doc_var = tk.StringVar()
        self.destinatario_nome_var = tk.StringVar()
        self.destinatario_ie_var = tk.StringVar()
        self.destinatario_endereco_var = tk.StringVar()
        self.destinatario_cep_var = tk.StringVar()

        self.prod_codigo_var = tk.StringVar()
        self.prod_descricao_var = tk.StringVar()
        self.prod_ncm_var = tk.StringVar()
        self.prod_cfop_var = tk.StringVar()
        self.prod_unidade_var = tk.StringVar(value="UN")
        self.prod_quantidade_var = tk.StringVar(value="1")
        self.prod_valor_unitario_var = tk.StringVar()
        self.prod_situacao_tributaria_var = tk.StringVar()
        self.prod_origem_var = tk.StringVar(value="0 - Nacional")

        self.modalidade_frete_var = tk.StringVar(value="Sem frete")
        self.pagamento_var = tk.StringVar()

        for var in (
            self.natureza_operacao_var,
            self.emitente_nome_var,
            self.emitente_endereco_var,
            self.destinatario_nome_var,
            self.destinatario_endereco_var,
            self.prod_descricao_var,
            self.prod_situacao_tributaria_var,
            self.pagamento_var,
        ):
            var.trace_add("write", lambda *args, v=var: self._maiusculo_var(v))

    def _montar_tela(self):
        topo = tk.Frame(self, bg="#111827", height=64)
        topo.pack(fill="x")
        topo.pack_propagate(False)

        tk.Label(
            topo,
            text="📦  Cadastro de NF-e de Produto",
            bg="#111827",
            fg="white",
            font=("Segoe UI", 16, "bold"),
        ).pack(side="left", padx=22)

        tk.Button(
            topo,
            text="Fechar",
            bg="#374151",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=6,
            command=self.destroy,
        ).pack(side="right", padx=22)

        area = tk.Frame(self, bg="#f5f6f8")
        area.pack(fill="both", expand=True)

        canvas = tk.Canvas(area, bg="#f5f6f8", highlightthickness=0)
        barra = ttk.Scrollbar(area, orient="vertical", command=canvas.yview)
        self.conteudo = tk.Frame(canvas, bg="#f5f6f8")

        self.conteudo.bind(
            "<Configure>",
            lambda event: canvas.configure(scrollregion=canvas.bbox("all")),
        )

        janela = canvas.create_window((0, 0), window=self.conteudo, anchor="nw")
        canvas.configure(yscrollcommand=barra.set)
        canvas.bind("<Configure>", lambda event: canvas.itemconfig(janela, width=event.width))

        canvas.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")

        self._secao_dados_nota()
        self._secao_emitente_destinatario()
        self._secao_produto()
        self._secao_frete_pagamento()
        self._secao_botoes()

    def _card(self, titulo):
        card = tk.LabelFrame(
            self.conteudo,
            text=titulo,
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=14,
            highlightbackground="#d7dce2",
            highlightthickness=1,
        )
        card.pack(fill="x", padx=18, pady=(14, 0))
        return card

    def _campo(self, parent, label, var, row, col, width=28, combo=None):
        box = tk.Frame(parent, bg="white")
        box.grid(row=row, column=col, sticky="w", padx=(0, 18), pady=(0, 12))

        tk.Label(
            box,
            text=label,
            bg="white",
            fg="#111827",
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w")

        if combo:
            entrada = ttk.Combobox(
                box,
                textvariable=var,
                values=combo,
                width=width,
                state="readonly",
                font=("Segoe UI", 10),
            )
        else:
            entrada = tk.Entry(
                box,
                textvariable=var,
                width=width,
                font=("Segoe UI", 10),
                relief="solid",
                bd=1,
            )

        entrada.pack(fill="x", pady=(4, 0), ipady=4)
        return entrada

    def _secao_dados_nota(self):
        card = self._card("1. Dados da nota fiscal")

        self._campo(card, "Modelo:", self.modelo_var, 0, 0, combo=["55 - NF-e", "65 - NFC-e"])
        self._campo(card, "Série:", self.serie_var, 0, 1)
        self._campo(card, "Número:", self.numero_var, 0, 2)
        self._campo(card, "Data de emissão:", self.data_emissao_var, 1, 0)
        self._campo(card, "Hora de emissão:", self.hora_emissao_var, 1, 1)
        self._campo(card, "Tipo de documento:", self.tipo_documento_var, 1, 2, combo=["Entrada", "Saída"])
        self._campo(card, "Finalidade:", self.finalidade_var, 2, 0, combo=["Normal", "Complementar", "Ajuste", "Devolução"])
        self._campo(card, "Consumidor final:", self.consumidor_final_var, 2, 1, combo=["Sim", "Não"])
        self._campo(card, "Destino da operação:", self.destino_operacao_var, 2, 2, combo=["Operação interna", "Interestadual", "Exterior"])
        self._campo(card, "Natureza da operação:", self.natureza_operacao_var, 3, 0, width=82)

    def _secao_emitente_destinatario(self):
        bloco = tk.Frame(self.conteudo, bg="#f5f6f8")
        bloco.pack(fill="x", padx=18, pady=(14, 0))

        emitente = tk.LabelFrame(
            bloco,
            text="2. Dados do emitente",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=14,
        )
        emitente.pack(side="left", fill="both", expand=True, padx=(0, 8))

        destinatario = tk.LabelFrame(
            bloco,
            text="3. Dados do destinatário",
            bg="white",
            fg="#0b63ce",
            font=("Segoe UI", 11, "bold"),
            padx=16,
            pady=14,
        )
        destinatario.pack(side="left", fill="both", expand=True, padx=(8, 0))

        self._campo(emitente, "CNPJ/CPF:", self.emitente_doc_var, 0, 0, width=34)
        self._campo(emitente, "Nome/Razão social:", self.emitente_nome_var, 1, 0, width=34)
        self._campo(emitente, "Inscrição estadual:", self.emitente_ie_var, 2, 0, width=34)
        self._campo(emitente, "Endereço com número:", self.emitente_endereco_var, 3, 0, width=34)
        self._campo(emitente, "CEP:", self.emitente_cep_var, 4, 0, width=34)

        self._campo(destinatario, "CNPJ/CPF:", self.destinatario_doc_var, 0, 0, width=34)
        self._campo(destinatario, "Nome/Razão social:", self.destinatario_nome_var, 1, 0, width=34)
        self._campo(destinatario, "Inscrição estadual:", self.destinatario_ie_var, 2, 0, width=34)
        self._campo(destinatario, "Endereço com número:", self.destinatario_endereco_var, 3, 0, width=34)
        self._campo(destinatario, "CEP:", self.destinatario_cep_var, 4, 0, width=34)

    def _secao_produto(self):
        card = self._card("4. Dados do produto")

        self._campo(card, "Código:", self.prod_codigo_var, 0, 0)
        self._campo(card, "Descrição:", self.prod_descricao_var, 0, 1, width=38)
        self._campo(card, "NCM:", self.prod_ncm_var, 0, 2)
        self._campo(card, "CFOP:", self.prod_cfop_var, 1, 0)
        self._campo(card, "Unidade comercial:", self.prod_unidade_var, 1, 1, combo=["UN", "PC", "KG", "LT", "CX", "M"])
        self._campo(card, "Quantidade:", self.prod_quantidade_var, 1, 2)
        self._campo(card, "Valor unitário:", self.prod_valor_unitario_var, 2, 0)
        self._campo(card, "Situação tributária:", self.prod_situacao_tributaria_var, 2, 1, width=38)
        self._campo(card, "Origem:", self.prod_origem_var, 2, 2, combo=["0 - Nacional", "1 - Estrangeira importação direta", "2 - Estrangeira mercado interno"])

        tk.Button(
            card,
            text="➕  Adicionar produto na nota",
            bg="#08803a",
            fg="white",
            activebackground="#06632d",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=6,
            font=("Segoe UI", 9, "bold"),
            command=self.adicionar_produto,
        ).grid(row=3, column=0, sticky="w", pady=(0, 10))

        cols = ("codigo", "descricao", "ncm", "cfop", "un", "qtd", "valor", "total")
        self.produtos_tree = ttk.Treeview(card, columns=cols, show="headings", height=5)

        colunas = [
            ("codigo", "Código", 90),
            ("descricao", "Descrição", 220),
            ("ncm", "NCM", 90),
            ("cfop", "CFOP", 80),
            ("un", "UN", 60),
            ("qtd", "Qtd", 70),
            ("valor", "Valor unit.", 100),
            ("total", "Total", 110),
        ]

        for col, titulo, largura in colunas:
            self.produtos_tree.heading(col, text=titulo)
            self.produtos_tree.column(col, width=largura, anchor="w")

        self.produtos_tree.grid(row=4, column=0, columnspan=3, sticky="ew", pady=(0, 6))

        tk.Button(
            card,
            text="🗑  Remover produto selecionado",
            bg="#dc2626",
            fg="white",
            activebackground="#991b1b",
            activeforeground="white",
            bd=0,
            padx=14,
            pady=6,
            font=("Segoe UI", 9, "bold"),
            command=self.remover_produto,
        ).grid(row=5, column=0, sticky="w")

    def _secao_frete_pagamento(self):
        card = self._card("5. Frete, pagamento e informações complementares")

        self._campo(card, "Modalidade do frete:", self.modalidade_frete_var, 0, 0, combo=["Sem frete", "Por conta do emitente", "Por conta do destinatário", "Terceiros"])
        self._campo(card, "Informações de pagamento:", self.pagamento_var, 0, 1, width=56)

        tk.Label(
            card,
            text="Informações complementares:",
            bg="white",
            fg="#111827",
            font=("Segoe UI", 9, "bold"),
        ).grid(row=1, column=0, columnspan=3, sticky="w")

        self.complementares_txt = tk.Text(
            card,
            width=100,
            height=5,
            font=("Segoe UI", 10),
            relief="solid",
            bd=1,
        )
        self.complementares_txt.grid(row=2, column=0, columnspan=3, sticky="ew", pady=(4, 0))

    def _secao_botoes(self):
        botoes = tk.Frame(self.conteudo, bg="#f5f6f8")
        botoes.pack(fill="x", padx=18, pady=18)

        tk.Button(
            botoes,
            text="💾  Salvar cadastro da nota",
            bg="#0b63ce",
            fg="white",
            activebackground="#084ea3",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            command=self.salvar_cadastro,
        ).pack(side="left", padx=(0, 12))

        tk.Button(
            botoes,
            text="🧹  Limpar tela",
            bg="#6b7280",
            fg="white",
            activebackground="#4b5563",
            activeforeground="white",
            bd=0,
            padx=18,
            pady=8,
            font=("Segoe UI", 10, "bold"),
            command=self.limpar_tela,
        ).pack(side="left")

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)

    def _converter_valor(self, valor):
        texto = str(valor or "").strip().replace("R$", "").replace(".", "").replace(",", ".")
        try:
            return float(texto)
        except ValueError:
            return None

    def _formatar_moeda(self, valor):
        return f"R$ {valor:.2f}".replace(".", ",")

    def adicionar_produto(self):
        codigo = self.prod_codigo_var.get().strip().upper()
        descricao = self.prod_descricao_var.get().strip().upper()
        ncm = self.prod_ncm_var.get().strip()
        cfop = self.prod_cfop_var.get().strip()
        unidade = self.prod_unidade_var.get().strip().upper()
        quantidade = self._converter_valor(self.prod_quantidade_var.get())
        valor_unitario = self._converter_valor(self.prod_valor_unitario_var.get())

        if not codigo or not descricao:
            messagebox.showwarning("Atenção", "Informe pelo menos o código e a descrição do produto.")
            return

        if quantidade is None or quantidade <= 0:
            messagebox.showwarning("Atenção", "Informe uma quantidade válida.")
            return

        if valor_unitario is None or valor_unitario < 0:
            messagebox.showwarning("Atenção", "Informe um valor unitário válido.")
            return

        total = quantidade * valor_unitario
        produto = {
            "codigo": codigo,
            "descricao": descricao,
            "ncm": ncm,
            "cfop": cfop,
            "unidade": unidade,
            "quantidade": quantidade,
            "valor_unitario": valor_unitario,
            "situacao_tributaria": self.prod_situacao_tributaria_var.get().strip().upper(),
            "origem": self.prod_origem_var.get().strip(),
            "total": total,
        }
        self.produtos.append(produto)

        self.produtos_tree.insert(
            "",
            "end",
            values=(
                codigo,
                descricao,
                ncm,
                cfop,
                unidade,
                str(quantidade).replace(".", ","),
                self._formatar_moeda(valor_unitario),
                self._formatar_moeda(total),
            ),
        )

        self.prod_codigo_var.set("")
        self.prod_descricao_var.set("")
        self.prod_ncm_var.set("")
        self.prod_cfop_var.set("")
        self.prod_quantidade_var.set("1")
        self.prod_valor_unitario_var.set("")
        self.prod_situacao_tributaria_var.set("")

    def remover_produto(self):
        selecionado = self.produtos_tree.selection()
        if not selecionado:
            messagebox.showwarning("Atenção", "Selecione um produto para remover.")
            return

        item = selecionado[0]
        indice = self.produtos_tree.index(item)
        self.produtos_tree.delete(item)

        if 0 <= indice < len(self.produtos):
            self.produtos.pop(indice)

    def salvar_cadastro(self):
        obrigatorios = [
            ("Natureza da operação", self.natureza_operacao_var.get()),
            ("CNPJ/CPF do emitente", self.emitente_doc_var.get()),
            ("Nome do emitente", self.emitente_nome_var.get()),
            ("CNPJ/CPF do destinatário", self.destinatario_doc_var.get()),
            ("Nome do destinatário", self.destinatario_nome_var.get()),
        ]

        for nome, valor in obrigatorios:
            if not str(valor).strip():
                messagebox.showwarning("Atenção", f"Preencha o campo: {nome}.")
                return

        if not self.produtos:
            messagebox.showwarning("Atenção", "Adicione pelo menos um produto na nota.")
            return

        total = sum(produto["total"] for produto in self.produtos)

        messagebox.showinfo(
            "Cadastro salvo",
            "Cadastro da NF-e de produto preenchido com sucesso.\n\n"
            f"Produtos adicionados: {len(self.produtos)}\n"
            f"Total da nota: {self._formatar_moeda(total)}\n\n"
            "Nesta primeira etapa os dados ficam apenas na tela.\n"
            "Na próxima etapa vamos criar as tabelas no banco e salvar esse cadastro definitivamente."
        )

    def limpar_tela(self):
        confirmar = messagebox.askyesno("Confirmar", "Deseja limpar todos os campos da nota?")
        if not confirmar:
            return

        self.destroy()
        CadastroNFeProdutoDialog(self.parent)

    def _centralizar(self):
        self.update_idletasks()
        largura = self.winfo_width()
        altura = self.winfo_height()
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = (sw // 2) - (largura // 2)
        y = (sh // 2) - (altura // 2)
        self.geometry(f"{largura}x{altura}+{x}+{y}")


class OrdersFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        top = tk.Frame(self, bg="#f5f6f8")
        top.pack(fill="x")
        tk.Label(
            top,
            text="Orçamentos / Ordens de Serviço",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")
        tk.Button(top, text="Nova OS", command=self.new_order).pack(side="right")

        cols = ("id", "cliente", "data", "status", "total")
        self.tree = ttk.Treeview(self, columns=cols, show="headings")
        for c, t, w in [
            ("id", "OS", 80),
            ("cliente", "Cliente", 260),
            ("data", "Data", 120),
            ("status", "Status", 140),
            ("total", "Total", 120),
        ]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor="w")
        self.tree.pack(fill="both", expand=True, pady=10)

        actions = tk.Frame(self, bg="#f5f6f8")
        actions.pack(fill="x")
        tk.Button(actions, text="Abrir", command=self.open_selected).pack(side="left")
        tk.Button(actions, text="Excluir", command=self.delete_selected).pack(side="left", padx=8)

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def new_order(self):
        OrderEditor(self, order_id=None, on_close=self.refresh)

    def open_selected(self):
        oid = self._selected_id()
        if not oid:
            messagebox.showwarning("Atenção", "Selecione uma OS.")
            return
        OrderEditor(self, order_id=oid, on_close=self.refresh)

    def delete_selected(self):
        oid = self._selected_id()
        if not oid:
            messagebox.showwarning("Atenção", "Selecione uma OS.")
            return
        if not messagebox.askyesno("Confirmar", "Excluir esta OS e itens?"):
            return
        con = db()
        cur = con.cursor()
        cur.execute("DELETE FROM order_items WHERE order_id=?", (oid,))
        cur.execute("DELETE FROM orders WHERE id=?", (oid,))
        con.commit()
        con.close()
        self.refresh()

    def refresh(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT o.id, COALESCE(c.name,'(sem cliente)'), o.date, o.status, o.total
            FROM orders o
            LEFT JOIN clients c ON c.id = o.client_id
            ORDER BY o.id DESC
            """
        )
        for row in cur.fetchall():
            self.tree.insert(
                "",
                "end",
                values=(row[0], row[1], row[2], row[3], f"R$ {row[4]:.2f}".replace(".", ",")),
            )
        con.close()

class FinanceFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        tk.Label(
            self,
            text="Financeiro (simples)",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 18, "bold"),
        ).pack(anchor="w")

        hint = (
            "Nesta versão, o financeiro lê o total das OS por status.\n"
            "Depois a gente adiciona: pagamentos (PIX/dinheiro/cartão), período, relatório e PDF."
        )
        tk.Label(
            self,
            text=hint,
            bg="#f5f6f8",
            fg="#6b7280",
            justify="left",
        ).pack(anchor="w", pady=(6, 12))

        self.box = tk.LabelFrame(
            self,
            text="Resumo",
            bg="#f5f6f8",
            fg="#374151",
            font=("Segoe UI", 10, "bold"),
        )
        self.box.pack(fill="x")

        self.lbl_aberta = tk.Label(self.box, bg="#f5f6f8", font=("Segoe UI", 11))
        self.lbl_andamento = tk.Label(self.box, bg="#f5f6f8", font=("Segoe UI", 11))
        self.lbl_finalizada = tk.Label(self.box, bg="#f5f6f8", font=("Segoe UI", 11))
        self.lbl_paga = tk.Label(self.box, bg="#f5f6f8", font=("Segoe UI", 11))

        for w in (
            self.lbl_aberta,
            self.lbl_andamento,
            self.lbl_finalizada,
            self.lbl_paga,
        ):
            w.pack(anchor="w", padx=10, pady=3)

        tk.Button(self, text="Atualizar", command=self.refresh).pack(anchor="w", pady=10)

    def refresh(self):
        con = db()
        cur = con.cursor()

        def sum_status(status):
            cur.execute("SELECT COALESCE(SUM(total),0) FROM orders WHERE status=?", (status,))
            return float(cur.fetchone()[0] or 0)

        aberta = sum_status("Aberta")
        andamento = sum_status("Em andamento")
        finalizada = sum_status("Finalizada")
        paga = sum_status("Paga")
        con.close()

        self.lbl_aberta.config(text=f"Aberta: R$ {aberta:.2f}".replace(".", ","))
        self.lbl_andamento.config(text=f"Em andamento: R$ {andamento:.2f}".replace(".", ","))
        self.lbl_finalizada.config(text=f"Finalizada: R$ {finalizada:.2f}".replace(".", ","))
        self.lbl_paga.config(text=f"Paga: R$ {paga:.2f}".replace(".", ","))

class ClientDialog(tk.Toplevel):
    def __init__(self, parent, title, on_save, initial=None):
        super().__init__(parent)
        self.title(title)
        self.resizable(False, False)
        self.on_save = on_save

        self.vars = [tk.StringVar() for _ in range(5)]

        fields = [
            ("CPF", 0),
            ("NOME*", 1),
            ("TELEFONE", 2),
            ("PLACA", 3),
            ("VEICULO", 4) ,
        ]
        for i, (label, idx) in enumerate(fields):
            tk.Label(self, text=label).grid(row=i, column=0, sticky="w", padx=10, pady=6)
            tk.Entry(self, textvariable=self.vars[idx], width=50).grid(
                row=i, column=1, padx=10, pady=6
            )

        btns = tk.Frame(self)
        btns.grid(row=5, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Salvar", command=self.save).pack(side="left", padx=8)
        tk.Button(btns, text="Cancelar", command=self.destroy).pack(side="left")

        if initial:
            self.vars[0].set(initial[0] or "")  # CPF
            self.vars[1].set(initial[1] or "")  # NOME
            self.vars[2].set(initial[2] or "")  # TELEFONE
            self.vars[3].set(initial[3] or "")  # PLACA
            self.vars[4].set(initial[4] or "")  # VEICULO

        self.grab_set()
        self.transient(parent)

    def save(self):
        cpf = self.vars[0].get().strip()
        name = self.vars[1].get().strip()
        if not name:
            messagebox.showwarning("Atenção", "Nome é obrigatório.")
            return
        phone = self.vars[2].get().strip()
        plate = self.vars[3].get().strip()
        vehicle = self.vars[4].get().strip()
        self.on_save((cpf, name, phone, plate, vehicle))
        self.destroy()

class ServiceDialog(tk.Toplevel):
    def __init__(self, parent, title, on_save, initial=None):
        super().__init__(parent)
        self.withdraw()
        self.title(title)
        self.transient(parent)
        self.grab_set()
        self.resizable(False, False)
        self.geometry("400x180")
        self.on_save = on_save
        self.update_idletasks()

        win_width = 400
        win_height = 180

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (win_width // 2)
        y = (screen_height // 2) - (win_height // 2)

        self.geometry(f"{win_width}x{win_height}+{x}+{y}")
        self.deiconify()

        self.quantity = tk.StringVar()
        self.desc = tk.StringVar()
        self.price = tk.StringVar()

        tk.Label(self, text="Quantidade*").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        self.entry_qtd = tk.Entry(self, textvariable=self.quantity, width=15)
        self.entry_qtd.grid(row=0, column=1, sticky="w", padx=10, pady=8)
        self.after(100, lambda: self.entry_qtd.focus())

        tk.Label(self, text="Descrição*").grid(row=1, column=0, sticky="w", padx=10, pady=8)

        self.entry_desc = tk.Entry(self, textvariable=self.desc, width=45)
        self.entry_desc.grid(row=1, column=1, padx=10, pady=8)
        self.entry_desc.bind("<KeyRelease>", self._maiusculo_descricao)

        tk.Label(self, text="Preço (R$)*").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(self, textvariable=self.price, width=15).grid(
            row=2, column=1, sticky="w", padx=10, pady=8
        )

        btns = tk.Frame(self)
        btns.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Salvar", command=self.save).pack(side="left", padx=8)
        tk.Button(btns, text="Cancelar", command=self.destroy).pack(side="left")

        if initial:
            self.quantity.set(f"{float(initial[0]):g}")
            self.desc.set(initial[1] or "")
            self.price.set(f"{float(initial[2]):.2f}".replace(".", ","))

        self.grab_set()
        self.transient(parent)

    def _maiusculo_descricao(self, event=None):
        texto = self.desc.get()
        pos = self.entry_desc.index("insert")

        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            self.desc.set(texto_maiusculo)
            self.entry_desc.icursor(pos)     

    def save(self):
        qtxt = self.quantity.get().strip().replace(",", ".")
        desc = self.desc.get().strip()
        ptxt = self.price.get().strip().replace(".", "").replace(",", ".")

        if not desc:
            messagebox.showwarning("Atenção", "Descrição é obrigatória.")
            return

        try:
            quantity = float(qtxt)
        except ValueError:
            messagebox.showwarning("Atenção", "Quantidade inválida.")
            return

        try:
            price = float(ptxt)
        except ValueError:
            messagebox.showwarning("Atenção", "Preço inválido.")
            return

        # salva no sistema apenas uma vez
        self.on_save((quantity, desc, price))

        # mantém a janela aberta
        self.quantity.set("1")
        self.desc.set("")
        self.price.set("")

        # foco no campo descrição para o próximo cadastro
        self.focus_set()

class OrderEditor(tk.Toplevel):
    def __init__(self, parent, order_id=None, on_close=None):
        super().__init__(parent)
        self.order_id = order_id
        self.on_close = on_close
        self.title("OS / Orçamento")
        self.geometry("900x560")

        self.client_var = tk.StringVar()
        self.date_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.status_var = tk.StringVar(value="Aberta")
        self.notes = tk.Text(self, height=3)

        self._load_clients()

        form = tk.LabelFrame(self, text="Dados", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Cliente").grid(row=0, column=0, sticky="w")
        self.client_cb = ttk.Combobox(
            form,
            textvariable=self.client_var,
            values=self.client_names,
            width=45,
            state="readonly",
        )
        self.client_cb.grid(row=0, column=1, sticky="w", padx=8)

        tk.Label(form, text="Data").grid(row=0, column=2, sticky="w", padx=(20, 0))
        tk.Entry(form, textvariable=self.date_var, width=12).grid(
            row=0, column=3, sticky="w", padx=8
        )

        tk.Label(form, text="Status").grid(row=0, column=4, sticky="w", padx=(20, 0))
        ttk.Combobox(
            form,
            textvariable=self.status_var,
            values=["Aberta", "Em andamento", "Finalizada", "Paga"],
            width=14,
            state="readonly",
        ).grid(row=0, column=5, sticky="w", padx=8)

        tk.Label(form, text="Obs").grid(row=1, column=0, sticky="nw", pady=(8, 0))
        self.notes.grid(row=1, column=1, columnspan=5, sticky="we", padx=8, pady=(8, 0))

        items_box = tk.LabelFrame(self, text="Itens (serviços)", padx=10, pady=10)
        items_box.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        cols = ("qty", "desc", "value")
        self.tree = ttk.Treeview(items_box, columns=cols, show="headings", height=10)
        for c, t, w, anchor in [
            ("qty", "QUANTIDADE", 110, "center"),
            ("desc", "DESCRIÇÃO", 420, "w"),
            ("value", "VALOR", 130, "e"),
        ]:
            self.tree.heading(c, text=t)
            self.tree.column(c, width=w, anchor=anchor)
        self.tree.pack(fill="both", expand=True)

        controls = tk.Frame(items_box)
        controls.pack(fill="x", pady=(10, 0))
        tk.Button(controls, text="Adicionar item", command=self.add_item).pack(side="left")
        tk.Button(controls, text="Remover item", command=self.remove_item).pack(
            side="left", padx=8
        )

        self.total_lbl = tk.Label(
            controls,
            text="Total: R$ 0,00",
            font=("Segoe UI", 12, "bold"),
        )
        self.total_lbl.pack(side="right")

        footer = tk.Frame(self)
        footer.pack(fill="x", padx=10, pady=(0, 10))
        tk.Button(footer, text="Salvar", command=self.save).pack(side="right", padx=8)
        tk.Button(footer, text="Fechar", command=self.close).pack(side="right")

        if self.order_id:
            self._load_order()

        self._recalc_total()
        self.protocol("WM_DELETE_WINDOW", self.close)
        self.grab_set()
        self.transient(parent)

    def _load_clients(self):
        con = db()
        cur = con.cursor()
        cur.execute("SELECT id, name FROM clients ORDER BY name")
        self.clients = cur.fetchall()
        con.close()
        self.client_names = [name for _, name in self.clients]
        if self.client_names and not self.client_var.get():
            self.client_var.set(self.client_names[0])

    def _client_id_from_name(self, name):
        for client_id, client_name in self.clients:
            if client_name == name:
                return client_id
        return None

    def _load_order(self):
        con = db()
        cur = con.cursor()
        cur.execute("SELECT client_id, date, status, notes FROM orders WHERE id=?", (self.order_id,))
        row = cur.fetchone()
        if not row:
            con.close()
            return

        client_id, date, status, notes = row

        cname = None
        for cid, nm in self.clients:
            if cid == client_id:
                cname = nm
                break

        if cname:
            self.client_var.set(cname)
        self.date_var.set(date)
        self.status_var.set(status)
        self.notes.delete("1.0", "end")
        self.notes.insert("1.0", notes or "")

        cur.execute(
            """
            SELECT description, quantity, unit_price
            FROM order_items WHERE order_id=?
            ORDER BY id
            """,
            (self.order_id,),
        )
        for desc, qty, unit in cur.fetchall():
            self.tree.insert(
                "",
                "end",
                values=(f"{qty:g}", desc, f"{unit:.2f}".replace(".", ",")),
            )
        con.close()

    def add_item(self):
        ItemDialog(self, on_add=self._add_item_row)

    def _add_item_row(self, desc, qty, unit):
        self.tree.insert(
            "",
            "end",
            values=(f"{qty:g}", desc, f"{unit:.2f}".replace(".", ",")),
        )
        self._recalc_total()

    def remove_item(self):
        sel = self.tree.selection()
        if not sel:
            return
        for item in sel:
            self.tree.delete(item)
        self._recalc_total()

    def _recalc_total(self):
        total = 0.0
        for item in self.tree.get_children():
            vals = self.tree.item(item, "values")
            try:
                qty = float(str(vals[0]).replace(",", "."))
                unit = float(str(vals[2]).replace(".", "").replace(",", "."))
                total += qty * unit
            except (ValueError, IndexError):
                pass
        self.total_lbl.config(text=f"Total: R$ {total:.2f}".replace(".", ","))

    def save(self):
        if not self.client_names:
            messagebox.showwarning("Atenção", "Cadastre um cliente primeiro.")
            return

        cid = self._client_id_from_name(self.client_var.get())
        date = self.date_var.get().strip()
        status = self.status_var.get().strip()
        notes = self.notes.get("1.0", "end").strip()

        rows = []
        total = 0.0
        for item in self.tree.get_children():
            qty_txt, desc, unit_txt = self.tree.item(item, "values")
            qty = float(str(qty_txt).replace(",", "."))
            unit = float(str(unit_txt).replace(".", "").replace(",", "."))
            line_total = qty * unit
            total += line_total
            rows.append((desc, qty, unit, line_total))

        con = db()
        cur = con.cursor()
        now = datetime.now().isoformat(timespec="seconds")
        if self.order_id is None:
            cur.execute(
                """
                INSERT INTO orders(client_id, date, status, notes, total, created_at)
                VALUES(?,?,?,?,?,?)
                """,
                (cid, date, status, notes, total, now),
            )
            self.order_id = cur.lastrowid
        else:
            cur.execute(
                """
                UPDATE orders SET client_id=?, date=?, status=?, notes=?, total=? WHERE id=?
                """,
                (cid, date, status, notes, total, self.order_id),
            )
            cur.execute("DELETE FROM order_items WHERE order_id=?", (self.order_id,))

        cur.executemany(
            """
            INSERT INTO order_items(order_id, description, quantity, unit_price, line_total)
            VALUES(?,?,?,?,?)
            """,
            [(self.order_id, d, q, u, t) for (d, q, u, t) in rows],
        )

        con.commit()
        con.close()
        messagebox.showinfo("OK", "OS salva com sucesso!")
        if self.on_close:
            self.on_close()
        self.destroy()

    def close(self):
        if self.on_close:
            self.on_close()
        self.destroy()

class ItemDialog(tk.Toplevel):
    def __init__(self, parent, on_add):
        super().__init__(parent)
        self.title("Adicionar item")
        self.resizable(False, False)
        self.on_add = on_add

        self.desc = tk.StringVar()
        self.qty = tk.StringVar(value="1")
        self.unit = tk.StringVar(value="0,00")

        tk.Label(self, text="Descrição*").grid(row=0, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(self, textvariable=self.desc, width=45).grid(row=0, column=1, padx=10, pady=8)

        tk.Label(self, text="Qtd").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(self, textvariable=self.qty, width=10).grid(row=1, column=1, sticky="w", padx=10, pady=8)

        tk.Label(self, text="Unit (R$)").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        tk.Entry(self, textvariable=self.unit, width=12).grid(row=2, column=1, sticky="w", padx=10, pady=8)

        btns = tk.Frame(self)
        btns.grid(row=3, column=0, columnspan=2, pady=10)
        tk.Button(btns, text="Adicionar", command=self.add).pack(side="left", padx=8)
        tk.Button(btns, text="Cancelar", command=self.destroy).pack(side="left")

        self.grab_set()
        self.transient(parent)

    def add(self):
        desc = self.desc.get().strip()
        if not desc:
            messagebox.showwarning("Atenção", "Descrição é obrigatória.")
            return
        try:
            qty = float(self.qty.get().strip().replace(",", "."))
        except ValueError:
            messagebox.showwarning("Atenção", "Qtd inválida.")
            return
        try:
            unit = float(self.unit.get().strip().replace(".", "").replace(",", "."))
        except ValueError:
            messagebox.showwarning("Atenção", "Preço unitário inválido.")
            return
        self.on_add(desc, qty, unit)
        self.destroy()


def limpar_veiculos_orfaos():
    """Remove veículos que ficaram no banco sem cliente vinculado.

    Isso corrige placas antigas que continuam bloqueando novos cadastros
    mesmo depois do cliente ter sido excluído.
    """
    try:
        con = db()
        cur = con.cursor()
        cur.execute(
            """
            DELETE FROM vehicles
            WHERE client_id IS NULL
               OR client_id NOT IN (
                    SELECT id FROM clients
               )
            """
        )
        con.commit()
        con.close()
    except Exception as e:
        print("Erro ao limpar veículos órfãos:", e)

def main():
    init_db()
    limpar_veiculos_orfaos()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
