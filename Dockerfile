FROM python:3.12-slim

# Microsoft EULA ni avtomatik qabul qilish
RUN echo "ttf-mscorefonts-installer msttcorefonts/accepted-mscorefonts-eula select true" | debconf-set-selections

# LibreOffice va shriftlarni o'rnatish
RUN apt-get update && apt-get install -y --no-install-recommends \
    debconf \
    libreoffice \
    libreoffice-writer \
    libreoffice-calc \
    fonts-liberation \
    fontconfig \
    ttf-mscorefonts-installer \
    && fc-cache -fv \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "bot.py"]
