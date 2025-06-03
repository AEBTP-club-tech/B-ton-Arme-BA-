import tkinter as tk
from tkinter import messagebox, ttk
import customtkinter as ctk
from PIL import Image, ImageTk
from BA import beton, acier, flection_simple, proposition_de_barre, combinaison_de_barre
import os
import random
from itertools import cycle
import time
import json
from datetime import datetime

# Constantes de style
STYLE = {
    "colors": {
        "primary": "#00A8E8",
        "secondary": "#0086BA",
        "background": "#1A1A1A",
        "background_light": "#2A2A2A",
        "text": "#FFFFFF",
        "error": "#FF4444",
        "success": "#44FF44"
    },
    "fonts": {
        "title": ("Arial Black", 24, "bold"),
        "subtitle": ("Arial", 16, "bold"),
        "normal": ("Arial", 12),
        "button": ("Arial", 14, "bold")
    },
    "dimensions": {
        "window": "800x900",
        "button_height": 40,
        "entry_height": 35
    }
}

class BetonArmeGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Calcul Béton Armé")
        self.root.geometry(STYLE["dimensions"]["window"])
        
        # Configuration du thème
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        
        # Initialisation des variables
        self.init_variables()
        
        # Chargement de l'interface
        self.load_background()
        self.create_main_frame()
        self.create_menu()
        self.create_flexion_widgets()
        
        # Historique des calculs
        self.calculation_history = []
        
    def init_variables(self):
        """Initialisation des variables de l'interface"""
        self.fck_var = ctk.StringVar(value="25")
        self.fyk_var = ctk.StringVar(value="500")
        self.mu_var = ctk.StringVar()
        self.h_var = ctk.StringVar()
        self.bw_var = ctk.StringVar()
        self.d_var = ctk.StringVar()
        self.d_prime_var = ctk.StringVar()
        self.situation_var = ctk.StringVar(value="normale")
        
        # Variables pour la validation
        self.validation_rules = {
            "fck": {"var": self.fck_var, "min": 12, "max": 90, "unit": "MPa"},
            "fyk": {"var": self.fyk_var, "min": 400, "max": 600, "unit": "MPa"},
            "mu": {"var": self.mu_var, "min": 0, "max": 1000, "unit": "kN.m"},
            "h": {"var": self.h_var, "min": 0.1, "max": 2, "unit": "m"},
            "bw": {"var": self.bw_var, "min": 0.1, "max": 2, "unit": "m"},
            "d": {"var": self.d_var, "min": 0.1, "max": 2, "unit": "m"},
            "d_prime": {"var": self.d_prime_var, "min": 0.02, "max": 0.1, "unit": "m", "optional": True}
        }
        
        # Configuration des traces pour la validation en temps réel
        for field, rules in self.validation_rules.items():
            rules["var"].trace_add("write", lambda *args, field=field: self.validate_input(field))
            
    def load_background(self):
        """Chargement de l'image de fond"""
        try:
            image_path = os.path.join(os.path.dirname(__file__), "2auvZs.jpg")
            bg_image = Image.open(image_path)
            bg_image = bg_image.resize((800, 900))
            self.bg_photo = ImageTk.PhotoImage(bg_image)
            
            bg_label = tk.Label(self.root, image=self.bg_photo)
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Erreur lors du chargement de l'image: {e}")
            
    def create_main_frame(self):
        """Création du cadre principal"""
        self.main_frame = ctk.CTkFrame(
            self.root,
            fg_color=(STYLE["colors"]["background"], STYLE["colors"]["background"]),
            corner_radius=15
        )
        self.main_frame.pack(expand=True, fill="both", padx=20, pady=20)
        
        # Titre
        title_label = ctk.CTkLabel(
            self.main_frame,
            text="CALCUL BÉTON ARMÉ",
            font=ctk.CTkFont(family=STYLE["fonts"]["title"][0], 
                            size=STYLE["fonts"]["title"][1],
                            weight=STYLE["fonts"]["title"][2]),
            text_color=STYLE["colors"]["primary"]
        )
        title_label.pack(pady=20)
        
    def create_menu(self):
        """Création de la barre de menu"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menu Fichier
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Fichier", menu=file_menu)
        file_menu.add_command(label="Exporter les résultats", command=self.export_results)
        file_menu.add_command(label="Historique des calculs", command=self.show_history)
        file_menu.add_separator()
        file_menu.add_command(label="Quitter", command=self.root.quit)
        
        # Menu Aide
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Aide", menu=help_menu)
        help_menu.add_command(label="À propos", command=self.show_about)
        help_menu.add_command(label="Aide", command=self.show_help)
        
    def validate_input(self, field):
        """Validation en temps réel des entrées"""
        rules = self.validation_rules[field]
        var = rules["var"]
        try:
            value = float(var.get() or 0)
            if not rules.get("optional", False) and value == 0:
                return
                
            if value < rules["min"] or value > rules["max"]:
                var.configure(text_color=STYLE["colors"]["error"])
            else:
                var.configure(text_color=STYLE["colors"]["text"])
        except ValueError:
            if var.get() == "" and rules.get("optional", False):
                var.configure(text_color=STYLE["colors"]["text"])
            else:
                var.configure(text_color=STYLE["colors"]["error"])
            
    def create_flexion_widgets(self):
        """Création des widgets pour le calcul en flexion"""
        # Frame pour les entrées
        input_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=STYLE["colors"]["background_light"],
            corner_radius=10
        )
        input_frame.pack(padx=20, pady=10, fill="x")
        
        # Style des entrées
        entry_style = {
            "corner_radius": 8,
            "border_color": STYLE["colors"]["primary"],
            "border_width": 2,
            "fg_color": ("#333333", "#222222"),
            "text_color": STYLE["colors"]["text"],
            "height": STYLE["dimensions"]["entry_height"]
        }
        
        # Labels et champs d'entrée avec unités
        entries = [
            ("fck", self.fck_var, "MPa"),
            ("fyk", self.fyk_var, "MPa"),
            ("Mu", self.mu_var, "kN.m"),
            ("h", self.h_var, "m"),
            ("bw", self.bw_var, "m"),
            ("d", self.d_var, "m"),
            ("d'", self.d_prime_var, "m")
        ]
        
        for label_text, var, unit in entries:
            frame = ctk.CTkFrame(input_frame, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=5)
            
            # Label avec info-bulle
            label = ctk.CTkLabel(
                frame,
                text=f"{label_text} ({unit}):",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=STYLE["colors"]["primary"]
            )
            label.pack(side="left", padx=10)
            
            # Création de l'info-bulle
            self.create_tooltip(label, self.get_field_description(label_text))
            
            # Champ d'entrée
            entry = ctk.CTkEntry(
                frame,
                textvariable=var,
                width=200,
                **entry_style
            )
            entry.pack(side="right", padx=10)
        
        # Frame situation
        situation_frame = ctk.CTkFrame(input_frame, fg_color="transparent")
        situation_frame.pack(fill="x", padx=20, pady=10)
        
        ctk.CTkLabel(
            situation_frame,
            text="Situation:",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=STYLE["colors"]["primary"]
        ).pack(side="left", padx=10)
        
        # Radio buttons
        for text, value in [("Normale", "normale"), ("Accidentelle", "accidentelle")]:
            ctk.CTkRadioButton(
                situation_frame,
                text=text,
                variable=self.situation_var,
                value=value,
                border_color=STYLE["colors"]["primary"],
                fg_color=STYLE["colors"]["primary"],
                text_color=STYLE["colors"]["text"]
            ).pack(side="left", padx=20)
        
        # Boutons d'action
        button_frame = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        button_frame.pack(pady=20)
        
        # Bouton Calculer
        calc_button = ctk.CTkButton(
            button_frame,
            text="CALCULER",
            command=self.calculate_flexion,
            width=200,
            height=STYLE["dimensions"]["button_height"],
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=STYLE["colors"]["primary"],
            hover_color=STYLE["colors"]["secondary"]
        )
        calc_button.pack(side="left", padx=10)
        
        # Bouton Réinitialiser
        reset_button = ctk.CTkButton(
            button_frame,
            text="RÉINITIALISER",
            command=self.reset_fields,
            width=200,
            height=STYLE["dimensions"]["button_height"],
            corner_radius=10,
            font=ctk.CTkFont(size=14, weight="bold"),
            fg_color=STYLE["colors"]["background_light"],
            hover_color=STYLE["colors"]["secondary"]
        )
        reset_button.pack(side="left", padx=10)
        
        # Frame résultats
        self.result_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=STYLE["colors"]["background_light"],
            corner_radius=10
        )
        self.result_frame.pack(padx=20, pady=10, fill="x")
        
    def create_tooltip(self, widget, text):
        """Crée une info-bulle pour un widget"""
        def show_tooltip(event):
            tooltip = tk.Toplevel()
            tooltip.wm_overrideredirect(True)
            tooltip.wm_geometry(f"+{event.x_root+10}+{event.y_root+10}")
            
            label = tk.Label(
                tooltip,
                text=text,
                justify='left',
                background="#ffffe0",
                relief='solid',
                borderwidth=1,
                font=("Arial", "8", "normal")
            )
            label.pack()
            
            def hide_tooltip():
                tooltip.destroy()
                
            widget.tooltip = tooltip
            widget.bind('<Leave>', lambda e: hide_tooltip())
            
        widget.bind('<Enter>', show_tooltip)
        
    def get_field_description(self, field):
        """Retourne la description d'un champ"""
        descriptions = {
            "fck": "Résistance caractéristique du béton en compression",
            "fyk": "Limite d'élasticité caractéristique de l'acier",
            "Mu": "Moment de flexion ultime",
            "h": "Hauteur totale de la section",
            "bw": "Largeur de la section",
            "d": "Hauteur utile",
            "d'": "Distance de l'axe des armatures comprimées à la fibre la plus comprimée"
        }
        return descriptions.get(field, "")
        
    def reset_fields(self):
        """Réinitialise tous les champs"""
        self.fck_var.set("25")
        self.fyk_var.set("500")
        self.mu_var.set("")
        self.h_var.set("")
        self.bw_var.set("")
        self.d_var.set("")
        self.d_prime_var.set("")
        self.situation_var.set("normale")
        
        # Nettoyage des résultats
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
    def calculate_flexion(self):
        """Calcule la flexion et affiche les résultats"""
        try:
            # Validation des entrées
            if not self.validate_all_inputs():
                return
                
            # Récupération des valeurs
            fck = float(self.fck_var.get())
            fyk = float(self.fyk_var.get())
            mu = float(self.mu_var.get())
            h = float(self.h_var.get())
            bw = float(self.bw_var.get())
            d = float(self.d_var.get())
            d_prime = float(self.d_prime_var.get()) if self.d_prime_var.get() else None
            situation = self.situation_var.get()
            
            # Calcul
            result = flection_simple(fck, fyk, mu, h, bw, "XC1", d, d_prime, situation)
            
            # Sauvegarde dans l'historique
            self.save_to_history(result)
            
            # Affichage des résultats
            self.display_results(result)
            
        except ValueError as e:
            messagebox.showerror(
                "Erreur de saisie",
                "Veuillez entrer des valeurs numériques valides"
            )
        except Exception as e:
            messagebox.showerror(
                "Erreur de calcul",
                f"Une erreur est survenue lors du calcul : {str(e)}"
            )
            
    def validate_all_inputs(self):
        """Valide toutes les entrées"""
        for field, rules in self.validation_rules.items():
            try:
                value = float(rules["var"].get() or 0)
                if not rules.get("optional", False) and value == 0:
                    messagebox.showerror(
                        "Erreur de validation",
                        f"Le champ {field} est obligatoire"
                    )
                    return False
                    
                if value < rules["min"] or value > rules["max"]:
                    messagebox.showerror(
                        "Erreur de validation",
                        f"La valeur de {field} doit être comprise entre "
                        f"{rules['min']} et {rules['max']} {rules['unit']}"
                    )
                    return False
            except ValueError:
                if not (rules["var"].get() == "" and rules.get("optional", False)):
                    messagebox.showerror(
                        "Erreur de validation",
                        f"La valeur de {field} doit être un nombre"
                    )
                    return False
        return True
        
    def display_results(self, result):
        """Affiche les résultats du calcul"""
        # Nettoyage des anciens résultats
        for widget in self.result_frame.winfo_children():
            widget.destroy()
            
        # Titre des résultats
        ctk.CTkLabel(
            self.result_frame,
            text="RÉSULTATS",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=STYLE["colors"]["primary"]
        ).pack(pady=10)
        
        # Affichage des résultats
        for key, value in result.items():
            result_line = ctk.CTkFrame(self.result_frame, fg_color="transparent")
            result_line.pack(fill="x", padx=20, pady=2)
            
            ctk.CTkLabel(
                result_line,
                text=f"{key}:",
                font=ctk.CTkFont(size=12, weight="bold"),
                text_color=STYLE["colors"]["primary"]
            ).pack(side="left", padx=10)
            
            ctk.CTkLabel(
                result_line,
                text=f"{value:.2f} cm²",
                font=ctk.CTkFont(size=12),
                text_color=STYLE["colors"]["text"]
            ).pack(side="right", padx=10)
            
    def save_to_history(self, result):
        """Sauvegarde le calcul dans l'historique"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.calculation_history.append({
            "timestamp": timestamp,
            "inputs": {
                "fck": self.fck_var.get(),
                "fyk": self.fyk_var.get(),
                "mu": self.mu_var.get(),
                "h": self.h_var.get(),
                "bw": self.bw_var.get(),
                "d": self.d_var.get(),
                "d_prime": self.d_prime_var.get(),
                "situation": self.situation_var.get()
            },
            "results": result
        })
        
    def show_history(self):
        """Affiche l'historique des calculs"""
        if not self.calculation_history:
            messagebox.showinfo("Historique", "Aucun calcul dans l'historique")
            return
            
        history_window = tk.Toplevel(self.root)
        history_window.title("Historique des calculs")
        history_window.geometry("600x400")
        
        # Création d'un Treeview pour afficher l'historique
        tree = ttk.Treeview(history_window, columns=("Date", "fck", "fyk", "mu", "h", "bw", "d"))
        tree.heading("#0", text="")
        tree.heading("Date", text="Date")
        tree.heading("fck", text="fck (MPa)")
        tree.heading("fyk", text="fyk (MPa)")
        tree.heading("mu", text="Mu (kN.m)")
        tree.heading("h", text="h (m)")
        tree.heading("bw", text="bw (m)")
        tree.heading("d", text="d (m)")
        
        for calc in self.calculation_history:
            tree.insert("", "end", values=(
                calc["timestamp"],
                calc["inputs"]["fck"],
                calc["inputs"]["fyk"],
                calc["inputs"]["mu"],
                calc["inputs"]["h"],
                calc["inputs"]["bw"],
                calc["inputs"]["d"]
            ))
            
        tree.pack(expand=True, fill="both", padx=10, pady=10)
        
    def export_results(self):
        """Exporte les résultats au format JSON"""
        if not self.calculation_history:
            messagebox.showinfo("Export", "Aucun résultat à exporter")
            return
            
        try:
            filename = f"calculs_beton_arme_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            with open(filename, "w") as f:
                json.dump(self.calculation_history, f, indent=4)
            messagebox.showinfo("Export", f"Les résultats ont été exportés dans {filename}")
        except Exception as e:
            messagebox.showerror("Erreur d'export", str(e))
            
    def show_about(self):
        """Affiche la fenêtre À propos"""
        messagebox.showinfo(
            "À propos",
            "Calcul Béton Armé v1.0\n\n"
            "Application de calcul de sections en béton armé\n"
            "Développée avec Python et CustomTkinter"
        )
        
    def show_help(self):
        """Affiche la fenêtre d'aide"""
        help_text = """
        Guide d'utilisation :
        
        1. Entrez les caractéristiques du béton (fck) et de l'acier (fyk)
        2. Entrez les dimensions de la section (h, bw, d)
        3. Entrez le moment de flexion ultime (Mu)
        4. Sélectionnez la situation (normale ou accidentelle)
        5. Cliquez sur CALCULER pour obtenir les résultats
        
        Les résultats donnent les sections d'armatures nécessaires.
        """
        messagebox.showinfo("Aide", help_text)

if __name__ == "__main__":
    root = ctk.CTk()
    app = BetonArmeGUI(root)
    root.mainloop() 