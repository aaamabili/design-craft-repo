# Development section — Portuguese content. Mirrors content_en.py (same ids, titles kept in English like the rest of the site).
from content_en import L

HEAD = dict(eyebrow='Seção 10', title='Development', desc='Publicar um web app de verdade, com contas, perfis compartilháveis e dados privados, sem vazar nada. HTTP, autenticação, Postgres e Row Level Security, as falhas do OWASP, segredos e infraestrutura, e a LGPD como requisito de produto, para qualquer app em que pessoas entram e guardam coisas que são delas.')

PT = [
dict(id='how-the-web-talks', title='How the Web Talks',
lede='Toda tela que você desenha é uma sequência de requisições HTTP. O método diz a intenção, o caminho diz o recurso, o status diz o que aconteceu. Ler isso na aba Network é a primeira habilidade de segurança, porque todo o resto é sobre quem pode mandar qual requisição.',
body='''<h3>Por quê</h3>
          <p>Um web app é um navegador conversando com uma API por HTTP. O navegador manda uma requisição com método, caminho, headers e às vezes um corpo; o servidor responde com um código de status, headers e um corpo, em geral JSON. Os métodos carregam significado: GET lê, POST cria, PATCH altera parte de algo, DELETE remove. Os códigos carregam o resultado: 200 ok, 201 criado, 204 feito sem nada para devolver, 400 você mandou algo errado, 401 você não está identificado, 403 você está identificado e mesmo assim não pode, 404 não está aqui, 429 devagar, 500 nós quebramos. A diferença entre 401 e 403 é a diferença entre autenticação e autorização, e ela aparece na aba Network muito antes de aparecer num design.</p>
          <p>Os headers são onde mora o material de segurança interessante. A requisição carrega o token ou o cookie que identifica a pessoa; a resposta carrega as políticas que restringem o navegador. Abra o DevTools em qualquer app que você usa, filtre por Fetch/XHR e leia uma requisição de ponta a ponta. Você vai ver o que o app manda, o que recebe de volta, e o quão pouco a interface bonita tem a ver com o que o servidor de fato impõe. Uma regra para a seção inteira: nunca cole um token ou cookie real num print ou num chat. Trate como senha, porque é.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Leia a aba Network</strong> do seu app uma vez por semana. Método, caminho, status, headers, corpo.</li>
            <li><strong>Use os métodos pelo significado.</strong> GET nunca altera dados; DELETE nunca finge ser POST.</li>
            <li><strong>Mapeie status para estados de UI:</strong> 401 vai para o login, 403 diz "não é seu", 404 diz "não há nada aqui", 429 pede para esperar.</li>
            <li><strong>Desenhe o diagrama</strong> React → Supabase (Auth, PostgREST, Storage) com cada seta rotulada pelo que carrega.</li>
          </ul>''',
details=['<strong>401 e 403 são telas diferentes.</strong> Uma pergunta quem você é, a outra diz não.',
 '<strong>204 é sucesso com corpo vazio;</strong> não mostre erro porque o JSON veio vazio.',
 '<strong>Idempotência:</strong> GET, PUT e DELETE podem repetir sem dano; POST não.',
 '<strong>O corpo de um 4xx é para quem desenvolve;</strong> o texto da UI é seu.',
 '<strong>Token em print é vazamento.</strong> Tarje antes de compartilhar.'],
sources=L(('MDN, An overview of HTTP', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Overview'), ('MDN, HTTP (em português)', 'https://developer.mozilla.org/pt-BR/docs/Web/HTTP'), ('MDN, HTTP response status codes', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Status'), ('MDN, HTTP request methods', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods'))),

dict(id='what-tls-protects', title='What TLS Protects',
lede='HTTPS cifra a conversa entre navegador e servidor. Esconde o conteúdo e o caminho, verifica que você chegou ao servidor certo e impede adulteração em trânsito. Não faz nada por dados em repouso, nada contra uma página maliciosa e nada sobre quem o servidor deixa entrar.',
body='''<h3>Por quê</h3>
          <p>O Transport Layer Security embrulha o HTTP de modo que alguém na mesma rede, o provedor ou um proxy hostil vê só qual host você acessou e mais ou menos quanto dado passou. Headers, cookies, tokens, corpos de requisição e respostas estão todos dentro do túnel. O certificado prova que o servidor é quem o domínio diz, e é isso que derrota uma "página de login" falsa entre você e a real. Cloudflare Pages e Supabase dão isso por padrão, com certificados renovados para você; seu trabalho é nunca oferecer um caminho em HTTP puro e dizer aos navegadores para pararem de tentar, via HSTS.</p>
          <p>Os limites importam tanto quanto as garantias. TLS protege bytes em movimento, não bytes guardados no banco, em backups ou numa linha de log. Não impede um script injetado na sua página de ler o que a página lê. Não decide se o usuário B pode ver o recurso privado do usuário A; isso é autorização, dentro do túnel, decidida pelo servidor. "O site tem o cadeado" significa exatamente uma coisa: a rede entre a pessoa e o seu servidor não é o ponto fraco.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>HTTPS em tudo, sem exceção,</strong> incluindo a URL base da API na sua configuração.</li>
            <li><strong>Ative HSTS</strong> no projeto do Pages para que navegadores recusem HTTP puro depois da primeira visita.</li>
            <li><strong>Não confunda o cadeado com segurança.</strong> Ele cobre trânsito, não armazenamento, scripts ou permissões.</li>
            <li><strong>Conteúdo misto é quebra:</strong> uma imagem ou script em http numa página https enfraquece a página.</li>
          </ul>''',
details=['<strong>O que a rede ainda vê:</strong> o hostname (SNI), tempos e tamanhos.',
 '<strong>Certificados expiram;</strong> plataformas gerenciadas renovam, self-hosted precisa de rotina.',
 '<strong>HSTS preload</strong> é compromisso; adicione só quando todo subdomínio estiver pronto.',
 '<strong>Dev local em http é ok;</strong> produção em http não.',
 '<strong>TLS não é criptografia em repouso.</strong> Pergunte o que cifra o banco e os backups.'],
sources=L(('MDN, Transport Layer Security', 'https://developer.mozilla.org/en-US/docs/Web/Security/Transport_Layer_Security'), ('web.dev, Why HTTPS matters', 'https://web.dev/articles/why-https-matters'), ('MDN, Strict-Transport-Security', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Strict-Transport-Security'), ('OWASP, TLS cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Transport_Layer_Security_Cheat_Sheet.html'))),

dict(id='cookies-sessions-storage', title='Cookies, Sessions and Browser Storage',
lede='O navegador guarda estado em três lugares: cookies, que viajam com as requisições; localStorage e sessionStorage, que scripts leem; e memória, que some ao recarregar. Onde o token de sessão mora decide quais ataques podem roubá-lo.',
body='''<h3>Por quê</h3>
          <p>Sessão é o servidor lembrando quem você é entre requisições. O portador usual é um token, e o token precisa ser guardado em algum lugar do navegador. Cookies são enviados automaticamente em toda requisição ao seu domínio, o que é conveniente e também a raiz do CSRF; com a flag HttpOnly um script não consegue lê-los, a melhor defesa contra XSS roubar a sessão; com Secure só viajam por HTTPS; com SameSite deixam de ser anexados a requisições de outros sites. O localStorage é a troca oposta: nada é enviado automaticamente, então CSRF não se aplica, mas qualquer script rodando na página consegue ler, então um único buraco de XSS entrega todas as sessões.</p>
          <p>O cliente de navegador do Supabase guarda a sessão em localStorage por padrão; configurações com renderização no servidor movem para cookies. As duas escolhas são defensáveis quando você sabe o que custam: com localStorage, XSS é o jogo inteiro e a Content Security Policy vira obrigatória; com cookies, SameSite e proteção contra CSRF viram obrigatórias. O que nunca é defensável é token em URL, token em log, ou token que nunca expira. Headers são o terceiro armazenamento que você não controla: o header Authorization é como o token chega à API a cada chamada, e a aba Network o mostra em texto claro para qualquer pessoa com o notebook aberto.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Saiba onde sua sessão mora</strong> e escreva as defesas correspondentes: CSP para localStorage, SameSite e tokens de CSRF para cookies.</li>
            <li><strong>Cookies levam HttpOnly, Secure e SameSite</strong> por padrão, sempre.</li>
            <li><strong>Nada sensível no sessionStorage também;</strong> scripts leem, só dura menos.</li>
            <li><strong>Nunca token em URL.</strong> URLs acabam em logs, histórico e referrers.</li>
          </ul>''',
details=['<strong>HttpOnly é para o token, não para preferências.</strong> Tema pode morar em localStorage.',
 '<strong>SameSite=Lax é o padrão sensato;</strong> Strict quebra links de e-mail, None exige Secure.',
 '<strong>Logout precisa limpar o armazenamento,</strong> não só o estado da UI.',
 '<strong>Computadores compartilhados:</strong> sessão persistida é decisão, ofereça "manter conectado" explicitamente.',
 '<strong>Inspecione Application → Storage</strong> no DevTools para ver exatamente o que seu app deixa para trás.'],
sources=L(('MDN, Using HTTP cookies', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Cookies'), ('OWASP, Session management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html'), ('OWASP, HTML5 security cheat sheet (local storage)', 'https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html'), ('Supabase, Sessions', 'https://supabase.com/docs/guides/auth/sessions'))),

dict(id='same-origin-and-cors', title='Same-Origin Policy and CORS',
lede='O navegador impede uma página de uma origem de ler respostas de outra. CORS é o servidor dizendo quais origens podem. Protege usuários de páginas maliciosas; não protege sua API de ninguém com curl.',
body='''<h3>Por quê</h3>
          <p>Origem é esquema mais host mais porta. A same-origin policy diz que um script em evil.example não pode ler a resposta de uma requisição à sua API, mesmo que o navegador a tenha enviado. É uma proteção do usuário: impede uma página aleatória de puxar seus dados logados através do seu próprio navegador. O CORS afrouxa isso de propósito: a API responde com Access-Control-Allow-Origin nomeando as origens que podem ler, e para requisições não simples o navegador manda antes um OPTIONS de preflight perguntando. O Supabase aceita chamadas de qualquer origem porque o portão de verdade é o token e a Row Level Security, não a origem.</p>
          <p>O mal-entendido a matar cedo: CORS é imposto por navegadores, para navegadores. Um script, um app mobile, Postman ou curl o ignoram por completo. Se sua API só funciona porque "o frontend é a única coisa que chama", ela está aberta. Do mesmo modo, um Allow-Origin curinga com credenciais é uma configuração que o navegador recusa, e um Allow-Origin refletido (ecoando a origem que pediu) é porta aberta para os ataques que a política existe para impedir. A regra: assuma que todo endpoint será chamado diretamente, por qualquer um, e faça o banco dizer não.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Trate CORS como cortesia do navegador,</strong> nunca como controle de acesso.</li>
            <li><strong>Permita origens específicas,</strong> nunca reflita a origem do pedido, nunca curinga com credenciais.</li>
            <li><strong>Todo endpoint precisa ser seguro chamado por curl</strong> com token roubado ou ausente.</li>
            <li><strong>Leia o preflight</strong> na aba Network uma vez, para o OPTIONS deixar de ser mistério.</li>
          </ul>''',
details=['<strong>Esquema, host, porta:</strong> https://app e http://app são origens diferentes.',
 '<strong>Site versus origem:</strong> cookies SameSite usam o site; CORS usa a origem.',
 '<strong>O preflight é cacheado;</strong> um OPTIONS falhando aparece como "network error" vago no console.',
 '<strong>O Supabase ignora a origem por design;</strong> RLS é o portão.',
 '<strong>Se remover o frontend expusesse dados,</strong> o backend nunca esteve protegido.'],
sources=L(('MDN, Same-origin policy', 'https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy'), ('MDN, Cross-Origin Resource Sharing', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS'), ('PortSwigger, CORS', 'https://portswigger.net/web-security/cors'), ('web.dev, Same-site and same-origin', 'https://web.dev/articles/same-site-same-origin'))),

dict(id='authentication-vs-authorization', title='Authentication vs Authorization',
lede='Autenticação responde quem você é. Autorização responde o que você pode fazer. A maioria das violações reais é falha de autorização: o sistema sabia exatamente quem era a pessoa e mesmo assim entregou os dados de outra.',
body='''<h3>Por quê</h3>
          <p>Fazer login prova identidade: esta requisição vem da conta que sabe a senha, tem o magic link ou passou pelo segundo fator. Não diz nada sobre permissões. Autorização é a decisão separada, tomada a cada requisição, de que esta identidade pode ler este recurso, editar este registro, excluir esta conta. As duas se confundem o tempo todo porque a tela de login é visível e a checagem de permissão não. O OWASP coloca Broken Access Control no topo da lista desde 2021 justamente porque times constroem fluxos de login lindos e depois confiam no frontend para esconder os botões que usuários não deveriam apertar.</p>
          <p>Para a maioria dos apps com dados de usuário, o modelo de autorização é pequeno e precisa estar escrito: visitante lê recursos públicos; pessoa logada lê recursos públicos e tudo que possui; ninguém além do dono escreve. Essa matriz é a especificação. Ela é imposta no banco, via Row Level Security, para que todo caminho até os dados, o app, uma chamada direta à API, um futuro cliente mobile, obedeça às mesmas regras. Esconder um botão Editar é interface; negar o UPDATE é segurança. Os dois são necessários, nessa ordem de importância invertida.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Escreva a matriz de permissões</strong> antes de escrever uma tabela: operação × papel, com Sim ou Não em cada célula.</li>
            <li><strong>Imponha no banco,</strong> reflita na UI. Nunca o contrário.</li>
            <li><strong>Autorize a cada requisição,</strong> não uma vez no login.</li>
            <li><strong>Teste como três pessoas:</strong> visitante, dono e outro usuário, para toda operação.</li>
          </ul>''',
details=['<strong>"Logado" não é permissão.</strong> É identidade.',
 '<strong>Negar por padrão:</strong> tudo é proibido até uma regra permitir.',
 '<strong>Dono é uma coluna, não um sentimento:</strong> user_id em toda linha que pertence a alguém.',
 '<strong>Admin é um papel com auditoria própria,</strong> não uma senha compartilhada.',
 '<strong>A matriz é o plano de testes.</strong> Cada célula é um teste.'],
sources=L(('Auth0, Authentication vs. authorization', 'https://auth0.com/docs/get-started/identity-fundamentals/authentication-and-authorization'), ('OWASP, Authorization cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'), ('OWASP Top 10, A01 Broken Access Control', 'https://owasp.org/Top10/A01_2021-Broken_Access_Control/'))),

dict(id='auth-flows', title='Sign Up, Sign In, Recover',
lede='Fluxos de conta são onde segurança e UX se encontram com mais força. Verificação de e-mail, regras de senha, links de recuperação e logout têm cada um uma forma correta, e o Supabase Auth implementa a maior parte, mas o produto ainda decide o que é exigido e o que a pessoa vê.',
body='''<h3>Por quê</h3>
          <p>Cadastro cria uma identidade; login prova; logout encerra a sessão; recuperação deixa alguém voltar sem a senha. Cada passo é superfície de ataque. E-mails não verificados permitem registrar endereços que a pessoa não possui, que depois viram forma de sequestrar contas ou enviar spam. Regras de senha fracas convidam credential stuffing; o conserto é tamanho mínimo, checagem contra senhas vazadas, e nenhuma regra de composição que produza "Senha1!". Recuperação é o buraco clássico: um link que nunca expira, que funciona mais de uma vez, ou que revela se um e-mail existe, entrega contas a atacantes. Logout que só limpa a UI deixa um token válido no aparelho.</p>
          <p>O Supabase Auth dá cadastro com e-mail de confirmação, login por senha, magic links, provedores OAuth, recuperação de senha e gestão de sessão. As decisões que sobram são de produto: exigir verificação antes de qualquer escrita; mostrar a mesma mensagem neutra exista ou não o e-mail; expirar links de recuperação rápido e uma única vez; invalidar outras sessões na troca de senha; e fazer "Sair" revogar o refresh token, não só descartar o estado local. Documente o fluxo como diagrama com todo estado, inclusive os tristes, porque esse diagrama também é a especificação de UX.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Exija verificação de e-mail</strong> antes de a conta poder criar ou compartilhar qualquer coisa.</li>
            <li><strong>Mensagens neutras:</strong> "Se esse e-mail existir, enviamos um link", para cadastro, recuperação e erro de login igualmente.</li>
            <li><strong>Links de recuperação expiram e são de uso único;</strong> troca de senha invalida outras sessões.</li>
            <li><strong>Sair revoga</strong> a sessão no servidor e limpa o armazenamento local.</li>
          </ul>''',
details=['<strong>Mínimo de 12 caracteres, sem regras de composição,</strong> checagem contra vazamentos conhecidos.',
 '<strong>O e-mail de verificação é parte do produto:</strong> escreva, teste, dê marca.',
 '<strong>SMTP próprio em produção;</strong> o remetente padrão tem limites estritos.',
 '<strong>Destinos de redirecionamento em allowlist,</strong> nunca tirados de query string.',
 '<strong>Duas contas de teste, sempre.</strong> Uma nunca basta para achar bug de autorização.'],
sources=L(('Supabase, Auth overview', 'https://supabase.com/docs/guides/auth'), ('Supabase, Password-based auth', 'https://supabase.com/docs/guides/auth/passwords'), ('Supabase, Password security', 'https://supabase.com/docs/guides/auth/password-security'), ('OWASP, Forgot password cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Forgot_Password_Cheat_Sheet.html'), ('OWASP, Authentication cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authentication_Cheat_Sheet.html'))),

dict(id='tokens-and-sessions', title='Tokens, JWTs and Expiry',
lede='Um JWT é uma afirmação assinada sobre quem é o portador, válida até expirar. Access tokens curtos limitam o dano de um roubo; refresh tokens estendem a sessão sem novo login. Assinado não é cifrado: qualquer um lê um JWT.',
body='''<h3>Por quê</h3>
          <p>Depois do login, o Supabase emite um access token, um JSON Web Token assinado pelo projeto, e um refresh token. O access token viaja em toda chamada à API no header Authorization; o Postgres lê suas claims, e é assim que auth.uid() sabe quem está pedindo. Ele expira em cerca de uma hora por padrão. Quando expira, o cliente usa o refresh token para obter um novo par, em silêncio. O desenho é uma troca: access tokens curtos fazem um token roubado servir por pouco tempo; refresh tokens evitam login a cada hora. A rotação de refresh token, ligada por padrão, torna cada refresh token de uso único, então um roubado que seja reusado depois de o cliente legítimo tê-lo usado derruba a sessão inteira.</p>
          <p>Três fatos evitam a maioria dos erros com JWT. Um: o payload é base64, não cifrado, então nunca ponha segredos nele e assuma que a pessoa lê as próprias claims. Dois: o servidor não consulta o token num banco; verifica a assinatura, por isso revogar é difícil e a expiração é o controle real. Três: o segredo de assinatura e a chave service role são as chaves do reino; nunca saem do servidor. A expiração da sessão também é decisão de produto: um app de baixo risco não precisa de timeout de banco, mas "lembrar para sempre" num computador compartilhado é escolha consciente, com um jeito visível de sair de todos os aparelhos.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Access tokens curtos,</strong> cliente renovando em silêncio, rotação ligada.</li>
            <li><strong>Nunca confie em claims do lado do cliente para permissões;</strong> o banco verifica a assinatura e aplica RLS.</li>
            <li><strong>Ofereça "sair de todos os aparelhos"</strong> e dispare isso na troca de senha.</li>
            <li><strong>Decodifique um token uma vez no jwt.io</strong> com conta de teste, para saber exatamente o que ele carrega.</li>
          </ul>''',
details=['<strong>exp é o controle.</strong> Todo o resto de um JWT é conveniência.',
 '<strong>Rotação detecta reuso:</strong> refresh token repetido mata a sessão.',
 '<strong>A claim role é "authenticated" ou "anon",</strong> não a flag de admin do seu app.',
 '<strong>Desvio de relógio existe;</strong> não entre em pânico com um token rejeitado segundos antes.',
 '<strong>Token em log é credencial em log.</strong> Limpe o header Authorization.'],
sources=L(('Supabase, JSON Web Tokens', 'https://supabase.com/docs/guides/auth/jwts'), ('Supabase, User sessions', 'https://supabase.com/docs/guides/auth/sessions'), ('jwt.io, Introduction to JSON Web Tokens', 'https://jwt.io/introduction'), ('PortSwigger, JWT attacks', 'https://portswigger.net/web-security/jwt'))),

dict(id='account-abuse', title='Rate Limits, CAPTCHA, MFA and Redirects',
lede='Atacantes automatizam. Rate limits tornam adivinhar caro, CAPTCHA sobe o custo de bots onde a fricção vale a pena, MFA protege as contas que mais importam, e uma allowlist de redirecionamento impede seu login de virar lançador de phishing.',
body='''<h3>Por quê</h3>
          <p>Um formulário de login sem limites é um oráculo: tente um milhão de senhas, guarde as que funcionam. O Supabase aplica rate limits nos endpoints de auth e deixa ajustar; seu app também deve recuar no cliente, mostrar o 429 como "muitas tentativas, espere um minuto", e nunca revelar se o e-mail ou a senha era a metade errada. CAPTCHA, via provedores como o Cloudflare Turnstile, cabe no cadastro e na recuperação, onde bots criam contas lixo e disparam enxurradas de e-mail, e deve ficar fora do login diário a menos que apareça abuso, porque cada desafio é fricção paga por gente honesta.</p>
          <p>Autenticação multifator é o maior upgrade para as contas que podem causar dano: a sua, como admin, e qualquer papel com direitos elevados. O Supabase suporta TOTP; exigir no login de admin custa segundos e tira a senha de ponto único de falha. Redirecionamentos são o item silencioso: fluxos de auth mandam a pessoa de volta a uma URL depois do login ou da recuperação, e se essa URL vem da requisição, um link forjado loga alguém no seu site real e a deixa numa página do atacante. O Supabase só redireciona para URLs registradas; mantenha a lista curta e nunca adicione a ela a partir de entrada do usuário.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Rate limits no auth e em todo endpoint que envia e-mail;</strong> mostre 429 como um "espere" calmo.</li>
            <li><strong>CAPTCHA no cadastro e na recuperação,</strong> não em todo login, a menos que veja abuso.</li>
            <li><strong>MFA obrigatório para contas admin,</strong> opcional para as outras, com códigos de recuperação.</li>
            <li><strong>Só allowlist de redirecionamento.</strong> Sem open redirect, sem redirecionamento vindo de query string.</li>
          </ul>''',
details=['<strong>Mesmo erro para e-mail errado e senha errada.</strong> Enumeração começa com uma mensagem prestativa.',
 '<strong>Bloqueio de conta é vetor de negação de serviço;</strong> prefira backoff a travas rígidas.',
 '<strong>Turnstile em vez de quebra-cabeças de imagem:</strong> invisível para a maioria, caro para bots.',
 '<strong>Admin é uma história de login separada,</strong> com MFA e log de auditoria próprio.',
 '<strong>Teste um redirecionamento forjado uma vez</strong> para ver a allowlist recusar.'],
sources=L(('Supabase, Rate limits', 'https://supabase.com/docs/guides/auth/rate-limits'), ('Supabase, Bot detection with CAPTCHA', 'https://supabase.com/docs/guides/auth/auth-captcha'), ('Supabase, Multi-factor authentication', 'https://supabase.com/docs/guides/auth/auth-mfa'), ('Supabase, Redirect URLs', 'https://supabase.com/docs/guides/auth/redirect-urls'), ('OWASP, Unvalidated redirects cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Unvalidated_Redirects_and_Forwards_Cheat_Sheet.html'), ('Cloudflare Turnstile', 'https://developers.cloudflare.com/turnstile/'))),

dict(id='data-model', title='Modeling Owners, Resources and Items',
lede='Três tabelas carregam o padrão: profiles, resources, items. Chaves estrangeiras tornam as relações reais, constraints tornam dados ruins impossíveis, e a coluna de dono em toda linha é o que a Row Level Security vai checar depois. Modele para as permissões que vai precisar.',
body='''<h3>Por quê</h3>
          <p>O Supabase mantém a autenticação em auth.users, que você não edita diretamente. O perfil público (nome de exibição, handle, avatar) mora numa tabela profiles com o mesmo id, criada por um trigger quando alguém se cadastra. Recursos referenciam o perfil por uma chave estrangeira user_id e carregam uma coluna de visibilidade; itens referenciam o recurso pai. Chaves estrangeiras com ON DELETE CASCADE fazem excluir uma conta remover seus recursos e itens, o que é limpo e, como as aulas de LGPD vão mostrar, uma necessidade legal. Constraints fazem o resto da higiene: NOT NULL onde o valor é obrigatório, UNIQUE no handle, CHECK na visibilidade para só existirem os três valores permitidos, e limite de tamanho nos títulos para ninguém guardar um romance.</p>
          <p>Índices deixam as consultas comuns rápidas: recursos por user_id, itens por resource_id, perfis por handle. Chaves primárias em UUID em vez de inteiros sequenciais fecham o ataque mais barato que existe, adivinhar o próximo id, embora UUID não substitua autorização. Escreva o esquema como migrações SQL no repositório, não como cliques num painel; SQL versionado é o que permite reconstruir o banco, revisar uma mudança e saber qual política existia quando.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>profiles(id → auth.users), resources(user_id, visibility), items(resource_id).</strong> Coluna de dono em tudo que tem dono.</li>
            <li><strong>Constraints antes de código:</strong> NOT NULL, UNIQUE, CHECK, limites de tamanho.</li>
            <li><strong>Chaves primárias UUID,</strong> e índice em toda chave estrangeira usada em filtro.</li>
            <li><strong>Migrações no git.</strong> O painel é para ler, o repositório é a verdade.</li>
          </ul>''',
details=['<strong>Nunca guarde o e-mail em profiles</strong> a menos que precise dele público; auth.users já o tem.',
 '<strong>CASCADE é decisão de design;</strong> escreva o que desaparece junto com a conta.',
 '<strong>Timestamps com fuso,</strong> created_at e updated_at em toda tabela.',
 '<strong>Visibilidade como CHECK constraint,</strong> não string livre.',
 '<strong>Popule com dados fictícios</strong> e mantenha um script para resetar.'],
sources=L(('Supabase, Managing user data', 'https://supabase.com/docs/guides/auth/managing-user-data'), ('PostgreSQL, Constraints', 'https://www.postgresql.org/docs/current/ddl-constraints.html'), ('PostgreSQL, Indexes', 'https://www.postgresql.org/docs/current/indexes.html'), ('Supabase, Cascade deletes', 'https://supabase.com/docs/guides/database/postgres/cascade-deletes'), ('PostgreSQL, Tutorial', 'https://www.postgresql.org/docs/current/tutorial.html'))),

dict(id='row-level-security', title='Row Level Security',
lede='RLS transforma autorização em regras do banco: cada tabela ganha políticas que dizem quais linhas um usuário pode selecionar, inserir, atualizar ou excluir. Com auth.uid() na política, o próprio banco recusa o que a pessoa não pode, seja quem for e de onde for.',
body='''<h3>Por quê</h3>
          <p>O Supabase expõe suas tabelas por uma API que o navegador chama diretamente com o token da pessoa. Isso só funciona porque Row Level Security está ligada: uma tabela sem RLS e com a chave anon no cliente é pública para o mundo. Com RLS ativa, o Postgres avalia uma política para cada linha em cada operação. A política pode ler auth.uid(), o id do token verificado, e comparar com a coluna de dono. Uma política por operação mantém a lógica legível: SELECT permite donos e, para recursos públicos, todo mundo; INSERT checa que o user_id da linha nova é quem chama; UPDATE e DELETE permitem só o dono. Políticas são aditivas: se qualquer uma permite, a linha passa, então uma permissiva esquecida de testes é um buraco.</p>
          <p>Duas práticas mantêm a RLS honesta. Primeira, teste de fora da UI: rode a mesma consulta como visitante sem token, como usuário A, como usuário B, pela API, e compare as linhas. Segunda, mantenha as políticas em migrações e revise como código, porque política é código. Performance vem junto: embrulhe auth.uid() num subselect para ser avaliado uma vez, indexe as colunas que as políticas comparam, e evite joins dentro de políticas. Os advisors do Supabase apontam tabelas sem RLS e políticas que parecem erradas; rode antes de todo release.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>ALTER TABLE … ENABLE ROW LEVEL SECURITY</strong> em toda tabela, antes da primeira linha.</li>
            <li><strong>Uma política por operação,</strong> nomeada pelo que permite: "donos atualizam seus recursos".</li>
            <li><strong>INSERT usa WITH CHECK</strong> para ninguém criar linhas de outro dono.</li>
            <li><strong>Teste pela API como três pessoas</strong> e guarde os resultados numa tabela no repositório.</li>
          </ul>''',
details=['<strong>Sem RLS mais chave anon é tabela pública.</strong> Não há meio-termo.',
 '<strong>Políticas são somadas com OU.</strong> Apague a "permite tudo para teste".',
 '<strong>(select auth.uid())</strong> em vez de auth.uid() para velocidade em tabelas grandes.',
 '<strong>service_role ignora RLS,</strong> por isso nunca chega ao cliente.',
 '<strong>Views e funções precisam de pensamento próprio;</strong> funções security definer pulam a RLS.'],
sources=L(('Supabase, Row Level Security', 'https://supabase.com/docs/guides/database/postgres/row-level-security'), ('PostgreSQL, Row security policies', 'https://www.postgresql.org/docs/current/ddl-rowsecurity.html'), ('PostgreSQL, CREATE POLICY', 'https://www.postgresql.org/docs/current/sql-createpolicy.html'), ('Supabase, Securing your data', 'https://supabase.com/docs/guides/database/secure-data'), ('Supabase, Database advisors', 'https://supabase.com/docs/guides/database/database-advisors'))),

dict(id='visibility-tiers', title='Public, Unlisted, Private',
lede='Um recurso de usuário tem três públicos: qualquer um, qualquer um com o link, só o dono. Cada nível é uma política no banco e uma frase na interface. Se a frase promete mais do que a política impõe, o produto está mentindo.',
body='''<h3>Por quê</h3>
          <p>Recursos públicos aparecem na busca e no perfil; não listados abrem para quem tem a URL mas não aparecem em lugar nenhum; privados são só do dono. A diferença é trivial na UI e decisiva no banco. Pública: SELECT permitido para todos onde visibility = public. Não listada: SELECT permitido para todos por id, mas a consulta que alimenta a página de perfil as exclui, então descobrir depende de saber o UUID, por isso o id precisa ser inadivinhável. Privada: SELECT só para o dono. Itens herdam a visibilidade do pai por uma política que faz join com o pai, ou por uma coluna desnormalizada mantida em sincronia por trigger.</p>
          <p>A interface precisa dizer exatamente o que cada nível significa, onde a pessoa escolhe, em palavras simples: "Qualquer um pode encontrar isto", "Só quem tem o link", "Só você". O princípio da transparência da LGPD torna isso mais que boa educação. E o padrão importa: um recurso novo deve ser privado até a pessoa decidir o contrário, porque um recurso público por acidente é um vazamento que a pessoa não consentiu. Teste os níveis como um atacante: busque um recurso não listado por id sem token, liste os recursos de um perfil e confira que os não listados estão ausentes, busque um privado como outro usuário e espere nada de volta.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Três valores, uma CHECK constraint, três políticas.</strong> Nenhum outro estado.</li>
            <li><strong>Privada por padrão.</strong> Compartilhar é ação que a pessoa toma.</li>
            <li><strong>Rótulos em linguagem simples</strong> no controle, não numa página de ajuda.</li>
            <li><strong>Filhos seguem o pai;</strong> nunca deixe um item mais visível que o pai.</li>
          </ul>''',
details=['<strong>Não listada significa inadivinhável:</strong> ids UUID v4, nenhum número sequencial em lugar nenhum.',
 '<strong>Mudar para privada vale na hora,</strong> incluindo páginas em cache e imagens.',
 '<strong>A busca indexa só recursos públicos;</strong> não listados nunca vazam pela busca.',
 '<strong>O diálogo de compartilhar repete a visibilidade</strong> no momento de copiar o link.',
 '<strong>URLs de imagem seguem o nível também;</strong> recurso privado com imagem pública não é privado.'],
sources=L(('Supabase, Row Level Security', 'https://supabase.com/docs/guides/database/postgres/row-level-security'), ('OWASP, Authorization cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html'), ('ANPD, materiais educativos', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'))),

dict(id='broken-access-control', title='Broken Access Control and IDOR',
lede='Troque o id na URL e veja os dados de outra pessoa: isso é uma Insecure Direct Object Reference, o bug sério mais comum da web. O conserto nunca é esconder o id; é fazer toda consulta checar propriedade, o que a RLS faz se as políticas estão certas.',
body='''<h3>Por quê</h3>
          <p>O OWASP coloca Broken Access Control em primeiro porque está em todo lugar e é simples: o app checa quem você é, busca o registro que você pediu, e esquece de checar se o registro é seu. A versão de API se chama BOLA, Broken Object Level Authorization. Sintomas: mudar /resources/42 para /resources/43 mostra o recurso privado de outra pessoa; um PATCH no item de outro usuário dá certo; um endpoint de exportação devolve os dados de todo mundo porque o filtro era aplicado no frontend. Ids inadivinháveis atrasam isso e não consertam; um atacante que viu um id uma vez, num link compartilhado ou num print, o tem para sempre.</p>
          <p>A defesa é estrutural. Com RLS ligada e correta, a consulta que busca o recurso 43 devolve nada para o usuário errado, mande o frontend o que mandar. O trabalho que sobra é testar: para cada operação da matriz de permissões, execute como o usuário errado pela API e confirme a recusa. Guarde um documento desses testes com a requisição, o resultado esperado e o obtido; é a evidência de que seu controle de acesso funciona, e a primeira coisa a rodar de novo depois de qualquer mudança de esquema. Vigie também os caminhos de segunda ordem: joins que puxam linhas relacionadas, funções que rodam com direitos elevados, e arquivos no storage cujas URLs pulam o banco por completo.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Toda busca de objeto é filtrada por propriedade ou visibilidade,</strong> no banco.</li>
            <li><strong>Teste troca de id</strong> em todo endpoint, como visitante e como outro usuário.</li>
            <li><strong>Ids inadivinháveis são cortesia,</strong> não controle.</li>
            <li><strong>Mantenha o log de testes ofensivos</strong> ao lado do esquema e rode de novo a cada mudança.</li>
          </ul>''',
details=['<strong>Negar por padrão devolve vazio ou 404,</strong> não 403 com o nome do objeto.',
 '<strong>Mass assignment é o primo:</strong> nunca deixe o cliente definir user_id ou visibilidade na linha de outro.',
 '<strong>Endpoints em lote filtram por linha,</strong> não por requisição.',
 '<strong>Funções SECURITY DEFINER</strong> precisam de checagem de propriedade própria.',
 '<strong>Automatize o teste de três usuários</strong> depois que funcionar à mão.'],
sources=L(('OWASP Top 10, A01 Broken Access Control', 'https://owasp.org/Top10/A01_2021-Broken_Access_Control/'), ('PortSwigger, Access control vulnerabilities', 'https://portswigger.net/web-security/access-control'), ('PortSwigger, IDOR', 'https://portswigger.net/web-security/access-control/idor'), ('OWASP API Security, Broken Object Level Authorization', 'https://owasp.org/API-Security/editions/2023/en/0xa1-broken-object-level-authorization/'))),

dict(id='xss-and-safe-rendering', title='XSS and Safe Rendering',
lede='Cross-site scripting é conteúdo de usuário executando como código no navegador de outro usuário. A defesa é renderizar texto como texto: o React faz isso por padrão, dangerouslySetInnerHTML desfaz, e uma Content Security Policy pega o que escapar.',
body='''<h3>Por quê</h3>
          <p>Todo app guarda texto que as pessoas digitam: títulos, notas, bios de perfil, URLs. Se qualquer parte disso entra na página como HTML, uma nota contendo uma tag script roda no navegador de todo mundo que vê a página, com a sessão de cada um. Isso é XSS armazenado, e com a sessão em localStorage é fim de jogo para todo visitante. O React escapa texto no JSX, então o caminho comum é seguro; os buracos são as saídas de emergência: dangerouslySetInnerHTML, escrever em innerHTML, montar strings de HTML, e atributos que recebem URLs, onde links javascript: executam no clique. Renderização de Markdown é fonte clássica, porque o renderizador produz HTML a partir de texto não confiável.</p>
          <p>As regras são curtas. Nunca renderize conteúdo de usuário como HTML a menos que tenha passado por um sanitizador como o DOMPurify com allowlist de tags. Valide URLs antes de usar como href ou src: só http e https, nada mais. Defina uma Content Security Policy que proíba scripts inline, para que mesmo uma tag injetada não rode. E teste com os payloads que importam: uma tag script, um img com onerror, uma URL javascript:, um svg com onload, em todo campo que depois é exibido. Codificação de saída é contextual, por isso "escapar tudo" não é estratégia; o contexto (texto HTML, atributo, URL, JavaScript) decide a codificação.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Texto continua texto.</strong> Nada de dangerouslySetInnerHTML com conteúdo de usuário, nunca.</li>
            <li><strong>Sanitize com allowlist</strong> se precisar renderizar texto rico; DOMPurify, não regex.</li>
            <li><strong>Permita só http(s) em URLs</strong> digitadas; renderize o resto como texto simples.</li>
            <li><strong>CSP sem unsafe-inline</strong> como segunda camada.</li>
          </ul>''',
details=['<strong>Markdown é HTML com passos extras;</strong> sanitize depois de renderizar.',
 '<strong>Teste campos com</strong> &lt;img src=x onerror=alert(1)&gt; e um link javascript:.',
 '<strong>DOM XSS mora no cliente:</strong> location.hash em innerHTML é clássico.',
 '<strong>rel="noopener"</strong> em links para URLs fornecidas por usuários.',
 '<strong>Scripts de terceiros compartilham sua origem;</strong> carregue o mínimo possível.'],
sources=L(('PortSwigger, Cross-site scripting', 'https://portswigger.net/web-security/cross-site-scripting'), ('OWASP, XSS prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html'), ('OWASP, DOM-based XSS prevention', 'https://cheatsheetseries.owasp.org/cheatsheets/DOM_based_XSS_Prevention_Cheat_Sheet.html'), ('React, dangerouslySetInnerHTML', 'https://react.dev/reference/react-dom/components/common#dangerously-setting-the-inner-html'), ('DOMPurify', 'https://github.com/cure53/DOMPurify'))),

dict(id='sql-injection', title='SQL Injection',
lede='Injeção acontece quando dado é colado numa consulta como texto e o banco o lê como código. Consultas parametrizadas mantêm os dois separados. O cliente do Supabase e o PostgREST parametrizam por você; o risco volta no momento em que você monta strings de SQL.',
body='''<h3>Por quê</h3>
          <p>O ataque tem quarenta anos e continua na lista do OWASP porque concatenar strings é fácil. Uma caixa de busca que vira WHERE title = \'… transforma uma aspa simples num jeito de encerrar a string e escrever mais SQL: ler outras tabelas, pular um login, derrubar uma tabela. A defesa não é escapar aspas; é nunca misturar dado ao texto da consulta. Consultas parametrizadas enviam o SQL e os valores separados, então o banco trata o valor como valor, sejam quais forem os caracteres. O cliente JavaScript do Supabase monta requisições parametrizadas, e o PostgREST faz o mesmo no servidor, então o caminho comum é seguro.</p>
          <p>Os buracos aparecem onde você escreve SQL: funções do banco que montam consultas dinâmicas por concatenação, chamadas RPC que recebem fragmentos crus, Edge Functions que falam direto com o Postgres, e scripts de admin. Em funções Postgres use format() com %L e %I, ou EXECUTE … USING, nunca || com entrada de usuário. Validação de entrada ajuda por sanidade (número de página é número) mas não é a defesa; uma string de aparência válida ainda pode ser injeção. Teste com os payloads clássicos em toda entrada que chega a uma consulta e observe erros que vazam a consulta, o que por si já é divulgação de informação.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Parâmetros, nunca concatenação,</strong> em todo lugar que toca SQL.</li>
            <li><strong>Em funções Postgres,</strong> format() com %L/%I ou EXECUTE … USING.</li>
            <li><strong>Usuário de banco com privilégio mínimo</strong> para qualquer código de servidor que você escreva.</li>
            <li><strong>Mensagens de erro para usuários são genéricas;</strong> o erro real vai para o log.</li>
          </ul>''',
details=['<strong>Teste com</strong> \' OR 1=1 -- e uma aspa em todo campo.',
 '<strong>ORMs e clientes são seguros até você chamar .raw()</strong> ou montar uma string de filtro.',
 '<strong>Nomes de coluna e tabela não são parâmetros;</strong> use allowlist.',
 '<strong>Entradas de busca full-text</strong> também passam por parâmetros.',
 '<strong>Um erro vazado com SQL dentro</strong> é um achado por si só.'],
sources=L(('PortSwigger, SQL injection', 'https://portswigger.net/web-security/sql-injection'), ('OWASP, SQL injection prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/SQL_Injection_Prevention_Cheat_Sheet.html'), ('OWASP Top 10, A03 Injection', 'https://owasp.org/Top10/A03_2021-Injection/'), ('OWASP, Database security cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Database_Security_Cheat_Sheet.html'))),

dict(id='csrf', title='CSRF and When It Applies',
lede='Cross-site request forgery é outro site fazendo o navegador mandar uma requisição ao seu com os cookies do usuário anexados. Só funciona quando a credencial viaja automaticamente. Saiba qual modelo você usa, depois aplique a defesa correspondente.',
body='''<h3>Por quê</h3>
          <p>Cookies são anexados às requisições pelo navegador, seja qual for a página que as iniciou. Um formulário escondido em evil.example que faz POST na sua API chegaria carregando o cookie de sessão da vítima, e o servidor acreditaria. Isso é CSRF. As defesas são cookies SameSite, que impedem o navegador de anexar cookies a requisições de outros sites, tokens anti-CSRF que o atacante não conhece, e checagem do header Origin. Se em vez disso o token de sessão mora em localStorage e é enviado como header Authorization pelo seu próprio JavaScript, uma página estranha não consegue adicionar esse header, e CSRF não se aplica; o preço, como a aula de armazenamento disse, é que XSS vira o jogo inteiro.</p>
          <p>O cliente de navegador padrão do Supabase usa o modelo de header, então um app simples construído nele não está exposto a CSRF. No momento em que você move a sessão para cookies, para renderização no servidor ou para um backend próprio, o CSRF volta e SameSite=Lax mais checagem de origem viram obrigatórios. Lembre também das variantes sem cookie: uma ação logada disparada por GET (um link de "descadastrar" ou "excluir") é forjável a partir de uma tag de imagem, mais um motivo para GET nunca mudar estado. Decida o modelo, escreva, e teste: um formulário em outra origem fazendo POST na sua API deve falhar.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Token em header: sem CSRF, CSP obrigatória.</strong> Token em cookie: SameSite mais tokens ou checagem de origem.</li>
            <li><strong>Requisições que mudam estado nunca são GET.</strong></li>
            <li><strong>Cheque Origin ou Referer no servidor</strong> quando cookies são a credencial.</li>
            <li><strong>Teste de uma página estranha</strong> uma vez; espere a requisição recusada.</li>
          </ul>''',
details=['<strong>SameSite=Lax ainda envia cookies em navegação GET de nível superior;</strong> por isso GET precisa ser seguro.',
 '<strong>CORS não previne CSRF;</strong> a requisição é enviada, só a resposta é escondida.',
 '<strong>Login CSRF também existe:</strong> logar a vítima na conta do atacante.',
 '<strong>Double-submit cookie</strong> é o esquema de token mais simples para um app pequeno.',
 '<strong>Documente o modelo de sessão</strong> para a próxima pessoa aplicar a defesa certa.'],
sources=L(('PortSwigger, CSRF', 'https://portswigger.net/web-security/csrf'), ('OWASP, CSRF prevention cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html'), ('MDN, SameSite cookies', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Set-Cookie/SameSite'), ('web.dev, SameSite cookies explained', 'https://web.dev/articles/samesite-cookies-explained'))),

dict(id='keys-and-secrets', title='Keys and Secrets',
lede='A chave anon foi feita para ser pública e é inútil sem RLS. A chave service role ignora a RLS e nunca pode sair de um servidor. Variáveis de ambiente, .gitignore e varredura de segredos mantêm a segunda fora do bundle e do repositório.',
body='''<h3>Por quê</h3>
          <p>O Supabase dá a todo projeto dois tipos de chave. A publishable ou anon identifica o projeto e vai no navegador; seu único poder é chamar a API como usuário anônimo ou autenticado, que a RLS então restringe. A secret ou service role é a chave mestra: ignora toda política e lê e escreve qualquer coisa. Ela pertence a um ambiente de servidor, uma Edge Function ou um script confiável, nunca a código de frontend, nunca a uma variável Vite com prefixo VITE_, porque tudo com esse prefixo é compilado no bundle público. Uma chave service role num bundle JavaScript é igual a um banco público.</p>
          <p>Segredos chegam ao repositório por descuido: um .env commitado sem querer, uma chave colada num arquivo de configuração, um print na documentação. As defesas são rotina: .env no .gitignore desde o primeiro commit, um .env.example com placeholders, varredura de segredos do GitHub ligada, um scanner local como o gitleaks num hook de pre-commit, e rotação no momento em que uma chave é suspeita de ter vazado, porque o histórico do git lembra de tudo. O Cloudflare Pages guarda variáveis de produção no painel, separadas dos ambientes de preview, e é aí que a divisão dev/prod começa a importar.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Chave anon no cliente, service role nunca.</strong> Sem prefixo VITE_ em nada secreto.</li>
            <li><strong>.env ignorado, .env.example commitado,</strong> variáveis definidas no painel da hospedagem.</li>
            <li><strong>Varredura de segredos no repositório</strong> e um scanner de pre-commit local.</li>
            <li><strong>Rotacione na suspeita,</strong> não na prova. Chave vazada é vazada para sempre no histórico.</li>
          </ul>''',
details=['<strong>Procure "service_role" no bundle compilado</strong> antes de todo deploy. Leva dez segundos.',
 '<strong>Chaves diferentes por ambiente;</strong> chave de staging vazada não pode abrir produção.',
 '<strong>Rotação é treino:</strong> pratique antes de precisar.',
 '<strong>Prints do painel</strong> frequentemente contêm chaves. Recorte.',
 '<strong>A chave anon é pública por design;</strong> pare de tratá-la como segredo e passe a tratar a RLS como a fechadura.'],
sources=L(('Supabase, API keys', 'https://supabase.com/docs/guides/api/api-keys'), ('Vite, Env variables and modes', 'https://vite.dev/guide/env-and-mode'), ('GitHub, About secret scanning', 'https://docs.github.com/en/code-security/secret-scanning/introduction/about-secret-scanning'), ('OWASP, Secrets management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Secrets_Management_Cheat_Sheet.html'), ('gitleaks', 'https://github.com/gitleaks/gitleaks'))),

dict(id='storage-and-uploads', title='Storage, Uploads and Signed URLs',
lede='Imagens enviadas são arquivos, e arquivos têm permissões próprias. Buckets são públicos ou privados, políticas decidem quem envia e quem lê, URLs assinadas dão acesso temporário a arquivos privados, e limites de tamanho e tipo impedem uploads de virarem ataque.',
body='''<h3>Por quê</h3>
          <p>O Supabase Storage guarda arquivos em buckets com políticas no estilo RLS sobre a tabela de objetos. Um bucket público serve qualquer arquivo por URL, para sempre, a qualquer um; isso é certo para avatares e errado para imagens ligadas a um recurso privado. Um bucket privado serve arquivos só por requisições autenticadas ou URLs assinadas, links que expiram depois de um tempo definido. A maioria dos apps precisa dos dois: bucket público para fotos de perfil, bucket privado para conteúdo de usuário, com políticas que espelham a visibilidade do recurso pai, para que as imagens de um recurso privado não vazem por uma URL copiada uma vez. Convenções de caminho ajudam: user_id/resource_id/arquivo, com políticas que comparam a primeira pasta com auth.uid().</p>
          <p>Upload é entrada. Limite tamanho por arquivo e por bucket, restrinja tipos MIME às imagens que você de fato exibe, e nunca confie na extensão; o servidor decide o tipo de conteúdo. Renomeie arquivos no upload para os caminhos não serem controlados pelo usuário, o que fecha truques de path traversal e sobrescrita. Remova metadados EXIF se localização puder vazar. E considere o que acontece ao excluir: remover um item deve remover sua imagem, ou você segue pagando por, e potencialmente servindo, arquivos que deveriam ter sumido, o que a LGPD vai cobrar.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Bucket público para avatares, privado para conteúdo de usuário,</strong> políticas espelhando a visibilidade do recurso.</li>
            <li><strong>URLs assinadas com expiração curta</strong> para tudo que é privado; nunca link permanente.</li>
            <li><strong>Limites de tamanho e MIME no bucket,</strong> nomes gerados pelo servidor, sem caminhos de usuário.</li>
            <li><strong>Exclua arquivos junto com as linhas,</strong> e teste que uma imagem excluída para de ser servida.</li>
          </ul>''',
details=['<strong>URLs de bucket público são cacheáveis para sempre;</strong> mover o recurso para privado não as recolhe.',
 '<strong>Caminhos pasta-por-usuário</strong> deixam políticas de propriedade numa linha.',
 '<strong>Transformações de imagem no servidor</strong> também removem conteúdo perigoso.',
 '<strong>Uploads de SVG podem carregar scripts;</strong> trate como código, não como imagem.',
 '<strong>Teste os três usuários em arquivos também,</strong> não só em linhas.'],
sources=L(('Supabase, Storage access control', 'https://supabase.com/docs/guides/storage/security/access-control'), ('Supabase, File limits', 'https://supabase.com/docs/guides/storage/uploads/file-limits'), ('Supabase, Serving downloads and signed URLs', 'https://supabase.com/docs/guides/storage/serving/downloads'), ('OWASP, File upload cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/File_Upload_Cheat_Sheet.html'), ('PortSwigger, File upload vulnerabilities', 'https://portswigger.net/web-security/file-upload'))),

dict(id='security-headers-and-csp', title='Security Headers and CSP',
lede='Um punhado de headers de resposta diz ao navegador como proteger sua página: quais scripts podem rodar, se ela pode ser emoldurada, como referrers vazam, quais recursos são permitidos. A Content Security Policy é o mais pesado e o mais valioso, porque amortece XSS mesmo quando existe um buraco.',
body='''<h3>Por quê</h3>
          <p>O navegador faz muito por você se pedido. Content-Security-Policy lista de onde scripts, estilos, imagens e conexões podem vir; uma política estrita sem unsafe-inline faz uma tag script injetada simplesmente não rodar. Strict-Transport-Security fixa HTTPS. X-Content-Type-Options impede sniffing de MIME. X-Frame-Options ou frame-ancestors impede seu login de ser emoldurado numa página de clickjacking. Referrer-Policy impede URLs completas, que podem conter ids de recursos não listados, de vazarem para outros sites. Permissions-Policy desliga câmera, geolocalização e afins que você não usa. O Cloudflare Pages define tudo isso por um arquivo _headers na saída do build.</p>
          <p>CSP é o que dá trabalho, porque um app Vite com cliente Supabase, Google Fonts e um script de analytics tem fontes reais para declarar, e estilos inline de bibliotecas brigam com um style-src estrito. Comece em modo report-only, leia as violações, aperte, depois imponha. O connect-src precisa incluir sua URL do Supabase; img-src precisa incluir o domínio do storage; script-src deve ser sua origem mais hashes ou nonces, nada inline. Teste com o securityheaders.com e com o console aberto. A recompensa é que o pior caso da aula de XSS, um script numa nota, vira uma requisição bloqueada em vez de uma sessão roubada.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Arquivo _headers no Pages</strong> com HSTS, nosniff, frame-ancestors, Referrer-Policy, Permissions-Policy.</li>
            <li><strong>CSP em report-only primeiro,</strong> depois imposta, sem unsafe-inline para scripts.</li>
            <li><strong>Declare só o que usa:</strong> sua origem, Supabase, fontes.</li>
            <li><strong>Reconfira os headers depois de toda mudança de infra</strong> com um scanner externo.</li>
          </ul>''',
details=['<strong>Referrer-Policy: strict-origin-when-cross-origin</strong> mantém ids não listados fora dos logs de outros sites.',
 '<strong>frame-ancestors \'none\'</strong> a menos que você embuta de propósito.',
 '<strong>Nonces ou hashes</strong> para o único script inline que não dá para evitar.',
 '<strong>Report-only não é proteção;</strong> marque uma data para impor.',
 '<strong>Headers são por resposta;</strong> cheque a API e o domínio do storage também, não só a página.'],
sources=L(('MDN, Content Security Policy', 'https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP'), ('web.dev, Strict CSP', 'https://web.dev/articles/strict-csp'), ('OWASP, HTTP headers cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/HTTP_Headers_Cheat_Sheet.html'), ('Cloudflare Pages, Headers', 'https://developers.cloudflare.com/pages/configuration/headers/'), ('securityheaders.com', 'https://securityheaders.com/'))),

dict(id='dependencies-and-supply-chain', title='Dependencies and the Supply Chain',
lede='Seu app é majoritariamente código dos outros. Um pacote vulnerável entrega sua vulnerabilidade; um pacote sequestrado entrega o malware de alguém. Lockfiles, auditorias, atualizações automáticas e o hábito de ler o que instala são os controles.',
body='''<h3>Por quê</h3>
          <p>Um projeto Vite com React puxa centenas de pacotes, cada um um buraco em potencial e cada um um caminho possível para uma atualização maliciosa. O OWASP lista componentes vulneráveis e desatualizados no Top 10; os incidentes de supply chain dos últimos anos acrescentaram typosquatting e sequestro de contas de mantenedores à lista. A base é mecânica: commite o lockfile para instalações serem reproduzíveis, rode npm audit no CI e leia o resultado, ligue o Dependabot ou equivalente para atualizações chegarem como pull requests revisáveis, e fixe versões maiores de tudo que toca autenticação ou renderização. A parte de julgamento é ler: antes de adicionar um pacote, veja manutenção, downloads, árvore de dependências e se você precisa mesmo dele.</p>
          <p>Código de frontend roda no navegador do usuário com a sessão do usuário, então uma biblioteca de UI comprometida é tão perigosa quanto um backend comprometido. Mantenha a lista de dependências curta, prefira recursos da plataforma a pacotes para necessidades pequenas, e evite pacotes que puxam dezenas de outros por uma função. Atualizações agendadas e chatas vencem as heroicas: uma janela mensal em que tudo avança um pouco é mais segura que um salto anual que quebra o build. Quando sair uma vulnerabilidade em algo que você usa, saiba em um dia, não num trimestre.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Lockfile commitado, npm audit no CI,</strong> falhas triadas na mesma semana.</li>
            <li><strong>PRs automáticos de atualização</strong> com cadência regular de merge.</li>
            <li><strong>Leia antes de instalar:</strong> mantenedores, atividade, tamanho, dependências transitivas.</li>
            <li><strong>Menos pacotes:</strong> cada dependência é uma decisão permanente de confiar num estranho.</li>
          </ul>''',
details=['<strong>npm audit fix --force</strong> pode quebrar coisas; leia o diff.',
 '<strong>Dependências de dev rodam na sua máquina;</strong> scripts postinstall também são vetor.',
 '<strong>Fixe pelo lockfile, não por versões exatas no package.json,</strong> para patches continuarem fluindo.',
 '<strong>Assine os avisos</strong> dos cinco pacotes que mais importam.',
 '<strong>Remova o que parou de usar;</strong> pacote sem uso ainda é instalado e ainda é hackeado.'],
sources=L(('OWASP Top 10, A06 Vulnerable and Outdated Components', 'https://owasp.org/Top10/A06_2021-Vulnerable_and_Outdated_Components/'), ('npm, npm audit', 'https://docs.npmjs.com/cli/v10/commands/npm-audit'), ('GitHub, Dependabot', 'https://docs.github.com/en/code-security/dependabot'), ('OWASP, Vulnerable dependency management cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Vulnerable_Dependency_Management_Cheat_Sheet.html'))),

dict(id='logs-backups-environments', title='Logs, Backups and Environments',
lede='Não se defende o que não se vê nem se restaura. Logs dizem que algo aconteceu, alertas dizem agora, backups deixam desfazer, e um teste de restauração prova que o backup é real. Ambientes separados mantêm experimentos longe dos dados de pessoas reais.',
body='''<h3>Por quê</h3>
          <p>Falhas de log e monitoramento são uma categoria própria do OWASP porque violações passam meses sem serem notadas. Para um app pequeno a régua é modesta e ainda assim real: o Supabase guarda logs de auth, API e banco; leia quando algo estiver estranho, e configure alertas para os eventos que importam, rajadas de login falho, erros disparando, volumes incomuns de leitura. Registre o que aconteceu e quem fez, nunca o que a pessoa digitou num campo de senha nem o token que carregava. Logs também são dado pessoal sob a LGPD, então ganham prazo de retenção como tudo mais.</p>
          <p>Backups são a diferença entre um incidente e uma catástrofe. O Supabase faz backups diários nos planos pagos, com recuperação pontual disponível; o plano gratuito não, e isso é motivo para decidir cedo o que perder tudo significaria. Um backup que ninguém restaurou é esperança, não controle; agende uma restauração num projeto descartável e cronometre. Ambientes completam o quadro: desenvolva contra um projeto separado com dados fictícios, use deploys de preview para revisão, e mantenha chaves de produção só em produção. O branching do Supabase e os previews do Cloudflare tornam a divisão barata; a disciplina é nunca apontar um build de dev para o banco de produção "só um minuto".</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Leia os logs semanalmente,</strong> alerte para rajadas de login falho e picos de erro.</li>
            <li><strong>Backups ligados, restauração testada</strong> ao menos uma vez antes do lançamento e depois de mudanças grandes.</li>
            <li><strong>Projetos separados para dev e prod,</strong> dados fictícios em dev, previews para revisão.</li>
            <li><strong>Logs têm retenção,</strong> e nunca contêm senhas ou tokens.</li>
          </ul>''',
details=['<strong>Cronometre o treino de restauração</strong> e anote quanto tempo levou.',
 '<strong>Fadiga de alerta é modo de falha;</strong> três alertas que importam vencem trinta.',
 '<strong>Limpe headers Authorization e e-mails</strong> de qualquer coisa que mande a um logger de terceiros.',
 '<strong>Quem tem acesso a produção?</strong> Escreva a lista; mantenha curta.',
 '<strong>Migrações rodam em dev primeiro,</strong> depois preview, depois prod, com plano de rollback.'],
sources=L(('OWASP Top 10, A09 Security Logging and Monitoring Failures', 'https://owasp.org/Top10/A09_2021-Security_Logging_and_Monitoring_Failures/'), ('OWASP, Logging cheat sheet', 'https://cheatsheetseries.owasp.org/cheatsheets/Logging_Cheat_Sheet.html'), ('Supabase, Backups', 'https://supabase.com/docs/guides/platform/backups'), ('Supabase, Branching', 'https://supabase.com/docs/guides/deployment/branching'), ('Supabase, Going into production', 'https://supabase.com/docs/guides/deployment/going-into-prod'), ('The Twelve-Factor App, Config', 'https://12factor.net/config'))),

dict(id='personal-data-under-lgpd', title='Personal Data Under the LGPD',
lede='A Lei Geral de Proteção de Dados se aplica no momento em que você guarda um nome ou um e-mail. Ela define dado pessoal e dado sensível, nomeia os papéis de controlador e operador, e fixa princípios que se leem como requisitos de produto: finalidade, necessidade, transparência, segurança.',
body='''<h3>Por quê</h3>
          <p>Dado pessoal é qualquer coisa que identifica ou pode identificar uma pessoa natural: nome, e-mail, handle, foto, endereço IP, id de dispositivo, e a combinação de campos inofensivos que juntos apontam para alguém. Dado sensível é um conjunto mais estreito com regras mais duras: saúde, orientação sexual, religião, etnia, política, biometria, genética. Um app de aparência inofensiva guarda texto livre que pode revelar uma gravidez, uma religião ou uma condição médica; desenhe os campos para não coletar o que não precisa, e trate texto livre como potencialmente sensível. A pessoa dona do dado detém os direitos; você, que decide por que e como ele é tratado, é o controlador; Supabase e Cloudflare, tratando sob suas instruções, são operadores.</p>
          <p>Os princípios do artigo 6 são o briefing de design. Finalidade: colete por um motivo específico e declarado. Adequação e necessidade: só o que esse motivo precisa. Transparência: diga às pessoas, em linguagem clara, o que você faz. Segurança: medidas proporcionais ao risco. Prevenção, não discriminação, responsabilização. O inventário é o primeiro passo prático: uma tabela com todo campo que você guarda, com finalidade, base legal que pretende usar, quem acessa, qual fornecedor o mantém e por quanto tempo. Essa tabela alimenta a política de privacidade, o fluxo de exclusão e o plano de incidentes, e é o que a ANPD, a autoridade nacional, pediria para ver.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Inventarie todo campo</strong> com finalidade, base legal, acesso, fornecedor e retenção.</li>
            <li><strong>Colete menos:</strong> se a finalidade não precisa da data de nascimento, não peça.</li>
            <li><strong>Nomeie os papéis:</strong> você é o controlador; liste seus operadores.</li>
            <li><strong>Trate texto livre como capaz de ser sensível</strong> e mantenha privado por padrão.</li>
          </ul>''',
details=['<strong>Endereços IP e ids de dispositivo são dado pessoal.</strong> Logs contam.',
 '<strong>Pseudonimizado ainda é pessoal;</strong> só anonimização de verdade sai da lei.',
 '<strong>Dados de crianças</strong> exigem consentimento específico dos pais e o melhor interesse da criança.',
 '<strong>O inventário é documento vivo;</strong> atualize a cada campo novo.',
 '<strong>Isto é educação, não assessoria jurídica;</strong> uma pessoa advogada revisa antes do lançamento.'],
sources=L(('Lei nº 13.709/2018 (LGPD), texto integral', 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm'), ('ANPD, Autoridade Nacional de Proteção de Dados', 'https://www.gov.br/anpd/pt-br'), ('ANPD, materiais educativos e publicações', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'), ('Serpro, LGPD explicada', 'https://www.serpro.gov.br/lgpd'))),

dict(id='legal-bases-and-rights', title='Legal Bases and the Rights of Data Subjects',
lede='Consentimento é uma de dez bases legais, e em geral não a melhor. Operar a conta que a pessoa pediu é execução de contrato; prevenir fraude é legítimo interesse. Seja qual for a base, a pessoa mantém direitos: acesso, correção, portabilidade, exclusão, e resposta em prazo razoável.',
body='''<h3>Por quê</h3>
          <p>A LGPD lista as bases legais no artigo 7: consentimento, obrigação legal, políticas públicas, pesquisa, execução de contrato, exercício de direitos, proteção da vida, tutela da saúde, legítimo interesse, proteção ao crédito. Um produto que pede consentimento para tudo ganha dois problemas: consentimento pode ser revogado a qualquer momento, o que significaria excluir a conta que a pessoa ainda quer, e um termo longo que ninguém lê não é o consentimento livre, informado e inequívoco que a lei exige. Para um app típico, guardar o e-mail e o conteúdo da própria pessoa é execução do contrato que a pessoa aceitou ao se cadastrar; logs de segurança são legítimo interesse; uma newsletter de marketing é consentimento, separado, opt-in, revogável com um clique.</p>
          <p>Direitos são a outra metade. A pessoa pode confirmar se você trata seus dados, acessá-los, corrigi-los, anonimizar ou excluir o desnecessário, recebê-los em formato portável, saber com quem você compartilhou, e revogar consentimento. Cada direito precisa de um caminho no produto ou de um processo manual documentado, e de resposta nos prazos da lei. Construa os óbvios: uma exportação dos dados da pessoa em JSON, exclusão de conta que exclui de verdade, uma página de perfil onde os campos são editáveis, e um canal de contato que responde. Registre pedidos e respostas; responsabilização é princípio, e o registro é sua prova.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Escolha a base por finalidade:</strong> contrato para o serviço, legítimo interesse para segurança, consentimento só para extras.</li>
            <li><strong>Consentimento é granular, opt-in e revogável</strong> onde você o usar.</li>
            <li><strong>Entregue exportação e exclusão</strong> como funcionalidades, não como tickets de suporte.</li>
            <li><strong>Registre pedidos e respostas</strong> com datas.</li>
          </ul>''',
details=['<strong>Caixas pré-marcadas não são consentimento.</strong>',
 '<strong>Legítimo interesse exige um teste de ponderação escrito</strong> que você possa mostrar.',
 '<strong>Exclusão tem exceções:</strong> obrigações legais podem exigir guardar alguns registros; diga quais.',
 '<strong>Portabilidade é exportação legível por máquina,</strong> JSON serve.',
 '<strong>Designe um encarregado</strong> mesmo que seja você, e publique o contato.'],
sources=L(('Lei nº 13.709/2018 (LGPD), artigos 7, 11 e 18', 'https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm'), ('ANPD, materiais educativos e publicações', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes'), ('ICO, Guide to the data protection principles (paralelo com o GDPR)', 'https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/'))),

dict(id='privacy-by-design-in-product', title='Privacy by Design in the Product',
lede='Privacy by design significa que a escolha segura é o padrão e a escolha privada é real no backend, não um botão que esconde outro. Controles de visibilidade, exclusão, retenção, cookies e a política de privacidade são funcionalidades de produto, construídas com o mesmo cuidado da funcionalidade principal.',
body='''<h3>Por quê</h3>
          <p>A LGPD pede privacidade desde a concepção e por padrão. Na prática isso significa: recursos novos privados, campos de perfil mínimos, analytics desligado até a pessoa concordar, e todo "privado" na interface sustentado por uma política no banco e no storage. A política de privacidade e os termos de uso são documentos diferentes com trabalhos diferentes: a política explica quais dados, por quê, em qual base, com quem, por quanto tempo e como exercer direitos; os termos fixam as regras do serviço. Os dois são lidos por poucos e importam a todos; escreva em linguagem simples e mantenha exatos, porque uma política que promete o que o sistema não faz é por si uma violação.</p>
          <p>Cookies ganham parágrafo próprio porque o folclore está errado. Cookies estritamente necessários, a sessão e a preferência que você precisa para rodar o serviço, não exigem banner de consentimento. Analytics e marketing exigem uma escolha real, desligada por padrão, com a mesma facilidade para recusar e para aceitar; a ANPD publicou orientação exatamente sobre isso. Retenção fecha o ciclo: decida por quanto tempo guarda uma conta inativa, dados de lista excluída, logs e backups, e automatize a exclusão. Excluir conta precisa cascatear por linhas, arquivos e, dentro da janela de backup, backups também, e a pessoa deve receber confirmação. Por fim, um contato de privacidade que responde, e um histórico datado de mudanças na política.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Privado por padrão,</strong> todo controle de visibilidade imposto no banco e no storage.</li>
            <li><strong>Política de privacidade e termos como páginas separadas, em linguagem simples,</strong> fiéis ao que o código faz.</li>
            <li><strong>Escolha de cookies só para analytics e marketing,</strong> desligados por padrão, recusar tão fácil quanto aceitar.</li>
            <li><strong>Cronograma de retenção automatizado,</strong> exclusão cascateando por linhas, arquivos e backups.</li>
          </ul>''',
details=['<strong>Excluir é excluir:</strong> linhas, objetos no storage, índices de busca, e a janela de backup declarada.',
 '<strong>Sem banner para cookies necessários;</strong> o que bloqueia a página para tudo é o anti-padrão.',
 '<strong>O diálogo de compartilhar é um momento de privacidade:</strong> repita o que ficará visível.',
 '<strong>Versione a política</strong> com datas, e avise em mudanças relevantes.',
 '<strong>Perfil mínimo:</strong> handle e nome de exibição; o resto opcional.'],
sources=L(('ANPD, guia orientativo sobre cookies e proteção de dados pessoais', 'https://www.gov.br/anpd/pt-br/documentos-e-publicacoes/guia-orientativo-cookies-e-protecao-de-dados-pessoais.pdf'), ('ANPD, guia de segurança para agentes de tratamento de pequeno porte', 'https://www.gov.br/anpd/pt-br/centrais-de-conteudo/materiais-educativos-e-publicacoes/guia-orientativo-sobre-seguranca-da-informacao-para-agentes-de-tratamento-de-pequeno-porte'), ('IF, Data patterns catalogue', 'https://catalogue.projectsbyif.com/'), ('ICO, advice for small organisations', 'https://ico.org.uk/for-organisations/advice-for-small-organisations/'))),

dict(id='vendors-incidents-and-launch', title='Vendors, Incidents and the Pre-Launch Review',
lede='Supabase, Cloudflare e GitHub tratam os dados dos seus usuários em seu nome, muitas vezes fora do Brasil. Conheça os termos, saiba onde os dados moram, e tenha um plano para o dia em que algo der errado. Depois rode a revisão de pré-lançamento: três usuários, toda operação, todo arquivo, todo header, com evidência.',
body='''<h3>Por quê</h3>
          <p>Operadores fazem parte da sua responsabilidade. Leia os termos de tratamento de dados de cada fornecedor, anote as regiões onde os dados ficam, e registre no inventário; a LGPD regula transferências internacionais e a ANPD tem regras para elas, então um banco numa região fora do Brasil é decisão a documentar, não acidente. Suboperadores mudam: assine os avisos dos fornecedores. Incidentes vão acontecer: uma chave vazada, um erro de política que expôs recursos privados, uma conta comprometida. A LGPD exige comunicar incidentes relevantes à ANPD e às pessoas afetadas; o plano prático tem quatro passos, detectar, conter, avaliar, comunicar, com contatos, modelos e critérios de decisão escritos antes de precisar.</p>
          <p>A revisão de pré-lançamento é onde esta seção inteira vira evidência. Percorra a matriz de permissões com visitante, dono e outro usuário, pela API, para toda operação, e registre resultados. Busque imagens privadas por URL como o usuário errado. Revise os fluxos de auth, regras de senha, e-mails e todo redirecionamento. Cheque headers, CSP, HTTPS, limites de upload e tratamento de URLs externas. Confirme que segredos estão fora do repositório e do bundle, dependências atualizadas, backups restauram, alertas disparam. Releia inventário, política, cronograma de retenção e fluxo de exclusão contra o que o código de fato faz. Liste os riscos residuais que aceita e os itens que adia, com responsável e data. Lance com esse documento, não com uma sensação.</p>

          <h3>Como aplicar</h3>
          <ul>
            <li><strong>Tabela de fornecedores:</strong> o que cada um trata, onde, sob quais termos, com link para o feed de avisos.</li>
            <li><strong>Plano de incidentes numa página:</strong> detectar, conter, avaliar, comunicar, com contatos e modelos.</li>
            <li><strong>Revisão de pré-lançamento com evidência:</strong> toda célula da matriz testada, todo check com print ou log anexado.</li>
            <li><strong>Registro de riscos residuais</strong> assinado antes de usuários reais chegarem.</li>
          </ul>''',
details=['<strong>"Configurado" não é "testado".</strong> A revisão testa.',
 '<strong>Pratique o plano de incidentes</strong> com um exercício de mesa de chave vazada.',
 '<strong>Reteste depois de toda mudança de esquema ou política,</strong> automatizado onde der.',
 '<strong>Prioridade se o tempo for curto:</strong> RLS e testes entre usuários, depois auth, depois storage e segredos, depois OWASP, depois documentos da LGPD.',
 '<strong>Esta trilha é educação;</strong> não é certificação nem conformidade jurídica. Peça revisão antes do lançamento.'],
sources=L(('ANPD, incidentes de segurança', 'https://www.gov.br/anpd/pt-br/assuntos/incidente-de-seguranca'), ('ANPD, transferência internacional de dados', 'https://www.gov.br/anpd/pt-br/assuntos/transferencia-internacional-de-dados'), ('OWASP, Web Security Testing Guide', 'https://owasp.org/www-project-web-security-testing-guide/'), ('OWASP, Application Security Verification Standard', 'https://owasp.org/www-project-application-security-verification-standard/'), ('Supabase, Going into production', 'https://supabase.com/docs/guides/deployment/going-into-prod'), ('Cloudflare Pages', 'https://developers.cloudflare.com/pages/'))),
]
