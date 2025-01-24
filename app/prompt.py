import json
import os
from enum import Enum
from typing import List, Optional

import cohere
import pydantic

os.environ["COHERE_API_KEY"] = "<YOUR-"API"-KEY>"


class Tags(str, Enum):
    bug_fix = "bug_fix"
    updates = "updates"
    security_fix = "security_fix"
    new_feature = "new_feature"

    def description(self):
        descriptions = {
            "bug_fix": "Correções de bugs",
            "updates": "Atualizações na nova versão",
            "security_fix": "Correções de segurança",
            "new_feature": "Novas funcionalidades",
        }
        return descriptions.get(self.value, "Descrição não disponível")


class News(pydantic.BaseModel):
    description: str = pydantic.Field(
        ..., description="The description of the news."
    )
    tag: Tags = pydantic.Field(..., description="The tag of the news.")


class Resume(pydantic.BaseModel):
    """
    Resume class represents a summary of a library with its name, bug fixes, updates, security fixes, and new features.

    """

    library_name: str = pydantic.Field(
        ..., description="The name of the library."
    )

    news: List[News] = pydantic.Field(
        ..., description="List of news of the library."
    )


class Smart:
    def __init__(self):
        self.llm = cohere.ClientV2(api_key=os.environ["COHERE_API_KEY"])

    def answer(self, path, lib, html):
        if path == "releases_url":
            return self.find_release(lib["library_name"], html)
        elif path == "releases_doc_url":
            return self.create_resume(lib, html)

    def query(self, prompt):
        return self.llm.chat(
            model="command-r-plus-08-2024",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

    def find_release(self, lib, html):
        prompt = f"""
        Com base no seguinte documento Markdown:

        ```markdown
        {html}
        ```

        Extraia a versão mais recente e a data de lançamento da biblioteca {lib}.

        Formate a resposta como um objeto JSON com as seguintes chaves:
        * `version`: (string) A versão mais recente. Use `null` se não encontrada.
        * `release_date`: (string no formato AAAA-MM-DD) A data de lançamento. Use `null` se não encontrada.
        Responda somente com o formato JSON.

        Exemplo de formato JSON:

        ```json
        {{
        "version": "1.2.3",
        "release_date": "2024-10-26"
        }}
        ```

        Se a informação não estiver disponível no documento, retorne:

        ```json
        {{
        "version": null,
        "release_date": null
        }}
        ```
        """
        return self.reply(prompt)

    def create_resume(self, lib, html):
        prompt = f"""
        Com base no documento Markdown:

        ```markdown
        {html}
        ```
        Faça:
            - Resumo das novidades da biblioteca {lib["library_name"]} na versão {lib["version"]} separados por categoria de acordo com o schema fornecido.
            - Caso alguma novidade for repetida na mesma categoria, liste apenas uma vez.
            - Não é necessário preencher todas as categorias, apenas as que possuem informações.
            - Se a informação não estiver disponível, retorne None para todos os campos, exceto para `library_name`.

        Não seja criativo, responda somente com que for encontrado no documento.
        Não seja criativo na formatação, responda exatamente como o schema fornecido.
        Verifique se sua resposta está no formato JSON para que seja possível usar o comando json.loads do python, Caso não esteja, formate-a corretamente.

        response_format:
        {json.dumps(Resume.model_json_schema())}
        """
        return self.reply(prompt)

    def reply(self, prompt):

        response = self.query(prompt)
        response = response.message.content[0].text
        response = response.replace("```json", "")
        response = response.replace("```", "")
        response = response.replace("\n", "")
        _response = {}
        one_time = True
        while len(response) > 10:
            try:
                _response = json.loads(response)
                break
            except json.JSONDecodeError:
                if one_time:
                    print("### COHERE retornou JSON em formato errado")
                    print(response)
                    print("### Tentando formatar ###")
                    one_time = False
                response = response[:-1]
        return _response
