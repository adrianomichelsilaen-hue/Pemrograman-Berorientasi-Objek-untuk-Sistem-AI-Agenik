import React, { useState, useEffect } from 'react';
import { Users, DollarSign, AlertCircle, TrendingUp, Plus, Search, Edit2, Trash2, Eye, Printer, X, Check } from 'lucide-react';

const SPPManagementSystem = () => {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [students, setStudents] = useState([]);
  const [payments, setPayments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [showModal, setShowModal] = useState(false);
  const [modalType, setModalType] = useState('');
  const [selectedStudent, setSelectedStudent] = useState(null);
  const [formData, setFormData] = useState({});
  const [receipt, setReceipt] = useState(null);

  // Load data dari storage
  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const studentsData = await window.storage.get('spp_students');
      const paymentsData = await window.storage.get('spp_payments');
      
      if (studentsData?.value) {
        setStudents(JSON.parse(studentsData.value));
      } else {
        // Data dummy untuk demo
        const dummyStudents = [
          { id: '1', nis: '2024001', name: 'Ahmad Rizki', class: 'X-A', phone: '081234567890' },
          { id: '2', nis: '2024002', name: 'Siti Nurhaliza', class: 'X-A', phone: '081234567891' },
          { id: '3', nis: '2024003', name: 'Budi Santoso', class: 'X-B', phone: '081234567892' },
        ];
        setStudents(dummyStudents);
        await window.storage.set('spp_students', JSON.stringify(dummyStudents));
      }
      
      if (paymentsData?.value) {
        setPayments(JSON.parse(paymentsData.value));
      }
    } catch (error) {
      console.error('Error loading data:', error);
    }
    setLoading(false);
  };

  const saveStudents = async (newStudents) => {
    try {
      await window.storage.set('spp_students', JSON.stringify(newStudents));
      setStudents(newStudents);
    } catch (error) {
      console.error('Error saving students:', error);
    }
  };

  const savePayments = async (newPayments) => {
    try {
      await window.storage.set('spp_payments', JSON.stringify(newPayments));
      setPayments(newPayments);
    } catch (error) {
      console.error('Error saving payments:', error);
    }
  };

  // Fungsi tambah/edit siswa
  const handleSaveStudent = async () => {
    if (!formData.name || !formData.nis || !formData.class) {
      alert('Mohon lengkapi semua data!');
      return;
    }

    if (modalType === 'add') {
      const newStudent = {
        id: Date.now().toString(),
        ...formData
      };
      await saveStudents([...students, newStudent]);
    } else if (modalType === 'edit') {
      const updated = students.map(s => 
        s.id === selectedStudent.id ? { ...s, ...formData } : s
      );
      await saveStudents(updated);
    }
    
    setShowModal(false);
    setFormData({});
  };

  // Fungsi hapus siswa
  const handleDeleteStudent = async (id) => {
    if (window.confirm('Yakin ingin menghapus siswa ini?')) {
      const filtered = students.filter(s => s.id !== id);
      await saveStudents(filtered);
      
      // Hapus juga payment history siswa ini
      const filteredPayments = payments.filter(p => p.studentId !== id);
      await savePayments(filteredPayments);
    }
  };

  // Fungsi tambah pembayaran
  const handleAddPayment = async () => {
    if (!formData.month || !formData.amount) {
      alert('Mohon lengkapi data pembayaran!');
      return;
    }

    const newPayment = {
      id: Date.now().toString(),
      studentId: selectedStudent.id,
      studentName: selectedStudent.name,
      studentNis: selectedStudent.nis,
      month: formData.month,
      amount: parseInt(formData.amount),
      date: new Date().toISOString(),
      status: 'Lunas'
    };

    const newPayments = [...payments, newPayment];
    await savePayments(newPayments);
    
    setReceipt(newPayment);
    setShowModal(false);
    setFormData({});
  };

  // Kalkulasi statistik
  const totalStudents = students.length;
  const totalPayments = payments.reduce((sum, p) => sum + p.amount, 0);
  const thisMonthPayments = payments.filter(p => {
    const payDate = new Date(p.date);
    const now = new Date();
    return payDate.getMonth() === now.getMonth() && 
           payDate.getFullYear() === now.getFullYear();
  }).length;

  // Hitung tunggakan (asumsi SPP per bulan Rp 500.000)
  const monthlyFee = 500000;
  const currentMonth = new Date().getMonth() + 1;
  const expectedPayments = totalStudents * currentMonth;
  const actualPayments = payments.length;
  const outstandingCount = expectedPayments - actualPayments;

  // Filter siswa
  const filteredStudents = students.filter(s => 
    s.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    s.nis.includes(searchTerm) ||
    s.class.toLowerCase().includes(searchTerm.toLowerCase())
  );

  // Hitung tunggakan per siswa
  const getStudentArrears = (studentId) => {
    const studentPayments = payments.filter(p => p.studentId === studentId);
    const paidMonths = studentPayments.length;
    const shouldPay = currentMonth;
    return (shouldPay - paidMonths) * monthlyFee;
  };

  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('id-ID', {
      style: 'currency',
      currency: 'IDR',
      minimumFractionDigits: 0
    }).format(amount);
  };

  const openModal = (type, student = null) => {
    setModalType(type);
    setSelectedStudent(student);
    if (type === 'edit' && student) {
      setFormData(student);
    } else {
      setFormData({});
    }
    setShowModal(true);
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Memuat data...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-gradient-to-r from-blue-600 to-blue-800 text-white p-6 shadow-lg">
        <div className="max-w-7xl mx-auto">
          <h1 className="text-3xl font-bold">Sistem Manajemen SPP</h1>
          <p className="text-blue-100 mt-1">Manajemen Pembayaran Pendidikan</p>
        </div>
      </div>

      {/* Navigation */}
      <div className="bg-white shadow">
        <div className="max-w-7xl mx-auto">
          <div className="flex space-x-1">
            {['dashboard', 'siswa', 'pembayaran', 'tunggakan', 'riwayat'].map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`px-6 py-3 font-medium capitalize transition-colors ${
                  activeTab === tab
                    ? 'text-blue-600 border-b-2 border-blue-600'
                    : 'text-gray-600 hover:text-blue-600'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto p-6">
        {/* Dashboard */}
        {activeTab === 'dashboard' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Dashboard</h2>
            
            {/* Stats Cards */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Siswa</p>
                    <p className="text-3xl font-bold text-gray-800 mt-2">{totalStudents}</p>
                  </div>
                  <Users className="text-blue-600" size={40} />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Total Pemasukan</p>
                    <p className="text-2xl font-bold text-green-600 mt-2">
                      {formatCurrency(totalPayments)}
                    </p>
                  </div>
                  <DollarSign className="text-green-600" size={40} />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Pembayaran Bulan Ini</p>
                    <p className="text-3xl font-bold text-gray-800 mt-2">{thisMonthPayments}</p>
                  </div>
                  <TrendingUp className="text-purple-600" size={40} />
                </div>
              </div>

              <div className="bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="flex items-center justify-between">
                  <div>
                    <p className="text-gray-600 text-sm">Tunggakan</p>
                    <p className="text-3xl font-bold text-red-600 mt-2">{outstandingCount}</p>
                  </div>
                  <AlertCircle className="text-red-600" size={40} />
                </div>
              </div>
            </div>

            {/* Grafik Sederhana */}
            <div className="bg-white p-6 rounded-lg shadow">
              <h3 className="text-lg font-semibold mb-4">Pembayaran 5 Terakhir</h3>
              <div className="space-y-3">
                {payments.slice(-5).reverse().map(payment => (
                  <div key={payment.id} className="flex items-center justify-between p-3 bg-gray-50 rounded">
                    <div>
                      <p className="font-medium">{payment.studentName}</p>
                      <p className="text-sm text-gray-600">{payment.month}</p>
                    </div>
                    <div className="text-right">
                      <p className="font-semibold text-green-600">{formatCurrency(payment.amount)}</p>
                      <p className="text-xs text-gray-500">{new Date(payment.date).toLocaleDateString('id-ID')}</p>
                    </div>
                  </div>
                ))}
                {payments.length === 0 && (
                  <p className="text-gray-500 text-center py-8">Belum ada pembayaran</p>
                )}
              </div>
            </div>
          </div>
        )}

        {/* Data Siswa */}
        {activeTab === 'siswa' && (
          <div>
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-2xl font-bold">Data Siswa</h2>
              <button
                onClick={() => openModal('add')}
                className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 flex items-center gap-2"
              >
                <Plus size={20} />
                Tambah Siswa
              </button>
            </div>

            {/* Search */}
            <div className="mb-4">
              <div className="relative">
                <Search className="absolute left-3 top-3 text-gray-400" size={20} />
                <input
                  type="text"
                  placeholder="Cari siswa (nama, NIS, kelas)..."
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  className="w-full pl-10 pr-4 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                />
              </div>
            </div>

            {/* Table */}
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">NIS</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nama</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kelas</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">No. Telp</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Aksi</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {filteredStudents.map(student => (
                    <tr key={student.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">{student.nis}</td>
                      <td className="px-6 py-4 whitespace-nowrap font-medium">{student.name}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{student.class}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{student.phone}</td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex gap-2">
                          <button
                            onClick={() => openModal('edit', student)}
                            className="text-blue-600 hover:text-blue-800"
                          >
                            <Edit2 size={18} />
                          </button>
                          <button
                            onClick={() => handleDeleteStudent(student.id)}
                            className="text-red-600 hover:text-red-800"
                          >
                            <Trash2 size={18} />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {filteredStudents.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Tidak ada data siswa
                </div>
              )}
            </div>
          </div>
        )}

        {/* Pembayaran */}
        {activeTab === 'pembayaran' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Input Pembayaran</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {students.map(student => (
                <div key={student.id} className="bg-white p-4 rounded-lg shadow hover:shadow-md transition-shadow">
                  <div className="flex items-start justify-between mb-3">
                    <div>
                      <h3 className="font-semibold">{student.name}</h3>
                      <p className="text-sm text-gray-600">NIS: {student.nis}</p>
                      <p className="text-sm text-gray-600">Kelas: {student.class}</p>
                    </div>
                  </div>
                  <button
                    onClick={() => openModal('payment', student)}
                    className="w-full bg-green-600 text-white py-2 rounded hover:bg-green-700 flex items-center justify-center gap-2"
                  >
                    <Plus size={18} />
                    Bayar SPP
                  </button>
                </div>
              ))}
            </div>

            {students.length === 0 && (
              <div className="text-center py-12 text-gray-500">
                Belum ada data siswa. Tambahkan siswa terlebih dahulu.
              </div>
            )}
          </div>
        )}

        {/* Tunggakan */}
        {activeTab === 'tunggakan' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Laporan Tunggakan</h2>
            
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">NIS</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nama</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Kelas</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Sudah Bayar</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tunggakan</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {students.map(student => {
                    const arrears = getStudentArrears(student.id);
                    const paidMonths = payments.filter(p => p.studentId === student.id).length;
                    return (
                      <tr key={student.id} className="hover:bg-gray-50">
                        <td className="px-6 py-4 whitespace-nowrap">{student.nis}</td>
                        <td className="px-6 py-4 whitespace-nowrap font-medium">{student.name}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{student.class}</td>
                        <td className="px-6 py-4 whitespace-nowrap">{paidMonths} bulan</td>
                        <td className="px-6 py-4 whitespace-nowrap font-semibold text-red-600">
                          {formatCurrency(arrears)}
                        </td>
                        <td className="px-6 py-4 whitespace-nowrap">
                          {arrears > 0 ? (
                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-red-100 text-red-800">
                              Menunggak
                            </span>
                          ) : (
                            <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                              Lunas
                            </span>
                          )}
                        </td>
                      </tr>
                    );
                  })}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Riwayat */}
        {activeTab === 'riwayat' && (
          <div>
            <h2 className="text-2xl font-bold mb-6">Riwayat Transaksi</h2>
            
            <div className="bg-white rounded-lg shadow overflow-hidden">
              <table className="w-full">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Tanggal</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">NIS</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Nama</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Bulan</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Jumlah</th>
                    <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {payments.slice().reverse().map(payment => (
                    <tr key={payment.id} className="hover:bg-gray-50">
                      <td className="px-6 py-4 whitespace-nowrap">
                        {new Date(payment.date).toLocaleDateString('id-ID')}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">{payment.studentNis}</td>
                      <td className="px-6 py-4 whitespace-nowrap font-medium">{payment.studentName}</td>
                      <td className="px-6 py-4 whitespace-nowrap">{payment.month}</td>
                      <td className="px-6 py-4 whitespace-nowrap font-semibold text-green-600">
                        {formatCurrency(payment.amount)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-green-100 text-green-800">
                          {payment.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
              {payments.length === 0 && (
                <div className="text-center py-8 text-gray-500">
                  Belum ada riwayat transaksi
                </div>
              )}
            </div>
          </div>
        )}
      </div>

      {/* Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="flex justify-between items-center mb-4">
              <h3 className="text-xl font-bold">
                {modalType === 'add' && 'Tambah Siswa Baru'}
                {modalType === 'edit' && 'Edit Data Siswa'}
                {modalType === 'payment' && 'Input Pembayaran'}
              </h3>
              <button onClick={() => setShowModal(false)} className="text-gray-500 hover:text-gray-700">
                <X size={24} />
              </button>
            </div>

            {(modalType === 'add' || modalType === 'edit') && (
              <div className="space-y-4">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">NIS</label>
                  <input
                    type="text"
                    value={formData.nis || ''}
                    onChange={(e) => setFormData({...formData, nis: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Masukkan NIS"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Nama Lengkap</label>
                  <input
                    type="text"
                    value={formData.name || ''}
                    onChange={(e) => setFormData({...formData, name: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Masukkan nama"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Kelas</label>
                  <input
                    type="text"
                    value={formData.class || ''}
                    onChange={(e) => setFormData({...formData, class: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="Contoh: X-A"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">No. Telepon</label>
                  <input
                    type="text"
                    value={formData.phone || ''}
                    onChange={(e) => setFormData({...formData, phone: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="08xxxxxxxxxx"
                  />
                </div>
                <button
                  onClick={handleSaveStudent}
                  className="w-full bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
                >
                  <Check size={20} />
                  Simpan Data
                </button>
              </div>
            )}

            {modalType === 'payment' && (
              <div className="space-y-4">
                <div className="bg-gray-50 p-3 rounded">
                  <p className="text-sm text-gray-600">Nama Siswa</p>
                  <p className="font-semibold">{selectedStudent?.name}</p>
                  <p className="text-sm text-gray-600 mt-1">NIS: {selectedStudent?.nis}</p>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Bulan Pembayaran</label>
                  <select
                    value={formData.month || ''}
                    onChange={(e) => setFormData({...formData, month: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                  >
                    <option value="">Pilih Bulan</option>
                    <option value="Januari 2026">Januari 2026</option>
                    <option value="Februari 2026">Februari 2026</option>
                    <option value="Maret 2026">Maret 2026</option>
                    <option value="April 2026">April 2026</option>
                    <option value="Mei 2026">Mei 2026</option>
                    <option value="Juni 2026">Juni 2026</option>
                    <option value="Juli 2026">Juli 2026</option>
                    <option value="Agustus 2026">Agustus 2026</option>
                    <option value="September 2026">September 2026</option>
                    <option value="Oktober 2026">Oktober 2026</option>
                    <option value="November 2026">November 2026</option>
                    <option value="Desember 2026">Desember 2026</option>
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">Jumlah Pembayaran</label>
                  <input
                    type="number"
                    value={formData.amount || ''}
                    onChange={(e) => setFormData({...formData, amount: e.target.value})}
                    className="w-full px-3 py-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
                    placeholder="500000"
                  />
                  <p className="text-xs text-gray-500 mt-1">Default: Rp 500.000</p>
                </div>
                <button
                  onClick={handleAddPayment}
                  className="w-full bg-green-600 text-white py-2 rounded-lg hover:bg-green-700 flex items-center justify-center gap-2"
                >
                  <Check size={20} />
                  Proses Pembayaran
                </button>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Receipt Modal */}
      {receipt && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center p-4 z-50">
          <div className="bg-white rounded-lg max-w-md w-full p-6">
            <div className="text-center mb-6">
              <div className="w-16 h-16 bg-green-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <Check className="text-green-600" size={32} />
              </div>
              <h3 className="text-2xl font-bold text-gray-800">Pembayaran Berhasil!</h3>
            </div>

            <div className="border-t border-b border-gray-200 py-4 mb-4 space-y-2">
              <div className="flex justify-between">
                <span className="text-gray-600">Nama</span>
                <span className="font-semibold">{receipt.studentName}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">NIS</span>
                <span className="font-semibold">{receipt.studentNis}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Bulan</span>
                <span className="font-semibold">{receipt.month}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-gray-600">Tanggal</span>
                <span className="font-semibold">{new Date(receipt.date).toLocaleDateString('id-ID')}</span>
              </div>
              <div className="flex justify-between text-lg">
                <span className="text-gray-600">Jumlah</span>
                <span className="font-bold text-green-600">{formatCurrency(receipt.amount)}</span>
              </div>
            </div>

            <div className="flex gap-3">
              <button
                onClick={() => window.print()}
                className="flex-1 bg-blue-600 text-white py-2 rounded-lg hover:bg-blue-700 flex items-center justify-center gap-2"
              >
                <Printer size={20} />
                Cetak Struk
              </button>
              <button
                onClick={() => setReceipt(null)}
                className="flex-1 bg-gray-200 text-gray-800 py-2 rounded-lg hover:bg-gray-300"
              >
                Tutup
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default SPPManagementSystem;