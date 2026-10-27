# Demos for the Development section. One per lesson, <=2 controls, interaction on the object. Class prefixes dvNN- are unique site-wide.
from html import escape as esc

def slider(name, label, mn, mx, step, val, unit=''):
    return ('<label class="ctl"><span class="ctl-label">%s</span><input type="range" name="%s" min="%s" max="%s" step="%s" value="%s" data-unit="%s"><output></output></label>' % (label, name, mn, mx, step, val, unit))
def toggle(name, label, on=False):
    return ('<label class="ctl ctl-switch"><span class="ctl-label">%s</span><input type="checkbox" name="%s" role="switch"%s><span class="switch" aria-hidden="true"></span></label>' % (label, name, ' checked' if on else ''))
def demo(key, stage, controls, caption, attrs=''):
    return ('''<figure class="demo-figure">
          <div class="demo" data-demo="%s">
            <div class="demo-stage"%s>
            %s
            </div>
            <div class="demo-controls">%s</div>
          </div>
            <figcaption class="demo-caption">%s</figcaption>
          </figure>''' % (key, (' ' + attrs) if attrs else '', stage, ''.join(controls), caption))
def da(**kw):
    return ' '.join('data-%s="%s"' % (k.replace('_', '-'), esc(v, quote=True)) for k, v in kw.items())
def btn(cls, label, extra=''):
    return '<button type="button" class="%s"%s>%s</button>' % (cls, (' ' + extra) if extra else '', label)
def seg(cls, items, on=0):
    return '<div class="dv-seg %s">%s</div>' % (cls, ''.join('<button type="button" class="dv-seg-b%s" data-v="%d">%s</button>' % (' is-on' if i == on else '', i, t) for i, t in enumerate(items)))

T = {
'en': dict(
  d01_anon='Not signed in', d01_other="Someone else's private list", d01_path='/lists/42', d01_send='Send', d01_first='Pick a method.',
  d01_s=dict(s200='200 OK · here is the list', s201='201 Created · item added', s204='204 No Content · deleted, nothing to return', s401='401 Unauthorized · who are you? Sign in first.', s403='403 Forbidden · we know who you are; this is not yours.', s404='404 Not Found · nothing here for you, and we do not say whether it exists.'),
  d01_cap='Pick a method on the request. Signed out, every method answers 401. Signed in on someone else\'s private list, reads answer 404 and writes answer 403. The status is the UI state before any design exists.',
  d02_https='HTTPS', d02_stolen='Database copy stolen', d02_sniff='Eavesdrop on the network', d02_rows=['Host: wishlist.app', 'Path: /lists/42', 'Cookie: session=eyJhbG…', 'Body: {"item": "Camera"}'],
  d02_seen='Visible on the wire:', d02_rest='In the stolen database copy, everything is readable. TLS covers transit only.', d02_h='With HTTPS the eavesdropper sees the host and the size. Nothing else.', d02_p='Without HTTPS the eavesdropper reads the cookie, the path and the body.',
  d02_cap='Eavesdrop with HTTPS on: host and size, nothing else. Turn it off: cookie, path and body in clear. Then steal the database copy: TLS did nothing for data at rest, because it was never meant to.',
  d03_httponly='HttpOnly cookie', d03_xss='Injected script running', d03_run='Script: read the session', d03_req='Send a request', d03_boxes=['Cookie', 'localStorage', 'Memory'],
  d03_tok='session=eyJ…', d03_mem='in memory: gone on reload', d03_read='The script read:', d03_none='nothing (HttpOnly keeps the cookie out of reach)', d03_got='the token in localStorage and the cookie', d03_got2='the token in localStorage', d03_noxss='No script injected. Turn on the injected script to try.', d03_sent='Request sent · cookie attached by the browser automatically, localStorage sent only if your code adds a header.',
  d03_cap='Run the injected script: it reads localStorage every time, and the cookie only when HttpOnly is off. Send a request: the cookie travels by itself, which is convenient for you and for CSRF.',
  d04_allow='Allow-Origin: app.example only', d04_curl='Call from curl instead', d04_send='Send request', d04_from_b='from a page on evil.example', d04_from_c='from curl, no browser',
  d04_resp=['response hidden by the browser', 'response read by the page', 'full response delivered'], d04_blocked='Browser blocked the page from reading the response. The API still answered; the user was protected.', d04_read='The page on evil.example read the response. Reflected or wildcard origins defeat the policy.', d04_curl_r='curl got the full response. CORS does not exist outside browsers; only the token and RLS protect the data.',
  d04_cap='Send from the evil page: the browser hides the response when the API names only app.example. Send from curl: the response arrives regardless. CORS protects people in browsers; the database protects the data.',
  d05_ui='Checks only in the UI', d05_roles=['Visitor', 'Owner', 'Other user'], d05_acts=['Read private list', 'Add item', 'Delete list'], d05_api='Call the API directly', d05_try='Try',
  d05_ok='allowed', d05_no='denied by the database', d05_hidden='button hidden', d05_leak='allowed by the API: the UI hid the button, the database never checked.', d05_first='Pick a role, then an action.',
  d05_cap='Switch roles and try the actions. With database checks, the visitor and the other user are denied whatever they call. With UI-only checks the buttons vanish, but "call the API directly" still succeeds.',
  d06_verify='Require email verification', d06_neutral='Neutral messages', d06_signup='Sign up', d06_signin='Sign in', d06_recover='Recover password', d06_email='ana@example.com', d06_unknown='nobody@example.com',
  d06_confirm='Confirm email', d06_s_noacct='401 · wrong email or password (same message whether or not the account exists)', d06_s_verified='Email confirmed · you can sign in', d06_s_created='Account created · verification email sent', d06_s_blocked='Sign-in blocked · verify your email first', d06_s_unverified='Signed in without verifying · anyone can register an address they do not own', d06_s_in='Signed in', d06_r_neutral='If that email exists, we sent a recovery link.', d06_r_leak='No account found for nobody@example.com. (Now the attacker knows.)', d06_first='Sign up, then try to sign in.',
  d06_cap='Sign up, then sign in: with verification required the door stays shut until the email is confirmed. Recover a password for an unknown address: the neutral message gives nothing away; the helpful one confirms which emails exist.',
  d07_ttl='Access token lifetime', d07_rotate='Refresh rotation', d07_use='Use the app (+20 min)', d07_steal='Attacker replays a stolen refresh token', d07_access='access token', d07_refresh='refresh token',
  d07_valid='valid', d07_dead='Session revoked · sign in again', d07_expired='expired → refreshed silently', d07_rev='Replay detected: rotation revoked the whole session. The attacker and the user are both signed out.', d07_hij='Replay accepted: without rotation the attacker now holds a fresh session.', d07_first='Use the app a few times, then replay a stolen token.',
  d07_cap='Use the app: every 20 minutes the clock moves; when the access token expires it is refreshed without a login. Replay a stolen refresh token: with rotation on, reuse revokes the session; off, the attacker is in.',
  d08_limit='Rate limit', d08_mfa='MFA for admin', d08_try='Try a password', d08_right='Correct password', d08_attempts='attempts', d08_wait='429 · too many attempts, wait', d08_wrong='401 · wrong email or password', d08_in='Signed in', d08_code='Password accepted · enter the 6-digit code', d08_first='Click "try a password" fast.',
  d08_cap='Hammer the login: after five wrong tries the rate limit answers 429 and the attacker waits. Then use the correct password: with MFA on, the admin still needs the code. The error never says which half was wrong.',
  d09_cascade='ON DELETE CASCADE', d09_del='Delete user Ana', d09_tables=['profiles', 'wishlists', 'wishlist_items'], d09_rows=[['ana', 'rui'], ['Birthday (ana)', 'Camping (ana)', 'Books (rui)'], ['Camera → Birthday', 'Tent → Camping', 'Atlas → Books']],
  d09_hint='Click a profile to see what belongs to it.', d09_gone='Deleted ana: her lists and items went with her.', d09_orphan='Deleted ana: 2 lists and 2 items are now orphans, still stored, pointing at nobody.',
  d09_cap='Click ana to see her lists and items light up through the foreign keys. Delete her: with CASCADE everything she owned disappears; without it, orphan rows stay behind, which the LGPD will eventually ask about.',
  d10_rls='RLS enabled', d10_left='Leftover "allow all" policy', d10_as=['Visitor', 'Ana', 'Rui'], d10_run='SELECT * FROM wishlists', d10_rows=[['Birthday', 'ana', 'public'], ['Camping', 'ana', 'private'], ['Books', 'rui', 'private']],
  d10_r='rows returned', d10_norls='No RLS: the anon key reads every row.', d10_leftover='A permissive leftover policy is OR-ed with the good ones: every row passes.', d10_first='Choose who is asking, then run the query.',
  d10_cap='Run the query as a visitor, as Ana, as Rui. With RLS on, each sees only public rows plus their own. Turn RLS off, or leave a testing "allow all" policy behind, and everyone sees everything.',
  d11_ui='Enforced only in the UI', d11_def='Private by default', d11_vis=['Public', 'Unlisted', 'Private'], d11_viewers=['Found via search', 'Has the link', 'Owner'], d11_new='New list', d11_labels=['Anyone can find this list', 'Only people with the link', 'Only you'],
  d11_yes='can open it', d11_no='cannot open it', d11_leak='opens it through the API: the UI hid the list, the database allowed it.', d11_newmsg='New list created as %s.', d11_first='Set a visibility, then try each viewer.',
  d11_cap='Set the tier and try each viewer. Unlisted hides from search and opens for the link; private opens only for the owner. Enforce in the UI only and the link holder reads a private list through the API. Private by default makes a new list safe before anyone decides.',
  d12_rls='RLS enabled', d12_uuid='UUID ids', d12_mine='My list', d12_next='Next id', d12_leaked='Leaked id', d12_ok='200 · your list', d12_empty='404 · nothing (RLS returned no rows)', d12_leak='200 · someone else\'s private list', d12_guess='UUIDs cannot be guessed, but a leaked one works forever.', d12_first='Change the id in the URL.',
  d12_cap='Fetch your list, then the next id. With RLS, the database returns nothing for a list that is not yours. Without it, the private list leaks. UUIDs stop guessing; the leaked-id button shows they do not stop a copied link.',
  d13_html='Render as HTML', d13_csp='CSP: no inline scripts', d13_pay=['A note about a camera', '<img src=x onerror="steal()">', '<a href="javascript:steal()">gift</a>'], d13_preview='Preview for other viewers',
  d13_text='Rendered as text: the markup is visible and harmless.', d13_ran='Script executed in every viewer\'s browser. Session stolen.', d13_blocked='Markup injected, but CSP blocked the inline script.', d13_first='Pick a note, then flip the rendering.',
  d13_cap='Pick a note and render it. As text, markup is just characters. As HTML, the image payload runs for every viewer; CSP is the second layer that blocks the inline script even after the mistake.',
  d14_param='Parameterized query', d14_in=['Camera', "' OR 1=1 --"], d14_search='Search', d14_sql='SQL sent', d14_rows=['Camera (ana, public)', 'Tent (ana, private)', 'Atlas (rui, private)'],
  d14_safe='The value is a parameter; the database looks for a title literally equal to the text.', d14_inj='The quote ended the string and the rest became code: every row returned, private ones included.', d14_first='Search a title, then try the payload.',
  d14_cap='Search "Camera", then the payload. Parameterized, the strange text is just a title nobody has. Concatenated, the quote closes the string and OR 1=1 returns every private row.',
  d15_cookie='Session in a cookie', d15_samesite='SameSite=Lax', d15_submit='Hidden form on evil.example submits', d15_req='POST /lists/42/items', d15_cred='Credential attached:', d15_c_yes='session cookie (browser added it)', d15_c_ss='none (SameSite kept the cookie home)', d15_c_hdr='none (the header is added only by your own code)', d15_ok='Server accepted: an item was added without the user knowing.', d15_rej='Server rejected: no credential, no forgery.',
  d15_cap='Let the evil form submit. With the session in a cookie and no SameSite, the browser attaches it and the forgery succeeds. SameSite keeps it home. With the token in a header, the foreign page cannot add it at all.',
  d16_srv='service_role in a VITE_ variable', d16_ignore='.env in .gitignore', d16_scan='Scan the repo', d16_bundle='dist/assets/index-8f2a.js', d16_anon='VITE_SUPABASE_ANON_KEY = "eyJ…anon"', d16_sr='VITE_SERVICE_ROLE = "eyJ…service_role"',
  d16_bad='The service role key is in the public bundle: anyone can bypass every RLS policy.', d16_good='Only the anon key ships. Without RLS it would still be a public database; with RLS it is useless to an attacker.', d16_found='Scan: .env committed in history with 2 keys. Rotate now; history never forgets.', d16_clean='Scan: no secrets in the repository.',
  d16_cap='Put the service role key in a VITE_ variable and read the built bundle: it is there, for everyone. Scan the repo with .env unignored: the keys are in history, and rotation is the only fix.',
  d17_private='Private bucket', d17_exp='Signed URL expiry', d17_copy='Copy image link', d17_open='Open as visitor, 30 min later', d17_file='camera.jpg', d17_pub='Public bucket: the link works forever, for anyone, even after the list goes private.', d17_signed='Signed URL copied · expires in %d min', d17_ok='Opened: the signature was still valid.', d17_expired='Expired: the signature stopped working. Private files stay private after a link is shared.', d17_first='Copy the link, then open it later.',
  d17_cap='Copy the image link and open it as a visitor half an hour later. A public bucket serves forever. A private bucket with a short signed URL stops working, which is what "private list" has to mean for its images too.',
  d18_csp='CSP enforced', d18_frame='frame-ancestors none', d18_inject='Inject inline script', d18_embed='Embed in evil frame', d18_headers=['Strict-Transport-Security', 'X-Content-Type-Options: nosniff', 'Referrer-Policy: strict-origin-when-cross-origin', 'Permissions-Policy: camera=(), geolocation=()'],
  d18_ran='Inline script ran. No CSP, no second layer.', d18_blk='Blocked: script-src has no unsafe-inline. The console shows the violation.', d18_framed='Your login rendered inside evil.example, ready for clickjacking.', d18_noframe='Refused to display in a frame.', d18_first='Try an injection, then a frame.',
  d18_cap='Inject an inline script with CSP off: it runs. With CSP on, the browser refuses and logs a violation. Embed the page in a hostile frame: frame-ancestors none refuses the frame. The other headers sit in the same _headers file.',
  d19_months='Months without updates', d19_bot='Dependabot + audit in CI', d19_audit='npm audit', d19_deps=['react 18.3', 'vite 5.4', 'markdown-it 14', '@supabase/supabase-js 2.4', 'lodash 4.17'], d19_known='known vulnerabilities', d19_rep='audit: %d vulnerabilities (%d high) · %s', d19_patched='patched within a week by automated PRs', d19_open='open, nobody looked', d19_first='Drag the months, then run the audit.',
  d19_cap='Let months pass without updates and run the audit: vulnerabilities accumulate in packages you never touched. With Dependabot and audit in CI, the same months produce PRs that get merged, and the count stays near zero.',
  d20_backup='Daily backups', d20_tested='Restore tested', d20_oops='Oops: DROP TABLE wishlists', d20_restore='Restore', d20_rows='12,480 wishlists', d20_lost='Table gone.', d20_nobackup='No backup. 12,480 wishlists are gone for good.', d20_untested='Backup exists, restore fails: wrong region, missing extension. Nobody had ever tried.', d20_ok='Restored from last night\'s backup in 14 minutes. Lost: up to 24 hours of changes.', d20_first='Drop the table, then restore.',
  d20_cap='Drop the table, then restore. No backup: gone. Backup never tested: the restore fails the first time it matters. Backup tested: fourteen minutes and a known loss window. The test is the control.',
  d21_reveal='Reveal answers', d21_fields=['Handle', 'Email', 'IP address in logs', 'Birthday', 'Item: "pregnancy test"', 'Item: "camera"', 'Avatar photo'], d21_opts=['Not personal', 'Personal', 'Sensitive'], d21_ans=[1, 1, 1, 1, 2, 0, 1],
  d21_notes=['Identifies a person.', 'Identifies a person.', 'Logs count: an IP can identify a device and a person.', 'Personal; with other fields, identifying.', 'Reveals health: sensitive data, special rules.', 'A product name identifies nobody.', 'A face is personal data; biometric templates would be sensitive.'], d21_score='%d / 7 classified right', d21_first='Classify each field, then reveal.',
  d21_cap='Classify every field the wishlist stores. Reveal: the IP in the logs is personal, the pregnancy test in a wishlist is sensitive, and the camera is nobody\'s business. The inventory starts with this exercise.',
  d22_rights='Rights built into the product', d22_rows=['Run the account (email, lists)', 'Security logs (IP, attempts)', 'Monthly newsletter'], d22_bases=['Consent', 'Contract', 'Legitimate interest'], d22_rec=[1, 2, 0], d22_withdraw='User withdraws consent', d22_export='Export my data', d22_delete='Delete my account',
  d22_w_ok='Newsletter stopped. The account and the logs continue on their own bases.', d22_w_bad='The account itself rests on consent: withdrawing it means deleting the account the person still wants.', d22_exp_ok='account.json ready: profile, lists, items.', d22_exp_manual='"Email support and we will get back to you." (Within the legal deadline, by hand.)', d22_del_ok='Account, lists, items and files deleted. Backups purge in 30 days.', d22_del_manual='Ticket opened. Someone will delete it manually, eventually.', d22_first='Pick a legal basis per purpose.',
  d22_cap='Pick a basis per purpose and withdraw consent: if the account rests on consent, withdrawal deletes it. With contract for the service and consent only for the newsletter, withdrawal stops the newsletter. Rights built in answer instantly; rights by ticket answer eventually.',
  d23_defpriv='New lists private by default', d23_analytics='Analytics on by default', d23_del='Delete my account', d23_banner_ok='Cookie notice: session cookie only; analytics off until you say yes.', d23_banner_bad='Cookie banner: analytics already running; "Accept all" is the big button.', d23_new='New list: %s', d23_pub='public', d23_priv='private', d23_deleted='Deleted: 3 lists, 11 items, 7 images, search entries. Backups purge within 30 days. Confirmation email sent.', d23_policy='Policy summary (generated from settings):',
  d23_cap='Flip the defaults and watch the policy summary rewrite itself: private-by-default and analytics-off are the privacy-by-design choices. Delete the account: rows, files, search entries and a stated backup window, with a confirmation.',
  d24_rls='RLS enabled', d24_run='Run all tests', d24_ops=['Read public list', 'Read private list', 'Add item', 'Edit or delete item', 'Delete list'], d24_roles=['Visitor', 'Owner', 'Other user'], d24_exp=[[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
  d24_pass='%d / 15 pass', d24_fail='%d failures: the matrix says No, the database said Yes.', d24_first='Click a cell to test it, or run all.',
  d24_cap='Each cell is one test: the operation, as that role, through the API. Run them all with RLS on: fifteen passes. Turn RLS off: the cells where the matrix says No and the database says Yes turn red. That is the pre-launch review in one grid.',
),
'pt': dict(
  d01_anon='Sem login', d01_other='Lista privada de outra pessoa', d01_path='/lists/42', d01_send='Enviar', d01_first='Escolha um método.',
  d01_s=dict(s200='200 OK · aqui está a lista', s201='201 Created · item adicionado', s204='204 No Content · excluído, nada para devolver', s401='401 Unauthorized · quem é você? Faça login primeiro.', s403='403 Forbidden · sabemos quem você é; isto não é seu.', s404='404 Not Found · nada aqui para você, e não dizemos se existe.'),
  d01_cap='Escolha um método na requisição. Sem login, todo método responde 401. Logada numa lista privada de outra pessoa, leituras respondem 404 e escritas 403. O status é o estado de UI antes de existir qualquer design.',
  d02_https='HTTPS', d02_stolen='Cópia do banco roubada', d02_sniff='Escutar a rede', d02_rows=['Host: wishlist.app', 'Path: /lists/42', 'Cookie: session=eyJhbG…', 'Body: {"item": "Câmera"}'],
  d02_seen='Visível no fio:', d02_rest='Na cópia roubada do banco, tudo é legível. TLS cobre só o trânsito.', d02_h='Com HTTPS quem escuta vê o host e o tamanho. Nada mais.', d02_p='Sem HTTPS quem escuta lê o cookie, o caminho e o corpo.',
  d02_cap='Escute a rede com HTTPS ligado: host e tamanho, nada mais. Desligue: cookie, caminho e corpo em texto claro. Depois roube a cópia do banco: TLS não fez nada pelos dados em repouso, porque nunca foi para isso.',
  d03_httponly='Cookie HttpOnly', d03_xss='Script injetado rodando', d03_run='Script: ler a sessão', d03_req='Enviar uma requisição', d03_boxes=['Cookie', 'localStorage', 'Memória'],
  d03_tok='session=eyJ…', d03_mem='na memória: some ao recarregar', d03_read='O script leu:', d03_none='nada (HttpOnly mantém o cookie fora de alcance)', d03_got='o token no localStorage e o cookie', d03_got2='o token no localStorage', d03_noxss='Nenhum script injetado. Ligue o script injetado para tentar.', d03_sent='Requisição enviada · cookie anexado pelo navegador sozinho, localStorage só vai se o seu código adicionar um header.',
  d03_cap='Rode o script injetado: ele lê o localStorage sempre, e o cookie só quando HttpOnly está desligado. Envie uma requisição: o cookie viaja sozinho, o que é conveniente para você e para o CSRF.',
  d04_allow='Allow-Origin: só app.example', d04_curl='Chamar do curl', d04_send='Enviar requisição', d04_from_b='de uma página em evil.example', d04_from_c='do curl, sem navegador',
  d04_resp=['resposta escondida pelo navegador', 'resposta lida pela página', 'resposta completa entregue'], d04_blocked='O navegador impediu a página de ler a resposta. A API respondeu mesmo assim; o usuário foi protegido.', d04_read='A página em evil.example leu a resposta. Origem refletida ou curinga derrota a política.', d04_curl_r='O curl recebeu a resposta inteira. CORS não existe fora de navegadores; só o token e a RLS protegem os dados.',
  d04_cap='Envie da página maliciosa: o navegador esconde a resposta quando a API nomeia só app.example. Envie do curl: a resposta chega de qualquer jeito. CORS protege pessoas em navegadores; o banco protege os dados.',
  d05_ui='Checagem só na UI', d05_roles=['Visitante', 'Dono', 'Outro usuário'], d05_acts=['Ler lista privada', 'Adicionar item', 'Excluir lista'], d05_api='Chamar a API diretamente', d05_try='Tentar',
  d05_ok='permitido', d05_no='negado pelo banco', d05_hidden='botão escondido', d05_leak='permitido pela API: a UI escondeu o botão, o banco nunca checou.', d05_first='Escolha um papel, depois uma ação.',
  d05_cap='Troque de papel e tente as ações. Com checagem no banco, visitante e outro usuário são negados chamem o que chamarem. Com checagem só na UI os botões somem, mas "chamar a API diretamente" continua funcionando.',
  d06_verify='Exigir verificação de e-mail', d06_neutral='Mensagens neutras', d06_signup='Cadastrar', d06_signin='Entrar', d06_recover='Recuperar senha', d06_email='ana@example.com', d06_unknown='ninguem@example.com',
  d06_confirm='Confirmar e-mail', d06_s_noacct='401 · e-mail ou senha incorretos (mesma mensagem exista ou não a conta)', d06_s_verified='E-mail confirmado · você pode entrar', d06_s_created='Conta criada · e-mail de verificação enviado', d06_s_blocked='Login bloqueado · verifique seu e-mail primeiro', d06_s_unverified='Logada sem verificar · qualquer um registra um endereço que não possui', d06_s_in='Logada', d06_r_neutral='Se esse e-mail existir, enviamos um link de recuperação.', d06_r_leak='Nenhuma conta para ninguem@example.com. (Agora o atacante sabe.)', d06_first='Cadastre, depois tente entrar.',
  d06_cap='Cadastre e depois entre: com verificação exigida a porta fica fechada até o e-mail ser confirmado. Recupere a senha de um endereço desconhecido: a mensagem neutra não entrega nada; a prestativa confirma quais e-mails existem.',
  d07_ttl='Duração do access token', d07_rotate='Rotação do refresh', d07_use='Usar o app (+20 min)', d07_steal='Atacante reusa um refresh token roubado', d07_access='access token', d07_refresh='refresh token',
  d07_valid='válido', d07_dead='Sessão revogada · entre de novo', d07_expired='expirou → renovado em silêncio', d07_rev='Reuso detectado: a rotação revogou a sessão inteira. Atacante e usuário saíram.', d07_hij='Reuso aceito: sem rotação o atacante agora tem uma sessão nova.', d07_first='Use o app algumas vezes, depois reuse um token roubado.',
  d07_cap='Use o app: a cada 20 minutos o relógio anda; quando o access token expira ele é renovado sem login. Reuse um refresh token roubado: com rotação ligada, o reuso revoga a sessão; desligada, o atacante entra.',
  d08_limit='Rate limit', d08_mfa='MFA para admin', d08_try='Tentar uma senha', d08_right='Senha correta', d08_attempts='tentativas', d08_wait='429 · muitas tentativas, espere', d08_wrong='401 · e-mail ou senha incorretos', d08_in='Logada', d08_code='Senha aceita · digite o código de 6 dígitos', d08_first='Clique em "tentar uma senha" rápido.',
  d08_cap='Martele o login: depois de cinco erros o rate limit responde 429 e o atacante espera. Depois use a senha correta: com MFA ligado, o admin ainda precisa do código. O erro nunca diz qual metade estava errada.',
  d09_cascade='ON DELETE CASCADE', d09_del='Excluir a usuária ana', d09_tables=['profiles', 'wishlists', 'wishlist_items'], d09_rows=[['ana', 'rui'], ['Aniversário (ana)', 'Camping (ana)', 'Livros (rui)'], ['Câmera → Aniversário', 'Barraca → Camping', 'Atlas → Livros']],
  d09_hint='Clique num perfil para ver o que pertence a ele.', d09_gone='Excluída ana: as listas e os itens dela foram junto.', d09_orphan='Excluída ana: 2 listas e 2 itens ficaram órfãos, ainda guardados, apontando para ninguém.',
  d09_cap='Clique em ana para ver as listas e os itens dela acenderem pelas chaves estrangeiras. Exclua: com CASCADE tudo que era dela desaparece; sem, linhas órfãs ficam para trás, o que a LGPD um dia vai perguntar.',
  d10_rls='RLS ligada', d10_left='Política "permite tudo" esquecida', d10_as=['Visitante', 'Ana', 'Rui'], d10_run='SELECT * FROM wishlists', d10_rows=[['Aniversário', 'ana', 'pública'], ['Camping', 'ana', 'privada'], ['Livros', 'rui', 'privada']],
  d10_r='linhas devolvidas', d10_norls='Sem RLS: a chave anon lê toda linha.', d10_leftover='Uma política permissiva esquecida é somada com OU às boas: toda linha passa.', d10_first='Escolha quem pergunta, depois rode a consulta.',
  d10_cap='Rode a consulta como visitante, como Ana, como Rui. Com RLS ligada, cada um vê só as públicas mais as próprias. Desligue a RLS, ou deixe uma política de teste "permite tudo", e todo mundo vê tudo.',
  d11_ui='Imposta só na UI', d11_def='Privada por padrão', d11_vis=['Pública', 'Não listada', 'Privada'], d11_viewers=['Achou na busca', 'Tem o link', 'Dono'], d11_new='Nova lista', d11_labels=['Qualquer um pode encontrar esta lista', 'Só quem tem o link', 'Só você'],
  d11_yes='consegue abrir', d11_no='não consegue abrir', d11_leak='abre pela API: a UI escondeu a lista, o banco permitiu.', d11_newmsg='Nova lista criada como %s.', d11_first='Defina a visibilidade, depois teste cada visitante.',
  d11_cap='Defina o nível e teste cada visitante. Não listada some da busca e abre pelo link; privada abre só para o dono. Imponha só na UI e quem tem o link lê uma lista privada pela API. Privada por padrão deixa a lista nova segura antes de alguém decidir.',
  d12_rls='RLS ligada', d12_uuid='Ids UUID', d12_mine='Minha lista', d12_next='Próximo id', d12_leaked='Id vazado', d12_ok='200 · sua lista', d12_empty='404 · nada (a RLS não devolveu linhas)', d12_leak='200 · lista privada de outra pessoa', d12_guess='UUIDs não se adivinham, mas um vazado funciona para sempre.', d12_first='Mude o id na URL.',
  d12_cap='Busque sua lista, depois o próximo id. Com RLS, o banco devolve nada para uma lista que não é sua. Sem, a lista privada vaza. UUIDs impedem adivinhar; o botão de id vazado mostra que não impedem um link copiado.',
  d13_html='Renderizar como HTML', d13_csp='CSP: sem scripts inline', d13_pay=['Uma nota sobre uma câmera', '<img src=x onerror="roubar()">', '<a href="javascript:roubar()">presente</a>'], d13_preview='Prévia para outros visitantes',
  d13_text='Renderizado como texto: a marcação aparece e é inofensiva.', d13_ran='Script executado no navegador de todo visitante. Sessão roubada.', d13_blocked='Marcação injetada, mas a CSP bloqueou o script inline.', d13_first='Escolha uma nota, depois troque a renderização.',
  d13_cap='Escolha uma nota e renderize. Como texto, marcação é só caractere. Como HTML, o payload da imagem roda para todo visitante; a CSP é a segunda camada que bloqueia o script inline mesmo depois do erro.',
  d14_param='Consulta parametrizada', d14_in=['Câmera', "' OR 1=1 --"], d14_search='Buscar', d14_sql='SQL enviado', d14_rows=['Câmera (ana, pública)', 'Barraca (ana, privada)', 'Atlas (rui, privada)'],
  d14_safe='O valor é um parâmetro; o banco procura um título literalmente igual ao texto.', d14_inj='A aspa encerrou a string e o resto virou código: toda linha devolvida, privadas incluídas.', d14_first='Busque um título, depois tente o payload.',
  d14_cap='Busque "Câmera", depois o payload. Parametrizado, o texto estranho é só um título que ninguém tem. Concatenado, a aspa fecha a string e OR 1=1 devolve toda linha privada.',
  d15_cookie='Sessão em cookie', d15_samesite='SameSite=Lax', d15_submit='Formulário escondido em evil.example envia', d15_req='POST /lists/42/items', d15_cred='Credencial anexada:', d15_c_yes='cookie de sessão (o navegador adicionou)', d15_c_ss='nenhuma (SameSite segurou o cookie em casa)', d15_c_hdr='nenhuma (o header só é adicionado pelo seu próprio código)', d15_ok='Servidor aceitou: um item foi adicionado sem a pessoa saber.', d15_rej='Servidor recusou: sem credencial, sem forjamento.',
  d15_cap='Deixe o formulário malicioso enviar. Com a sessão em cookie e sem SameSite, o navegador anexa e o forjamento funciona. SameSite segura o cookie em casa. Com o token em header, a página estranha não consegue adicioná-lo.',
  d16_srv='service_role numa variável VITE_', d16_ignore='.env no .gitignore', d16_scan='Varrer o repositório', d16_bundle='dist/assets/index-8f2a.js', d16_anon='VITE_SUPABASE_ANON_KEY = "eyJ…anon"', d16_sr='VITE_SERVICE_ROLE = "eyJ…service_role"',
  d16_bad='A chave service role está no bundle público: qualquer um ignora toda política de RLS.', d16_good='Só a chave anon é enviada. Sem RLS seria um banco público; com RLS, é inútil para um atacante.', d16_found='Varredura: .env commitado no histórico com 2 chaves. Rotacione agora; o histórico nunca esquece.', d16_clean='Varredura: nenhum segredo no repositório.',
  d16_cap='Ponha a chave service role numa variável VITE_ e leia o bundle compilado: ela está lá, para todos. Varra o repositório com o .env fora do ignore: as chaves estão no histórico, e rotacionar é o único conserto.',
  d17_private='Bucket privado', d17_exp='Expiração da URL assinada', d17_copy='Copiar link da imagem', d17_open='Abrir como visitante, 30 min depois', d17_file='camera.jpg', d17_pub='Bucket público: o link funciona para sempre, para qualquer um, mesmo depois de a lista ficar privada.', d17_signed='URL assinada copiada · expira em %d min', d17_ok='Abriu: a assinatura ainda valia.', d17_expired='Expirou: a assinatura parou de funcionar. Arquivos privados seguem privados depois de um link compartilhado.', d17_first='Copie o link, depois abra mais tarde.',
  d17_cap='Copie o link da imagem e abra como visitante meia hora depois. Bucket público serve para sempre. Bucket privado com URL assinada curta para de funcionar, que é o que "lista privada" precisa significar para as imagens também.',
  d18_csp='CSP imposta', d18_frame='frame-ancestors none', d18_inject='Injetar script inline', d18_embed='Embutir em frame malicioso', d18_headers=['Strict-Transport-Security', 'X-Content-Type-Options: nosniff', 'Referrer-Policy: strict-origin-when-cross-origin', 'Permissions-Policy: camera=(), geolocation=()'],
  d18_ran='Script inline rodou. Sem CSP, sem segunda camada.', d18_blk='Bloqueado: script-src não tem unsafe-inline. O console mostra a violação.', d18_framed='Seu login renderizado dentro de evil.example, pronto para clickjacking.', d18_noframe='Recusou exibir dentro de um frame.', d18_first='Tente uma injeção, depois um frame.',
  d18_cap='Injete um script inline com a CSP desligada: ele roda. Com a CSP ligada, o navegador recusa e registra a violação. Embuta a página num frame hostil: frame-ancestors none recusa. Os outros headers moram no mesmo arquivo _headers.',
  d19_months='Meses sem atualizar', d19_bot='Dependabot + audit no CI', d19_audit='npm audit', d19_deps=['react 18.3', 'vite 5.4', 'markdown-it 14', '@supabase/supabase-js 2.4', 'lodash 4.17'], d19_known='vulnerabilidades conhecidas', d19_rep='audit: %d vulnerabilidades (%d altas) · %s', d19_patched='corrigidas em uma semana por PRs automáticos', d19_open='abertas, ninguém olhou', d19_first='Arraste os meses, depois rode o audit.',
  d19_cap='Deixe os meses passarem sem atualizar e rode o audit: vulnerabilidades se acumulam em pacotes que você nunca tocou. Com Dependabot e audit no CI, os mesmos meses produzem PRs que são mesclados, e a contagem fica perto de zero.',
  d20_backup='Backups diários', d20_tested='Restauração testada', d20_oops='Ops: DROP TABLE wishlists', d20_restore='Restaurar', d20_rows='12.480 wishlists', d20_lost='Tabela sumiu.', d20_nobackup='Sem backup. 12.480 wishlists se foram para sempre.', d20_untested='Backup existe, restauração falha: região errada, extensão faltando. Ninguém nunca tinha tentado.', d20_ok='Restaurado do backup de ontem em 14 minutos. Perda: até 24 horas de mudanças.', d20_first='Derrube a tabela, depois restaure.',
  d20_cap='Derrube a tabela, depois restaure. Sem backup: perdido. Backup nunca testado: a restauração falha na primeira vez que importa. Backup testado: catorze minutos e uma janela de perda conhecida. O teste é o controle.',
  d21_reveal='Revelar respostas', d21_fields=['Handle', 'E-mail', 'IP nos logs', 'Data de nascimento', 'Item: "teste de gravidez"', 'Item: "câmera"', 'Foto do avatar'], d21_opts=['Não pessoal', 'Pessoal', 'Sensível'], d21_ans=[1, 1, 1, 1, 2, 0, 1],
  d21_notes=['Identifica uma pessoa.', 'Identifica uma pessoa.', 'Logs contam: um IP pode identificar um aparelho e uma pessoa.', 'Pessoal; junto com outros campos, identificador.', 'Revela saúde: dado sensível, regras especiais.', 'Nome de produto não identifica ninguém.', 'Um rosto é dado pessoal; um template biométrico seria sensível.'], d21_score='%d / 7 classificados certo', d21_first='Classifique cada campo, depois revele.',
  d21_cap='Classifique todo campo que a wishlist guarda. Revele: o IP nos logs é pessoal, o teste de gravidez numa wishlist é sensível, e a câmera não é de ninguém. O inventário começa com este exercício.',
  d22_rights='Direitos construídos no produto', d22_rows=['Operar a conta (e-mail, listas)', 'Logs de segurança (IP, tentativas)', 'Newsletter mensal'], d22_bases=['Consentimento', 'Contrato', 'Legítimo interesse'], d22_rec=[1, 2, 0], d22_withdraw='Usuária revoga o consentimento', d22_export='Exportar meus dados', d22_delete='Excluir minha conta',
  d22_w_ok='Newsletter parada. A conta e os logs continuam nas próprias bases.', d22_w_bad='A própria conta repousa em consentimento: revogar significa excluir a conta que a pessoa ainda quer.', d22_exp_ok='conta.json pronto: perfil, listas, itens.', d22_exp_manual='"Mande e-mail ao suporte que retornamos." (Dentro do prazo legal, à mão.)', d22_del_ok='Conta, listas, itens e arquivos excluídos. Backups expurgam em 30 dias.', d22_del_manual='Ticket aberto. Alguém vai excluir manualmente, uma hora.', d22_first='Escolha uma base legal por finalidade.',
  d22_cap='Escolha a base por finalidade e revogue o consentimento: se a conta repousa em consentimento, revogar a exclui. Com contrato para o serviço e consentimento só para a newsletter, revogar para a newsletter. Direitos construídos respondem na hora; direitos por ticket respondem uma hora.',
  d23_defpriv='Listas novas privadas por padrão', d23_analytics='Analytics ligado por padrão', d23_del='Excluir minha conta', d23_banner_ok='Aviso de cookies: só o cookie de sessão; analytics desligado até você aceitar.', d23_banner_bad='Banner de cookies: analytics já rodando; "Aceitar tudo" é o botão grande.', d23_new='Nova lista: %s', d23_pub='pública', d23_priv='privada', d23_deleted='Excluído: 3 listas, 11 itens, 7 imagens, entradas de busca. Backups expurgam em até 30 dias. E-mail de confirmação enviado.', d23_policy='Resumo da política (gerado das configurações):',
  d23_cap='Inverta os padrões e veja o resumo da política se reescrever: privada por padrão e analytics desligado são as escolhas de privacy by design. Exclua a conta: linhas, arquivos, entradas de busca e uma janela de backup declarada, com confirmação.',
  d24_rls='RLS ligada', d24_run='Rodar todos os testes', d24_ops=['Ler lista pública', 'Ler lista privada', 'Adicionar item', 'Editar ou excluir item', 'Excluir lista'], d24_roles=['Visitante', 'Dono', 'Outro usuário'], d24_exp=[[1, 1, 1], [0, 1, 0], [0, 1, 0], [0, 1, 0], [0, 1, 0]],
  d24_pass='%d / 15 passam', d24_fail='%d falhas: a matriz diz Não, o banco disse Sim.', d24_first='Clique numa célula para testar, ou rode todos.',
  d24_cap='Cada célula é um teste: a operação, como aquele papel, pela API. Rode todos com RLS ligada: quinze aprovados. Desligue a RLS: as células em que a matriz diz Não e o banco diz Sim ficam vermelhas. É a revisão de pré-lançamento numa grade.',
)}

def build(L):
    t = T[L]; D = {}
    # 01 HTTP
    D['how-the-web-talks'] = demo('dev-01',
      '<div class="dv01-wrap"><div class="dv01-req"><span class="dv01-line">%s <code>%s</code></span>%s</div><div class="dv01-res"><b class="dv01-status"></b><span class="dv01-read"></span></div></div>' % ('', t['d01_path'], seg('dv01-m', ['GET', 'POST', 'PATCH', 'DELETE'], -1)),
      [toggle('anon', t['d01_anon']), toggle('other', t['d01_other'])], t['d01_cap'],
      da(first=t['d01_first'], **t['d01_s']))
    # 02 TLS
    rows = ''.join('<div class="dv02-row" data-i="%d"><span class="dv02-plain">%s</span><span class="dv02-enc"></span></div>' % (i, r) for i, r in enumerate(t['d02_rows']))
    D['what-tls-protects'] = demo('dev-02',
      '<div class="dv02-wrap"><div class="dv02-wire">%s</div><div class="dv02-bar">%s</div><div class="dv02-db"><span>wishlists.sql</span><q>ana · camping · private · "Camera"</q></div><span class="dv02-read"></span></div>' % (rows, btn('dv02-sniff', t['d02_sniff'])),
      [toggle('https', t['d02_https'], True), toggle('stolen', t['d02_stolen'])], t['d02_cap'],
      da(seen=t['d02_seen'], rest=t['d02_rest'], h=t['d02_h'], p=t['d02_p']))
    # 03 Storage
    boxes = ''.join('<div class="dv03-box" data-k="%d"><b>%s</b><code>%s</code></div>' % (i, b, t['d03_mem'] if i == 2 else t['d03_tok']) for i, b in enumerate(t['d03_boxes']))
    D['cookies-sessions-storage'] = demo('dev-03',
      '<div class="dv03-wrap"><div class="dv03-shelf">%s</div><div class="dv03-bar">%s%s</div><span class="dv03-read"></span></div>' % (boxes, btn('dv03-run', t['d03_run']), btn('dv03-req', t['d03_req'])),
      [toggle('httponly', t['d03_httponly'], True), toggle('xss', t['d03_xss'], True)], t['d03_cap'],
      da(read=t['d03_read'], none=t['d03_none'], got=t['d03_got'], got2=t['d03_got2'], noxss=t['d03_noxss'], sent=t['d03_sent']))
    # 04 CORS
    D['same-origin-and-cors'] = demo('dev-04',
      '<div class="dv04-wrap"><div class="dv04-flow"><div class="dv04-node dv04-src"><b>evil.example</b><small class="dv04-from"></small></div><i class="dv04-arrow"></i><div class="dv04-node dv04-api"><b>api.wishlist.app</b><small>Access-Control-Allow-Origin: <span class="dv04-acao"></span></small></div></div><em class="dv04-resp"></em>%s<span class="dv04-read"></span></div>' % btn('dv04-send', t['d04_send']),
      [toggle('allow', t['d04_allow'], True), toggle('curl', t['d04_curl'])], t['d04_cap'],
      da(fromb=t['d04_from_b'], fromc=t['d04_from_c'], blocked=t['d04_blocked'], read=t['d04_read'], curlr=t['d04_curl_r'], resp='|'.join(t['d04_resp'])))
    # 05 AuthN vs AuthZ
    acts = ''.join('<div class="dv05-act" data-a="%d"><span>%s</span>%s%s%s<i class="dv05-res"></i></div>' % (i, a, btn('dv05-btn', t['d05_try']), '<i class="dv05-hid">%s</i>' % t['d05_hidden'], btn('dv05-api', t['d05_api'])) for i, a in enumerate(t['d05_acts']))
    D['authentication-vs-authorization'] = demo('dev-05',
      '<div class="dv05-wrap">%s<div class="dv05-acts">%s</div><span class="dv05-read"></span></div>' % (seg('dv05-role', t['d05_roles'], 1), acts),
      [toggle('uionly', t['d05_ui'])], t['d05_cap'],
      da(ok=t['d05_ok'], no=t['d05_no'], hidden=t['d05_hidden'], leak=t['d05_leak'], first=t['d05_first']))
    # 06 Auth flows
    D['auth-flows'] = demo('dev-06',
      '<div class="dv06-wrap"><div class="dv06-card"><span class="dv06-email">%s</span><div class="dv06-btns">%s%s%s</div><div class="dv06-state"></div></div><div class="dv06-card"><span class="dv06-email">%s</span><div class="dv06-btns">%s</div><div class="dv06-state dv06-rec"></div></div><span class="dv06-read"></span></div>' % (t['d06_email'], btn('dv06-signup', t['d06_signup']), btn('dv06-confirm', t['d06_confirm'], 'hidden'), btn('dv06-signin', t['d06_signin']), t['d06_unknown'], btn('dv06-recover', t['d06_recover'])),
      [toggle('verify', t['d06_verify'], True), toggle('neutral', t['d06_neutral'], True)], t['d06_cap'],
      da(created=t['d06_s_created'], noacct=t['d06_s_noacct'], verified=t['d06_s_verified'], blocked=t['d06_s_blocked'], unverified=t['d06_s_unverified'], sin=t['d06_s_in'], rneutral=t['d06_r_neutral'], rleak=t['d06_r_leak'], first=t['d06_first']))
    # 07 Tokens
    D['tokens-and-sessions'] = demo('dev-07',
      '<div class="dv07-wrap"><div class="dv07-clock">t = <b class="dv07-t">0</b> min</div><div class="dv07-tokens"><div class="dv07-tok dv07-a"><span>%s</span><i class="dv07-bar"><b></b></i><small class="dv07-as"></small></div><div class="dv07-tok dv07-r"><span>%s</span><small class="dv07-rs">#1</small></div></div><div class="dv07-btns">%s%s</div><span class="dv07-read"></span></div>' % (t['d07_access'], t['d07_refresh'], btn('dv07-use', t['d07_use']), btn('dv07-steal', t['d07_steal'])),
      [slider('ttl', t['d07_ttl'], 5, 60, 5, 30, ' min'), toggle('rotate', t['d07_rotate'], True)], t['d07_cap'],
      da(valid=t['d07_valid'], dead=t['d07_dead'], expired=t['d07_expired'], rev=t['d07_rev'], hij=t['d07_hij'], first=t['d07_first']))
    # 08 Abuse
    D['account-abuse'] = demo('dev-08',
      '<div class="dv08-wrap"><div class="dv08-login"><span class="dv08-field">admin@wishlist.app</span><span class="dv08-field">••••••••</span><div class="dv08-btns">%s%s</div><div class="dv08-out"></div></div><span class="dv08-count"><b>0</b> %s</span><span class="dv08-read"></span></div>' % (btn('dv08-try', t['d08_try']), btn('dv08-right', t['d08_right']), t['d08_attempts']),
      [toggle('limit', t['d08_limit'], True), toggle('mfa', t['d08_mfa'], True)], t['d08_cap'],
      da(wait=t['d08_wait'], wrong=t['d08_wrong'], sin=t['d08_in'], code=t['d08_code'], first=t['d08_first']))
    # 09 Data model
    tables = ''.join('<div class="dv09-table" data-t="%d"><b>%s</b>%s</div>' % (ti, name, ''.join('<span class="dv09-row" data-owner="%s">%s</span>' % ('ana' if 'ana' in r or r.startswith(('Camera', 'Tent', 'Câmera', 'Barraca')) else 'rui', r) for r in t['d09_rows'][ti])) for ti, name in enumerate(t['d09_tables']))
    D['data-model'] = demo('dev-09',
      '<div class="dv09-wrap"><div class="dv09-tables">%s</div>%s<span class="dv09-read"></span></div>' % (tables, btn('dv09-del', t['d09_del'])),
      [toggle('cascade', t['d09_cascade'], True)], t['d09_cap'],
      da(hint=t['d09_hint'], gone=t['d09_gone'], orphan=t['d09_orphan']))
    # 10 RLS
    rows = ''.join('<div class="dv10-row" data-owner="%s" data-vis="%s"><span>%s</span><span>%s</span><span>%s</span></div>' % (r[1], 'public' if r[2] in ('public', 'pública') else 'private', r[0], r[1], r[2]) for r in t['d10_rows'])
    D['row-level-security'] = demo('dev-10',
      '<div class="dv10-wrap">%s<div class="dv10-bar">%s<span class="dv10-count"></span></div><div class="dv10-table">%s</div><span class="dv10-read"></span></div>' % (seg('dv10-as', t['d10_as'], 0), btn('dv10-run', t['d10_run']), rows),
      [toggle('rls', t['d10_rls'], True), toggle('leftover', t['d10_left'])], t['d10_cap'],
      da(r=t['d10_r'], norls=t['d10_norls'], leftover=t['d10_leftover'], first=t['d10_first']))
    # 11 Visibility
    viewers = ''.join(btn('dv11-viewer', v, 'data-v="%d"' % i) for i, v in enumerate(t['d11_viewers']))
    D['visibility-tiers'] = demo('dev-11',
      '<div class="dv11-wrap"><div class="dv11-card"><b>Camping</b>%s<small class="dv11-label"></small></div><div class="dv11-viewers">%s</div><div class="dv11-bar">%s</div><span class="dv11-read"></span></div>' % (seg('dv11-vis', t['d11_vis'], 2), viewers, btn('dv11-new', t['d11_new'])),
      [toggle('uionly', t['d11_ui']), toggle('defpriv', t['d11_def'], True)], t['d11_cap'],
      da(labels='|'.join(t['d11_labels']), vis='|'.join(t['d11_vis']), yes=t['d11_yes'], no=t['d11_no'], leak=t['d11_leak'], newmsg=t['d11_newmsg'], first=t['d11_first']))
    # 12 IDOR
    D['broken-access-control'] = demo('dev-12',
      '<div class="dv12-wrap"><div class="dv12-url"><span>GET /lists/</span><b class="dv12-id">42</b></div><div class="dv12-btns">%s%s%s</div><div class="dv12-res"></div><span class="dv12-read"></span></div>' % (btn('dv12-mine', t['d12_mine']), btn('dv12-next', t['d12_next']), btn('dv12-leaked', t['d12_leaked'])),
      [toggle('rls', t['d12_rls'], True), toggle('uuid', t['d12_uuid'])], t['d12_cap'],
      da(ok=t['d12_ok'], empty=t['d12_empty'], leak=t['d12_leak'], guess=t['d12_guess'], first=t['d12_first']))
    # 13 XSS
    pays = ''.join(btn('dv13-pay', esc(p), 'data-i="%d"' % i) for i, p in enumerate(t['d13_pay']))
    D['xss-and-safe-rendering'] = demo('dev-13',
      '<div class="dv13-wrap"><div class="dv13-pays">%s</div><div class="dv13-card"><small>%s</small><div class="dv13-out"></div></div><span class="dv13-read"></span></div>' % (pays, t['d13_preview']),
      [toggle('html', t['d13_html']), toggle('csp', t['d13_csp'])], t['d13_cap'],
      da(text=t['d13_text'], ran=t['d13_ran'], blocked=t['d13_blocked'], first=t['d13_first'], p0=t['d13_pay'][0], p1=t['d13_pay'][1], p2=t['d13_pay'][2]))
    # 14 SQLi
    ins = ''.join(btn('dv14-in', esc(p), 'data-i="%d"' % i) for i, p in enumerate(t['d14_in']))
    rows = ''.join('<span class="dv14-row">%s</span>' % r for r in t['d14_rows'])
    D['sql-injection'] = demo('dev-14',
      '<div class="dv14-wrap"><div class="dv14-ins">%s</div><div class="dv14-sql"><small>%s</small><code class="dv14-q"></code></div><div class="dv14-rows">%s</div><span class="dv14-read"></span></div>' % (ins, t['d14_sql'], rows),
      [toggle('param', t['d14_param'], True)], t['d14_cap'],
      da(safe=t['d14_safe'], inj=t['d14_inj'], first=t['d14_first'], i0=t['d14_in'][0], i1=t['d14_in'][1]))
    # 15 CSRF
    D['csrf'] = demo('dev-15',
      '<div class="dv15-wrap"><div class="dv15-evil"><b>evil.example</b>%s</div><div class="dv15-req"><code>%s</code><small>%s <span class="dv15-cred">—</span></small></div><span class="dv15-read"></span></div>' % (btn('dv15-submit', t['d15_submit']), t['d15_req'], t['d15_cred']),
      [toggle('cookie', t['d15_cookie'], True), toggle('samesite', t['d15_samesite'])], t['d15_cap'],
      da(cyes=t['d15_c_yes'], css=t['d15_c_ss'], chdr=t['d15_c_hdr'], ok=t['d15_ok'], rej=t['d15_rej']))
    # 16 Keys
    D['keys-and-secrets'] = demo('dev-16',
      '<div class="dv16-wrap"><div class="dv16-bundle"><small>%s</small><code class="dv16-anon">%s</code><code class="dv16-sr">%s</code></div><div class="dv16-bar">%s</div><span class="dv16-read"></span></div>' % (t['d16_bundle'], t['d16_anon'], t['d16_sr'], btn('dv16-scan', t['d16_scan'])),
      [toggle('srv', t['d16_srv']), toggle('ignore', t['d16_ignore'], True)], t['d16_cap'],
      da(bad=t['d16_bad'], good=t['d16_good'], found=t['d16_found'], clean=t['d16_clean']))
    # 17 Storage
    D['storage-and-uploads'] = demo('dev-17',
      '<div class="dv17-wrap"><div class="dv17-file"><i></i><span>%s</span><small class="dv17-bucket"></small></div><div class="dv17-btns">%s%s</div><code class="dv17-url"></code><span class="dv17-read"></span></div>' % (t['d17_file'], btn('dv17-copy', t['d17_copy']), btn('dv17-open', t['d17_open'])),
      [toggle('private', t['d17_private'], True), slider('exp', t['d17_exp'], 5, 60, 5, 15, ' min')], t['d17_cap'],
      da(pub=t['d17_pub'], signed=t['d17_signed'], ok=t['d17_ok'], expired=t['d17_expired'], first=t['d17_first']))
    # 18 CSP
    hdrs = ''.join('<span class="dv18-h">%s</span>' % h for h in t['d18_headers'])
    D['security-headers-and-csp'] = demo('dev-18',
      '<div class="dv18-wrap"><div class="dv18-page"><div class="dv18-frame"><span>evil.example</span></div><div class="dv18-app"><b>wishlist.app</b><div class="dv18-out"></div></div></div><div class="dv18-btns">%s%s</div><div class="dv18-hdrs"><span class="dv18-h dv18-csp">Content-Security-Policy: script-src \'self\'</span><span class="dv18-h dv18-fa">Content-Security-Policy: frame-ancestors \'none\'</span>%s</div><span class="dv18-read"></span></div>' % (btn('dv18-inject', t['d18_inject']), btn('dv18-embed', t['d18_embed']), hdrs),
      [toggle('csp', t['d18_csp'], True), toggle('frame', t['d18_frame'], True)], t['d18_cap'],
      da(ran=t['d18_ran'], blk=t['d18_blk'], framed=t['d18_framed'], noframe=t['d18_noframe'], first=t['d18_first']))
    # 19 Deps
    deps = ''.join('<div class="dv19-dep"><span>%s</span><i class="dv19-v"></i></div>' % d for d in t['d19_deps'])
    D['dependencies-and-supply-chain'] = demo('dev-19',
      '<div class="dv19-wrap"><div class="dv19-deps">%s</div><div class="dv19-bar">%s<span class="dv19-known"></span></div><span class="dv19-read"></span></div>' % (deps, btn('dv19-audit', t['d19_audit'])),
      [slider('months', t['d19_months'], 0, 24, 1, 0, ''), toggle('bot', t['d19_bot'])], t['d19_cap'],
      da(known=t['d19_known'], rep=t['d19_rep'], patched=t['d19_patched'], open=t['d19_open'], first=t['d19_first']))
    # 20 Backups
    D['logs-backups-environments'] = demo('dev-20',
      '<div class="dv20-wrap"><div class="dv20-table"><b>wishlists</b><span class="dv20-rows">%s</span></div><div class="dv20-btns">%s%s</div><span class="dv20-read"></span></div>' % (t['d20_rows'], btn('dv20-oops', t['d20_oops']), btn('dv20-restore', t['d20_restore'])),
      [toggle('backup', t['d20_backup'], True), toggle('tested', t['d20_tested'])], t['d20_cap'],
      da(rows=t['d20_rows'], lost=t['d20_lost'], nobackup=t['d20_nobackup'], untested=t['d20_untested'], ok=t['d20_ok'], first=t['d20_first']))
    # 21 Personal data
    fields = ''.join('<div class="dv21-f" data-i="%d"><span class="dv21-name">%s</span>%s<small class="dv21-note"></small></div>' % (i, f, seg('dv21-c', t['d21_opts'], -1)) for i, f in enumerate(t['d21_fields']))
    D['personal-data-under-lgpd'] = demo('dev-21',
      '<div class="dv21-wrap"><div class="dv21-fields">%s</div><span class="dv21-read"></span></div>' % fields,
      [toggle('reveal', t['d21_reveal'])], t['d21_cap'],
      da(ans='|'.join(str(a) for a in t['d21_ans']), notes='|'.join(t['d21_notes']), score=t['d21_score'], first=t['d21_first']))
    # 22 Legal bases
    rows = ''.join('<div class="dv22-row" data-i="%d"><span>%s</span>%s</div>' % (i, r, seg('dv22-b', t['d22_bases'], t['d22_rec'][i])) for i, r in enumerate(t['d22_rows']))
    D['legal-bases-and-rights'] = demo('dev-22',
      '<div class="dv22-wrap"><div class="dv22-rows">%s</div><div class="dv22-btns">%s%s%s</div><span class="dv22-read"></span></div>' % (rows, btn('dv22-withdraw', t['d22_withdraw']), btn('dv22-export', t['d22_export']), btn('dv22-delete', t['d22_delete'])),
      [toggle('rights', t['d22_rights'], True)], t['d22_cap'],
      da(wok=t['d22_w_ok'], wbad=t['d22_w_bad'], expok=t['d22_exp_ok'], expman=t['d22_exp_manual'], delok=t['d22_del_ok'], delman=t['d22_del_manual'], first=t['d22_first']))
    # 23 Privacy by design
    D['privacy-by-design-in-product'] = demo('dev-23',
      '<div class="dv23-wrap"><div class="dv23-banner"></div><div class="dv23-policy"><small>%s</small><ul class="dv23-list"></ul></div><div class="dv23-btns">%s%s</div><span class="dv23-read"></span></div>' % (t['d23_policy'], btn('dv23-new', t['d11_new']), btn('dv23-del', t['d23_del'])),
      [toggle('defpriv', t['d23_defpriv'], True), toggle('analytics', t['d23_analytics'])], t['d23_cap'],
      da(bok=t['d23_banner_ok'], bbad=t['d23_banner_bad'], new=t['d23_new'], pub=t['d23_pub'], priv=t['d23_priv'], deleted=t['d23_deleted']))
    # 24 Matrix
    head = '<div class="dv24-h"></div>' + ''.join('<div class="dv24-h">%s</div>' % r for r in t['d24_roles'])
    cells = ''.join('<div class="dv24-op">%s</div>' % op + ''.join('<button type="button" class="dv24-cell" data-o="%d" data-r="%d" data-exp="%d">%s</button>' % (oi, ri, t['d24_exp'][oi][ri], '✓' if t['d24_exp'][oi][ri] else '✗') for ri in range(3)) for oi, op in enumerate(t['d24_ops']))
    D['vendors-incidents-and-launch'] = demo('dev-24',
      '<div class="dv24-wrap"><div class="dv24-grid">%s%s</div><div class="dv24-bar">%s<span class="dv24-read"></span></div></div>' % (head, cells, btn('dv24-run', t['d24_run'])),
      [toggle('rls', t['d24_rls'], True)], t['d24_cap'],
      da(pass_=t['d24_pass'].replace('%d', '%d'), fail=t['d24_fail'], first=t['d24_first']).replace('data-pass-=', 'data-pass='))
    return D
