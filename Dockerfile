FROM apache/airflow:2.9.0

USER root

RUN pip3 install pandas

USER airflow