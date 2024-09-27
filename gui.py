import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import logging
from main import processar_cnpjs
from database import DatabaseConnection

class AppGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Consulta de CNPJ')
        self.root.geometry('1100x600')
        self.arquivo_cnpjs = ''
        self.create_widgets()

    def create_widgets(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=10)
        self.select_button = tk.Button(
            top_frame, text='Selecionar Arquivo', command=self.selecionar_arquivo
        )
        self.select_button.pack(side=tk.LEFT)
        self.file_label = tk.Label(top_frame, text='Nenhum arquivo selecionado')
        self.file_label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=10)
        self.start_button = tk.Button(
            top_frame, text='Iniciar Consulta', command=self.iniciar_consulta, state='disabled'
        )
        self.start_button.pack(side=tk.RIGHT)
        self.loading_label = tk.Label(self.root, text="")
        self.loading_label.pack()

        table_frame = tk.Frame(self.root)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        columns = (
            'cnpj',
            'inscricao_estadual',
            'razao_social',
            'nome_fantasia',
            'logradouro',
            'cep',
            'uf',
            'telefone',
            'email'
        )
        self.tree = ttk.Treeview(table_frame, columns=columns, show='headings')
        self.tree.heading('cnpj', text='CNPJ')
        self.tree.heading('inscricao_estadual', text='Inscrição Estadual')
        self.tree.heading('razao_social', text='Razão Social')
        self.tree.heading('nome_fantasia', text='Nome Fantasia')
        self.tree.heading('logradouro', text='Logradouro')
        self.tree.heading('cep', text='CEP')
        self.tree.heading('uf', text='UF')
        self.tree.heading('telefone', text='Telefone')
        self.tree.heading('email', text='Email')
        self.tree.column('cnpj', width=120)
        self.tree.column('inscricao_estadual', width=150)
        self.tree.column('razao_social', width=200)
        self.tree.column('nome_fantasia', width=150)
        self.tree.column('logradouro', width=200)
        self.tree.column('cep', width=80)
        self.tree.column('uf', width=50)
        self.tree.column('telefone', width=120)
        self.tree.column('email', width=200)

        vsb = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        hsb = ttk.Scrollbar(table_frame, orient=tk.HORIZONTAL, command=self.tree.xview)
        self.tree.configure(yscroll=vsb.set, xscroll=hsb.set)
        vsb.pack(side=tk.RIGHT, fill=tk.Y)
        hsb.pack(side=tk.BOTTOM, fill=tk.X)
        self.tree.pack(fill=tk.BOTH, expand=True)

        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Copiar", command=self.copiar_valor)
        self.menu.add_command(label="Excluir", command=self.excluir_linha)

        self.tree.bind("<Button-3>", self.mostrar_menu_contexto)

        self.load_data()

    def mostrar_menu_contexto(self, event):
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.menu.post(event.x_root, event.y_root)

    def copiar_valor(self):
        selected_item = self.tree.selection()[0]
        column_index = self.tree.identify_column(self.root.winfo_pointerx() - self.tree.winfo_rootx())
        column_number = int(column_index.replace('#', '')) - 1
        value = self.tree.item(selected_item)['values'][column_number]
        self.root.clipboard_clear()
        self.root.clipboard_append(value)

    def excluir_linha(self):
        selected_item = self.tree.selection()[0]
        cnpj = self.tree.item(selected_item)['values'][0]
        if messagebox.askyesno("Confirmar", f"Tem certeza que deseja excluir o CNPJ {cnpj}?"):
            try:
                db = DatabaseConnection()
                db.excluir_linha_por_cnpj(cnpj)
                self.tree.delete(selected_item)
            except Exception as e:
                logging.error(f'Erro ao excluir o CNPJ {cnpj}: {e}')
                messagebox.showerror("Erro", f"Erro ao excluir o CNPJ {cnpj}")

    def selecionar_arquivo(self):
        self.arquivo_cnpjs = filedialog.askopenfilename(
            title='Selecione o arquivo Excel',
            filetypes=[('Arquivos Excel', '*.xlsx *.xls')]
        )
        if self.arquivo_cnpjs:
            self.start_button.config(state='normal')
            self.file_label.config(text=self.arquivo_cnpjs)
            logging.info(f'Arquivo selecionado: {self.arquivo_cnpjs}')

    def iniciar_consulta(self):
        self.start_button.config(state='disabled')
        self.select_button.config(state='disabled')
        self.loading_label.config(text="Processando...")
        threading.Thread(target=self.processar).start()

    def processar(self):
        try:
            processar_cnpjs(self.arquivo_cnpjs)
            with open('cnpj_consulta.log', 'r') as log_file:
                log_content = log_file.read()
            if 'CNPJ inválido ignorado' in log_content:
                messagebox.showwarning('Aviso', 'Alguns CNPJs inválidos foram ignorados. Verifique o log para mais detalhes.')
            else:
                messagebox.showinfo('Sucesso', 'Processamento concluído com sucesso.')
            self.load_data()
        except Exception as e:
            logging.error(f'Erro durante o processamento: {e}')
            messagebox.showerror('Erro', f'Ocorreu um erro: {e}')
        finally:
            self.start_button.config(state='normal')
            self.select_button.config(state='normal')
            self.loading_label.config(text="")

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        db = DatabaseConnection()
        try:
            rows = db.load_data()
            for row in rows:
                self.tree.insert('', tk.END, values=row)
            logging.info('Dados carregados na tabela.')
        except Exception as e:
            logging.error(f'Erro ao carregar dados: {e}')
        finally:
            db.close()

    def run(self):
        self.root.mainloop()
