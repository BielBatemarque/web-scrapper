import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import csv

class WebScrapper:

    def __init__(self) -> None:
        self.crome_options: Options = Options()

    def configura_busca(self):
        self.crome_options.add_argument('--no-sandbox') 
        self.crome_options.add_argument('--disable-dev-shm-usage')

        return uc.Chrome(options=self.crome_options)
    
    def retorna_csv_listagem(self, lista_produtos: list):
        nome_arquivo = 'produtos.csv'
        
        with open(nome_arquivo, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["nome", "avaliacao", "preco"])
            
            writer.writeheader()
            
            for produto in lista_produtos:
                writer.writerow(produto)

    def buscar_produtos(self, nome_produto: str):
        driver = self.configura_busca()
        driver.get(f"https://www.americanas.com.br/busca/{nome_produto}")

        element_busca = driver.find_elements(By.CLASS_NAME, "src__Wrapper-sc-1l8mow4-0")

        produtos = []
        for produto in element_busca:
            produtos.append({
                "nome": produto.find_element(By.TAG_NAME, "h3").text,
                "avaliacao": produto.find_elements(By.TAG_NAME, "span")[0].text,
                "preco": produto.find_elements(By.TAG_NAME, "span")[1].text,
            })

        driver.close()

        return produtos


if __name__ == "__main__":
    scrapper = WebScrapper()
    produto = input("Qual produto deseja buscar: ")

    produtos = scrapper.buscar_produtos(produto)

    scrapper.retorna_csv_listagem(lista_produtos=produtos)

    print("Sucesso - Listagem gerada.")