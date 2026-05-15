# 🔧 Como Estender o Pulsar Explorer

Este documento explica como você pode adicionar novas funcionalidades ao frontend.

---

## 📋 Estrutura do Projeto

```
├── app.py                   # Backend Flask
│   ├── @app.route('/')      → Serve index.html
│   ├── @app.route('/api/stats')
│   ├── @app.route('/api/feature-stats')
│   ├── @app.route('/api/models-performance')
│   └── @app.route('/api/dataset-info')
│
├── index.html               # Frontend tudo-em-um
│   ├── <head>              → Meta, imports CDN
│   ├── <style>             → Todo CSS embutido
│   ├── <body>              → HTML structure
│   └── <script>            → Todo JavaScript embutido
│
└── run.sh                   # Script de inicialização
```

---

## 🎨 Adicionar Nova Seção de Dados

### 1. Criar novo Endpoint na API

Edite `app.py` e adicione uma função:

```python
@app.route('/api/new-data')
def get_new_data():
    """Retorna dados para a nova seção"""
    return jsonify({
        'metric1': 123,
        'metric2': 456,
        'metric3': 789
    })
```

### 2. Criar função para carregar dados no Frontend

Em `index.html`, dentro da função `loadData()`:

```javascript
async function loadData() {
    try {
        const newData = await fetch('/api/new-data').then(r => r.json());
        displayNewSection(newData);
        // ... resto do código
    }
}
```

### 3. Criar função para exibir

Dentro de `<script>`:

```javascript
function displayNewSection(data) {
    const container = document.querySelector('#new-section-container');
    container.innerHTML = `
        <div class="card">
            <h2>📊 Nova Seção</h2>
            <div class="stat-value">${data.metric1}</div>
            <div class="stat-label">Métrica 1</div>
        </div>
    `;
}
```

### 4. Adicionar container no HTML

Em `<main>`:

```html
<section class="card" id="new-section-container">
    <h2>📊 Nova Seção</h2>
    <div class="loader"></div>
</section>
```

---

## 📈 Adicionar Novo Gráfico

### Usando Chart.js

```javascript
// No final da função createCharts()
const myCtx = document.getElementById('myChart').getContext('2d');
new Chart(myCtx, {
    type: 'bar',  // bar, line, pie, etc
    data: {
        labels: ['Label 1', 'Label 2'],
        datasets: [{
            label: 'Dataset',
            data: [10, 20],
            backgroundColor: '#00ff88',
            borderColor: '#00d4ff',
            borderWidth: 2
        }]
    },
    options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
            legend: {
                labels: { color: '#e0e7ff' }
            }
        }
    }
});
```

No HTML:

```html
<div class="chart-container">
    <canvas id="myChart"></canvas>
</div>
```

---

## 🎨 Customizar Cores

No bloco `:root` do `<style>`:

```css
:root {
    --color-primary: #00d4ff;      /* Azul Ciano */
    --color-secondary: #ff00ff;    /* Magenta */
    --color-accent: #00ff88;       /* Verde Neon */
    --color-dark: #0a0e27;         /* Azul Escuro */
    --color-darker: #050812;       /* Mais Escuro */
    --color-light: #e0e7ff;        /* Branco Frio */
    --color-muted: #6366f1;        /* Roxo Suave */
}
```

Use em qualquer lugar:

```css
.my-element {
    color: var(--color-primary);
    background: var(--color-dark);
}
```

---

## ✨ Adicionar Animação

### Keyframes

No `<style>`:

```css
@keyframes my-animation {
    0% {
        opacity: 0;
        transform: translateY(10px);
    }
    100% {
        opacity: 1;
        transform: translateY(0);
    }
}

.animated {
    animation: my-animation 0.5s ease-out;
}
```

### Com GSAP

No `<script>`:

```javascript
// Animar um elemento
gsap.to('#myElement', {
    duration: 1,
    opacity: 1,
    y: -20,
    ease: 'power2.out'
});

// Timeline
const tl = gsap.timeline();
tl.to('#el1', { duration: 0.5, opacity: 1 })
  .to('#el2', { duration: 0.5, opacity: 1 });
```

---

## 🎯 Adicionar Interatividade

### Eventos de Mouse

```javascript
const card = document.querySelector('.card');

card.addEventListener('mouseenter', () => {
    console.log('Mouse entrou');
});

card.addEventListener('click', () => {
    console.log('Clicado');
});
```

### Mudança de Abas

Exemplo (já implementado):

```javascript
function switchTab(tabName) {
    // Esconder todas as abas
    document.querySelectorAll('.tab-content').forEach(el => {
        el.classList.remove('active');
    });
    
    // Mostrar a nova aba
    document.getElementById(tabName).classList.add('active');
}
```

---

## 🔄 Conectar a Dados em Tempo Real

Se você quiser atualizar dados periodicamente:

```javascript
// Atualizar a cada 5 segundos
setInterval(async () => {
    const data = await fetch('/api/stats').then(r => r.json());
    updateDisplay(data);
}, 5000);
```

---

## 🚀 Adicionar Novos Modelos

### Backend (app.py)

```python
@app.route('/api/models-performance')
def get_models_performance():
    return jsonify({
        'pmc': { /* ... */ },
        'rbf': { /* ... */ },
        'seu-modelo': {
            'name': 'Seu Modelo',
            'accuracy': 0.95,
            'precision': 0.92,
            'recall': 0.88,
            'f1': 0.90,
            'color': '#ff6b6b'
        }
    })
```

### Frontend (index.html)

A função `displayModels()` já iterará automaticamente sobre todos os modelos no JSON!

---

## 📱 Responsive Design

### Adicionar Breakpoints

```css
@media (max-width: 768px) {
    .seu-elemento {
        font-size: 1rem;
        padding: 1rem;
    }
}

@media (max-width: 480px) {
    .seu-elemento {
        font-size: 0.875rem;
        padding: 0.5rem;
    }
}
```

---

## 🐛 Debugging

### Console do Navegador

Pressione **F12** e vá para a aba **Console** para:
- Ver erros
- Testar JavaScript
- Ver logs de rede

### Inspecionar Elementos

F12 → **Elements** → Clique para inspecionar elemento

### Network

F12 → **Network** → Veja requisições HTTP

---

## 📚 Recursos Úteis

### Chart.js
- Docs: https://www.chartjs.org/docs/latest/
- Tipos: Bar, Line, Pie, Doughnut, Radar, etc

### GSAP
- Docs: https://greensock.com/gsap/
- Animações avançadas

### CSS Variáveis
```css
:root {
    --my-var: value;
}

.element {
    color: var(--my-var);
}
```

---

## 💡 Exemplos de Extensões Possíveis

1. **Previsões em Tempo Real**
   - Adicione input para usuário enviar um novo sinal
   - Chame a rede neural no backend
   - Mostre resultado com animação

2. **Análise Comparativa**
   - Gráfico comparando treino vs teste
   - Matriz de confusão visual
   - Curva ROC

3. **Sistema de Abas**
   - Modelos diferentes
   - Diferentes datasets
   - Comparação histórica

4. **Exportar Dados**
   - Botão para baixar CSV
   - Gerar PDF com relatório
   - Screenshot do dashboard

5. **Modo Escuro/Claro**
   - Toggle no header
   - Salvar preferência em localStorage
   - Diferentes paletas de cores

6. **Detalhes de Features**
   - Click em uma feature para ver distribuição
   - Histogramas individuais
   - Correlação entre features

---

## 🚀 Deploy

Para colocar em produção:

1. Use **Gunicorn** ao invés de Flask dev:
```bash
pip install gunicorn
gunicorn app:app
```

2. Configure **CORS** adequadamente:
```python
CORS(app, resources={r"/api/*": {"origins": "seu-dominio.com"}})
```

3. Use variáveis de ambiente:
```python
import os
DEBUG = os.getenv('DEBUG', 'False') == 'True'
```

---

## 📞 Dúvidas Frequentes

**Como adicionar mais dados?**
- Estenda o CSV com mais linhas
- A interface carregar os dados automaticamente

**Como mudar a porta?**
- Em `app.py`: `app.run(port=8000)`
- Em `run.sh`: `PORT=8000`

**Como usar de forma remota?**
- Use `app.run(host='0.0.0.0')`
- Configure firewall
- Acesse de outro computador: `http://seu-ip:5001`

---

**Boa sorte na customização! 🚀**
