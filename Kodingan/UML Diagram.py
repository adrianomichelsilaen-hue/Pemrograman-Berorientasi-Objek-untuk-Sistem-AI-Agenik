class Kampus:
    """Mewakili kampus tempat Mahasiswa beraktivitas."""
    def __init__(self, status_awal="Belum Lulus"):
        self.status = status_awal
        print(f"Kampus diinisialisasi dengan status: {self.status}")

    def get_status(self):
        return self.status

    def ubah_status(self, aksi):
        if aksi == "Ubah ke Lulus":
            self.status = "Lulus"
            print("Kampus: Status diubah menjadi 'Lulus'.")
        else:
            print(f"Kampus: Aksi '{aksi}' tidak mengubah status.")

class Mahasiswa:
    """Mewakili mahasiswa yang berinteraksi dengan Kampus."""
    def __init__(self, nama, tujuan):
        self.nama = nama
        self.tujuan = tujuan
        print(f"Mahasiswa '{self.nama}' memiliki tujuan: {self.tujuan}")

    def observasi(self, kampus):
        status_kampus = kampus.get_status()
        print(f"{self.nama}: Mengamati status kampus: {status_kampus}")
        return status_kampus

    def berpikir(self, status_kampus):
        if status_kampus != self.tujuan:
            aksi = "Ubah ke Lulus"
            print(f"{self.nama}: Berpikir untuk melakukan aksi '{aksi}'.")
            return aksi
        else:
            aksi = "Tidak melakukan apa-apa"
            print(f"{self.nama}: Tujuan sudah tercapai. Berpikir untuk melakukan aksi '{aksi}'.")
            return aksi

    def bertindak(self, kampus):
        status = self.observasi(kampus)
        aksi_yang_dipilih = self.berpikir(status)
        if aksi_yang_dipilih != "Tidak melakukan apa-apa":
            kampus.ubah_status(aksi_yang_dipilih)
        else:
            print(f"{self.nama}: Tidak ada aksi yang dilakukan.")

# --- Simulasi Sistem ---
kampus_utama = Kampus()
mahasiswa_aktif = Mahasiswa(nama="Budi", tujuan="Lulus")

print("\n--- Semester 1 ---")
mahasiswa_aktif.bertindak(kampus_utama)

print("\n--- Semester 2 ---")
mahasiswa_aktif.bertindak(kampus_utama)
