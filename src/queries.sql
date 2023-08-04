CREATE DATABASE vacancies;

CREATE TABLE IF NOT EXISTS vacancies(
                        id INT PRIMARY KEY,
                        vacancy_name TEXT,
                        salary_from INT,
                        salary_to INT,
                        company_name TEXT,
                        url TEXT,
                        requirements TEXT
                    );

INSERT INTO vacancies (id,
                        vacancy_name,
                        salary_from,
                        salary_to,
                        company_name,
                        url,
                        requirements)
                        VALUES (%s, %s, %s, %s, %s, %s, %s);

TRUNCATE TABLE vacancies;

SELECT company_name, COUNT(*) as vacancies_count
            FROM vacancies
            GROUP BY company_name
            ORDER BY vacancies_count DESC;

SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            ORDER BY salary_from DESC;

SELECT AVG(salary_from) FROM vacancies;

SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE salary_from > {avg_salary}
            ORDER BY salary_from DESC;

SELECT company_name, vacancy_name, salary_from, url
            FROM vacancies
            WHERE vacancy_name LIKE '%{keyword}%'
            ORDER BY salary_from DESC