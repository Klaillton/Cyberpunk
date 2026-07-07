#!/usr/bin/env sh
# Baixa modelos Ollama no stack local (profile init).
# Executar na raiz do repositório:
#   sh deploy/scripts/pull_models.sh

set -e
cd "$(dirname "$0")/../.."

if [ ! -f deploy/.env ]; then
  echo "Criando deploy/.env a partir de .env.example..."
  cp deploy/.env.example deploy/.env
fi

docker compose -f deploy/docker-compose.yml --env-file deploy/.env --profile init run --rm ollama-pull

echo "Modelos instalados. Suba o stack com:"
echo "  docker compose -f deploy/docker-compose.yml --env-file deploy/.env up -d"