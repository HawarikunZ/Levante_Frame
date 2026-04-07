import os
import sys
import time
import threading
import re
from datetime import datetime
import getpass

# =============================================================
#  Levante.py — Terminal Color, Style & Indo Syntax Utility
#  Levante Edition v4.0
# =============================================================


# ─────────────────────────────────────────
#  KODE ANSI DASAR
# ─────────────────────────────────────────

RESET   = "\033[0m"
BOLD    = "\033[1m"
ITALIC  = "\033[3m"
UNDER   = "\033[4m"


# ─────────────────────────────────────────
#  PRESET WARNA ANSI STANDAR (16 warna)
# ─────────────────────────────────────────

MERAH   = "\033[31m"
HIJAU   = "\033[32m"
KUNING  = "\033[33m"
BIRU    = "\033[34m"
MAGENTA = "\033[35m"
CYAN    = "\033[36m"
PUTIH   = "\033[37m"


# ─────────────────────────────────────────
#  PRESET WARNA 256
# ─────────────────────────────────────────

GOLD       = "\033[38;5;220m"
ORANGE     = "\033[38;5;208m"
PINK_NEON  = "\033[38;5;198m"
UNGU_SOFT  = "\033[38;5;141m"
BIRU_LAUT  = "\033[38;5;39m"
HIJAU_MINT = "\033[38;5;121m"
ABU_TUA    = "\033[38;5;240m"


# ─────────────────────────────────────────
#  PRESET WARNA HEX (untuk referensi)
# ─────────────────────────────────────────

LIME        = "#32cd32"
SKY_BLUE    = "#87ceeb"
VIOLET      = "#ee82ee"
GOLDEN      = "#ffd700"
CORAL       = "#ff7f50"
DARK_MODE   = "#282a36"
CYBER_PINK  = "#ff00ff"
DEEP_BLUE   = "#00008b"
MINT_GREEN  = "#98ff98"
SOFT_PURPLE = "#b39ddb"
TOMATO_RED  = "#ff6347"


# ─────────────────────────────────────────
#  TEMA GLOBAL
# ─────────────────────────────────────────

class Tema:
    """
    Palet warna global yang dipakai oleh seluruh fungsi UI.
    Ubah via Atur_Tema() agar perubahan berlaku ke semua komponen.

    Contoh:
        Atur_Tema(utama=CYAN, aksen=GOLD)
        Atur_Tema(utama="#6272a4", sukses=HIJAU_MINT, error=TOMATO_RED)
    """
    UTAMA  = SKY_BLUE
    AKSEN  = GOLDEN
    SUKSES = "#2ecc71"
    ERROR  = "#e74c3c"
    INFO   = "#3498db"
    TEKS   = PUTIH

def Atur_Tema(utama=None, aksen=None, sukses=None, error=None, info=None, teks=None):
    """
    Mengubah palet warna seluruh aplikasi secara instan.
    Semua parameter opsional — hanya yang diisi yang berubah.
    Mendukung warna HEX maupun ANSI preset.

    Contoh:
        Atur_Tema(utama=CYAN, aksen=GOLD)
        Atur_Tema(sukses="#00ff88", error=MERAH)
        Atur_Tema(utama="#6272a4", aksen="#ffd700", sukses="#2ecc71")
    """
    if utama:  Tema.UTAMA  = utama
    if aksen:  Tema.AKSEN  = aksen
    if sukses: Tema.SUKSES = sukses
    if error:  Tema.ERROR  = error
    if info:   Tema.INFO   = info
    if teks:   Tema.TEKS   = teks


# ─────────────────────────────────────────
#  HELPER INTERNAL
# ─────────────────────────────────────────

def _hex_to_rgb(hex_code):
    """Mengubah kode HEX (#FFFFFF) menjadi tuple RGB (255, 255, 255)."""
    hex_code = hex_code.lstrip('#')
    return tuple(int(hex_code[i:i+2], 16) for i in (0, 2, 4))

def _warna_ke_ansi(warna):
    """Mengubah warna (HEX atau ANSI) menjadi kode ANSI foreground siap pakai."""
    if str(warna).startswith('#'):
        r, g, b = _hex_to_rgb(warna)
        return f"\033[38;2;{r};{g};{b}m"
    return warna

def _warna_ke_bg_ansi(warna):
    """
    Mengubah warna (HEX atau ANSI foreground) menjadi kode ANSI background.
    Lebih aman daripada string replace karena menangani semua format.
    """
    if str(warna).startswith('#'):
        r, g, b = _hex_to_rgb(warna)
        return f"\033[48;2;{r};{g};{b}m"
    # Konversi ANSI foreground → background dengan regex
    # Format: \033[38;5;Nm  →  \033[48;5;Nm
    #         \033[38;2;R;G;Bm  →  \033[48;2;R;G;Bm
    #         \033[3Nm  →  \033[4Nm  (standar 16 warna)
    hasil = re.sub(r'\033\[38(;)', r'\033[48\1', warna)
    hasil = re.sub(r'\033\[3([0-7])m', r'\033[4\1m', hasil)
    return hasil

def _get_padding(teks, posisi):
    """Menghitung spasi kiri berdasarkan posisi teks di terminal."""
    try:
        terminal_lebar = os.get_terminal_size().columns
    except OSError:
        terminal_lebar = 80
    panjang = len(teks)
    if posisi == "tengah":
        return " " * max(0, (terminal_lebar - panjang) // 2)
    elif posisi == "kanan":
        return " " * max(0, terminal_lebar - panjang)
    return ""


# ─────────────────────────────────────────
#  FUNGSI WARNA TEKS
# ─────────────────────────────────────────

def rgb(r, g, b, teks):
    """
    Teks dengan warna RGB kustom (True Color).

    Contoh:
        print(rgb(255, 100, 0, "Teks Oranye"))
        print(rgb(0, 200, 255, "Teks Biru Langit"))
    """
    return f"\033[38;2;{r};{g};{b}m{teks}{RESET}"

def hex_text(hex_code, teks):
    """
    Teks dengan warna HEX kustom.

    Contoh:
        print(hex_text("#ff7f50", "Teks Coral"))
        print(hex_text(VIOLET, "Teks Ungu"))
    """
    r, g, b = _hex_to_rgb(hex_code)
    return rgb(r, g, b, teks)

def color256(kode, teks):
    """
    Teks dengan warna 256-color (kode 0–255).

    Contoh:
        print(color256(220, "Teks Gold"))
        print(color256(198, "Teks Pink Neon"))
    """
    return f"\033[38;5;{kode}m{teks}{RESET}"

def text(warna_ansi, teks):
    """
    Teks dengan kode warna ANSI preset langsung.

    Contoh:
        print(text(MERAH, "Teks Merah"))
        print(text(BOLD,  "Teks Tebal"))
        print(text(UNDER, "Teks Garis Bawah"))
    """
    return f"{warna_ansi}{teks}{RESET}"


# ─────────────────────────────────────────
#  FUNGSI WARNA BACKGROUND
# ─────────────────────────────────────────

def bg_rgb(r, g, b, teks):
    """
    Teks dengan background warna RGB.

    Contoh:
        print(bg_rgb(40, 44, 54, "Background Gelap"))
        print(bg_rgb(46, 204, 113, "Background Hijau"))
    """
    return f"\033[48;2;{r};{g};{b}m{teks}{RESET}"

def bg_hex(hex_code, teks):
    """
    Teks dengan background warna HEX.

    Contoh:
        print(bg_hex("#282a36", "Background Dark Mode"))
        print(bg_hex("#ff7f50", "Background Coral"))
    """
    r, g, b = _hex_to_rgb(hex_code)
    return bg_rgb(r, g, b, teks)


# ─────────────────────────────────────────
#  FUNGSI GRADASI WARNA
# ─────────────────────────────────────────

def gradasi_kustom(teks, hex_start, hex_end):
    """
    Gradasi teks dari satu warna HEX ke warna HEX lainnya.

    Contoh:
        print(gradasi_kustom("Halo Dunia!", "#ff0000", "#0000ff"))
        print(gradasi_kustom("Levante", CORAL, VIOLET))
    """
    r1, g1, b1 = _hex_to_rgb(hex_start)
    r2, g2, b2 = _hex_to_rgb(hex_end)
    n = len(teks)
    hasil = ""
    for i, char in enumerate(teks):
        r = int(r1 + (r2 - r1) * (i / n))
        g = int(g1 + (g2 - g1) * (i / n))
        b = int(b1 + (b2 - b1) * (i / n))
        hasil += f"\033[38;2;{r};{g};{b}m{char}"
    return hasil + RESET

def gradasi_sunset(teks):
    """
    Gradasi warna Sunset (merah ke kuning).

    Contoh:
        print(gradasi_sunset("Selamat Sore!"))
        print(gradasi_sunset("Matahari Terbenam"))
    """
    n = len(teks)
    hasil = ""
    for i, char in enumerate(teks):
        r = 255
        g = int(255 * (i / n))
        b = int(255 * (1 - (i / n)))
        hasil += f"\033[38;2;{r};{g};{b}m{char}"
    return hasil + RESET

def gradasi_ocean(teks):
    """
    Gradasi warna laut (biru ke hijau).

    Contoh:
        print(gradasi_ocean("Samudra Luas"))
        print(gradasi_ocean("Biru Kehijauan"))
    """
    n = len(teks)
    hasil = ""
    for i, char in enumerate(teks):
        g = int(255 * (i / n))
        hasil += f"\033[38;2;0;{g};255m{char}"
    return hasil + RESET

def rainbow(teks):
    """
    Teks berwarna pelangi otomatis.

    Contoh:
        print(rainbow("Warna Warni!"))
        print(rainbow("Hello World"))
    """
    colors = ["#ff0000", "#ff7f00", "#ffff00", "#00ff00", "#0000ff", "#4b0082", "#9400d3"]
    return "".join(hex_text(colors[i % len(colors)], char) for i, char in enumerate(teks))


# ─────────────────────────────────────────
#  KOMPONEN UI — menggunakan Tema global
# ─────────────────────────────────────────

def cetak_sukses(pesan):
    """
    Mencetak pesan sukses bergaya (warna dari Tema.SUKSES).

    Contoh:
        cetak_sukses("Data berhasil disimpan!")
        cetak_sukses("Login berhasil.")
    """
    w = _warna_ke_ansi(Tema.SUKSES)
    print(f"{w}{BOLD}SUKSES: {RESET}{w}{pesan}{RESET}")

def cetak_error(pesan):
    """
    Mencetak pesan error bergaya (warna dari Tema.ERROR).

    Contoh:
        cetak_error("File tidak ditemukan!")
        cetak_error("Koneksi gagal.")
    """
    w = _warna_ke_ansi(Tema.ERROR)
    print(f"{w}{BOLD}ERROR: {RESET}{w}{pesan}{RESET}")

def alert(tipe, pesan):
    """
    Komponen alert dengan background berwarna.
    tipe: 'sukses', 'error', atau 'info'.
    Warna background mengikuti Tema.SUKSES / Tema.ERROR / Tema.INFO.

    Contoh:
        print(alert("sukses", "Data berhasil diunggah!"))
        print(alert("error",  "Password salah!"))
        print(alert("info",   "Versi terbaru tersedia."))
    """
    tipe = tipe.lower()
    if tipe == "sukses":
        w = Tema.SUKSES
        return bg_hex(w if w.startswith('#') else "#2ecc71",
                      f" {BOLD}✔ SUCCESS ") + f" {_warna_ke_ansi(w)}{pesan}{RESET}"
    elif tipe == "error":
        w = Tema.ERROR
        return bg_hex(w if w.startswith('#') else "#e74c3c",
                      f" {BOLD}✖ ERROR ") + f" {_warna_ke_ansi(w)}{pesan}{RESET}"
    elif tipe == "info":
        w = Tema.INFO
        return bg_hex(w if w.startswith('#') else "#3498db",
                      f" {BOLD}ℹ INFO ") + f" {_warna_ke_ansi(w)}{pesan}{RESET}"

def header(judul):
    """
    Header sederhana dengan garis pemisah (warna dari Tema.UTAMA).

    Contoh:
        header("Menu Utama")
        header("Hasil Pencarian")
    """
    w = _warna_ke_ansi(Tema.UTAMA)
    print("\n" + "=" * 50)
    print(f"{w}{BOLD}{judul.center(50)}{RESET}")
    print("=" * 50)

def banner(teks, warna=None, lebar=50, posisi="tengah"):
    """
    Banner header dengan background berwarna.
    warna  : HEX atau ANSI preset. Default: Tema.UTAMA.
    lebar  : Jumlah karakter lebar banner (default 50).
    posisi : 'kiri', 'tengah', atau 'kanan'.

    Contoh:
        banner("Selamat Datang!")
        banner("Dashboard",  warna=BIRU,      lebar=60, posisi="kiri")
        banner("PERINGATAN", warna="#e74c3c",  lebar=40)
    """
    warna = warna or Tema.UTAMA
    bg_kode = _warna_ke_bg_ansi(warna)
    fg_kode = "\033[38;5;255m"   # putih terang, kontras di semua background
    spasi   = _get_padding(" " * lebar, posisi)
    print(spasi + f"{bg_kode}{' ' * lebar}{RESET}")
    print(spasi + f"{bg_kode}{BOLD}{fg_kode}{teks.center(lebar)}{RESET}")
    print(spasi + f"{bg_kode}{' ' * lebar}{RESET}")

def tabel(header_list, data_rows, warna=None, posisi="kiri"):
    """
    Mencetak tabel dengan garis ASCII.
    header_list : List judul kolom.
    data_rows   : List of list, isi data tiap baris.
    warna       : Warna garis dan header. Default: Tema.UTAMA.
    posisi      : 'kiri', 'tengah', atau 'kanan'.

    Contoh:
        tabel(
            ["Nama", "Usia", "Kota"],
            [["Budi", 25, "Jakarta"], ["Ani", 30, "Bandung"]]
        )
        tabel(
            ["Produk", "Harga"],
            [["Apel", "Rp5.000"], ["Jeruk", "Rp8.000"]],
            warna="#ffd700", posisi="tengah"
        )
    """
    warna = warna or Tema.UTAMA
    col_widths = [len(str(h)) for h in header_list]
    for row in data_rows:
        for i, cell in enumerate(row):
            col_widths[i] = max(col_widths[i], len(str(cell)))

    separator  = "+" + "+".join("-" * (w + 2) for w in col_widths) + "+"
    format_row = lambda row: "|" + "|".join(
        f" {str(c).ljust(col_widths[i])} " for i, c in enumerate(row)
    ) + "|"

    baris = [separator, format_row(header_list), separator]
    for row in data_rows:
        baris.append(format_row(row))
    baris.append(separator)

    warna_final = _warna_ke_ansi(warna)
    spasi = _get_padding(separator, posisi)
    for line in baris:
        print(f"{spasi}{warna_final}{line}{RESET}")

def Kotak(teks, warna=None, posisi="tengah"):
    """
    Membungkus teks di dalam bingkai garis ganda.
    warna  : HEX atau ANSI. Default: Tema.AKSEN.
    posisi : 'kiri', 'tengah', atau 'kanan'.

    Contoh:
        Kotak("Selamat Datang!")
        Kotak("PERINGATAN", warna=MERAH,     posisi="kiri")
        Kotak("Info",       warna="#ffd700")
    """
    warna = warna or Tema.AKSEN
    lebar_isi  = len(teks)
    garis_atas = "╔" + "═" * (lebar_isi + 2) + "╗"
    isi_kotak  = "║ " + teks + " ║"
    garis_bwh  = "╚" + "═" * (lebar_isi + 2) + "╝"
    warna_final = _warna_ke_ansi(warna)
    for baris in [garis_atas, isi_kotak, garis_bwh]:
        spasi = _get_padding(baris, posisi)
        print(f"{spasi}{warna_final}{baris}{RESET}")

def Kotak_Pro(teks, warna=None, posisi="tengah"):
    """
    Kotak garis ganda dengan efek bayangan.
    warna  : HEX atau ANSI. Default: Tema.AKSEN.
    posisi : 'kiri', 'tengah', atau 'kanan'.

    Contoh:
        Kotak_Pro("Selamat Datang!")
        Kotak_Pro("Dashboard", warna=CYAN,      posisi="kiri")
        Kotak_Pro("Peringatan", warna="#e74c3c")
    """
    warna   = warna or Tema.AKSEN
    lebar   = len(teks) + 2
    warna_f = _warna_ke_ansi(warna)
    spasi   = _get_padding(" " * (lebar + 2), posisi)
    print(f"{spasi}{warna_f}╔{'═' * lebar}╗{RESET}")
    print(f"{spasi}{warna_f}║ {teks} ║{RESET}{ABU_TUA}█{RESET}")
    print(f"{spasi}{warna_f}╚{'═' * lebar}╝{RESET}{ABU_TUA}█{RESET}")
    print(f"{spasi} {ABU_TUA} {'▀' * (lebar + 1)}{RESET}")

def clear():
    """
    Membersihkan terminal.

    Contoh:
        clear()
        input("Tekan Enter..."); clear()
    """
    os.system('cls' if os.name == 'nt' else 'clear')

def Loading(simbol="█", maksimal=20, jeda=0.05):
    """
    Animasi loading bar sederhana (blocking).
    simbol  : Karakter pengisi bar (default '█').
    maksimal: Jumlah langkah (default 20).
    jeda    : Waktu tiap langkah dalam detik (default 0.05).

    Contoh:
        Loading()
        Loading(simbol="▓", maksimal=30, jeda=0.03)
        Loading(simbol="=", maksimal=10, jeda=0.1)
    """
    w = _warna_ke_ansi(Tema.UTAMA)
    sys.stdout.write(f"{w}Memproses [{' ' * maksimal}] 0%{RESET}")
    sys.stdout.flush()
    for i in range(1, maksimal + 1):
        filled = simbol * i
        persen = int((i / maksimal) * 100)
        sys.stdout.write(f"\r{w}Memproses [{filled:<{maksimal}}] {persen}%{RESET}")
        sys.stdout.flush()
        time.sleep(jeda)
    ws = _warna_ke_ansi(Tema.SUKSES)
    print(f"  {ws}{BOLD}[SELESAI]{RESET}")


# ─────────────────────────────────────────
#  PROGRESS BAR REALTIME
# ─────────────────────────────────────────

class _ProgressBar:
    def __init__(self, total, lebar, label, warna, warna_selesai):
        self.total          = total
        self.lebar          = lebar
        self.label          = label
        self.warna          = _warna_ke_ansi(warna)
        self.warna_selesai  = _warna_ke_ansi(warna_selesai)
        self._cetak(0)

    def _cetak(self, nilai):
        persen = min(int((nilai / self.total) * 100), 100)
        filled = int(self.lebar * nilai / self.total)
        bar    = "█" * filled + "░" * (self.lebar - filled)
        w      = self.warna_selesai if persen == 100 else self.warna
        status = f"{BOLD}{self.warna_selesai}SELESAI{RESET}" if persen == 100 else f"{persen}%"
        sys.stdout.write(f"\r  {w}{BOLD}{self.label}{RESET} {w}[{bar}]{RESET} {status}  ")
        sys.stdout.flush()

    def update(self, nilai):
        """Update nilai progres saat ini."""
        self._cetak(nilai)

    def selesai(self):
        """Tandai selesai dan pindah ke baris baru."""
        self._cetak(self.total)
        print()

def progress_bar(total=100, lebar=30, label="Progres", warna=None, warna_selesai=None):
    """
    Membuat progress bar realtime yang diupdate manual via .update(nilai).

    total        : Nilai maksimal (default 100).
    lebar        : Lebar bar dalam karakter (default 30).
    label        : Teks label di kiri bar.
    warna        : Warna saat berjalan. Default: Tema.UTAMA.
    warna_selesai: Warna saat 100%. Default: Tema.SUKSES.

    Contoh:
        pb = progress_bar(total=50, label="Download")
        for i in range(50):
            time.sleep(0.05)
            pb.update(i + 1)
        pb.selesai()

        pb = progress_bar(total=100, label="Upload", warna=GOLD, lebar=40)
        for i in range(100):
            pb.update(i + 1)
        pb.selesai()
    """
    warna         = warna         or Tema.UTAMA
    warna_selesai = warna_selesai or Tema.SUKSES
    return _ProgressBar(total, lebar, label, warna, warna_selesai)

def bar_statis(tugas, total, lebar=30, warna=None, posisi="kiri"):
    """
    Mencetak progress bar statis [████░░░] 50% — cocok dipakai di dalam loop.
    Berbeda dari progress_bar() yang realtime dan bisa di-update.

    tugas  : Nilai saat ini.
    total  : Nilai maksimal.
    lebar  : Lebar bar dalam karakter (default 30).
    warna  : Warna bar. Default: Tema.SUKSES.
    posisi : 'kiri', 'tengah', atau 'kanan'.

    Contoh:
        for i in range(1, 6):
            bar_statis(i, 5)
            time.sleep(0.3)

        bar_statis(7, 10, lebar=20, warna=GOLD, posisi="tengah")
    """
    warna   = warna or Tema.SUKSES
    persen  = int((tugas / total) * 100)
    isi     = int(lebar * tugas // total)
    bar     = "█" * isi + "░" * (lebar - isi)
    teks_bar = f"|{bar}| {persen}%"
    Katakan(teks_bar, warna, posisi=posisi)


# ─────────────────────────────────────────
#  SPINNER
# ─────────────────────────────────────────

_spinner_aktif = {}

def spinner(pesan="Memuat", warna=None, kecepatan=0.1):
    """
    Animasi spinner yang berjalan di background (non-blocking).
    Hentikan dengan spinner_stop(thread).

    pesan    : Teks di samping kanan spinner.
    warna    : Warna spinner. Default: Tema.UTAMA.
    kecepatan: Kecepatan putaran dalam detik.

    Contoh:
        t = spinner("Mengambil data...")
        time.sleep(3)
        spinner_stop(t, sukses=True, pesan_akhir="Selesai!")

        t = spinner("Menghubungkan", warna=GOLD, kecepatan=0.08)
        time.sleep(2)
        spinner_stop(t, sukses=False, pesan_akhir="Gagal terhubung.")
    """
    warna       = warna or Tema.UTAMA
    frame       = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
    warna_final = _warna_ke_ansi(warna)

    def jalankan():
        id_sp = threading.get_ident()
        _spinner_aktif[id_sp] = True
        i = 0
        while _spinner_aktif.get(id_sp):
            sys.stdout.write(f"\r  {warna_final}{frame[i % len(frame)]}  {pesan}...{RESET}")
            sys.stdout.flush()
            time.sleep(kecepatan)
            i += 1

    t = threading.Thread(target=jalankan, daemon=True)
    t.start()
    return t

def spinner_stop(thread, sukses=True, pesan_akhir=""):
    """
    Menghentikan spinner dan menampilkan hasil akhir.

    sukses     : True = cetak_sukses, False = cetak_error.
    pesan_akhir: Teks yang ditampilkan (opsional).

    Contoh:
        t = spinner("Memproses")
        time.sleep(2)
        spinner_stop(t, sukses=True,  pesan_akhir="Berhasil!")
        spinner_stop(t, sukses=False, pesan_akhir="Gagal.")
        spinner_stop(t)  # berhenti tanpa pesan
    """
    _spinner_aktif[thread.ident] = False
    thread.join(timeout=1)
    try:
        lebar = os.get_terminal_size().columns
    except OSError:
        lebar = 80
    sys.stdout.write(f"\r{' ' * lebar}\r")
    sys.stdout.flush()
    if pesan_akhir:
        if sukses:
            cetak_sukses(pesan_akhir)
        else:
            cetak_error(pesan_akhir)


# ─────────────────────────────────────────
#  ANIMASI BERKELANJUTAN (THREADING)
# ─────────────────────────────────────────

_animasi_aktif = {}

def anim(tipe, teks, warna=None, posisi="kiri", kecepatan=0.2):
    """
    Animasi teks berkelanjutan di background (non-blocking).
    Hentikan dengan anim_stop(thread).

    tipe:
        1 = Marquee (teks berjalan dari kiri ke kanan)
        2 = Blink   (teks berkedip)
        3 = Shake   (teks goyang kiri-kanan)
    warna: Default Tema.UTAMA.

    Contoh:
        t = anim(1, "Selamat datang!", warna=CYAN)
        time.sleep(4); anim_stop(t)

        t = anim(2, "⚠ PERHATIAN ⚠", warna=MERAH, posisi="tengah")
        time.sleep(3); anim_stop(t)

        t = anim(3, "ERROR!", warna="#e74c3c")
        time.sleep(2); anim_stop(t)
    """
    warna       = warna or Tema.UTAMA
    warna_final = _warna_ke_ansi(warna)

    def jalankan():
        id_anim = threading.get_ident()
        _animasi_aktif[id_anim] = True

        while _animasi_aktif.get(id_anim):
            try:
                terminal_lebar = os.get_terminal_size().columns
            except OSError:
                terminal_lebar = 80

            if tipe == 1:   # Marquee
                for i in range(terminal_lebar - len(teks)):
                    if not _animasi_aktif.get(id_anim): break
                    sys.stdout.write(f"\r{' ' * i}{warna_final}{teks}{RESET}")
                    sys.stdout.flush()
                    time.sleep(kecepatan)
                sys.stdout.write(f"\r{' ' * terminal_lebar}\r")

            elif tipe == 2: # Blink
                spasi = _get_padding(teks, posisi)
                sys.stdout.write(f"\r{spasi}{warna_final}{teks}{RESET}")
                sys.stdout.flush()
                time.sleep(kecepatan * 2)
                sys.stdout.write(f"\r{spasi}{' ' * len(teks)}\r")
                sys.stdout.flush()
                time.sleep(kecepatan * 2)

            elif tipe == 3: # Shake
                spasi_base = _get_padding(teks, posisi)
                for offset in [spasi_base + " ", spasi_base, spasi_base + "  "]:
                    if not _animasi_aktif.get(id_anim): break
                    sys.stdout.write(f"\r{offset}{warna_final}{teks}{RESET}")
                    sys.stdout.flush()
                    time.sleep(kecepatan)

    thread = threading.Thread(target=jalankan, daemon=True)
    thread.start()
    return thread

def anim_stop(thread):
    """
    Menghentikan animasi dan membersihkan baris terminal.

    Contoh:
        t = anim(2, "Loading...", warna=CYAN)
        time.sleep(3)
        anim_stop(t)
        Katakan("Selesai!", HIJAU)
    """
    _animasi_aktif[thread.ident] = False
    thread.join(timeout=1)
    try:
        terminal_lebar = os.get_terminal_size().columns
    except OSError:
        terminal_lebar = 80
    sys.stdout.write(f"\r{' ' * terminal_lebar}\r")
    sys.stdout.flush()


# ─────────────────────────────────────────
#  LOG & CATAT
# ─────────────────────────────────────────

def Catat(pesan, tipe="info", posisi="kiri", simpan=False, file="levante.log"):
    """
    Mencetak log aktivitas dengan timestamp real-time ke terminal.
    Opsional: simpan ke file log dengan simpan=True.

    tipe   : 'info', 'sukses', 'error', atau 'warning'.
    posisi : Posisi teks di terminal.
    simpan : True = tulis juga ke file log (default False).
    file   : Nama file log jika simpan=True (default 'levante.log').

    Contoh:
        Catat("Aplikasi dimulai")
        Catat("Login berhasil",   tipe="sukses")
        Catat("Koneksi gagal",    tipe="error")
        Catat("Disk hampir penuh", tipe="warning")
        Catat("Data disimpan",    tipe="sukses", simpan=True)
        Catat("Crash terjadi",    tipe="error",  simpan=True, file="error.log")
    """
    waktu = datetime.now().strftime("%H:%M:%S")

    warna_map = {
        "info":    Tema.INFO,
        "sukses":  Tema.SUKSES,
        "error":   Tema.ERROR,
        "warning": KUNING,
    }
    ikon_map = {
        "info":    "ℹ",
        "sukses":  "✔",
        "error":   "✖",
        "warning": "⚠",
    }

    warna_final = warna_map.get(tipe.lower(), Tema.TEKS)
    ikon        = ikon_map.get(tipe.lower(), "•")
    teks_full   = f"[{waktu}] {ikon} {pesan}"

    Katakan(teks_full, warna_final, posisi=posisi)

    if simpan:
        label = tipe.upper().ljust(7)
        waktu_full = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(file, "a", encoding="utf-8") as f:
            f.write(f"[{waktu_full}] [{label}] {pesan}\n")


# ─────────────────────────────────────────
#  SYNTAX HIGHLIGHTING
# ─────────────────────────────────────────

def cetak_kode(kode, bahasa="python"):
    """
    Syntax highlighting untuk menampilkan potongan kode di terminal.
    Mendukung Python, HTML, dan JSON.
    Menggunakan single-pass tokenizer agar kode ANSI tidak ikut di-highlight.

    bahasa: 'python', 'html', atau 'json'.

    Contoh:
        cetak_kode(kode_python_string)
        cetak_kode(kode_html_string,  bahasa='html')
        cetak_kode(kode_json_string,  bahasa='json')
    """
    TOKEN = {
        "python": [
            ("COMMENT", r'#[^\n]*'),
            ("STRING",  r'"""[\s\S]*?"""|' + r"'''[\s\S]*?'''|" + r'"[^"]*"|' + r"'[^']*'"),
            ("KEYWORD", r'\b(def|class|return|import|from|if|elif|else|for|while|in|not|and|or|True|False|None|try|except|with|as|pass|break|continue|lambda|yield)\b'),
            ("NUMBER",  r'\b\d+\.?\d*\b'),
            ("OTHER",   r'.'),
        ],
        "html": [
            ("COMMENT", r'<!--.*?-->'),
            ("TAG",     r'<[^>]+>'),
            ("STRING",  r'"[^"]*"'),
            ("OTHER",   r'.'),
        ],
        "json": [
            ("KEY",     r'"[^"]*"(?=\s*:)'),
            ("STRING",  r':\s*"[^"]*"'),
            ("KEYWORD", r'\b(true|false|null)\b'),
            ("NUMBER",  r'\b\d+\.?\d*\b'),
            ("OTHER",   r'.'),
        ],
    }

    WARNA_TOKEN = {
        "python": {"COMMENT": ABU_TUA,    "STRING":  GOLD,      "KEYWORD": MAGENTA, "NUMBER": CYAN},
        "html":   {"COMMENT": ABU_TUA,    "TAG":     BIRU,      "STRING":  GOLD},
        "json":   {"KEY":     CYAN,       "STRING":  GOLD,      "KEYWORD": MAGENTA, "NUMBER": HIJAU_MINT},
    }

    def _highlight(baris, token_list, warna_map):
        combined = "|".join(f"(?P<T{i}_{name}>{pat})"
                            for i, (name, pat) in enumerate(token_list))
        hasil = ""
        for m in re.finditer(combined, baris, re.DOTALL):
            tipe  = m.lastgroup.split("_", 1)[1]
            val   = m.group()
            warna = warna_map.get(tipe, "")
            hasil += f"{warna}{val}{RESET}" if warna else val
        return hasil

    bahasa_lower = bahasa.lower()
    token_list   = TOKEN.get(bahasa_lower, TOKEN["python"])
    warna_map    = WARNA_TOKEN.get(bahasa_lower, WARNA_TOKEN["python"])

    garis_atas = "┌" + "─" * 50 + "┐"
    garis_bwh  = "└" + "─" * 50 + "┘"
    label      = f" {bahasa.upper()} "
    border     = f"\033[38;5;240m│\033[0m"

    print(f"  \033[38;5;240m{garis_atas}\033[0m")
    print(f"  {border} {bg_hex('#44475a', text(PUTIH, label))}")
    print(f"  {border}")

    for nomor, baris in enumerate(kode.strip().split("\n"), 1):
        no_baris = f"\033[38;5;240m{nomor:>3} \033[0m"
        print(f"  {border} {no_baris}{_highlight(baris, token_list, warna_map)}")

    print(f"  \033[38;5;240m{garis_bwh}\033[0m\n")


# ─────────────────────────────────────────
#  INSPECT (DEBUG)
# ─────────────────────────────────────────

def inspect(variabel, nama="variabel"):
    """
    Pretty-print isi variabel dengan warna dan info tipe data.
    Berguna untuk debugging.

    Contoh:
        inspect({"nama": "Budi", "usia": 25}, "user")
        inspect([1, 2, 3], "angka")
        inspect("Hello", "pesan")
        inspect(3.14,    "pi")
    """
    tipe = type(variabel).__name__
    print(f"\n  {bg_hex('#1e1e2e', f'  inspect → {nama}  ')}")
    print(f"  {ABU_TUA}Tipe  : {RESET}{text(CYAN, tipe)}")

    if isinstance(variabel, dict):
        print(f"  {ABU_TUA}Isi   :{RESET}")
        for k, v in variabel.items():
            print(f"    {text(GOLD, str(k))}{ABU_TUA} : {RESET}{text(HIJAU_MINT, repr(v))}")
    elif isinstance(variabel, (list, tuple, set)):
        print(f"  {ABU_TUA}Panjang: {RESET}{text(CYAN, str(len(variabel)))}")
        print(f"  {ABU_TUA}Isi   :{RESET}")
        for i, v in enumerate(variabel):
            print(f"    {text(GOLD, f'[{i}]')}{ABU_TUA} : {RESET}{text(HIJAU_MINT, repr(v))}")
    else:
        print(f"  {ABU_TUA}Nilai : {RESET}{text(HIJAU_MINT, repr(variabel))}")

    print(f"  {ABU_TUA}{'─' * 36}{RESET}\n")


# ─────────────────────────────────────────
#  SINTAKS INDONESIA
# ─────────────────────────────────────────

# Alias perintah dasar
Tanya     = input
Bersihkan = clear
Tunggu    = time.sleep
Selesai   = sys.exit


class _LevanteOutput:
    """
    Engine output Levante — cetak instan dan animasi mengetik,
    dengan dukungan warna (HEX/ANSI) dan posisi (kiri/tengah/kanan).
    """
    def __call__(self, teks, warna=None, posisi="kiri"):
        """
        Cetak teks instan dengan warna dan posisi.

        Contoh:
            Katakan("Halo!")
            Katakan("Selamat datang!", CYAN)
            Katakan("Peringatan!", "#e74c3c", posisi="tengah")
        """
        warna = warna or Tema.TEKS
        spasi = _get_padding(teks, posisi)
        warna_final = _warna_ke_ansi(warna)
        print(f"{spasi}{warna_final}{teks}{RESET}")

    def ani(self, teks, warna=None, posisi="kiri", kecepatan=0.05):
        """
        Animasi mengetik (typewriter effect).

        Contoh:
            Katakan.ani("Halo, selamat datang!")
            Katakan.ani("Memuat data...", CYAN,     kecepatan=0.03)
            Katakan.ani("PERINGATAN!",   "#e74c3c", posisi="tengah")
        """
        warna = warna or Tema.TEKS
        spasi = _get_padding(teks, posisi)
        warna_final = _warna_ke_ansi(warna)
        sys.stdout.write(spasi)
        for char in teks:
            sys.stdout.write(f"{warna_final}{char}{RESET}")
            sys.stdout.flush()
            time.sleep(kecepatan)
        print()


Cetak   = _LevanteOutput()
Katakan = Cetak


def Tanya_User(pertanyaan, warna=None):
    """
    Input dengan warna dan simbol panah. Mendukung HEX dan ANSI.

    Contoh:
        nama = Tanya_User("Siapa namamu?")
        usia = Tanya_User("Berapa usiamu?", KUNING)
        kota = Tanya_User("Kota asalmu?",  "#ff7f50")
    """
    warna = warna or Tema.AKSEN
    warna_final = _warna_ke_ansi(warna)
    return input(f"{warna_final}{pertanyaan} ➜ {RESET}")

def Rahasia(pertanyaan, warna=None):
    """
    Input password dengan sensor tanda bintang (*).
    Mendukung Windows dan Linux/Unix.
    """
    warna = warna or Tema.ERROR
    warna_final = _warna_ke_ansi(warna)
    sys.stdout.write(f"{warna_final}{pertanyaan} ➜ {RESET}")
    sys.stdout.flush()

    password = ""
    
    # Deteksi Sistem Operasi
    if os.name == 'nt':  # Windows
        import msvcrt
        while True:
            char = msvcrt.getch()
            if char in [b'\r', b'\n']:
                sys.stdout.write('\n')
                break
            elif char == b'\x08':
                if len(password) > 0:
                    password = password[:-1]
                    sys.stdout.write('\b \b')
            else:
                password += char.decode('utf-8')
                sys.stdout.write('*')
            sys.stdout.flush()
    else:
        import tty, termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            while True:
                char = sys.stdin.read(1)
                if char in ['\r', '\n']: # Enter
                    sys.stdout.write('\r\n')
                    break
                elif char in ['\x7f', '\x08']: # Backspace
                    if len(password) > 0:
                        password = password[:-1]
                        sys.stdout.write('\b \b')
                else:
                    password += char
                    sys.stdout.write('*')
                sys.stdout.flush()
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
            
    return password

def Konfirmasi(pertanyaan, warna=None):
    """
    Prompt yes/no — mengembalikan True atau False.
    Menerima: y / ya / yes / 1 → True, selain itu → False.

    Contoh:
        if Konfirmasi("Yakin ingin menghapus?"):
            cetak_sukses("Dihapus.")

        if Konfirmasi("Simpan perubahan?", warna=CYAN):
            Katakan("Tersimpan!", HIJAU)
    """
    warna = warna or Tema.AKSEN
    warna_final = _warna_ke_ansi(warna)
    jawaban = input(
        f"  {warna_final}{BOLD}{pertanyaan}{RESET} {ABU_TUA}[y/n]{RESET} ➜ "
    ).strip().lower()
    return jawaban in ("y", "ya", "yes", "1")

def Ulangi(jumlah, fungsi):
    """
    Pengganti loop 'for i in range(jumlah)'.

    Contoh:
        Ulangi(3, lambda i: print(f"Baris ke-{i}"))
        Ulangi(5, lambda i: Katakan(f"Item {i+1}", CYAN))
    """
    for i in range(jumlah):
        fungsi(i)

def Selama(kondisi_fungsi, aksi_fungsi):
    """
    Pengganti loop 'while kondisi(): aksi()'.

    Contoh:
        n = [3]
        Selama(
            lambda: n[0] > 0,
            lambda: (print(n[0]), n.__setitem__(0, n[0] - 1))
        )
    """
    while kondisi_fungsi():
        aksi_fungsi()

def Jika(kondisi):
    """
    Membantu keterbacaan dalam struktur if.

    Contoh:
        if Jika(nilai >= 75):
            Katakan("Lulus!", HIJAU)
    """
    return kondisi

def Menu(judul, daftar_pilihan, warna=None, posisi="tengah"):
    """
    Menu interaktif bernomor otomatis.
    Mengembalikan tuple (nomor_str, nama_pilihan).

    Contoh:
        pilih, nama = Menu("Main Menu", ["Mulai", "Pengaturan", "Keluar"])
        if pilih == "1": Katakan("Memulai...")

        pilih, nama = Menu("Kategori", ["Elektronik", "Pakaian"],
                           warna=CYAN, posisi="kiri")
    """
    warna = warna or Tema.AKSEN
    banner(judul, warna, lebar=40, posisi=posisi)
    pilihan_map = {}
    for i, opsi in enumerate(daftar_pilihan, 1):
        Katakan(f"  [{i}] {opsi}", warna, posisi=posisi)
        pilihan_map[str(i)] = opsi
    print()
    pilih = Tanya_User("Masukkan Pilihan", warna)
    return pilih, pilihan_map.get(pilih, "Invalid")

def Pilih(daftar_pilihan, judul="Pilih salah satu", warna=None, warna_aktif=None):
    """
    Menu navigasi interaktif menggunakan keyboard panah ↑↓ + Enter.
    Mengembalikan tuple (index, nama_pilihan).
    Hanya berfungsi di Linux/macOS (membutuhkan tty).

    Contoh:
        idx, pilihan = Pilih(["Mulai", "Pengaturan", "Keluar"])
        print(f"Dipilih: {pilihan}")

        idx, pilihan = Pilih(
            ["Merah", "Hijau", "Biru"],
            judul="Pilih warna favoritmu",
            warna_aktif=CORAL
        )
    """
    import tty, termios

    warna      = warna      or Tema.TEKS
    warna_aktif = warna_aktif or Tema.AKSEN

    def _getch():
        fd  = sys.stdin.fileno()
        old = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            ch = sys.stdin.read(1)
            if ch == '\x1b':
                ch += sys.stdin.read(2)
            return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    def _render(aktif):
        sys.stdout.write(f"\033[{len(daftar_pilihan) + 2}A\033[J")
        w_aktif = _warna_ke_ansi(warna_aktif)
        w_biasa = _warna_ke_ansi(warna)
        print(f"  {BOLD}{w_biasa}{judul}{RESET}")
        print()
        for i, opsi in enumerate(daftar_pilihan):
            if i == aktif:
                print(f"  {w_aktif}{BOLD}  ❯  {opsi}{RESET}")
            else:
                print(f"  {w_biasa}     {opsi}{RESET}")

    w_biasa = _warna_ke_ansi(warna)
    print(f"  {BOLD}{w_biasa}{judul}{RESET}")
    print()
    for opsi in daftar_pilihan:
        print(f"  {w_biasa}     {opsi}{RESET}")

    aktif = 0
    _render(aktif)

    while True:
        ch = _getch()
        if ch == '\x1b[A':
            aktif = (aktif - 1) % len(daftar_pilihan)
        elif ch == '\x1b[B':
            aktif = (aktif + 1) % len(daftar_pilihan)
        elif ch in ('\r', '\n'):
            print()
            return aktif, daftar_pilihan[aktif]
        _render(aktif)

def Judul_Halaman(teks, warna=None):
    """
    Shortcut: bersihkan layar lalu tampilkan banner judul.

    Contoh:
        Judul_Halaman("Halaman Utama")
        Judul_Halaman("Dashboard Admin", warna=BIRU)
        Judul_Halaman("Selamat Datang",  warna="#2ecc71")
    """
    Bersihkan()
    banner(teks, warna, lebar=60, posisi="tengah")
    print()
    
def Pilih_Menu(judul, daftar_pilihan, warna=None):
    """
    Menampilkan daftar menu dan meminta input angka.
    """
    warna = warna or Tema.UTAMA
    header(judul)
    for i, opsi in enumerate(daftar_pilihan, 1):
        Katakan(f"  {text(warna, str(i))} ➜ {opsi}")
    
    while True:
        pilih = Tanya_User("Pilih nomor menu")
        if pilih.isdigit() and 1 <= int(pilih) <= len(daftar_pilihan):
            return int(pilih)
        Catat("Pilihan tidak valid!", "error")


# ─────────────────────────────────────────
#  OPERATOR PERBANDINGAN (SINTAKS INDONESIA)
# ─────────────────────────────────────────

def Lebih_Dari(a, b):   return a > b
def Kurang_Dari(a, b):  return a < b
def Sama_Dengan(a, b):  return a == b
def Tidak_Sama(a, b):   return a != b
def Lebih_Sama(a, b):   return a >= b
def Kurang_Sama(a, b):  return a <= b

# Alias singkat
lebih     = Lebih_Dari
kurang    = Kurang_Dari
sama      = Sama_Dengan
tidaksama = Tidak_Sama

import json

# ─────────────────────────────────────────
#  SISTEM DATA (SAVE & LOAD)
# ─────────────────────────────────────────

class _LevanteData:
    """
    Engine untuk menyimpan dan memuat data JSON dengan gaya Levante.
    """
    def __init__(self):
        self._temp_data = None

    def Simpan(self, data):
        """Menyiapkan data yang akan disimpan."""
        self._temp_data = data
        return self

    def Muat(self, nama_file):
        """Memuat data dari file JSON."""
        try:
            with open(nama_file, "r", encoding="utf-8") as f:
                data = json.load(f)
            Catat(f"Data berhasil dimuat dari {nama_file}", "sukses")
            return data
        except FileNotFoundError:
            Catat(f"File {nama_file} tidak ditemukan!", "error")
            return None
        except Exception as e:
            Catat(f"Gagal memuat data: {e}", "error")
            return None

    def file(self, nama_file):
        """Eksekusi penyimpanan ke file spesifik."""
        if self._temp_data is None:
            Catat("Tidak ada data untuk disimpan!", "warning")
            return
        
        try:
            # Pastikan nama file berakhiran .json
            if not nama_file.endswith(".json"):
                nama_file += ".json"
                
            with open(nama_file, "w", encoding="utf-8") as f:
                json.dump(self._temp_data, f, indent=4, ensure_ascii=False)
            
            Catat(f"Data berhasil disimpan ke {nama_file}", "sukses")
            self._temp_data = None # Reset temp
        except Exception as e:
            Catat(f"Gagal menyimpan file: {e}", "error")

# Inisialisasi Objek Global
Data = _LevanteData()
Simpan = Data.Simpan
Muat = Data.Muat