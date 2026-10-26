import { createServer } from 'node:http';
import { readFile, stat } from 'node:fs/promises';
import { resolve, extname, sep } from 'node:path';

const root = resolve(import.meta.dirname, '..');
const production = process.argv.includes('--production');
const pages = resolve(root, production ? 'dist' : 'src/reference');
const assets = resolve(root, production ? 'dist' : 'public');
const port = Number(process.env.PORT || 5173);
const mime = { '.pdf': 'application/pdf', '.html': 'text/html; charset=utf-8', '.mjs': 'text/javascript', '.js': 'text/javascript', '.json': 'application/json', '.css': 'text/css', '.svg': 'image/svg+xml', '.png': 'image/png', '.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.webp': 'image/webp', '.avif': 'image/avif', '.woff2': 'font/woff2', '.woff': 'font/woff', '.ttf': 'font/ttf', '.mp4': 'video/mp4', '.webm': 'video/webm' };
const server = createServer(async (request, response) => {
  try {
    const pathname = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (!production && pathname === '/__diagnostics' && request.method === 'POST') {
      let body = '';
      for await (const chunk of request) { body += chunk; if (body.length > 20000) break; }
      console.log('Browser diagnostic:', body);
      response.writeHead(204).end(); return;
    }
    const isAsset = pathname.startsWith('/reference/');
    const base = isAsset ? assets : pages;
    let file = resolve(base, '.' + pathname);
    if (file !== base && !file.startsWith(base + sep)) {
      response.writeHead(403).end(); return;
    }
    let status = 200;
    try {
      const entry = await stat(file);
      if (entry.isDirectory()) file = resolve(file, 'index.html');
    } catch {
      if (isAsset) { response.writeHead(404).end('Asset not found'); return; }
      file = resolve(pages, '404/index.html'); status = 404;
    }
    let data = await readFile(file);
    if (!production && extname(file) === '.html') {
      const diagnostics = `<script>window.addEventListener('error',e=>fetch('/__diagnostics',{method:'POST',body:JSON.stringify({message:e.message,stack:e.error?.stack,file:e.filename})}));window.addEventListener('unhandledrejection',e=>fetch('/__diagnostics',{method:'POST',body:String(e.reason?.stack||e.reason)}));</script>`;
      data = Buffer.from(data.toString().replace('<head>', '<head>' + diagnostics));
    }
    const headers = { 'Content-Type': mime[extname(file)] || 'application/octet-stream', 'Cache-Control': 'no-cache', 'X-Content-Type-Options': 'nosniff', 'Accept-Ranges': 'bytes' };
    const range = request.headers.range?.match(/^bytes=(\d+)-(\d*)$/);
    if (range && status === 200) {
      const start = Number(range[1]);
      const end = Math.min(range[2] ? Number(range[2]) : data.length - 1, data.length - 1);
      if (start > end) { response.writeHead(416, { 'Content-Range': `bytes */${data.length}` }).end(); return; }
      response.writeHead(206, { ...headers, 'Content-Range': `bytes ${start}-${end}/${data.length}`, 'Content-Length': end - start + 1 });
      response.end(request.method === 'HEAD' ? undefined : data.subarray(start, end + 1)); return;
    }
    response.writeHead(status, { ...headers, 'Content-Length': data.length });
    response.end(request.method === 'HEAD' ? undefined : data);
  } catch { response.writeHead(500).end('Unable to serve the page. Run npm run build before production preview.'); }
});
server.listen(port, '127.0.0.1', () => console.log(`Ajaymon ${production ? 'production preview' : 'local development'}: http://127.0.0.1:${port}`));
