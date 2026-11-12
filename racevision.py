import tkinter as tk
import tkinter.ttk as ttk
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
plt.ioff()


# PALETTE F1


F1_BG        = "#0D0D0D"   # fond principal noir
F1_BG2       = "#1A1A1A"   # fond secondaire
F1_CARD      = "#242424"   # fond des cartes
F1_RED       = "#E10600"   # rouge F1 officiel
F1_WHITE     = "#FFFFFF"
F1_GREY      = "#CCCCCC"
F1_GREY_DIM  = "#888888"
F1_YELLOW    = "#FFD700"   # accent doré

def appliquer_theme(fenetre):
    fenetre.configure(bg=F1_BG)

def style_global():
    s = ttk.Style()
    s.theme_use("clam")

    # Fenêtre / fond général
    s.configure(".",           background=F1_BG,  foreground=F1_WHITE,  font=("Helvetica", 11))

    # Labels
    s.configure("TLabel",      background=F1_BG,  foreground=F1_WHITE)
    s.configure("Dim.TLabel",  background=F1_BG,  foreground=F1_GREY_DIM)
    s.configure("Title.TLabel",background=F1_BG,  foreground=F1_WHITE,  font=("Helvetica", 36, "bold"))
    s.configure("Sub.TLabel",  background=F1_BG,  foreground=F1_GREY,   font=("Helvetica", 16))
    s.configure("Sect.TLabel", background=F1_BG,  foreground=F1_RED,    font=("Helvetica", 14, "bold"))
    s.configure("Head.TLabel", background=F1_BG,  foreground=F1_YELLOW, font=("Helvetica", 11, "bold"))

    # Séparateurs
    s.configure("TSeparator",  background=F1_RED)

    # Boutons — fond rouge, texte blanc
    s.configure("TButton",
                background=F1_RED, foreground=F1_WHITE,
                font=("Helvetica", 11, "bold"),
                borderwidth=0, relief="flat", padding=6)
    s.map("TButton",
          background=[("active", "#FF3D33"), ("pressed", "#B00400")],
          foreground=[("active", F1_WHITE)])

    # Bouton retour — plus discret
    s.configure("Back.TButton",
                background=F1_BG2, foreground=F1_GREY,
                font=("Helvetica", 10),
                borderwidth=0, relief="flat", padding=4)
    s.map("Back.TButton",
          background=[("active", "#2A2A2A")],
          foreground=[("active", F1_WHITE)])

    # Combobox
    s.configure("TCombobox",
                fieldbackground=F1_CARD, background=F1_CARD,
                foreground=F1_WHITE, selectbackground=F1_RED,
                selectforeground=F1_WHITE, arrowcolor=F1_RED,
                borderwidth=1, relief="flat")
    s.map("TCombobox",
          fieldbackground=[("readonly", F1_CARD)],
          foreground=[("readonly", F1_WHITE)])

    # Scrollbar
    s.configure("TScrollbar",
                background=F1_BG2, troughcolor=F1_BG,
                arrowcolor=F1_RED, borderwidth=0)


# LECTURE DU CSV

def lire_csv(chemin):
    donnees = []
    f = open(chemin, "r", encoding="utf-8-sig")
    premiere_ligne = f.readline().rstrip("\n").rstrip("\r")
    colonnes = premiere_ligne.split(";")
    for ligne in f:
        ligne = ligne.rstrip("\n").rstrip("\r")
        if ligne == "":
            continue
        valeurs = ligne.split(";")
        entree = {}
        for i in range(len(colonnes)):
            entree[colonnes[i]] = valeurs[i] if i < len(valeurs) else ""
        donnees.append(entree)
    f.close()
    return donnees

def get_pilotes(donnees):
    pilotes = []
    for e in donnees:
        if e["Pilote"] not in pilotes and e["Pilote"] != "":
            pilotes.append(e["Pilote"])
    pilotes.sort()
    return pilotes

def get_courses(donnees):
    courses = []
    for e in donnees:
        if e["Grand Prix"] not in courses and e["Grand Prix"] != "":
            courses.append(e["Grand Prix"])
    return courses

donnees = lire_csv("F1_2025_Data_Ultimate.csv")
pilotes = get_pilotes(donnees)
courses = get_courses(donnees)


# HELPERS UI


def mk_fenetre(titre):
    """Crée une Toplevel stylisée."""
    f = tk.Toplevel(fenetre)
    f.title(titre)
    f.geometry("1150x740")
    f.configure(bg=F1_BG)
    return f

def barre_rouge(parent, h=4):
    tk.Frame(parent, bg=F1_RED, height=h).pack(fill="x")

def btn_retour(parent):
    ttk.Button(parent, text="← Retour à l'accueil",
               style="Back.TButton",
               command=parent.destroy).pack(anchor="w", padx=20, pady=10)

def titre_page(parent, texte):
    ttk.Label(parent, text=texte, style="Title.TLabel").pack(pady=20)

def separateur(parent):
    ttk.Separator(parent, orient="horizontal").pack(fill="x", padx=100, pady=16)

def label_info(parent, texte, **kw):
    ttk.Label(parent, text=texte,
              font=("Helvetica", 11), wraplength=900,
              justify="left", background=F1_BG, foreground=F1_GREY,
              **kw).pack(anchor="w", pady=2, padx=10)

# PAGE STATISTIQUES MOYENNES

def ouvrir_stat_moy():

    def stats_pilote(pilote):
        resultats = [e for e in donnees if e["Pilote"] == pilote]
        if not resultats:
            return {}
        derniere  = resultats[-1]
        victoires = sum(1 for e in resultats if e["Pos Arrivée"] == "1")
        return {
            "moy_points":   derniere["Moyenne Points/GP"],
            "moy_position": derniere["Moyenne Pos Arrivée"],
            "taux_dnf":     derniere["Taux DNF (%)"],
            "victoires":    str(victoires),
        }

    def afficher_stats():
        pilote = var_pilote.get()
        if pilote == "":
            return
        stats = stats_pilote(pilote)
        label_moy_points.config(  text="Moyenne de points par course : " + stats["moy_points"])
        label_moy_position.config(text="Moyenne de position d'arrivée : " + stats["moy_position"])
        label_taux_dnf.config(    text="Taux de DNF : " + stats["taux_dnf"] + "%")
        label_victoires.config(   text="Nombre de victoires : " + stats["victoires"])

    f2 = mk_fenetre("Statistiques moyennes")
    barre_rouge(f2)
    btn_retour(f2)
    titre_page(f2, "Statistiques moyennes")
    separateur(f2)

    ttk.Label(f2, text="Choisissez un pilote :",
              font=("Helvetica", 13)).pack(pady=10)

    var_pilote = tk.StringVar()
    ttk.Combobox(f2, textvariable=var_pilote, values=pilotes,
                 state="readonly", width=40).pack(pady=10, ipady=5)

    ttk.Button(f2, text="Afficher les statistiques", width=40,
               command=afficher_stats).pack(pady=15, ipady=8)

    separateur(f2)

    def stat_label(texte):
        l = tk.Label(f2, text=texte,
                     font=("Helvetica", 13),
                     bg=F1_CARD, fg=F1_WHITE,
                     padx=20, pady=10, relief="flat")
        l.pack(pady=6, ipadx=10)
        return l

    label_moy_points   = stat_label("Moyenne de points par course : ")
    label_moy_position = stat_label("Moyenne de position d'arrivée : ")
    label_taux_dnf     = stat_label("Taux de DNF : ")
    label_victoires    = stat_label("Nombre de victoires : ")


# PAGE STATISTIQUES PRÉCISES

def ouvrir_stat_precise():

    def get_stats(pilote, course):
        for e in donnees:
            if e["Pilote"] == pilote and e["Grand Prix"] == course:
                return e
        return {}

    def afficher_stats():
        pilote = var_pilote.get()
        course = var_course.get()
        if pilote == "" or course == "":
            return
        stats = get_stats(pilote, course)
        vide  = "—"
        if not stats:
            for v in [val_depart, val_arrivee, val_points, val_temps,
                      val_podium, val_dnf, val_cumules, val_moy_pts,
                      val_moy_pos, val_taux_dnf]:
                v.config(text=vide)
            return
        podium = "✅ Oui" if stats["Podium"] == "1" else "❌ Non"
        dnf    = "❌ Oui" if stats["DNF"]    == "1" else "✅ Non"
        val_depart.config(   text=stats["Pos Départ"])
        val_arrivee.config(  text=stats["Pos Arrivée"])
        val_points.config(   text=stats["Points Course"] + " pts")
        val_temps.config(    text=stats["Temps"])
        val_podium.config(   text=podium)
        val_dnf.config(      text=dnf)
        val_cumules.config(  text=stats["Points Cumulés"] + " pts")
        val_moy_pts.config(  text=stats["Moyenne Points/GP"] + " pts")
        val_moy_pos.config(  text=stats["Moyenne Pos Arrivée"])
        val_taux_dnf.config( text=stats["Taux DNF (%)"] + "%")

    def bloc(parent, titre):
        cadre = tk.Frame(parent, bg=F1_CARD, padx=20, pady=10)
        cadre.pack(side="left", padx=10)
        tk.Label(cadre, text=titre,
                 font=("Helvetica", 9), bg=F1_CARD, fg=F1_GREY_DIM).pack()
        val = tk.Label(cadre, text="—",
                       font=("Helvetica", 22, "bold"),
                       bg=F1_CARD, fg=F1_WHITE)
        val.pack()
        return val

    def titre_section(parent, texte):
        tk.Label(parent, text=texte,
                 font=("Helvetica", 10, "bold"),
                 bg=F1_BG, fg=F1_RED).pack(pady=(14, 4))

    f3 = mk_fenetre("Statistiques précises")
    barre_rouge(f3)
    btn_retour(f3)
    titre_page(f3, "Statistiques précises")
    separateur(f3)

    cadre_sel = tk.Frame(f3, bg=F1_BG)
    cadre_sel.pack(pady=15)

    for label_txt, var_attr, width in [("Pilote", "var_pilote", 30), ("Grand Prix", "var_course", 30)]:
        c = tk.Frame(cadre_sel, bg=F1_BG)
        c.pack(side="left", padx=40)
        tk.Label(c, text=label_txt, font=("Helvetica", 11),
                 bg=F1_BG, fg=F1_GREY).pack()
        locals()[var_attr] = tk.StringVar()

    # Rebuild properly (closures need explicit vars)
    for w in cadre_sel.winfo_children():
        w.destroy()

    c1 = tk.Frame(cadre_sel, bg=F1_BG); c1.pack(side="left", padx=40)
    tk.Label(c1, text="Pilote", font=("Helvetica", 11), bg=F1_BG, fg=F1_GREY).pack()
    var_pilote = tk.StringVar()
    ttk.Combobox(c1, textvariable=var_pilote, values=pilotes,
                 state="readonly", width=30).pack(ipady=4)

    c2 = tk.Frame(cadre_sel, bg=F1_BG); c2.pack(side="left", padx=40)
    tk.Label(c2, text="Grand Prix", font=("Helvetica", 11), bg=F1_BG, fg=F1_GREY).pack()
    var_course = tk.StringVar()
    ttk.Combobox(c2, textvariable=var_course, values=courses,
                 state="readonly", width=30).pack(ipady=4)

    ttk.Button(f3, text="Afficher les statistiques", width=40,
               command=afficher_stats).pack(pady=15, ipady=8)

    separateur(f3)

    titre_section(f3, "RÉSULTATS DE LA COURSE")
    cadre_ligne1 = tk.Frame(f3, bg=F1_BG)
    cadre_ligne1.pack(pady=6)
    val_depart  = bloc(cadre_ligne1, "Pos. Départ")
    val_arrivee = bloc(cadre_ligne1, "Pos. Arrivée")
    val_points  = bloc(cadre_ligne1, "Points")
    val_temps   = bloc(cadre_ligne1, "Temps")
    val_podium  = bloc(cadre_ligne1, "Podium")
    val_dnf     = bloc(cadre_ligne1, "DNF")

    titre_section(f3, "STATISTIQUES SAISON")
    cadre_ligne2 = tk.Frame(f3, bg=F1_BG)
    cadre_ligne2.pack(pady=6)
    val_cumules  = bloc(cadre_ligne2, "Points cumulés")
    val_moy_pts  = bloc(cadre_ligne2, "Moy. points/GP")
    val_moy_pos  = bloc(cadre_ligne2, "Moy. position")
    val_taux_dnf = bloc(cadre_ligne2, "Taux DNF")


# PAGE COMPARAISON

def ouvrir_comparaison():

    def get_stats_comp(pilote, course):
        for e in donnees:
            if e["Pilote"] == pilote and e["Grand Prix"] == course:
                try:    pts = float(e["Points Course"])
                except: pts = 0.0
                try:    pos_dep = float(e["Pos Départ"])
                except: pos_dep = 20.0
                try:    pos_arr = float(e["Pos Arrivée"])
                except: pos_arr = 20.0
                podium = 1.0 if e["Podium"] == "1" else 0.0
                try:    taux_dnf = float(e["Taux DNF (%)"])
                except: taux_dnf = 0.0
                return {
                    "Points":       pts,
                    "Pos. départ":  pos_dep,
                    "Pos. arrivée": pos_arr,
                    "Podium":       podium,
                    "Taux DNF (%)": taux_dnf,
                }
        return None

    def dessiner_radar(stats1, stats2, pilote1, pilote2):
        for w in cadre_graphique.winfo_children():
            w.destroy()
        categories = list(stats1.keys())
        N          = len(categories)
        inverser   = ["Pos. départ", "Pos. arrivée", "Taux DNF (%)"]
        max_fixes  = {
            "Points":       25.0,
            "Pos. départ":  20.0,
            "Pos. arrivée": 20.0,
            "Podium":       1.0,
            "Taux DNF (%)": 100.0,
        }
        valeurs1 = list(stats1.values())
        valeurs2 = list(stats2.values())
        valeurs_norm1 = []
        valeurs_norm2 = []
        for i in range(N):
            cat  = categories[i]
            maxi = max_fixes.get(cat, max(valeurs1[i], valeurs2[i], 1))
            n1   = valeurs1[i] / maxi
            n2   = valeurs2[i] / maxi
            if cat in inverser:
                n1 = 1 - n1
                n2 = 1 - n2
            valeurs_norm1.append(n1)
            valeurs_norm2.append(n2)
        valeurs_norm1 += [valeurs_norm1[0]]
        valeurs_norm2 += [valeurs_norm2[0]]
        angles  = [n / float(N) * 2 * np.pi for n in range(N)]
        angles += [angles[0]]

        fig = Figure(figsize=(7, 6), facecolor=F1_BG2)
        ax  = fig.add_subplot(111, polar=True)
        ax.set_facecolor(F1_BG2)
        ax.set_theta_offset(np.pi / 2)
        ax.set_theta_direction(-1)
        ax.set_xticks(angles[:-1])
        ax.set_xticklabels(categories, fontsize=10, color=F1_WHITE)
        ax.tick_params(pad=16, colors=F1_WHITE)
        ax.set_yticklabels([])
        ax.set_ylim(0, 1)
        ax.spines["polar"].set_color(F1_GREY_DIM)
        ax.grid(color=F1_GREY_DIM, linestyle="--", alpha=0.4)

        ax.plot(angles, valeurs_norm1, linewidth=2, color=F1_RED,    label=pilote1)
        ax.fill(angles, valeurs_norm1, alpha=0.25,  color=F1_RED)
        ax.plot(angles, valeurs_norm2, linewidth=2, color=F1_YELLOW, label=pilote2)
        ax.fill(angles, valeurs_norm2, alpha=0.25,  color=F1_YELLOW)

        legend = ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.15), fontsize=10)
        legend.get_frame().set_facecolor(F1_CARD)
        for text in legend.get_texts():
            text.set_color(F1_WHITE)

        ax.set_title("Comparaison", pad=25, fontsize=12, color=F1_WHITE)
        fig.tight_layout(pad=3)

        canvas = FigureCanvasTkAgg(fig, master=cadre_graphique)
        canvas.draw()
        canvas.get_tk_widget().pack()

    def afficher():
        pilote1 = var_pilote1.get()
        pilote2 = var_pilote2.get()
        course  = var_course.get()
        if pilote1 == "" or pilote2 == "" or course == "" or pilote1 == pilote2:
            return
        stats1 = get_stats_comp(pilote1, course)
        stats2 = get_stats_comp(pilote2, course)
        if not stats1 or not stats2:
            return
        dessiner_radar(stats1, stats2, pilote1, pilote2)

    f5 = mk_fenetre("Comparaison par course")
    barre_rouge(f5)
    btn_retour(f5)
    titre_page(f5, "Comparaison par course")
    separateur(f5)

    cadre_sel = tk.Frame(f5, bg=F1_BG)
    cadre_sel.pack(pady=10)

    for label_txt, var_name, vals in [
        ("Pilote 1",   "var_pilote1", pilotes),
        ("Pilote 2",   "var_pilote2", pilotes),
        ("Grand Prix", "var_course",  courses),
    ]:
        c = tk.Frame(cadre_sel, bg=F1_BG)
        c.pack(side="left", padx=30)
        tk.Label(c, text=label_txt, font=("Helvetica", 11),
                 bg=F1_BG, fg=F1_GREY).pack()

    # Rebuild with proper variable scope
    for w in cadre_sel.winfo_children():
        w.destroy()

    cp1 = tk.Frame(cadre_sel, bg=F1_BG); cp1.pack(side="left", padx=30)
    tk.Label(cp1, text="Pilote 1", font=("Helvetica", 11), bg=F1_BG, fg=F1_GREY).pack()
    var_pilote1 = tk.StringVar()
    ttk.Combobox(cp1, textvariable=var_pilote1, values=pilotes,
                 state="readonly", width=25).pack(ipady=4)

    cp2 = tk.Frame(cadre_sel, bg=F1_BG); cp2.pack(side="left", padx=30)
    tk.Label(cp2, text="Pilote 2", font=("Helvetica", 11), bg=F1_BG, fg=F1_GREY).pack()
    var_pilote2 = tk.StringVar()
    ttk.Combobox(cp2, textvariable=var_pilote2, values=pilotes,
                 state="readonly", width=25).pack(ipady=4)

    cgp = tk.Frame(cadre_sel, bg=F1_BG); cgp.pack(side="left", padx=30)
    tk.Label(cgp, text="Grand Prix", font=("Helvetica", 11), bg=F1_BG, fg=F1_GREY).pack()
    var_course = tk.StringVar()
    ttk.Combobox(cgp, textvariable=var_course, values=courses,
                 state="readonly", width=25).pack(ipady=4)

    ttk.Button(f5, text="Comparer", width=40,
               command=afficher).pack(pady=15, ipady=8)

    separateur(f5)

    cadre_graphique = tk.Frame(f5, bg=F1_BG)
    cadre_graphique.pack()


# PAGE INFOS UTILES

def ouvrir_infos():

    f6 = mk_fenetre("Infos utiles")
    barre_rouge(f6)
    btn_retour(f6)
    titre_page(f6, "Infos utiles")
    separateur(f6)

    # Zone scrollable
    cadre_scroll = tk.Frame(f6, bg=F1_BG)
    cadre_scroll.pack(fill="both", expand=True, padx=40, pady=10)

    scrollbar = ttk.Scrollbar(cadre_scroll)
    scrollbar.pack(side="right", fill="y")

    canvas_scroll = tk.Canvas(cadre_scroll, yscrollcommand=scrollbar.set,
                              bg=F1_BG, highlightthickness=0)
    canvas_scroll.pack(side="left", fill="both", expand=True)
    scrollbar.config(command=canvas_scroll.yview)

    cadre_contenu = tk.Frame(canvas_scroll, bg=F1_BG)
    canvas_scroll.create_window((0, 0), window=cadre_contenu, anchor="nw")

    def maj_scroll(event):
        canvas_scroll.configure(scrollregion=canvas_scroll.bbox("all"))
    cadre_contenu.bind("<Configure>", maj_scroll)

    def section(titre):
        tk.Frame(cadre_contenu, bg=F1_RED, height=2).pack(fill="x", pady=(16, 0))
        tk.Label(cadre_contenu, text=titre,
                 font=("Helvetica", 14, "bold"),
                 bg=F1_BG2, fg=F1_RED,
                 padx=10, pady=6, anchor="w"
                 ).pack(fill="x", pady=(0, 6))

    def texte(contenu):
        tk.Label(cadre_contenu, text=contenu,
                 font=("Helvetica", 11),
                 wraplength=960, justify="left",
                 bg=F1_BG, fg=F1_GREY,
                 anchor="w").pack(anchor="w", pady=2, padx=14)

    # ── SYSTÈME DE POINTS ──────────────────────────────

    # Couleurs par position (or / argent / bronze / reste)
    COULEURS_POSITIONS = {
        0: ("#FFD700", "#1A1700"),   # 1er — or
        1: ("#C0C0C0", "#111111"),   # 2ème — argent
        2: ("#CD7F32", "#1A0E00"),   # 3ème — bronze
    }
    COULEUR_DEFAUT = (F1_WHITE, F1_CARD)

    section("🏆  Système de points")
    texte("Les points sont attribués aux 10 premiers pilotes à l'arrivée de chaque Grand Prix.")

    cadre_pts = tk.Frame(cadre_contenu, bg=F1_BG)
    cadre_pts.pack(anchor="w", padx=14, pady=6)

    # En-tête du tableau
    ent = tk.Frame(cadre_pts, bg=F1_RED)
    ent.pack(fill="x")
    for txt, w in [("Position", 18), ("Points attribués", 22)]:
        tk.Label(ent, text=txt, font=("Helvetica", 11, "bold"),
                 bg=F1_RED, fg=F1_WHITE, width=w, anchor="w",
                 padx=8, pady=4).pack(side="left")

    bareme = [
        ("1ère place",  "25 points"),
        ("2ème place",  "18 points"),
        ("3ème place",  "15 points"),
        ("4ème place",  "12 points"),
        ("5ème place",  "10 points"),
        ("6ème place",  "8 points"),
        ("7ème place",  "6 points"),
        ("8ème place",  "4 points"),
        ("9ème place",  "2 points"),
        ("10ème place", "1 point"),
    ]
    for i, (pos, pts) in enumerate(bareme):
        fg, bg = COULEURS_POSITIONS.get(i, COULEUR_DEFAUT)
        ligne = tk.Frame(cadre_pts, bg=bg)
        ligne.pack(fill="x")
        tk.Label(ligne, text=pos, font=("Helvetica", 11, "bold"),
                 bg=bg, fg=fg, width=18, anchor="w", padx=8, pady=3).pack(side="left")
        tk.Label(ligne, text=pts, font=("Helvetica", 11),
                 bg=bg, fg=fg, width=22, anchor="w", padx=8, pady=3).pack(side="left")

    texte("Le pilote avec le plus de points en fin de saison remporte le titre de Champion du Monde.")
    texte("Pour les constructeurs, les points des deux pilotes de l'équipe sont additionnés à chaque course.")

    #  RÈGLES GÉNÉRALES 

    section("📋  Règles générales")
    regles = [
        "• Un Grand Prix se déroule sur un week-end : essais libres (vendredi), qualifications (samedi), course (dimanche).",
        "• La grille de départ est déterminée par les qualifications : le plus rapide part en pole position (1ère place).",
        "• La course dure environ 305 km (sauf Monaco : 260 km).",
        "• Chaque pilote doit utiliser au moins 2 types de pneus différents pendant la course.",
        "• Un arrêt au stand (pit stop) est obligatoire pour changer les pneus.",
        "• DNF (Did Not Finish) : un pilote qui abandonne ne marque aucun point.",
        "• En cas d'égalité de points en fin de saison, le pilote avec le plus de victoires est champion.",
        "• La saison 2025 compte 24 Grands Prix sur tous les continents.",
    ]
    for r in regles:
        texte(r)

    #  LES DRAPEAUX 
    # Couleurs réelles des drapeaux

    DRAPEAUX_STYLE = {
        # (bg_badge, fg_badge, bg_ligne, fg_desc)
        "🟢  Vert":             ("#1DB954", "#FFFFFF", "#0A2010", F1_GREY),
        "🟡  Jaune":            ("#FFD700", "#111111", "#1A1500", F1_GREY),
        "🔴  Rouge":            (F1_RED,    "#FFFFFF", "#1A0000", F1_GREY),
        "⬛  Noir":             ("#222222", "#FFFFFF", "#111111", F1_GREY),
        "⬜  Blanc":            ("#DDDDDD", "#111111", "#1A1A1A", F1_GREY),
        "🏁  Damier":           ("#FFFFFF", "#111111", "#1A1A1A", F1_GREY),
        "🟡⬛ Jaune et noir":  ("#FFD700", "#111111", "#1A1500", F1_GREY),
        "🔵  Bleu":             ("#1565C0", "#FFFFFF", "#001020", F1_GREY),
        "🔴⬛ Rouge et noir":  (F1_RED,    "#FFFFFF", "#1A0000", F1_GREY),
    }

    section("🚩  Les drapeaux")

    drapeaux = [
        ("🟢  Vert",             "La piste est dégagée, la course est en cours normalement."),
        ("🟡  Jaune",            "Danger sur la piste. Les pilotes doivent ralentir et ne pas dépasser. Un seul jaune = danger localisé. Deux jaunes = danger important."),
        ("🔴  Rouge",            "La course est interrompue. Tous les pilotes doivent rejoindre les stands lentement."),
        ("⬛  Noir",             "Affiché avec un numéro : ce pilote est disqualifié et doit rentrer aux stands immédiatement."),
        ("⬜  Blanc",            "Un véhicule lent est sur la piste (voiture de sécurité, ambulance...)."),
        ("🏁  Damier",           "Fin de la course ! Agité quand le vainqueur franchit la ligne d'arrivée."),
        ("🟡⬛ Jaune et noir",   "Avertissement pour comportement antisportif. Deux fois = disqualification."),
        ("🔵  Bleu",             "Un pilote va être doublé par un pilote ayant un tour d'avance. Il doit laisser passer."),
        ("🔴⬛ Rouge et noir",   "La voiture a un problème mécanique dangereux. Le pilote doit rentrer aux stands."),
    ]

    cadre_drapeaux = tk.Frame(cadre_contenu, bg=F1_BG)
    cadre_drapeaux.pack(anchor="w", padx=14, pady=6, fill="x")

    for drapeau, description in drapeaux:
        style = DRAPEAUX_STYLE.get(drapeau, ("#555555", F1_WHITE, F1_BG, F1_GREY))
        bg_badge, fg_badge, bg_ligne, fg_desc = style

        ligne = tk.Frame(cadre_drapeaux, bg=bg_ligne, pady=2)
        ligne.pack(fill="x", pady=2)

        tk.Label(ligne, text=drapeau,
                 font=("Helvetica", 11, "bold"),
                 bg=bg_badge, fg=fg_badge,
                 width=20, anchor="w", padx=8, pady=5).pack(side="left")

        tk.Label(ligne, text=description,
                 font=("Helvetica", 11),
                 bg=bg_ligne, fg=fg_desc,
                 wraplength=750, justify="left",
                 padx=12).pack(side="left")

    #  VOITURE DE SÉCURITÉ 

    section("🚗  Voiture de sécurité (Safety Car)")
    texte("La Safety Car entre en piste quand il y a un danger important mais pas suffisant pour arrêter la course.")
    texte("Pendant le Safety Car : tous les pilotes doivent suivre à vitesse réduite, les dépassements sont interdits.")
    texte("Le Virtual Safety Car (VSC) est similaire mais sans voiture physique — les pilotes maintiennent une vitesse minimale imposée.")

    # LES PNEUS 
    
    PNEUS_STYLE = {
        "🔴  Soft (tendre)":   ("#E10600", "#FFFFFF", "#1A0000", F1_GREY),
        "🟡  Medium (médium)": ("#FFD700", "#111111", "#1A1500", F1_GREY),
        "⬜  Hard (dur)":      ("#EEEEEE", "#111111", "#1A1A1A", F1_GREY),
        "🟢  Intermédiaire":   ("#1DB954", "#FFFFFF", "#0A2010", F1_GREY),
        "🔵  Pluie (wet)":     ("#1565C0", "#FFFFFF", "#001020", F1_GREY),
    }

    section("🔄  Les pneus Pirelli")

    pneus = [
        ("🔴  Soft (tendre)",   "Le plus rapide mais s'use très vite. Utilisé sur circuit court ou en qualifications."),
        ("🟡  Medium (médium)", "Bon compromis entre vitesse et durée. Le pneu le plus polyvalent."),
        ("⬜  Hard (dur)",      "Le plus lent mais dure très longtemps. Idéal pour les longues relances."),
        ("🟢  Intermédiaire",   "Pour piste humide mais pas détrempée. Évacue l'eau rapidement."),
        ("🔵  Pluie (wet)",     "Pour fortes pluies. Évacue beaucoup d'eau mais très lent sur piste sèche."),
    ]

    cadre_pneus = tk.Frame(cadre_contenu, bg=F1_BG)
    cadre_pneus.pack(anchor="w", padx=14, pady=6, fill="x")

    for pneu, description in pneus:
        style = PNEUS_STYLE.get(pneu, ("#555555", F1_WHITE, F1_BG, F1_GREY))
        bg_badge, fg_badge, bg_ligne, fg_desc = style

        ligne = tk.Frame(cadre_pneus, bg=bg_ligne, pady=2)
        ligne.pack(fill="x", pady=3)

        tk.Label(ligne, text=pneu,
                 font=("Helvetica", 11, "bold"),
                 bg=bg_badge, fg=fg_badge,
                 width=20, anchor="w", padx=8, pady=6).pack(side="left")

        tk.Label(ligne, text=description,
                 font=("Helvetica", 11),
                 bg=bg_ligne, fg=fg_desc,
                 wraplength=750, justify="left",
                 padx=12).pack(side="left")

    texte("Règle des pneus : chaque pilote doit utiliser au moins 2 types de pneus secs différents pendant la course.")

    # Espace en bas
    tk.Frame(cadre_contenu, bg=F1_BG, height=30).pack()


# PAGE ACCUEIL — fenêtre principale


fenetre = tk.Tk()
fenetre.title("RaceVision - Analyse F1")
fenetre.geometry("1150x740")
fenetre.configure(bg=F1_BG)

style_global()

# Barre rouge du haut
tk.Frame(fenetre, bg=F1_RED, height=6).pack(fill="x")

# Logo / titre
tk.Label(fenetre, text="RACEVISION",
         font=("Helvetica", 48, "bold"),
         bg=F1_BG, fg=F1_WHITE).pack(pady=(40, 4))

tk.Label(fenetre, text="Analyse des performances F1",
         font=("Helvetica", 16),
         bg=F1_BG, fg=F1_GREY_DIM).pack()

# Ligne rouge décorative
tk.Frame(fenetre, bg=F1_RED, height=3, width=300).pack(pady=20)

ttk.Separator(fenetre, orient="horizontal").pack(fill="x", padx=150, pady=10)

tk.Label(fenetre, text="Que voulez-vous consulter ?",
         font=("Helvetica", 13),
         bg=F1_BG, fg=F1_GREY).pack(pady=20)

for txt, cmd in [
    ("Statistiques moyennes", ouvrir_stat_moy),
    ("Statistiques précises", ouvrir_stat_precise),
    ("Comparateur",           ouvrir_comparaison),
    ("Infos utiles",          ouvrir_infos),
]:
    ttk.Button(fenetre, text=txt, width=50, command=cmd).pack(pady=10, ipadx=10, ipady=8)

# Barre rouge du bas
tk.Frame(fenetre, bg=F1_RED, height=4).pack(fill="x", side="bottom")

fenetre.mainloop()

