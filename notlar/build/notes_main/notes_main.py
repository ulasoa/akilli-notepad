

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import*
#2.hafta
import json
#--


app = QApplication([])


""" #2.hafta ----3.hafta da sil..
'''json'daki notlar'''
notes = {
    "Hoş geldiniz!" : {
        "metin" : "Bu dünyanın en iyi not alma uygulaması!",
        "etiketler" : ["iyilik", "talimat"]
    }
}
with open("notes_data.json", "w") as file:
    json.dump(notes, file)
#-- """


'''Uygulama arayüzü'''
#uygulama penceresi parametreleri
notes_win =QWidget()
notes_win.setWindowTitle('Akıllı notlar')
notes_win.resize(900,600)


#uygulama penceresi widget'ları
list_notes =QListWidget()
list_notes_label = QLabel('Notların Listesi')


button_note_create =QPushButton('Not oluştur')
button_note_del = QPushButton('Not Sil')
button_note_save = QPushButton('Notu Kaydet')


field_tag = QLineEdit('')#sağ alttaki küçük kutucuk
field_tag.setPlaceholderText('Etiketi giriniz..')
field_text =QTextEdit()#soldaki büyük alan


button_tag_add =QPushButton('Nota ekle')
button_tag_del =QPushButton('Nottan çıkar')
button_tag_search =QPushButton('Notları etikete göre ara')


list_tags = QListWidget()
list_tags_label =QLabel('Etiket listesi')
#anahat düzenine göre widget'ların konumu


layout_notes = QHBoxLayout()#genel yatay hizalama
col_1 =QVBoxLayout()#1.dikey çizgi
col_1.addWidget(field_text)


col_2=QVBoxLayout()#2.dikey
col_2.addWidget(list_notes_label)
col_2.addWidget(list_notes)


row_1 = QHBoxLayout()
row_1.addWidget(button_note_create)
row_1.addWidget(button_note_del)


row_2=QHBoxLayout()
row_2.addWidget(button_note_save)


col_2.addLayout(row_1)#2.dikey çizgiye ekle
col_2.addLayout(row_2)#2.dikey çizgiye ekle


col_2.addWidget(list_tags_label)
col_2.addWidget(list_tags)
col_2.addWidget(field_tag)


row_3 =QHBoxLayout()
row_3.addWidget(button_tag_add)#butonlar
row_3.addWidget(button_tag_del)


row_4 =QHBoxLayout()
row_4.addWidget(button_tag_search)


col_2.addLayout(row_3)#2.dikeye yatay çizgi ekle
col_2.addLayout(row_4)


#ekranı 3'e bölüyoruz
layout_notes.addLayout(col_1, stretch=2)
layout_notes.addLayout(col_2, stretch=1)
notes_win.setLayout(layout_notes)


#2.hafta
def show_note():
    #nottan metni vurgulanan adıyla alır ve düzenle alanında görüntüleriz
    key = list_notes.selectedItems()[0].text()
    print(key)
    field_text.setText(notes[key]["metin"])#soldaki büyük alana seçtimiz notu getirir.
    list_tags.clear()#etiket temizle
    list_tags.addItems(notes[key]["etiketler"])#Seçilen notun etiketlerini listede gösterir.


def add_note():#Yeni not ismini sorar ve boş bir not oluşturur.
    note_name, ok = QInputDialog.getText(notes_win, "Not ekle", "Notun adı: ")
    if ok and note_name != "":# ok basıldı ve boş değilse
        notes[note_name] = {"metin" : "", "etiketler" : []}#sözlük yapısını oluştur
        list_notes.addItem(note_name)#Notlar listesine ekle
        list_tags.addItems(notes[note_name]["etiketler"])#etiketler listesine ekle
        print(notes) 


def save_note():#seçilen notu güncelleyip kaydeder.
    if list_notes.selectedItems():#bir not seçili ise
        key = list_notes.selectedItems()[0].text()#Seçilen notun ilk elamanını al
        notes[key]["metin"] = field_text.toPlainText()#Soldaki büyük alandan yeni metini al.metin sözlüğüne kaydet
        with open("notes_data.json", "w") as file: #yeni metin olduğundan json dosyasnı güncelliyoruz
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Kaydedilecek not seçili değil!")


def del_note():
    if list_notes.selectedItems():
        key = list_notes.selectedItems()[0].text()
        del notes[key]
        list_notes.clear()
        list_tags.clear()
        field_text.clear()
        list_notes.addItems(notes)#Sildiğimiz için notları tekrar notlarımıza son halini ekliyoruz.
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Silinecek not seçili değil!")


'''Not etiketiyle çalışma'''
def add_tag():
    if list_notes.selectedItems():#list nottan bir not seçili ise
        key = list_notes.selectedItems()[0].text()
        tag = field_tag.text()#tag alanında ki etiketi okur 
        if not tag in notes[key]["etiketler"]:
            notes[key]["etiketler"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Etiket eklemek için not seçili değil!")


def del_tag():
    if list_tags.selectedItems():
        key = list_notes.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["etiketler"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["etiketler"])
        with open("notes_data.json", "w") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
    else:
        print("Silinecek etiket seçili değil!")


def search_tag():
    print(button_tag_search.text())
    tag = field_tag.text()#tag kısmındaki etiketi oku
    if button_tag_search.text() == "Notları etikete göre ara" and tag:
        print(tag)
        notes_filtered = {} #burada vurgulanmış etikete sahip notlar olacak
        for note in notes:# notları dolaş
            if tag in notes[note]["etiketler"]: #aranan tag notların içinde varsa
                notes_filtered[note]=notes[note] #tagı filtered sözlüğüne aktar
        button_tag_search.setText("Aramayı sıfırla")#düğmenin adını değiş
        list_notes.clear()#listeleri temizle
        list_tags.clear()
        list_notes.addItems(notes_filtered)#bulunan listeyi notlara ekle
        print(button_tag_search.text())
    elif button_tag_search.text() == "Aramayı sıfırla":
        field_tag.clear()
        list_notes.clear()
        list_tags.clear()
        list_notes.addItems(notes)
        button_tag_search.setText("Notları etikete göre ara")
        print(button_tag_search.text())
    else:
        pass


#olay işlemeyi bağlama
list_notes.itemClicked.connect(show_note)#seçtiğim an o fonksiyonu çağır.
button_note_create.clicked.connect(add_note)
button_note_save.clicked.connect(save_note)
button_note_del.clicked.connect(del_note)
button_tag_add.clicked.connect(add_tag)
button_tag_del.clicked.connect(del_tag)
button_tag_search.clicked.connect(search_tag)


#--



#uygulamayı başlatma 
notes_win.show()


#2.hafta
with open("notes_data.json", "r") as file:
    notes = json.load(file)
list_notes.addItems(notes)


#--


app.exec_()

