# CONECTAR AO SUPABASE  |  CONECT TO SUPABASE 
# BUSCAR OS CONTATOS    |  FETCH CONTACTS
#  PEGAR ATÉ 3 CONTATOS |  GET UP TO 3 CONTACTS
# MONTAR A MENSAGEM     |  BUILD THE MESSAGE
# ENVIAR PELO WHATSAPP USANDO A Z-API |  SEND VIA WHATSAPP USING Z-API
# MOSTRAR NO TERMINAL OQUE ACONTECEU |  SHOW IN TERMINAL WHAT HAPPENED
import os
import logging as log
import requests as rq
from dotenv import load_dotenv
from supabase import create_client, Client
load_dotenv()

log.basicConfig(
    level=log.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = log.getLogger(__name__)

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

ZAPI_INSTANCE_ID: str = os.environ["ZAPI_INSTANCE_ID"]
ZAPI_TOKEN: str = os.environ["ZAPI_TOKEN"]
ZAPI_CLIENT_TOKEN: str = os.environ["ZAPI_CLIENT_TOKEN"]

MAX_CONTACTS = 3

# SUPABASE
def fetch_contacts(client: Client) -> list[dict]:
    """puxa os contatos da tabela 'contacts' do Supabase. | Fetches contacts from the 'contacts' table in Supabase."""
    logger.info("Buscando contatos no Supabase...")

    response = (
        client.table("contacts")
        .select("name, phone")
        .limit(MAX_CONTACTS)
        .execute()
    )

    contacts = response.data
    logger.info(f"{len(contacts)} contato(s) encontrado(s).")
    return contacts


# API DO WHATS

def send_whatsapp_message(name: str, phone: str) -> bool:
    """Envia uma mensagem personalizada via Z-API. Retorna True se der sucesso. | Sends a personalized WhatsApp message via Z-API. Returns True on success."""
    url = f"https://api.z-api.io/instances/{ZAPI_INSTANCE_ID}/token/{ZAPI_TOKEN}/send-text"

    message = f"Olá, {name} tudo bem com você?"

    payload = {
        "phone": phone,
        "message": message,
    }

    headers = {
        "Content-Type": "application/json",
        "Client-Token": ZAPI_CLIENT_TOKEN,
    }

    try:
        response = rq.post(url, json=payload, headers=headers, timeout=10)
        response.raise_for_status()
        logger.info(f"Mensagem enviada para {name} ({phone}).")
        return True

    except rq.exceptions.HTTPError as e:
        logger.error(f"Erro HTTP ao enviar para {name} ({phone}): {e.response.status_code} - {e.response.text}")
    except rq.exceptions.ConnectionError:
        logger.error(f"Erro de conexão ao enviar para {name} ({phone}). Verifique suas credenciais da Z-API.")
    except rq.exceptions.Timeout:
        logger.error(f"Tempo de espera esgotado ao enviar para {name} ({phone}).")
    except rq.exceptions.RequestException as e:
        logger.error(f"Erro inesperado ao enviar para {name} ({phone}): {e}")

    return False

# Funcão principal | Main function
def main() -> None:
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

    contacts = fetch_contacts(supabase)

    if not contacts:
        logger.warning("Nenhum contato encontrado. Encerrando.")
        return

    success_count = 0

    for contact in contacts:
        name: str = contact.get("name", "").strip()
        phone: str = contact.get("phone", "").strip()

        if not name or not phone:
            logger.warning(f"Pulando contato incompleto: {contact}")
            continue

        sent = send_whatsapp_message(name, phone)
        if sent:
            success_count += 1

    logger.info(f"Concluído. {success_count}/{len(contacts)} mensagem(ns) enviada(s) com sucesso.")


if __name__ == "__main__":
    main()