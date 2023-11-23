-- For student :- Companies table

CREATE TABLE company_table ( id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                          c_name TEXT NOT NULL,
                          c_loc TEXT NOT NULL,
                          c_min_SCGPA INTEGER DEFAULT 00.00,
                          c_min_Sal TEXT DEFAULT "   -  ",
                          c_max_Sal TEXT DEFAULT "   -  ",
                          vacancies TEXT DEFAULT "   -  ",
                          FOREIGN KEY (user_id) REFERENCES users(id));
-- /////////////////////////////////////////////////////////////////////////////////

CREATE TABLE users (  id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
                             username TEXT NOT NULL,
                             hash TEXT NOT NULL,
                             user_type TEXT);

-- /////////////////////////////////////////////////////////////////////////////////
-- For companies :- student table

CREATE TABLE applicant_table ( applicant_id INTEGER PRIMARY KEY AUTOINCREMENT,
                            user_id INTEGER NOT NULL,
                          stud_name TEXT NOT NULL,
                          stud_sub TEXT NOT NULL,
                          s_SCGPA TEXT NOT NULL,
                          linkedin_link TEXT,
                          timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                          FOREIGN KEY (user_id) REFERENCES users(id));
-- ////////////////////////////////////////////////////////////////////////////////
CREATE TABLE hire_request_table ( request_c_id INTEGER PRIMARY KEY AUTOINCREMENT,
                                  user_id INTEGER,
                                  company_name TEXT,
                                  FOREIGN KEY (user_id) REFERENCES users(id));
-- /////////////////////////////////////////////////////////////////////////////////////////////////////////
CREATE TABLE applicant_company_request AS
SELECT a.user_id, a.stud_name, a.stud_sub, a.s_SCGPA, a.linkedin_link, h.company_name
FROM applicant_table AS a
INNER JOIN hire_request_table AS h
ON a.user_id = h.user_id;

-- SELECT * FROM users;
-- SELECT * FROM applicant_table;
-- SELECT * FROM company_table;
-- SELECT * FROM hire_request_table;
-- SELECT * FROM applicant_company_request;
