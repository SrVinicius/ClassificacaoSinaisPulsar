# 🌌 Pulsar Explorer - Frontend Interativo

Um dashboard moderno e interativo para visualização dos resultados do classificador de pulsares HTRU2, com tema galáxia e animações.

## 🚀 Início Rápido

### 1. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o Servidor

```bash
python app.py
```

O servidor será iniciado em `http://localhost:5000`

### 3. Abrir no Navegador

Acesse: **http://localhost:5000**

## ✨ Características

### Design Temático 🎨
- **Tema Galáxia**: Cores cósmicas (azul ciano, magenta, verde neon)
- **Animações**: Pulsação de estrelas, efeito de linha de varredura, transições suaves
- **Ícone Pulsar**: Animação 3D interativa no cabeçalho
- **Fundo Dinâmico**: Estrelas cintilantes criadas proceduralmente

### Interatividade 🖱️
- **Cards Responsivos**: Hover effects com glow e transformações
- **Abas Dinâmicas**: Navegação entre diferentes visualizações
- **Gráficos Interativos**: Chart.js para visualizações de dados
- **Animações GSAP**: Transições suaves de valores e progressões

### Seções Principais 📊

1. **Overview Stats**
   - Total de amostras de treino/teste
   - Número de features e classes
   - Distribuição de classes com barras de progresso animadas

2. **Desempenho dos Modelos**
   - Cards comparativos entre MLP e RBF
   - Métricas: Acurácia, Precisão, Recall, F1-Score
   - Cores distintivas por modelo

3. **Análise de Features**
   - Grid com descrição de cada feature
   - Estatísticas (média, desvio padrão, valores nulos)
   - Gráfico doughnut da distribuição de classes

4. **Comparação de Métricas**
   - Gráfico radar comparando os dois modelos
   - Visualização fácil de diferenças de performance

## 🎯 Endpoints da API

- `GET /` - Página principal
- `GET /api/stats` - Estatísticas gerais do dataset
- `GET /api/feature-stats` - Estatísticas por feature
- `GET /api/models-performance` - Métricas dos modelos
- `GET /api/dataset-info` - Informações detalhadas do dataset

## 🛠️ Stack Tecnológico

- **Backend**: Flask + Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript Vanilla
- **Gráficos**: Chart.js 3.9.1
- **Animações**: GSAP 3.12.2
- **Data**: NumPy, Pandas

## 📱 Responsividade

O frontend é totalmente responsivo:
- Desktop: Layout de múltiplas colunas
- Tablet: Grid adaptativo
- Mobile: Coluna única com navegação simplificada

## 🎨 Paleta de Cores

```css
--color-primary:    #00d4ff  (Azul Ciano)
--color-secondary:  #ff00ff  (Magenta)
--color-accent:     #00ff88  (Verde Neon)
--color-dark:       #0a0e27  (Azul Escuro)
--color-light:      #e0e7ff  (Branco Frio)
--color-muted:      #6366f1  (Roxo Suave)
```

## 🌟 Características Especiais

- **Glow Effects**: Brilhos neon no hover
- **Scan Lines**: Efeito CRT de linhas de varredura
- **Pulse Animation**: Ícone do pulsar com pulsação contínua
- **Float Animation**: Elementos flutuantes no ícone
- **Backdrop Filter**: Efeito glassmorphism nos cards

## 📝 Notas

- A aplicação carrega dados automaticamente ao abrir
- Se houver erro de conexão, é exibida uma mensagem de erro
- Todos os valores são animados suavemente ao carregar
- A interface se adapta automaticamente a diferentes tamanhos de tela

## 🎬 Como Funciona

1. O servidor Flask carrega os dados do CSV
2. O frontend faz requisições AJAX aos endpoints da API
3. Os dados são processados e animados com GSAP
4. Chart.js renderiza os gráficos interativos
5. A interface é totalmente responsiva e acessível

---

**Desenvolvido para Prova 3 - Laboratório de Inteligência Artificial** 🌌
