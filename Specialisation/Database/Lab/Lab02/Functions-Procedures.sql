-- Question 1: Create fullname function which concat the firstname and the lastname into a string value. Use this function for listing fullname of all employees.
CREATE FUNCTION FULLNAME(@FIRST_NAME VARCHAR(20),@LAST_NAME VARCHAR(20))
	RETURNS VARCHAR(20) AS 
	BEGIN 
		RETURN @FIRST_NAME + ' '+ @LAST_NAME
	END;
SELECT dbo.FULLNAME(FIRST_NAME,LAST_NAME) FROM employees;

-- Question 2: Create get_job_title function which return a job title for a given job id. Use this function for listing all employees’ names and their job title
CREATE FUNCTION GET_JOB_TITLE(@JOB_ID varchar(10))
	RETURNS table AS
		RETURN 
			SELECT JOB_TITLE FROM jobs
			WHERE JOB_ID = @JOB_ID;

-- Question 3: Create a function that count the number of departments in a specific country. Using this function for counting number of departments in every regions
DROP FUNCTION IF EXISTS funcCountDepartments;
GO

CREATE FUNCTION funcCountDepartments (@country_id CHAR(2))
RETURNS INT AS
BEGIN
    RETURN (
        SELECT COUNT(departments.DEPARTMENT_ID)
        FROM departments 
            INNER JOIN locations ON departments.LOCATION_ID = locations.LOCATION_ID
            INNER JOIN countries ON countries.COUNTRY_ID = locations.COUNTRY_ID
        WHERE countries.COUNTRY_ID = @country_id
    );
END;
GO

SELECT regions.REGION_ID, SUM(dbo.funcCountDepartments(countries.COUNTRY_ID)) AS NUM_OF_DEPARTMENTS
FROM regions
    INNER JOIN countries ON  regions.REGION_ID = countries.REGION_ID
GROUP BY regions.REGION_ID;
GO


-- Question 4: Create a procedure for changing job of an employee
CREATE PROCEDURE change_job (@employee_id INT, @job_id VARCHAR(10))
AS
BEGIN
	INSERT INTO job_history VALUES
	(@employee_id, (SELECT HIRE_DATE FROM employees WHERE EMPLOYEE_ID = @employee_id), (SELECT CONVERT(DATE,GETDATE())),(SELECT JOB_ID FROM employees WHERE EMPLOYEE_ID = @employee_id),(SELECT DEPARTMENT_ID FROM employees WHERE EMPLOYEE_ID = @employee_id));
	UPDATE employees
	SET SALARY = (SELECT MIN(SALARY) FROM employees WHERE JOB_ID = @job_id),
		JOB_ID = @job_id
	WHERE EMPLOYEE_ID = @employee_id;
END