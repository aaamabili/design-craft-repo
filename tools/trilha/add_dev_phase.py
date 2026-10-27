# Adds "Fase 4 · Desenvolvimento seguro" (weeks 17–24) to the Trilha Interface Craft artifact.
# Usage: python3 tools/trilha/add_dev_phase.py <saved live artifact html> <output page html>
# Reads the live page (so progress state and any later edits are kept), injects LESSONS.dev, the phase and tokens.
import re, sys, json, html, os
SRC, OUT = sys.argv[1], sys.argv[2]
SITE = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
s = open(SRC, encoding='utf-8').read()

# ---- lessons from the site
dev_rows = []
page = open(os.path.join(SITE, 'development.html'), encoding='utf-8').read()
for i, (lid, body) in enumerate(re.findall(r'<article class="lesson" id="([^"]+)">(.*?)</article>', page, re.S), 1):
    title = html.unescape(re.search(r'<h2>(.*?)</h2>', body).group(1))
    fh = re.search(r'<footer class="sources">(.*?)</footer>', body, re.S).group(1)
    links = [[html.unescape(re.sub('<[^>]+>', '', t)).strip(), u] for u, t in re.findall(r'<a href="([^"]+)"[^>]*>(.*?)</a>', fh, re.S)]
    dev_rows.append(dict(n=i, id=lid, title=title, src=links, books=[], extra=[]))

EXTRA = {
'how-the-web-talks': [['Chrome DevTools, Inspect network activity', 'https://developer.chrome.com/docs/devtools/network'], ['MDN, HTTP (em português)', 'https://developer.mozilla.org/pt-BR/docs/Web/HTTP']],
'what-tls-protects': [['Cloudflare Learning, What is TLS?', 'https://www.cloudflare.com/learning/ssl/transport-layer-security-tls/']],
'cookies-sessions-storage': [['MDN, Window.localStorage', 'https://developer.mozilla.org/en-US/docs/Web/API/Window/localStorage'], ['Supabase, Advanced guide to server-side auth', 'https://supabase.com/docs/guides/auth/server-side/advanced-guide']],
'same-origin-and-cors': [['web.dev, SameSite cookies explained', 'https://web.dev/articles/samesite-cookies-explained']],
'authentication-vs-authorization': [['PortSwigger, Authentication vulnerabilities', 'https://portswigger.net/web-security/authentication'], ['OWASP Top 10, A07 Identification and Authentication Failures', 'https://owasp.org/Top10/A07_2021-Identification_and_Authentication_Failures/']],
'auth-flows': [['OWASP, Password storage cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Password_Storage_Cheat_Sheet.html'], ['Supabase, Custom SMTP', 'https://supabase.com/docs/guides/auth/auth-smtp']],
'tokens-and-sessions': [['OWASP, Session management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html']],
'account-abuse': [['OWASP, Multifactor authentication cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Multifactor_Authentication_Cheat_Sheet.html']],
'data-model': [['Supabase, Storage schema design (folders per user)', 'https://supabase.com/docs/guides/storage/schema/design']],
'row-level-security': [['Supabase, RLS performance recommendations', 'https://supabase.com/docs/guides/database/postgres/row-level-security#rls-performance-recommendations'], ['OWASP, Database security cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html']],
'visibility-tiers': [['PortSwigger, Information disclosure', 'https://portswigger.net/web-security/information-disclosure']],
'broken-access-control': [['PortSwigger, Business logic vulnerabilities', 'https://portswigger.net/web-security/logic-flaws'], ['OWASP Juice Shop (laboratório)', 'https://github.com/juice-shop/juice-shop']],
'xss-and-safe-rendering': [['Hacksplaining, lições interativas', 'https://www.hacksplaining.com/lessons']],
'sql-injection': [['PostgreSQL, CREATE POLICY (format %L/%I)', 'https://www.postgresql.org/docs/current/sql-createpolicy.html']],
'csrf': [['OWASP, CSRF (community page)', 'https://owasp.org/www-community/attacks/csrf']],
'keys-and-secrets': [['The Twelve-Factor App, Config', 'https://12factor.net/config']],
'storage-and-uploads': [['Supabase, Storage access control', 'https://supabase.com/docs/guides/storage/security/access-control']],
'security-headers-and-csp': [['OWASP, Content Security Policy cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Content_Security_Policy_Cheat_Sheet.html'], ['OWASP, Secure Headers Project', 'https://owasp.org/www-project-secure-headers/'], ['MDN, Referrer-Policy', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Referrer-Policy']],
'dependencies-and-supply-chain': [['OWASP Top 10, A05 Security Misconfiguration', 'https://owasp.org/Top10/A05_2021-Security_Misconfiguration/']],
'logs-backups-environments': [['Supabase, Logs', 'https://supabase.com/docs/guides/telemetry/logs'], ['Supabase, Platform logs', 'https://supabase.com/docs/guides/platform/logs']],
'personal-data-under-lgpd': [['ICO, A guide to the data protection principles (GDPR)', 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/']],
'legal-bases-and-rights': [['gdpr.eu, DPIA template (paralelo útil)', 'https://gdpr.eu/data-protection-impact-assessment-template/']],
'privacy-by-design-in-product': [['IF, Data patterns catalogue', 'https://catalogue.projectsbyif.com/']],
'vendors-incidents-and-launch': [['roadmap.sh, Cyber security', 'https://roadmap.sh/cyber-security'], ['Supabase, Security', 'https://supabase.com/docs/guides/security']],
}
for r in dev_rows: r['extra'] = EXTRA.get(r['id'], [])

# ---- inject LESSONS.dev
i = s.index('var LESSONS = ') + len('var LESSONS = '); j = s.index(';\n  function lessonsIn', i)
L = json.loads(s[i:j].replace('<\\/', '</'))
L['dev'] = dev_rows
s = s[:i] + json.dumps(L, ensure_ascii=False).replace('</', '<\\/') + s[j:]

# ---- SEC map
s = s.replace("ai: 'AI', inbox: 'Caixa' }", "ai: 'AI', dev: 'Development', inbox: 'Caixa' }")

# ---- CSS tokens
s = s.replace("--ai: oklch(58% 0.17 275); --inbox: oklch(60% 0.05 80);", "--ai: oklch(58% 0.17 275); --dev: oklch(58% 0.15 230); --inbox: oklch(60% 0.05 80);")
s = s.replace("--ai: oklch(76% 0.13 275); --inbox: oklch(72% 0.05 80);", "--ai: oklch(76% 0.13 275); --dev: oklch(74% 0.12 230); --inbox: oklch(72% 0.05 80);")

# ---- phase 4
PHASE4 = r"""    { id: 'f4', name: 'Desenvolvimento seguro', weeks: '17 a 24', desc: 'A trilha de cybersecurity, Supabase e LGPD para qualquer app com contas e dados privados. Desenvolva com dados fictícios até os controles essenciais estarem prontos; nada aqui é certificação ou conformidade jurídica.', weeks_: [
      { n: 17, sec: 'dev', title: 'Fundamentos de web e HTTP', why: 'Requisições, status, TLS, cookies, same-origin e CORS. É a base para entender quem pode mandar qual requisição, e o que o navegador protege sozinho.',
        lessons: [['dev', 1, 4]],
        read: [
          ['MDN, HTTP', 'A referência. Comece por Overview, Methods e Status; volte quando precisar.', 'https://developer.mozilla.org/pt-BR/docs/Web/HTTP', 'voce'],
          ['web.dev, Why HTTPS matters', 'O que o cadeado garante e o que ele não garante.', 'https://web.dev/articles/why-https-matters'],
          ['OWASP, Session management cheat sheet', 'Onde a sessão mora e o que cada escolha custa.', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'],
          ['PortSwigger, CORS', 'Por que CORS não é controle de acesso, com laboratórios.', 'https://portswigger.net/web-security/cors']
        ],
        do_: [
          ['Ler a aba Network do seu app', 'Abra o DevTools, filtre por Fetch/XHR e identifique método, headers e dados de cinco requisições. Sem tokens em prints.'],
          ['Entregável: diagrama React ↔ Supabase', 'Cada seta rotulada pelo que carrega: token, JSON, arquivo. Auth, PostgREST e Storage como caixas separadas.']
        ],
        tools: [['Chrome DevTools, Network', 'documentação', 'https://developer.chrome.com/docs/devtools/network'], ['MDN, HTTP status', 'referência', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status'], ['securityheaders.com', 'checar headers', 'https://securityheaders.com/']]
      },
      { n: 18, sec: 'dev', title: 'Autenticação e sessões', why: 'Autenticação versus autorização, os fluxos de conta do Supabase Auth, tokens e expiração, e as defesas contra abuso: rate limit, CAPTCHA, MFA, redirecionamentos.',
        lessons: [['dev', 5, 8]],
        read: [
          ['Supabase Auth', 'A documentação inteira de Auth; leia Passwords, Sessions, JWTs e Redirect URLs nesta ordem.', 'https://supabase.com/docs/guides/auth', 'voce'],
          ['OWASP, Authentication cheat sheet', 'As regras de senha, mensagens neutras e recuperação, com justificativa.', 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'],
          ['jwt.io, Introduction', 'Decodifique um token de teste e veja o que ele carrega.', 'https://jwt.io/introduction'],
          ['PortSwigger, Authentication vulnerabilities', 'Laboratórios de enumeração, brute force e recuperação quebrada.', 'https://portswigger.net/web-security/authentication']
        ],
        do_: [
          ['Implementar cadastro e login com duas contas fictícias', 'Verificação de e-mail exigida, mensagens neutras, logout que revoga.'],
          ['Testar recuperação de senha e expiração de sessão', 'Link de uso único que expira; access token renovando em silêncio; "sair de todos os aparelhos".'],
          ['Entregável: fluxo de autenticação funcional e documentado', 'Um diagrama com todos os estados, inclusive os tristes.']
        ],
        tools: [['Supabase, Rate limits', 'configurar', 'https://supabase.com/docs/guides/auth/rate-limits'], ['Cloudflare Turnstile', 'CAPTCHA', 'https://developers.cloudflare.com/turnstile/'], ['Supabase, MFA', 'TOTP', 'https://supabase.com/docs/guides/auth/auth-mfa']]
      },
      { n: 19, sec: 'dev', title: 'PostgreSQL, autorização e RLS', why: 'O esquema de profiles, resources e items; auth.uid() e propriedade; uma política por operação; pública, não listada e privada impostas no banco.',
        lessons: [['dev', 9, 11]],
        read: [
          ['Supabase, Row Level Security', 'O guia oficial, com os exemplos de política que você vai adaptar.', 'https://supabase.com/docs/guides/database/postgres/row-level-security', 'voce'],
          ['PostgreSQL Tutorial', 'SQL básico até JOIN; o suficiente para escrever e ler políticas.', 'https://www.postgresql.org/docs/current/tutorial.html', 'voce'],
          ['PostgreSQL, CREATE POLICY', 'A referência de USING e WITH CHECK.', 'https://www.postgresql.org/docs/current/sql-createpolicy.html'],
          ['Supabase, Securing your data', 'A lista de erros comuns: tabelas sem RLS, views e funções que pulam políticas.', 'https://supabase.com/docs/guides/database/secure-data']
        ],
        do_: [
          ['Criar as políticas', 'Dono edita o que é seu; terceiros não leem o privado nem modificam nada. INSERT com WITH CHECK.'],
          ['Testar como visitante, usuário A e usuário B', 'Inclusive por chamadas diretas à API, sem a UI. Guarde requisição, esperado e obtido.'],
          ['Entregável: esquema, políticas SQL versionadas e matriz de permissões testada', 'Migrações no repositório; a matriz como tabela com uma linha por teste.']
        ],
        tools: [['Supabase, Database advisors', 'tabelas sem RLS', 'https://supabase.com/docs/guides/database/database-advisors'], ['PostgreSQL, Row security policies', 'referência', 'https://www.postgresql.org/docs/current/ddl-rowsecurity.html'], ['Supabase, Managing user data', 'profiles', 'https://supabase.com/docs/guides/auth/managing-user-data']]
      },
      { n: 20, sec: 'dev', title: 'OWASP e vulnerabilidades web', why: 'Broken access control e IDOR, XSS e renderização segura, SQL injection, CSRF e quando ele se aplica, configurações inseguras e dependências.',
        lessons: [['dev', 12, 15]],
        read: [
          ['OWASP Top 10', 'Leia A01, A03, A05, A06 e A07 com o app na cabeça.', 'https://owasp.org/www-project-top-ten/', 'voce'],
          ['PortSwigger Web Security Academy', 'Laboratórios gratuitos: access control, XSS, SQLi e CSRF. Faça pelo menos um de cada.', 'https://portswigger.net/web-security', 'voce'],
          ['OWASP, XSS prevention cheat sheet', 'Codificação por contexto, sanitização com allowlist.', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'],
          ['OWASP, Input validation cheat sheet', 'O que validar, onde, e por que validação não substitui parâmetros.', 'https://cheatsheetseries.owasp.org/cheatsheets/Input_Validation_Cheat_Sheet.html']
        ],
        do_: [
          ['Testar descrições com HTML e caracteres especiais', 'Payloads de XSS e SQLi em todo campo exibido. Só na sua aplicação de testes e em laboratórios autorizados.'],
          ['Trocar IDs nas requisições', 'Tente acessar dados de outra conta; confirme que o banco recusa.'],
          ['Entregável: lista de testes ofensivos e defensivos com resultados', 'Guarde ao lado do esquema e rode de novo a cada mudança.']
        ],
        tools: [['OWASP Juice Shop', 'app vulnerável para praticar', 'https://github.com/juice-shop/juice-shop'], ['Hacksplaining', 'lições interativas', 'https://www.hacksplaining.com/lessons'], ['DOMPurify', 'sanitizador', 'https://github.com/cure53/DOMPurify']]
      },
      { n: 21, sec: 'dev', title: 'Infraestrutura, uploads e DevSecOps', why: 'Chaves públicas versus privilegiadas, segredos fora do repositório, buckets e políticas de upload, headers e CSP, dependências, logs, backups e ambientes.',
        lessons: [['dev', 16, 20]],
        read: [
          ['Supabase, Storage access control', 'Buckets públicos e privados, políticas de objeto, URLs assinadas.', 'https://supabase.com/docs/guides/storage/security/access-control', 'voce'],
          ['Supabase, Going into production', 'A checklist oficial de produção; compare com a sua.', 'https://supabase.com/docs/guides/deployment/going-into-prod', 'voce'],
          ['Cloudflare Pages', 'Deploy, previews, variáveis e o arquivo _headers.', 'https://developers.cloudflare.com/pages/', 'voce'],
          ['web.dev, Strict CSP', 'Como chegar a uma CSP sem unsafe-inline num app real.', 'https://web.dev/articles/strict-csp'],
          ['OWASP, Secrets management cheat sheet', 'Onde segredos moram e como rotacionar.', 'https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html']
        ],
        do_: [
          ['Configurar buckets e políticas de upload', 'Avatares públicos, imagens de lista privadas; limites de tamanho e tipo; URLs assinadas curtas.'],
          ['Headers no Cloudflare Pages', 'HSTS, nosniff, frame-ancestors, Referrer-Policy, Permissions-Policy, CSP em report-only e depois imposta.'],
          ['Inspecionar o repositório em busca de segredos e simular uma restauração', 'gitleaks no pre-commit; um restore cronometrado num projeto descartável.'],
          ['Entregável: checklist técnico de deploy seguro', 'Com evidência por item: print do header, log do scan, tempo do restore.']
        ],
        tools: [['gitleaks', 'varredura de segredos', 'https://github.com/gitleaks/gitleaks'], ['npm audit', 'dependências', 'https://docs.npmjs.com/cli/v10/commands/npm-audit'], ['Dependabot', 'atualizações', 'https://docs.github.com/en/code-security/dependabot'], ['Supabase, Backups', 'planos e PITR', 'https://supabase.com/docs/guides/platform/backups']]
      },
      { n: 22, sec: 'dev', title: 'Fundamentos da LGPD', why: 'Dado pessoal e sensível, controlador e operador, os princípios do artigo 6, por que nem tudo exige consentimento, direitos dos titulares, crianças e adolescentes.',
        lessons: [['dev', 21, 21]],
        read: [
          ['Lei nº 13.709/2018 (LGPD), texto integral', 'Leia os artigos 5, 6, 7, 11, 14 e 18. O resto, quando precisar.', 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm', 'voce'],
          ['ANPD', 'O portal da autoridade: resoluções, guias e notícias de fiscalização.', 'https://www.gov.br/anpd/pt-br', 'voce'],
          ['Serpro, LGPD explicada', 'Resumo em português dos conceitos, bom para a primeira leitura.', 'https://www.serpro.gov.br/lgpd'],
          ['ICO, Guide to the data protection principles', 'O paralelo britânico do GDPR, mais didático que a lei brasileira.', 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/']
        ],
        do_: [
          ['Listar todos os dados armazenados', 'Para cada um: finalidade, base legal a avaliar, quem acessa, fornecedor e prazo de retenção. Inclua logs e backups.'],
          ['Entregável: inventário de dados pessoais e hipóteses de tratamento a validar', 'Uma tabela; vira a política de privacidade e o plano de incidentes depois.']
        ],
        tools: [['ANPD, materiais educativos', 'guias', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'], ['IF, Data patterns catalogue', 'padrões de consentimento', 'https://catalogue.projectsbyif.com/']]
      },
      { n: 23, sec: 'dev', title: 'LGPD aplicada ao produto', why: 'Privacy by design, perfil público versus lista privada com controle real no backend, política e termos, cookies, retenção e exclusão, fornecedores e incidentes.',
        lessons: [['dev', 22, 23]],
        read: [
          ['ANPD, materiais educativos e publicações', 'Os guias orientativos; cookies e agentes de pequeno porte primeiro.', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes', 'voce'],
          ['ANPD, guia de segurança para agentes de tratamento de pequeno porte', 'O mínimo esperado de um projeto pequeno, em linguagem direta.', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte', 'voce'],
          ['ANPD, guia orientativo sobre cookies', 'Quais cookies precisam de consentimento e como pedir.', 'https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf'],
          ['ANPD, incidentes de segurança', 'O que comunicar, a quem e quando.', 'https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca']
        ],
        do_: [
          ['Implementar controle de visibilidade, exclusão de conta, página de privacidade e canal de contato', 'Excluir cascateia por linhas, arquivos e índices; a página diz o prazo dos backups.'],
          ['Revisar termos e documentação dos fornecedores', 'Supabase, Cloudflare, GitHub: o que tratam, onde, sob quais termos. Avalie a necessidade de apoio jurídico.'],
          ['Entregável: pacote mínimo de documentação e funcionalidades de privacidade', 'Política, termos, inventário, fluxo de exclusão, contato, plano de incidentes numa página.']
        ],
        tools: [['ANPD, transferência internacional', 'regras', 'https://www.gov.br/anpd/pt-br/assuntos/transferencia-internacional-de-dados'], ['ICO, advice for small organisations', 'paralelo', 'https://ico.org.uk/for-organisations/advice-for-small-organisations/']]
      },
      { n: 24, sec: 'dev', title: 'Testes, revisão e pré-lançamento', why: 'A revisão com evidência: três usuários em toda operação, arquivos e URLs, auth, headers, segredos, dependências, backups, documentos da LGPD, plano de incidentes e riscos residuais.',
        lessons: [['dev', 24, 24]],
        read: [
          ['OWASP, Web Security Testing Guide', 'O método de teste; use o índice para montar seu roteiro.', 'https://owasp.org/www-project-web-security-testing-guide/'],
          ['OWASP, Application Security Verification Standard', 'Os requisitos verificáveis; nível 1 é a meta de um app pequeno.', 'https://owasp.org/www-project-application-security-verification-standard/'],
          ['Supabase, Going into production', 'Releia como checklist final.', 'https://supabase.com/docs/guides/deployment/going-into-prod', 'voce']
        ],
        do_: [
          ['Testes com visitante, dono e outro usuário em todas as operações', 'A matriz de permissões inteira, pela API, com resultado registrado.'],
          ['Testes de permissões de arquivos e URLs de imagens privadas', 'Buscar como o usuário errado; conferir que links copiados expiram.'],
          ['Revisão de autenticação, senhas, e-mails e redirecionamentos', 'Mensagens neutras, links de uso único, allowlist de redirecionamento.'],
          ['Verificação de headers, CSP, HTTPS, uploads e URLs externas', 'Scanner externo mais console aberto.'],
          ['Revisão de segredos, dependências, backups e alertas', 'Bundle sem service_role; audit limpo; restore feito; alertas disparando.'],
          ['Revisão do inventário, política, retenção e exclusão', 'Contra o que o código de fato faz.'],
          ['Plano de incidentes: detectar, conter, avaliar, comunicar', 'Contatos, modelos e critérios escritos; um exercício de mesa de chave vazada.'],
          ['Registro de riscos residuais e pendências', 'Com responsável e data, assinado antes de aceitar usuários reais.'],
          ['Checklist final de preparação', 'Sei explicar autenticação versus autorização · RLS ativa, testada com múltiplas contas · chave privilegiada nunca no cliente · Storage respeita as listas · HTTPS, headers e validação revisados · dependências, segredos, logs e backups com procedimento · inventário e bases legais documentados · informação clara sobre visibilidade · usuários exercem direitos · procedimento de incidentes · termos e políticas revisados.'],
          ['Entregável: relatório de pré-lançamento com evidências e pendências', 'Simule o lançamento com contas de teste; documente falhas, correções e retestes.']
        ],
        tools: [['Supabase, Security', 'visão geral', 'https://supabase.com/docs/guides/security'], ['roadmap.sh, Cyber security', 'o que vem depois', 'https://roadmap.sh/cyber-security'], ['roadmap.sh, Backend', 'o que vem depois', 'https://roadmap.sh/backend']]
      }
    ] }"""
k = s.index('  var HABITS'); k2 = s.rindex('  ];', 0, k)
s = s[:k2].rstrip() + ',\n' + PHASE4 + '\n' + s[k2:]

# ---- repair the self-publish escaping bug (it corrupted the esc() regex) and make it script-only
s = s.replace("replace(/<\\/g, '&lt;')", "replace(/</g, '&lt;')")
s = s.replace(".replace(/<\\//g, '<\\\\/')", ".replace(/<\\/script/gi, '<\\\\/script')")

# ---- hero copy
s = s.replace('16 semanas · 3 sessões de 60 a 90 min por semana', '24 semanas · 3 sessões de 60 a 90 min por semana')
s = s.replace('e por último a fronteira. Cada semana', 'depois a fronteira, e por último o desenvolvimento seguro do seu próprio app. Cada semana')
s = s.replace('Se faltar tempo, corte pela metade as semanas de Practice e AI e nunca as de UX e Primitives, que são onde a profundidade aparece no trabalho.', 'Se faltar tempo, corte pela metade as semanas de Practice e AI e nunca as de UX e Primitives, que são onde a profundidade aparece no trabalho. Na fase 4, a ordem de prioridade é: autorização e RLS com testes entre usuários; autenticação e sessões; Storage, segredos e infraestrutura; OWASP; LGPD.')

# ---- output: the page content only (between the skeleton's <body> and </body></html>), with the root left for the script to render
body = s[s.index('<title>'):s.rindex('</body></html>')]
body = re.sub(r'<div id="root" class="wrap">.*?</div>\n\n<script type="application/json" id="state">', '<div id="root" class="wrap"></div>\n\n<script type="application/json" id="state">', body, count=1, flags=re.S)
open(OUT, 'w', encoding='utf-8').write(body)
print('dev lessons', len(dev_rows), 'phase inserted', 'f4' in body, 'out bytes', len(body))
