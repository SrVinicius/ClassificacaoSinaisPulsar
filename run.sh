#!/bin/bash

# Cores para output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════╗"
echo "║  🌌 PULSAR EXPLORER - INICIANDO...     ║"
echo "╚════════════════════════════════════════╝"
echo -e "${NC}"

# Verificar se Python3 está instalado
if ! command -v python3 &> /dev/null; then
    echo -e "${YELLOW}❌ Python3 não encontrado. Por favor, instale Python3.${NC}"
    exit 1
fi

echo -e "${BLUE}📦 Verificando dependências...${NC}"

# Instalar dependências se necessário
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⏳ Instalando dependências...${NC}"
    pip install -q Flask Flask-CORS 2>/dev/null
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✅ Dependências instaladas com sucesso${NC}"
    else
        echo -e "${YELLOW}⚠️  Não foi possível instalar automaticamente.${NC}"
        echo -e "${YELLOW}Execute manualmente: pip install -r requirements.txt${NC}"
    fi
else
    echo -e "${GREEN}✅ Dependências já instaladas${NC}"
fi

# Matar processos antigos na porta 5001
PORT=5001
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null 2>&1; then
    echo -e "${YELLOW}⏳ Limpando porta $PORT...${NC}"
    pkill -f "python.*app.py" 2>/dev/null
    sleep 2
fi

echo -e "${BLUE}🚀 Iniciando servidor Flask na porta $PORT...${NC}"
python3 app.py &

# Aguardar servidor iniciar
sleep 3

# Verificar se servidor está rodando
if curl -s http://localhost:$PORT/ > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Servidor rodando com sucesso!${NC}"
    echo -e "${GREEN}✨ Abrindo navegador...${NC}"

    # Tentar abrir no navegador padrão
    if command -v open &> /dev/null; then
        open "http://localhost:$PORT"
    elif command -v xdg-open &> /dev/null; then
        xdg-open "http://localhost:$PORT"
    elif command -v start &> /dev/null; then
        start "http://localhost:$PORT"
    fi

    echo -e "${BLUE}"
    echo "╔════════════════════════════════════════╗"
    echo "║  🌌 PULSAR EXPLORER RODANDO!          ║"
    echo "╠════════════════════════════════════════╣"
    echo "║  URL: http://localhost:$PORT"
    echo "║  Pressione CTRL+C para parar           ║"
    echo "╚════════════════════════════════════════╝"
    echo -e "${NC}"

    # Manter o processo rodando
    wait
else
    echo -e "${YELLOW}❌ Falha ao iniciar o servidor${NC}"
    echo -e "${YELLOW}Verifique o arquivo server.log para mais detalhes${NC}"
    exit 1
fi
