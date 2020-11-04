# Podemos agregarle opciones al driver para utilizar los distintos modos del Chrome
from selenium import webdriver
from bs4 import BeautifulSoup
import time

def obtener_precios(vuelo):
    # Funcion que retorna una lista de diccionarios con las distintas tarifas
    precios = []
    # Ahora hay que click sobre el vuelo
    vuelo.find_element_by_xpath('.//div[@class="flight-container"]/button').click()
    time.sleep(0.5)

    fare_type = vuelo.find_elements_by_xpath('.//table[@class="fare-options-table"]//thead//th[contains(@class, "fare")]//span')
    currency = vuelo.find_elements_by_xpath('.//table[@class="fare-options-table"]//tfoot//td[contains(@class, "fare")]//span[@class="currency-symbol"]')
    tarifas = vuelo.find_elements_by_xpath('.//table[@class="fare-options-table"]//tfoot//td[contains(@class, "fare")]//span[@class="value"]')

    for i in range(len(tarifas)):
        nombre = fare_type[i].text
        moneda = currency[i].text
        valor = tarifas[i].text
        dict_tarifa = {nombre : {'Moneda':moneda, 'Valor': valor}}
        precios.append(dict_tarifa)

    vuelo.find_element_by_xpath('.//div[@class="flight-container"]/button').click()
    return precios


def obtener_datos_escalas(vuelo):
# Funcion que retorna una lista de diccionariso con la informaci[on de las escalas de cada vuelo
    info_escalas = []
    vuelo.find_element_by_xpath('.//div[@class="flight-summary-stops-description"]/button').click()
    time.sleep(0.5)

    segmentos = vuelo.find_elements_by_xpath('//div[@class="sc-cLQEGU hyoued"]')
    
    segmentos_procesados = 0

    tiempo_escala = vuelo.find_elements_by_xpath('//div[@class="sc-hZSUBg gfeULV"]/div[@class="sc-cLQEGU dnKRNG"]//span[@class="sc-esjQYD dMquDU"]/time') 

    for segmento in segmentos:

        city = segmento.find_elements_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/abbr')
        de_city = city[0].text
        ar_city = city[1].text

        schedule = segmento.find_elements_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/time')
        de_schedule = schedule[0].get_attribute('datetime')
        ar_schedule = schedule[1].get_attribute('datetime')

        flight_no = segmento.find_element_by_xpath('.//div[@class="airline-flight-details"]/b').text
        airplane = segmento.find_element_by_xpath('.//div[@class="airline-flight-details"]/span[@class="sc-gzOgki uTyOl"]').text

        if segmento != segmentos[-1]:
            duration_stop = tiempo_escala[segmentos_procesados].get_attribute('datetime')
            segmentos_procesados =+ 1
        else:
            duration_stop = ''

        data_dict = {
            'Origen': de_city,
            'Dep time': de_schedule,
            'Destino': ar_city,
            'Arr Time': ar_schedule,
            'Numero vuelo': flight_no,
            'Modelo Avion': airplane,
            'Duracion escala': duration_stop
        }
        info_escalas.append(data_dict)

    driver.find_element_by_xpath('//div[@class="modal-header sc-dnqmqq cGfTsx"]/button').click()

    return info_escalas


def obtener_tiempos(vuelo):
# Funcion que retorna un diccionario con los horarios de salida y llegada de cada vuelo, incluyendo la duracion.
# Nota: La duracion del vuelo no es la hora de llegada - la hora de salida porque puede haber diferencia de horarios en las ciudades.
    tiempos = []
    vuelo.find_element_by_xpath('.//div[@class="flight-summary-stops-description"]/button').click()

    segmentos = vuelo.find_elements_by_xpath('//div[@class="sc-cLQEGU hyoued"]')  
    for segmento in segmentos:
        city = segmento.find_elements_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/abbr')
        de_city = city[0].text
        ar_city = city[1].text

        schedule = segmento.find_elements_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/time')
        de_schedule = schedule[0].get_attribute('datetime')
        ar_schedule = schedule[1].get_attribute('datetime')

        duration = segmento.find_element_by_xpath('.//span[@class="sc-esjQYD dMquDU"]/time').get_attribute('datetime')
        data_dict = {
            'Origen': de_city,
            'Dep time': de_schedule,
            'Destino': ar_city,
            'Arr Time': ar_schedule,
            'Duracion del vuelo': duration
        }
        tiempos.append(data_dict)
    
    driver.find_element_by_xpath('//div[@class="modal-header sc-dnqmqq cGfTsx"]/button').click()

    return tiempos


def main():

    time.sleep(8)
    try:
        driver.find_element_by_xpath('//div[@class="slidedown-footer"]/button[@class="align-right secondary slidedown-button"]').click()
    except:
        pass
    try:
        driver.find_element_by_xpath('//div[@class="lightbox-container"]//span[@class="close"]').click()
    except:
        pass

    # Para seleccionar las cosas, necesitamos usar un XPATH
    vuelos = driver.find_elements_by_xpath('//li[@class="flight"]')
    vuelo = vuelos[10]
    
    precios = obtener_precios(vuelo)
    print(precios)

    info_escalas = obtener_datos_escalas(vuelo)
    print(info_escalas)

    tiempos = obtener_tiempos(vuelo)
    print(tiempos)

    driver.close()

if __name__ == "__main__":

    url = 'https://www.latam.com/es_co/apps/personas/booking?fecha1_dia=16&fecha1_anomes=2021-01&auAvailability=1&ida_vuelta=ida&vuelos_origen=Bogot%C3%A1&from_city1=BOG&vuelos_destino=Lima&to_city1=SCL&flex=1&vuelos_fecha_salida_ddmmaaaa=20/01/2021&cabina=Y&nadults=1&nchildren=0&ninfants=0&cod_promo=&stopover_outbound_days=0&stopover_inbound_days=0&application=#/'
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    driver.get(url)

    main()