-- Question 1: Write a query to find the name (first_name, last_name), job, department ID and name of the employees who works in London.
SELECT em.first_name, em.last_name, jb.job_title, em.department_id
FROM employees AS em
JOIN departments AS dp ON dp.DEPARTMENT_ID = em.DEPARTMENT_ID
JOIN jobs AS jb ON jb.JOB_ID = em.JOB_ID
JOIN locations AS lc ON lc.LOCATION_ID = dp.LOCATION_ID
WHERE lc.CITY ILIKE 'London';


-- Question 2: Write a query to find the employee id, name (last_name) along with their manager_id and name (last_name).
SELECT em1.employee_id, em1.last_name, em1.manager_id, em2.last_name AS "manager_name"
FROM employees AS em1
JOIN employees AS em2
ON em1.manager_id = em2.employee_id;


-- Question 3: Write a query to find the employee ID, job title, number of days between ending date and starting date for all jobs in department 90.
SELECT em.employee_id, jb.job_title, (jh.end_date - jh.start_date) AS days
FROM employees AS em
JOIN job_history AS jh
ON jh.employee_id = em.employee_id
JOIN departments AS dp
ON dp.department_id = em.department_id
JOIN jobs AS jb
ON jb.job_id = em.job_id
WHERE dp.department_id = 90;

-- SHOULD BE THIS (Filter first, then Join!) -> More optimised 
-- // TODO sth is wrong here pls check again // 
SELECT em.employee_id, jb.job_title, (jh.end_date - jh.start_date) AS days
FROM (SELECT department_id FROM departments WHERE department_id=90) AS dp 
JOIN employees AS em 
ON em.department_id = dp.department_id
JOIN jobs AS jb
ON jb.job_id = em.job_id
JOIN job_history AS jh
ON jh.job_id = jb.job_id;

-- Question 4: Write a query to display the job title and average salary of employees.
SELECT jb.job_title, AVG(salary)
FROM employees AS em
JOIN JOBS AS jb
ON jb.job_id = em.job_id
GROUP BY job_title;

-- Question 5: Write a query to display job title, employee name, and the difference between salary of the employee and minimum salary for the job.
SELECT jb.job_title, em.first_name, em.last_name, em.salary - jb.min_salary AS "salary_difference"
FROM employees as em
JOIN jobs as jb
ON jb.job_id = em.job_id;


-- Question 6: Write a query to display the job history that were done by any employee who is currently drawing more than 10000 of salary.
SELECT jh.* 
FROM job_history AS jh 
JOIN employees AS em
ON (jh.employee_id = em.employee_id) 
WHERE salary > 10000;


-- Question 7: Write a query to display department name, name (first_name, last_name), hire date, salary of the manager for all managers whose experience is more than 15 years.
SELECT dp.department_name, em.first_name, em.last_name, em.hire_date, em.salary
FROM employees AS em
JOIN departments AS dp
ON em.department_id = dp.department_id
WHERE em.employee_id IN (
SELECT manager_id FROM departments)
AND (EXTRACT(DAY FROM (SELECT NOW() - em.hire_date))) / 365 > 15;
-- OR
select department_name, first_name, last_name, sala?, hire_date
from 
(select employee_id, first_name, last_name, salary, hire_date
from employees
where year(getdate())-year(hire_date) >= 15) as m -- sqlserver
join departments
on m.emmployee_id = departments.manager_id




-- Question 8: Write a query to get the firstname, lastname who joined in the month of June.
SELECT first_name, last_name FROM employees
WHERE EXTRACT(MONTH FROM hire_date) = 6;


-- Question 9: Write a query to get the years in which more than 10 employees joined.
SELECT EXTRACT(YEAR FROM hire_date)
FROM employees  
GROUP BY EXTRACT(YEAR FROM hire_date) 
HAVING COUNT(EMPLOYEE_ID) > 10;


-- Question 10: Write a query to get first name of employees who joined in 1987.
SELECT first_name
FROM employees
WHERE EXTRACT(YEAR FROM hire_date) = 1987;


-- Question 11: Write a query to get department name, manager name, and salary of the manager for all managers whose experience is more than 5 years.
SELECT dp.department_name, em.first_name, em.last_name, salary
FROM employees AS em
JOIN departments AS dp
ON em.department_id = dp.department_id
WHERE employee_id IN
(SELECT manager_id FROM departments)
AND EXTRACT(DAY FROM(SELECT NOW() - em.hire_date))/365 > 5;


-- Question 12: Write a query to find all employees where first names are in upper case.
SELECT *
FROM employees
WHERE first_name = UPPER(first_name);


-- Question 13: 
SELECT RIGHT(phone_number, 4) AS "phone_number" FROM employees;

