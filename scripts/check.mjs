import { readFile, readdir, access } from 'node:fs/promises';
import { resolve, dirname } from 'node:path';

const root = resolve(import.meta.dirname, '..');
export async function check() {
  let files = 0;
  const errors = [];
  async function walk(dir) {
    for (const entry of await readdir(dir, { withFileTypes: true })) {
      const path = resolve(dir, entry.name);
      if (entry.isDirectory()) { await walk(path); continue; }
      if (!/\.(html|mjs|css|svg)$/.test(path)) continue;
      files++;
      const text = await readFile(path, 'utf8');
      const paths = new Set([...text.matchAll(/\/reference\/assets\/[^\s<>"'`\\)?#&]+/g)].map(match => resolve(root, 'public', '.' + match[0])));
      if (path.endsWith('.mjs')) {
        for (const match of text.matchAll(/["'`]((?:\.\/|\.\.\/)[^"'`\s]+\.mjs)["'`]/g)) paths.add(resolve(dirname(path), match[1]));
      }
      for (const asset of paths) {
        try { await access(asset); } catch { errors.push(`${path}: missing ${asset}`); }
      }
    }
  }
  await walk(resolve(root, 'src/reference'));
  await walk(resolve(root, 'public/reference'));
  if (errors.length) throw new Error(errors.join('\n'));
  console.log(`Checked ${files} source files: all local assets and module imports resolve.`);
}
if (process.argv[1] === import.meta.filename) await check();
