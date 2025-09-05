(function () {
  const vscode = acquireVsCodeApi();
  const mode = document.getElementById('mode');
  const text = document.getElementById('text');
  const ctx = document.getElementById('context');
  const out = document.getElementById('out');
  const run = document.getElementById('run');
  const insert = document.getElementById('insert');

  run.addEventListener('click', () => {
    out.textContent = 'Running…';
    vscode.postMessage({ type: 'generate', mode: mode.value, text: text.value, context: ctx.value });
  });

  insert.addEventListener('click', () => {
    vscode.postMessage({ type: 'insertLast' });
  });

  window.addEventListener('message', (event) => {
    const msg = event.data;
    if (msg.type === 'result') {
      if (!msg.ok) {
        out.textContent = '❌ ' + (msg.error || 'Unknown error');
        return;
      }
      if (msg.json) {
        // pretty print JSON with code blocks if present
        const j = msg.json;
        let html = '<pre>' + escapeHtml(JSON.stringify(j, null, 2)) + '</pre>';
        if (j.code) html += '<h4>Code</h4><pre>' + escapeHtml(j.code) + '</pre>';
        if (j.fixed_code) html += '<h4>Fixed Code</h4><pre>' + escapeHtml(j.fixed_code) + '</pre>';
        out.innerHTML = html;
      } else if (msg.text) {
        out.innerHTML = '<pre>' + escapeHtml(msg.text) + '</pre>';
      } else {
        out.textContent = 'No result.';
      }
    }
  });

  function escapeHtml(s) {
    return s.replace(/[&<>]/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));
  }
})();