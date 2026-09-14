# Automatic-Docking-Visualization
Automatically visualize docking results both with PyMol and Discovery Studio

# Molecular Docking Automation & Visualization Suite

[English] | [Türkçe]

---

## English

A collection of Python scripts designed to automate post-processing, visualization, complex preparation, and 2D interaction mapping for molecular docking runs.

### Overview of Scripts

* **pymol_render_script.py**: High-throughput 3D rendering of docking poses via PyMOL.
* **Complex_Merger_pdbqt_and_cleanprotein.py**: Merges docking poses (.pdbqt) with target structures (.pdb) into unified complex files.
* **Discovery_Oto.py**: GUI automation pipeline via pyautogui to generate 2D interaction maps using BIOVIA Discovery Studio.

---

### 1. pymol_render_script.py

**Features**

* Loads 5-run docking replicates (*_1_best.pdbqt to *_5_best.pdbqt) directly onto the receptor structure.
* Renders the receptor in translucent surface + wireframe representation, and ligands in multi-color stick format.
* Automatically exports dual camera angles (close-up and overview) at high resolution (1920x1080, 600 DPI, ray-traced).

**Prerequisites & Setup**

* Place the script, target receptor, and ligand files in the same working directory.
* Receptor filename: protein_clean.pdb.
* Ligand format: <molecule_name>_1_best.pdbqt ... <molecule_name>_5_best.pdbqt.
* Camera Views: Open PyMOL, orient your receptor to the desired close/overview views, run get_view, and paste the matrix tuples into view_uzak and view_yakin in the script.
* Color Palette: Ligands are assigned oxygen, violet, deepsalmon, hotpink, and lightpink by default (configurable via ligand_colors).

**Output**

* Generates two ray-traced .png images per molecule:
* <molecule_name>_uzak.png (Overview)
* <molecule_name>_yakin.png (Close-up)



**Usage**
Terminal:
python pymol_render_script.py

Via PyMOL CLI:
pymol -c -q pymol_render_script.py

Note: High-resolution ray-tracing (ray=1, 600 DPI) requires significant computational time depending on molecule count and hardware specifications.

---

### 2. Complex_Merger_pdbqt_and_cleanprotein.py

**Features**

* Iterates over .pdbqt docking results, aligns them with protein_clean.pdb, and saves each pose as a unified .pdb complex.
* Automatically clusters replicate poses of the same ligand into organized subdirectories.

**Prerequisites**

* Python 3.x
* PyMOL installed and accessible (update the PyMOL executable path inside the script if not in your default system PATH).

**Directory Structure**

* Input: protein_clean.pdb and *.pdbqt files in the execution directory.
* Output: Structured under Interaction_Maps/:
* Interaction_Maps/<molecule_name>*complex_interaction/protein*<molecule_name>_1_complex.pdb
* Interaction_Maps/<molecule_name>*complex_interaction/protein*<molecule_name>_2_complex.pdb



**Usage**
python Complex_Merger_pdbqt_and_cleanprotein.py

---

### 3. Discovery_Oto.py

**Features**

* Automates BIOVIA Discovery Studio through computer vision and GUI interaction (pyautogui).
* Handles receptor/ligand definition, 2D diagram generation, and batch export of interaction diagrams.

**Dependencies**
pip install pyautogui pyperclip opencv-python

* Discovery Studio Path: Configure the executable path inside the script (e.g., /opt/BIOVIA/... or your custom installation folder).

**Assets & Layout**

* Reference UI Templates: Ensure the following screenshot anchors are in the script directory:
* interactions_tab.png
* define_receptor_anchor.png
* ligand_icon.png
* define_receptor_btn.png
* define_ligand_btn.png
* show_2d_btn.png


* Input Hierarchy: Interaction_Maps/<molecule_name>*complex_interaction/protein*<ligand_name>_complex.pdb
* Output: Interaction_Maps/<molecule_name>_complex_interaction/<ligand_name>_interaction_map.png

**Critical Precautions**

* Clean State: Close all open BIOVIA Discovery Studio instances before launching (the script initializes its own session).
* Hands-off Execution: The script captures mouse and keyboard control. Do not interact with the system while running.
* Fail-Safe: Move the mouse cursor rapidly to the absolute top-left corner of your screen to trigger pyautogui.FAILSAFE and abort the process.
* DPI/Scaling Sensitivity: If OS resolution, display scale (e.g., 125%), or theme changes, re-crop the reference UI images.

**Usage**
python3 Discovery_Oto.py

---

## Türkçe

Moleküler docking (kenetlenme) sonrası veri işleme, görselleştirme, kompleks hazırlama ve 2D etkileşim haritalaması için geliştirilmiş Python betikleri.

### Betik Özeti

* **pymol_render_script.py**: PyMOL kullanarak docking pozlarını toplu ve yüksek kaliteli (ray-traced) olarak görselleştirir.
* **Complex_Merger_pdbqt_and_cleanprotein.py**: .pdbqt docking çıktılarını hedef .pdb proteini ile birleştirerek tek bir kompleks .pdb dosyasına dönüştürür.
* **Discovery_Oto.py**: pyautogui ile BIOVIA Discovery Studio arayüzünü kontrol ederek 2D etkileşim diyagramlarını otomatik oluşturur.

---

### 1. pymol_render_script.py

**Ne İşe Yarar?**

* 5 tekrarlı docking sonuçlarını (*_1_best.pdbqt ... *_5_best.pdbqt) hedef protein üzerine aktarır.
* Proteini yarı saydam yüzey + tel kafes (wireframe), ligandları ise farklı renklerde çubuk (sticks) olarak yapılandırır.
* Belirlenen iki kamera açısından (genel ve odak/yakın) 1920x1080, 600 DPI çözünürlükte render alır.

**Gereksinimler ve Dosya Düzeni**

* Betik, hedef protein ve ligandlar aynı çalışma dizininde bulunmalıdır.
* Hedef protein: protein_clean.pdb
* Ligand isimlendirmesi: <molekul_adi>_1_best.pdbqt ... <molekul_adi>_5_best.pdbqt
* Kamera Ayarları: PyMOL GUI'de proteini istenen açılara getirip konsola get_view yazın. Dönen matris değerlerini betik içerisindeki view_uzak ve view_yakin değişkenlerine aktarın.
* Renk Paleti: Varsayılan renkler oxygen, violet, deepsalmon, hotpink, lightpink olup ligand_colors listesinden özelleştirilebilir.

**Çıktılar**

* Her molekül için 2 adet ray-traced .png oluşturulur:
* <molekul_adi>_uzak.png
* <molekul_adi>_yakin.png



**Çalıştırma**
Terminalden:
python pymol_render_script.py

PyMOL üzerinden:
pymol -c -q pymol_render_script.py

Not: 600 DPI ve ray=1 render işlemi donanım özelliklerine ve molekül yoğunluğuna bağlı olarak zaman alabilir.

---

### 2. Complex_Merger_pdbqt_and_cleanprotein.py

**Ne İşe Yarar?**

* Çalışma dizinindeki .pdbqt docking çıktılarını protein_clean.pdb ile hizalayıp tek bir kompleks .pdb formatında birleştirir.
* Aynı molekülün tekrarlarını (zinc001_1, zinc001_2 vb.) otomatik olarak tek bir klasörde toplar.

**Gereksinimler**

* Python 3.x
* Sisteminizde kurulu PyMOL (Betik içindeki PyMOL yolunu kendi ortamınıza göre güncelleyin).

**Girdi / Çıktı Düzeni**

* Girdi: protein_clean.pdb ve aynı dizindeki *.pdbqt dosyaları.
* Çıktı: Interaction_Maps/ hiyerarşisinde oluşturulur:
* Interaction_Maps/<molekul_adi>*complex_interaction/protein*<molekul_adi>_1_complex.pdb
* Interaction_Maps/<molekul_adi>*complex_interaction/protein*<molekul_adi>_2_complex.pdb



**Çalıştırma**
python Complex_Merger_pdbqt_and_cleanprotein.py

---

### 3. Discovery_Oto.py

**Ne İşe Yarar?**

* BIOVIA Discovery Studio GUI'sini bilgisayarlı görü ve arayüz otomasyonu (pyautogui) ile kontrol eder.
* Reseptör/ligand tanımlama, 2B diyagram oluşturma ve dışa aktarma adımlarını otomatik yürütür.

**Bağımlılıklar**
pip install pyautogui pyperclip opencv-python

* Discovery Studio Yolu: Betik içerisindeki uygulama yolu çalıştırılacak sistemdeki BIOVIA dizinine göre düzenlenmelidir.

**Dosya ve Arayüz Şablonları**

* Referans Görseller: Aşağıdaki buton/arayüz kırpmaları betik ile aynı klasörde olmalıdır:
* interactions_tab.png
* define_receptor_anchor.png
* ligand_icon.png
* define_receptor_btn.png
* define_ligand_btn.png
* show_2d_btn.png


* Girdi Klasör Yapısı: Interaction_Maps/<molekul_adi>*complex_interaction/protein*<ligand_adi>_complex.pdb
* Çıktı: Interaction_Maps/<molekul_adi>_complex_interaction/<ligand_adi>_interaction_map.png

**Dikkat Edilmesi Gerekenler**

* Temiz Başlangıç: Açık olan tüm Discovery Studio oturumlarını kapatın (betik yeni bir oturum başlatır).
* Müdahale Etmeyin: Betik çalışırken fare ve klavye girişleri simüle edilir; bilgisayara dokunulmamalıdır.
* Acil Durum (Fail-Safe): İşlemi acil durdurmak için fare imlecini hızlıca ekranın en sol üst köşesine çekin (pyautogui.FAILSAFE).
* Ölçeklendirme Hassasiyeti: Ekran çözünürlüğü veya işletim sistemi ölçeklendirmesi (%125 vb.) değişirse referans görsellerin yeniden kırpılması gerekir.

**Çalıştırma**
python3 Discovery_Oto.py
