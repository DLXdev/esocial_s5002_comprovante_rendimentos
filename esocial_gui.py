import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import os
import sys
from pathlib import Path

class ESocialConverterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Conversor e-Social S-5002 para PDF")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Variables
        self.input_dir = tk.StringVar()
        self.output_dir = tk.StringVar()
        self.csv_file = tk.StringVar()
        self.csv_dependentes = tk.StringVar()
        self.csv_entidades = tk.StringVar()
        self.ano = tk.StringVar(value="2025")
        self.workers = tk.StringVar(value="4")
        
        # Create UI
        self.create_widgets()
        
    def create_widgets(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        header_frame.columnconfigure(1, weight=1)
        
        title_label = ttk.Label(header_frame, text="Conversor e-Social S-5002 para PDF", 
                               font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 5))
        
        subtitle_label = ttk.Label(header_frame, text="Converta arquivos XML do e-Social em comprovantes de rendimentos PDF")
        subtitle_label.grid(row=1, column=0, columnspan=2, sticky="w")
        
        # Status bar
        self.status_var = tk.StringVar(value="Pronto")
        status_frame = ttk.Frame(main_frame)
        status_frame.grid(row=3, column=0, sticky="ew", pady=(10, 0))
        status_frame.columnconfigure(0, weight=1)
        
        self.status_label = ttk.Label(status_frame, textvariable=self.status_var, 
                                     relief=tk.SUNKEN, anchor=tk.W)
        self.status_label.grid(row=0, column=0, sticky="ew")
        
        # Notebook (tabs)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.grid(row=2, column=0, sticky="nsew")
        
        # Configurations tab
        self.create_config_tab()
        
        # Conversion tab
        self.create_conversion_tab()
        
        # XML Generation tab
        self.create_xml_generation_tab()
        
        # Log tab
        self.create_log_tab()
        
    def create_xml_generation_tab(self):
        xml_frame = ttk.Frame(self.notebook, padding="10")
        xml_frame.grid(row=0, column=0, sticky="nsew")
        xml_frame.columnconfigure(0, weight=1)
        xml_frame.rowconfigure(1, weight=1)
        
        # Generation controls
        gen_control_frame = ttk.Frame(xml_frame)
        gen_control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        gen_control_frame.columnconfigure(1, weight=1)
        
        ttk.Label(gen_control_frame, text="Diretório de Saída para XMLs:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        xml_output_frame = ttk.Frame(gen_control_frame)
        xml_output_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        xml_output_frame.columnconfigure(0, weight=1)
        
        self.xml_output_dir = tk.StringVar()
        ttk.Entry(xml_output_frame, textvariable=self.xml_output_dir).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(xml_output_frame, text="Procurar...", command=self.browse_xml_output_dir, width=10).grid(row=0, column=1)
        
        # Generate button
        self.generate_xml_button = ttk.Button(gen_control_frame, text="Gerar XMLs de Teste", 
                                            command=self.start_xml_generation)
        self.generate_xml_button.grid(row=2, column=0, pady=(10, 0))
        
        # Results frame
        xml_results_frame = ttk.LabelFrame(xml_frame, text="Resultados da Geração", padding="10")
        xml_results_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        xml_results_frame.columnconfigure(0, weight=1)
        xml_results_frame.rowconfigure(0, weight=1)
        
        # Results text
        self.xml_results_text = tk.Text(xml_results_frame, wrap=tk.WORD, state=tk.DISABLED)
        xml_results_scroll = ttk.Scrollbar(xml_results_frame, orient=tk.VERTICAL, command=self.xml_results_text.yview)
        self.xml_results_text.configure(yscrollcommand=xml_results_scroll.set)
        
        self.xml_results_text.grid(row=0, column=0, sticky="nsew")
        xml_results_scroll.grid(row=0, column=1, sticky="ns")
        
        # Add tab to notebook
        self.notebook.add(xml_frame, text="04 - Gerar XMLs")
        
    def browse_xml_output_dir(self):
        directory = filedialog.askdirectory(title="Selecione o diretório de saída para XMLs")
        if directory:
            self.xml_output_dir.set(directory)
            self.update_status("Diretório de saída para XMLs selecionado")
            
    def start_xml_generation(self):
        # Validate inputs
        if not self.xml_output_dir.get():
            messagebox.showerror("Erro", "Por favor, selecione o diretório de saída para XMLs.")
            return
            
        # Run generation in a separate thread
        generation_thread = threading.Thread(target=self.generate_test_xmls)
        generation_thread.daemon = True
        generation_thread.start()
        
    def generate_test_xmls(self):
        self.root.after(0, lambda: self.generate_xml_button.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.update_status("Iniciando geração de XMLs de teste..."))
        
        try:
            # Update results text
            self.root.after(0, lambda: self.xml_results_text.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.xml_results_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.xml_results_text.insert(tk.END, "Iniciando geração de XMLs de teste...\n"))
            
            # Get output directory
            output_dir = self.xml_output_dir.get()
            if output_dir:
                self.root.after(0, lambda out_dir=output_dir: self.update_status(f"Diretório de saída: {os.path.abspath(out_dir)}"))
                self.root.after(0, lambda out_dir=output_dir: self.xml_results_text.insert(tk.END, f"Diretório de saída: {os.path.abspath(out_dir)}\n"))
            
            # Import and run the XML generator
            from gerador_xml_s5002_v6 import gerar_todos_xmls
            
            # Generate XMLs
            gerar_todos_xmls(output_dir)
            
            # Success
            self.root.after(0, lambda: self.update_status("Geração de XMLs concluída com sucesso!"))
            self.root.after(0, lambda: self.xml_results_text.insert(tk.END, "\nGeração de XMLs concluída com sucesso!\n"))
            self.root.after(0, lambda: self.xml_results_text.insert(tk.END, "Verifique a pasta de saída para os XMLs gerados.\n"))
            self.root.after(0, lambda: self.xml_results_text.see(tk.END))
            
        except Exception as e:
            # Error
            self.root.after(0, lambda: self.update_status(f"Erro na geração: {str(e)}"))
            self.root.after(0, lambda: self.xml_results_text.insert(tk.END, f"\nErro: {str(e)}\n"))
            import traceback
            self.root.after(0, lambda: self.xml_results_text.insert(tk.END, f"Detalhes: {traceback.format_exc()}\n"))
            messagebox.showerror("Erro", f"Ocorreu um erro durante a geração:\n{str(e)}")
            
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.generate_xml_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.xml_results_text.config(state=tk.DISABLED))
            
    def create_config_tab(self):
        config_frame = ttk.Frame(self.notebook, padding="10")
        config_frame.grid(row=0, column=0, sticky="nsew")
        config_frame.columnconfigure(0, weight=1)
        
        # Input/Output section
        io_frame = ttk.LabelFrame(config_frame, text="Diretórios", padding="10")
        io_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        io_frame.columnconfigure(1, weight=1)
        
        # Input directory
        ttk.Label(io_frame, text="Diretório de Entrada (XMLs):").grid(row=0, column=0, sticky="w", pady=(0, 5))
        input_frame = ttk.Frame(io_frame)
        input_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        input_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(input_frame, textvariable=self.input_dir).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(input_frame, text="Procurar...", command=self.browse_input_dir, width=10).grid(row=0, column=1)
        
        # Output directory
        ttk.Label(io_frame, text="Diretório de Saída (PDFs):").grid(row=2, column=0, sticky="w", pady=(0, 5))
        output_frame = ttk.Frame(io_frame)
        output_frame.grid(row=3, column=0, columnspan=2, sticky="ew")
        output_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(output_frame, textvariable=self.output_dir).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(output_frame, text="Procurar...", command=self.browse_output_dir, width=10).grid(row=0, column=1)
        
        # CSV Files section
        csv_frame = ttk.LabelFrame(config_frame, text="Arquivos CSV (Opcional)", padding="10")
        csv_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        csv_frame.columnconfigure(1, weight=1)
        
        # Main CSV
        ttk.Label(csv_frame, text="CSV de Funcionários:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        csv_main_frame = ttk.Frame(csv_frame)
        csv_main_frame.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        csv_main_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(csv_main_frame, textvariable=self.csv_file).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(csv_main_frame, text="Procurar...", command=self.browse_csv_file, width=10).grid(row=0, column=1)
        
        # Dependentes CSV
        ttk.Label(csv_frame, text="CSV de Dependentes:").grid(row=2, column=0, sticky="w", pady=(0, 5))
        csv_dep_frame = ttk.Frame(csv_frame)
        csv_dep_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))
        csv_dep_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(csv_dep_frame, textvariable=self.csv_dependentes).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(csv_dep_frame, text="Procurar...", command=self.browse_csv_dependentes, width=10).grid(row=0, column=1)
        
        # Entidades CSV
        ttk.Label(csv_frame, text="CSV de Entidades:").grid(row=4, column=0, sticky="w", pady=(0, 5))
        csv_ent_frame = ttk.Frame(csv_frame)
        csv_ent_frame.grid(row=5, column=0, columnspan=2, sticky="ew")
        csv_ent_frame.columnconfigure(0, weight=1)
        
        ttk.Entry(csv_ent_frame, textvariable=self.csv_entidades).grid(row=0, column=0, sticky="ew", padx=(0, 5))
        ttk.Button(csv_ent_frame, text="Procurar...", command=self.browse_csv_entidades, width=10).grid(row=0, column=1)
        
        # Options section
        options_frame = ttk.LabelFrame(config_frame, text="Opções", padding="10")
        options_frame.grid(row=2, column=0, sticky="ew")
        options_frame.columnconfigure(1, weight=1)
        
        # Year
        ttk.Label(options_frame, text="Ano-Calendário:").grid(row=0, column=0, sticky="w", pady=(0, 5))
        year_combo = ttk.Combobox(options_frame, textvariable=self.ano, 
                                 values=["2023", "2024", "2025", "2026"], 
                                 width=10, state="readonly")
        year_combo.grid(row=0, column=1, sticky="w", padx=(10, 0))
        
        # Workers
        ttk.Label(options_frame, text="Número de Workers:").grid(row=1, column=0, sticky="w", pady=(5, 0))
        workers_combo = ttk.Combobox(options_frame, textvariable=self.workers, 
                                    values=["1", "2", "3", "4"], 
                                    width=10, state="readonly")
        workers_combo.grid(row=1, column=1, sticky="w", padx=(10, 0), pady=(5, 0))
        
        # Add tab to notebook
        self.notebook.add(config_frame, text="01 - Configurações")
        
    def create_conversion_tab(self):
        conversion_frame = ttk.Frame(self.notebook, padding="10")
        conversion_frame.grid(row=0, column=0, sticky="nsew")
        conversion_frame.columnconfigure(0, weight=1)
        conversion_frame.rowconfigure(1, weight=1)
        
        # Control buttons
        control_frame = ttk.Frame(conversion_frame)
        control_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        control_frame.columnconfigure(2, weight=1)
        
        self.convert_button = ttk.Button(control_frame, text="Converter XMLs para PDFs", 
                                        command=self.start_conversion)
        self.convert_button.grid(row=0, column=0, padx=(0, 5))
        
        self.open_output_button = ttk.Button(control_frame, text="Abrir Pasta de Saída", 
                                            command=self.open_output_folder, 
                                            state=tk.DISABLED)
        self.open_output_button.grid(row=0, column=1, padx=(0, 5))
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(control_frame, variable=self.progress_var, 
                                           maximum=100, length=300)
        self.progress_bar.grid(row=0, column=2, sticky="ew", padx=(10, 0))
        
        # Results frame
        results_frame = ttk.LabelFrame(conversion_frame, text="Resultados", padding="10")
        results_frame.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        results_frame.columnconfigure(0, weight=1)
        results_frame.rowconfigure(0, weight=1)
        
        # Results text
        self.results_text = tk.Text(results_frame, wrap=tk.WORD, state=tk.DISABLED)
        results_scroll = ttk.Scrollbar(results_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scroll.set)
        
        self.results_text.grid(row=0, column=0, sticky="nsew")
        results_scroll.grid(row=0, column=1, sticky="ns")
        
        # Stats frame
        stats_frame = ttk.Frame(conversion_frame)
        stats_frame.grid(row=2, column=0, sticky="ew")
        stats_frame.columnconfigure(3, weight=1)
        
        self.files_processed_var = tk.StringVar(value="Arquivos Processados: 0")
        self.success_var = tk.StringVar(value="Sucesso: 0")
        self.errors_var = tk.StringVar(value="Erros: 0")
        
        ttk.Label(stats_frame, textvariable=self.files_processed_var).grid(row=0, column=0, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.success_var).grid(row=0, column=1, padx=(0, 20))
        ttk.Label(stats_frame, textvariable=self.errors_var).grid(row=0, column=2, padx=(0, 20))
        
        # Add tab to notebook
        self.notebook.add(conversion_frame, text="02 - Conversão")
        
    def create_log_tab(self):
        log_frame = ttk.Frame(self.notebook, padding="10")
        log_frame.grid(row=0, column=0, sticky="nsew")
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Log text
        self.log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_text.grid(row=0, column=0, sticky="nsew")
        
        # Clear button
        clear_button = ttk.Button(log_frame, text="Limpar Log", command=self.clear_log)
        clear_button.grid(row=1, column=0, sticky="e", pady=(5, 0))
        
        # Add tab to notebook
        self.notebook.add(log_frame, text="03 - Log")
        
    def browse_input_dir(self):
        directory = filedialog.askdirectory(title="Selecione o diretório de entrada")
        if directory:
            self.input_dir.set(directory)
            self.update_status("Diretório de entrada selecionado")
            
    def browse_output_dir(self):
        directory = filedialog.askdirectory(title="Selecione o diretório de saída")
        if directory:
            self.output_dir.set(directory)
            self.update_status("Diretório de saída selecionado")
            
    def browse_csv_file(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo CSV de funcionários",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_file.set(file_path)
            self.update_status("CSV de funcionários selecionado")
            
    def browse_csv_dependentes(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo CSV de dependentes",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_dependentes.set(file_path)
            self.update_status("CSV de dependentes selecionado")
            
    def browse_csv_entidades(self):
        file_path = filedialog.askopenfilename(
            title="Selecione o arquivo CSV de entidades",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if file_path:
            self.csv_entidades.set(file_path)
            self.update_status("CSV de entidades selecionado")
            
    def update_status(self, message):
        self.status_var.set(message)
        self.log_text.insert(tk.END, f"{message}\n")
        self.log_text.see(tk.END)
        
    def clear_log(self):
        self.log_text.delete(1.0, tk.END)
        
    def open_output_folder(self):
        output_dir = self.output_dir.get()
        if output_dir and os.path.exists(output_dir):
            # Open folder in system explorer
            import subprocess
            if sys.platform == "win32":
                subprocess.run(["explorer", output_dir])
            elif sys.platform == "darwin":
                subprocess.run(["open", output_dir])
            else:
                subprocess.run(["xdg-open", output_dir])
                
    def start_conversion(self):
        # Validate inputs
        if not self.input_dir.get():
            messagebox.showerror("Erro", "Por favor, selecione o diretório de entrada.")
            return
            
        if not self.output_dir.get():
            messagebox.showerror("Erro", "Por favor, selecione o diretório de saída.")
            return
            
        # Log output directory
        output_dir = self.output_dir.get()
        if output_dir:
            self.update_status(f"Pasta de saída selecionada: {os.path.abspath(output_dir)}")
            
        # Run conversion in a separate thread
        conversion_thread = threading.Thread(target=self.convert_xmls_to_pdfs)
        conversion_thread.daemon = True
        conversion_thread.start()
        
    def convert_xmls_to_pdfs(self):
        self.root.after(0, lambda: self.convert_button.config(state=tk.DISABLED))
        self.root.after(0, lambda: self.update_status("Iniciando conversão..."))
        self.root.after(0, lambda: self.progress_var.set(0))
        
        try:
            # Update results text
            self.root.after(0, lambda: self.results_text.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.results_text.delete(1.0, tk.END))
            self.root.after(0, lambda: self.results_text.insert(tk.END, "Iniciando conversão...\n"))
            
            # Log output directory path
            output_dir = self.output_dir.get()
            if output_dir:
                self.root.after(0, lambda out_dir=output_dir: self.update_status(f"Pasta de saída: {os.path.abspath(out_dir)}"))
                self.root.after(0, lambda out_dir=output_dir: self.results_text.insert(tk.END, f"Pasta de saída: {os.path.abspath(out_dir)}\n"))
            
            # Prepare arguments for the actual conversion
            input_dir = self.input_dir.get()
            output_dir = self.output_dir.get()
            ano = self.ano.get()
            workers = self.workers.get()
            
            # Import the actual converter
            from s5002_to_pdf import main as convert_main
            import sys
            import argparse
            
            # Save original sys.argv
            original_argv = sys.argv[:]
            
            # Prepare arguments
            sys.argv = [
                'esocial_gui.py',  # Script name (dummy)
                input_dir,
                output_dir,
                '--ano', ano,
                '--workers', workers
            ]
            
            # Add CSV files if provided
            if self.csv_file.get():
                sys.argv.extend(['--csv', self.csv_file.get()])
                
            if self.csv_dependentes.get():
                sys.argv.extend(['--csv-dependentes', self.csv_dependentes.get()])
                
            if self.csv_entidades.get():
                sys.argv.extend(['--csv-entidades', self.csv_entidades.get()])
            
            # Create a namespace object to simulate parsed arguments
            args = argparse.Namespace(
                input_dir=input_dir,
                output_dir=output_dir,
                ano=ano,
                workers=int(workers),
                csv=self.csv_file.get() if self.csv_file.get() else None,
                csv_dependentes=self.csv_dependentes.get() if self.csv_dependentes.get() else None,
                csv_entidades=self.csv_entidades.get() if self.csv_entidades.get() else None
            )
            
            # Run actual conversion by directly calling the main function logic
            # We need to replicate the main function logic here since we can't easily mock argparse
            from pathlib import Path
            from s5002_to_pdf import DadosComplementares, agrupar_xmls_por_cpf, processar_xmls_agrupados
            from concurrent.futures import ProcessPoolExecutor
            
            # Validar diretórios
            if not os.path.isdir(args.input_dir):
                raise FileNotFoundError(f"Diretório de entrada não existe: {args.input_dir}")
            
            os.makedirs(args.output_dir, exist_ok=True)
            
            # Carregar dados complementares
            dados_compl = DadosComplementares(args.csv, args.csv_dependentes, args.csv_entidades)
            
            # Listar arquivos XML
            xml_files = list(Path(args.input_dir).glob('*.xml'))
            
            if not xml_files:
                self.root.after(0, lambda: self.update_status(f"Nenhum arquivo XML encontrado em {args.input_dir}"))
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"\nNenhum arquivo XML encontrado em {args.input_dir}\n"))
            else:
                self.root.after(0, lambda: self.update_status(f"Encontrados {len(xml_files)} arquivo(s) XML para processar"))
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"\nEncontrados {len(xml_files)} arquivo(s) XML para processar\n"))
                
                # Agrupar XMLs por CPF
                self.root.after(0, lambda: self.update_status("Agrupando XMLs por CPF..."))
                self.root.after(0, lambda: self.results_text.insert(tk.END, "Agrupando XMLs por CPF...\n"))
                
                grupos_cpf = agrupar_xmls_por_cpf(xml_files)
                self.root.after(0, lambda: self.update_status(f"Encontrados {len(grupos_cpf)} CPF(s) únicos"))
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"Encontrados {len(grupos_cpf)} CPF(s) únicos\n"))
                
                # Processar arquivos em paralelo (por CPF)
                total_sucesso = 0
                total_erros = 0
                
                with ProcessPoolExecutor(max_workers=args.workers) as executor:
                    futures = []
                    for cpf, xmls_do_cpf in grupos_cpf.items():
                        if len(xmls_do_cpf) > 1:
                            self.root.after(0, lambda: self.results_text.insert(tk.END, f"CPF {cpf}: {len(xmls_do_cpf)} XMLs serão consolidados\n"))
                        future = executor.submit(
                            processar_xmls_agrupados,
                            (xmls_do_cpf, args.output_dir, args.ano, args.csv, dados_compl)
                        )
                        futures.append(future)
                    
                    # Aguardar conclusão
                    for future in futures:
                        sucesso, erros = future.result()
                        total_sucesso += sucesso
                        total_erros += erros
                
                # Update results
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"\nProcessamento concluído:\n"))
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"  Sucessos: {total_sucesso}\n"))
                self.root.after(0, lambda: self.results_text.insert(tk.END, f"  Erros: {total_erros}\n"))
            
            # Restore original sys.argv
            sys.argv = original_argv
            
            # Success
            self.root.after(0, lambda: self.update_status("Conversão concluída com sucesso!"))
            self.root.after(0, lambda: self.results_text.insert(tk.END, "\nConversão concluída com sucesso!\n"))
            self.root.after(0, lambda: self.results_text.insert(tk.END, "Verifique a pasta de saída para os PDFs gerados.\n"))
            self.root.after(0, lambda: self.results_text.see(tk.END))
            self.root.after(0, lambda: self.open_output_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.files_processed_var.set("Arquivos Processados: Verifique pasta"))
            self.root.after(0, lambda: self.success_var.set("Sucesso: Verifique pasta"))
            self.root.after(0, lambda: self.errors_var.set("Erros: Verifique pasta"))
            
        except Exception as e:
            # Error
            self.root.after(0, lambda: self.update_status(f"Erro na conversão: {str(e)}"))
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"\nErro: {str(e)}\n"))
            import traceback
            self.root.after(0, lambda: self.results_text.insert(tk.END, f"Detalhes: {traceback.format_exc()}\n"))
            messagebox.showerror("Erro", f"Ocorreu um erro durante a conversão:\n{str(e)}")
            
        finally:
            # Re-enable buttons
            self.root.after(0, lambda: self.convert_button.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.results_text.config(state=tk.DISABLED))

def main():
    root = tk.Tk()
    app = ESocialConverterGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()