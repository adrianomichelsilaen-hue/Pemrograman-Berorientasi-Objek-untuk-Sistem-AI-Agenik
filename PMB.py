 create_engine, Column, Integer, String,
    DateTime, ForeignKey, Enum
)
from sqlalchemy.orm import sessionmaker, declarative_base, relationship, Session
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
import enum

# ======================================================
# DATABASE SETUP
# ======================================================

DATABASE_URL = "sqlite:///./pmb.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# ======================================================
# MODEL
# ======================================================

class StatusEnum(str, enum.Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"

class ProgramStudi(Base):
    __tablename__ = "program_studi"

    id = Column(Integer, primary_key=True)
    kode = Column(String(3), unique=True, nullable=False)
    nama = Column(String, nullable=False)
    fakultas = Column(String, nullable=False)

    mahasiswa = relationship("CalonMahasiswa", back_populates="program_studi")

class CalonMahasiswa(Base):
    __tablename__ = "calon_mahasiswa"

    id = Column(Integer, primary_key=True)
    nama_lengkap = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    phone = Column(String, nullable=False)
    alamat = Column(String)
    status = Column(Enum(StatusEnum), default=StatusEnum.pending)
    nim = Column(String, unique=True, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    approved_at = Column(DateTime, nullable=True)

    program_studi_id = Column(Integer, ForeignKey("program_studi.id"))
    program_studi = relationship("ProgramStudi", back_populates="mahasiswa")

# ======================================================
# SCHEMA
# ======================================================

class PMBRegister(BaseModel):
    nama_lengkap: str
    email: EmailStr
    phone: str = Field(pattern=r"^08\d{8,11}$")
    alamat: str | None = None
    program_studi_id: int

class PMBResponse(BaseModel):
    id: int
    nama_lengkap: str
    email: EmailStr
    status: str
    nim: str | None

    class Config:
        from_attributes = True

# ======================================================
# NIM GENERATOR
# ======================================================

def generate_nim(tahun: int, kode_prodi: str, db: Session) -> str:
    prefix = f"{tahun}{kode_prodi}"

    last = (
        db.query(CalonMahasiswa)
        .filter(CalonMahasiswa.nim.like(f"{prefix}%"))
        .order_by(CalonMahasiswa.nim.desc())
        .first()
    )

    if last and last.nim:
        last_number = int(last.nim[-4:])
        new_number = last_number + 1
    else:
        new_number = 1

    return f"{prefix}{str(new_number).zfill(4)}"

# ======================================================
# FASTAPI APP
# ======================================================

app = FastAPI(title="Modul PMB - Single File")

Base.metadata.create_all(bind=engine)

# ======================================================
# ENDPOINT
# ======================================================

@app.post("/api/pmb/register", response_model=PMBResponse)
def register_pmb(data: PMBRegister, db: Session = Depends(get_db)):
    if db.query(CalonMahasiswa).filter_by(email=data.email).first():
        raise HTTPException(status_code=409, detail="Email already registered")

    mahasiswa = CalonMahasiswa(
        nama_lengkap=data.nama_lengkap,
        email=data.email,
        phone=data.phone,
        alamat=data.alamat,
        program_studi_id=data.program_studi_id
    )

    db.add(mahasiswa)
    db.commit()
    db.refresh(mahasiswa)
    return mahasiswa


@app.put("/api/pmb/approve/{mahasiswa_id}", response_model=PMBResponse)
def approve_pmb(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(CalonMahasiswa).filter_by(id=mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Data not found")

    if mhs.status == StatusEnum.approved:
        return mhs

    prodi = db.query(ProgramStudi).filter_by(id=mhs.program_studi_id).first()
    if not prodi:
        raise HTTPException(status_code=400, detail="Program studi not found")

    nim = generate_nim(datetime.now().year, prodi.kode, db)

    mhs.nim = nim
    mhs.status = StatusEnum.approved
    mhs.approved_at = datetime.utcnow()

    db.commit()
    db.refresh(mhs)
    return mhs


@app.get("/api/pmb/status/{mahasiswa_id}", response_model=PMBResponse)
def cek_status(mahasiswa_id: int, db: Session = Depends(get_db)):
    mhs = db.query(CalonMahasiswa).filter_by(id=mahasiswa_id).first()
    if not mhs:
        raise HTTPException(status_code=404, detail="Data not found")
    return mhs


@app.get("/api/pmb/stats")
def statistik(db: Session = Depends(get_db)):
    total = db.query(CalonMahasiswa).count()
    approved = db.query(CalonMahasiswa).filter_by(status=StatusEnum.approved).count()
    pending = db.query(CalonMahasiswa).filter_by(status=StatusEnum.pending).count()

    return {
        "total_pendaftar": total,
        "approved": approved,
        "pending": pending
    }
