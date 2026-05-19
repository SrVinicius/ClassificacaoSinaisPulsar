"""
=======================================================================
Prova 3 — Laboratório de Inteligência Artificial
Classificação de Estrelas Pulsar (HTRU2)
Modelos: PMC (Perceptron Multicamadas) e Rede RBF
=======================================================================
RESTRIÇÃO: Somente NumPy e Pandas — sem scikit-learn, TensorFlow ou PyTorch.
Todos os algoritmos (pré-processamento, modelos, métricas) implementados
do zero usando apenas operações matriciais com NumPy.

NOTA SOBRE OS DADOS:
  O arquivo de teste fornecido (pulsar_data_test.csv) não contém rótulos
  (target_class = NaN em todas as linhas). Portanto, utilizamos o arquivo
  de treino (pulsar_data_train.csv, 12.528 amostras rotuladas) e o
  dividimos manualmente em 80% treino / 20% teste para avaliação.
=======================================================================
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os
import time


# =======================================================================
# MÓDULO 1 — PRÉ-PROCESSAMENTO DE DADOS
# =======================================================================

def carregar_dataset(caminho_arquivo: str) -> pd.DataFrame:
    """
    Carrega o dataset HTRU2 a partir de um CSV e renomeia as colunas.
    Imprime um resumo de valores ausentes por coluna.
    """
    df = pd.read_csv(caminho_arquivo)

    # Substituir os nomes longos originais por nomes mais legíveis
    nomes_colunas = [
        'media_perfil',
        'desvio_perfil',
        'curtose_perfil',
        'assimetria_perfil',
        'media_dm_snr',
        'desvio_dm_snr',
        'curtose_dm_snr',
        'assimetria_dm_snr',
        'classe',
    ]
    df.columns = nomes_colunas

    print(f"  Dataset carregado: {df.shape[0]} amostras, {df.shape[1] - 1} features")
    print("  Valores ausentes por coluna (antes da imputação):")
    for col, n_nulos in df.isnull().sum().items():
        if n_nulos > 0:
            print(f"    {col:<25}: {n_nulos}")

    return df


def preprocessar(
    df: pd.DataFrame,
    proporcao_treino: float = 0.8,
    semente: int = 42,
) -> tuple:
    """
    Pipeline de pré-processamento completo (sem sklearn):

    1. Embaralhamento com NumPy (np.random.permutation).
    2. Divisão treino/teste via indexação manual.
    3. Imputação de NaN com a MEDIANA do treino (sem vazamento de dados).
    4. Padronização Z-score: (X - média_treino) / desvio_treino.

    Retorna: X_treino, y_treino, X_teste, y_teste (np.ndarray float64)
    """
    colunas_x = df.columns[:-1].tolist()
    coluna_y  = df.columns[-1]

    # --- Passo 1: Embaralhar com NumPy ---
    np.random.seed(semente)
    idx_emb = np.random.permutation(len(df))
    df_emb  = df.iloc[idx_emb].reset_index(drop=True)

    # --- Passo 2: Divisão manual treino/teste ---
    n_total  = len(df_emb)
    n_treino = int(n_total * proporcao_treino)

    df_treino = df_emb.iloc[:n_treino].copy()
    df_teste  = df_emb.iloc[n_treino:].copy()

    # --- Passo 3: Imputação com mediana do TREINO ---
    medianas_treino = df_treino[colunas_x].median()
    df_treino[colunas_x] = df_treino[colunas_x].fillna(medianas_treino)
    df_teste[colunas_x]  = df_teste[colunas_x].fillna(medianas_treino)

    # Converter para arrays NumPy
    X_treino = df_treino[colunas_x].values.astype(np.float64)
    y_treino = df_treino[coluna_y].values.astype(np.float64)
    X_teste  = df_teste[colunas_x].values.astype(np.float64)
    y_teste  = df_teste[coluna_y].values.astype(np.float64)

    # --- Passo 4: Z-score com estatísticas APENAS do treino ---
    media_treino  = X_treino.mean(axis=0)
    desvio_treino = X_treino.std(axis=0)
    # Evitar divisão por zero em features com variância nula
    desvio_treino[desvio_treino == 0.0] = 1.0

    X_treino = (X_treino - media_treino) / desvio_treino
    X_teste  = (X_teste  - media_treino) / desvio_treino

    return X_treino, y_treino, X_teste, y_teste


# =======================================================================
# MÓDULO 2 — MÉTRICAS DE AVALIAÇÃO (IMPLEMENTADAS DO ZERO)
# =======================================================================

def calcular_matriz_confusao(y_real: np.ndarray, y_pred: np.ndarray) -> np.ndarray:
    """
    Calcula a Matriz de Confusão 2x2 para classificação binária.

    Layout:
        [[TN, FP],
         [FN, TP]]

    Onde:
      TN = Verdadeiro Negativo   FP = Falso Positivo
      FN = Falso Negativo        TP = Verdadeiro Positivo
    """
    y_real = y_real.astype(int)
    y_pred = y_pred.astype(int)

    tn = int(np.sum((y_real == 0) & (y_pred == 0)))
    fp = int(np.sum((y_real == 0) & (y_pred == 1)))
    fn = int(np.sum((y_real == 1) & (y_pred == 0)))
    tp = int(np.sum((y_real == 1) & (y_pred == 1)))

    return np.array([[tn, fp], [fn, tp]], dtype=int)


def calcular_metricas(
    y_real: np.ndarray,
    y_pred: np.ndarray,
    nome_modelo: str = "Modelo",
) -> dict:
    """
    Calcula Acurácia, Precisão, Revocação (Recall) e F1-Score
    a partir dos vetores de rótulos reais e preditos.
    Todas as fórmulas implementadas manualmente — sem sklearn.
    """
    mc = calcular_matriz_confusao(y_real, y_pred)
    tn, fp, fn, tp = mc[0, 0], mc[0, 1], mc[1, 0], mc[1, 1]
    total = tn + fp + fn + tp

    acuracia  = (tp + tn) / total   if total > 0              else 0.0
    precisao  = tp / (tp + fp)      if (tp + fp) > 0          else 0.0
    revocacao = tp / (tp + fn)      if (tp + fn) > 0          else 0.0
    f1_score  = (2.0 * precisao * revocacao) / (precisao + revocacao) \
                if (precisao + revocacao) > 0 else 0.0

    return {
        'nome':            nome_modelo,
        'matriz_confusao': mc,
        'acuracia':        acuracia,
        'precisao':        precisao,
        'revocacao':       revocacao,
        'f1_score':        f1_score,
    }


def exibir_metricas(metricas: dict) -> None:
    """Formata e imprime todas as métricas de um modelo no terminal."""
    mc  = metricas['matriz_confusao']
    sep = "-" * 50

    print(f"\n  {sep}")
    print(f"  Resultados: {metricas['nome']}")
    print(f"  {sep}")
    print(f"  Matriz de Confusão:")
    print(f"               Predito 0   Predito 1")
    print(f"  Real 0:      {mc[0, 0]:>9d}   {mc[0, 1]:>9d}")
    print(f"  Real 1:      {mc[1, 0]:>9d}   {mc[1, 1]:>9d}")
    print(f"  {sep}")
    print(f"  Acuracia:   {metricas['acuracia']:.4f}")
    print(f"  Precisao:   {metricas['precisao']:.4f}")
    print(f"  Revocacao:  {metricas['revocacao']:.4f}")
    print(f"  F1-Score:   {metricas['f1_score']:.4f}")
    print(f"  {sep}")


# =======================================================================
# MÓDULO 3 — PMC: PERCEPTRON MULTICAMADAS
# =======================================================================

class PerceptronMulticamadas:
    """
    PMC / MLP implementado do zero com NumPy.

    Arquitetura fixa:
        Entrada(8) → Oculta(n_ocultos, ReLU) → Saida(1, Sigmoid)

    Inicialização de pesos:
        W1: He initialization  — ideal para ReLU
        W2: Xavier/Glorot      — ideal para Sigmoid

    Treinamento:
        Mini-batch Gradient Descent com Retropropagação (backpropagation)
        Perda: Binary Cross-Entropy (BCE)
    """

    def __init__(
        self,
        n_entrada:       int   = 8,
        n_ocultos:       int   = 16,
        taxa_aprendizado: float = 0.01,
        epocas:          int   = 200,
        tamanho_lote:    int   = 64,
        semente:         int   = 42,
    ):
        self.n_entrada        = n_entrada
        self.n_ocultos        = n_ocultos
        self.taxa_aprendizado = taxa_aprendizado
        self.epocas           = epocas
        self.tamanho_lote     = tamanho_lote
        self.historico_perda  = []

        np.random.seed(semente)

        # Camada 1 (Entrada → Oculta): inicialização He — fator sqrt(2/n_entrada)
        self.W1 = np.random.randn(n_entrada, n_ocultos) * np.sqrt(2.0 / n_entrada)
        self.b1 = np.zeros((1, n_ocultos))

        # Camada 2 (Oculta → Saída): inicialização Xavier — fator sqrt(1/n_ocultos)
        self.W2 = np.random.randn(n_ocultos, 1) * np.sqrt(1.0 / n_ocultos)
        self.b2 = np.zeros((1, 1))

    # -------------------------------------------------------------------
    # Funções de Ativação e Derivadas
    # -------------------------------------------------------------------

    @staticmethod
    def _relu(Z: np.ndarray) -> np.ndarray:
        """ReLU: f(z) = max(0, z)"""
        return np.maximum(0.0, Z)

    @staticmethod
    def _derivada_relu(Z: np.ndarray) -> np.ndarray:
        """Derivada da ReLU: f'(z) = 1 se z > 0, senão 0"""
        return (Z > 0.0).astype(np.float64)

    @staticmethod
    def _sigmoid(Z: np.ndarray) -> np.ndarray:
        """
        Sigmoid com clipping numérico para evitar overflow em np.exp.
        f(z) = 1 / (1 + e^{-z})
        """
        Z_clip = np.clip(Z, -500.0, 500.0)
        return 1.0 / (1.0 + np.exp(-Z_clip))

    # -------------------------------------------------------------------
    # Propagação Direta (Forward Pass)
    # -------------------------------------------------------------------

    def _forward(self, X: np.ndarray) -> tuple:
        """
        Calcula as ativações de todas as camadas.

        Retorna a saída final A2 (probabilidades) e um cache com os
        valores intermediários necessários para a retropropagação.
        """
        # Camada oculta: pré-ativação Z1, ativação A1 via ReLU
        Z1 = X @ self.W1 + self.b1     # shape: (m, n_ocultos)
        A1 = self._relu(Z1)             # shape: (m, n_ocultos)

        # Camada de saída: pré-ativação Z2, ativação A2 via Sigmoid
        Z2 = A1 @ self.W2 + self.b2    # shape: (m, 1)
        A2 = self._sigmoid(Z2)          # shape: (m, 1)

        cache = (Z1, A1, Z2, A2)
        return A2, cache

    # -------------------------------------------------------------------
    # Função de Perda — Binary Cross-Entropy
    # -------------------------------------------------------------------

    @staticmethod
    def _bce_loss(y_real: np.ndarray, y_pred: np.ndarray) -> float:
        """
        BCE: L = -mean[ y*log(p) + (1-y)*log(1-p) ]

        y_pred é achatado para 1D antes do cálculo para evitar broadcasting
        incorreto quando A2 tem shape (m, 1) e y_real tem shape (m,).
        Sem o flatten, NumPy expande (m,) × (m,1) → (m,m), corrompendo a perda.
        """
        eps          = 1e-8
        y_pred_flat  = np.clip(y_pred.flatten(), eps, 1.0 - eps)
        return float(
            -np.mean(y_real * np.log(y_pred_flat) + (1.0 - y_real) * np.log(1.0 - y_pred_flat))
        )

    # -------------------------------------------------------------------
    # Retropropagação (Backpropagation)
    # -------------------------------------------------------------------

    def _backward(
        self,
        X: np.ndarray,
        y: np.ndarray,
        cache: tuple,
    ) -> tuple:
        """
        Calcula todos os gradientes via regra da cadeia.

        Para BCE + Sigmoid na última camada, a derivada combinada é:
            dL/dZ2 = A2 - y   (resultado analítico simplificado)
        """
        Z1, A1, Z2, A2 = cache
        m = X.shape[0]  # tamanho do mini-lote

        # --- Gradientes da camada de saída ---
        dZ2 = A2 - y.reshape(-1, 1)             # (m, 1)
        dW2 = (A1.T @ dZ2) / m                  # (n_ocultos, 1)
        db2 = dZ2.mean(axis=0, keepdims=True)    # (1, 1)

        # --- Retropropagar o erro para a camada oculta ---
        dA1 = dZ2 @ self.W2.T                   # (m, n_ocultos)
        # Multiplicar elemento a elemento pela derivada da ReLU
        dZ1 = dA1 * self._derivada_relu(Z1)     # (m, n_ocultos)
        dW1 = (X.T @ dZ1) / m                   # (n_entrada, n_ocultos)
        db1 = dZ1.mean(axis=0, keepdims=True)   # (1, n_ocultos)

        return dW1, db1, dW2, db2

    # -------------------------------------------------------------------
    # Treinamento
    # -------------------------------------------------------------------

    def treinar(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Treina o PMC com Mini-batch Gradient Descent.

        A cada época:
          1. Embaralha os dados aleatoriamente.
          2. Divide em mini-lotes de tamanho `tamanho_lote`.
          3. Para cada lote: forward → calcula perda → backward → atualiza pesos.
          4. Registra a perda média da época em `historico_perda`.
        """
        m       = X.shape[0]
        n_lotes = int(np.ceil(m / self.tamanho_lote))

        print(
            f"  Iniciando: {self.epocas} epocas | "
            f"lote={self.tamanho_lote} | lr={self.taxa_aprendizado}"
        )

        for epoca in range(1, self.epocas + 1):
            # Embaralhar os índices para garantir aleatoriedade a cada época
            idx   = np.random.permutation(m)
            X_emb = X[idx]
            y_emb = y[idx]

            perdas_lote = []

            for k in range(n_lotes):
                inicio  = k * self.tamanho_lote
                fim     = min(inicio + self.tamanho_lote, m)
                X_lote  = X_emb[inicio:fim]
                y_lote  = y_emb[inicio:fim]

                # Propagação direta
                A2, cache = self._forward(X_lote)

                # Perda do lote
                perdas_lote.append(self._bce_loss(y_lote, A2))

                # Retropropagação e atualização dos pesos
                dW1, db1, dW2, db2 = self._backward(X_lote, y_lote, cache)
                self.W1 -= self.taxa_aprendizado * dW1
                self.b1 -= self.taxa_aprendizado * db1
                self.W2 -= self.taxa_aprendizado * dW2
                self.b2 -= self.taxa_aprendizado * db2

            # Perda média da época
            perda_media = float(np.mean(perdas_lote))
            self.historico_perda.append(perda_media)

            if epoca % 20 == 0 or epoca == 1:
                print(f"    Epoca {epoca:3d}/{self.epocas}  |  BCE: {perda_media:.5f}")

    # -------------------------------------------------------------------
    # Predição
    # -------------------------------------------------------------------

    def prever(self, X: np.ndarray) -> tuple:
        """
        Realiza predições no conjunto X.

        Retorna:
            classes:        vetor de inteiros {0, 1} com limiar 0.5
            probabilidades: vetor de floats com P(classe=1|x)
        """
        A2, _ = self._forward(X)
        probabilidades = A2.flatten()
        classes        = (probabilidades >= 0.5).astype(int)
        return classes, probabilidades


# =======================================================================
# MÓDULO 4 — REDE DE FUNÇÃO DE BASE RADIAL (RBF)
# =======================================================================

class RedeRBF:
    """
    Rede RBF implementada do zero com NumPy.

    Arquitetura:
        Entrada(8) → Oculta(K centros, Gaussiana) → Saida(1, linear)

    Funções de base:
        phi_j(x) = exp(-gamma * ||x - c_j||^2)

    Centros c_j:
        K amostras aleatórias do conjunto de treino (sem K-Means).

    Parâmetro gamma:
        Calculado automaticamente via: gamma = 1 / (2 * sigma^2)
        onde sigma = d_max / sqrt(2K)  e  d_max = maior dist. entre centros.

    Pesos de saída:
        Estimados via Pseudoinversa de Moore-Penrose (np.linalg.pinv):
            [W; b] = pinv([Phi | 1]) @ y
    """

    def __init__(
        self,
        k_centros: int   = 100,
        gamma:     float = None,
        semente:   int   = 42,
    ):
        self.k_centros        = k_centros
        self.gamma            = gamma       # None → calculado automaticamente
        self.semente          = semente
        self.centros          = None
        self.pesos_saida      = None
        self.bias_saida       = None
        self._gamma_efetivo   = None        # valor de gamma realmente usado

    # -------------------------------------------------------------------
    # Métodos de Inicialização
    # -------------------------------------------------------------------

    def _selecionar_centros(self, X: np.ndarray) -> np.ndarray:
        """
        Seleciona K centros aleatoriamente do conjunto de treino, sem reposição.
        Estratégia deliberadamente simples (sem K-Means) conforme especificado.
        """
        np.random.seed(self.semente)
        idx = np.random.choice(X.shape[0], self.k_centros, replace=False)
        return X[idx].copy()

    def _calcular_gamma(self, centros: np.ndarray) -> float:
        """
        Calcula gamma automaticamente usando a distância máxima entre centros.

        Fórmula:
            d_max  = max_{i,j} ||c_i - c_j||
            sigma  = d_max / sqrt(2 * K)
            gamma  = 1 / (2 * sigma^2)

        Usa broadcast matricial para calcular todas as distâncias de forma eficiente:
            ||c_i - c_j||^2 = ||c_i||^2 + ||c_j||^2 - 2 * c_i · c_j
        """
        normas_quad = np.sum(centros ** 2, axis=1)    # (K,)
        # Matriz de distâncias quadráticas: (K, K)
        dist_quad = (
            normas_quad[:, np.newaxis]
            + normas_quad[np.newaxis, :]
            - 2.0 * (centros @ centros.T)
        )
        # Corrigir possíveis erros numéricos de ponto flutuante
        dist_quad = np.maximum(dist_quad, 0.0)

        d_max = float(np.sqrt(np.max(dist_quad)))

        if d_max < 1e-10:
            return 1.0  # fallback: centros coincidentes

        sigma = d_max / np.sqrt(2.0 * self.k_centros)
        return 1.0 / (2.0 * sigma ** 2)

    # -------------------------------------------------------------------
    # Ativação RBF Gaussiana
    # -------------------------------------------------------------------

    def _ativar(self, X: np.ndarray) -> np.ndarray:
        """
        Calcula a Design Matrix Phi para o conjunto X.

        Phi[i, j] = exp(-gamma * ||x_i - c_j||^2)

        Implementado com broadcasting 3D para eficiência vetorial:
            diff[i, j, :] = x_i - c_j
        via: X[:, None, :] - centros[None, :, :]  →  (n, K, d)
        """
        # diff: (n, K, d) — diferença de cada amostra para cada centro
        diff     = X[:, np.newaxis, :] - self.centros[np.newaxis, :, :]
        dist_quad = np.sum(diff ** 2, axis=2)              # (n, K)
        return np.exp(-self._gamma_efetivo * dist_quad)    # (n, K)

    # -------------------------------------------------------------------
    # Treinamento
    # -------------------------------------------------------------------

    def treinar(self, X: np.ndarray, y: np.ndarray) -> None:
        """
        Treina a rede RBF em três etapas:

        1. Seleciona K centros aleatoriamente do treino.
        2. Determina o parâmetro gamma (automático ou manual).
        3. Constrói a Design Matrix aumentada Phi = [Phi | 1]
           e resolve os pesos via pseudoinversa de Moore-Penrose:
               [W; b] = pinv(Phi_aumentada) @ y
        """
        # Etapa 1: centros aleatórios
        self.centros = self._selecionar_centros(X)

        # Etapa 2: gamma
        self._gamma_efetivo = self.gamma if self.gamma is not None \
                              else self._calcular_gamma(self.centros)

        print(f"  Centros selecionados: {self.k_centros}")
        print(f"  Gamma (gamma):        {self._gamma_efetivo:.6f}")

        # Etapa 3: Design Matrix Phi de dimensão (n_treino, K)
        Phi = self._ativar(X)

        # Aumentar com coluna de bias: (n_treino, K+1)
        Phi_aug = np.hstack([Phi, np.ones((Phi.shape[0], 1))])

        # Resolver sistema linear via pseudoinversa:
        # [W; b] = pinv(Phi_aug) @ y    →    dimensão (K+1,)
        pesos = np.linalg.pinv(Phi_aug) @ y

        self.pesos_saida = pesos[:-1]   # pesos das K unidades RBF: (K,)
        self.bias_saida  = pesos[-1]    # escalar de bias

    # -------------------------------------------------------------------
    # Predição
    # -------------------------------------------------------------------

    @staticmethod
    def _sigmoid(z: np.ndarray) -> np.ndarray:
        """Sigmoid para converter saída linear em probabilidade."""
        z_clip = np.clip(z, -500.0, 500.0)
        return 1.0 / (1.0 + np.exp(-z_clip))

    def prever(self, X: np.ndarray) -> tuple:
        """
        Realiza predições com a RBF treinada.

        A pseudoinversa minimiza ||Phi @ W - y||², portanto a saída linear
        já aproxima os alvos em {0, 1}. O limiar de 0.5 é aplicado
        DIRETAMENTE na saída linear — NÃO usar sigmoid antes do limiar,
        pois sigmoid(0) = 0.5, colocando amostras classe-0 (saída ≈ 0)
        exatamente na fronteira e causando falsos positivos em massa.

        A probabilidade reportada usa sigmoid apenas para ter escala [0,1].

        Retorna:
            classes:        vetor de inteiros {0, 1}
            probabilidades: vetor de floats com P(classe=1|x) (via sigmoid)
        """
        Phi           = self._ativar(X)
        saida_linear  = Phi @ self.pesos_saida + self.bias_saida   # (n,)

        # Decisão: limiar 0.5 na saída linear (escala dos alvos {0,1})
        classes        = (saida_linear >= 0.5).astype(int)

        # Probabilidade reportada: sigmoid para escala interpretável
        probabilidades = self._sigmoid(saida_linear)               # (n,)

        return classes, probabilidades


# =======================================================================
# MÓDULO 5 — VISUALIZAÇÃO
# =======================================================================

def plotar_convergencia_pmc(
    historico_perda: list,
    caminho_saida:   str = None,
) -> None:
    """
    Plota a curva de convergência da BCE Loss durante o treinamento do PMC.
    Destaca o ponto de perda mínima com um marcador vermelho.
    """
    epocas = np.arange(1, len(historico_perda) + 1)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Curva principal
    ax.plot(epocas, historico_perda,
            color='royalblue', linewidth=2, label='Perda BCE (treino)', zorder=3)

    # Área preenchida abaixo da curva (auxiliar visual)
    ax.fill_between(epocas, historico_perda, alpha=0.12, color='royalblue')

    # Marcar a época com menor perda
    idx_min   = int(np.argmin(historico_perda))
    perda_min = historico_perda[idx_min]
    ax.scatter(idx_min + 1, perda_min, color='crimson', s=80, zorder=5,
               label=f'Minimo: {perda_min:.5f} (epoca {idx_min + 1})')

    ax.set_xlabel('Epoca', fontsize=12)
    ax.set_ylabel('Binary Cross-Entropy Loss', fontsize=12)
    ax.set_title(
        'Curva de Convergencia — PMC (Perceptron Multicamadas)\n'
        'Dataset: Predicting Pulsar Star (HTRU2)',
        fontsize=13,
    )
    ax.legend(fontsize=11)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlim(1, len(historico_perda))

    plt.tight_layout()

    if caminho_saida:
        plt.savefig(caminho_saida, dpi=150, bbox_inches='tight')
        print(f"  Grafico salvo: {caminho_saida}")

    plt.show()


def plotar_comparacao_metricas(
    metricas_pmc:  dict,
    metricas_rbf:  dict,
    caminho_saida: str = None,
) -> None:
    """
    Gráfico de barras comparando Acurácia, Precisão, Revocação e F1-Score
    entre PMC e RBF.
    """
    labels  = ['Acuracia', 'Precisao', 'Revocacao', 'F1-Score']
    chaves  = ['acuracia', 'precisao', 'revocacao', 'f1_score']
    v_pmc   = [metricas_pmc[k] for k in chaves]
    v_rbf   = [metricas_rbf[k] for k in chaves]

    x      = np.arange(len(labels))
    largura = 0.35

    fig, ax = plt.subplots(figsize=(9, 5))

    barras_pmc = ax.bar(x - largura / 2, v_pmc, largura,
                        label='PMC (MLP)', color='royalblue', alpha=0.85)
    barras_rbf = ax.bar(x + largura / 2, v_rbf, largura,
                        label='Rede RBF',  color='coral',     alpha=0.85)

    # Valores sobre as barras
    for barra in (*barras_pmc, *barras_rbf):
        h = barra.get_height()
        ax.annotate(
            f'{h:.4f}',
            xy=(barra.get_x() + barra.get_width() / 2, h),
            xytext=(0, 3), textcoords='offset points',
            ha='center', va='bottom', fontsize=9,
        )

    ax.set_xlabel('Metrica', fontsize=12)
    ax.set_ylabel('Valor', fontsize=12)
    ax.set_title(
        'Comparacao de Metricas — PMC vs Rede RBF\n'
        'Dataset: Predicting Pulsar Star (HTRU2)',
        fontsize=13,
    )
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=11)
    ax.set_ylim(0.0, 1.12)
    ax.legend(fontsize=11)
    ax.grid(True, axis='y', alpha=0.3, linestyle='--')

    plt.tight_layout()

    if caminho_saida:
        plt.savefig(caminho_saida, dpi=150, bbox_inches='tight')
        print(f"  Grafico salvo: {caminho_saida}")

    plt.show()


# =======================================================================
# MÓDULO 5b — VISUALIZAÇÃO GAMIFICADA (SPACE INVADERS)
# =======================================================================

def visualizacao_space_invaders(
    metricas_pmc:    dict,
    metricas_rbf:    dict,
    historico_perda: list,
    t_pmc:           float = None,
    t_rbf:           float = None,
    caminho_saida:   str   = None,
) -> None:
    """
    Visualização gamificada no estilo Space Invaders.
    Cada nave destruída revela uma informação da análise.

    Ondas:
      WAVE 1 — Dataset (4 naves, vermelho)
      WAVE 2 — PMC     (5 naves, ciano)
      WAVE 3 — RBF     (5 naves, amarelo)
      WAVE 4 — BOSS    (1 nave,  magenta)
    """
    t_pmc_s = f"{t_pmc:.2f}s" if t_pmc is not None else "?"
    t_rbf_s = f"{t_rbf:.2f}s" if t_rbf is not None else "?"
    venc = 'PMC' if metricas_pmc['f1_score'] >= metricas_rbf['f1_score'] else 'RBF'

    # ── Definição dos invasores ──────────────────────────────────────────
    # Estrutura: (label, info_revelada, tipo, wave, x0, y)
    inv_defs = [
        # WAVE 1 — Dataset (y=60)
        ('DAT', 'Dataset: HTRU2 — Predicting Pulsar Star',                  'A', 1, 18, 60),
        ('FTR', 'Features: 8  |  Total: 12.528 amostras  |  Classes: 2',   'A', 1, 38, 60),
        ('SPL', 'Treino: 10.022  |  Teste: 2.506  (divisao 80/20)',         'A', 1, 59, 60),
        ('CLS', 'Classe 0: ~91% (nao-pulsar)  |  Classe 1: ~9% (pulsar)',  'A', 1, 80, 60),
        # WAVE 2 — PMC (y=70)
        ('PMC', '>>> PMC — Perceptron Multicamadas <<<',                                              'B', 2, 10, 70),
        ('ACC', f'[PMC] Acuracia:  {metricas_pmc["acuracia"]:.4f}',                                  'B', 2, 27, 70),
        ('PRE', f'[PMC] Precisao:  {metricas_pmc["precisao"]:.4f}',                                  'B', 2, 47, 70),
        ('REC', f'[PMC] Revocacao: {metricas_pmc["revocacao"]:.4f}',                                 'B', 2, 67, 70),
        ('F1 ', f'[PMC] F1-Score:  {metricas_pmc["f1_score"]:.4f}  |  Epocas: {len(historico_perda)}  |  t={t_pmc_s}', 'B', 2, 87, 70),
        # WAVE 3 — RBF (y=80)
        ('RBF', '>>> Rede RBF — Funcao de Base Radial <<<',                                          'C', 3, 10, 80),
        ('ACC', f'[RBF] Acuracia:  {metricas_rbf["acuracia"]:.4f}',                                  'C', 3, 27, 80),
        ('PRE', f'[RBF] Precisao:  {metricas_rbf["precisao"]:.4f}',                                  'C', 3, 47, 80),
        ('REC', f'[RBF] Revocacao: {metricas_rbf["revocacao"]:.4f}',                                 'C', 3, 67, 80),
        ('F1 ', f'[RBF] F1-Score:  {metricas_rbf["f1_score"]:.4f}  |  t={t_rbf_s}',                 'C', 3, 87, 80),
        # WAVE 4 — BOSS (y=89)
        ('BOSS',
         f'VENCEDOR: {venc}  |  PMC F1={metricas_pmc["f1_score"]:.4f}  RBF F1={metricas_rbf["f1_score"]:.4f}',
         'X', 4, 50, 89),
    ]
    n_inv = len(inv_defs)

    # ── Figura ──────────────────────────────────────────────────────────
    fig = plt.figure(figsize=(14, 9), facecolor='black')
    ax  = fig.add_axes([0.0, 0.0, 1.0, 1.0])
    ax.set_facecolor('black')
    ax.set_xlim(0, 100)
    ax.set_ylim(0, 100)
    ax.axis('off')

    # Estrelas de fundo
    np.random.seed(77)
    sx = np.random.uniform(0, 100, 220)
    sy = np.random.uniform(0, 100, 220)
    ss = np.random.uniform(0.3, 3.5, 220)
    ax.scatter(sx, sy, s=ss, c='white', alpha=0.5, zorder=0)

    # Título e HUD
    ax.text(50, 98.5, '★  PULSAR SPACE INVADERS  ★',
            color='#00FF41', fontsize=14, ha='center', va='top',
            fontfamily='monospace', fontweight='bold', zorder=10)
    ax.text(50, 95.2, 'HTRU2  —  PMC vs RBF  —  Analise Gamificada',
            color='#555555', fontsize=8, ha='center', va='top',
            fontfamily='monospace', zorder=10)

    score_obj = ax.text(1, 98.5, 'SCORE: 0',
                        color='#00FF41', fontsize=9, va='top',
                        fontfamily='monospace', fontweight='bold', zorder=10)
    wave_obj  = ax.text(72, 98.5, 'WAVE: 1',
                        color='#FFFF00', fontsize=9, va='top',
                        fontfamily='monospace', fontweight='bold', zorder=10)

    # Divisória do log
    ax.plot([1, 99], [55.5, 55.5], color='#00FF41', lw=0.6, alpha=0.3, zorder=5)
    ax.text(50, 55, '[ ANALYSIS LOG ]',
            color='#00FF41', fontsize=6.5, ha='center', va='top',
            fontfamily='monospace', alpha=0.45, zorder=5)

    # ── Invasores ───────────────────────────────────────────────────────
    inv_chars  = {'A': '(=v=)', 'B': '[>+<]', 'C': '{*-*}', 'X': '<<BOSS>>'}
    inv_colors = {'A': '#FF6B6B', 'B': '#4ECDC4', 'C': '#FFE66D', 'X': '#FF44FF'}
    inv_sizes  = {'A': 9,         'B': 9,         'C': 9,         'X': 12}

    inv_objs = []
    for lbl, info, typ, wave, x0, y in inv_defs:
        co = inv_colors[typ]
        char_t = ax.text(x0, y, inv_chars[typ],
                         color=co, fontsize=inv_sizes[typ],
                         ha='center', va='center',
                         fontfamily='monospace', fontweight='bold',
                         zorder=8, alpha=1.0)
        lbl_t = ax.text(x0, y - 3.5, lbl,
                        color='#777777', fontsize=5.5,
                        ha='center', va='top',
                        fontfamily='monospace', zorder=8, alpha=1.0)
        inv_objs.append({'char': char_t, 'lbl': lbl_t,
                         'alive': True, 'x': float(x0), 'y': float(y)})

    # ── Nave do jogador ──────────────────────────────────────────────────
    player_obj = ax.text(50, 4, ' /^\\ \n/___\\',
                         color='#00BFFF', fontsize=10,
                         ha='center', va='bottom',
                         fontfamily='monospace', fontweight='bold', zorder=8)

    # ── Projétil ─────────────────────────────────────────────────────────
    bullet_obj = ax.text(50, 10, '|',
                         color='#FF4444', fontsize=14,
                         ha='center', va='center',
                         fontfamily='monospace', fontweight='bold',
                         zorder=9, visible=False)

    # ── Explosão ─────────────────────────────────────────────────────────
    expl_obj = ax.text(50, 50, '* + *\n+ * +\n* + *',
                       color='#FFAA00', fontsize=11,
                       ha='center', va='center',
                       fontfamily='monospace', fontweight='bold',
                       zorder=9, visible=False)

    # ── Slots de texto do log ─────────────────────────────────────────────
    ys_info = np.linspace(53, 11, n_inv)
    info_slots = []
    for iy in ys_info:
        t = ax.text(2, iy, '', color='#00FF41', fontsize=7.5,
                    va='center', fontfamily='monospace', zorder=10, alpha=0.0)
        info_slots.append(t)

    # ── Estado da animação ────────────────────────────────────────────────
    S = {
        'phase': 'aiming',
        'pf':    0,
        'tidx':  0,
        'bx':    50.0,
        'by':    7.0,
        'px':    50.0,
        'score': 0,
        'revealed': 0,
    }

    FA = 5    # frames mira
    FE = 8    # frames explosão
    FR = 10   # frames fade do texto
    FP = 8    # frames pausa
    BS = 7.5  # velocidade do projétil (unidades/frame)

    def update(frame):
        S['pf'] += 1

        # Oscilação lateral dos invasores vivos
        osc = 2.5 * np.sin(frame * 0.06)
        for i in range(n_inv):
            if inv_objs[i]['alive']:
                nx = inv_defs[i][4] + osc
                ny = inv_defs[i][5]
                inv_objs[i]['char'].set_position((nx, ny))
                inv_objs[i]['lbl'].set_position((nx, ny - 3.5))
                inv_objs[i]['x'] = nx

        # Estado final
        if S['tidx'] >= n_inv:
            if S['phase'] != 'done':
                S['phase'] = 'done'
                bullet_obj.set_visible(False)
                expl_obj.set_visible(False)
                ax.text(50, 31, '★  MISSAO CONCLUIDA!  ★\n\nTodos os dados de analise foram revelados!',
                        color='#00FF41', fontsize=13, ha='center', va='center',
                        fontfamily='monospace', fontweight='bold', zorder=20,
                        bbox=dict(boxstyle='round,pad=0.8', facecolor='#000800',
                                  edgecolor='#00FF41', linewidth=2.5, alpha=0.95))
            return

        tidx = S['tidx']
        tgt  = inv_objs[tidx]
        d    = inv_defs[tidx]

        phase = S['phase']

        if phase == 'aiming':
            bullet_obj.set_visible(False)
            # Nave desliza suavemente para o alvo
            tx = tgt['x']
            S['px'] += (tx - S['px']) * 0.45
            player_obj.set_position((S['px'], 4))

            if S['pf'] >= FA:
                S['phase'] = 'firing'
                S['pf']    = 0
                S['bx']    = S['px']
                S['by']    = 7.0
                bullet_obj.set_position((S['bx'], S['by']))
                bullet_obj.set_visible(True)

        elif phase == 'firing':
            S['by'] += BS
            S['bx']  = tgt['x']  # míssil guiado
            bullet_obj.set_position((S['bx'], S['by']))

            if S['by'] >= tgt['y'] - 1.2:
                bullet_obj.set_visible(False)
                tgt['alive'] = False
                tgt['char'].set_visible(False)
                tgt['lbl'].set_visible(False)

                expl_obj.set_position((tgt['x'], tgt['y']))
                expl_obj.set_color(inv_colors[d[2]])
                expl_obj.set_visible(True)

                S['score'] += 100 * d[3]
                score_obj.set_text(f'SCORE: {S["score"]}')
                S['phase'] = 'exploding'
                S['pf']    = 0

        elif phase == 'exploding':
            expl_obj.set_visible(S['pf'] % 2 == 0)

            if S['pf'] >= FE:
                expl_obj.set_visible(False)
                S['phase'] = 'revealing'
                S['pf']    = 0

        elif phase == 'revealing':
            ri    = S['revealed']
            alpha = min(1.0, S['pf'] / FR)
            if ri < n_inv:
                info_slots[ri].set_text(f'> {d[1]}')
                info_slots[ri].set_color(inv_colors[d[2]])
                info_slots[ri].set_alpha(alpha)

            if S['pf'] >= FR:
                if S['revealed'] < n_inv:
                    info_slots[S['revealed']].set_alpha(1.0)
                    S['revealed'] += 1
                S['phase'] = 'pausing'
                S['pf']    = 0

        elif phase == 'pausing':
            if S['pf'] >= FP:
                S['tidx'] += 1
                if S['tidx'] < n_inv:
                    wave_obj.set_text(f'WAVE: {inv_defs[S["tidx"]][3]}')
                S['phase'] = 'aiming'
                S['pf']    = 0

    avg_bullet_f = int(((60 - 7) + (89 - 7)) / 2 / BS) + 2
    total_frames = n_inv * (FA + avg_bullet_f + FE + FR + FP) + 100

    anim = animation.FuncAnimation(
        fig, update, frames=total_frames,
        interval=50, repeat=False, blit=False,
    )

    # Detecta se está em IPython/Jupyter (VS Code notebook, JupyterLab, etc.)
    _in_ipython = False
    try:
        _ip = get_ipython()  # type: ignore[name-defined]  # builtin do IPython
        if _ip is not None:
            _in_ipython = True
    except NameError:
        pass

    if _in_ipython:
        # Jupyter / VS Code Interactive: salva GIF e exibe inline
        _gif = caminho_saida or 'space_invaders_analise.gif'
        print(f"  Renderizando GIF ({total_frames} frames), aguarde...")
        try:
            anim.save(_gif, writer='pillow', fps=20, dpi=90)
            print(f"  GIF salvo: {_gif}")
            from IPython.display import Image, display as _ipy_display  # type: ignore
            plt.close(fig)
            _ipy_display(Image(_gif))
        except Exception as exc:
            print(f"  Erro ao gerar GIF: {exc}")
            plt.show()
    else:
        # Script normal: animação ao vivo
        if caminho_saida:
            try:
                anim.save(caminho_saida, writer='pillow', fps=20, dpi=90)
                print(f"  Animacao salva: {caminho_saida}")
            except Exception as exc:
                print(f"  Aviso: nao foi possivel salvar ({exc})")
        plt.show()


# =======================================================================
# BLOCO PRINCIPAL DE EXECUÇÃO
# =======================================================================

if __name__ == '__main__':

    # Caminho para o único arquivo com rótulos (arquivo de teste não tem labels)
    CAMINHO_TREINO = os.path.join('data_train', 'pulsar_data_train.csv')
    SEP = '=' * 65

    print(SEP)
    print('  PROVA 3 — LABORATORIO DE INTELIGENCIA ARTIFICIAL')
    print('  Classificacao de Estrelas Pulsar (HTRU2)')
    print('  PMC (Perceptron Multicamadas)  vs  Rede RBF')
    print('  Implementacao do zero — somente NumPy e Pandas')
    print(SEP)

    # ---------------------------------------------------------------
    # ETAPA 1 — Pré-processamento
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 1] Carregamento e Pre-processamento dos Dados')
    print(f"{'─'*65}")

    df = carregar_dataset(CAMINHO_TREINO)
    X_treino, y_treino, X_teste, y_teste = preprocessar(df, proporcao_treino=0.8)

    print(f'\n  Divisao 80/20:')
    print(f'    Treino: {X_treino.shape[0]:5d} amostras  '
          f'(classe 0: {int(np.sum(y_treino == 0))}, '
          f'classe 1: {int(np.sum(y_treino == 1))})')
    print(f'    Teste:  {X_teste.shape[0]:5d} amostras  '
          f'(classe 0: {int(np.sum(y_teste == 0))}, '
          f'classe 1: {int(np.sum(y_teste == 1))})')

    # ---------------------------------------------------------------
    # ETAPA 2 — PMC: Treinamento
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 2] Treinamento do PMC (Perceptron Multicamadas)')
    print(f"{'─'*65}")
    print('  Arquitetura: Entrada(8) -> Oculta(16, ReLU) -> Saida(1, Sigmoid)')

    t0  = time.time()
    pmc = PerceptronMulticamadas(
        n_entrada        = 8,
        n_ocultos        = 16,
        taxa_aprendizado = 0.01,
        epocas           = 200,
        tamanho_lote     = 64,
    )
    pmc.treinar(X_treino, y_treino)
    t_pmc = time.time() - t0
    print(f'  Tempo de treinamento PMC: {t_pmc:.2f}s')

    # ---------------------------------------------------------------
    # ETAPA 3 — RBF: Treinamento
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 3] Treinamento da Rede RBF')
    print(f"{'─'*65}")
    print('  Ativacao: Gaussiana phi(x) = exp(-gamma * ||x - c||^2)')
    print('  Pesos de saida: Pseudoinversa de Moore-Penrose')

    t0  = time.time()
    rbf = RedeRBF(k_centros=100)
    rbf.treinar(X_treino, y_treino)
    t_rbf = time.time() - t0
    print(f'  Tempo de treinamento RBF: {t_rbf:.2f}s')

    # ---------------------------------------------------------------
    # ETAPA 4 — Avaliação no Conjunto de Teste
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 4] Avaliacao no Conjunto de Teste')
    print(f"{'─'*65}")

    y_pred_pmc, y_prob_pmc = pmc.prever(X_teste)
    y_pred_rbf, y_prob_rbf = rbf.prever(X_teste)

    metricas_pmc = calcular_metricas(y_teste, y_pred_pmc, 'PMC (MLP)')
    metricas_rbf = calcular_metricas(y_teste, y_pred_rbf, 'Rede RBF')

    exibir_metricas(metricas_pmc)
    exibir_metricas(metricas_rbf)

    # ---------------------------------------------------------------
    # ETAPA 5 — Tabela Comparativa
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 5] Comparacao Lado a Lado — PMC vs RBF')
    print(f"{'─'*65}")
    print(f"\n  {'Metrica':<16} {'PMC (MLP)':>12}  {'Rede RBF':>12}  {'Dif. (PMC-RBF)':>14}")
    print(f"  {'─'*58}")

    for chave, nome in [
        ('acuracia',  'Acuracia'),
        ('precisao',  'Precisao'),
        ('revocacao', 'Revocacao'),
        ('f1_score',  'F1-Score'),
    ]:
        v_p   = metricas_pmc[chave]
        v_r   = metricas_rbf[chave]
        diff  = v_p - v_r
        sinal = '+' if diff >= 0 else ''
        print(f'  {nome:<16} {v_p:>12.4f}  {v_r:>12.4f}  {sinal}{diff:>13.4f}')

    print(f'\n  Tempo PMC: {t_pmc:.2f}s  |  Tempo RBF: {t_rbf:.2f}s')

    # ---------------------------------------------------------------
    # ETAPA 6 — Visualização Gamificada (Space Invaders)
    # ---------------------------------------------------------------
    print(f"\n{'─'*65}")
    print('  [ETAPA 6] Iniciando Visualizacao Gamificada — Space Invaders')
    print('  Cada nave destruida revela uma informacao da analise.')
    print(f"{'─'*65}")

    visualizacao_space_invaders(
        metricas_pmc,
        metricas_rbf,
        pmc.historico_perda,
        t_pmc=t_pmc,
        t_rbf=t_rbf,
    )

    print(f'\n{SEP}')
    print('  Execucao concluida com sucesso!')
    print(SEP)
