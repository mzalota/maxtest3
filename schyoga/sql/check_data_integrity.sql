-- Check if there are instructors with duplicate name_url
SELECT *
FROM schyoga_instructor instr
LEFT JOIN schyoga_instructor_studios instr_st on instr_st.instructor_id = instr.id
WHERE instr.name_url in (select name_url from schyoga_instructor group by name_url having count(id) > 1)
ORDER BY instr.name_url, instr.id;

-- insert into schyoga_instructor_studios (instructor_id, studio_id) values (315,50);
-- insert into schyoga_instructor_studios (instructor_id, studio_id) values (9,88);
-- insert into schyoga_instructor_studios (instructor_id, studio_id) values (159,88);
--
-- delete from schyoga_instructor_studios where instructor_id in (334,604,610);
-- delete from schyoga_event where instructor_id in (334,604,610);
-- delete from schyoga_instructor where id in (334,604,610);


-- Check if instructor is teaching more then one class at once
SELECT studio_id, st.name, instructor_name, instructor_id, start_time, ev.modified_on, count(*)
FROM schyoga_event ev
JOIN schyoga_studio st on st.id=ev.studio_id
WHERE instructor_id is not null
GROUP BY instructor_id, studio_id, start_time
HAVING count(*) > 1
UNION
SELECT studio_id, st.name, instructor_name, instructor_id, start_time, ev.modified_on, count(*)
FROM schyoga_event ev
JOIN schyoga_studio st on st.id=ev.studio_id
WHERE instructor_id is null
GROUP BY instructor_name, studio_id, start_time
HAVING count(*) > 1;


-- inspect the format of the instructor names in Event table for which there is no Instructor object
select distinct(instructor_name) from schyoga_event where instructor_id is null;
