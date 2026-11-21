#!/bin/zsh
cd "$(dirname "$0")" || exit 1

PORT=8080
LOCAL_IP=$(ipconfig getifaddr en0 2>/dev/null || ipconfig getifaddr en1 2>/dev/null || echo "localhost")
URL="http://${LOCAL_IP}:${PORT}/index.html"

clear
echo "=================================================="
echo "   قاموس لابات وميتاماير — خادم التثبيت على الموبايل"
echo "=================================================="
echo ""
echo "1. تأكد أن الايفون أو الاندرويد متصل بنفس شبكة الواي فاي."
echo "2. افتح الرابط التالي على متصفح الهاتف (Safari للايفون / Chrome للاندرويد):"
echo ""
echo "   $URL"
echo ""
echo "3. للايفون (Safari): اضغط زر المشاركة ⬆️ ثم (إضافة إلى الشاشة الرئيسية)."
echo "4. للاندرويد (Chrome): اضغط القائمة (⋮) ثم (تثبيت التطبيق)."
echo ""
echo "بعد التثبيت سيعمل التطبيق بالكامل 100% بدون إنترنت حتى لو أغلقت هذا الخادم."
echo "--------------------------------------------------"

python3 - <<PY 2>/dev/null
try:
    import qrcode
    qr = qrcode.QRCode(border=1)
    qr.add_data("$URL")
    qr.print_ascii(invert=True)
except Exception:
    pass
PY

echo "جاري تشغيل الخادم على المنفذ $PORT ... (للايقاف اضغط Ctrl+C)"
python3 -m http.server "$PORT" --bind 0.0.0.0
