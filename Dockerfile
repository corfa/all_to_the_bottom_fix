FROM python:latest
EXPOSE 8000
COPY ./ ./
RUN pip install --no-cache-dir -r requirements.txt
RUN hypercorn main:app