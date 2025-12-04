FROM python:3.12

WORKDIR /streamlit_apps

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "main.py"]