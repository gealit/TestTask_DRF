# TestTask_DRF
Test task API mortgage calculator DRF.

### Пользовательский сценарий
Клиент вводит следующие данные:
1. Стоимость объекта недвижимости, в рублях без копеек. Тип данных: integer
2. Первоначальный взнос, в рублях без копеек. Тип данных: integer
3. Срок, в годах. Тип данных: integer

В ответ ему приходит массив с объектами ипотечных предложений. В каждом объекте есть следующие данные:
1. Наименование банка. Тип данных: string
2. Ипотечная ставка, в процентах. Тип данных: float
3. Платеж по ипотеке, в рублях без копеек.  Тип данных: integer

----

### Технические требования
Исходя из выше описанного пользовательского сценария, нужно:
1. Написать модель для хранения ипотечных предложений.
2. Написать ViewSet для реализации функционала CRUD ипотечных предложений.
3. Фильтрацию ипотечных предложений, по введенным параметрам.
4. Реализовать функционал, который будет рассчитывать платеж у всех валидных ипотечных предложений.

Следущие пункты не обязательны, но мы будем рады увидеть их:
1. Сортировка ипотечных предложений по ставке(процент по ипотеке) и по платежу. 
2. Тесты для всего вышеперечилсенного.

----

### Используемый стек
1) Django.
2) DRF.
