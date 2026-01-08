import pandas as pd
import numpy as np
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker('pt_BR')

def gerar_dados_clientes(n_clientes=500):
    planos = {
        'Basic': {'preco': 99.0, 'churn_base': 0.05},      # 5% de chance de cancelar/mês
        'Pro': {'preco': 249.0, 'churn_base': 0.03},       # 3% de chance de cancelar/mês
        'Enterprise': {'preco': 799.0, 'churn_base': 0.01} # 1% de chance de cancelar/mês
    }
    
    lista_eventos = []
    data_inicio = datetime(2020, 1, 1)
    
    for _ in range(n_clientes):
        cliente_id = fake.uuid4()
        cliente_nome = fake.company()
        plano_nome = random.choice(list(planos.keys()))
        valor_mensal = planos[plano_nome]['preco']
        
        data_adesao = data_inicio + timedelta(days=random.randint(0, 600))
        
        data_atual = data_adesao
        ativo = True
        
        while ativo and data_atual < datetime(2025, 12, 31):
            #Vou registrar um evento de pagamento para este mês
            lista_eventos.append({
                'data_evento': data_atual,
                'cliente_id': cliente_id,
                'cliente_nome': cliente_nome,
                'plano': plano_nome,
                'valor': valor_mensal,
                'tipo_evento': 'Pagamento',
            })
            
            # Lógica de Churn: O cliente vai cancelar este mês?
            # Se o número aleatório for menor que o churn_base, ele cancela.
            if random.random() < planos[plano_nome]['churn_base']:
                lista_eventos.append({
                    'data_evento': data_atual + timedelta(days=28),
                    'cliente_id': cliente_id,
                    'cliente_nome': cliente_nome,
                    'plano': plano_nome,
                    'valor': 0,
                    'tipo_evento': 'Cancelamento',
                })
                ativo = False
            
            data_atual += timedelta(days=30)  # Próximo mês
    
    df = pd.DataFrame(lista_eventos)
    df.to_csv('data/clientes_eventos.csv', index=False)
    print("Dados de clientes gerados e salvos em 'data/clientes_eventos.csv'.")

if __name__ == "__main__":
    gerar_dados_clientes()