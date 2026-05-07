# Laporan Tahap Modeling & EDA (`main.ipynb`)

## Deskripsi dan Detail Pengerjaan
File `main.ipynb` merupakan inti dari proses Eksplorasi Data (EDA) hingga Pemodelan Machine Learning dari data yang sudah disiapkan sebelumnya. Langkah-langkah detail yang dikerjakan meliputi:

1. **Penggabungan Data (Data Merging):**
   - Melakukan pembacaan file master `TouchLog` dan `SensorLog`.
   - Menggunakan fungsi `pd.merge_asof` dari library `pandas` untuk menyatukan data sensor dan sentuhan secara toleransi waktu *(time-series matching)*. Hal ini merekam posisi/sensor fisik HP tepat ketika ketukan layar atau pergeseran *(scroll)* terjadi.

2. **Exploratory Data Analysis (EDA):**
   - Visualisasi distribusi fitur dengan membandingkan perilaku pengguna saat 'Mindful' vs 'Mindless'.
   - Menggunakan grafik boxplot dan violin plot secara logaritmik, memvisualisasikan `Scroll_Velocity`, `Time_Delta_Sec`, dan `Magnitude`.
   - Menemukan perbedaan rentang kecepatan scroll dan jeda interaksi pada target label yang ada.

3. **Strategi Pembagian Data (Train-Test Split) Anti-Leakage:**
   - Memastikan tidak ada *data leakage* (kebocoran data) atau overfit dengan cara mengatur pemisahan data berbasis pengguna menggunakan `GroupShuffleSplit`. 
   - Ini memastikan semua data (Mindful maupun Mindless) dari beberapa partisipan spesifik (contoh: P-001, P-002, dll.) 100% dipisahkan ke dalam set *Testing*. Model mempelajari kebiasaan umum secara logikal dan diuji pada partisipan yang belum pernah dilihat sama sekali (unseen users).

4. **Training Model Klasifikasi:**
   - Menyeragamkan distribusi skala fitur dengan `StandardScaler`.
   - Melatih tiga model Machine Learning: **Random Forest**, **XGBoost**, dan **SVM (RBF)**.
   - Target klasifikasi membedakan kesadaran fokus: `0` (Mindful) dan `1` (Mindless).

5. **Evaluasi dan Interpretasi:**
   - Membandingkan hasil performa melalui nilai `Accuracy` dan `F1-Score` di mana Random Forest menunjukkan nilai akurasi paling baik.

## Kesimpulan
Notebook `main.ipynb` secara sukses merangkum keseluruhan metodologi _Data Science_, dimulai dari integrasi data time-series secara sinkron hingga visualisasi analitik (EDA). Penggunaan _GroupShuffleSplit_ mencegah terjadinya model _overfitting_ akibat mengingat kebiasaan unik satu partisipan, murni memodelkan perilaku _smartphone user_ secara meluas. Dengan hasil ini, Machine Learning (khususnya Random Forest/XGBoost) terbukti mampu mengenali secara otomatis apakah profil mental pengguna sedang `Mindful` atau `Mindless` hanya melalui kecepatan gerak jari (*Scroll Velocity*) serta goyangan HP (*Magnitude/Pitch/Roll*).
