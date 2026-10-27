# Development section — English content. Each lesson: id, title, lede, body (why + how), details, sources.
def L(*pairs):
    return ' · '.join('<a href="%s" target="_blank" rel="noopener">%s</a>' % (u, t) for t, u in pairs)

HEAD = dict(eyebrow='Section 10', title='Development', desc='Shipping a real web app with accounts, shared profiles and private data, without leaking any of it. HTTP, authentication, Postgres and Row Level Security, the OWASP failures, secrets and infrastructure, and the LGPD as a product requirement, for any app where people sign in and keep things that are theirs.')

EN = [
dict(id='how-the-web-talks', title='How the Web Talks',
lede='Every screen you design is a sequence of HTTP requests. Method says intent, path says resource, status says what happened. Reading them in the Network tab is the first security skill, because everything else is about who may send which request.',
body='''<h3>Why</h3>
          <p>A web app is a browser talking to an API over HTTP. The browser sends a request with a method, a path, headers and sometimes a body; the server answers with a status code, headers and a body, usually JSON. The methods carry meaning: GET reads, POST creates, PATCH changes part of something, DELETE removes. Status codes carry the outcome: 200 ok, 201 created, 204 done with nothing to return, 400 you sent something wrong, 401 you are not identified, 403 you are identified and still not allowed, 404 not here, 429 slow down, 500 we broke. The difference between 401 and 403 is the difference between authentication and authorization, and it shows up in the Network tab long before it shows up in a design.</p>
          <p>Headers are where the interesting security material lives. The request carries the token or cookie that identifies the person; the response carries the policies that constrain the browser. Open DevTools on any app you use, filter by Fetch/XHR, and read one request end to end. You will see what the app sends, what it gets back, and how little the pretty interface has to do with what the server actually enforces. One rule for this whole section: never paste a real token or cookie into a screenshot or a chat. Treat them as passwords, because they are.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Read the Network tab</strong> of your own app once a week. Method, path, status, headers, body.</li>
            <li><strong>Use methods for meaning.</strong> A GET never changes data; a DELETE never pretends to be a POST.</li>
            <li><strong>Map status codes to UI states:</strong> 401 goes to login, 403 says "not yours", 404 says "nothing here", 429 asks to wait.</li>
            <li><strong>Draw the diagram</strong> React → Supabase (Auth, PostgREST, Storage) with every arrow labeled by what it carries.</li>
          </ul>''',
details=['<strong>401 and 403 are different screens.</strong> One asks who you are, the other says no.',
 '<strong>204 means success with an empty body;</strong> do not show an error because the JSON was empty.',
 '<strong>Idempotency:</strong> GET, PUT and DELETE can be repeated safely; POST cannot.',
 '<strong>The body of a 4xx is for developers;</strong> the UI copy is yours.',
 '<strong>Tokens in screenshots are leaks.</strong> Redact before sharing.'],
sources=L(('MDN, An overview of HTTP', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview'), ('MDN, HTTP response status codes', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status'), ('MDN, HTTP request methods', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods'))),

dict(id='what-tls-protects', title='What TLS Protects',
lede='HTTPS encrypts the conversation between the browser and the server. It hides the content and the path, verifies you reached the right server, and stops tampering in transit. It does nothing for data at rest, nothing against a malicious page, and nothing about who the server lets in.',
body='''<h3>Why</h3>
          <p>Transport Layer Security wraps HTTP so that someone on the same network, the ISP, or a hostile proxy sees only which host you connected to and roughly how much data moved. Headers, cookies, tokens, request bodies and responses are all inside the tunnel. The certificate proves the server is who the domain says it is, which is what defeats a fake "login page" sitting between you and the real one. Cloudflare Pages and Supabase give you this by default, with certificates renewed for you; your job is to never offer a plain-HTTP path and to tell browsers to stop trying one, through HSTS.</p>
          <p>The limits matter as much as the guarantees. TLS protects bytes in motion, not bytes stored in the database, in backups, or in a log line. It does not stop a script injected into your page from reading what the page can read. It does not decide whether user B may see user A's private resource; that is authorization, inside the tunnel, decided by the server. "The site has the padlock" means exactly one thing: the network between the person and your server is not the weak point.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>HTTPS everywhere, no exceptions,</strong> including the API base URL in your config.</li>
            <li><strong>Enable HSTS</strong> on the Pages project so browsers refuse plain HTTP after the first visit.</li>
            <li><strong>Do not mistake the padlock for safety.</strong> It covers transit, not storage, scripts or permissions.</li>
            <li><strong>Mixed content is a break:</strong> an http image or script on an https page weakens the page.</li>
          </ul>''',
details=['<strong>What the network still sees:</strong> the hostname (SNI), timing and sizes.',
 '<strong>Certificates expire;</strong> managed platforms renew them, self-hosted ones need a job.',
 '<strong>HSTS preload</strong> is a commitment; add it only when every subdomain is ready.',
 '<strong>Local dev over http is fine;</strong> production over http is not.',
 '<strong>TLS is not encryption at rest.</strong> Ask what encrypts the database and the backups.'],
sources=L(('MDN, Transport Layer Security', 'https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security'), ('web.dev, Why HTTPS matters', 'https://web.dev/articles/why-https-matters'), ('MDN, Strict-Transport-Security', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security'), ('OWASP, TLS cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html'))),

dict(id='cookies-sessions-storage', title='Cookies, Sessions and Browser Storage',
lede='The browser keeps state in three places: cookies, which travel with requests; localStorage and sessionStorage, which scripts read; and memory, which vanishes on reload. Where the session token lives decides which attacks can steal it.',
body='''<h3>Why</h3>
          <p>A session is the server remembering who you are between requests. The usual carrier is a token, and the token has to be stored somewhere in the browser. Cookies are sent automatically with every request to their domain, which is convenient and also the root of CSRF; with the HttpOnly flag a script cannot read them, which is the best defense against XSS stealing them; with Secure they only travel over HTTPS; with SameSite they stop being attached to cross-site requests. localStorage is the opposite trade: nothing is sent automatically, so CSRF is moot, but any script running on the page can read it, so one XSS hole hands over every session.</p>
          <p>Supabase's browser client stores the session in localStorage by default; server-side rendering setups move it to cookies. Either choice is defensible once you know what it costs: with localStorage, XSS is the whole game and the Content Security Policy becomes mandatory; with cookies, SameSite and CSRF protections become mandatory. What is never defensible is a token in a URL, a token in a log, or a token that never expires. Headers are the third storage you do not control: the Authorization header is how a token reaches the API on each call, and the Network tab shows it in clear text to anyone with the laptop open.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Know where your session lives</strong> and write the matching defenses: CSP for localStorage, SameSite and CSRF tokens for cookies.</li>
            <li><strong>Cookies get HttpOnly, Secure and SameSite</strong> by default, every time.</li>
            <li><strong>Nothing sensitive in sessionStorage either;</strong> it is script-readable too, just shorter-lived.</li>
            <li><strong>Never put a token in a URL.</strong> URLs end up in logs, history and referrers.</li>
          </ul>''',
details=['<strong>HttpOnly is for the token, not for preferences.</strong> Theme can live in localStorage.',
 '<strong>SameSite=Lax is the sensible default;</strong> Strict breaks links from email, None needs Secure.',
 '<strong>Logout must clear the storage,</strong> not only the UI state.',
 '<strong>Shared computers:</strong> a persisted session is a decision, offer "keep me signed in" explicitly.',
 '<strong>Inspect Application → Storage</strong> in DevTools to see exactly what your app leaves behind.'],
sources=L(('MDN, Using HTTP cookies', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies'), ('OWASP, Session management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'), ('OWASP, HTML5 security cheat sheet (local storage)', 'https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html'), ('Supabase, Sessions', 'https://supabase.com/docs/guides/auth/sessions'))),

dict(id='same-origin-and-cors', title='Same-Origin Policy and CORS',
lede='The browser stops a page on one origin from reading responses from another. CORS is the server saying which origins may. It protects users from malicious pages; it does not protect your API from anyone with curl.',
body='''<h3>Why</h3>
          <p>An origin is scheme plus host plus port. The same-origin policy says a script on evil.example cannot read the response of a request to your API, even if the browser sent it. That is a user protection: it keeps a random page from pulling your logged-in data through the user's own browser. CORS loosens it on purpose: the API answers with Access-Control-Allow-Origin naming the origins that may read, and for non-simple requests the browser first sends a preflight OPTIONS to ask. Supabase allows your project to be called from any origin because the real gate is the token and Row Level Security, not the origin.</p>
          <p>The misunderstanding to kill early: CORS is enforced by browsers, for browsers. A script, a mobile app, Postman or curl ignores it entirely. If your API only works because "the frontend is the only thing calling it", it is open. Likewise a wildcard Allow-Origin with credentials is a misconfiguration the browser will refuse, and a reflected Allow-Origin (echoing whatever origin asked) is an open door for the attacks the policy exists to prevent. The rule: assume every endpoint will be called directly, by anyone, and make the database say no.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Treat CORS as a browser courtesy,</strong> never as access control.</li>
            <li><strong>Allow specific origins,</strong> never reflect the request origin, never wildcard with credentials.</li>
            <li><strong>Every endpoint must be safe to call with curl</strong> and a stolen or absent token.</li>
            <li><strong>Read the preflight</strong> in the Network tab once, so OPTIONS stops being mysterious.</li>
          </ul>''',
details=['<strong>Scheme, host, port:</strong> https://app and http://app are different origins.',
 '<strong>Site vs origin:</strong> SameSite cookies use the site; CORS uses the origin.',
 '<strong>Preflight caches;</strong> a failing OPTIONS shows up as a vague "network error" in the console.',
 '<strong>Supabase is origin-agnostic by design;</strong> RLS is the gate.',
 '<strong>If removing the frontend would expose data,</strong> the backend was never protected.'],
sources=L(('MDN, Same-origin policy', 'https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy'), ('MDN, Cross-Origin Resource Sharing', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS'), ('PortSwigger, CORS', 'https://portswigger.net/web-security/cors'), ('web.dev, Same-site and same-origin', 'https://web.dev/articles/same-site-same-origin'))),

dict(id='authentication-vs-authorization', title='Authentication vs Authorization',
lede='Authentication answers who you are. Authorization answers what you may do. Most real breaches are authorization failures: the system knew exactly who the person was and still handed them someone else\'s data.',
body='''<h3>Why</h3>
          <p>Logging in proves identity: this request comes from the account that knows the password, holds the magic link, or passed the second factor. It says nothing about permissions. Authorization is the separate decision, made on every request, that this identity may read this resource, edit this record, delete this account. The two are confused constantly because the login screen is visible and the permission check is not. OWASP has put Broken Access Control at the top of its list since 2021 precisely because teams build beautiful login flows and then trust the frontend to hide the buttons users should not press.</p>
          <p>For most apps with user-owned data, the authorization model is small and must be written down: a visitor can read public resources; a signed-in person can read public resources and everything they own; nobody but the owner can write. That matrix is the specification. It gets enforced in the database, through Row Level Security, so that every path to the data, the app, a direct API call, a future mobile client, obeys the same rules. Hiding an Edit button is interface; denying the UPDATE is security. Both are needed, in that order of importance reversed.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Write the permission matrix</strong> before writing a table: operation × role, with Yes or No in each cell.</li>
            <li><strong>Enforce in the database,</strong> reflect in the UI. Never the other way around.</li>
            <li><strong>Authorize on every request,</strong> not once at login.</li>
            <li><strong>Test as three people:</strong> a visitor, the owner, another user, for every operation.</li>
          </ul>''',
details=['<strong>"Logged in" is not a permission.</strong> It is an identity.',
 '<strong>Default deny:</strong> everything is forbidden until a rule allows it.',
 '<strong>Owner is a column, not a feeling:</strong> user_id on every row that belongs to someone.',
 '<strong>Admin is a role with its own audit,</strong> not a shared password.',
 '<strong>The matrix is the test plan.</strong> Each cell is one test.'],
sources=L(('Auth0, Authentication vs. authorization', 'https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization'), ('OWASP, Authorization cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'), ('OWASP Top 10, A01 Broken Access Control', 'https://owasp.org/Top10/A01_2021-Broken_Access_Control/'))),

dict(id='auth-flows', title='Sign Up, Sign In, Recover',
lede='Account flows are where security and UX meet hardest. Email verification, password rules, recovery links and logout each have a correct shape, and Supabase Auth implements most of it, but the product still has to decide what is required and what the person sees.',
body='''<h3>Why</h3>
          <p>Sign-up creates an identity; sign-in proves it; logout ends the session; recovery lets someone back in without the password. Each step is an attack surface. Unverified emails let people register addresses they do not own, which later become a way to hijack accounts or spam. Weak password rules invite credential stuffing; the fix is a minimum length, a check against breached passwords, and no composition rules that produce "Password1!". Recovery is the classic hole: a link that never expires, that works more than once, or that reveals whether an email exists, hands accounts to attackers. Logout that only clears the UI leaves a valid token on the device.</p>
          <p>Supabase Auth gives you sign-up with confirmation emails, password sign-in, magic links, OAuth providers, password recovery and session handling. The decisions left to you are product decisions: require verification before any write; show the same neutral message whether or not the email exists; expire recovery links fast and once; invalidate other sessions on password change; and make "Sign out" revoke the refresh token, not only drop the local state. Document the flow as a diagram with every state, including the sad ones, because that diagram is also the UX spec.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Require email verification</strong> before the account can create or share anything.</li>
            <li><strong>Neutral messages:</strong> "If that email exists, we sent a link", for sign-up, recovery and login errors alike.</li>
            <li><strong>Recovery links expire and are single-use;</strong> password change invalidates other sessions.</li>
            <li><strong>Sign out revokes</strong> the session server-side and clears local storage.</li>
          </ul>''',
details=['<strong>Minimum 12 characters, no composition rules,</strong> check against known breaches.',
 '<strong>The verification email is part of the product:</strong> write it, test it, brand it.',
 '<strong>Custom SMTP in production;</strong> the default sender has strict limits.',
 '<strong>Redirect targets are allowlisted,</strong> never taken from a query string.',
 '<strong>Two test accounts, always.</strong> One is never enough to find an authorization bug.'],
sources=L(('Supabase, Auth overview', 'https://supabase.com/docs/guides/auth'), ('Supabase, Password-based auth', 'https://supabase.com/docs/guides/auth/passwords'), ('Supabase, Password security', 'https://supabase.com/docs/guides/auth/password-security'), ('OWASP, Forgot password cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html'), ('OWASP, Authentication cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'))),

dict(id='tokens-and-sessions', title='Tokens, JWTs and Expiry',
lede='A JWT is a signed statement about who the holder is, valid until it expires. Short-lived access tokens limit the damage of theft; refresh tokens extend the session without a new login. Signed is not encrypted: anyone can read a JWT.',
body='''<h3>Why</h3>
          <p>After login, Supabase issues an access token, a JSON Web Token signed by the project, and a refresh token. The access token travels with every API call in the Authorization header; Postgres reads its claims, which is how auth.uid() knows who is asking. It expires in about an hour by default. When it does, the client uses the refresh token to get a new pair, silently. The design is a trade: short access tokens mean a stolen one is useful briefly; refresh tokens mean the person does not log in every hour. Refresh token rotation, on by default, makes each refresh token single-use, so a stolen one that is replayed after the legitimate client used it gets the whole session revoked.</p>
          <p>Three facts prevent most JWT mistakes. One: the payload is base64, not encrypted, so never put secrets in it and assume the person can read their own claims. Two: the server does not look the token up; it verifies the signature, which is why revocation is hard and expiry is the real control. Three: the signing secret and the service role key are the keys to the kingdom; they never leave the server. Session expiry is also a product decision: a low-risk app does not need bank-grade timeouts, but "remember me forever" on a shared computer is a choice to make consciously, with a visible way to sign out everywhere.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Keep access tokens short,</strong> let the client refresh silently, keep rotation on.</li>
            <li><strong>Never trust client-side claims for permissions;</strong> the database verifies the signature and applies RLS.</li>
            <li><strong>Offer "sign out of all devices"</strong> and trigger it on password change.</li>
            <li><strong>Decode a token once in jwt.io</strong> with a test account, so you know exactly what it carries.</li>
          </ul>''',
details=['<strong>exp is the control.</strong> Everything else about a JWT is convenience.',
 '<strong>Rotation detects reuse:</strong> a replayed refresh token kills the session.',
 '<strong>The role claim is "authenticated" or "anon",</strong> not your app\'s admin flag.',
 '<strong>Clock skew exists;</strong> do not panic over a token rejected a few seconds early.',
 '<strong>Tokens in logs are credentials in logs.</strong> Scrub the Authorization header.'],
sources=L(('Supabase, JSON Web Tokens', 'https://supabase.com/docs/guides/auth/jwts'), ('Supabase, User sessions', 'https://supabase.com/docs/guides/auth/sessions'), ('jwt.io, Introduction to JSON Web Tokens', 'https://jwt.io/introduction'), ('PortSwigger, JWT attacks', 'https://portswigger.net/web-security/jwt'))),

dict(id='account-abuse', title='Rate Limits, CAPTCHA, MFA and Redirects',
lede='Attackers automate. Rate limits make guessing expensive, CAPTCHA raises the cost of bots where it is worth the friction, MFA protects the accounts that matter most, and a redirect allowlist keeps your login from becoming a phishing launcher.',
body='''<h3>Why</h3>
          <p>A login form without limits is an oracle: try a million passwords, keep the ones that work. Supabase applies rate limits on auth endpoints and lets you tune them; your app should also back off on the client, show the 429 as "too many attempts, wait a minute", and never reveal whether the email or the password was the wrong half. CAPTCHA, through providers like Cloudflare Turnstile, belongs on sign-up and recovery, where bots create junk accounts and trigger email floods, and should stay off the daily login path unless abuse appears, because every challenge is friction paid by honest people.</p>
          <p>Multi-factor authentication is the single biggest upgrade for the accounts that can do damage: yours, as the admin, and any role with elevated rights. Supabase supports TOTP; requiring it for admin logins costs seconds and removes the password as a single point of failure. Redirects are the quiet one: auth flows send people back to a URL after login or recovery, and if that URL comes from the request, a crafted link logs someone in on your real site and lands them on an attacker's page. Supabase only redirects to URLs you register; keep that list tight and never append to it from user input.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Rate limits on auth and on any endpoint that sends email;</strong> show 429 as a calm "wait".</li>
            <li><strong>CAPTCHA on sign-up and recovery,</strong> not on every login, unless you see abuse.</li>
            <li><strong>MFA required for admin accounts,</strong> optional for everyone else, with recovery codes.</li>
            <li><strong>Redirect allowlist only.</strong> No open redirects, no redirect from query strings.</li>
          </ul>''',
details=['<strong>Same error for wrong email and wrong password.</strong> Enumeration starts with a helpful message.',
 '<strong>Lockouts are a denial-of-service vector;</strong> prefer backoff over hard locks.',
 '<strong>Turnstile over image puzzles:</strong> invisible for most people, costly for bots.',
 '<strong>Admin is a separate login story,</strong> with MFA and its own audit log.',
 '<strong>Test a crafted redirect once</strong> to see the allowlist refuse it.'],
sources=L(('Supabase, Rate limits', 'https://supabase.com/docs/guides/auth/rate-limits'), ('Supabase, Bot detection with CAPTCHA', 'https://supabase.com/docs/guides/auth/auth-captcha'), ('Supabase, Multi-factor authentication', 'https://supabase.com/docs/guides/auth/auth-mfa'), ('Supabase, Redirect URLs', 'https://supabase.com/docs/guides/auth/redirect-urls'), ('OWASP, Unvalidated redirects cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html'), ('Cloudflare Turnstile', 'https://developers.cloudflare.com/turnstile/'))),

dict(id='data-model', title='Modeling Owners, Resources and Items',
lede='Three tables carry the pattern: profiles, resources, items. Foreign keys make the relations real, constraints make bad data impossible, and the owner column on every row is what Row Level Security will later check. Model for the permissions you will need.',
body='''<h3>Why</h3>
          <p>Supabase keeps authentication in auth.users, which you do not edit directly. The public profile (display name, handle, avatar) lives in a profiles table keyed by the same id, created by a trigger when a user signs up. Resources reference the profile through a user_id foreign key and carry a visibility column; items reference their parent resource. Foreign keys with ON DELETE CASCADE mean deleting an account removes its resources and items, which is both tidy and, as you will see in the LGPD lessons, a legal need. Constraints do the rest of the hygiene: NOT NULL where a value is required, UNIQUE on the handle, CHECK on visibility so only the three allowed values exist, and a length limit on titles so nobody stores a novel.</p>
          <p>Indexes make the common queries fast: resources by user_id, items by resource_id, profiles by handle. Primary keys as UUIDs instead of sequential integers close the cheapest attack there is, guessing the next id, though UUIDs are not a substitute for authorization. Write the schema as SQL migrations in the repository, not as clicks in a dashboard; versioned SQL is what lets you rebuild the database, review a change, and know which policy existed when.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>profiles(id → auth.users), resources(user_id, visibility), items(resource_id).</strong> Owner column on everything owned.</li>
            <li><strong>Constraints before code:</strong> NOT NULL, UNIQUE, CHECK, length limits.</li>
            <li><strong>UUID primary keys,</strong> and indexes on every foreign key you filter by.</li>
            <li><strong>Migrations in git.</strong> The dashboard is for reading, the repository is for truth.</li>
          </ul>''',
details=['<strong>Never store the email in profiles</strong> unless you need it public; auth.users already has it.',
 '<strong>CASCADE deletes are a design decision;</strong> write down what disappears with an account.',
 '<strong>Timestamps with time zone,</strong> created_at and updated_at on every table.',
 '<strong>Visibility as a CHECK constraint,</strong> not a free string.',
 '<strong>Seed with fictional data</strong> and keep a script to reset it.'],
sources=L(('Supabase, Managing user data', 'https://supabase.com/docs/guides/auth/managing-user-data'), ('PostgreSQL, Constraints', 'https://www.postgresql.org/docs/current/ddl-constraints.html'), ('PostgreSQL, Indexes', 'https://www.postgresql.org/docs/current/indexes.html'), ('Supabase, Cascade deletes', 'https://supabase.com/docs/guides/database/postgres/cascade-deletes'), ('PostgreSQL, Tutorial', 'https://www.postgresql.org/docs/current/tutorial.html'))),

dict(id='row-level-security', title='Row Level Security',
lede='RLS turns authorization into database rules: each table gets policies that say which rows a given user may select, insert, update or delete. With auth.uid() in the policy, the database itself refuses what the person may not do, whoever is asking and from wherever.',
body='''<h3>Why</h3>
          <p>Supabase exposes your tables through an API that the browser calls directly with the person\'s token. That only works because Row Level Security is on: a table without RLS and with the anon key in the client is public to the world. With RLS enabled, Postgres evaluates a policy for every row on every operation. The policy can read auth.uid(), the id from the verified token, and compare it with the owner column. One policy per operation keeps the logic readable: SELECT allows owners and, for public resources, everyone; INSERT checks that the new row\'s user_id is the caller; UPDATE and DELETE allow only the owner. Policies are additive: if any policy permits, the row passes, so a permissive leftover from testing is a hole.</p>
          <p>Two practices keep RLS honest. First, test it from outside the UI: run the same query as a visitor with no token, as user A, as user B, through the API, and compare the rows. Second, keep the policies in migrations and review them like code, because a policy is code. Performance follows: wrap auth.uid() in a subselect so it is evaluated once, index the columns policies compare, and avoid joins inside policies. Supabase\'s advisors flag tables without RLS and policies that look wrong; run them before every release.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>ALTER TABLE … ENABLE ROW LEVEL SECURITY</strong> on every table, before the first row.</li>
            <li><strong>One policy per operation,</strong> named for what it allows: "owners update their resources".</li>
            <li><strong>INSERT uses WITH CHECK</strong> so nobody creates rows owned by someone else.</li>
            <li><strong>Test from the API as three people</strong> and keep the results as a table in the repo.</li>
          </ul>''',
details=['<strong>No RLS plus anon key equals public table.</strong> There is no middle state.',
 '<strong>Policies are OR-ed.</strong> Delete the "allow all for testing" one.',
 '<strong>(select auth.uid())</strong> instead of auth.uid() for speed on big tables.',
 '<strong>service_role bypasses RLS,</strong> which is why it never reaches the client.',
 '<strong>Views and functions need their own thought;</strong> security definer functions skip RLS.'],
sources=L(('Supabase, Row Level Security', 'https://supabase.com/docs/guides/database/postgres/row-level-security'), ('PostgreSQL, Row security policies', 'https://www.postgresql.org/docs/current/ddl-rowsecurity.html'), ('PostgreSQL, CREATE POLICY', 'https://www.postgresql.org/docs/current/sql-createpolicy.html'), ('Supabase, Securing your data', 'https://supabase.com/docs/guides/database/secure-data'), ('Supabase, Database advisors', 'https://supabase.com/docs/guides/database/database-advisors'))),

dict(id='visibility-tiers', title='Public, Unlisted, Private',
lede='A user-owned resource has three audiences: anyone, anyone with the link, only the owner. Each tier is a policy in the database and a sentence in the interface. If the sentence promises more than the policy enforces, the product is lying.',
body='''<h3>Why</h3>
          <p>Public resources appear in search and on the profile; unlisted ones open for anyone who has the URL but are not listed anywhere; private ones are the owner\'s alone. The difference is trivial in the UI and decisive in the database. Public: SELECT allowed for everyone where visibility = public. Unlisted: SELECT allowed for everyone by id, but the listing query that feeds the profile page excludes them, so discovery depends on knowing the UUID, which is why the id must be unguessable. Private: SELECT only for the owner. Items inherit the parent\'s visibility through a policy that joins to the parent, or through a denormalized column kept in sync by a trigger.</p>
          <p>The interface has to say exactly what each tier means, where the person chooses it, in plain words: "Anyone can find this", "Only people with the link", "Only you". The LGPD\'s transparency principle makes this more than good manners. And the default matters: a new resource should be private until the person decides otherwise, because an accidentally public one is a data leak the person did not consent to. Test the tiers the way an attacker would: fetch an unlisted resource by id without a token, list a profile\'s resources and check that unlisted ones are absent, fetch a private one as another user and expect nothing back.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Three values, one CHECK constraint, three policies.</strong> No other states.</li>
            <li><strong>Private by default.</strong> Sharing is an action the person takes.</li>
            <li><strong>Plain-language labels</strong> at the control, not in a help page.</li>
            <li><strong>Children follow the parent;</strong> never let an item be more visible than its parent.</li>
          </ul>''',
details=['<strong>Unlisted means unguessable:</strong> UUID v4 ids, no sequential numbers anywhere.',
 '<strong>Changing to private must take effect immediately,</strong> including cached pages and images.',
 '<strong>Search indexes only public resources;</strong> unlisted must never leak via search.',
 '<strong>The share dialog repeats the visibility</strong> at the moment of copying the link.',
 '<strong>Image URLs follow the tier too;</strong> a private resource with public image URLs is not private.'],
sources=L(('Supabase, Row Level Security', 'https://supabase.com/docs/guides/database/postgres/row-level-security'), ('OWASP, Authorization cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'), ('ANPD, materiais educativos', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'))),

dict(id='broken-access-control', title='Broken Access Control and IDOR',
lede='Change the id in the URL and see someone else\'s data: that is an Insecure Direct Object Reference, the most common serious bug on the web. The fix is never to hide the id; it is to make every query check ownership, which RLS does if the policies are right.',
body='''<h3>Why</h3>
          <p>OWASP ranks Broken Access Control first because it is everywhere and it is simple: the app checks who you are, fetches the record you asked for, and forgets to check whether the record is yours. The API version is called BOLA, Broken Object Level Authorization. Symptoms: changing /resources/42 to /resources/43 shows another person\'s private resource; a PATCH to someone else\'s item succeeds; an export endpoint returns everyone\'s data because the filter was applied in the frontend. Unguessable ids slow this down and do not fix it; an attacker who ever sees an id, in a shared link or a screenshot, has it forever.</p>
          <p>The defense is structural. With RLS enabled and correct, the query that fetches resource 43 returns nothing for the wrong user, whatever the frontend sent. The remaining work is testing: for every operation in the permission matrix, perform it as the wrong user through the API and confirm the refusal. Keep a document of these tests with the request, the expected result, and the actual result; it is the evidence your access control works, and the first thing to rerun after any schema change. Also watch the second-order paths: joins that pull related rows, functions that run with elevated rights, and storage files whose URLs skip the database entirely.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Every object fetch is filtered by ownership or visibility,</strong> in the database.</li>
            <li><strong>Test id swapping</strong> on every endpoint, as a visitor and as another user.</li>
            <li><strong>Unguessable ids are a courtesy,</strong> not a control.</li>
            <li><strong>Keep the offensive test log</strong> next to the schema and rerun it on change.</li>
          </ul>''',
details=['<strong>Deny by default returns empty or 404,</strong> not 403 with the object\'s name.',
 '<strong>Mass assignment is the cousin:</strong> never let the client set user_id or visibility on another\'s row.',
 '<strong>Bulk endpoints filter per row,</strong> not per request.',
 '<strong>Functions with SECURITY DEFINER</strong> need their own ownership checks.',
 '<strong>Automate the three-user test</strong> once it works by hand.'],
sources=L(('OWASP Top 10, A01 Broken Access Control', 'https://owasp.org/Top10/A01_2021-Broken_Access_Control/'), ('PortSwigger, Access control vulnerabilities', 'https://portswigger.net/web-security/access-control'), ('PortSwigger, IDOR', 'https://portswigger.net/web-security/access-control/idor'), ('OWASP API Security, Broken Object Level Authorization', 'https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/'))),

dict(id='xss-and-safe-rendering', title='XSS and Safe Rendering',
lede='Cross-site scripting is user content executing as code in another user\'s browser. The defense is to render text as text: React does it by default, dangerouslySetInnerHTML undoes it, and a Content Security Policy catches what slips through.',
body='''<h3>Why</h3>
          <p>Every app stores text people type: titles, notes, profile bios, URLs. If any of it is inserted into the page as HTML, a note containing a script tag runs in the browser of everyone who views the page, with their session. That is stored XSS, and with the session in localStorage it is game over for every viewer. React escapes text in JSX, so the ordinary path is safe; the holes are the escape hatches: dangerouslySetInnerHTML, writing to innerHTML, building HTML strings, and attributes that take URLs, where javascript: links execute on click. Markdown rendering is a classic source, because the renderer produces HTML from untrusted text.</p>
          <p>The rules are short. Never render user content as HTML unless it has passed a sanitizer like DOMPurify with an allowlist of tags. Validate URLs before using them as href or src: only http and https, nothing else. Set a Content Security Policy that forbids inline scripts, so even an injected tag does not run. And test with the payloads that matter: a script tag, an img with onerror, a javascript: URL, an svg with onload, in every field that is later displayed. Output encoding is contextual, which is why "escape everything" is not a strategy; the context (HTML text, attribute, URL, JavaScript) decides the encoding.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Text stays text.</strong> No dangerouslySetInnerHTML with user content, ever.</li>
            <li><strong>Sanitize with an allowlist</strong> if you must render rich text; DOMPurify, not a regex.</li>
            <li><strong>Allow only http(s) in URLs</strong> people enter; render the rest as plain text.</li>
            <li><strong>CSP without unsafe-inline</strong> as the second layer.</li>
          </ul>''',
details=['<strong>Markdown is HTML with extra steps;</strong> sanitize after rendering.',
 '<strong>Test fields with</strong> &lt;img src=x onerror=alert(1)&gt; and a javascript: link.',
 '<strong>DOM XSS lives in the client:</strong> location.hash into innerHTML is a classic.',
 '<strong>rel="noopener"</strong> on links to user-provided URLs.',
 '<strong>Third-party scripts share your origin;</strong> load as few as possible.'],
sources=L(('PortSwigger, Cross-site scripting', 'https://portswigger.net/web-security/cross-site-scripting'), ('OWASP, XSS prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'), ('OWASP, DOM-based XSS prevention', 'https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html'), ('React, dangerouslySetInnerHTML', 'https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html'), ('DOMPurify', 'https://github.com/cure53/DOMPurify'))),

dict(id='sql-injection', title='SQL Injection',
lede='Injection happens when data is glued into a query as text and the database reads it as code. Parameterized queries keep the two apart. Supabase\'s client and PostgREST parameterize for you; the risk returns the moment you build SQL strings yourself.',
body='''<h3>Why</h3>
          <p>The attack is forty years old and still on the OWASP list because string concatenation is easy. A search box that becomes WHERE title = \'… turns a single quote into a way to end the string and write more SQL: read other tables, bypass a login, drop a table. The defense is not escaping quotes; it is never mixing data into the query text. Parameterized queries send the SQL and the values separately, so the database treats the value as a value, whatever characters it holds. Supabase\'s JavaScript client builds parameterized requests, and PostgREST does the same on the server, so the ordinary path is safe.</p>
          <p>The holes appear where you write SQL: database functions that build dynamic queries with string concatenation, RPC calls that take raw fragments, Edge Functions that talk to Postgres directly, and admin scripts. In Postgres functions use format() with %L and %I, or EXECUTE … USING, never || with user input. Input validation helps for sanity (a page number is a number) but is not the defense; a valid-looking string can still be an injection. Test with the classic payloads in every input that reaches a query and watch for errors that leak the query, which is itself information disclosure.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Parameters, never concatenation,</strong> in every place that touches SQL.</li>
            <li><strong>In Postgres functions,</strong> format() with %L/%I or EXECUTE … USING.</li>
            <li><strong>Database user with least privilege</strong> for any server-side code you write.</li>
            <li><strong>Error messages for users are generic;</strong> the real error goes to the log.</li>
          </ul>''',
details=['<strong>Test with</strong> \' OR 1=1 -- and a quote in every field.',
 '<strong>ORMs and clients are safe until you call .raw()</strong> or build a filter string.',
 '<strong>Column and table names are not parameters;</strong> allowlist them.',
 '<strong>Full-text search inputs</strong> still go through parameters.',
 '<strong>A leaked error with SQL in it</strong> is a finding on its own.'],
sources=L(('PortSwigger, SQL injection', 'https://portswigger.net/web-security/sql-injection'), ('OWASP, SQL injection prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'), ('OWASP Top 10, A03 Injection', 'https://owasp.org/Top10/A03_2021-Injection/'), ('OWASP, Database security cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html'))),

dict(id='csrf', title='CSRF and When It Applies',
lede='Cross-site request forgery is another site making the browser send a request to yours with the user\'s cookies attached. It only works when the credential travels automatically. Know which model you use, then apply the matching defense.',
body='''<h3>Why</h3>
          <p>Cookies are attached to requests by the browser, regardless of which page started them. A hidden form on evil.example that posts to your API would arrive carrying the victim\'s session cookie, and the server would believe it. That is CSRF. The defenses are SameSite cookies, which stop the browser from attaching cookies to cross-site requests, anti-CSRF tokens the attacker cannot know, and checking the Origin header. If instead the session token lives in localStorage and is sent as an Authorization header by your own JavaScript, a foreign page cannot add that header, and CSRF does not apply; the price, as the storage lesson said, is that XSS becomes the whole game.</p>
          <p>Supabase\'s default browser client uses the header model, so a plain app built on it is not CSRF-exposed. The moment you move the session to cookies, for server-side rendering or for a custom backend, CSRF comes back and SameSite=Lax plus origin checks become mandatory. Also remember the non-cookie variants: a logged-in action triggered by a GET (an "unsubscribe" or "delete" link) is forgeable from an image tag, which is one more reason a GET never changes state. Decide the model, write it down, and test it: a form on another origin that posts to your API should fail.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Header-carried tokens: no CSRF, mandatory CSP.</strong> Cookie-carried: SameSite plus tokens or origin checks.</li>
            <li><strong>State-changing requests are never GET.</strong></li>
            <li><strong>Check Origin or Referer on the server</strong> when cookies are the credential.</li>
            <li><strong>Test from a foreign page</strong> once; expect the request to be refused.</li>
          </ul>''',
details=['<strong>SameSite=Lax still sends cookies on top-level GET navigation;</strong> that is why GET must be safe.',
 '<strong>CORS does not prevent CSRF;</strong> the request is sent, only the response is hidden.',
 '<strong>Login CSRF exists too:</strong> logging the victim into the attacker\'s account.',
 '<strong>Double-submit cookies</strong> are the simplest token scheme for a small app.',
 '<strong>Document the session model</strong> so the next person applies the right defense.'],
sources=L(('PortSwigger, CSRF', 'https://portswigger.net/web-security/csrf'), ('OWASP, CSRF prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html'), ('MDN, SameSite cookies', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite'), ('web.dev, SameSite cookies explained', 'https://web.dev/articles/samesite-cookies-explained'))),

dict(id='keys-and-secrets', title='Keys and Secrets',
lede='The anon key is designed to be public and useless without RLS. The service role key bypasses RLS and must never leave a server. Environment variables, .gitignore and secret scanning keep the second one out of the bundle and the repository.',
body='''<h3>Why</h3>
          <p>Supabase gives every project two kinds of keys. The publishable or anon key identifies the project and ships in the browser; its only power is to call the API as an anonymous or authenticated user, which RLS then constrains. The secret or service role key is the master key: it bypasses every policy and reads and writes anything. It belongs in a server environment, an Edge Function, or a trusted script, never in frontend code, never in a Vite variable prefixed VITE_, because everything with that prefix is compiled into the public bundle. One service role key in a JavaScript bundle equals a public database.</p>
          <p>Secrets reach the repository through carelessness: a .env committed by accident, a key pasted in a config file, a screenshot in the docs. The defenses are routine: .env in .gitignore from the first commit, an .env.example with placeholders, GitHub secret scanning turned on, a local scanner like gitleaks in a pre-commit hook, and rotation the moment a key is suspected to have leaked, because git history remembers everything. Cloudflare Pages keeps production variables in its dashboard, separate from preview environments, which is where the dev/prod split starts to matter.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Anon key in the client, service role key never.</strong> No VITE_ prefix on anything secret.</li>
            <li><strong>.env ignored, .env.example committed,</strong> variables set in the hosting dashboard.</li>
            <li><strong>Secret scanning on the repo</strong> and a pre-commit scanner locally.</li>
            <li><strong>Rotate on suspicion,</strong> not on proof. A leaked key is leaked forever in history.</li>
          </ul>''',
details=['<strong>Search the built bundle for "service_role"</strong> before every deploy. It takes ten seconds.',
 '<strong>Different keys per environment;</strong> a leaked staging key must not open production.',
 '<strong>Rotation is a drill:</strong> practice it before you need it.',
 '<strong>Screenshots of the dashboard</strong> often contain keys. Crop.',
 '<strong>The anon key is public by design;</strong> stop treating it as a secret and start treating RLS as the lock.'],
sources=L(('Supabase, API keys', 'https://supabase.com/docs/guides/api/api-keys'), ('Vite, Env variables and modes', 'https://vite.dev/guide/env-and-mode'), ('GitHub, About secret scanning', 'https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning'), ('OWASP, Secrets management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html'), ('gitleaks', 'https://github.com/gitleaks/gitleaks'))),

dict(id='storage-and-uploads', title='Storage, Uploads and Signed URLs',
lede='Uploaded images are files, and files have their own permissions. Buckets are public or private, policies decide who uploads and who reads, signed URLs give temporary access to private files, and limits on size and type keep uploads from becoming an attack.',
body='''<h3>Why</h3>
          <p>Supabase Storage keeps files in buckets with RLS-style policies on the objects table. A public bucket serves any file by URL, forever, to anyone; that is right for avatars and wrong for images attached to a private resource. A private bucket serves files only through authenticated requests or signed URLs, links that expire after a set time. Most apps need both: a public bucket for profile pictures, a private bucket for user content, with policies that mirror the parent resource\'s visibility, so that a private resource\'s images do not leak through a URL copied once. Path conventions help: user_id/resource_id/file, with policies that compare the first folder to auth.uid().</p>
          <p>Uploads are input. Limit size per file and per bucket, restrict MIME types to the images you actually display, and never trust the extension; the server decides the content type. Rename files on upload so paths are not user-controlled, which closes path traversal and overwrite tricks. Strip EXIF metadata if location data could leak. And consider what happens on delete: removing an item should remove its image, or you keep paying for, and potentially serving, files that should be gone, which the LGPD will care about.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Public bucket for avatars, private bucket for user content,</strong> policies mirroring resource visibility.</li>
            <li><strong>Signed URLs with short expiry</strong> for anything private; never a permanent link.</li>
            <li><strong>Size and MIME limits at the bucket,</strong> server-generated file names, no user paths.</li>
            <li><strong>Delete files with their rows,</strong> and test that a deleted image stops serving.</li>
          </ul>''',
details=['<strong>Public bucket URLs are cacheable forever;</strong> moving a resource to private does not recall them.',
 '<strong>Folder-per-user paths</strong> make ownership policies a one-liner.',
 '<strong>Image transforms on the server</strong> also strip dangerous content.',
 '<strong>SVG uploads can carry scripts;</strong> treat them as code, not images.',
 '<strong>Test the three users on files too,</strong> not only on rows.'],
sources=L(('Supabase, Storage access control', 'https://supabase.com/docs/guides/storage/security/access-control'), ('Supabase, File limits', 'https://supabase.com/docs/guides/storage/uploads/file-limits'), ('Supabase, Serving downloads and signed URLs', 'https://supabase.com/docs/guides/storage/serving/downloads'), ('OWASP, File upload cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html'), ('PortSwigger, File upload vulnerabilities', 'https://portswigger.net/web-security/file-upload'))),

dict(id='security-headers-and-csp', title='Security Headers and CSP',
lede='A handful of response headers tell the browser how to protect your page: which scripts may run, whether it may be framed, how referrers leak, which features are allowed. Content Security Policy is the heaviest and the most valuable, because it blunts XSS even when a hole exists.',
body='''<h3>Why</h3>
          <p>The browser will do a lot for you if asked. Content-Security-Policy lists where scripts, styles, images and connections may come from; a strict policy with no unsafe-inline means an injected script tag simply does not run. Strict-Transport-Security pins HTTPS. X-Content-Type-Options stops MIME sniffing. X-Frame-Options or frame-ancestors prevents your login from being framed into a clickjacking page. Referrer-Policy keeps full URLs, which may include ids of unlisted resources, from leaking to other sites. Permissions-Policy disables camera, geolocation and friends you do not use. Cloudflare Pages sets these through a _headers file in the build output.</p>
          <p>CSP is the one that takes work, because a Vite app with a Supabase client, Google Fonts and an analytics script has real sources to declare, and inline styles from libraries fight a strict style-src. Start in report-only mode, read the violations, tighten, then enforce. The connect-src must include your Supabase URL; img-src must include the storage domain; script-src should be your origin plus hashes or nonces, nothing inline. Test with securityheaders.com and with the console open. The reward is that the XSS lesson\'s worst case, a script in a note, becomes a blocked request instead of a stolen session.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>_headers file on Pages</strong> with HSTS, nosniff, frame-ancestors, Referrer-Policy, Permissions-Policy.</li>
            <li><strong>CSP in report-only first,</strong> then enforced, with no unsafe-inline for scripts.</li>
            <li><strong>Declare only what you use:</strong> your origin, Supabase, fonts.</li>
            <li><strong>Re-check headers after every infra change</strong> with an external scanner.</li>
          </ul>''',
details=['<strong>Referrer-Policy: strict-origin-when-cross-origin</strong> keeps unlisted ids out of other sites\' logs.',
 '<strong>frame-ancestors \'none\'</strong> unless you embed on purpose.',
 '<strong>Nonces or hashes</strong> for the one inline script you cannot avoid.',
 '<strong>Report-only is not protection;</strong> set a date to enforce.',
 '<strong>Headers are per response;</strong> check the API and the storage domain too, not only the page.'],
sources=L(('MDN, Content Security Policy', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP'), ('web.dev, Strict CSP', 'https://web.dev/articles/strict-csp'), ('OWASP, HTTP headers cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html'), ('Cloudflare Pages, Headers', 'https://developers.cloudflare.com/pages/configuration/headers/'), ('securityheaders.com', 'https://securityheaders.com/'))),

dict(id='dependencies-and-supply-chain', title='Dependencies and the Supply Chain',
lede='Your app is mostly other people\'s code. A vulnerable package ships your vulnerability; a hijacked package ships someone\'s malware. Lockfiles, audits, automated updates and a habit of reading what you install are the controls.',
body='''<h3>Why</h3>
          <p>A Vite and React project pulls hundreds of packages, each a potential hole and each a potential path for a malicious update. OWASP lists vulnerable and outdated components in the Top 10; the supply-chain incidents of recent years added typosquatting and maintainer-account takeovers to the list. The baseline is mechanical: commit the lockfile so installs are reproducible, run npm audit in CI and read it, enable Dependabot or an equivalent so updates arrive as reviewable pull requests, and pin major versions of anything that touches auth or rendering. The judgment part is reading: before adding a package, check its maintenance, its download count, its dependency tree and whether you need it at all.</p>
          <p>Frontend code runs in the user\'s browser with the user\'s session, so a compromised UI library is as dangerous as a compromised backend. Keep the dependency list short, prefer platform features over packages for small needs, and avoid packages that pull in dozens of others for one function. Scheduled, boring updates beat heroic ones: a monthly update window where everything moves a little is safer than a yearly jump that breaks the build. When a vulnerability drops in something you use, know within a day, not a quarter.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Lockfile committed, npm audit in CI,</strong> failures triaged the same week.</li>
            <li><strong>Automated update PRs</strong> with a regular merge cadence.</li>
            <li><strong>Read before you install:</strong> maintainers, activity, size, transitive deps.</li>
            <li><strong>Fewer packages:</strong> every dependency is a standing decision to trust a stranger.</li>
          </ul>''',
details=['<strong>npm audit fix --force</strong> can break things; read the diff.',
 '<strong>Dev dependencies run on your machine;</strong> postinstall scripts are a vector too.',
 '<strong>Pin by lockfile, not by exact versions in package.json,</strong> so patches still flow.',
 '<strong>Subscribe to advisories</strong> for the five packages that matter most.',
 '<strong>Remove what you stopped using;</strong> unused packages still get installed and still get hacked.'],
sources=L(('OWASP Top 10, A06 Vulnerable and Outdated Components', 'https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/'), ('npm, npm audit', 'https://docs.npmjs.com/cli/v10/commands/npm-audit'), ('GitHub, Dependabot', 'https://docs.github.com/en/code-security/dependabot'), ('OWASP, Vulnerable dependency management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html'))),

dict(id='logs-backups-environments', title='Logs, Backups and Environments',
lede='You cannot defend what you cannot see or restore. Logs tell you something happened, alerts tell you now, backups let you undo it, and a restore test proves the backup is real. Separate environments keep experiments away from real people\'s data.',
body='''<h3>Why</h3>
          <p>Security logging and monitoring failures are an OWASP category of their own because breaches go unnoticed for months. For a small app the bar is modest and still real: Supabase keeps auth, API and database logs; read them when something is odd, and set alerts for the events that matter, failed logins in bursts, errors spiking, unusual volumes of reads. Log what happened and who did it, never what they typed in a password field or the token they carried. Logs are also personal data under the LGPD, so they get a retention period like everything else.</p>
          <p>Backups are the difference between an incident and a catastrophe. Supabase takes daily backups on paid plans, with point-in-time recovery available; the free tier does not, which is a reason to decide early what losing everything would mean. A backup nobody has restored is a hope, not a control; schedule a restore into a scratch project and time it. Environments complete the picture: develop against a separate project with fictional data, use preview deployments for review, and keep production keys in production only. Supabase branching and Cloudflare preview deployments make the split cheap; the discipline is never pointing a dev build at the production database "just for a minute".</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Read the logs weekly,</strong> alert on failed-login bursts and error spikes.</li>
            <li><strong>Backups on, restore tested</strong> at least once before launch and after big changes.</li>
            <li><strong>Separate projects for dev and prod,</strong> fictional data in dev, previews for review.</li>
            <li><strong>Logs have retention,</strong> and never contain passwords or tokens.</li>
          </ul>''',
details=['<strong>Timebox the restore drill</strong> and write down how long it took.',
 '<strong>Alert fatigue is a failure mode;</strong> three alerts that matter beat thirty.',
 '<strong>Scrub Authorization headers and emails</strong> from anything you ship to a third-party logger.',
 '<strong>Who has production access?</strong> Write the list; keep it short.',
 '<strong>Migrations run in dev first,</strong> then preview, then prod, with a rollback plan.'],
sources=L(('OWASP Top 10, A09 Security Logging and Monitoring Failures', 'https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/'), ('OWASP, Logging cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html'), ('Supabase, Backups', 'https://supabase.com/docs/guides/platform/backups'), ('Supabase, Branching', 'https://supabase.com/docs/guides/deployment/branching'), ('Supabase, Going into production', 'https://supabase.com/docs/guides/deployment/going-into-prod'), ('The Twelve-Factor App, Config', 'https://12factor.net/config'))),

dict(id='personal-data-under-lgpd', title='Personal Data Under the LGPD',
lede='Brazil\'s Lei Geral de Proteção de Dados applies the moment you store a name or an email. It defines personal and sensitive data, names the roles of controller and operator, and sets principles that read like product requirements: purpose, necessity, transparency, security.',
body='''<h3>Why</h3>
          <p>Personal data is anything that identifies or can identify a natural person: name, email, handle, photo, IP address, device id, and the combination of innocuous fields that together point at someone. Sensitive data is a narrower set with stricter rules: health, sexual orientation, religion, ethnicity, politics, biometrics, genetics. A harmless-looking app stores free text that can reveal a pregnancy, a religion or a medical condition; design the fields so you do not collect what you do not need, and treat free text as potentially sensitive. The person whose data it is holds the rights; you, deciding why and how it is processed, are the controller; Supabase and Cloudflare, processing on your instructions, are operators.</p>
          <p>The principles in article 6 are the design brief. Purpose: collect for a specific, stated reason. Adequacy and necessity: only what that reason needs. Transparency: tell people, in clear language, what you do. Security: measures proportional to the risk. Prevention, non-discrimination, accountability. The inventory is the practical first step: a table of every field you store, with its purpose, the legal basis you intend to rely on, who can access it, which vendor holds it and for how long. That table drives the privacy policy, the deletion flow and the incident plan, and it is what the ANPD, the national authority, would ask to see.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Inventory every field</strong> with purpose, legal basis, access, vendor and retention.</li>
            <li><strong>Collect less:</strong> if the purpose does not need the birthday, do not ask.</li>
            <li><strong>Name the roles:</strong> you are the controller; list your operators.</li>
            <li><strong>Treat free text as sensitive-capable</strong> and keep it private by default.</li>
          </ul>''',
details=['<strong>IP addresses and device ids are personal data.</strong> Logs count.',
 '<strong>Pseudonymized is still personal;</strong> only true anonymization leaves the law.',
 '<strong>Children\'s data</strong> needs specific parental consent and the best interest of the child.',
 '<strong>The inventory is a living document;</strong> update it with every new field.',
 '<strong>This is education, not legal advice;</strong> a lawyer reviews before launch.'],
sources=L(('Lei nº 13.709/2018 (LGPD), texto integral', 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm'), ('ANPD, Autoridade Nacional de Proteção de Dados', 'https://www.gov.br/anpd/pt-br'), ('ANPD, materiais educativos e publicações', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'), ('Serpro, LGPD explicada', 'https://www.serpro.gov.br/lgpd'))),

dict(id='legal-bases-and-rights', title='Legal Bases and the Rights of Data Subjects',
lede='Consent is one of ten legal bases, and usually not the best one. Running the account a person asked for is contract performance; preventing fraud is legitimate interest. Whatever the basis, the person keeps rights: access, correction, portability, deletion, and an answer within a reasonable time.',
body='''<h3>Why</h3>
          <p>The LGPD lists the legal bases in article 7: consent, legal obligation, public policy, research, contract execution, exercise of rights, protection of life, health protection, legitimate interest, credit protection. A product that asks for consent for everything gets two problems: consent can be withdrawn at any time, which would mean deleting the account the person still wants, and a long consent form nobody reads is not the free, informed, unambiguous consent the law requires. For a typical app, storing the email and the person\'s own content is execution of the contract the person signed up for; security logs are legitimate interest; a marketing newsletter is consent, separate, opt-in, revocable with one click.</p>
          <p>Rights are the other half. The person may confirm whether you process their data, access it, correct it, anonymize or delete what is unnecessary, receive it in a portable format, know who you shared it with, and withdraw consent. Each right needs a path in the product or a documented manual process, and a response within the law\'s timeframes. Build the obvious ones in: an export of the person\'s data as JSON, account deletion that actually deletes, a profile page where fields are editable, and a contact channel that is answered. Keep a record of requests and responses; accountability is a principle, and the record is its proof.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Pick the basis per purpose:</strong> contract for the service, legitimate interest for security, consent only for extras.</li>
            <li><strong>Consent is granular, opt-in and revocable</strong> where you use it at all.</li>
            <li><strong>Ship export and deletion</strong> as features, not as support tickets.</li>
            <li><strong>Log requests and answers</strong> with dates.</li>
          </ul>''',
details=['<strong>Pre-checked boxes are not consent.</strong>',
 '<strong>Legitimate interest needs a written balancing test</strong> you can show.',
 '<strong>Deletion has exceptions:</strong> legal obligations may require keeping some records; say which.',
 '<strong>Portability means a machine-readable export,</strong> JSON is fine.',
 '<strong>Designate a contact (encarregado)</strong> even if it is you, and publish it.'],
sources=L(('Lei nº 13.709/2018 (LGPD), artigos 7, 11 e 18', 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm'), ('ANPD, materiais educativos e publicações', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'), ('ICO, Guide to the data protection principles (GDPR parallel)', 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/'))),

dict(id='privacy-by-design-in-product', title='Privacy by Design in the Product',
lede='Privacy by design means the safe choice is the default and the private choice is real in the backend, not a toggle that hides a button. Visibility controls, deletion, retention, cookies and the privacy policy are product features, built with the same care as the main feature.',
body='''<h3>Why</h3>
          <p>The LGPD asks for privacy from conception and by default. In practice that means: new resources private, profile fields minimal, analytics off until the person agrees, and every "private" in the interface backed by a policy in the database and in storage. The privacy policy and the terms of use are different documents with different jobs: the policy explains what data, why, on which basis, with whom, for how long and how to exercise rights; the terms set the rules of the service. Both are read by few and matter to all; write them in plain language and keep them accurate, because a policy that promises what the system does not do is itself a violation.</p>
          <p>Cookies get their own paragraph because the folklore is wrong. Strictly necessary cookies, the session and the preference you need to run the service, need no consent banner. Analytics and marketing do need a real choice, off by default, with the same ease to refuse as to accept; the ANPD has published guidance on exactly this. Retention closes the loop: decide how long you keep an inactive account, deleted-list data, logs and backups, and automate the deletion. Account deletion must cascade through rows, files and, within the backup window, backups too, and the person should get a confirmation. Finally, a privacy contact that answers, and a dated change log for the policy.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Private by default,</strong> every visibility control enforced in the database and in storage.</li>
            <li><strong>Privacy policy and terms as separate, plain-language pages,</strong> accurate to what the code does.</li>
            <li><strong>Cookie choice only for analytics and marketing,</strong> off by default, refuse as easy as accept.</li>
            <li><strong>Retention schedule automated,</strong> deletion cascades through rows, files and backups.</li>
          </ul>''',
details=['<strong>Delete means delete:</strong> rows, storage objects, search indexes, and the backup window stated.',
 '<strong>No consent banner for necessary cookies;</strong> one that blocks the page for everything is the anti-pattern.',
 '<strong>The share dialog is a privacy moment:</strong> repeat what will be visible.',
 '<strong>Policy versioning</strong> with dates, and notify on material changes.',
 '<strong>Minimal profile:</strong> handle and display name; everything else optional.'],
sources=L(('ANPD, guia orientativo sobre cookies e proteção de dados pessoais', 'https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf'), ('ANPD, guia de segurança para agentes de tratamento de pequeno porte', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte'), ('IF, Data patterns catalogue', 'https://catalogue.projectsbyif.com/'), ('ICO, advice for small organisations', 'https://ico.org.uk/for-organisations/advice-for-small-organisations/'))),

dict(id='vendors-incidents-and-launch', title='Vendors, Incidents and the Pre-Launch Review',
lede='Supabase, Cloudflare and GitHub process your users\' data on your behalf, often outside Brazil. Know their terms, know where the data lives, and have a plan for the day something goes wrong. Then run the pre-launch review: three users, every operation, every file, every header, with evidence.',
body='''<h3>Why</h3>
          <p>Operators are part of your responsibility. Read the data processing terms of each vendor, note the regions where data is stored, and record them in the inventory; the LGPD regulates international transfers and the ANPD has rules for them, so a database in a non-Brazilian region is a decision to document, not an accident. Subprocessors change: subscribe to the vendors\' notices. Incidents will happen: a leaked key, a policy mistake that exposed private resources, a compromised account. The LGPD requires communicating relevant incidents to the ANPD and to affected people; the practical plan is four steps, detect, contain, assess, communicate, with the contacts, the templates and the decision criteria written before you need them.</p>
          <p>The pre-launch review is where this whole section becomes evidence. Walk the permission matrix with a visitor, the owner and another user, through the API, for every operation, and record results. Fetch private images by URL as the wrong user. Review the auth flows, the password rules, the emails and every redirect. Check headers, CSP, HTTPS, upload limits and external URL handling. Confirm secrets are out of the repo and the bundle, dependencies are current, backups restore, alerts fire. Reread the inventory, the policy, the retention schedule and the deletion flow against what the code actually does. List the residual risks you accept and the items you postpone, with an owner and a date. Launch with that document, not with a feeling.</p>

          <h3>How to apply</h3>
          <ul>
            <li><strong>Vendor table:</strong> what each processes, where, under which terms, with a link to the notice feed.</li>
            <li><strong>Incident plan on one page:</strong> detect, contain, assess, communicate, with contacts and templates.</li>
            <li><strong>Pre-launch review with evidence:</strong> every matrix cell tested, every check screenshot or log attached.</li>
            <li><strong>Residual risk register</strong> signed before real users arrive.</li>
          </ul>''',
details=['<strong>"Configured" is not "tested".</strong> The review tests.',
 '<strong>Practice the incident plan</strong> with a tabletop exercise of a leaked key.',
 '<strong>Retest after every schema or policy change,</strong> automated where possible.',
 '<strong>Priority if time is short:</strong> RLS and cross-user tests, then auth, then storage and secrets, then OWASP, then LGPD documents.',
 '<strong>This trail is education;</strong> it is not a certification or legal compliance. Get a review before launch.'],
sources=L(('ANPD, incidentes de segurança', 'https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca'), ('ANPD, transferência internacional de dados', 'https://www.gov.br/anpd/pt-br/assuntos/transferencia-internacional-de-dados'), ('OWASP, Web Security Testing Guide', 'https://owasp.org/www-project-web-security-testing-guide/'), ('OWASP, Application Security Verification Standard', 'https://owasp.org/www-project-application-security-verification-standard/'), ('Supabase, Going into production', 'https://supabase.com/docs/guides/deployment/going-into-prod'), ('Cloudflare Pages', 'https://developers.cloudflare.com/pages/'))),
]
