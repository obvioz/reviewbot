# v1(MVP)
- [x] клиент переходит по QR и попадает в ТГ бота      
- [x] бот приветствует клиента и просит ввести отзыв о продукции + при желании прикрепить медиафайл
- [x] процесс взаимодействия клиента с телеграм ботом: 
    - клиент нажимает кнопку "запустить"
    - бот отправляет клиенту приветственное сообщение с указанием нажать на кнопку "оставить отзыв"
    - клиенту доступна одна кнопка "Оставить отзыв"
    - после нажатия клиентом кнопки "Оставить отзыв" ТГ бот отправляет сообщение с инструкцией что нужно делать пользователю
    - пользователь может прикрепить фотографию
    - отзыв опубликовывается после ввода текстовой информации
    - бот пишет "спасибо за отзыв!
- [x] процесс взаимодействия администратора с телеграм ботом:
    - администратор нажимает кнопку "запустить"
    - бот отправляет администратору приветственное сообщение с указанием нажать на кнопку "оставить отзыв" 
    - администратору доступны две кнопки "Получить отзыв" и "Оставить отзыв"
    - при нажатии на кнопку "Получить отзыв" у администратора выпадает 2 кнопки - "Последний отзыв", "Отзывы за неделю"
    - при нажатии на кнопку "Последний отзыв" отображается последний добавленный отзыв
    - при нажатии на кнопку "Отзывы за неделю" отображаются последние добавленные отзывы за 7 дней
- [x] отзывы хранятся в базе данных совместно с ссылкой которая указывает на местонахождение файла на сервере
# v1.1
- [ ] все кнопки работают как команды( работают через / )
- [ ] добавлена кнопка BUTTON_CREATE_MESSAGE = "Создание текста для отправки"
# v2
- [ ] в базе данных в таблице reviews добавлено новая колонка "location" в которой хранятся значения типа str и формата ТА/ТЧ 
    - *расписать работу БД*
    -в колонке location хранится место откуда был оставлен отзыв
        - M - розничный магазин
        - V - вендинговый аппарат
- [ ] после нажатия кнопки "Оставить отзыв" бот отправляет сообщение "пожалуйста выберите где вы находитесь"
    - бот отправлет  две кнопки "Магазин" и "Вендинговый аппарат" 
        - После нажатия на кнопку "Магазин" пользователю выводится приветственное сообщение о том что теперь он может оставить свой отзыв
            *можно добавить опросник, чтобы пользователю было проще, например "понравилось ли вам обслуживание в магазине?"*
        - После нажатия на кнопку "Вендинговый аппарат" пользователю выводится сообщение о том что теперь он может оставить свой отзыв
            *можно добавить опросник, чтобы пользователю было проще, например '1 укажите что вы приобрели', 2 понравилось ли вам блюдо?*
- [ ] *расписать работу кнопок*
- [ ] у администратора после нажатия "запустить" выводится новая кнопка "Рассылка"
    - после нажатия  кнопки "Рассылка" выводится кнопки "Отправка клиентам из магазина" и "Отправка клиентам из ТА"
    - после нажатиня на кнопку "Отправка клиентам из магазина" или "Отправка клиентам из ТА" выводится 
        сообщение с инструкцией "введите сообщение и прикрепите фотографию"
    - администратор может в кнопках "Отправка клиентам из магазина" и "Отправка клиентам из ТА":
        - отправить текст
        - отправить фото
        - отправить текст + фото
    - сообщение будет доставлено пользователям в зависимости от группы " location " в базе данных
- [ ] узнать что происходит когда человек останавливает бота!
- [ ] узнать что происходит если бота начинают спамить!

# v3

- [ ] добавлена возможность генерировать персональный промокод на единоразовую скидку по id пользователя
- [ ] в опредленное время(раз в неделю, месяц) бот рассылает сообщение в зависимости от категории "location"
    - для категории "M" о новинках/скидках этой недели/месяца а также ссылку интернет магазин и купон на первый заказ
    - для категории "v" *разработать*

    



