# 🌌 Pulsar Explorer - Frontend Interativo

Um **dashboard moderno e imersivo** para visualizar resultados do classificador de pulsares HTRU2 com tema galáxia.

## 🚀 Como Usar

### ⚡ Forma Mais Rápida (Linux/Mac):

```bash
./run.sh
```

Ou manualmente:

```bash
python3 app.py
# Abra o navegador em: http://localhost:5001
```

### Windows:

```bash
pip install -r requirements.txt
python app.py
```

Então acesse: **http://localhost:5001**

---

## ✨ O Que Você Vai Ver

### 🎨 Interface Galáxia
- Tema cósmico com cores neon (azul, magenta, verde)
- Animações fluidas de estrelas piscantes
- Efeito de ícone pulsar pulsando continuamente
- Cards com brilho neon ao passar o mouse

### 📊 Painéis de Dados
1. **Overview Stats** - 12.528 amostras de treino, distribuição de classes
2. **Desempenho dos Modelos** - MLP vs RBF (acurácia, precisão, recall, F1)
3. **Análise de Features** - 8 características do dataset HTRU2
4. **Gráficos Interativos** - Radar chart e doughnut chart

### 🎯 Resultados Principais

#### 🟢 MLP (Perceptron Multicamadas)
- **Acurácia**: 97.7%
- **Precisão**: 90.4%
- **Recall**: 82.1%
- **F1-Score**: 86.1%

#### 🔴 RBF (Rede Radial Básica)
- **Acurácia**: 96.0%
- **Precisão**: 74.8%
- **Recall**: 81.7%
- **F1-Score**: 78.1%

---

## 📁 Arquivos Criados

```
├── app.py                  # Backend Flask com APIs
├── index.html              # Frontend com todo CSS/JS
├── run.sh                  # Script de inicialização automática
├── requirements.txt        # Dependências Python
├── GUIA_VISUAL.md         # Guia detalhado de uso
└── README_FRONTEND.md     # Documentação técnica
```

---

## 🛠️ Dependências

```
Flask==2.3.3
Flask-CORS==4.0.0
numpy>=1.24.0
pandas>=1.5.0
```

Já estão definidas em `requirements.txt` e serão instaladas automaticamente se usar `./run.sh`.

---

## 🌟 Características Especiais

✅ **100% Interativo** - Gráficos com hover, abas dinâmicas, animações  
✅ **Responsivo** - Funciona em desktop, tablet e mobile  
✅ **Tema Galáxia** - Cores cósmicas neon com efeitos luminosos  
✅ **Sem Dependências Pesadas** - Usa HTML5/CSS3/JS puro + Chart.js  
✅ **APIs RESTful** - Backend Flask serve dados em JSON  

---

## 📡 Endpoints da API

```
GET  /                    → Página principal (HTML)
GET  /api/stats          → Estatísticas do dataset
GET  /api/feature-stats  → Estatísticas por feature
GET  /api/models-performance → Métricas dos modelos
GET  /api/dataset-info   → Informações detalhadas
```

---

## 🎨 Paleta de Cores

```
Azul Ciano:    #00d4ff (Primária)
Magenta:       #ff00ff (RBF)
Verde Neon:    #00ff88 (MLP)
Azul Escuro:   #0a0e27 (Fundo)
Roxo Suave:    #6366f1 (Textos)
```

---

## 🐛 Problemas Comuns

**Porta 5001 em uso?**
```bash
pkill -f "python.*app.py"
```

**Módulos não encontrados?**
```bash
pip install -r requirements.txt
```

**Gráficos em branco?**
- Verifique a conexão de internet (Chart.js usa CDN)
- Abra DevTools (F12) e verifique console para erros

---

## 📚 Documentação Completa

Para um guia detalhado com screenshots e exemplos, veja:
- **GUIA_VISUAL.md** - Layout, seções, e como usar
- **README_FRONTEND.md** - Documentação técnica completa

---

## 🌌 Tecnologias

- **Backend**: Flask + Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Gráficos**: Chart.js 3.9.1
- **Animações**: GSAP 3.12.2
- **Data**: NumPy, Pandas

---

## 📝 Notas

- Implementado **sem sklearn/TensorFlow/PyTorch** (conforme requerimento)
- Usa apenas **NumPy e Pandas** para processamento
- Dataset HTRU2 com 12.528 amostras rotuladas
- Problema de classificação binária: Pulsar vs Não-Pulsar

---

## 🎓 Sobre o Projeto

Prova 3 - Laboratório de Inteligência Artificial  
Classificação de Pulsares usando MLP e RBF implementados do zero

---

**Bem-vindo ao Pulsar Explorer! 🌌✨**

Explore visualmente os dados astronômicos e veja como redes neurais
conseguem distinguir sinais de pulsares em meio ao ruído cósmico!
