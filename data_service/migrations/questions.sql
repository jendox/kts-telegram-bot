-- Вставляем вопросы и ответы
DO $$
DECLARE
    q_id INTEGER;
BEGIN
    -- Вопрос 1
    INSERT INTO questions (title) VALUES ('Что можно найти в женской сумочке?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Помада', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Зеркало', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кошелек', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Телефон', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Расческа', 5);

    -- Вопрос 2
    INSERT INTO questions (title) VALUES ('Что люди обычно делают утром?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Чистят зубы', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Завтракают', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Умываются', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Пьют кофе', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Одеваются', 5);

    -- Вопрос 3
    INSERT INTO questions (title) VALUES ('Что можно приготовить из картошки?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Пюре', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Жареная картошка', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Суп', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Чипсы', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Оладьи', 5);

    -- Вопрос 4
    INSERT INTO questions (title) VALUES ('Что может испугать человека ночью?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Тень', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Шум', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кошка', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Скрип двери', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Свет фонаря', 5);

    -- Вопрос 5
    INSERT INTO questions (title) VALUES ('Что чаще всего теряют люди?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Телефон', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ключи', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Деньги', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Документы', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Очки', 10);

    -- Вопрос 6
    INSERT INTO questions (title) VALUES ('Что берут с собой на пляж?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Полотенце', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Купальник', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Солнцезащитный крем', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Очки', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Зонт', 10);

    -- Вопрос 7
    INSERT INTO questions (title) VALUES ('Что можно увидеть в зоопарке?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Лев', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Обезьяна', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Слон', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Тигр', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Зебра', 10);

    -- Вопрос 8
    INSERT INTO questions (title) VALUES ('Что люди любят есть летом?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Мороженое', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Арбуз', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Шашлык', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Овощи', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Фрукты', 5);

    -- Вопрос 9
    INSERT INTO questions (title) VALUES ('Что может разбудить человека?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Будильник', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Шум', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Свет', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Телефон', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кошка', 5);

    -- Вопрос 10
    INSERT INTO questions (title) VALUES ('Что можно забыть дома?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Телефон', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ключи', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кошелек', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Документы', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Очки', 5);

    -- Вопрос 11
    INSERT INTO questions (title) VALUES ('Что может испортить настроение?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Дождь', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Пробка', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ссора', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Потеря денег', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Болезнь', 10);

    -- Вопрос 12
    INSERT INTO questions (title) VALUES ('Что можно подарить на день рождения?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Цветы', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Книгу', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Духи', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Игрушку', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Сладости', 10);

    -- Вопрос 13
    INSERT INTO questions (title) VALUES ('Что может быть круглым?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Мяч', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Солнце', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Колесо', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Тарелка', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Луна', 5);

    -- Вопрос 14
    INSERT INTO questions (title) VALUES ('Что может быть горячим?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Чай', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кофе', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Плита', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Песок', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Солнце', 5);

    -- Вопрос 15
    INSERT INTO questions (title) VALUES ('Что может быть мягким?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Подушка', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Игрушка', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Диван', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Хлеб', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Одеяло', 5);

    -- Вопрос 16
    INSERT INTO questions (title) VALUES ('Что можно увидеть в небе?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Солнце', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Облака', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Самолет', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Птицы', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Звезды', 5);

    -- Вопрос 17
    INSERT INTO questions (title) VALUES ('Что может быть холодным?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Лед', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Мороженое', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Вода', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Зима', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ветер', 5);

    -- Вопрос 18
    INSERT INTO questions (title) VALUES ('Что может быть сладким?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Шоколад', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Мед', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Торт', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Фрукты', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Конфеты', 5);

    -- Вопрос 19
    INSERT INTO questions (title) VALUES ('Что может быть острым?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Нож', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Перец', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Игла', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Лезвие', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Вилка', 5);

    -- Вопрос 20
    INSERT INTO questions (title) VALUES ('Что может быть быстрым?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Автомобиль', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Самолет', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Поезд', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Бег', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ветер', 5);

    -- Вопрос 21
    INSERT INTO questions (title) VALUES ('Что можно увидеть в деревне?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Корова', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Курица', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Огород', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Дом', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Трактор', 10);

    -- Вопрос 22
    INSERT INTO questions (title) VALUES ('Что можно увидеть в школе?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Учитель', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ученики', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Доска', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Парты', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Учебники', 5);

    -- Вопрос 23
    INSERT INTO questions (title) VALUES ('Что можно увидеть в лесу?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Деревья', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Грибы', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Звери', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Птицы', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Ягоды', 5);

    -- Вопрос 24
    INSERT INTO questions (title) VALUES ('Что можно увидеть в больнице?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Врач', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Больные', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Уколы', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Таблетки', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Халаты', 5);

    -- Вопрос 25
    INSERT INTO questions (title) VALUES ('Что можно увидеть в магазине?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Продавец', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Покупатели', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Продукты', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Касса', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Витрина', 10);

    -- Вопрос 26
    INSERT INTO questions (title) VALUES ('Что можно увидеть в парке?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Деревья', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Лавочки', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Детская площадка', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Фонтаны', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Гуляющие', 10);

    -- Вопрос 27
    INSERT INTO questions (title) VALUES ('Что можно увидеть в кинотеатре?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Экран', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Зрители', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кресла', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Попкорн', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Билеты', 5);

    -- Вопрос 28
    INSERT INTO questions (title) VALUES ('Что можно увидеть в кафе?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Столы', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Официант', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Меню', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Еда', 15);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Кофе', 10);

    -- Вопрос 29
    INSERT INTO questions (title) VALUES ('Что можно увидеть в библиотеке?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Книги', 40);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Стеллажи', 25);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Читатели', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Библиотекарь', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Тишина', 5);

    -- Вопрос 30
    INSERT INTO questions (title) VALUES ('Что можно увидеть в музее?') RETURNING id INTO q_id;
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Картины', 35);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Экспонаты', 30);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Посетители', 20);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Гид', 10);
    INSERT INTO answers (question_id, title, points) VALUES (q_id, 'Билеты', 5);
END $$;