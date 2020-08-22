import streamlit as st
import pandas as pd
import requests as r
import base64


from bs4 import BeautifulSoup
from io import BytesIO

def has_data_index(tag):
    return tag.has_attr('data-index') and tag.has_attr('data-uuid')

def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Produtos')
    writer.save()
    processed_data = output.getvalue()
    return processed_data

def get_table_download_link(df):
    """Generates a link allowing the data in a given panda dataframe to be downloaded
    in:  dataframe
    out: href string
    """
    val = to_excel(df)
    b64 = base64.b64encode(val)  # val looks like b'...'
    href = f'<a href="data:application/octet-stream;base64,{b64.decode()}" download="tabela.xlsx">Download xlsx file</a>'  # decode b'abc' => abc
    return href


if __name__ == '__main__':

    products = []
    prices = []

    url = 'https://www.amazon.com.br/s?k={}&__mk_pt_BR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&ref=nb_sb_noss/'
    word = 'iphone'
    count = 1  # count que vai ate 24 que é quantidade de item por pagina

    st.title('Websraping')
    st.markdown('Essa é uma aplicação te retorna uma lista com os nomes e preços de todos os produtos encontrados na primeira página da Amazon.')

    word = st.text_input("Digite o nome do produto ")

    if word:

        response = r.get(url.format(word))

        soup = BeautifulSoup(response.text, "html.parser")
        search_results = soup.find_all(has_data_index)

        print(search_results)

        if search_results:

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
                        #nao tem preco
                        prices.append('Sem preço')

                count = count + 1


            produtos = {'Nome': products, 'Valor': prices}
            df = pd.DataFrame(produtos, columns=('Nome', 'Valor'))
            st.table(df)

            st.subheader('Faça download da tabela: ')
            st.markdown(get_table_download_link(df), unsafe_allow_html=True)

        else:
            st.write('Desculpe, ocorreu um erro :(')
            st.write('Tente novamente mais tarde !')


