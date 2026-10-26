import { cp, mkdir, rm } from 'node:fs/promises';
import { resolve } from 'node:path';
import { check } from './check.mjs';

const root = resolve(import.meta.dirname, '..');
await check();
await rm(resolve(root, 'dist'), { recursive: true, force: true });
await mkdir(resolve(root, 'dist'), { recursive: true });
await cp(resolve(root, 'public/reference'), resolve(root, 'dist/reference'), { recursive: true });
await cp(resolve(root, 'src/reference'), resolve(root, 'dist'), { recursive: true });
console.log('Built all Visualfolio pages and their original motion runtime into dist/.');
