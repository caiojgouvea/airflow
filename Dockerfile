FROM apache/airflow:2.6.1

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy your DAGs and scripts into the container
COPY dags /opt/airflow/dags
COPY scripts /opt/airflow/scripts