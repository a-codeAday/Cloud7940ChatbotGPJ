FROM python
COPY chatbot_spoon_wine.py .
COPY connection.py .
COPY requirements.txt .
RUN pip install pip update
RUN pip install -r requirements.txt
EXPOSE 8080
CMD ["python","chatbot_spoon_wine.py"]
