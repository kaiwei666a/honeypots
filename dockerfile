
FROM python:3.12

RUN apt-get update && apt-get install -y python3 python3-pip \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .



RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 2222
EXPOSE 8186

CMD ["python", "honeypots_agent.py"]

