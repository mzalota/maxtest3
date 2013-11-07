SELECT *
FROM schyoga_instructor instr
LEFT JOIN schyoga_instructor_studios instr_st on instr_st.instructor_id = instr.id
WHERE instr.name_url in (select name_url from schyoga_instructor group by name_url having count(id) > 1)
ORDER BY instr.name_url, instr.id

insert into schyoga_instructor_studios (instructor_id, studio_id) values (315,50);
insert into schyoga_instructor_studios (instructor_id, studio_id) values (9,88);
insert into schyoga_instructor_studios (instructor_id, studio_id) values (159,88);

delete from schyoga_instructor_studios where instructor_id in (334,604,610);
delete from schyoga_event where instructor_id in (334,604,610);
delete from schyoga_instructor where id in (334,604,610);