// @ts-check
import { defineConfig } from 'astro/config';

// Static output for Cloudflare Pages. `file` format gives /audit.html, which Pages serves at /audit.
export default defineConfig({
  site: 'https://technehora.ai',
  trailingSlash: 'never',
  build: { format: 'file' },
  devToolbar: { enabled: false },
});
