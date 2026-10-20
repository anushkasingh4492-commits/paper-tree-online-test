// Render student/teacher/sample HTML books from canonical JSON with KaTeX pre-rendered (works offline).
// usage: node render_html.js <records.json> <outdir> <title> [sample_paper.json]
const fs = require('fs');
const path = require('path');
const katex = require(__dirname + '/node_modules/katex');

const [,, recPath, outDir, title, samplePath] = process.argv;
const STU = process.env.STU_NAME || 'Student_Complete_Bank.html';
const TEA = process.env.TEA_NAME || 'Teacher_Complete_Bank.html';
const SKIP_BOOKS = process.env.SKIP_BOOKS === '1';
const KDIR = process.env.KATEX_DIR || outDir;
const recs = JSON.parse(fs.readFileSync(recPath, 'utf8'));

function esc(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
function tex(s) {
  if (s === null || s === undefined) return '';
  const parts = String(s).split(/(?<!\\)\$/);
  let out = '';
  parts.forEach((p, k) => {
    if (k % 2 === 0) out += esc(p).replace(/\n/g, '<br>');
    else out += katex.renderToString(p, {throwOnError: true, strict: 'ignore', output: 'html'});
  });
  return out;
}

const CSS = `body{font:17px/1.6 Arial,sans-serif;margin:0;background:#f2f5f7;color:#183244}
header{padding:42px max(25px,calc((100% - 1020px)/2));background:#1d3557;color:#fff}h1{font-size:36px;margin:0}
header p{max-width:900px}.bar{position:sticky;top:0;z-index:5;background:#fff;padding:12px;display:flex;gap:10px;flex-wrap:wrap;box-shadow:0 2px 10px #0001}
input,select,button{font:inherit;padding:9px;border:1px solid #ccd8df;border-radius:5px}main{max-width:1020px;margin:20px auto}
article{background:#fff;padding:26px 30px;margin:18px;border-radius:8px;border:1px solid #dae4e9;break-inside:avoid}
.meta{font-size:13px;color:#557383}.q{margin:10px 0 6px}ol{list-style:none;padding:0;margin:8px 0}li{margin:8px 0}li b{display:inline-block;width:28px}
li.key{background:#e8f5ee;border-radius:4px}details{background:#eef4fb;padding:14px 18px;border-radius:6px;margin-top:10px}summary{cursor:pointer;font-weight:bold}
.nv{background:#fff7e6;padding:10px 14px;border-radius:6px;margin-top:10px;font-size:15px}article[hidden]{display:none}
.count{align-self:center;color:#557383;font-size:14px}
@media print{body{background:#fff;font-size:10.5pt}.bar{display:none}header{padding:8mm;color:#1d3557;background:#fff}main{margin:0}
article{border:0;border-top:1px solid #ddd;margin:0;padding:4mm 0}details{display:block}details>summary{display:none}}`;

function shell(t, sub, body, filters) {
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>${esc(t)}</title><link rel="stylesheet" href="${process.env.KATEX_PREFIX || ""}katex/katex.min.css"><style>${CSS}</style></head><body>
<header><h1>${esc(t)}</h1>${sub}</header>${filters || ''}<main id="list">${body}</main>
<script>
const qs=[...document.querySelectorAll('article')];const f=()=>{const s=(document.getElementById('search')||{}).value||'';
const t=(document.getElementById('topic')||{}).value||'';const d=(document.getElementById('diff')||{}).value||'';let n=0;
qs.forEach(a=>{const ok=(!s||a.textContent.toLowerCase().includes(s.toLowerCase()))&&(!t||a.dataset.topic===t)&&(!d||a.dataset.diff===d);a.hidden=!ok;if(ok)n++;});
const c=document.getElementById('count');if(c)c.textContent=n+' shown';};
document.querySelectorAll('.bar input,.bar select').forEach(e=>e.addEventListener('input',f));f();
</script></body></html>`;
}

function filters() {
  const topics = [...new Set(recs.map(r => r.topic))];
  return `<div class="bar"><input id="search" placeholder="Search text or ID"><select id="topic"><option value="">All topics</option>${
    topics.map(t => `<option>${esc(t)}</option>`).join('')}</select><select id="diff"><option value="">All levels</option><option>Easy</option><option>Medium</option><option>Difficult</option></select><button onclick="print()">Print</button><span class="count" id="count"></span></div>`;
}

function article(r, teacher, num) {
  let h = `<article data-topic="${esc(r.topic)}" data-diff="${r.difficulty}"><div class="meta">${num ? 'Q' + num + ' &middot; ' : ''}${r.id} &middot; ${esc(r.unit)} &middot; ${esc(r.topic)} &middot; ${r.difficulty} &middot; Class ${r.source_class}</div>`;
  h += `<div class="q">${tex(r.question)}</div><ol>`;
  for (const L of ['A', 'B', 'C', 'D']) h += `<li class="${teacher && L === r.correct_option ? 'key' : ''}"><b>(${L})</b>${tex(r.options[L])}</li>`;
  h += '</ol>';
  if (teacher) {
    h += `<details open><summary>Answer and solution</summary><p><b>Answer: (${r.correct_option})</b> ${tex(r.correct_answer)}</p><p>${tex(r.explanation)}</p>`;
    h += `<p class="meta"><b>Targets:</b> ${tex(r.common_misconception)}<br><b>Difficulty:</b> ${tex(r.difficulty_reason)}<br><b>Family:</b> ${esc(r.family_dependencies.join(', '))} &middot; <b>Check:</b> ${esc(r.validation_status)}</p></details>`;
    if (r.numerical_variant) h += `<div class="nv"><b>Numerical-answer form:</b> ${tex(r.numerical_variant.question)} <b>Answer: ${r.numerical_variant.answer_integer}</b></div>`;
  }
  return h + '</article>';
}

fs.mkdirSync(path.join(KDIR, 'katex'), {recursive: true});
fs.copyFileSync(__dirname + '/node_modules/katex/dist/katex.min.css', path.join(KDIR, 'katex', 'katex.min.css'));
fs.cpSync(__dirname + '/node_modules/katex/dist/fonts', path.join(KDIR, 'katex', 'fonts'), {recursive: true});

const sub = `<p>${recs.length} questions &middot; four options, one correct &middot; marking +4 / &minus;1 / 0. Difficulty labels are editorial estimates. Unless a question says otherwise: log without a base and log<sub>e</sub> denote the natural logarithm; arguments of complex numbers are principal values in (&minus;&pi;, &pi;]; inverse trigonometric functions take principal values. Syllabus basis: NTA JEE Main 2026.</p>`;
if (!SKIP_BOOKS) fs.writeFileSync(path.join(outDir, STU), shell(title + ': Student bank', sub, recs.map(r => article(r, false)).join(''), filters()));
if (!SKIP_BOOKS) fs.writeFileSync(path.join(outDir, TEA), shell(title + ': Teacher bank', sub + '<p>Includes keys, worked solutions, targeted misconceptions and numerical-answer forms.</p>', recs.map(r => article(r, true)).join(''), filters()));

if (samplePath) {
  const sp = JSON.parse(fs.readFileSync(samplePath, 'utf8'));
  const byId = Object.fromEntries(recs.map(r => [r.id, r]));
  let qb = '', sb = '';
  sp.section_a.forEach((id, i) => { qb += article(byId[id], false, i + 1); sb += article(byId[id], true, i + 1); });
  qb += '<h2 style="margin:30px 18px 0">Section B: numerical answer (enter an integer)</h2>';
  sb += '<h2 style="margin:30px 18px 0">Section B: numerical answer</h2>';
  sp.section_b.forEach((id, i) => {
    const r = byId[id]; const n = 21 + i;
    qb += `<article><div class="meta">Q${n} &middot; ${r.id} &middot; ${r.difficulty}</div><div class="q">${tex(r.numerical_variant.question)}</div></article>`;
    sb += `<article><div class="meta">Q${n} &middot; ${r.id} &middot; ${r.difficulty}</div><div class="q">${tex(r.numerical_variant.question)}</div><details open><summary>Answer</summary><p><b>Answer: ${r.numerical_variant.answer_integer}</b></p><p>${tex(r.explanation)}</p></details></article>`;
  });
  const ssub = `<p>${esc(sp.description)} Seed ${sp.seed}. 25 questions, maximum 100 marks, +4 / &minus;1 / 0.</p>`;
  fs.writeFileSync(path.join(outDir, 'Sample_Paper.html'), shell(title + ': Sample section', ssub, qb));
  fs.writeFileSync(path.join(outDir, 'Sample_Solutions.html'), shell(title + ': Sample solutions', ssub, sb));
}
console.log('rendered', recs.length);
