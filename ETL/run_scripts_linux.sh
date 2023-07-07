#!/bin/bash
BLUE='\033[1;34m'
NC='\033[0m' # No Color
#Transformações
python3 transformDisasters.py
python3 transformAgricultura.py
python3 transformDesempregados.py
python3 transformGDP.py
python3 transformPopulacao.py
python3 transformTurismo.py
echo -e "${BLUE}Transformations Completed...${NC}"
#Criação das Dimensões
python3 dimData.py
python3 dimEvent.py
python3 dimLocation.py
python3 dimType.py
python3 factDisaster.py
echo -e "${BLUE}Dimensions Created Completed...${NC}"
#Load na DB
python3 loadData.py
python3 loadEvent.py
python3 loadLocation.py
python3 loadType.py
python3 factDisaster.py
echo -e "${BLUE}Load Completed...${NC}"

