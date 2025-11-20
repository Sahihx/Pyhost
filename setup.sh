#!/bin/bash
# Python Host Setup Script with Language Selection for Termux

echo "=== تحديث الحزم ==="
pkg update -y && pkg upgrade -y

echo "=== تثبيت بايثون والأدوات المطلوبة ==="
pkg install -y python openssl nano git curl

echo "=== تثبيت مكتبات بايثون ==="
pip install --upgrade pip
pip install fastapi uvicorn jinja2 psutil

mkdir -p cert templates static/css static/js

# TLS certificate
if [ ! -f cert/cert.pem ] || [ ! -f cert/key.pem ]; then
    openssl req -x509 -newkey rsa:4096 -keyout cert/key.pem -out cert/cert.pem -days 365 -nodes -subj "/CN=localhost"
fi

# jobs_db.json
if [ ! -f jobs_db.json ]; then echo "{}" > jobs_db.json; fi

# lang.json
if [ ! -f lang.json ]; then
cat > lang.json <<EOL
{
  "en": {"run_code": "Run Python Code", "run": "Run", "jobs": "Jobs"},
  "ar": {"run_code": "تشغيل كود بايثون", "run": "تشغيل", "jobs": "المهام"}
}
EOL
fi

# اختيار اللغة
echo "=== اختر لغة الواجهة ==="
echo "1) English"
echo "2) عربي"
read -p "اختر اللغة / Choose language [1-2]: " LANG_CHOICE
if [ "$LANG_CHOICE" == "2" ]; then SELECTED_LANG="ar"; else SELECTED_LANG="en"; fi

# تعديل app.py
if grep -q "LANG = " app.py; then
    sed -i "s/LANG = .*/LANG = \"$SELECTED_LANG\"/" app.py
else
    echo "LANG = \"$SELECTED_LANG\"" >> app.py
fi

echo "=== اللغة المختارة: $SELECTED_LANG ==="

# تشغيل الخادم في الخلفية مع Wake Lock
termux-wake-lock
nohup python app.py > nohup.log 2>&1 &

echo "=== انتهى التثبيت ==="
echo "الخادم يعمل على https://localhost:8443"
echo "لمشاهدة اللوج: cat nohup.log"
