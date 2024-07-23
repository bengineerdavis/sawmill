SELECT * FROM df_entries as e
        WHERE e.log_status in ('ERROR')
        OR e.entry ilike '%exception%'
        ORDER BY e.component ASC, e.log_status ASC
