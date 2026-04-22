
"""
Sistema: Juliano Automecânica
Versão: 1.0
Desenvolvido por: Wagnerdev
Ano: 2026
Descrição: Sistema de gestão de oficina mecânica desenvolvido em Python com Tkinter e SQLite.
"""

import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import webbrowser
import urllib.parse
from datetime import datetime
import os
import tempfile

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
        for F in (DashboardFrame, ClientsFrame, ServicesFrame, OrdersFrame, FinanceFrame):
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
        self._nav_btn("🔧  Ordem de Serviço", "ServicesFrame")
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
        if hasattr(frame, "refresh"):
            frame.refresh()

class DashboardFrame(tk.Frame):
    def __init__(self, parent, app):
        super().__init__(parent, bg="#f5f6f8")
        self.app = app

        tk.Label(
            self,
            text="Orçamento",
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
        self.selected_client_id = None
        self._resultados_busca = []

        top = tk.Frame(self, bg="#f5f6f8")
        top.pack(fill="x")
        tk.Label(
            top,
            text="Clientes",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")

        search = tk.Frame(self, bg="#f5f6f8")
        search.pack(fill="x", pady=(10, 6))
        tk.Label(search, text="Buscar:", bg="#f5f6f8").pack(side="left")

        self.q_var = tk.StringVar()
        self.q_var.trace_add("write", lambda *args: self.buscar_clientes())

        self.q = tk.Entry(search, width=40, textvariable=self.q_var)
        self.q.pack(side="left", padx=8)
        
        tk.Button(search, text="Limpar", command=self._clear).pack(side="left", padx=6)

        self.sugestoes = tk.Listbox(self, height=5, font=("Segoe UI", 10))
        self.sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao)
        self.sugestoes.pack(fill="x", padx=15, pady=(0, 6))
        self.sugestoes.pack_forget()

        # FICHA DO CLIENTE
        container = tk.Frame(self, bg="#edeef0")
        container.pack(fill="x", padx=15, pady=(12, 0))
        ficha = tk.Frame(container, bg="#edeef0")
        ficha.pack(fill="x", padx=1, pady=1)

        ficha_interna = tk.Frame(ficha, bg="#eef1f5")
        ficha_interna.pack(fill="x", padx=12, pady=12)

        # Variáveis dos campos
        self.cpf_var = tk.StringVar()
        self.cpf_var.trace_add("write", self._limitar_cpf)
        self.nome_var = tk.StringVar()
        self.cidade_var = tk.StringVar()
        self.endereco_var = tk.StringVar()
        self.placa_var = tk.StringVar()
        self.veiculo_var = tk.StringVar()

        self.telefone_var = tk.StringVar()
        self.cidade2_var = tk.StringVar()
        self.bairro_var = tk.StringVar()
        self.placa2_var = tk.StringVar()
        self.km_var = tk.StringVar()
        self.telefone_var.trace_add("write", self._limitar_telefone)

        # Coluna esquerda
        col_esq = tk.Frame(ficha_interna, bg="#f5f6f8")
        col_esq.pack(side="left", fill="both", expand=True, padx=(0, 20))

        tk.Label(col_esq, text="CPF:", bg="#f5f6f8", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.cpf_var, width=32).grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(col_esq, text="Nome:", bg="#f5f6f8", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.nome_var, width=32).grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(col_esq, text="Cidade:", bg="#f5f6f8", anchor="w").grid(row=2, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.cidade_var, width=32).grid(row=2, column=1, sticky="w", pady=6)

        tk.Label(col_esq, text="Endereço:", bg="#f5f6f8", anchor="w").grid(row=3, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.endereco_var, width=32).grid(row=3, column=1, sticky="w", pady=6)

        tk.Label(col_esq, text="Placa:", bg="#f5f6f8", anchor="w").grid(row=4, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.placa_var, width=32).grid(row=4, column=1, sticky="w", pady=6)

        tk.Label(col_esq, text="Veículo:", bg="#f5f6f8", anchor="w").grid(row=5, column=0, sticky="w", pady=6)
        tk.Entry(col_esq, textvariable=self.veiculo_var, width=32).grid(row=5, column=1, sticky="w", pady=6)

        # Coluna direita
        col_dir = tk.Frame(ficha_interna, bg="#f5f6f8")
        col_dir.pack(side="left", fill="both", expand=True)

        tk.Label(col_dir, text="Telefone:", bg="#f5f6f8", anchor="w").grid(row=0, column=0, sticky="w", pady=6)
        tk.Entry(col_dir, textvariable=self.telefone_var, width=32).grid(row=0, column=1, sticky="w", pady=6)

        tk.Label(col_dir, text="COR:", bg="#f5f6f8", anchor="w").grid(row=1, column=0, sticky="w", pady=6)
        tk.Entry(col_dir, textvariable=self.cidade2_var, width=32).grid(row=1, column=1, sticky="w", pady=6)

        tk.Label(col_dir, text="Bairro:", bg="#f5f6f8", anchor="w").grid(row=2, column=0, sticky="w", pady=6)
        tk.Entry(col_dir, textvariable=self.bairro_var, width=32).grid(row=2, column=1, sticky="w", pady=6)

        tk.Label(col_dir, text="ANO:", bg="#f5f6f8", anchor="w").grid(row=3, column=0, sticky="w", pady=6)
        tk.Entry(col_dir, textvariable=self.placa2_var, width=32).grid(row=3, column=1, sticky="w", pady=6)

        tk.Label(col_dir, text="Quilometragem:", bg="#f5f6f8", anchor="w").grid(row=4, column=0, sticky="w", pady=6)
        tk.Entry(col_dir, textvariable=self.km_var, width=32).grid(row=4, column=1, sticky="w", pady=6)

        tk.Label(col_dir, text="ORÇADO POR:", bg="#f5f6f8", anchor="w").grid(row=5, column=0, sticky="w", pady=6)
        tk.Label(
            col_dir,
            text="Juliano",
            bg="#f5f6f8",
            anchor="w",
            font=("Segoe UI", 10, "bold"),
            fg="#2c3e50",
        ).grid(row=5, column=1, sticky="w", pady=6)

        actions = tk.Frame(self, bg="#f5f6f8")
        actions.pack(fill="x", pady=(10, 0))
        btn_container = tk.Frame(actions, bg="#f5f6f8")
        btn_container.pack()
        tk.Button(btn_container, text="Adicionar", command=self.add_client).pack(side="left", padx=10)
        tk.Button(btn_container, text="Editar", command=self.open_edit_dialog).pack(side="left", padx=10)
        tk.Button(btn_container, text="Excluir", command=self.delete_selected).pack(side="left", padx=10)

    def open_edit_dialog(self):
        cid = self._selected_id()
        if not cid:
              messagebox.showwarning("Atenção", "Selecione um cliente na busca primeiro.")
              return

        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT cpf, name, city, address, plate, vehicle, phone,
                   color, district, year, mileage
            FROM clients
            WHERE id=?
            """,
            (cid,),
        )
        row = cur.fetchone()
        con.close()

        if not row:
            messagebox.showwarning("Atenção", "Cliente não encontrado.")
            return

        EditClientDialog(self, cid, row)

    def _selected_id(self):
        return self.selected_client_id

    def _limpar_campos(self):
        for var in (
            self.cpf_var,
            self.nome_var,
            self.cidade_var,
            self.endereco_var,
            self.placa_var,
            self.veiculo_var,
            self.telefone_var,
            self.cidade2_var,
            self.bairro_var,
            self.placa2_var,
            self.km_var,
        ):
            var.set("")

    def _coletar_dados(self):
          return {
        "cpf": self.cpf_var.get().strip(),
        "name": self.nome_var.get().strip(),
        "city": self.cidade_var.get().strip(),
        "address": self.endereco_var.get().strip(),
        "plate": self.placa_var.get().strip().upper(),
        "vehicle": self.veiculo_var.get().strip(),
        "phone": self.telefone_var.get().strip(),
        "color": self.cidade2_var.get().strip(),
        "district": self.bairro_var.get().strip(),
        "year": self.placa2_var.get().strip(),
        "mileage": self.km_var.get().strip(),
    }

    def _preencher_campos(self, row):
         cpf, name, city, address, plate, vehicle, phone, color, district, year, mileage = row

         self.cpf_var.set(cpf or "")
         self.nome_var.set(name or "")
         self.cidade_var.set(city or "")
         self.endereco_var.set(address or "")
         self.placa_var.set(plate or "")
         self.veiculo_var.set(vehicle or "")
         self.telefone_var.set(phone or "")
         self.cidade2_var.set(color or "")
         self.bairro_var.set(district or "")
         self.placa2_var.set(year or "")
         self.km_var.set(mileage or "")

    def _carregar_cliente_por_id(self, client_id):
        con = db()
        cur = con.cursor()
        cur.execute(
            """
             SELECT cpf, name, city, address, plate, vehicle, phone,
               color, district, year, mileage
              FROM clients
              WHERE id=?
           """,
            (client_id,),
        )
        row = cur.fetchone()
        con.close()

        if not row:
            self.selected_client_id = None
            self._limpar_campos()
            return False

        self.selected_client_id = client_id
        self._preencher_campos(row)
        return True

    def _limitar_cpf(self, *args):
        texto = self.cpf_var.get()
        texto = "".join(ch for ch in texto if ch.isdigit())[:11]
        if self.cpf_var.get() != texto:
            self.cpf_var.set(texto)

    def _limitar_telefone(self, *args):
       texto = self.telefone_var.get()
       texto = "".join(ch for ch in texto if ch.isdigit())[:11]
       if self.telefone_var.get() != texto:
          self.telefone_var.set(texto)        

    def buscar_clientes(self):
        termo_original = self.q_var.get().strip()
        termo_maiusculo = termo_original.upper()
        termo_cpf = "".join(ch for ch in termo_original if ch.isdigit())

        self.sugestoes.delete(0, tk.END)
        self._resultados_busca = []

        if not termo_original:
            self.sugestoes.pack_forget()
            return

        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, cpf, plate, name, vehicle
            FROM clients
            WHERE
                REPLACE(REPLACE(REPLACE(COALESCE(cpf, ''), '.', ''), '-', ''), '/', '') LIKE ?
                OR UPPER(COALESCE(name, '')) LIKE ?
                OR UPPER(COALESCE(plate, '')) LIKE ?
            ORDER BY name
            LIMIT 10
            """,
            (
                f"{termo_cpf}%" if termo_cpf else "",
                f"{termo_maiusculo}%",
                f"{termo_maiusculo}%",
            ),
        )
        resultados = cur.fetchall()
        con.close()

        if not resultados:
            self.sugestoes.pack_forget()
            return

        self._resultados_busca = resultados
        for client_id, cpf, plate, name, vehicle in resultados:
            texto = (
                f"CPF: {cpf or '-'} | PLACA: {plate or '-'} | "
                f"NOME: {name or '-'} | VEÍCULO: {vehicle or '-'}"
            )
            self.sugestoes.insert(tk.END, texto)

        self.sugestoes.pack(fill="x", padx=15, pady=(0, 6))

    def selecionar_sugestao(self, event=None):
        selecao = self.sugestoes.curselection()
        if not selecao:
            return

        indice = selecao[0]
        if indice >= len(self._resultados_busca):
            return

        client_id, _cpf, _plate, _name, _vehicle = self._resultados_busca[indice]
        self._carregar_cliente_por_id(client_id)

        self.q_var.set("")
        self.sugestoes.pack_forget()

    def _clear(self):
        self.q_var.set("")
        self.selected_client_id = None
        self._resultados_busca = []
        self.sugestoes.delete(0, tk.END)
        self.sugestoes.pack_forget()
        self._limpar_campos()

    def _normalizar_cpf(self, valor):
        return "".join(ch for ch in str(valor or "") if ch.isdigit())

    def _normalizar_placa(self, valor):
        return "".join(ch for ch in str(valor or "").upper() if ch.isalnum())

    def add_client(self):
        dados = self._coletar_dados()

        if not dados["cpf"] or not dados["name"]:
            messagebox.showwarning("Atenção", "CPF e Nome são obrigatórios!")
            return

        cpf_normalizado = self._normalizar_cpf(dados["cpf"])
        placa_normalizada = self._normalizar_placa(dados["plate"])

        con = db()
        cur = con.cursor()

        if cpf_normalizado:
            cur.execute("SELECT cpf FROM clients")
            for (cpf_existente,) in cur.fetchall():
                if self._normalizar_cpf(cpf_existente) == cpf_normalizado:
                    con.close()
                    messagebox.showwarning("Atenção", "Este CPF já está cadastrado.")
                    return

        if placa_normalizada:
            cur.execute("SELECT plate FROM clients")
            for (placa_existente,) in cur.fetchall():
                if self._normalizar_placa(placa_existente) == placa_normalizada:
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
                cpf_normalizado or dados["cpf"].strip(),
                dados["name"],
                dados["city"],
                dados["address"],
                placa_normalizada or dados["plate"].strip().upper(),
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

        self._carregar_cliente_por_id(new_id)
        self.q_var.set("")
        self.sugestoes.delete(0, tk.END)
        self.sugestoes.pack_forget()
        messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso.")

    def delete_selected(self):
        cid = self._selected_id()
        if not cid:
            messagebox.showwarning("Atenção", "Selecione um cliente na busca primeiro.")
            return
        if not messagebox.askyesno("Confirmar", "Excluir este cliente?"):
            return

        con = db()
        cur = con.cursor()
        cur.execute("DELETE FROM clients WHERE id=?", (cid,))
        con.commit()
        con.close()
        self._clear()

    def refresh(self):
        if self.selected_client_id:
            self._carregar_cliente_por_id(self.selected_client_id)
        else:
            self.sugestoes.pack_forget()
 
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
        mao_de_obra="R$ 0,00",
        total_pecas="R$ 0,00",
        total_servicos="R$ 0,00",
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
        self.mao_de_obra = mao_de_obra
        self.total_pecas = total_pecas
        self.total_servicos = total_servicos

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
            pady=8,
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
            pady=8,
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
            pady=8,
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

    def enviar_para_cliente(self):
        telefone_base = str(self.telefone or "").strip()
        telefone_limpo = "".join(ch for ch in telefone_base if ch.isdigit())

        if not telefone_limpo:
            telefone_digitado = simpledialog.askstring(
                "Telefone do Cliente",
                "Digite o telefone com WhatsApp (com DDD):",
                parent=self
            )

            if not telefone_digitado:
                return

            telefone_limpo = "".join(ch for ch in telefone_digitado if ch.isdigit())

            if len(telefone_limpo) < 10:
                messagebox.showwarning(
                    "Atenção",
                    "Telefone inválido. Digite um número com DDD."
                )
                return

            self.telefone = telefone_limpo

        if len(telefone_limpo) == 11:
            telefone_limpo = "55" + telefone_limpo
        elif len(telefone_limpo) == 10:
            telefone_limpo = "55" + telefone_limpo

        if not self.salvar_orcamento_enviado():
            return

        mensagem = (
            f"Olá {self.nome_cliente}!\n\n"
            f"Segue seu orçamento da *Juliano Automecânica* 🔧\n\n"
            f"Qualquer dúvida estou à disposição."
        )

        link = f"https://wa.me/{telefone_limpo}?text={urllib.parse.quote(mensagem)}"

        try:
            os.startfile(link)
        except Exception:
            try:
                webbrowser.open(link)
            except Exception as e:
                messagebox.showerror("Erro", f"Não foi possível abrir o WhatsApp:\n{e}")
                return

    def imprimir_orcamento(self):
        if not os.path.exists(self.caminho_imagem):
            messagebox.showerror("Erro", "Imagem do orçamento não encontrada.")
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
        super().__init__(parent, bg="#f5f6f8")
        self.app = app
        self.selected_client_id = None
        self._resultados_busca = []

        # estado atual do orçamento
        self.orcamento_cliente_nome = ""
        self.orcamento_cliente_veiculo = ""
        self.orcamento_cliente_tipo = ""   # "novo" ou "existente"

        top = tk.Frame(self, bg="#f5f6f8")
        top.pack(fill="x")
        tk.Label(
            top,
            text="Orçamento",
            bg="#f5f6f8",
            fg="#1f2a37",
            font=("Segoe UI", 18, "bold"),
        ).pack(side="left")

        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "Services.Treeview",
            background="white",
            foreground="black",
            fieldbackground="white",
            rowheight=24,
        )
        style.configure(
            "Services.Treeview.Heading",
            background="#f3f4f6",
            foreground="#1f2937",
        )

        # ================================
        # CAMPOS DO ORÇAMENTO (CLIENTE NOVO)
        # ================================
        campos_orcamento = tk.Frame(self, bg="#f5f6f8")
        campos_orcamento.pack(anchor="w", pady=(8, 6))

        self.nome_orcamento_var = tk.StringVar()
        self.veiculo_orcamento_var = tk.StringVar()

        self.nome_orcamento_var.trace_add(
             "write", lambda *args: self._maiusculo_var(self.nome_orcamento_var)
        )

        self.veiculo_orcamento_var.trace_add(
            "write", lambda *args: self._maiusculo_var(self.veiculo_orcamento_var)
        ) 

        tk.Label(
            campos_orcamento,
            text="Cliente novo (preencha abaixo):",
            bg="#f5f6f8",
            fg="#b45309",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 6))

        tk.Label(
            campos_orcamento,
            text="Nome:",
            bg="#f5f6f8",
            fg="#374151",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=1, column=0, sticky="w", padx=(0, 8), pady=(0, 6))

        tk.Entry(
            campos_orcamento,
            textvariable=self.nome_orcamento_var,
            font=("Segoe UI", 10),
            width=35,
        ).grid(row=1, column=1, sticky="w", pady=(0, 6))

        tk.Label(
            campos_orcamento,
            text="Veículo:",
            bg="#f5f6f8",
            fg="#374151",
            font=("Segoe UI", 10, "bold"),
        ).grid(row=2, column=0, sticky="w", padx=(0, 8))

        tk.Entry(
            campos_orcamento,
            textvariable=self.veiculo_orcamento_var,
            font=("Segoe UI", 10),
            width=35,
        ).grid(row=2, column=1, sticky="w")

        tk.Button(
            campos_orcamento,
            text="Vincular Cliente Novo",
            command=self.vincular_cliente_novo
        ).grid(row=1, column=2, padx=(20, 0), pady=(0, 6))

        tk.Button(
            campos_orcamento,
            text="Limpar Cliente",
            command=self.limpar_cliente
        ).grid(row=2, column=2, sticky="w", padx=(20, 0))

        self.cliente_vinculado_var = tk.StringVar(value="Cliente vinculado: nenhum")
        tk.Label(
            self,
            textvariable=self.cliente_vinculado_var,
            bg="#f5f6f8",
            fg="#1f2937",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=10, pady=(4, 8))

        cols = ("id", "quantity", "description", "price")
        self.tree = ttk.Treeview(self, columns=cols, show="headings", style="Services.Treeview")
        self.tree.tag_configure("linha1", background="white")
        self.tree.tag_configure("linha2", background="#e6e6e6")
        self.tree.heading("id", text="ID")
        self.tree.column("id", width=0, stretch=False)
        for c, t, w, a in [
            ("quantity", "QUANTIDADE", 100, "center"),
            ("description", "DESCRIÇÃO", 420, "center"),
            ("price", "VALOR (R$)", 120, "center"),
        ]:
            self.tree.heading(c, text=t, anchor="center")
            self.tree.column(c, width=w, anchor=a)
        self.tree.pack(fill="both", expand=True, pady=10)

        # ==============================
        # LINHA 1 (BUSCA + BOTÕES)
        # ==============================
        linha1 = tk.Frame(self, bg="#f5f6f8")
        linha1.pack(fill="x", pady=(5, 0))

        tk.Label(
            linha1,
            text="Buscar (Placa / CPF / Nome):",
            bg="#f5f6f8",
            font=("Segoe UI", 10, "bold"),
        ).pack(side="left", padx=(10, 5))

        self.search_var = tk.StringVar()
        self.search_plate = tk.Entry(
            linha1,
            textvariable=self.search_var,
            font=("Segoe UI", 10),
            width=15,
        )
        self.search_plate.pack(side="left", padx=(0, 10))
        self.search_var.trace_add("write", lambda *args: self.buscar_cliente())

        tk.Button(linha1, text="Adicionar", command=self.add_dialog).pack(side="left", padx=10)
        tk.Button(linha1, text="Editar", command=self.edit_dialog).pack(side="left", padx=5)
        tk.Button(linha1, text="Excluir", command=self.delete_selected).pack(side="left", padx=10)
        tk.Button(linha1, text="CriarOrçamento", command=self.criar_orcamento_imagem).pack(side="left", padx=5)

        # ==============================
        # LINHA 2 (VALORES)
        # ==============================
        linha2 = tk.Frame(self, bg="#f5f6f8")
        linha2.pack(fill="x", pady=(5, 10))

        tk.Label(
            linha2,
            text="Mão de Obra:",
            bg="#f5f6f8",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(10, 5))

        self.mao_obra_var = tk.StringVar()
        self.mao_obra = tk.Entry(
            linha2,
            textvariable=self.mao_obra_var,
            width=10,
            justify="center"
        )
        self.mao_obra.pack(side="left", padx=(0, 15))
        self.mao_obra_var.trace_add("write", lambda *args: self.atualizar_totais())

        tk.Label(
            linha2,
            text="Total de Peças:",
            bg="#f5f6f8",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(10, 5))

        self.total_pecas_var = tk.StringVar(value="R$ 0,00")
        self.total_pecas = tk.Label(
            linha2,
            textvariable=self.total_pecas_var,
            bg="#f5f6f8",
            fg="#1f2937",
            font=("Segoe UI", 11, "bold")
        )
        self.total_pecas.pack(side="left", padx=(0, 15))

        tk.Label(
            linha2,
            text="Total de Serviços:",
            bg="#f5f6f8",
            font=("Segoe UI", 10, "bold")
        ).pack(side="left", padx=(10, 5))

        self.total_servicos = tk.Label(
            linha2,
            text="R$ 0,00",
            bg="#f5f6f8",
            fg="green",
            font=("Segoe UI", 11, "bold")
        )
        self.total_servicos.pack(side="left")

        self.sugestoes = tk.Listbox(self, height=4, font=("Segoe UI", 10))
        self.sugestoes.pack(fill="x", padx=10, pady=(5, 0))
        self.sugestoes.pack_forget()
        self.sugestoes.bind("<<ListboxSelect>>", self.selecionar_sugestao)

    def _maiusculo_var(self, var):
        texto = var.get()
        texto_maiusculo = texto.upper()
        if texto != texto_maiusculo:
            var.set(texto_maiusculo)          

    def limpar_cliente(self):
        # limpa cliente novo
        self.nome_orcamento_var.set("")
        self.veiculo_orcamento_var.set("")

        # limpa cliente existente
        self.selected_client_id = None

        # limpa busca
        self.search_var.set("")
        self.sugestoes.pack_forget()

        # limpa cliente vinculado
        self.orcamento_cliente_nome = ""
        self.orcamento_cliente_veiculo = ""
        self.orcamento_cliente_tipo = ""

        # limpa ordem de serviço
        for item in self.tree.get_children():
         self.tree.delete(item)

        # limpa mão de obra
        self.mao_obra_var.set("") 

        # atualiza label
        self.atualizar_label_cliente()
        self.atualizar_totais()     

    def atualizar_label_cliente(self):
        if self.orcamento_cliente_nome and self.orcamento_cliente_veiculo:
            tipo = "Novo" if self.orcamento_cliente_tipo == "novo" else "Existente"
            self.cliente_vinculado_var.set(
                f"Cliente vinculado: {self.orcamento_cliente_nome} | "
                f"Veículo: {self.orcamento_cliente_veiculo} | Tipo: {tipo}"
            )
        else:
            self.cliente_vinculado_var.set("Cliente vinculado: nenhum")

    def vincular_cliente_novo(self):
        nome = self.nome_orcamento_var.get().strip()
        veiculo = self.veiculo_orcamento_var.get().strip()

        if not nome:
            messagebox.showwarning("Atenção", "Preencha o nome do cliente.")
            return

        if not veiculo:
            messagebox.showwarning("Atenção", "Preencha o veículo.")
            return

        if self.selected_client_id:
            messagebox.showwarning(
                "Atenção",
                "Já existe um cliente selecionado pela busca.\n"
                "Limpe a busca antes de vincular um cliente novo."
            )
            return

        self.orcamento_cliente_nome = nome
        self.orcamento_cliente_veiculo = veiculo
        self.orcamento_cliente_tipo = "novo"
        self.atualizar_label_cliente()
        messagebox.showinfo("Sucesso", "Cliente novo vinculado ao orçamento.")

    def buscar_cliente(self):
        termo_original = self.search_var.get().strip()
        termo_maiusculo = termo_original.upper()
        termo_cpf = "".join(ch for ch in termo_original if ch.isdigit())

        self.sugestoes.delete(0, tk.END)
        self._resultados_busca = []

        if not termo_original:
            self.sugestoes.pack_forget()
            return

        con = db()
        cur = con.cursor()
        cur.execute(
            """
            SELECT id, cpf, plate, name, vehicle
            FROM clients
            WHERE
                REPLACE(REPLACE(REPLACE(COALESCE(cpf, ''), '.', ''), '-', ''), '/', '') LIKE ?
                OR UPPER(COALESCE(name, '')) LIKE ?
                OR UPPER(COALESCE(plate, '')) LIKE ?
            ORDER BY name
            LIMIT 10
            """,
            (
                f"{termo_cpf}%" if termo_cpf else "",
                f"{termo_maiusculo}%",
                f"{termo_maiusculo}%",
            ),
        )
        resultados = cur.fetchall()
        con.close()

        if not resultados:
            self.sugestoes.pack_forget()
            return

        self._resultados_busca = resultados
        for client_id, cpf, plate, name, vehicle in resultados:
            texto = (
                f"CPF: {cpf or '-'} | PLACA: {plate or '-'} | "
                f"NOME: {name or '-'} | VEÍCULO: {vehicle or '-'}"
            )
            self.sugestoes.insert(tk.END, texto)

        self.sugestoes.pack(fill="x", padx=10, pady=(5, 0))

    def selecionar_sugestao(self, event=None):
        selecao = self.sugestoes.curselection()
        if not selecao:
            return

        indice = selecao[0]
        if indice >= len(self._resultados_busca):
            return

        client_id, cpf, plate, name, vehicle = self._resultados_busca[indice]

        self.selected_client_id = client_id
        self.nome_orcamento_var.set(name or "")
        self.veiculo_orcamento_var.set(vehicle or "")

        self.orcamento_cliente_nome = name or ""
        self.orcamento_cliente_veiculo = vehicle or ""
        self.orcamento_cliente_tipo = "existente"

        self.search_var.set("")
        self.sugestoes.pack_forget()
        self.atualizar_label_cliente()

    def atualizar_totais(self):
        total_pecas = 0.0

        for item in self.tree.get_children():
            valores = self.tree.item(item, "values")
            if len(valores) >= 4:
                valor_str = str(valores[3]).strip()
                try:
                    valor_str = valor_str.replace("R$", "").replace(" ", "")
                    valor_str = valor_str.replace(".", "").replace(",", ".")
                    preco = float(valor_str)
                    total_pecas += preco
                except Exception:
                    pass

        texto = self.mao_obra_var.get().strip()
        try:
            texto = texto.replace("R$", "").replace(" ", "")
            texto = texto.replace(".", "").replace(",", ".")
            mao_obra = float(texto) if texto else 0.0
        except Exception:
            mao_obra = 0.0

        total_servicos = mao_obra + total_pecas
        self.total_pecas_var.set(f"R$ {total_pecas:.2f}".replace(".", ","))
        self.total_servicos.config(text=f"R$ {total_servicos:.2f}".replace(".", ","))

    def _selected_id(self):
        sel = self.tree.selection()
        if not sel:
            return None
        return int(self.tree.item(sel[0], "values")[0])

    def _proximo_id_tree(self):
        maior = 0
        for item in self.tree.get_children():
            try:
                atual = int(self.tree.item(item, "values")[0])
                if atual > maior:
                    maior = atual
            except Exception:
                pass
        return maior + 1

    def add_dialog(self):
        if not self.orcamento_cliente_nome or not self.orcamento_cliente_veiculo:
            messagebox.showwarning(
                "Atenção",
                "Vincule primeiro um cliente ao orçamento.\n\n"
                "Use o botão 'Vincular Cliente Novo' ou selecione um cliente pela busca."
            )
            return

        ServiceDialog(self, title="Adicionar Serviço", on_save=self._insert_manual)

    def edit_dialog(self):
        sid = self._selected_id()
        if not sid:
            messagebox.showwarning("Atenção", "Selecione um serviço.")
            return

        item_selecionado = self.tree.selection()[0]
        valores = self.tree.item(item_selecionado, "values")
        if len(valores) < 4:
            messagebox.showwarning("Atenção", "Serviço inválido.")
            return

        initial = (
            float(str(valores[1]).replace(",", ".")),
            valores[2],
            float(str(valores[3]).replace(".", "").replace(",", "."))
        )

        ServiceDialog(
            self,
            title="Editar Serviço",
            initial=initial,
            on_save=lambda data: self._update_manual(item_selecionado, sid, data),
        )

    def _insert_manual(self, data):
        quantidade = float(data[0])

        if quantidade.is_integer():
           quantidade = int(quantidade)

        descricao = data[1]
        preco = float(data[2])

        novo_id = self._proximo_id_tree()
        tag = "linha1" if (len(self.tree.get_children()) % 2 == 0) else "linha2"

        self.tree.insert(
            "",
            "end",
            values=(
                novo_id,
                quantidade,
                descricao,
                f"{preco:.2f}".replace(".", ",")
            ),
            tags=(tag,),
        )
        self.atualizar_totais()

    def _update_manual(self, item_id, sid, data):
        quantidade = float(data[0])

        if quantidade.is_integer():
           quantidade = int(quantidade)

        descricao = data[1]
        preco = float(data[2])

        tags = self.tree.item(item_id, "tags")
        self.tree.item(
            item_id,
            values=(sid, quantidade, descricao, f"{preco:.2f}".replace(".", ",")),
            tags=tags,
        )
        self.atualizar_totais()

    def delete_selected(self):
        sel = self.tree.selection()
        if not sel:
            messagebox.showwarning("Atenção", "Selecione um serviço.")
            return

        if not messagebox.askyesno(
            "Confirmação",
            "Tem certeza que deseja excluir este serviço?"
        ):
            return

        for item in sel:
            self.tree.delete(item)

        self.atualizar_totais()

    def criar_orcamento_imagem(self):
        try:
            nome_cliente = self.orcamento_cliente_nome.strip() or self.nome_orcamento_var.get().strip()
            veiculo_cliente = self.orcamento_cliente_veiculo.strip() or self.veiculo_orcamento_var.get().strip()

            if not nome_cliente:
                messagebox.showwarning("Atenção", "Informe o nome do cliente.")
                return

            if not veiculo_cliente:
                messagebox.showwarning("Atenção", "Informe o veículo do cliente.")
                return

            itens = []
            for item_id in self.tree.get_children():
                valores = self.tree.item(item_id, "values")
                if len(valores) >= 4:
                    quantidade = str(valores[1])
                    descricao = str(valores[2])
                    valor = str(valores[3])
                    itens.append((quantidade, descricao, valor))

            if not itens:
                messagebox.showwarning("Atenção", "Adicione pelo menos um serviço ao orçamento.")
                return

            nome_oficina = "Juliano Automecânica"
            data_atual = datetime.now().strftime("%d/%m/%Y")
            hora_arquivo = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

            mao_de_obra = self.mao_obra_var.get().strip() or "0,00"
            total_pecas = self.total_pecas_var.get().strip() or "R$ 0,00"
            total_servicos = self.total_servicos.cget("text").strip() or "R$ 0,00"

            largura = 1000
            altura = 1400
            margem = 50

            img = Image.new("RGB", (largura, altura), "white")
            draw = ImageDraw.Draw(img)

            try:
                fonte_titulo = ImageFont.truetype("arial.ttf", 42)
                fonte_subtitulo = ImageFont.truetype("arial.ttf", 28)
                fonte_texto = ImageFont.truetype("arial.ttf", 24)
                fonte_negrito = ImageFont.truetype("arialbd.ttf", 24)
                fonte_pequena = ImageFont.truetype("arial.ttf", 20)
            except Exception:
                fonte_titulo = ImageFont.load_default()
                fonte_subtitulo = ImageFont.load_default()
                fonte_texto = ImageFont.load_default()
                fonte_negrito = ImageFont.load_default()
                fonte_pequena = ImageFont.load_default()

            y = margem

            logo_path = LOGO_PATH
            if os.path.exists(logo_path):
                try:
                    logo = Image.open(logo_path).convert("RGBA")
                    logo.thumbnail((140, 140))
                    img.paste(logo, (margem, y), logo)
                except Exception:
                    pass

            draw.text((220, y + 20), nome_oficina, fill="black", font=fonte_titulo)
            draw.text((220, y + 80), "ORÇAMENTO", fill="black", font=fonte_subtitulo)

            y += 170
            draw.line((margem, y, largura - margem, y), fill="black", width=2)
            y += 30

            draw.text((margem, y), f"Data: {data_atual}", fill="black", font=fonte_negrito)
            y += 45
            draw.text((margem, y), f"Cliente: {nome_cliente}", fill="black", font=fonte_texto)
            y += 40
            draw.text((margem, y), f"Veículo: {veiculo_cliente}", fill="black", font=fonte_texto)
            y += 50

            draw.line((margem, y, largura - margem, y), fill="gray", width=1)
            y += 25

            x_qtd = margem
            x_desc = 180
            x_valor = 800

            draw.text((x_qtd, y), "QTD", fill="black", font=fonte_negrito)
            draw.text((x_desc, y), "DESCRIÇÃO", fill="black", font=fonte_negrito)
            draw.text((x_valor, y), "VALOR", fill="black", font=fonte_negrito)
            y += 35

            draw.line((margem, y, largura - margem, y), fill="black", width=1)
            y += 20

            for qtd, descricao, valor in itens:
                draw.text((x_qtd, y), qtd, fill="black", font=fonte_texto)
                draw.text((x_desc, y), descricao, fill="black", font=fonte_texto)
                draw.text((x_valor, y), f"R$ {valor}", fill="black", font=fonte_texto)
                y += 35

                if y > altura - 250:
                    break

            y += 20
            draw.line((margem, y, largura - margem, y), fill="gray", width=1)
            y += 30

            mao_de_obra_formatado = mao_de_obra
            if not mao_de_obra_formatado.startswith("R$"):
                mao_de_obra_formatado = f"R$ {mao_de_obra_formatado}"

            draw.text((margem, y), f"Mão de Obra: {mao_de_obra_formatado}", fill="black", font=fonte_texto)
            y += 40
            draw.text((margem, y), f"Total de Peças: {total_pecas}", fill="black", font=fonte_texto)
            y += 40
            draw.text((margem, y), f"Total de Serviços: {total_servicos}", fill="black", font=fonte_negrito)
            y += 70

            draw.line((margem, y, largura - margem, y), fill="black", width=1)
            y += 25
            draw.text((margem, y), "Obrigado pela preferência!", fill="black", font=fonte_pequena)

            pasta_saida = "orcamentos"
            os.makedirs(pasta_saida, exist_ok=True)

            nome_limpo = "".join(c for c in nome_cliente if c.isalnum() or c in (" ", "_", "-")).strip()
            nome_limpo = nome_limpo.replace(" ", "_")

            nome_arquivo = f"orcamento_{nome_limpo}_{hora_arquivo}.png"
            caminho_saida = os.path.join(pasta_saida, nome_arquivo)

            img.save(caminho_saida)

            telefone_cliente = ""

            if self.orcamento_cliente_tipo == "existente" and self.selected_client_id:
                con = db()
                cur = con.cursor()
                cur.execute("SELECT phone FROM clients WHERE id = ?", (self.selected_client_id,))
                row = cur.fetchone()
                con.close()

                if row and row[0]:
                    telefone_cliente = row[0]

            OrcamentoPreview(
                self,
                caminho_imagem=caminho_saida,
                nome_cliente=nome_cliente,
                telefone=telefone_cliente,
                veiculo=veiculo_cliente,
                mao_de_obra=mao_de_obra_formatado,
                total_pecas=total_pecas,
                total_servicos=total_servicos,
            )

        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar orçamento:\n{e}")

    def refresh(self):
        self.atualizar_label_cliente()
        self.atualizar_totais()

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

def main():
    init_db()
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()
