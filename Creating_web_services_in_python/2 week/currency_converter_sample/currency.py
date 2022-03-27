"""
Конвертер валют
Описание задания
В этом задании придется написать свой конвертер валют (см. приложенный файл). Курсы валют нужно брать из API
Центробанка. Документация по нему тут, потребуется только XML_daily.asp. (Обратите внимание, что указанный в
документации API протокол http больше не поддерживается при запросах с помощью requests.get, указывайте в строке
запроса https)
В функцию convert(amount, cur_from, cur_to, date, requests) будет передана сумма amount в валюте с кодом cur_from, и
её требуется перевести в валюту cur_to через рубль (код: RUR). Для запроса к API нужно использовать переданный
requests, точнее, его метод get().
Все суммы и курсы требуется хранить в Decimal, т.к. для финансовых данных вычисления с фиксированной точкой подходят
больше.
Конечный результат нужно округлить до 4-х знаков, перед тем как вернуть его из функции. Посмотрите метод quantize().
Для некоторых валют курс возвращается из расчета не на одну денежную единицу указанной валюты, а на 10 или даже 100,
поэтому у курса валюты в XML есть не только Value, но и Nominal, и справедлива формула: Nominal ед. валюты = Value
рублей.
При проверке на сервере сеть недоступна. В функцию будет передан фейковый requests, его интерфейс и response
аналогичны настоящему. Если его использовать в объеме, требуемом для задания, разницы не будет заметно.
"""

from bs4 import BeautifulSoup
from decimal import Decimal


def convert(amount, cur_from, cur_to, date, requests):
    response = requests.get('https://www.cbr.ru/scripts/XML_daily.asp',
                            {'date_req': date})
    soup = BeautifulSoup(response.content, 'xml')
    rates = {}
    for i in soup('Valute'):
        rates[i.CharCode.string] = (Decimal(i.Value.string.replace(',', '.')),
                                    int(i.Nominal.string))
    rates['RUR'] = (Decimal('1.0000'), 1)
    result = amount * rates[cur_from][0] * rates[cur_to][1] /\
             rates[cur_from][1] / rates[cur_to][0]

    return result.quantize(Decimal('.0001'))

#######################################################################################################################
# Конвертер валют от преподавателей
#######################################################################################################################

# from bs4 import BeautifulSoup
# from decimal import Decimal
#
#
# def convert(amount, cur_from, cur_to, date, requests):
#     result = requests.get("https://www.cbr.ru/scripts/XML_daily.asp", {"date_req": date})
#     soup = BeautifulSoup(result.content, 'xml')
#     rates = {i.CharCode.string: (
#         Decimal(i.Value.string.replace(',', '.')),
#         int(i.Nominal.string)
#     ) for i in soup('Valute')
#     }
#     rates['RUR'] = (Decimal(1), 1)
#
#     result = amount * rates[cur_from][0] * rates[cur_to][1] / rates[cur_from][1] / \
#              rates[cur_to][0]
#     return result.quantize(Decimal('.0001'))
