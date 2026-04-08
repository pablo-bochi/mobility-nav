# mobility-nav

Projeto de estudo e implementação incremental de um app web de mobilidade, inspirado em funcionalidades centrais de produtos como Google Maps e Waze.

## Objetivo do projeto

Construir, passo a passo, um **web app de mobilidade** com foco inicial em:

- mapa interativo
- busca de lugares
- definição de origem e destino
- cálculo de rotas
- ETA (tempo estimado de chegada)

O objetivo **não é** começar com todas as complexidades de um app real de navegação, mas sim construir uma base sólida e evolutiva, entendendo os principais componentes técnicos e arquiteturais.

---

# Escopo inicial do MVP

## O que entra no MVP

- exibir mapa interativo no navegador
- permitir busca de lugares/endereço
- permitir definir origem e destino
- calcular rota entre dois pontos
- exibir distância e ETA
- desenhar a rota no mapa

A ideia é manter o projeto **o mais simples possível no início**, para focar no domínio principal: **mapa + busca + rota + ETA**.

---

# Visão geral da arquitetura inicial

A arquitetura inicial será separada em **frontend** e **backend**, mas ambos viverão no **mesmo repositório**.

Essa abordagem busca o melhor dos dois mundos:

- simplicidade de organização em um único repo
- separação clara de responsabilidades
- possibilidade de evoluir o frontend e o backend de forma independente
- facilidade para substituir o frontend no futuro, se necessário

## Frontend
Responsável por:

- renderizar o mapa
- permitir interação do usuário
- buscar lugares
- capturar origem e destino
- chamar a API do backend
- desenhar a rota recebida
- mostrar distância e ETA

## Backend
Responsável por:

- expor endpoints HTTP para o frontend
- integrar busca geográfica
- integrar com a engine de roteamento
- retornar rota, distância e duração
- servir como camada de abstração e composição de dados
- preparar o sistema para futuras evoluções

## Banco de dados
Responsável por:

- armazenar dados geoespaciais próprios, se necessário
- suportar consultas espaciais futuras
- permitir evolução para features mais avançadas

---

# Stack escolhida

## Frontend

### Dash
Framework Python para construção de aplicações web interativas.

**Por que essa escolha?**
- permite criar o frontend em Python
- mantém o projeto simples
- funciona bem no mesmo repositório do backend
- possui boa abordagem reativa baseada em callbacks
- é uma escolha mais adequada que Streamlit para um app centrado em mapa

### dash-leaflet
Biblioteca para integrar mapas Leaflet ao Dash.

**Por que essa escolha?**
- o mapa é o centro da experiência do projeto
- facilita trabalhar com marcadores, linhas, camadas e eventos de mapa
- combina melhor com o caso de uso do que soluções mais focadas em dashboards genéricos

### Leaflet
Biblioteca JavaScript amplamente usada para mapas interativos na web.

No projeto, ela aparecerá de forma indireta através do `dash-leaflet`.

---

## Backend

### FastAPI
Framework Python moderno para criação de APIs.

**Por que essa escolha?**
- rápido para desenvolver
- boa integração com Pydantic
- tipagem clara
- documentação automática
- ótimo para projeto de estudo e arquitetura
- permite manter o núcleo da lógica desacoplado do frontend

### Pydantic
Usado para validação e serialização de dados na API.

---

## Banco de dados

### PostgreSQL
Banco relacional principal do projeto.

### PostGIS
Extensão geoespacial do PostgreSQL.

**Por que usar PostGIS desde cedo?**
Mesmo que o MVP inicial não dependa totalmente dele, ele prepara o projeto para:
- consultas por proximidade
- filtros geográficos
- armazenamento de pontos, linhas e polígonos
- futuras evoluções como incidentes, POIs próprios e zonas geográficas

---

## Cache / apoio

### Redis
Inicialmente opcional, mas recomendado para:
- cache de buscas frequentes
- cache de rotas frequentes
- dados temporários e aceleração futura

---

## Roteamento

### OSRM
Open Source Routing Machine.

É uma engine open source de roteamento construída sobre dados do OpenStreetMap.

**Por que usar OSRM?**
- é focado em rotas
- é rápido
- pode ser executado localmente
- é excelente para aprender a arquitetura de um app de mobilidade

---

## Busca geográfica inicial

### Nominatim
Serviço de busca geográfica e geocodificação baseado em OpenStreetMap.

**Por que usar no início?**
- resolve a busca de lugares/endereço sem precisarmos construir isso do zero
- é ótimo para o MVP
- pode ser substituído ou complementado no futuro

---

## Base cartográfica

### OSM (OpenStreetMap)
Base de dados aberta de mapas do mundo.

Usaremos o OSM como origem principal de dados geográficos para:
- engine de rotas
- busca geográfica
- futuras evoluções do projeto

---

## Infra local

### Docker Compose
Para subir facilmente:
- frontend Dash
- backend FastAPI
- postgres/postgis
- redis
- osrm

---

# Definições importantes

## OSM (OpenStreetMap)
É uma base de dados geográfica aberta e colaborativa, como uma “Wikipedia dos mapas”.

Ela contém:
- ruas
- avenidas
- cidades
- bairros
- pontos de interesse
- geometrias viárias

No projeto, o OSM será a base de dados geográficos utilizada pela engine de roteamento e pela busca inicial.

---

## OSRM
Significa **Open Source Routing Machine**.

É uma engine que pega dados do OSM e calcula:
- rotas
- distância
- duração estimada
- geometrias da rota

Ela funciona como um serviço especializado em resolver o problema de roteamento.

---

## Nominatim
É um serviço de geocodificação e busca sobre dados do OpenStreetMap.

Ele permite:
- buscar lugares por nome
- transformar texto em coordenadas
- transformar coordenadas em endereços em alguns cenários

No projeto, ele será usado inicialmente para a funcionalidade de busca de lugares.

---

## POI
Significa **Point of Interest**.

São locais relevantes para o usuário, como:
- restaurantes
- postos
- aeroportos
- escolas
- farmácias
- shoppings

No futuro, a busca por lugares pode ser tratada parcialmente como busca por POIs.

---

## ETA
Significa **Estimated Time of Arrival**.

É o tempo estimado para chegar ao destino.

No MVP, o ETA será inicialmente baseado no retorno da engine de roteamento, sem considerar trânsito em tempo real.

---

# Arquitetura inicial proposta

## Componentes

### Frontend Dash
Responsável por:
- exibir mapa
- permitir busca
- selecionar origem/destino
- chamar a API
- desenhar rota
- exibir ETA e distância
- organizar a experiência do usuário no navegador

### Backend FastAPI
Responsável por:
- receber requisições do frontend
- consultar Nominatim para busca
- consultar OSRM para rotas
- padronizar respostas
- aplicar cache quando necessário
- preparar a base para futuras evoluções

### OSRM
Responsável por:
- calcular rota
- retornar geometria da rota
- retornar distância
- retornar duração

### Nominatim
Responsável por:
- resolver busca textual de lugares/endereço
- retornar sugestões com latitude e longitude

### PostgreSQL + PostGIS
Responsável por:
- suportar futuras consultas geoespaciais
- armazenar entidades próprias do projeto, se necessário

### Redis
Responsável por:
- cache de buscas e rotas
- apoio à performance

---

# Fluxo principal do MVP

## Busca de lugares
1. usuário digita um lugar
2. frontend chama endpoint de busca do backend
3. backend consulta o Nominatim
4. backend retorna sugestões padronizadas ao frontend
5. frontend exibe sugestões

## Cálculo de rota
1. usuário define origem
2. usuário define destino
3. frontend chama endpoint de rota no backend
4. backend consulta o OSRM
5. backend recebe rota, distância e duração
6. backend devolve resposta padronizada
7. frontend desenha a rota no mapa
8. frontend mostra ETA e distância

---

# Organização inicial sugerida do repositório

## Estrutura sugerida

```text
mobility-nav/
├── frontend_dash/
├── backend_fastapi/
├── infra/
├── docs/
├── README.md
└── .gitignore