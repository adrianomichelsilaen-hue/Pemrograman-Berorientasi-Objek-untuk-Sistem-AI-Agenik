"""
Sistem Transkrip Mahasiswa
Aplikasi untuk mengelola dan menampilkan transkrip nilai mahasiswa
"""

import json
from datetime import datetime
from typing import List, Dict, Optional
import statistics


class MataKuliah:
    """Class untuk merepresentasikan Mata Kuliah"""
    
    def __init__(self, kode: str, nama: str, sks: int, semester: int, nilai: str = None):
        self.kode = kode
        self.nama = nama
        self.sks = sks
        self.semester = semester
        self.nilai = nilai
        self.bobot = self._hitung_bobot()
    
    def _hitung_bobot(self) -> float:
        """Menghitung bobot nilai berdasarkan huruf nilai"""
        bobot_map = {
            'A': 4.0,
            'A-': 3.7,
            'B+': 3.3,
            'B': 3.0,
            'B-': 2.7,
            'C+': 2.3,
            'C': 2.0,
            'C-': 1.7,
            'D': 1.0,
            'E': 0.0
        }
        return bobot_map.get(self.nilai, 0.0) if self.nilai else 0.0
    
    def set_nilai(self, nilai: str):
        """Set nilai mata kuliah"""
        self.nilai = nilai
        self.bobot = self._hitung_bobot()
    
    def to_dict(self) -> Dict:
        """Konversi ke dictionary"""
        return {
            'kode': self.kode,
            'nama': self.nama,
            'sks': self.sks,
            'semester': self.semester,
            'nilai': self.nilai,
            'bobot': self.bobot
        }
    
    def __repr__(self):
        return f"{self.kode} - {self.nama} ({self.sks} SKS) - Nilai: {self.nilai}"


class Mahasiswa:
    """Class untuk merepresentasikan Mahasiswa"""
    
    def __init__(self, nim: str, nama: str, program_studi: str, fakultas: str, angkatan: str):
        self.nim = nim
        self.nama = nama
        self.program_studi = program_studi
        self.fakultas = fakultas
        self.angkatan = angkatan
        self.mata_kuliah: List[MataKuliah] = []
        self.status = "Aktif"
    
    def tambah_mata_kuliah(self, mk: MataKuliah):
        """Menambah mata kuliah ke transkrip"""
        self.mata_kuliah.append(mk)
    
    def hapus_mata_kuliah(self, kode: str) -> bool:
        """Menghapus mata kuliah berdasarkan kode"""
        for i, mk in enumerate(self.mata_kuliah):
            if mk.kode == kode:
                self.mata_kuliah.pop(i)
                return True
        return False
    
    def cari_mata_kuliah(self, keyword: str) -> List[MataKuliah]:
        """Mencari mata kuliah berdasarkan kode atau nama"""
        keyword = keyword.lower()
        return [mk for mk in self.mata_kuliah 
                if keyword in mk.kode.lower() or keyword in mk.nama.lower()]
    
    def hitung_ipk(self) -> float:
        """Menghitung IPK (Indeks Prestasi Kumulatif)"""
        if not self.mata_kuliah:
            return 0.0
        
        total_sks = sum(mk.sks for mk in self.mata_kuliah if mk.nilai)
        total_bobot = sum(mk.sks * mk.bobot for mk in self.mata_kuliah if mk.nilai)
        
        return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
    
    def hitung_ips(self, semester: int) -> float:
        """Menghitung IPS (Indeks Prestasi Semester) untuk semester tertentu"""
        mk_semester = [mk for mk in self.mata_kuliah 
                       if mk.semester == semester and mk.nilai]
        
        if not mk_semester:
            return 0.0
        
        total_sks = sum(mk.sks for mk in mk_semester)
        total_bobot = sum(mk.sks * mk.bobot for mk in mk_semester)
        
        return round(total_bobot / total_sks, 2) if total_sks > 0 else 0.0
    
    def get_total_sks(self) -> int:
        """Mendapatkan total SKS yang sudah diambil"""
        return sum(mk.sks for mk in self.mata_kuliah if mk.nilai)
    
    def get_mata_kuliah_by_semester(self, semester: int = None) -> List[MataKuliah]:
        """Mendapatkan mata kuliah berdasarkan semester"""
        if semester is None:
            return self.mata_kuliah
        return [mk for mk in self.mata_kuliah if mk.semester == semester]
    
    def get_statistik(self) -> Dict:
        """Mendapatkan statistik akademik"""
        nilai_list = [mk.bobot for mk in self.mata_kuliah if mk.nilai]
        semester_list = list(set(mk.semester for mk in self.mata_kuliah))
        
        return {
            'ipk': self.hitung_ipk(),
            'total_sks': self.get_total_sks(),
            'total_mk': len([mk for mk in self.mata_kuliah if mk.nilai]),
            'semester_aktif': max(semester_list) if semester_list else 0,
            'nilai_tertinggi': max(nilai_list) if nilai_list else 0.0,
            'nilai_terendah': min(nilai_list) if nilai_list else 0.0,
            'rata_rata': round(statistics.mean(nilai_list), 2) if nilai_list else 0.0
        }
    
    def cetak_transkrip(self):
        """Mencetak transkrip ke console"""
        print("\n" + "="*80)
        print("TRANSKRIP AKADEMIK".center(80))
        print("="*80)
        print(f"\nNIM              : {self.nim}")
        print(f"Nama             : {self.nama}")
        print(f"Program Studi    : {self.program_studi}")
        print(f"Fakultas         : {self.fakultas}")
        print(f"Angkatan         : {self.angkatan}")
        print(f"Status           : {self.status}")
        print("\n" + "-"*80)
        
        # Group by semester
        semester_list = sorted(set(mk.semester for mk in self.mata_kuliah))
        
        for sem in semester_list:
            print(f"\nSEMESTER {sem}")
            print("-"*80)
            print(f"{'Kode':<10} {'Mata Kuliah':<40} {'SKS':<5} {'Nilai':<8} {'Bobot':<6}")
            print("-"*80)
            
            mk_semester = self.get_mata_kuliah_by_semester(sem)
            for mk in mk_semester:
                nilai_display = mk.nilai if mk.nilai else "-"
                bobot_display = f"{mk.bobot:.1f}" if mk.nilai else "-"
                print(f"{mk.kode:<10} {mk.nama:<40} {mk.sks:<5} {nilai_display:<8} {bobot_display:<6}")
            
            print("-"*80)
            ips = self.hitung_ips(sem)
            total_sks_sem = sum(mk.sks for mk in mk_semester if mk.nilai)
            print(f"IPS Semester {sem}: {ips} | Total SKS: {total_sks_sem}")
        
        print("\n" + "="*80)
        print("RINGKASAN")
        print("="*80)
        stats = self.get_statistik()
        print(f"IPK                 : {stats['ipk']}")
        print(f"Total SKS Lulus     : {stats['total_sks']}")
        print(f"Total Mata Kuliah   : {stats['total_mk']}")
        print(f"Semester Aktif      : {stats['semester_aktif']}")
        print("="*80)
        print(f"Dicetak pada: {datetime.now().strftime('%d %B %Y, %H:%M:%S')}")
        print("="*80 + "\n")
    
    def export_to_json(self, filename: str):
        """Export transkrip ke file JSON"""
        data = {
            'mahasiswa': {
                'nim': self.nim,
                'nama': self.nama,
                'program_studi': self.program_studi,
                'fakultas': self.fakultas,
                'angkatan': self.angkatan,
                'status': self.status
            },
            'statistik': self.get_statistik(),
            'mata_kuliah': [mk.to_dict() for mk in self.mata_kuliah],
            'exported_at': datetime.now().isoformat()
        }
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        
        print(f"Transkrip berhasil di-export ke {filename}")
    
    def to_dict(self) -> Dict:
        """Konversi mahasiswa ke dictionary"""
        return {
            'nim': self.nim,
            'nama': self.nama,
            'program_studi': self.program_studi,
            'fakultas': self.fakultas,
            'angkatan': self.angkatan,
            'status': self.status,
            'mata_kuliah': [mk.to_dict() for mk in self.mata_kuliah]
        }


class SistemTranskrip:
    """Class untuk mengelola sistem transkrip"""
    
    def __init__(self):
        self.mahasiswa_list: List[Mahasiswa] = []
    
    def tambah_mahasiswa(self, mahasiswa: Mahasiswa):
        """Menambah mahasiswa ke sistem"""
        self.mahasiswa_list.append(mahasiswa)
    
    def cari_mahasiswa(self, nim: str) -> Optional[Mahasiswa]:
        """Mencari mahasiswa berdasarkan NIM"""
        for mhs in self.mahasiswa_list:
            if mhs.nim == nim:
                return mhs
        return None
    
    def hapus_mahasiswa(self, nim: str) -> bool:
        """Menghapus mahasiswa dari sistem"""
        for i, mhs in enumerate(self.mahasiswa_list):
            if mhs.nim == nim:
                self.mahasiswa_list.pop(i)
                return True
        return False
    
    def cetak_daftar_mahasiswa(self):
        """Mencetak daftar semua mahasiswa"""
        print("\n" + "="*80)
        print("DAFTAR MAHASISWA".center(80))
        print("="*80)
        print(f"{'NIM':<15} {'Nama':<30} {'Program Studi':<20} {'IPK':<6}")
        print("-"*80)
        
        for mhs in self.mahasiswa_list:
            print(f"{mhs.nim:<15} {mhs.nama:<30} {mhs.program_studi:<20} {mhs.hitung_ipk():<6}")
        
        print("="*80 + "\n")


# ==================== DEMO PENGGUNAAN ====================

def demo():
    """Fungsi demo untuk mendemonstrasikan penggunaan sistem"""
    
    # Inisialisasi sistem
    sistem = SistemTranskrip()
    
    # Buat mahasiswa
    mahasiswa1 = Mahasiswa(
        nim="2021110001",
        nama="Budi Santoso",
        program_studi="Teknik Informatika",
        fakultas="Fakultas Teknik",
        angkatan="2021"
    )
    
    # Tambah mata kuliah semester 1
    mk_list_sem1 = [
        MataKuliah("TIF101", "Pemrograman Dasar", 3, 1, "A"),
        MataKuliah("TIF102", "Matematika Diskrit", 3, 1, "A-"),
        MataKuliah("TIF103", "Algoritma dan Struktur Data", 4, 1, "B+"),
        MataKuliah("UNV101", "Bahasa Indonesia", 2, 1, "A"),
        MataKuliah("UNV102", "Pancasila", 2, 1, "A"),
    ]
    
    # Tambah mata kuliah semester 2
    mk_list_sem2 = [
        MataKuliah("TIF201", "Pemrograman Berorientasi Objek", 3, 2, "A"),
        MataKuliah("TIF202", "Basis Data", 3, 2, "A-"),
        MataKuliah("TIF203", "Sistem Operasi", 3, 2, "B+"),
        MataKuliah("MAT201", "Kalkulus II", 3, 2, "B"),
        MataKuliah("UNV201", "Kewarganegaraan", 2, 2, "A"),
    ]
    
    # Tambah mata kuliah semester 3
    mk_list_sem3 = [
        MataKuliah("TIF301", "Jaringan Komputer", 3, 3, "A"),
        MataKuliah("TIF302", "Rekayasa Perangkat Lunak", 3, 3, "A-"),
        MataKuliah("TIF303", "Pemrograman Web", 3, 3, "A"),
        MataKuliah("TIF304", "Interaksi Manusia dan Komputer", 3, 3, "B+"),
        MataKuliah("MAT301", "Statistika", 3, 3, "B+"),
    ]
    
    # Tambahkan semua mata kuliah ke mahasiswa
    for mk in mk_list_sem1 + mk_list_sem2 + mk_list_sem3:
        mahasiswa1.tambah_mata_kuliah(mk)
    
    # Tambah mahasiswa ke sistem
    sistem.tambah_mahasiswa(mahasiswa1)
    
    # Demo fitur-fitur
    print("\n🎓 DEMO SISTEM TRANSKRIP MAHASISWA 🎓\n")
    
    # 1. Cetak transkrip lengkap
    mahasiswa1.cetak_transkrip()
    
    # 2. Cetak statistik
    print("\n📊 STATISTIK DETAIL:")
    print("-" * 50)
    stats = mahasiswa1.get_statistik()
    for key, value in stats.items():
        print(f"{key.replace('_', ' ').title():<20}: {value}")
    
    # 3. Cari mata kuliah
    print("\n\n🔍 PENCARIAN MATA KULIAH:")
    print("-" * 50)
    hasil_cari = mahasiswa1.cari_mata_kuliah("Pemrograman")
    print(f"Hasil pencarian 'Pemrograman': {len(hasil_cari)} mata kuliah")
    for mk in hasil_cari:
        print(f"  - {mk}")
    
    # 4. Hitung IPS per semester
    print("\n\n📈 IPS PER SEMESTER:")
    print("-" * 50)
    for sem in [1, 2, 3]:
        ips = mahasiswa1.hitung_ips(sem)
        print(f"Semester {sem}: {ips}")
    
    # 5. Export ke JSON
    print("\n\n💾 EXPORT DATA:")
    print("-" * 50)
    mahasiswa1.export_to_json("transkrip_mahasiswa.json")
    
    # 6. Cetak daftar mahasiswa dalam sistem
    sistem.cetak_daftar_mahasiswa()


if __name__ == "__main__":
    demo()