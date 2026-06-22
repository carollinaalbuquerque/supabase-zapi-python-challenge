B2BFLOW Challenge

Aplicação em Python que busca contatos armazenados no Supabase e envia mensagens personalizadas via Z-API.

Estrutura da Tabela

Tabela: "contacts"

Campo| Tipo
id| integer
name| text
phone| text

Exemplo

id| name| phone
1| João| 5511999999999
2| Maria| 5511888888888
3| Pedro| 5511777777777

Variáveis de Ambiente

Crie um arquivo ".env" na raiz do projeto:

SUPABASE_URL=
SUPABASE_KEY=

ZAPI_INSTANCE_ID=
ZAPI_TOKEN=

Instalação

pip install -r requirements.txt

Execução

python main.py

Fluxo

1. Busca os contatos no Supabase.
2. Seleciona até 3 contatos.
3. Personaliza a mensagem no formato:

Olá, <nome_contato> tudo bem com você?

4. Envia a mensagem via Z-API.
5. Exibe o resultado da operação no terminal.