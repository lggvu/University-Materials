-- 1
SELECT first_name AS "First Name",  last_name AS "Last Name" FROM EMPLOYEES;

-- 2
SELECT DISTINCT department_id FROM employees;

-- 3
SELECT * FROM employees
ORDER BY first_name DESC;

-- 4
SELECT first_name, last_name, salary, 0.15*salary AS PF
FROM employees;

-- 5
SELECT employee_id, first_name, last_name, salary
FROM employees
ORDER BY salary;

-- 6
SELECT SUM(salary) FROM employees;

-- 7
SELECT MAX(salary), MIN(salary)
FROM employees;

-- 8
SELECT AVG(salary), COUNT(employee_id)
FROM employees;

-- 9
SELECT department_id, COUNT(employee_id)
FROM employees
GROUP BY department_id;

-- 10
SELECT COUNT(job_id)
FROM employees;