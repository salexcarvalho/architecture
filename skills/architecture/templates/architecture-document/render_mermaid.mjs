// Renderiza blocos Mermaid (.mmd) para PNG usando o Chromium local.
// Uso: node render_mermaid.mjs <dir-com-.mmd> [viewport-px=1600] [escala=2.5]
// Gera <nome>.png ao lado de cada <nome>.mmd. Sai com código 1 se algum diagrama falhar.
// Dependências (ver setup.sh): mermaid e playwright-core em $ARCH_PDF_HOME/node.
import fs from 'node:fs';
import os from 'node:os';
import path from 'node:path';
import { createRequire } from 'node:module';

const [dir, widthArg, scaleArg] = process.argv.slice(2);  // largura = viewport (px); o tamanho do diagrama é o natural
if (!dir) { console.error('uso: node render_mermaid.mjs <dir> [largura] [escala]'); process.exit(2); }
const width = Number(widthArg || 1600), scale = Number(scaleArg || 2.5);
const home = process.env.ARCH_PDF_HOME || path.join(os.homedir(), '.cache', 'architecture-pdf');
const require = createRequire(path.join(home, 'node', 'package.json'));
const { chromium } = require('playwright-core');
const mermaidJs = require.resolve('mermaid/dist/mermaid.min.js');

function findChrome() {
  if (process.env.CHROMIUM_PATH && fs.existsSync(process.env.CHROMIUM_PATH)) return process.env.CHROMIUM_PATH;
  const pw = path.join(os.homedir(), '.cache', 'ms-playwright');
  if (fs.existsSync(pw)) {
    const dirs = fs.readdirSync(pw).filter(d => d.startsWith('chromium-')).sort().reverse();
    for (const d of dirs) {
      for (const sub of fs.readdirSync(path.join(pw, d)).filter(s => s.startsWith('chrome-linux'))) {
        const p = path.join(pw, d, sub, 'chrome'); if (fs.existsSync(p)) return p;
      }
    }
  }
  for (const p of ['/usr/bin/google-chrome', '/usr/bin/chromium', '/usr/bin/chromium-browser']) if (fs.existsSync(p)) return p;
  return undefined;
}

// Paleta azul no estilo C4 (caixas #438DD5, atores #08427B), igual à do documento de referência.
const theme = {
  theme: 'base',
  themeVariables: {
    fontFamily: 'Liberation Sans, Arial, sans-serif', fontSize: '14px',
    primaryColor: '#438DD5', primaryTextColor: '#ffffff', primaryBorderColor: '#3C7FC0',
    secondaryColor: '#08427B', secondaryTextColor: '#ffffff', secondaryBorderColor: '#073B6F',
    tertiaryColor: '#f4f7fb', tertiaryTextColor: '#0F4761', tertiaryBorderColor: '#9db7d3',
    lineColor: '#555555', textColor: '#222222', noteBkgColor: '#fff8c5', noteTextColor: '#333333',
    actorBkg: '#08427B', actorTextColor: '#ffffff', actorBorder: '#073B6F', signalColor: '#333333', signalTextColor: '#222222',
    labelBoxBkgColor: '#eaf1f8', labelTextColor: '#0F4761', loopTextColor: '#0F4761',
    clusterBkg: '#f4f7fb', clusterBorder: '#9db7d3', edgeLabelBackground: '#ffffff',
    attributeBackgroundColorEven: '#ffffff', attributeBackgroundColorOdd: '#f4f7fb',
  },
  fontSize: 13, securityLevel: 'loose', startOnLoad: false,
  // rótulos de aresta e de subgrafo em cor escura (o texto padrão do tema é branco, para as caixas)
  themeCSS: '.edgeLabel, .edgeLabel p, .edgeLabel span, .labelBkg { color:#333 !important; fill:#333 !important; background-color:#fff !important; } .cluster-label span, .cluster-label p, .cluster text { color:#0F4761 !important; fill:#0F4761 !important; font-weight:700; } .messageText { fill:#222 !important; }',
  flowchart: { htmlLabels: true, curve: 'basis', useMaxWidth: false, nodeSpacing: 35, rankSpacing: 40 }, sequence: { useMaxWidth: false, wrap: true, width: 105, messageFontSize: 13, actorFontSize: 13, noteFontSize: 12, messageFontFamily: 'Liberation Sans, Arial, sans-serif', actorFontFamily: 'Liberation Sans, Arial, sans-serif', noteFontFamily: 'Liberation Sans, Arial, sans-serif', actorMargin: 24, messageMargin: 30, boxMargin: 6, noteMargin: 8 }, er: { useMaxWidth: false },
};

const files = fs.readdirSync(dir).filter(f => f.endsWith('.mmd')).sort();
if (!files.length) process.exit(0);
const browser = await chromium.launch({ executablePath: findChrome(), args: ['--no-sandbox'] });
const page = await browser.newPage({ viewport: { width, height: 800 }, deviceScaleFactor: scale });
await page.setContent('<html><body style="margin:0;background:#fff"><div id="c" style="padding:8px;display:inline-block"></div></body></html>');
await page.addScriptTag({ path: mermaidJs });
await page.evaluate(t => window.mermaid.initialize(t), theme);
let failed = 0;
for (const [i, f] of files.entries()) {
  const code = fs.readFileSync(path.join(dir, f), 'utf8');
  try {
    await page.evaluate(async ([c, n]) => {
      const { svg } = await window.mermaid.render('g' + n, c);
      document.getElementById('c').innerHTML = svg;
    }, [code, i]);
    const el = await page.$('#c svg');
    await el.screenshot({ path: path.join(dir, f.replace(/\.mmd$/, '.png')), omitBackground: false });
    console.log('ok   ' + f);
  } catch (e) {
    failed++; console.error('ERRO ' + f + ': ' + String(e.message || e).split('\n')[0]);
  }
}
await browser.close();
process.exit(failed ? 1 : 0);
