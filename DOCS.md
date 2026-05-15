# 📚 Documentação - Pulsar Explorer

## 🚀 Início Rápido

| Documento | Conteúdo | Para Quem |
|-----------|----------|----------|
| **[LEIA-ME.md](LEIA-ME.md)** | Como iniciar em 3 passos | Todos (comece aqui!) |
| **[PREVIEW.txt](PREVIEW.txt)** | Preview ASCII da interface | Curiosos sobre o visual |

---

## 📖 Documentação Completa

| Documento | Conteúdo | Para Quem |
|-----------|----------|----------|
| **[GUIA_VISUAL.md](GUIA_VISUAL.md)** | Guia detalhado com layout e seções | Usuários finais, investigadores |
| **[SUMARIO.md](SUMARIO.md)** | Sumário técnico, endpoints, stack | Desenvolvedores, arquitetos |
| **[README_FRONTEND.md](README_FRONTEND.md)** | Documentação técnica do frontend | Devs frontend, contribuidores |

---

## 🔧 Para Desenvolvedores

| Documento | Conteúdo | Para Quem |
|-----------|----------|----------|
| **[EXTENSOES.md](EXTENSOES.md)** | Como estender, adicionar features | Desenvolvedores, customização |

---

## 📁 Estrutura de Arquivos

```
📌 DOCUMENTAÇÃO (Leia nesta ordem)
├── LEIA-ME.md                  ← ⭐ Comece aqui (início rápido)
├── PREVIEW.txt                 ← Visualização ASCII
├── GUIA_VISUAL.md              ← Guia completo com layout
├── SUMARIO.md                  ← Sumário técnico
├── README_FRONTEND.md          ← Docs técnicas
├── EXTENSOES.md                ← Como estender
└── DOCS.md                     ← Este arquivo

🔴 CÓDIGO
├── app.py                      ← Backend Flask (APIs)
├── index.html                  ← Frontend (25KB puro)
├── requirements.txt            ← Dependências Python
└── run.sh                      ← Script automático

📊 DADOS
├── data_train/                 ← 12.528 amostras de treino
│   └── pulsar_data_train.csv
├── data_test/                  ← 5.370 amostras de teste
│   └── pulsar_data_test.csv
└── pulsar_pmc_rbf.py          ← Código original do projeto
```

---

## 🎯 Roteiros de Uso

### Cenário 1: "Quero Ver o Dashboard em 30 Segundos"
1. Abra [LEIA-ME.md](LEIA-ME.md)
2. Execute `./run.sh`
3. Pronto! Dashboard abre automaticamente

### Cenário 2: "Quero Entender o Visual"
1. Leia [PREVIEW.txt](PREVIEW.txt) para ver como fica
2. Abra [GUIA_VISUAL.md](GUIA_VISUAL.md) para detalhes
3. Veja cada seção em detalhe

### Cenário 3: "Quero Estender o Projeto"
1. Leia [SUMARIO.md](SUMARIO.md) para entender a arquitetura
2. Consulte [EXTENSOES.md](EXTENSOES.md) para padrões
3. Veja exemplos de código em `app.py` e `index.html`

### Cenário 4: "Quero Entender a Implementação"
1. Comece por [SUMARIO.md](SUMARIO.md) - visão geral
2. Leia [README_FRONTEND.md](README_FRONTEND.md) - stack técnico
3. Explore o código em `app.py` (backend) e `index.html` (frontend)

---

## 💡 Perguntas Frequentes

### "Por onde começo?"
→ **[LEIA-ME.md](LEIA-ME.md)** - Instruções de 30 segundos

### "Como fica a interface?"
→ **[PREVIEW.txt](PREVIEW.txt)** + **[GUIA_VISUAL.md](GUIA_VISUAL.md)**

### "Como funciona tecnicamente?"
→ **[SUMARIO.md](SUMARIO.md)** + **[README_FRONTEND.md](README_FRONTEND.md)**

### "Como adiciono novas features?"
→ **[EXTENSOES.md](EXTENSOES.md)** + código em `app.py` e `index.html`

### "Qual é a porta?"
→ **5001** (veja [LEIA-ME.md](LEIA-ME.md))

### "Quais dados estão sendo mostrados?"
→ **[GUIA_VISUAL.md](GUIA_VISUAL.md)** seção "Principais Seções"

---

## 🎨 Quick Reference

### Como Iniciar
```bash
./run.sh
# ou manualmente:
python3 app.py
```

### URL
```
http://localhost:5001
```

### Endpoints da API
```
GET /api/stats
GET /api/feature-stats
GET /api/models-performance
GET /api/dataset-info
```

### Cores Temáticas
```
🔵 Azul Ciano:    #00d4ff
🟣 Magenta:       #ff00ff
🟢 Verde Neon:    #00ff88
⚫ Azul Escuro:   #0a0e27
```

### Performance dos Modelos
```
MLP: 97.7% acurácia, 86.1% F1
RBF: 96.0% acurácia, 78.1% F1
```

---

## 📊 Dados do Projeto

### Dataset HTRU2
- **Amostras**: 12.528 treino + 5.370 teste
- **Features**: 8 características estatísticas
- **Classes**: Binária (Pulsar vs Não-Pulsar)
- **Imbalance**: 90.8% / 9.2%

### Modelos
1. **MLP (Perceptron Multicamadas)**
   - Acurácia: 97.7%
   - F1-Score: 86.1%
   - Melhor em: precisão geral

2. **RBF (Rede Radial Básica)**
   - Acurácia: 96.0%
   - F1-Score: 78.1%
   - Melhor em: recall

---

## 🛠️ Troubleshooting

### "Página em branco"
→ Veja [LEIA-ME.md](LEIA-ME.md) seção "Troubleshooting"

### "Porta 5001 em uso"
→ Execute: `pkill -f "python.*app.py"`

### "Módulos não encontrados"
→ Execute: `pip install -r requirements.txt`

### "Gráficos não aparecem"
→ Abra DevTools (F12) → Console e verifique erros

---

## 📞 Suporte

1. **Problemas de inicialização**: [LEIA-ME.md](LEIA-ME.md) → Troubleshooting
2. **Perguntas sobre o visual**: [GUIA_VISUAL.md](GUIA_VISUAL.md)
3. **Perguntas técnicas**: [SUMARIO.md](SUMARIO.md)
4. **Como estender**: [EXTENSOES.md](EXTENSOES.md)

---

## 🎓 Informações do Projeto

- **Disciplina**: Prova 3 - Laboratório de Inteligência Artificial
- **Dataset**: HTRU2 (Pulsar Classification)
- **Modelos**: MLP e RBF (NumPy puro, sem sklearn)
- **Frontend**: HTML5/CSS3/JS moderno com tema galáxia

---

## ✅ Checklist de Leitura

Recomendamos ler na seguinte ordem:

- [ ] **[LEIA-ME.md](LEIA-ME.md)** (5 min) - Entender como usar
- [ ] **[PREVIEW.txt](PREVIEW.txt)** (5 min) - Ver como fica
- [ ] **[GUIA_VISUAL.md](GUIA_VISUAL.md)** (10 min) - Entender as seções
- [ ] **[SUMARIO.md](SUMARIO.md)** (10 min) - Arquitetura geral
- [ ] **[EXTENSOES.md](EXTENSOES.md)** (opcional) - Para customização

---

## 🚀 Próximos Passos

1. **Começar**: Execute `./run.sh`
2. **Explorar**: Navegue pelo dashboard
3. **Entender**: Leia a documentação apropriada
4. **Customizar**: Siga [EXTENSOES.md](EXTENSOES.md) se desejar

---

## 📈 Recursos

- **Chart.js**: https://www.chartjs.org
- **GSAP**: https://greensock.com/gsap
- **Flask**: https://flask.palletsprojects.com
- **NumPy/Pandas**: https://numpy.org / https://pandas.pydata.org

---

## 🌟 Destaques

✨ **25KB** de HTML/CSS/JS puro (sem build tools)  
✨ **100 estrelas** cintilantes no fundo  
✨ **4 gráficos** interativos  
✨ **100% responsivo** (desktop, tablet, mobile)  
✨ **Tema galáxia** imersivo  
✨ **APIs REST** bem estruturadas  

---

**Status**: ✅ **COMPLETO E DOCUMENTADO**

*Bem-vindo ao Pulsar Explorer! 🌌✨*
