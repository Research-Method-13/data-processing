# Laporan Preprocessing Data (`preprocess.py`)

## Deskripsi dan Detail Pengerjaan
Skrip `preprocess.py` dirancang untuk melakukan pra-pemrosesan (preprocessing) pada raw data log perilaku dan sensor dari 20 partisipan penelitian. Langkah-langkah detail yang dilakukan dalam skrip ini meliputi:

1. **Iterasi & Validasi Direktori:** Skrip membaca direktori `P-001` hingga `P-020` secara otomatis dan mengecek ketersediaan file `TouchLog` maupun `SensorLog` untuk kondisi 'Mindful' dan 'Mindless'.
2. **Penyaringan Aplikasi Target:** Pada data *TouchLog*, difilter hanya aktivitas yang berasal dari aplikasi target, yaitu `com.ss.android.ugc.trill` (TikTok).
3. **Ekstraksi Fitur TouchLog:**
   - Melakukan standarisasi format `Timestamp` menjadi numerik.
   - Mengurutkan baris data berdasarkan waktu.
   - Menghitung `Time_Delta_Sec` (selisih waktu antar baris).
   - Menghitung `Swipe_Distance` berdasarkan *ScrollDeltaX* dan *ScrollDeltaY*.
   - Mengekstraksi fitur utama `Scroll_Velocity` (Kecepatan Scroll) dengan membagi _Distance_ dengan _Time_Delta_Sec_.
4. **Ekstraksi Fitur SensorLog:**
   - Melakukan filter timestamps dengan batas awalan/akhiran data sentuhan (`min_timestamp` - `max_timestamp`).
   - Menghitung `Magnitude` dari akselerometer (berdasarkan sumbu X, Y, Z).
   - Menghitung sudut rotasi orientasi perangkat yaitu `Pitch` dan `Roll`.
5. **Agregasi Data:** Seluruh data *Touch* dan *Sensor* dari 20 partisipan digabungkan (concatenate) menjadi satu, kemudian diekspor menjadi dua file utama: `Master_TouchLog_All.csv` dan `Master_SensorLog_All.csv` di dalam folder `master/`.

## Kesimpulan
File `preprocess.py` berhasil menyelesaikan tantangan raw data yang berserakan dengan melakukan agregasi, ekstraksi fitur esensial (seperti *scroll velocity*, *magnitude*, *pitch*, dan *roll*), serta penyaringan data spesifik aplikasi TikTok. Hasil akhir berupa file Master (*Master_TouchLog_All* dan *Master_SensorLog_All*) memastikan bahwa dataset yang kotor telah seragam, bersih dari *error/missing values* kronis, dan sangat siap untuk dihubungkan (merging) pada proses pemodelan Machine Learning di tahap selanjutnya.
