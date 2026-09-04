// Password gate for the whole site (Vercel Edge Middleware, works on the Hobby plan).
// Set SITE_USER and SITE_PASS in the Vercel project's Environment Variables; nothing is served without them.
export const config = { matcher: '/:path*' };

export default function middleware(request) {
  const user = process.env.SITE_USER;
  const pass = process.env.SITE_PASS;
  if (!user || !pass) {
    return new Response('Site password is not configured (SITE_USER / SITE_PASS).', { status: 503 });
  }
  const auth = request.headers.get('authorization') || '';
  const expected = 'Basic ' + btoa(`${user}:${pass}`);
  if (auth === expected) return; // authenticated: let the static file through
  return new Response('Authentication required', {
    status: 401,
    headers: {
      'WWW-Authenticate': 'Basic realm="Interface Craft", charset="UTF-8"',
      'Cache-Control': 'no-store',
    },
  });
}
