-- #1
-- select * from df_entries as e where e.log_status in ('WARN', 'ERROR')

-- #2
-- select * from df_lines as l
-- join df_entries as e on l.entry_id = e.id

-- #3
-- select length(e.line_numbers) as line_numbers_length from df_entries as e where length(e.line_numbers) > 1

-- #4
select l.id
     , l.line as line_contents
     , e.log_status
     , e.line_numbers as related_entry_lines
     -- , e.entry as entry_contents
     , l.entry_id
from df_lines as l
join df_entries as e on l.entry_id = e.id
where l.entry_id = 2455
