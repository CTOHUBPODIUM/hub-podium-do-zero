# Lançamento do Site Institucional HUB-Podium

## Status

- Site institucional pré-produto: ativo
- Data: 2026-05-04
- Owner técnico: CTO Rafael Duarte
- Objetivo: apresentar a HUB-Podium publicamente sem vender o app como se já estivesse pronto para operação comercial plena

## Estrutura publicada

O site foi refeito para operar como presença institucional da HUB-Podium, com foco em:

- marca e posicionamento
- visão da empresa
- frentes de construção
- governança
- confiança institucional
- contato público atual via LinkedIn

Além da landing principal, o pacote web agora inclui:

- `404.html`
- `robots.txt`
- `site.webmanifest`
- ícones PWA e favicon
- imagem de compartilhamento social
- workflow de deploy para GitHub Pages

## Arquivos principais

- `landing-page/index.html`
- `landing-page/404.html`
- `landing-page/styles.css`
- `landing-page/assets/hub-podium-site-hero-v2.png`
- `landing-page/assets/hub-podium-mark-v2.png`
- `landing-page/assets/hub-podium-icon-192.png`
- `landing-page/assets/hub-podium-icon-512.png`
- `landing-page/assets/hub-podium-og-1200x630.png`
- `tools/generate_site_assets.py`
- `.github/workflows/deploy-landing-page.yml`

## Endereços de acesso

- Preview local: `landing-page/index.html`
- Servidor local: `http://127.0.0.1:4173`
- URL pública temporária: `https://session-crm-york-submit.trycloudflare.com`
- URL pública estável: `https://ctohubpodium.github.io/hub-podium-do-zero/`
- Domínio customizado configurado no GitHub Pages: `https://hub-podium.com/`

## Observação importante

A URL pública atual foi aberta por quick tunnel do Cloudflare. Ela é útil para validação imediata, apresentação e compartilhamento rápido, mas não deve ser tratada como endereço definitivo da HUB-Podium, porque pode mudar quando o processo for reiniciado.

## Próximo nível de publicação

Para versão estável de produção, o caminho adotado foi GitHub Pages com workflow próprio.

### Como ativar

1. Fazer push do repositório com os arquivos novos.
2. No GitHub, abrir `Settings > Pages`.
3. Em `Build and deployment`, selecionar `GitHub Actions`.
4. Deixar o workflow `.github/workflows/deploy-landing-page.yml` publicar a pasta `landing-page/`.

### URL esperada

Se o repositório permanecer `CTOHUBPODIUM/hub-podium-do-zero`, a URL padrão esperada do GitHub Pages será:

- `https://ctohubpodium.github.io/hub-podium-do-zero/`

### Próxima evolução institucional

A recomendação depois da primeira publicação estável é:

1. conectar domínio próprio da HUB-Podium
2. criar e-mail institucional
3. revisar `Website` do LinkedIn da empresa com a URL definitiva
4. adicionar política de privacidade final assim que o Jurídico concluir a versão pública oficial
