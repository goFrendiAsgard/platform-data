select
    id
    , date_trunc('day', vote_time) as day_bucket
    , candidate
    , vote_time
    , voter
from {{ source('mydb', 'voting') }}
