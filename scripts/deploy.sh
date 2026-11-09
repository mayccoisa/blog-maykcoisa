#!/usr/bin/env bash
# Deploy do weon-site em produção (VM GCP weon-com-br).
#
#   npm run deploy        (ou: bash scripts/deploy.sh)
#
# Fluxo: build SSR local → tarball → scp → extrai em /opt/weon-site-next →
# troca atômica (build anterior vira /opt/weon-site-prev) → restart do
# container weon-site → health check. Se o health check falhar, volta o
# build anterior sozinho.
#
# Requisitos: Git Bash (tar/ssh/scp) e chave SSH autorizada p/ isolve na VM.
set -euo pipefail

HOST=isolve@34.95.136.161
SITE_URL=https://weon.com.br
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
TARBALL="$(mktemp -t weon-site-output-XXXX).tar.gz"
trap 'rm -f "$TARBALL"' EXIT

echo "==> 1/5 Build SSR (nuxi build)"
cd "$ROOT"
npx nuxi build

echo "==> 2/5 Empacotando .output"
tar czf "$TARBALL" .output
du -h "$TARBALL" | cut -f1

echo "==> 3/5 Enviando para a VM"
scp -o BatchMode=yes "$TARBALL" "$HOST":/home/isolve/weon-site-output.tar.gz

echo "==> 4/5 Trocando build e reiniciando container"
ssh -o BatchMode=yes "$HOST" '
set -e
docker run --rm -v /home/isolve:/src -v /opt:/opt alpine sh -c "
  rm -rf /opt/weon-site-next && mkdir -p /opt/weon-site-next &&
  tar xzf /src/weon-site-output.tar.gz -C /opt/weon-site-next &&
  test -f /opt/weon-site-next/.output/server/index.mjs &&
  rm -rf /opt/weon-site-prev &&
  ( [ -d /opt/weon-site ] && mv /opt/weon-site /opt/weon-site-prev || true ) &&
  mv /opt/weon-site-next /opt/weon-site
"
docker restart weon-site >/dev/null
sleep 4
# health check interno; se falhar, volta o build anterior
if docker run --rm --network weon-network alpine wget -qO- -T 10 http://172.100.0.10:3000/ 2>/dev/null | grep -q "<title>"; then
  echo "health check interno: OK"
else
  echo "health check FALHOU — revertendo para o build anterior..."
  docker run --rm -v /opt:/opt alpine sh -c "rm -rf /opt/weon-site-failed && mv /opt/weon-site /opt/weon-site-failed && mv /opt/weon-site-prev /opt/weon-site"
  docker restart weon-site >/dev/null
  exit 1
fi
'

echo "==> 5/5 Smoke test externo"
sleep 2
code=$(curl -sk -o /dev/null -w '%{http_code}' "$SITE_URL/")
title=$(curl -sk "$SITE_URL/" | grep -oE '<title>[^<]*' | head -1)
echo "$SITE_URL -> $code | $title"
[ "$code" = "200" ] || { echo "ATENÇÃO: resposta $code — verifique!"; exit 1; }

echo "✅ Deploy concluído. Rollback manual, se precisar:"
echo "   ssh $HOST 'docker run --rm -v /opt:/opt alpine sh -c \"mv /opt/weon-site /opt/weon-site-bad && mv /opt/weon-site-prev /opt/weon-site\" && docker restart weon-site'"
