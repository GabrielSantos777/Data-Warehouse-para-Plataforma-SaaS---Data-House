from dotenv import load_dotenv, find_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from faker import Faker
import random
from datetime import datetime, timedelta
import os

dotenv_path = find_dotenv()

load_dotenv(dotenv_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URI)
fake = Faker('pt-br')


def carregar_dimensoes():
    print("Iniciando carga das Dimensões...")
    planos = [
        {'nome_plano': 'Basic', 'valor_mensal': 99.0, 'limite_usuarios': 5},
        {'nome_plano': 'Pro', 'valor_mensal': 299.0, 'limite_usuarios': 20},
        {'nome_plano': 'Enterprise', 'valor_mensal': 999.0, 'limite_usuarios': 100}
    ]
    pd.DataFrame(planos).to_sql('dim_planos', engine, schema='public', if_exists='append', index=False)

    clientes = []
    for _ in range(50):
        clientes.append({
            'id_natural_cliente': fake.uuid4(),
            'nome_cliente': fake.name(),
            'email_cliente': fake.email(),
            'empresa_cliente': fake.company(),
            'segmento_empresa': random.choice(['Tech', 'Varejo', 'Saúde']),
            'pais': 'Brasil'
        })
    pd.DataFrame(clientes).to_sql('dim_clientes', engine, schema='public', if_exists='append', index=False)

    datas = []
    start_date = datetime(2024, 1, 1)
    for i in range(365):
        dt = start_date + timedelta(days=i)
        datas.append({
            'data_completa': dt, 'ano': dt.year, 'mes': dt.month,
            'nome_mes': dt.strftime('%B'), 'trimestre': (dt.month-1)//3+1,
            'dia_semana': dt.strftime('%A'), 'final_semana': dt.weekday() >= 5
        })
    pd.DataFrame(datas).to_sql('dim_tempo', engine, schema='public', if_exists='append', index=False)
    print("Dimensões carregadas!")

def carregar_fato():
    print("Iniciando carga da Tabela Fato...")
    with engine.connect() as conn:
        clientes = pd.read_sql("SELECT sk_cliente FROM public.dim_clientes LIMIT 1",conn)
        planos = pd.read_sql("SELECT sk_plano, valor_mensal FROM public.dim_planos", conn)
        datas = pd.read_sql("SELECT sk_tempo FROM public.dim_tempo", conn)

        vendas = []
        for _ in range(200):
            p = planos.sample(1).iloc[0]
            vendas.append({
                'fk_cliente': clientes.sample(1).iloc[0]['sk_cliente'],
                'fk_plano': p['sk_plano'],
                'fk_data_inicio': datas.sample(1).iloc[0]['sk_tempo'],
                'valor_contrato': float(p['valor_mensal']) * random.randint(1, 12),
                'status_assinatura': random.choice(['Ativa', 'Cancelada'])
            })
        pd.DataFrame(vendas).to_sql('fato_assinaturas', engine, schema='public', if_exists='append', index=False)
    print("Tabela Fato carregada!")

if __name__ == "__main__":
    carregar_dimensoes()
    carregar_fato()