# ============================================
# MODUL JADWAL SISTEM INFORMASI AKADEMIK
# Single File Implementation
# ============================================

from typing import List
from datetime import time

# ==============================
# ENTITY
# ==============================

class Jadwal:
    def __init__(self, kode, mata_kuliah, hari, jam_mulai, jam_selesai, ruangan, dosen, kapasitas):
        self.kode = kode
        self.mata_kuliah = mata_kuliah
        self.hari = hari
        self.jam_mulai = jam_mulai
        self.jam_selesai = jam_selesai
        self.ruangan = ruangan
        self.dosen = dosen
        self.kapasitas = kapasitas

# ==============================
# OBSERVER PATTERN
# ==============================

class Observer:
    def update(self, event, jadwal):
        pass

class StudentObserver(Observer):
    def update(self, event, jadwal):
        print(f"[NOTIF MAHASISWA] {event} - {jadwal.mata_kuliah}")

class LecturerObserver(Observer):
    def update(self, event, jadwal):
        print(f"[NOTIF DOSEN] {event} - {jadwal.mata_kuliah}")

class AdminObserver(Observer):
    def update(self, event, jadwal):
        print(f"[NOTIF ADMIN] {event} - {jadwal.mata_kuliah}")

class ScheduleSubject:
    def __init__(self):
        self.observers: List[Observer] = []

    def attach(self, observer):
        self.observers.append(observer)

    def notify(self, event, jadwal):
        for obs in self.observers:
            obs.update(event, jadwal)

# ==============================
# SERVICE
# ==============================

class ScheduleService:
    def __init__(self):
        self.jadwal_list: List[Jadwal] = []
        self.subject = ScheduleSubject()

    def is_time_overlap(self, j1, j2):
        return j1.jam_mulai < j2.jam_selesai and j2.jam_mulai < j1.jam_selesai

    def detect_conflict(self, new_jadwal):
        for j in self.jadwal_list:
            if j.hari == new_jadwal.hari and self.is_time_overlap(j, new_jadwal):
                if j.ruangan == new_jadwal.ruangan:
                    return "KONFLIK RUANGAN"
                if j.dosen == new_jadwal.dosen:
                    return "KONFLIK DOSEN"
        return None

    def create_jadwal(self, jadwal):
        conflict = self.detect_conflict(jadwal)
        if conflict:
            print(f"[ERROR] {conflict}")
            return

        self.jadwal_list.append(jadwal)
        self.subject.notify("JADWAL DITAMBAHKAN", jadwal)

    def update_jadwal(self, kode, jadwal_baru):
        for i, j in enumerate(self.jadwal_list):
            if j.kode == kode:
                self.jadwal_list.pop(i)
                conflict = self.detect_conflict(jadwal_baru)
                if conflict:
                    print(f"[ERROR] {conflict}")
                    self.jadwal_list.insert(i, j)
                    return

                self.jadwal_list.insert(i, jadwal_baru)
                self.subject.notify("JADWAL DIUBAH", jadwal_baru)
                return

    def delete_jadwal(self, kode):
        for j in self.jadwal_list:
            if j.kode == kode:
                self.jadwal_list.remove(j)
                self.subject.notify("JADWAL DIHAPUS", j)
                return

# ==============================
# DEMO / MAIN PROGRAM
# ==============================

if __name__ == "__main__":
    service = ScheduleService()

    # Register observers
    service.subject.attach(StudentObserver())
    service.subject.attach(LecturerObserver())
    service.subject.attach(AdminObserver())

    jadwal1 = Jadwal(
        kode="J001",
        mata_kuliah="Kalkulus I",
        hari="Senin",
        jam_mulai=time(8, 0),
        jam_selesai=time(10, 0),
        ruangan="A101",
        dosen="Pak Budi",
        kapasitas=40
    )

    jadwal2 = Jadwal(
        kode="J002",
        mata_kuliah="Fisika",
        hari="Senin",
        jam_mulai=time(9, 0),
        jam_selesai=time(11, 0),
        ruangan="A101",
        dosen="Bu Ani",
        kapasitas=35
    )

    print("\n=== TAMBAH JADWAL 1 ===")
    service.create_jadwal(jadwal1)

    print("\n=== TAMBAH JADWAL 2 (BENTROK) ===")
    service.create_jadwal(jadwal2)

    print("\n=== HAPUS JADWAL 1 ===")
    service.delete_jadwal("J001")
