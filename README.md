# AgroSat Mission Control AI

**Global Solution**  
**Trilha 1 — AgroSat: Sensoriamento Agrícola**

---

##  Grupo

| Nome            | RM        |
|-----------------|-----------|
| *Thiago nakano* | RM 569151 |
| *Leticia okano* | RM 571988 |
| *Enzo furtado*  | RM 570824 |

---

##  O que o projeto faz

O *AgroSat Mission Control AI* é um sistema de monitoramento operacional de satélite de sensoriamento agrícola que recebe dados simulados de telemetria do AgroSat-1, detecta anomalias em tempo real via lógica Python e gera diagnósticos em linguagem natural usando IA generativa (Ollama Cloud). A IA é integrada diretamente ao fluxo de análise: após cada leitura de telemetria, o modelo gpt-oss:120b recebe os dados brutos e os alertas detectados pelo código Python e produz uma análise contextualizada com nível de risco, impacto terrestre e ações recomendadas — além de estar disponível em modo chat para perguntas livres do operador.

### Personas atendidas
| Persona | O que precisa |
|---------|--------------|
|  Engenheiro de Operações | Diagnósticos técnicos e ações imediatas |
|  Produtor Rural | Saber se os dados NDVI da sua área estão confiáveis |
|  Analista de Seguro Agrícola | Verificar se a qualidade dos dados compromete laudos de sinistro |

---

##  Tecnologias utilizadas

- Python 3.10+
- Ollama Cloud API (modelo gpt-oss:120b)
- Bibliotecas: openai, python-dotenv, rich

---

## System Prompt

Arquivo completo em prompts/system_prompt.md

Você apoia três personas terrestres:
1. Engenheiro de Operações — diagnósticos técnicos e ações imediatas.
2. Produtor Rural — saber se os dados NDVI da sua área estão confiáveis.
3. Analista de Seguro Agrícola — verificar se os dados comprometem laudos.

Parâmetros monitorados e faixas normais:
- NDVI Sensor Health  : 85–100%      | alerta < 85%  | crítico < 60%
- Temperatura Payload : -10°C a 40°C | alerta > 40°C | crítico > 55°C
- Storage a Bordo     : 0–80%        | alerta > 80%  | crítico > 90%
- Janela de Downlink  : 8–30 min     | alerta < 8min | crítico < 3min
- Estab. de Atitude   : 92–100%      | alerta < 92%  | crítico < 80%

Diretrizes:
- Cite sempre o parâmetro anômalo e o valor atual.
- Explique o impacto concreto para o setor agrícola.
- Indique o nível de urgência: NORMAL, ALERTA ou CRÍTICO.
- Sugira uma ação recomendada clara e objetiva.
- Responda sempre em português brasileiro.
---

## Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar a chave da API
```bash
cp .env .env
# Edite o .env e insira sua OLLAMA_API_KEY
```

### 3. Entrar no cmd e abrir o projeto, após isso colocar
```bash
.venv\Scripts\activate
# após dar enter adicionar:
python main.py
```

---

##  Cenários de teste demonstrados
Na teoria:
1. Operação normal — todos os parâmetros dentro da faixa operacional
2. Sobrecarga térmica — temperatura do payload acima de 55°C; risco de dano permanente ao sensor óptico
3. Storage crítico + downlink reduzido — buffer acima de 90% com janela de transmissão abaixo de 3 min; risco de perda de imagens
4. Falha múltipla — NDVI degradado abaixo de 60%, instabilidade de atitude abaixo de 80% e storage crítico simultaneamente

---

## Limitações conhecidas

- Os dados de telemetria são simulados (gerados por random.uniform) e não provêm de um satélite real
- A análise da IA depende de conexão com a internet para acessar a Ollama Cloud API

