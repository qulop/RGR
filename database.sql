CREATE TABLE item (
    id serial NOT NULL PRIMARY KEY,
    title varchar(100) NOT NULL,
    writer varchar(50) NOT NULL,
    genre varchar(30) NOT NULL,
    issue_year int2 NOT NULL,
    price float4 NOT NULL,
    rating numeric(2, 1)
);


INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Эмма', 'роман', 2018, 13.00, 5.0, 2, 4);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Клара и солнце', 'антиутопия', 2021, 13.00, 5.0, 3, 16);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Освенцим: нацисты и окончательное решение еврейского вопроса', 'исторческий обзор', 2021, 24.6, 4.8, 1, 5);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Нацисты: предостережение истории', 'исторческий обзор', 2021, 25.99, 4.9, 1, 10);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('451° по Фаренгейту', 'антиутопия', 2017, 8.99, 4.3, 4, 2);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Краткие ответы на большие вопросы', 'научно-популярная литература', 2019, 21.5, 4.6, 6, 13);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('На Западном фронте без перемен', 'роман', 2018, 13.00, 4.7, 5, 18);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Три товарища', 'роман', 2017, 10.5, 4.0, 5, 17);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Доктор Живаго', 'роман', 2019, 12.5, 4.3, 7, 7);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Шпиль', 'роман', 2016, 12.00, 4.3, 8, 14);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('1984', 'антиутопия', 2015, 9.99, 4.8, 9, 3);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Скотный двор. Эссе', 'сатира', 2017, 9.99, 4.7, 9, 6);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Фауст', 'трагедия', 2013, 14.99, 4.6, 10, 8);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Великий Гэтсби', 'роман', 2018, 12.3, 4.4, 11, 9);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('О дивный новый мир', 'антиутопия', 2016, 9.99, 4.4, 12, 11);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Процесс', 'роман', 2015, 10.00, 4.0, 13, 12);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Письма незнакомке ', 'письма', 2015, 11.5, 4.4, 14, 15);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Человек, который принял жену за шляпу', 'нейропсихология', 2019, 12.99, 4.8, 15, 19);
INSERT INTO item (id, title, genre, issue_year, price, rating, writer_id, photo_id) VALUES (19, 'Виктория. Пан', 'роман', 2021, 13.00, 5.0, 16, 20);
INSERT INTO item (title, genre, issue_year, price, rating, writer_id, photo_id) VALUES ('Уличный кот по имени Боб', 'история из жизни', 2017, 9.99, 4.5, 17, 21);


INSERT INTO writer (full_name) VALUES ('Джейн Остен');
INSERT INTO writer (full_name) VALUES ('Кадзуо Исигуро');
INSERT INTO writer (full_name) VALUES ('Рей Бредбери');
INSERT INTO writer (full_name) VALUES ('Эрих Мария Ремарк');
INSERT INTO writer (full_name) VALUES ('Стивен Хокинг');
INSERT INTO writer (full_name) VALUES ('Борис Пастернак');
INSERT INTO writer (full_name) VALUES ('Уильям Голдинг');
INSERT INTO writer (full_name) VALUES ('Джордж Оруэлл');
INSERT INTO writer (full_name) VALUES ('Иоганн Вольфганг фон Гете');
INSERT INTO writer (full_name) VALUES ('Фрэнсис Скотт Фицджеральд');
INSERT INTO writer (full_name) VALUES ('Олдос Хаксли');
INSERT INTO writer (full_name) VALUES ('Франц Кафка');
INSERT INTO writer (full_name) VALUES ('Андре Моруа');
INSERT INTO writer (full_name) VALUES ('Оливер Сакс');
INSERT INTO writer (full_name) VALUES ('Кнут Гамсун');


INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/451-degree.png');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/1984.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/amy.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/auschwitz.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/barnyard.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/dr-jivago.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/faust.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/great-gatsby.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/nazis.png');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/new-world.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/process.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/short-answers.png');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/spire.jpeg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/stranger-letters.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/sun-clara.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/three-comrades.jpg');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/west-front.png');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/wife-hat.png');
INSERT INTO item_photo (path) VALUES ('/home/qlop/PythonAll/RGR/content/item-photo/vika.jpg');
