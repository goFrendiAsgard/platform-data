-- Create table
CREATE OR REPLACE TABLE mydb.voting_copy
(
    id UInt64,
    vote_time DateTime not null,
    voter varchar not null,
    candidate varchar not null
)
ENGINE = MergeTree
ORDER BY id;