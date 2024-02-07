import os
import requests
import logging


client_id = os.environ.get('AZURE_CLIENT_ID')
tenant_id = os.environ.get('AZURE_TENANT_ID')
client_secret = os.environ.get('AZURE_CLIENT_SECRET')
pipeline = os.environ.get('POWERBI_PIPELINE_ID')
sourceStageOrder = os.environ.get('POWERBI_SOURCE_STAGE_ORDER')
note_deploy = os.environ.get('POWERBI_NOTE')


# Configuração de Logging
def get_access_token(client_id, client_secret, tenant_id):
    """Obtém o token de acesso para autenticação na API do Power BI."""
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    payload = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': 'https://analysis.windows.net/powerbi/api/.default'
    }
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    response = requests.post(url, headers=headers, data=payload)

    if response.status_code == 200:
        return response.json().get('access_token')
    else:
        logging.error(f"Erro ao obter o token de acesso: {response.text}")
        return None

def deploy_all_in_power_bi_pipeline(access_token, pipeline_id, source_stage_order, note, options):
    """Implanta todos os itens do Power BI de um estágio do pipeline para outro."""
    url = f"https://api.powerbi.com/v1.0/myorg/pipelines/{pipeline_id}/deployAll"
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json'
    }
    payload = {
        "sourceStageOrder": source_stage_order,
        "options": options,
        "note": note
    }
    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 202:
        logging.info("Deploy iniciado com sucesso no Power BI Pipeline.")
    else:
        logging.error(f"Erro ao iniciar o deploy: {response.text}")

def main():
    # Substitua com suas credenciais reais

    # Obter o token de acesso
    access_token = get_access_token(client_id, client_secret, tenant_id)
    if access_token is None:
        return

    # Dados do Pipeline
    pipeline_id = pipeline
    source_stage_order = sourceStageOrder  # Exemplo: 0 para Desenvolvimento
    note = note_deploy
    options = {
        "allowOverwriteArtifact": True,
        "allowCreateArtifact": True
    }

    # Iniciar o Deploy
    deploy_all_in_power_bi_pipeline(access_token, pipeline_id, source_stage_order, note, options)

if __name__ == "__main__":
    main()