# Rental Sepeda Dataset

Proyek ini menganalisis data penyewaan sepeda menggunakan dua dataset utama:

- `data/day.csv` — data harian
- `data/hour.csv` — data per jam

Analisis dilakukan di Jupyter Notebook (`notebook.ipynb`) dan disertai dashboard menggunakan Streamlit (`dashboard/dashboard.py`).

## Struktur proyek

- `notebook.ipynb` — Notebook Jupyter (pembersihan, segmentasi, EDA, visualisasi, penyimpanan hasil).
- `data/` — Folder sumber data (`day.csv`, `hour.csv`).
- `dashboard/` — Streamlit app (`dashboard.py`).
- `day_df.csv`, `hour_df.csv`, `day_hour_df.csv` — Output data
- `requirements.txt` — daftar dependensi untuk environment.
- `app-streamlit.py` - digunakan untuk deploy app di streamlit

## Langkah analisis

1. Gathering data: `day.csv` dan `hour.csv` ke pandas DataFrame.
2. Assessing Data: tipe data, missing values, duplikasi.
3. cleaning data: ubah `dteday` ke tipe `datetime`.
4. Segmentasi permintaan harian (`cnt`) menjadi 3 segmen: `low`, `medium`, `high` (berdasarkan kuantil).
5. Membuat tabel 2D rata-rata penggunaan per jam untuk tiap hari untuk heatmap
6. Visualisasi: scatter plot (total, casual, registered) dan heatmap pola jam-hari.
7. Simpan data ke CSV (`day_df.csv`, `hour_df.csv`, `day_hour_df.csv`).

## Instalasi

Direkomendasikan membuat virtual environment venv atau conda, lalu instal dependensi dari `requirements.txt`:

Jika menggunakan conda :

1. conda create -n rental-bike python=3.9 -y
2. conda activate rental-bike
3. pip install -r requirements.txt

## Menjalankan notebook

1. Aktifkan environment seperti di atas.
2. Jalankan JupyterLab / Notebook: jupyter notebook
3. Buka `notebook.ipynb` dan jalankan sel-selnya secara berurutan. Notebook menulis tiga file output: `day_df.csv`, `hour_df.csv`, `day_hour_df.csv`.
4. Pindahkan ke-3 file output ke folder dashboard

## Menjalankan dashboard Streamlit di lokal

Setelah menjalankan notebook

```bash
cd "~/Documents/latihan python/submission-dicoding-analisa-data"
streamlit run dashboard/dashboard.py

```
