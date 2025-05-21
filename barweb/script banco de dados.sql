CREATE DATABASE IF NOT EXISTS gerencia_bar;

USE gerencia_bar;

CREATE TABLE IF NOT EXISTS mesa (
  id_mesa INT NOT NULL AUTO_INCREMENT,
  num_mesa INT NULL,
  PRIMARY KEY (id_mesa)
);

CREATE TABLE IF NOT EXISTS produto (
  cod INT NOT NULL AUTO_INCREMENT,
  nome VARCHAR(20) NULL,
  valor INT NULL,
  PRIMARY KEY (cod)
);

CREATE TABLE IF NOT EXISTS item_mesa (
  id_item INT NOT NULL AUTO_INCREMENT,
  id_mesa INT NOT NULL,
  cod_produto INT NOT NULL,
  quantidade INT NOT NULL,
  PRIMARY KEY (id_item),
  FOREIGN KEY (id_mesa) REFERENCES mesa(id_mesa),
  FOREIGN KEY (cod_produto) REFERENCES produto(cod)
);

CREATE TABLE Venda (
    id_venda INT AUTO_INCREMENT PRIMARY KEY,
    id_mesa INT,
    valor_total INT,
    data_venda DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_mesa) REFERENCES Mesa(id_mesa)
);



INSERT INTO mesa (num_mesa) VALUES (1),(2),(3),(4),(5);

INSERT INTO produto (cod, nome, valor) VALUES (1, 'kaiser', 5);
INSERT INTO produto (cod, nome, valor) VALUES (2, 'skol', 6);
INSERT INTO produto (cod, nome, valor) VALUES (3, 'dose 51', 10);
INSERT INTO produto (cod, nome, valor) VALUES (4, 'dose de 88', 12);
INSERT INTO produto (cod, nome, valor) VALUES (5, 'marmita', 8);

select * from item_mesa;
SELECT * FROM Venda;
