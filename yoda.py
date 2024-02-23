import requests
from decouple import config


url = "https://api.edenai.run/v2/aiproducts/askyoda/"


headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "authorization": config("EDENAI_KEY"),
}


def create_project(project_name, db_provider, collection_name):
    payload = {
        "db_provider": db_provider,
        "embeddings_provider": "cohere",
        "project_name": project_name,
        "collection_name": collection_name,
    }

    response = requests.post(url, json=payload, headers=headers)


def custom_classification(text):
    url = "https://api.edenai.run/v2/text/custom_classification"
    payload = {
        "providers": "openai",
        "labels": ["politness", "question"],
        "texts": [text],
        "examples": [
            ["What is the cost of this request ?", "question"],
            ["Have a nice day", "politness"],
            ["Thanks for the support ", "politness"],
            ["What is text to speech ?", "question"],
        ],
        "fallback_providers": "",
    }

    response = requests.post(url, json=payload, headers=headers)
    print(response.text)
    if response.ok:
        return response.json()["openai"]["classifications"][0]


class Askyoda:
    def __init__(self, id) -> None:
        self.id = id
        self.url = url + id
        self.history = []

    def add_urls(self, urls) -> None:
        """Add a list of URLs to the current Askyoda Project"""
        try:
            payload = {"urls": urls}
            response = requests.post(
                self.url + "/add_url", json=payload, headers=headers
            )
            if response.ok:
                return f"Added  {len(urls)} URLs to the project" # type: ignore
        except Exception as e:
            return e  # type: ignore

    def get_collection_info(self):
        """Get information about the Collection in use for this project."""
        try:
            response = requests.get(self.url + "/get_collection_info", headers=headers)
            if response.ok:
                return "All chunks {}".format(response.text)
        except Exception as e:
            return f"Error : {e}"

    def create_bot_profile(self, language, compagny, name, job_title, personality):
        try:
            payload = {
                "personality": personality,
                "company_name": compagny,
                "name": name,
                "job_title": job_title,
                "language": language,
            }
            response = requests.post(
                self.url + "/create_bot_profile", json=payload, headers=headers
            )
            if response.status_code == 201:
                return "Bot profile created successfully with name {}".format(name)
        except Exception as e:
            return f"Error : {e}"

    def ask_llm(self, question):
        try:
            print(question)
            """Ask Language Learning Model (LLM). Returns an answer from LLM"""
            payload = {
                "query": question
                ,
                "llm_provider": "mistral",
                "llm_model": "small",
                "k": 5,
            }
            response = requests.post(
                self.url + "/ask_llm", json=payload, headers=headers
            )
            print(f"Response from LLM:\n{response}")
            if response.status_code == 200:
                print(response.json())
                print("I don't know" in response.text)
                if "I don't know" == response.json()["result"]:
                    result = custom_classification(question)
                    print(
                        result
                    )
                    if result:# Call to a function that classifies the input text into different categories
                        if result["label"] == "politeness":
                            return "Thanks"
                        else:
                            return True
                    raise Exception
                else:

                    return response.json()["result"]
            else:
                return response.text
        except Exception as e:
            return e

    def add_data(self, data):
        try:
            files = {
                "file": (
                    f"))%20{data}",
                    open(
                        f"))%20{data}",
                        "rb",
                    ),
                    "application/pdf",
                )
            }
            payload = {"provider": "amazon"}

            response = requests.post(self.url + "/add_file", data=payload, files=files)
        except Exception as e:
            return e

    def add_texts(self, text):
        try:
            payload = {"texts": [text]}
            response = requests.post(
                self.url + "/add_text", json=payload, headers=headers
            )

            if response.ok:

                return response.text
            else:
                return "De la merde"
        except Exception as e:
            return str(e)
