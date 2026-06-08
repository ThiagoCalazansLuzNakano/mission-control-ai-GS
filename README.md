# 🛰️ AgroSat Mission Control AI

**Global Solution 2026.1 — FIAP**  
**Trilha 1 — AgroSat: Sensoriamento Agrícola**

---

## 👥 Grupo

| Nome | RM |
|------|----|
| *(Integrante 1)* | RM XXXXX |
| *(Integrante 2)* | RM XXXXX |
| *(Integrante 3)* | RM XXXXX |

---

## 🎯 Proposta de Valor

O **AgroSat Mission Control AI** é um sistema de monitoramento operacional inteligente para satélites de sensoriamento agrícola. Ele recebe dados simulados de telemetria do **AgroSat-1** — um satélite multiespectral em órbita baixa —, detecta anomalias via lógica Python e analisa o estado da missão em linguagem natural usando IA generativa.

### Personas atendidas
| Persona | O que precisa |
|---------|--------------|
| 🔧 Engenheiro de Operações | Diagnósticos técnicos e ações imediatas |
| 🌾 Produtor Rural | Saber se os dados NDVI da sua área estão confiáveis |
| 📋 Analista de Seguro Agrícola | Verificar se a qualidade dos dados compromete laudos de sinistro |

---

## 🛰️ Parâmetros Monitorados

| Parâmetro | Faixa Normal | Alerta | Crítico |
|-----------|-------------|--------|---------|
| NDVI Sensor Health | 85–100% | < 85% | < 60% |
| Temperatura do Payload | -10°C a 40°C | > 40°C / < -10°C | > 55°C / < -20°C |
| Storage a Bordo | 0–80% | > 80% | > 90% |
| Janela de Downlink | 8–30 min | < 8 min | < 3 min |
| Estabilidade de Atitude | 92–100% | < 92% | < 80% |

---

## ⚙️ Stack Técnica

| Componente | Tecnologia |
|------------|-----------|
| Linguagem | Python 3.10+ |
| IA Generativa | Ollama Cloud API — `gpt-oss:120b` |
| SDK API | `openai` (compatível com Ollama Cloud) |
| Interface CLI | `rich` |
| Config | `python-dotenv` |

---

## 📁 Estrutura do Projeto

```
mission-control-ai/
├── main.py                  # Entrada do sistema
├── banner_ascii.py          # Banner ASCII do sistema
├── requirements.txt         # Dependências
├── .env.example             # Template das variáveis de ambiente
├── .env                     # Chave Ollama (não commitar)
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── telemetria.py        # Geração de dados simulados
│   ├── alertas.py           # Thresholds e regras de decisão
│   ├── engine.py            # Motor de análise com IA
│   └── ui.py                # Interface CLI Rich
├── prompts/
│   └── system_prompt.md     # System prompt da IA
└── data/
    └── cenarios.json        # Cenários pré-definidos para teste
```

---

## 🚀 Como Executar

### 1. Instalar dependências
```bash
pip install -r requirements.txt
```

### 2. Configurar a chave da API
```bash
cp .env.example .env
# Edite o .env e insira sua OLLAMA_API_KEY
```

### 3. Executar o sistema
```bash
python main.py
```

---

## 🔄 Fluxo do Sistema

```
[Usuário escolhe cenário]
        ↓
[telemetria.py] → Gera dados simulados do AgroSat-1
        ↓
[alertas.py]    → Avalia thresholds com lógica Python (if/elif/else)
        ↓
[engine.py]     → Monta contexto + chama Ollama Cloud API
        ↓
[ui.py]         → Exibe telemetria, alertas e análise da IA via Rich CLI
        ↓
[Loop Chat]     → Usuário pode fazer perguntas livres à IA
```

---

## 🌾 Impacto Terrestre

Cada alerta detectado é traduzido para impacto real no setor agrícola brasileiro:

- **NDVI degradado** → índices de vegetação imprecisos para produtores e analistas de seguro
- **Temperatura crítica** → risco de dano permanente ao sensor óptico; interrupção do serviço
- **Storage cheio** → perda de imagens de talhões; lacunas em plataformas como Climate FieldView
- **Downlink reduzido** → atraso na entrega de dados para decisões de plantio e colheita
- **Instabilidade de atitude** → imagens com motion blur; mapas de precisão comprometidos
