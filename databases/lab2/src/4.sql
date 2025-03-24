-- 4. В таблице Н_ГРУППЫ_ПЛАНОВ найти номера планов, по которым обучается (обучалось) менее 2 групп ФКТИУ. 
-- Для реализации использовать соединение таблиц.

SELECT "Н_ГРУППЫ_ПЛАНОВ"."ПЛАН_ИД"
FROM "Н_ГРУППЫ_ПЛАНОВ"
    INNER JOIN "Н_ПЛАНЫ" ON "Н_ГРУППЫ_ПЛАНОВ"."ПЛАН_ИД" = "Н_ПЛАНЫ"."ИД"
    INNER JOIN "Н_ОТДЕЛЫ" ON "Н_ПЛАНЫ"."ОТД_ИД" = "Н_ОТДЕЛЫ"."ИД"
WHERE "Н_ОТДЕЛЫ"."КОРОТКОЕ_ИМЯ" = 'КТиУ'
GROUP BY "Н_ГРУППЫ_ПЛАНОВ"."ПЛАН_ИД"
HAVING COUNT(*) > 2;