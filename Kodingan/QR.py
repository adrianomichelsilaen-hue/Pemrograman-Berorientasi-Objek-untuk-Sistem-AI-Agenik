<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>QR Code Generator Pro</title>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js"></script>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        .container {
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            max-width: 900px;
            width: 100%;
            padding: 40px;
        }

        h1 {
            text-align: center;
            color: #667eea;
            margin-bottom: 10px;
            font-size: 2.5em;
        }

        .subtitle {
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-size: 1.1em;
        }

        .content-wrapper {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 30px;
            margin-top: 20px;
        }

        .input-section {
            display: flex;
            flex-direction: column;
            gap: 20px;
        }

        .form-group {
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        label {
            font-weight: 600;
            color: #333;
            font-size: 0.95em;
        }

        input[type="text"],
        input[type="url"],
        textarea {
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 1em;
            transition: all 0.3s;
        }

        input[type="text"]:focus,
        input[type="url"]:focus,
        textarea:focus {
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }

        textarea {
            resize: vertical;
            min-height: 100px;
            font-family: inherit;
        }

        .color-group {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .color-input {
            display: flex;
            align-items: center;
            gap: 10px;
        }

        input[type="color"] {
            width: 60px;
            height: 40px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            cursor: pointer;
        }

        .size-control {
            display: flex;
            flex-direction: column;
            gap: 10px;
        }

        input[type="range"] {
            width: 100%;
            height: 8px;
            border-radius: 5px;
            background: #e0e0e0;
            outline: none;
            -webkit-appearance: none;
        }

        input[type="range"]::-webkit-slider-thumb {
            -webkit-appearance: none;
            appearance: none;
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
        }

        input[type="range"]::-moz-range-thumb {
            width: 20px;
            height: 20px;
            border-radius: 50%;
            background: #667eea;
            cursor: pointer;
            border: none;
        }

        .size-value {
            text-align: center;
            font-weight: 600;
            color: #667eea;
            font-size: 1.1em;
        }

        .button-group {
            display: flex;
            gap: 10px;
        }

        button {
            flex: 1;
            padding: 14px;
            border: none;
            border-radius: 8px;
            font-size: 1em;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s;
        }

        .btn-generate {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }

        .btn-generate:hover {
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(102, 126, 234, 0.4);
        }

        .btn-download {
            background: #4CAF50;
            color: white;
        }

        .btn-download:hover {
            background: #45a049;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(76, 175, 80, 0.4);
        }

        .btn-clear {
            background: #f44336;
            color: white;
        }

        .btn-clear:hover {
            background: #da190b;
            transform: translateY(-2px);
            box-shadow: 0 5px 15px rgba(244, 67, 54, 0.4);
        }

        button:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none !important;
        }

        .preview-section {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #f8f9fa;
            border-radius: 12px;
            padding: 30px;
            min-height: 400px;
        }

        #qrcode {
            background: white;
            padding: 20px;
            border-radius: 12px;
            box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }

        #qrcode canvas {
            display: block !important;
        }

        .placeholder {
            text-align: center;
            color: #999;
        }

        .placeholder svg {
            width: 150px;
            height: 150px;
            opacity: 0.3;
            margin-bottom: 20px;
        }

        .info-box {
            background: #e3f2fd;
            border-left: 4px solid #2196F3;
            padding: 15px;
            border-radius: 8px;
            margin-top: 20px;
        }

        .info-box h3 {
            color: #1976D2;
            margin-bottom: 8px;
            font-size: 1em;
        }

        .info-box ul {
            margin-left: 20px;
            color: #555;
            line-height: 1.6;
        }

        .stats {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 15px;
            margin-top: 20px;
        }

        .stat-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 20px;
            border-radius: 12px;
            text-align: center;
        }

        .stat-value {
            font-size: 2em;
            font-weight: bold;
            margin-bottom: 5px;
        }

        .stat-label {
            font-size: 0.9em;
            opacity: 0.9;
        }

        @media (max-width: 768px) {
            .content-wrapper {
                grid-template-columns: 1fr;
            }

            .container {
                padding: 20px;
            }

            h1 {
                font-size: 2em;
            }

            .stats {
                grid-template-columns: 1fr;
            }
        }

        .error-message {
            background: #ffebee;
            color: #c62828;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }

        .success-message {
            background: #e8f5e9;
            color: #2e7d32;
            padding: 12px;
            border-radius: 8px;
            margin-top: 10px;
            display: none;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎯 QR Code Generator Pro</h1>
        <p class="subtitle">Generate Custom QR Codes Instantly</p>

        <div class="stats">
            <div class="stat-card">
                <div class="stat-value" id="qrGenerated">0</div>
                <div class="stat-label">QR Generated</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="qrDownloaded">0</div>
                <div class="stat-label">Downloaded</div>
            </div>
            <div class="stat-card">
                <div class="stat-value" id="currentSize">256</div>
                <div class="stat-label">Current Size</div>
            </div>
        </div>

        <div class="content-wrapper">
            <div class="input-section">
                <div class="form-group">
                    <label for="qrType">📝 Tipe Konten:</label>
                    <select id="qrType" style="padding: 12px; border: 2px solid #e0e0e0; border-radius: 8px; font-size: 1em;">
                        <option value="text">Text / URL</option>
                        <option value="email">Email</option>
                        <option value="phone">Nomor Telepon</option>
                        <option value="sms">SMS</option>
                        <option value="wifi">WiFi</option>
                    </select>
                </div>

                <div class="form-group">
                    <label for="qrText">💬 Konten QR Code:</label>
                    <textarea id="qrText" placeholder="Masukkan text, URL, atau data lainnya..." rows="3"></textarea>
                </div>

                <div class="form-group">
                    <label>🎨 Warna QR Code:</label>
                    <div class="color-group">
                        <div class="color-input">
                            <input type="color" id="colorDark" value="#000000">
                            <span>Foreground</span>
                        </div>
                        <div class="color-input">
                            <input type="color" id="colorLight" value="#ffffff">
                            <span>Background</span>
                        </div>
                    </div>
                </div>

                <div class="form-group">
                    <label>📏 Ukuran QR Code:</label>
                    <div class="size-control">
                        <input type="range" id="qrSize" min="128" max="512" value="256" step="32">
                        <div class="size-value"><span id="sizeDisplay">256</span> x <span id="sizeDisplay2">256</span> px</div>
                    </div>
                </div>

                <div class="button-group">
                    <button class="btn-generate" onclick="generateQR()">🚀 Generate</button>
                    <button class="btn-clear" onclick="clearQR()">🗑️ Clear</button>
                </div>

                <button class="btn-download" id="downloadBtn" onclick="downloadQR()" disabled>⬇️ Download PNG</button>

                <div class="error-message" id="errorMsg"></div>
                <div class="success-message" id="successMsg"></div>

                <div class="info-box">
                    <h3>📚 Panduan Penggunaan:</h3>
                    <ul>
                        <li>Pilih tipe konten QR Code</li>
                        <li>Masukkan data yang ingin diencode</li>
                        <li>Customize warna dan ukuran</li>
                        <li>Klik Generate untuk membuat QR</li>
                        <li>Download hasil QR Code</li>
                    </ul>
                </div>
            </div>

            <div class="preview-section">
                <div id="qrcode">
                    <div class="placeholder">
                        <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                            <rect x="10" y="10" width="35" height="35" fill="currentColor"/>
                            <rect x="55" y="10" width="35" height="35" fill="currentColor"/>
                            <rect x="10" y="55" width="35" height="35" fill="currentColor"/>
                            <rect x="20" y="20" width="15" height="15" fill="white"/>
                            <rect x="65" y="20" width="15" height="15" fill="white"/>
                            <rect x="20" y="65" width="15" height="15" fill="white"/>
                        </svg>
                        <p><strong>QR Code Preview</strong></p>
                        <p>Generate QR code untuk melihat preview</p>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <script>
        let qrcode = null;
        let generatedCount = 0;
        let downloadedCount = 0;

        // Update size display
        document.getElementById('qrSize').addEventListener('input', function() {
            const size = this.value;
            document.getElementById('sizeDisplay').textContent = size;
            document.getElementById('sizeDisplay2').textContent = size;
            document.getElementById('currentSize').textContent = size;
        });

        // Auto-format based on type
        document.getElementById('qrType').addEventListener('change', function() {
            const type = this.value;
            const textArea = document.getElementById('qrText');
            
            switch(type) {
                case 'email':
                    textArea.placeholder = 'mailto:example@email.com?subject=Hello';
                    break;
                case 'phone':
                    textArea.placeholder = 'tel:+62812345678';
                    break;
                case 'sms':
                    textArea.placeholder = 'sms:+62812345678?body=Hello';
                    break;
                case 'wifi':
                    textArea.placeholder = 'WIFI:T:WPA;S:NetworkName;P:Password;;';
                    break;
                default:
                    textArea.placeholder = 'Masukkan text, URL, atau data lainnya...';
            }
        });

        function showError(message) {
            const errorMsg = document.getElementById('errorMsg');
            errorMsg.textContent = message;
            errorMsg.style.display = 'block';
            setTimeout(() => {
                errorMsg.style.display = 'none';
            }, 3000);
        }

        function showSuccess(message) {
            const successMsg = document.getElementById('successMsg');
            successMsg.textContent = message;
            successMsg.style.display = 'block';
            setTimeout(() => {
                successMsg.style.display = 'none';
            }, 3000);
        }

        function generateQR() {
            const text = document.getElementById('qrText').value.trim();
            
            if (!text) {
                showError('❌ Konten tidak boleh kosong!');
                return;
            }

            const size = parseInt(document.getElementById('qrSize').value);
            const colorDark = document.getElementById('colorDark').value;
            const colorLight = document.getElementById('colorLight').value;

            // Clear previous QR code
            document.getElementById('qrcode').innerHTML = '';

            // Generate new QR code
            qrcode = new QRCode(document.getElementById('qrcode'), {
                text: text,
                width: size,
                height: size,
                colorDark: colorDark,
                colorLight: colorLight,
                correctLevel: QRCode.CorrectLevel.H
            });

            // Enable download button
            document.getElementById('downloadBtn').disabled = false;

            // Update stats
            generatedCount++;
            document.getElementById('qrGenerated').textContent = generatedCount;

            showSuccess('✅ QR Code berhasil dibuat!');
        }

        function downloadQR() {
            const canvas = document.querySelector('#qrcode canvas');
            
            if (!canvas) {
                showError('❌ Generate QR Code terlebih dahulu!');
                return;
            }

            // Convert canvas to blob and download
            canvas.toBlob(function(blob) {
                const url = URL.createObjectURL(blob);
                const link = document.createElement('a');
                const timestamp = new Date().getTime();
                link.download = `qrcode_${timestamp}.png`;
                link.href = url;
                link.click();
                URL.revokeObjectURL(url);

                // Update stats
                downloadedCount++;
                document.getElementById('qrDownloaded').textContent = downloadedCount;

                showSuccess('✅ QR Code berhasil didownload!');
            });
        }

        function clearQR() {
            document.getElementById('qrText').value = '';
            document.getElementById('qrcode').innerHTML = `
                <div class="placeholder">
                    <svg viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
                        <rect x="10" y="10" width="35" height="35" fill="currentColor"/>
                        <rect x="55" y="10" width="35" height="35" fill="currentColor"/>
                        <rect x="10" y="55" width="35" height="35" fill="currentColor"/>
                        <rect x="20" y="20" width="15" height="15" fill="white"/>
                        <rect x="65" y="20" width="15" height="15" fill="white"/>
                        <rect x="20" y="65" width="15" height="15" fill="white"/>
                    </svg>
                    <p><strong>QR Code Preview</strong></p>
                    <p>Generate QR code untuk melihat preview</p>
                </div>
            `;
            document.getElementById('downloadBtn').disabled = true;
            qrcode = null;

            showSuccess('🗑️ QR Code berhasil dihapus!');
        }

        // Keyboard shortcuts
        document.addEventListener('keydown', function(e) {
            if (e.ctrlKey && e.key === 'Enter') {
                generateQR();
            } else if (e.ctrlKey && e.key === 'd') {
                e.preventDefault();
                downloadQR();
            }
        });
    </script>
</body>
</html>