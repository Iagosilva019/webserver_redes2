# Projeto de Teste de Servidores Web

Este projeto contém dois servidores web (sequencial e concorrente) e um cliente que realiza experimentos de requisições HTTP para medir latência e status. O ambiente é configurado usando Docker Compose.

## Estrutura do Projeto

- **servidor_sequencial**: Servidor que processa requisições de forma sequencial.
- **servidor_concorrente**: Servidor que processa requisições de forma concorrente (multithread ou async).
- **cliente**: Script `run_experiment.py` que envia requisições para os servidores e salva resultados em CSV.

---

## Requisitos

- Docker >= 20.10  
- Docker Compose >= 1.29  
- Python 3.12.3 no container (já incluído na imagem)

---

## Instalação

1. Clone o repositório:

```git clone github.com/Iagosilva019/webserver_redes2```
 ```cd webserver_redes2```


2. Construir a imagem docker:
   
```sudo docker-compose up --build```

 **Isso irá criar as imagens para:**
- servidor_sequencial
- servidor_concorrente
- cliente

## Execução
1. Executar os servidores

Os servidores podem ser executados em contêineres separados:

 **Servidor sequencial:**
 
```sudo docker-compose up -d servidor_sequencial```

 **Servidor concorrente:**
 
```sudo docker-compose up -d servidor_concorrente```

2. Executar o cliente

O cliente envia requisições para os servidores e gera arquivos de logs CSV.

 **Para servidor sequencial:**
 
``` sudo docker-compose run --rm cliente 89.34.0.2```

 **Para servidor concorrente:**
 
``` sudo docker-compose run --rm cliente 89.34.0.3```



# Para verificar os logs:

```sudo docker-compose logs -f servidor_sequencial```

```sudo docker-compose logs -f servidor_concorrente```

# Comparação dos resultados
Após ter executado o cliente para os dois servidores.

1. Entre na pasta cliente:

```cd cliente/```

2. Execute o script para gerar o gráfico:

```python3 comparacao.py```





