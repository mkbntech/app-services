FROM docker.io/library/python:3.12-slim AS base
WORKDIR /srv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY app ./app
ENV PORT=8001
EXPOSE 8001
HEALTHCHECK --interval=15s --timeout=3s --start-period=5s CMD python -c "import urllib.request;urllib.request.urlopen('http://localhost:8001/health')" || exit 1
USER 1000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8001"]
