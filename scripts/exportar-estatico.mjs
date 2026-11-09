/**
 * Exporta o Ghost local como site estatico, pronto para GitHub Pages.
 *
 * Uso:
 *   node scripts/exportar-estatico.mjs
 *
 * Variaveis de ambiente (opcionais):
 *   GHOST_URL   origem do Ghost        (padrao http://localhost:2368)
 *   SITE_URL    URL publica do site    (padrao https://mayccoisa.github.io)
 *   BASE_PATH   subpasta do projeto    (padrao /blog-maykcoisa)
 *   SAIDA       pasta de saida         (padrao dist-pages)
 *
 * O script percorre as paginas a partir da home, baixa paginas e assets,
 * reescreve as URLs para o endereco publico e remove o que depende do servidor
 * do Ghost (busca Sodo).
 */

import { mkdir, readdir, rm, writeFile } from 'node:fs/promises';
import { dirname, join, resolve } from 'node:path';

const ORIGEM = (process.env.GHOST_URL || 'http://localhost:2368').replace(/\/$/, '');
const SITE = (process.env.SITE_URL || 'https://mayccoisa.github.io').replace(/\/$/, '');
const BASE = (process.env.BASE_PATH ?? '/blog-maykcoisa').replace(/\/$/, '');
const SAIDA = resolve(process.env.SAIDA || 'dist-pages');

const EXTENSOES_ASSET = new Set([
    '.css', '.js', '.mjs', '.png', '.jpg', '.jpeg', '.gif', '.svg', '.webp',
    '.ico', '.woff', '.woff2', '.ttf', '.eot', '.xml', '.txt', '.json', '.map', '.md',
]);

// Rotas que nao devem virar pagina estatica
const IGNORAR = ['/rss/', '/webmentions/', '/ghost/', '/members/', '/portal/', '/.ghost/'];

const paginasVistas = new Set();
const assetsVistos = new Set();
const fila = ['/'];
const relatorio = { paginas: 0, assets: 0, erros: [] };

const baseDoSite = SITE + BASE;
const cssExtra = '.nav-search,.side-search{display:none !important}';

function extensao(caminho) {
    const semQuery = caminho.split('?')[0].split('#')[0];
    const ponto = semQuery.lastIndexOf('.');
    const barra = semQuery.lastIndexOf('/');
    if (ponto === -1 || ponto < barra) return '';
    return semQuery.slice(ponto).toLowerCase();
}

function ehAsset(caminho) {
    return EXTENSOES_ASSET.has(extensao(caminho));
}

function destinoDoHtml(urlPath) {
    const limpo = urlPath.split('?')[0].split('#')[0];
    if (limpo === '/' || limpo === '') return join(SAIDA, 'index.html');
    if (limpo.endsWith('/')) return join(SAIDA, limpo.slice(1), 'index.html');
    if (extensao(limpo) === '.html') return join(SAIDA, limpo.slice(1));
    return join(SAIDA, limpo.slice(1), 'index.html');
}

function destinoDoAsset(urlPath) {
    const limpo = urlPath.split('?')[0].split('#')[0];
    return join(SAIDA, limpo.slice(1));
}

async function salvar(caminho, conteudo) {
    await mkdir(dirname(caminho), { recursive: true });
    await writeFile(caminho, conteudo);
}

function hrefsDe(html) {
    const achados = new Set();
    const padrao = /\b(href|src|action)="([^"]+)"/g;
    let m;
    while ((m = padrao.exec(html)) !== null) achados.add(m[2]);

    const srcsetPadrao = /\bsrcset="([^"]+)"/g;
    while ((m = srcsetPadrao.exec(html)) !== null) {
        for (const parte of m[1].split(',')) {
            const url = parte.trim().split(/\s+/)[0];
            if (url) achados.add(url);
        }
    }

    // Imagens de compartilhamento ficam em meta tags
    const metaPadrao = /<meta[^>]+(?:property|name)="(?:og:image|twitter:image)"[^>]*content="([^"]+)"/g;
    while ((m = metaPadrao.exec(html)) !== null) achados.add(m[1]);

    return achados;
}

function normalizar(url) {
    if (!url) return null;
    if (url.startsWith(ORIGEM)) {
        const resto = url.slice(ORIGEM.length);
        return resto === '' ? '/' : resto;
    }
    if (url.startsWith('/') && !url.startsWith('//')) return url;
    return null;
}

function transformar(html) {
    let saida = html;

    // A busca do Ghost depende da API do servidor: sai do site estatico.
    saida = saida.replace(/<script[^>]*sodo-search[^>]*>\s*<\/script>/gi, '');
    saida = saida.replace(/<link[^>]*sodo[^>]*>/gi, '');

    // Caminhos absolutos da raiz recebem a subpasta do projeto
    saida = saida.replace(/\b(href|src|action|content)="\/(?!\/)([^"]*)"/g, `$1="${BASE}/$2"`);

    // srcset: cada URL recebe a subpasta, sem duplicar
    saida = saida.replace(/\bsrcset="([^"]+)"/g, (tudo, valor) => {
        const partes = valor.split(',').map((parte) => {
            const [url, ...descritor] = parte.trim().split(/\s+/);
            let novo = url;
            if (url.startsWith('/') && !url.startsWith(`${BASE}/`)) novo = BASE + url;
            return [novo, ...descritor].join(' ');
        });
        return `srcset="${partes.join(', ')}"`;
    });

    // Origem do Ghost vira o endereco publico
    saida = saida.split(ORIGEM).join(baseDoSite);

    // O RSS sai como arquivo unico
    saida = saida.split(`${BASE}/rss/`).join(`${BASE}/rss.xml`);

    return saida;
}

async function baixarAsset(urlPath) {
    if (assetsVistos.has(urlPath)) return;
    assetsVistos.add(urlPath);

    try {
        const resposta = await fetch(ORIGEM + urlPath);
        if (!resposta.ok) {
            relatorio.erros.push(`asset ${urlPath}: ${resposta.status}`);
            return;
        }
        let corpo = Buffer.from(await resposta.arrayBuffer());

        // Esconde a busca no CSS do tema
        if (extensao(urlPath) === '.css' && urlPath.includes('/assets/css/')) {
            corpo = Buffer.concat([corpo, Buffer.from(`\n${cssExtra}\n`)]);
        }

        // Sitemaps e afins precisam apontar para o endereco publico
        if (extensao(urlPath) === '.xml') {
            let texto = corpo.toString('utf8');
            texto = texto.replace(/<\?xml-stylesheet[^?]*\?>/g, '');
            texto = texto.split(ORIGEM).join(baseDoSite);
            corpo = Buffer.from(texto, 'utf8');
        }

        await salvar(destinoDoAsset(urlPath), corpo);
        relatorio.assets += 1;
    } catch (erro) {
        relatorio.erros.push(`asset ${urlPath}: ${erro.message}`);
    }
}

async function processarPagina(urlPath) {
    if (paginasVistas.has(urlPath)) return;
    paginasVistas.add(urlPath);

    let html;
    try {
        const resposta = await fetch(ORIGEM + urlPath);
        if (!resposta.ok) {
            relatorio.erros.push(`pagina ${urlPath}: ${resposta.status}`);
            return;
        }
        html = await resposta.text();
    } catch (erro) {
        relatorio.erros.push(`pagina ${urlPath}: ${erro.message}`);
        return;
    }

    const transformado = transformar(html);
    await salvar(destinoDoHtml(urlPath), transformado);
    relatorio.paginas += 1;

    for (const bruto of hrefsDe(html)) {
        const caminho = normalizar(bruto);
        if (!caminho) continue;
        if (caminho.startsWith('//')) continue;
        if (IGNORAR.some((prefixo) => caminho.startsWith(prefixo))) continue;

        if (ehAsset(caminho)) {
            await baixarAsset(caminho);
        } else {
            fila.push(caminho);
        }
    }
}

async function baixarRss() {
    try {
        const resposta = await fetch(`${ORIGEM}/rss/`);
        if (!resposta.ok) {
            relatorio.erros.push(`rss: ${resposta.status}`);
            return;
        }
        let xml = await resposta.text();
        xml = xml.split(ORIGEM).join(baseDoSite);
        await salvar(join(SAIDA, 'rss.xml'), xml);
        console.log('rss.xml gerado');
    } catch (erro) {
        relatorio.erros.push(`rss: ${erro.message}`);
    }
}

async function baixarExtras() {
    for (const [caminho, destino] of [
        ['/sitemap.xml', 'sitemap.xml'],
        ['/robots.txt', 'robots.txt'],
    ]) {
        try {
            const resposta = await fetch(ORIGEM + caminho);
            if (!resposta.ok) continue;
            let texto = await resposta.text();
            texto = texto.split(ORIGEM).join(baseDoSite);
            await salvar(join(SAIDA, destino), texto);
        } catch {
            /* opcional */
        }
    }
}

async function copiarRestante() {
    // arquivos que o Ghost serve direto e nao aparecem no HTML
    const extras = [
        '/favicon.ico',
        '/content/images/maykcoisa/icone.png',
        '/content/images/maykcoisa/compartilhamento.png',
    ];
    for (const caminho of extras) await baixarAsset(caminho);
}

async function lerSitemap(url) {
    const vistas = new Set();
    const paginas = [];
    const mapas = [];

    async function visitar(endereco) {
        if (vistas.has(endereco)) return;
        vistas.add(endereco);
        mapas.push(endereco);

        const resposta = await fetch(endereco);
        if (!resposta.ok) return;

        const xml = await resposta.text();
        const locais = [...xml.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
        const ehIndice = xml.includes('<sitemapindex');

        for (const local of locais) {
            if (ehIndice) await visitar(local);
            else paginas.push(local);
        }
    }

    await visitar(url);
    return { paginas, mapas };
}

async function main() {
    console.log(`Exportando ${ORIGEM} -> ${SAIDA} (${baseDoSite}/)`);
    await rm(SAIDA, { recursive: true, force: true });
    await mkdir(SAIDA, { recursive: true });

    // O sitemap do Ghost e um indice: cada filho lista posts, paginas, assuntos ou autores
    try {
        const { paginas, mapas } = await lerSitemap(`${ORIGEM}/sitemap.xml`);
        for (const local of paginas) {
            const caminho = normalizar(local);
            if (caminho && !IGNORAR.some((p) => caminho.startsWith(p))) fila.push(caminho);
        }
        for (const mapa of mapas) {
            const caminho = normalizar(mapa);
            if (caminho) await baixarAsset(caminho);
        }
        console.log(`Sitemap: ${paginas.length} URLs`);
    } catch {
        console.log('Sitemap indisponivel, seguindo pelo HTML');
    }

    while (fila.length > 0) {
        const lote = fila.splice(0, 8);
        await Promise.all(lote.map(processarPagina));
    }

    await baixarRss();
    await baixarExtras();
    await copiarRestante();

    await salvar(join(SAIDA, '.nojekyll'), '');

    console.log(`\nPaginas: ${relatorio.paginas}`);
    console.log(`Assets:  ${relatorio.assets}`);
    if (relatorio.erros.length) {
        console.log(`\nFalhas (${relatorio.erros.length}):`);
        for (const erro of relatorio.erros) console.log(`  - ${erro}`);
        process.exitCode = 1;
    }
}

await main();
