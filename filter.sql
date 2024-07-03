-- select * from df_entries as e where e.log_status in ('WARN', 'ERROR')

-- select * from df_lines as l 
-- join df_entries as e on l.entry_id = e.id 

select l.id
     , l.entry_id
     , l.line as line_contents
     , e.entry as entry_contents 

from df_lines as l 
join df_entries as e on l.entry_id = e.id
where l.entry_id = 2455

-- select length(e.line_numbers) as line_numbers_length from df_entries as e where length(e.line_numbers) > 1

-- select l.id
-- , l.line as line_contents
-- , l.entry_id 
-- from df_lines as l 
