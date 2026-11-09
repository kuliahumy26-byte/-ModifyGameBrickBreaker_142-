Breakout Game

Game brick breaker sederhana menggunakan Python dan Pygame.

adalah paddle yang digerakkan pemain ke kiri/kanan menggunakan tombol panah. Gerakannya dibatasi agar tidak keluar dari layar.
bergerak otomatis dan memantul dari dinding kiri, kanan, dan atas. Jika bola menyentuh bagian bawah layar, nyawa berkurang dan bola direset ke posisi awal.
punya dua jenis — hijau (hancur 1 hit) dan putih (hancur 2 hit). Blok putih yang sudah kena sekali akan berubah warna menjadi abu-abu dan menampilkan retakan sebagai tanda sudah rusak. Setiap blok yang hancur menambah score sebesar 5.
berjalan terus menerus: cek input → gerak paddle → cek tabrakan → update posisi bola → gambar ulang layar. Jika semua blok hancur, blok di-respawn. Jika nyawa habis, game over.
