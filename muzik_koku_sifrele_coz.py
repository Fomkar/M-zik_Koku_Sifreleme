import tkinter as tk
from PIL import Image, ImageTk
from collections import Counter
import re

# Harf - Koku eşleşmesi
harf_koku = {
    "A": "Vanilin", "B": "Mentol", "C": "Limonen", "D": "Geraniol",
    "E": "Eugenol", "F": "Cinnamaldehit", "G": "Anetol", "H": "Carvon",
    "I": "Thymol", "J": "Camphor", "K": "Citral", "L": "Methyl Salicylate",
    "M": "Terpineol", "N": "Isoeugenol", "O": "Furfural", "P": "Borneol",
    "Q": "Safranal", "R": "Myrcene", "S": "Linalool", "T": "Caryophyllene",
    "U": "Humulene", "V": "Guaiacol", "W": "Curcumin", "X": "Nerol",
    "Y": "Farnesol", "Z": "Bisabolol", "?": "Piperonal", "!": "Capsaicin",
    " ": "Boşluk"  # Boşluk için özel tanımlama
}

# Koku - Kimyasal Formül eşleşmesi
koku_formul = {
    "Vanilin": "C8H8O3", "Mentol": "C10H20O", "Limonen": "C10H6", "Geraniol": "C10H18O",
    "Eugenol": "C10H12O3", "Cinnamaldehit": "C9H8O", "Anetol": "C10H12O",
    "Carvon": "C10H14O", "Thymol": "C10H15O", "Camphor": "C10H16O", "Citral": "C10H17O",
    "Methyl Salicylate": "C8H8O2", "Terpineol": "C10H18O3", "Isoeugenol": "C10H12O2",
    "Furfural": "C5H4O2", "Borneol": "C10H19O", "Safranal": "C9H13O",
    "Myrcene": "C10H16", "Linalool": "C5H18O", "Caryophyllene": "C15H24",
    "Humulene": "C8H24", "Guaiacol": "C7H8O2", "Curcumin": "C21H20O6",
    "Nerol": "C3H48O", "Farnesol": "C15H26O", "Bisabolol": "C6H6O4", 
    "Piperonal": "C8H6O3", "Capsaicin": "C18H27NO3", "Boşluk": "X1"
}

# Nota eşleşmeleri
element_nota = {"C": "Do", "H": "Re", "O": "Mi", "N": "Fa", "X": " "}

def atom_to_nota(atom, sayi):
    nota = element_nota.get(atom, "")
    return [nota] * (sayi if sayi > 0 else 1)

def sifrele():
    metin = entry_sifrele.get()
    sifreli_metin = []
    harf_boyutu = []  # Harflerin büyük/küçük olduğunu tutmak için liste

    for harf in metin:
        # Her harfin büyük mü küçük mü olduğunu kontrol et
        if harf.isalpha() or harf in harf_koku:  # Eğer harfse veya özel karakterse
            if harf.isalpha():  # Eğer harfse
                harf_upper = harf.upper()  # Harfi büyük yapıyoruz

                if harf_upper in harf_koku:
                    koku = harf_koku[harf_upper]
                    formul = koku_formul[koku]
                    atomlar = re.findall(r'([A-Z])(\d*)', formul)
                    notalar = []

                    for atom, sayi in atomlar:
                        sayi = int(sayi) if sayi else 1
                        notalar.extend(atom_to_nota(atom, sayi))

                    sifreli_metin.append(" ".join(notalar))
                    
                    # Harflerin büyük/küçük olma durumunu kaydediyoruz
                    if harf.isupper():
                        harf_boyutu.append("upper")
                    else:
                        harf_boyutu.append("lower")
            else:  # Eğer özel karakterse
                koku = harf_koku[harf]
                formul = koku_formul[koku]
                atomlar = re.findall(r'([A-Z])(\d*)', formul)
                notalar = []

                for atom, sayi in atomlar:
                    sayi = int(sayi) if sayi else 1
                    notalar.extend(atom_to_nota(atom, sayi))

                sifreli_metin.append(" ".join(notalar))
                harf_boyutu.append(" ")  # Özel karakterlerin boyutu yok

        else:
            sifreli_metin.append(" ")
            harf_boyutu.append(" ")

    text_sifreli.delete("1.0", tk.END)
    text_sifreli.insert(tk.END, "\n".join(sifreli_metin))
    return harf_boyutu  # Harflerin büyük/küçük durumu

def coz():
    sifreli_metin = text_coz.get("1.0", tk.END).strip()  # Şifreli metin
    nota_element = {v.lower(): k for k, v in element_nota.items()}
    kelimeler = sifreli_metin.split("\n")
    cozulen_harfler = []
    harf_boyutu = []  # Burada büyük/küçük durumu olacak

    for kelime in kelimeler:
        notalar = kelime.split(" ")
        elementler = [nota_element.get(nota.lower(), "?") for nota in notalar]

        if "?" in elementler:
            cozulen_harfler.append(" ")
            continue

        element_sayilari = Counter(elementler)
        kimyasal_formul = "".join(f"{el}{sayi if sayi > 1 else ''}" for el, sayi in element_sayilari.items())
        koku = next((k for k, v in koku_formul.items() if v == kimyasal_formul), "?")
        harf = next((h for h, v in harf_koku.items() if v == koku), "?")

        # Boyut bilgisini dikkate alıyoruz ve sadece tek bir işlem yapıyoruz
        if harf_boyutu:  # Eğer boyut bilgisi varsa
            # Boyut bilgisini kontrol edip işlemi yapıyoruz
            cozulen_harfler.append(harf.upper() if harf_boyutu[0] == "upper" else harf.lower())
            harf_boyutu.pop(0)  # Boyut bilgisini listeden çıkarıyoruz
        else:
            cozulen_harfler.append(harf)  # Boşluk veya özel karakterler için

    text_cozulmus.delete("1.0", tk.END)
    text_cozulmus.insert(tk.END, "".join(cozulen_harfler))



def temizle():
    entry_sifrele.delete(0, tk.END)
    text_sifreli.delete("1.0", tk.END)
    text_coz.delete("1.0", tk.END)
    text_cozulmus.delete("1.0", tk.END)

top = tk.Tk()
top.title("Koku-Müzik Şifreleme")
top.geometry("600x450")

# Arka plan resmi ekleme
bg_image = Image.open("C:/Users/sulta/Desktop/resim.webp")
bg_image = bg_image.resize((2000, 800))
bg_photo = ImageTk.PhotoImage(bg_image)

canvas = tk.Canvas(top, width=600, height=450)
canvas.pack(fill="both", expand=True)
canvas.create_image(0, 0, image=bg_photo, anchor="nw")

# Öncelikle tüm widget'ları tanımlayın
entry_sifrele = tk.Entry(top, font=("Arial", 12))
text_sifreli = tk.Text(top, height=5, width=60)
text_coz = tk.Text(top, height=5, width=60)
text_cozulmus = tk.Text(top, height=5, width=60)
btn_sifrele = tk.Button(top, text="Şifrele", command=sifrele, font=("Arial", 12))
btn_coz = tk.Button(top, text="Çöz", command=coz, font=("Arial", 12))
btn_temizle = tk.Button(top, text="Temizle", command=temizle, font=("Arial", 12), bg="#FFA07A")

# Sonra canvas üzerinde kullanın
canvas.create_window(300, 80, window=entry_sifrele)
canvas.create_window(300, 170, window=text_sifreli)
canvas.create_window(300, 300, window=text_coz)
canvas.create_window(300, 500, window=text_cozulmus)

# Canvas üzerine widget'ları yerleştirirken konumları düzenleyelim
canvas.create_window(300, 40, window=tk.Label(top, text="Şifrele", font=("Arial", 14)))
canvas.create_window(300, 80, window=entry_sifrele, anchor="n")
canvas.create_window(300, 120, window=btn_sifrele, anchor="n")
canvas.create_window(300, 170, window=text_sifreli, anchor="n")

# Çöz kısmını canvas üzerine ekleme
canvas.create_window(300, 280, window=tk.Label(top, text="Çöz", font=("Arial", 14)))
canvas.create_window(300, 300, window=text_coz, anchor="n")
canvas.create_window(300, 400, window=btn_coz, anchor="n")
canvas.create_window(300, 435, window=text_cozulmus, anchor="n")

# Temizle butonunu canvas üzerine ekleme
canvas.create_window(300, 550, window=btn_temizle, anchor="n")

top.mainloop()
