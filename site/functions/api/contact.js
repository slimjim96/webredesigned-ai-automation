// POST /api/contact: the fallback form on /book, emailed to the owner (Cloudflare Pages Function).
//
// Settings (Cloudflare Pages → Settings → Variables and Secrets):
//   RESEND_API_KEY    secret  Resend API key; Resend sends the email (free tier is plenty)
//   CONTACT_TO        plain   where notes go, e.g. hello@technehora.ai
//   CONTACT_FROM      plain   a sender on a domain verified in Resend, e.g. "Techne Hora site <site@technehora.ai>"
//   TURNSTILE_SECRET  secret  Cloudflare Turnstile secret; when set, every note must pass the check
//
// Answers JSON ({ ok: true } or { ok: false, error }) to the page's script. The form needs JavaScript
// (Turnstile does too); without it, /book shows the phone and email instead.

const LIMITS = { name: 200, business: 200, contact: 200, question: 2000 };
const CONTACT = /^(\+?1[\s.-]?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}$|^[^\s@]+@[^\s@]+\.[^\s@]+$/;
const EMAIL = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

function reply(status, body) {
  return new Response(JSON.stringify(body), { status, headers: { 'Content-Type': 'application/json' } });
}

async function passesTurnstile(env, token, ip) {
  if (!env.TURNSTILE_SECRET) return true;
  if (!token) return false;
  const res = await fetch('https://challenges.cloudflare.com/turnstile/v0/siteverify', {
    method: 'POST',
    body: new URLSearchParams({ secret: env.TURNSTILE_SECRET, response: token, ...(ip ? { remoteip: ip } : {}) }),
  });
  const data = await res.json();
  return data.success === true;
}

export async function onRequestPost({ request, env }) {
  let form;
  try { form = await request.formData(); } catch { return reply(400, { ok: false, error: 'bad-request' }); }

  // Bots fill the hidden field; tell them it worked and send nothing.
  if (String(form.get('website') || '').trim()) return reply(200, { ok: true });

  const v = Object.fromEntries(Object.keys(LIMITS).map((k) => [k, String(form.get(k) || '').trim()]));
  const tooLong = Object.entries(LIMITS).some(([k, max]) => v[k].length > max);
  if (!v.name || !v.business || !CONTACT.test(v.contact) || tooLong) return reply(422, { ok: false, error: 'invalid' });

  const ip = request.headers.get('CF-Connecting-IP');
  if (!(await passesTurnstile(env, form.get('cf-turnstile-response'), ip))) return reply(403, { ok: false, error: 'turnstile' });

  if (!env.RESEND_API_KEY || !env.CONTACT_TO || !env.CONTACT_FROM) return reply(503, { ok: false, error: 'not-configured' });

  const text = [
    `Name: ${v.name}`,
    `Business: ${v.business}`,
    `Phone or email: ${v.contact}`,
    '',
    'What eats most of their week:',
    v.question || '(left blank)',
    '',
    'Sent from the form on technehora.ai/book. Promised reply: within one business day.',
  ].join('\n');

  const res = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: env.CONTACT_FROM,
      to: [env.CONTACT_TO],
      subject: `Website note from ${v.name} (${v.business})`,
      text,
      ...(EMAIL.test(v.contact) ? { reply_to: v.contact } : {}),
    }),
  });
  if (!res.ok) return reply(502, { ok: false, error: 'send-failed' });
  return reply(200, { ok: true });
}
