FROM python
COPY chatbot_spoon_wine.py .
COPY requirements.txt .
RUN pip install pip update
RUN pip install -r requirements.txt
ENV ACCESS_TOKEN=5260465865:AAGEBv51BLalzMkM3IF3TwB_9mysSy21_No
ENV PYMYSQL_HOST=159.223.93.84
ENV PYMYSQL_USER=comp7940GP15cloud
ENV PYMYSQL_PASSWORD=comp7940GP15cloud
ENV PYMYSQL_DB_NAME=comp7940gp15
ENV PYMYSQL_PORT=3306
ENV SPOON_KEY=3ee7d67b42f94c428880b12b632e1177
EXPOSE 8080
CMD ["python","chatbot_spoon_wine.py"]