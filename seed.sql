INSERT INTO funcionario (id,nome) VALUES
	 (1,'Victor Souza');
INSERT INTO web_site (id,name,url) VALUES
	 (1,'TJSP ESAJ','https://esaj.tjsp.jus.br/cpopg/open.do');
INSERT INTO lote (id,funcionario_id,prazo,tipo,prioridade,data_criacao) VALUES
	 (2,1,'2025-07-21 00:00:00-03',NULL,1,'2025-07-20 15:32:36.557053-03');
INSERT INTO servico_pesquisa (id,lote_id,web_site_id,tipo,resultado) VALUES
	 (2,2,1,'nome_parte',NULL),
	 (3,2,1,'nome_parte',NULL),
	 (4,2,1,'documento',NULL),
	 (5,2,1,'documento',NULL);
INSERT INTO pesquisa (id,servico_pesquisa_id,nome,cpf,rg,uf_rg,nascimento,uf_nascimento,nome_mae,data_entrada,data_conclusao,anexo) VALUES
	 (2,2,'Victor Souza','57163334001',NULL,NULL,NULL,NULL,NULL,'2025-07-20 15:41:05.278905-03',NULL,NULL),
	 (3,3,'Italo Rocha','57163334001',NULL,NULL,NULL,NULL,NULL,'2025-07-20 15:41:05.283308-03',NULL,NULL),
	 (4,4,'Jose Silva','57163334001',NULL,NULL,NULL,NULL,NULL,'2025-07-20 15:41:05.286466-03',NULL,NULL),
	 (5,5,'Maria Gomes','57163334001',NULL,NULL,NULL,NULL,NULL,'2025-07-20 15:41:05.288918-03',NULL,NULL);
