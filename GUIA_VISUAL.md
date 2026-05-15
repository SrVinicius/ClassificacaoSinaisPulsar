# 🌌 Pulsar Explorer - Guia de Uso

## ⚡ Inicialização Rápida

### Opção 1: Script Automático (Recomendado)

```bash
cd /Users/viniciusferreira/Prova3Lab_IA_PMC_ou_RBF
./run.sh
```

O script irá:
- ✅ Verificar dependências Python
- ✅ Instalar Flask e Flask-CORS se necessário
- ✅ Iniciar o servidor
- ✅ Abrir automaticamente no navegador

### Opção 2: Manual

```bash
cd /Users/viniciusferreira/Prova3Lab_IA_PMC_ou_RBF
pip install -r requirements.txt
python3 app.py
```

Então acesse: **http://localhost:5001**

---

## 🎨 Layout da Interface

```
┌─────────────────────────────────────────────────────────────┐
│ 🌌 PULSAR EXPLORER                                          │
│ Classificação Inteligente de Sinais Astronômicos             │
└─────────────────────────────────────────────────────────────┘

┌─────────────────┬─────────────────┬──────────────────────────┐
│ 📊 Overview     │ ⚙️ Configuração │ 🎯 Distribuição          │
│                 │                 │                          │
│ Train: 12,528   │ Features: 8     │ Classe 0: 90.8%         │
│ Test: 5,370     │ Classes: 2      │ Classe 1: 9.2%          │
└─────────────────┴─────────────────┴──────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🚀 DESEMPENHO DOS MODELOS                                   │
├─────────────────────────────┬───────────────────────────────┤
│ 🟢 MLP (PMC)                │ 🔴 RBF                        │
│                             │                               │
│ Acurácia:   97.7%          │ Acurácia:   96.0%            │
│ Precisão:   90.4%          │ Precisão:   74.8%            │
│ Recall:     82.1%          │ Recall:     81.7%            │
│ F1-Score:   86.1%          │ F1-Score:   78.1%            │
└─────────────────────────────┴───────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 🔬 ANÁLISE DE FEATURES                                      │
│ [Visão Geral] [Estatísticas]                               │
│                                                             │
│ Grid com 8 features do dataset HTRU2                       │
└─────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────┐
│ 📈 GRÁFICOS INTERATIVOS                                     │
│                                                             │
│ - Radar Chart: Comparação de Métricas                      │
│ - Doughnut Chart: Distribuição de Classes                  │
└─────────────────────────────────────────────────────────────┘
```

---

## 🎯 Principais Seções

### 1️⃣ Dataset Overview
- **Amostras de Treino**: 12,528 sinais
- **Amostras de Teste**: 5,370 sinais
- **Total de Features**: 8 características por sinal
- **Classes**: Binária (Pulsar vs Não-Pulsar)

### 2️⃣ Distribuição de Classes
Visualização com barra de progresso animada:
- **Classe 0 (Não-Pulsar)**: 90.8% - Sinal verde
- **Classe 1 (Pulsar)**: 9.2% - Sinal magenta

*Nota: Dataset desbalanceado, refletindo a rareidade de pulsares*

### 3️⃣ Desempenho dos Modelos
Comparação lado-a-lado de dois classificadores:

#### 🟢 MLP (Perceptron Multicamadas)
- **Melhor em**: Acurácia geral (97.7%)
- **Força**: Alta precisão (90.4%)
- **Cor**: Verde Neon (#00ff88)

#### 🔴 RBF (Rede de Função Radial Básica)
- **Melhor em**: Recall (81.7%)
- **Força**: Mais balanço Precisão/Recall
- **Cor**: Magenta (#ff00ff)

### 4️⃣ Análise de Features

As 8 features do dataset HTRU2:

1. **media_perfil** - Média do perfil integrado
2. **desvio_perfil** - Desvio padrão do perfil
3. **curtose_perfil** - Curtose da distribuição
4. **assimetria_perfil** - Assimetria da distribuição
5. **media_dm_snr** - Média da medida de dispersão vs ruído
6. **desvio_dm_snr** - Desvio padrão da dispersão
7. **curtose_dm_snr** - Curtose da dispersão
8. **assimetria_dm_snr** - Assimetria da dispersão

Cada feature mostra:
- μ (média)
- σ (desvio padrão)
- Número de valores nulos

### 5️⃣ Gráficos Interativos

#### Radar Chart
Comparação visual em tempo real de:
- Acurácia
- Precisão
- Recall
- F1-Score

*Hover sobre os pontos para ver valores exatos*

#### Doughnut Chart
Proporção de classes no dataset

---

## ✨ Recursos Visuais

### Animações
- ⭐ **Estrelas Cintilantes**: Fundo dinâmico com 100 estrelas
- 🔴 **Ícone Pulsar**: Pulsação contínua no topo
- 💫 **Hover Effects**: Brilho neon ao passar o mouse
- 📊 **Valores Animados**: Transições suaves de números
- 📈 **Barras de Progresso**: Preenchimento animado

### Cores Temáticas
```
🔵 Primária:   Azul Ciano (#00d4ff)    - Elementos principais
🟣 Secundária: Magenta (#ff00ff)       - Destaque RBF
🟢 Destaque:   Verde Neon (#00ff88)    - Destaque MLP
⚫ Dark:       Azul Escuro (#0a0e27)   - Fundo
🟡 Muted:      Roxo Suave (#6366f1)    - Textos secundários
```

### Efeitos de Design
- 🎆 **Glow Effects**: Brilho neon ao hover
- 📺 **Scan Lines**: Efeito CRT de varredura
- 🔮 **Glassmorphism**: Fundo desfocado (backdrop-filter)
- 🌟 **Text Shadow**: Textos com sombra luminosa

---

## 🎮 Interatividade

### Cards Responsivos
- Hover: Cor muda, brilho aumenta, levanta-se
- Clique: Alguns cards têm links e ações futuras
- Toque (Mobile): Efeitos otimizados para touchscreen

### Abas Dinâmicas
Na seção de Features, alterne entre:
- **Visão Geral**: Grid com descrição de features
- **Estatísticas**: Gráfico doughnut da distribuição

Clique nos botões de aba para trocar visualizações.

### Gráficos
- **Interativos**: Hover para ver valores
- **Responsivos**: Redimensionam com a janela
- **Animados**: Preenchem progressivamente ao carregar

---

## 📱 Responsividade

### Desktop (1024px+)
- Layout de múltiplas colunas
- Cards lado a lado
- Gráficos em tamanho completo

### Tablet (768px - 1023px)
- Grid adaptativo
- 2 colunas onde possível
- Fonte ligeiramente reduzida

### Mobile (< 768px)
- Coluna única
- Cards empilhados
- Botões ampliados para toque
- Sem scroll horizontal

---

## 🛠️ Troubleshooting

### Porta 5001 em Uso
```bash
# Matar processos na porta
lsof -ti:5001 | xargs kill -9

# Ou usar porta diferente
python3 app.py --port 5002
```

### Dependências Não Instaladas
```bash
pip install Flask Flask-CORS numpy pandas
```

### Página em Branco
1. Abra o DevTools (F12)
2. Verifique a aba "Console" para erros
3. Verifique se o servidor está rodando: `curl http://localhost:5001`

### Gráficos Não Aparecem
- Certifique-se que a biblioteca Chart.js foi carregada
- Verifique a conexão de internet (CDN)
- Limpe o cache do navegador (Ctrl+Shift+Del)

---

## 📊 Dados Técnicos

### Dataset HTRU2
- **Nome Completo**: High Time Resolution Universe Pulsar Data Set
- **Fonte**: UCI Machine Learning Repository
- **Total de Amostras**: 12,528 (treino) + 5,370 (teste)
- **Features**: 8 características estatísticas
- **Target**: Classificação Binária (Pulsar/Não-Pulsar)
- **Desbalanceamento**: 91% / 9%

### Features
- Obtidas de análise espectral e temporal de sinais de rádio
- Normalizadas e padronizadas
- 3 features com valores ausentes pequenos (<15%)

---

## 🌟 Dicas de Uso

1. **Explore os Gráficos**: Passe o mouse sobre os pontos para detalhes
2. **Compare Modelos**: Use o radar chart para análise rápida
3. **Mobile-First**: Teste em diferentes dispositivos
4. **Full Screen**: Pressione F11 para melhor imersão visual
5. **Dev Tools**: Abra (F12) para inspecionar elementos

---

## 📞 Suporte

Se encontrar problemas:

1. Verifique se Python 3.7+ está instalado: `python3 --version`
2. Confirme que o servidor está rodando: `curl http://localhost:5001/api/stats`
3. Veja os logs: `cat server.log`

---

**Desenvolvido com ❤️ para Prova 3 - Laboratório de Inteligência Artificial**

🌌 Uma experiência visual imersiva no universo dos pulsares! 🌌
