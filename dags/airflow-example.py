from airflow import DAG 
from datetime import datetime
from airflow.operators.python import PythonOperator, BranchPythonOperator
from airflow.operators.bash import BashOperator
import pandas as pd
import requests
import json

def extracao_dados_pockemon():
    # url = "https://zenodo.org/record/4552785/files/pokemon-descriptioncorpus.json?download=1"
    # response = requests.get(url)
    # df = pd.DataFrame(json.loads(response.content))
    df = pd.read_csv('dags/pokemon.csv', delimiter=',', skiprows=1)
    print(df)
    qtd = len(df.index)
    return qtd

def e_valida(ti):
    qtd = ti.xcom_pull(task_ids = 'extracao_dados_pockemon')
    if (qtd > 1000):
        return 'valido'
    return 'nvalido'

with DAG('apresentacao_airflow', start_date = datetime(2023,6,3),
    schedule_interval="30 * * * *", catchup=False) as dag:

    captura_conta_dados = PythonOperator(
         task_id = 'extracao_dados_pockemon',
         python_callable = extracao_dados_pockemon
    )

    e_valida = BranchPythonOperator(
        task_id = 'e_valida',
        python_callable = e_valida)
    
    valido = BashOperator(
        task_id = 'valido',
        bash_command = "echo 'Quantidade ok'"
        )

    nvalido = BashOperator(
        task_id = 'nvalido',
        bash_command = "echo 'Quantidade não ok'"
        )
    
    captura_conta_dados >> e_valida >> [valido, nvalido]