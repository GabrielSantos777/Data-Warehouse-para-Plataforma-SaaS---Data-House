CREATE TABLE dim_tempo (
	sk_tempo SERIAL PRIMARY KEY,
	data_completa DATE NOT NULL,
	ano INT NOT NULL,
	mes INT NOT NULL,
	nome_mes VARCHAR(20),
	trimestre INT NOT NULL,
	dia_semana VARCHAR(20),
	final_semana BOOLEAN
);

CREATE TABLE dim_clientes(
	sk_cliente SERIAL PRIMARY KEY,
	id_natural_cliente VARCHAR(50) UNIQUE,
	nome_cliente VARCHAR(100),
	email_cliente VARCHAR(100),
	empresa_cliente VARCHAR(100),
	segmento_empresa VARCHAR(50),
	pais VARCHAR(50)
);


CREATE TABLE dim_planos (
	sk_plano SERIAL PRIMARY KEY,
	nome_plano VARCHAR(50), -- BASIC, PRO, ENTERPRISE
	valor_mensal NUMERIC(10, 2),
	limite_usuarios INT
);

CREATE TABLE fato_assinaturas(
	sk_assinatura SERIAL PRIMARY KEY,
	fk_cliente INT REFERENCES dim_clientes(sk_cliente),
	fk_plano INT REFERENCES dim_planos(sk_plano),
	fk_data_inicio INT REFERENCES dim_tempo(sk_tempo),
	valor_contrato NUMERIC(10, 2),
	status_assinatura VARCHAR(20)
)