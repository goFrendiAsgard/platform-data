-- Create table
create table mydb.public.voting (
    id serial primary key
    , vote_time timestamp not null
    , voter varchar not null
    , candidate varchar not null
);


-- Populate values
DO $$ 
DECLARE
    start_date TIMESTAMP := NOW(); -- Replace with your desired start date
    end_date TIMESTAMP := NOW() + INTERVAL '15 days'; -- Add 15 days to the start date
    voters VARCHAR[] := ARRAY['Alice', 'Bob', 'Charlie', 'David', 'Eva']; -- Sample voter names
    candidates VARCHAR[] := ARRAY['Charmender', 'Squirtle', 'Bulbasaur']; -- Sample candidate names
    vote_index INT := 0;
    max_vote INT := 0;
BEGIN
    WHILE start_date <= end_date LOOP
	    max_vote := random() * 100;
	    vote_index := 0;
	    WHILE vote_index <= max_vote LOOP
	        INSERT INTO mydb.public.voting (vote_time, voter, candidate)
	        VALUES (
	            start_date + (random() * (end_date - start_date)), -- Random date within the range
	            voters[1 + (random() * (array_length(voters, 1) - 1))], -- Random voter name
	            candidates[1 + (random() * (array_length(candidates, 1) - 1))] -- Random candidate name
	        );
	       	vote_index := vote_index + 1;
        END LOOP;
        start_date := start_date + INTERVAL '1 day'; -- Move to the next day
    END LOOP;
END $$;

-- Create view
create view mydb.public.daily_voting as (
    select
        date_trunc('day', vote_time) as vote_day_bucket
        , candidate
        , count(1) as vote_count
    from mydb.public.voting
    group by vote_day_bucket, candidate
    order by vote_day_bucket, candidate
);
