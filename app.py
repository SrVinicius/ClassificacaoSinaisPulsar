"""
API Flask para servir dados do classificador de pulsares
"""
import json
import numpy as np
import pandas as pd
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import os

app = Flask(__name__, template_folder='.', static_folder='static')
CORS(app)

# Carregar dados
try:
    df_train = pd.read_csv('data_train/pulsar_data_train.csv')
    df_test = pd.read_csv('data_test/pulsar_data_test.csv')

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
    df_train.columns = nomes_colunas
    df_test.columns = nomes_colunas
except Exception as e:
    print(f"Erro ao carregar dados: {e}")
    df_train = None
    df_test = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Retorna estatísticas gerais dos dados"""
    if df_train is None:
        return jsonify({'error': 'Dados não carregados'}), 500

    return jsonify({
        'train_samples': len(df_train),
        'test_samples': len(df_test),
        'total_features': 8,
        'class_0_count': int((df_train['classe'] == 0).sum()),
        'class_1_count': int((df_train['classe'] == 1).sum()),
        'class_0_percentage': float((df_train['classe'] == 0).sum() / len(df_train) * 100),
        'class_1_percentage': float((df_train['classe'] == 1).sum() / len(df_train) * 100),
    })

@app.route('/api/feature-stats')
def get_feature_stats():
    """Retorna estatísticas de cada feature"""
    if df_train is None:
        return jsonify({'error': 'Dados não carregados'}), 500

    features = ['media_perfil', 'desvio_perfil', 'curtose_perfil', 'assimetria_perfil',
                'media_dm_snr', 'desvio_dm_snr', 'curtose_dm_snr', 'assimetria_dm_snr']

    stats = {}
    for feature in features:
        stats[feature] = {
            'mean': float(df_train[feature].mean()),
            'std': float(df_train[feature].std()),
            'min': float(df_train[feature].min()),
            'max': float(df_train[feature].max()),
            'null_count': int(df_train[feature].isna().sum())
        }
    return jsonify(stats)

@app.route('/api/models-performance')
def get_models_performance():
    """Retorna performance dos modelos"""
    return jsonify({
        'pmc': {
            'name': 'Perceptron Multicamadas (MLP)',
            'accuracy': 0.977,
            'precision': 0.904,
            'recall': 0.821,
            'f1': 0.861,
            'color': '#00ff88'
        },
        'rbf': {
            'name': 'Rede RBF',
            'accuracy': 0.960,
            'precision': 0.748,
            'recall': 0.817,
            'f1': 0.781,
            'color': '#ff00ff'
        }
    })

@app.route('/api/dataset-info')
def get_dataset_info():
    """Retorna informações detalhadas do dataset"""
    return jsonify({
        'name': 'HTRU2 - High Time Resolution Universe Pulsar Dataset',
        'description': 'Classificação de sinais pulsar vs ruído em observações astronômicas',
        'total_samples': 12528,
        'total_features': 8,
        'task': 'Classificação Binária',
        'imbalance_ratio': '91% classe 0 (não-pulsar) vs 9% classe 1 (pulsar)',
        'features': [
            {'name': 'media_perfil', 'description': 'Média do perfil integrado'},
            {'name': 'desvio_perfil', 'description': 'Desvio padrão do perfil integrado'},
            {'name': 'curtose_perfil', 'description': 'Curtose (grau de achatamento)'},
            {'name': 'assimetria_perfil', 'description': 'Assimetria da distribuição'},
            {'name': 'media_dm_snr', 'description': 'Média da medida de dispersão vs ruído'},
            {'name': 'desvio_dm_snr', 'description': 'Desvio padrão da medida de dispersão'},
            {'name': 'curtose_dm_snr', 'description': 'Curtose da dispersão'},
            {'name': 'assimetria_dm_snr', 'description': 'Assimetria da dispersão'}
        ]
    })

if __name__ == '__main__':
    app.run(debug=True, port=5001)
