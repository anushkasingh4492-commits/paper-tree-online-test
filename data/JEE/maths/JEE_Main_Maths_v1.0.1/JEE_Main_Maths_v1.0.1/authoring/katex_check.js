// Reads JSON [{id, field, text}] from stdin; renders every $...$ segment with KaTeX (throwOnError).
// Prints JSON list of failures.
const katex = require(__dirname + '/node_modules/katex');
let buf = '';
process.stdin.on('data', d => buf += d);
process.stdin.on('end', () => {
  const items = JSON.parse(buf);
  const fails = [];
  for (const it of items) {
    const t = it.text || '';
    // split on unescaped $
    const parts = t.split(/(?<!\\)\$/);
    if (parts.length % 2 === 0) { fails.push({...it, error: 'unbalanced $'}); continue; }
    for (let k = 1; k < parts.length; k += 2) {
      try { katex.renderToString(parts[k], {throwOnError: true, strict: 'ignore'}); }
      catch (e) { fails.push({id: it.id, field: it.field, error: String(e.message).slice(0, 160), math: parts[k].slice(0, 120)}); }
    }
  }
  console.log(JSON.stringify(fails));
});
