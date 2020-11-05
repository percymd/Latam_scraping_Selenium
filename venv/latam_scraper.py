from selenium import webdriver
from bs4 import BeautifulSoup
import time

def obtener_precios(vuelo):
    
    precios = []
    
    vuelo.find_element_by_xpath('.//div[@class="flight-container"]/button').click()
    time.sleep(0.5)
    
    fare_type = vuelo.find_elements_by_xpath('.//table[@class="fare-options-table"]//thead//th[contains(@class, "fare")]//span')
    currency = vuelo.find_element_by_xpath('//span[@class="price"]/span[@class="currency-symbol"]')
    fare = vuelo.find_elements_by_xpath('.//table[@class="fare-options-table"]//tfoot//td[contains(@class, "fare")]//span[@class="value"]')
    
    for i in range(len(fare)):
        
        nombre = fare_type[i].txt
        moneda = currency[i].txt
        valor = fare[i].txt
        dict_fare = {nombre:{'moneda':moneda, 'valor':valor}}
        precios.append(fare)
        
    vuelo.find_element_by_xpath('.//div[@class="flight-container"]/button').click()
    
    return precios

def obtener_datos_escalas(vuelo):
    
    info_escalas = []
    
    boton_escalas = vuelo.find_element_by_xpath('//div[@class="flight-summary-stops-description"]/button').click()
    time.sleep(0.5)
    
    segmentos = vuelo.find_elements_by_xpath('//div[@class="sc-hZSUBg gfeULV"]/div[@class="sc-cLQEGU hyoued"]')    
    segmentos_procesados = 0
    
    stop_time = vuelo.find_element_by_xpath('.//div[@class="sc-bMVAic hShZwU"]/div[@class="sc-eXEjpC fqUnRK"]//span[@class="sc-esjQYD dMquDU"]/time')
    
    for segmento in segmentos:
        #Ciudad
        city = segmento.find_element_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/abbr')
        origin_city = city[0].txt
        dest_city = city[1].txt 
        
        #Horario
        schedule = segmento.find_element_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/time')
        origin_schedule = schedule[0].get_attribute('datetime')
        dest_schedule = schedule[1].get_attribute('datetime')
        
        #Número de vuelo
        flight_number = segmento.find_element_by_xpath('.//div[@class="airline-flight-details"]/b').txt
        
        #Modelo del avión
        plane_model = segmento.find_element_by_xpath('//div[@class="airline-flight-details"]/span[@class="sc-gzOgki uTyOl"]').txt
        
        if segmento != segmentos[-1]:
            duration_stop = stop_time[segmentos_procesados].get_attribute('datetime')
            segmentos_procesados =+ 1
        else:
            duration_stop = ''
        
        data_dict={
            'origen': origin_city,
            'dep_time': origin_schedule,
            'destino': dest_city,
            'arr_time': dest_schedule,
            'numero_vuelo': flight_number,
            'modelo_avion': plane_model,
            'duracion_escala': duration_stop
        }
        info_escalas.append(data_dict)
        
    driver.find_element_by_xpath('//div[@class="modal-header sc-dnqmqq cGfTsx"]//button[@class="close"]').click()
    
    return info_escalas


def obtener_tiempos(vuelo):
    # Nota: La duracion del vuelo no es la hora de llegada - la hora de salida porque puede haber diferencia de horarios en las ciudades.
    tiempos = []
    
    vuelo.find_element_by_xpath('//div[@class="flight-summary-stops-description"]/button').click()
    
    segmentos = vuelo.find_elements_by_xpath('//div[@class="sc-hZSUBg gfeULV"]/div[@class="sc-cLQEGU hyoued"]')
    
    for segmento in segmentos:
        
        city = segmento.find_element_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/abbr')
        origin_city = city[0].txt
        dest_city = city[1].txt         
        
        schedule = segmento.find_element_by_xpath('.//div[@class="sc-bwCtUz iybVbT"]/time')
        origin_schedule = schedule[0].get_attribute('datetime')
        dest_schedule = schedule[1].get_attribute('datetime')
        
        duration = vuelo.find_element_by_xpath('.//span[@class="sc-esjQYD dMquDU"]/time').get_attribute('datetime')
        time_dict = {
            'origen': origin_city,
            'dep_time': origin_schedule,
            'destino': dest_city,
            'arr_time': dest_schedule,
            'duracion_vuelo': duration
        }
        tiempos.append(time_dict) 
    driver.find_element_by_xpath('//div[@class="modal-header sc-dnqmqq cGfTsx"]//button[@class="close"]').click()
    
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

    url = 'https://www.latam.com/es_pe/apps/personas/booking?fecha1_dia=07&fecha1_anomes=2020-11&auAvailability=1&ida_vuelta=ida&vuelos_origen=Lima&from_city1=LIM&vuelos_destino=Madrid&to_city1=MAD&flex=1&vuelos_fecha_salida_ddmmaaaa=07/11/2020&cabina=Y&nadults=1&nchildren=0&ninfants=0&cod_promo=&stopover_outbound_days=0&stopover_inbound_days=0#/'
    # Podemos agregarle opciones al driver para utilizar los distintos modos del Chrome
    options = webdriver.ChromeOptions()
    options.add_argument('--incognito')
    driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
    driver.get(url)

    main()