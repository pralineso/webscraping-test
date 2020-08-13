import pandas as pd
import requests as r
from bs4 import BeautifulSoup


def has_data_index(tag):
    return tag.has_attr('data-index')


if __name__ == '__main__':

    products = []
    prices = []

    url = 'https://www.amazon.com.br/s?k={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss/'
    word = 'iphone'
    count = 1  # count que vai ate 24 que é quantidade de item por pagina

    response = r.get(url.format(word))

    print('Acessando o site \n')

    soup = BeautifulSoup(response.text, "html.parser")
    search_results = soup.find_all(has_data_index)

    #parte para funcao expecifica


    print('Buscando... \n')
    for result in search_results:
        product_name = result.find('h2', class_='a-size-mini a-spacing-none a-color-base s-line-clamp-4')
        product_price = result.find('span', class_='a-offscreen')

        if (count <= 24):

            if product_name:
                product = product_name.text.strip()
                products.append(product)
                #print(product)

            if product_price:
                price = product_price.text
                prices.append(price)
            else:
                #ai pega o preco menor
                prices.append('Sem preço')

        count = count + 1

    print('Busca finalizada! \n')

    print('Gerando Tabela... \n')
    produtos = {'Nome': products, 'Valor': prices}
    df = pd.DataFrame(produtos, columns=('Nome', 'Valor'))

    print('Gerando Arquivo... \n')
    df.to_excel("tabela.xlsx", sheet_name='Produtos')

    print('Programa finalizado!')
