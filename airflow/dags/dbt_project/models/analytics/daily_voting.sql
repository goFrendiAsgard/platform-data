select
    day_bucket
    , candidate
    , count(1) as vote_count
from {{ ref('voting') }}
group by
    day_bucket
    , candidate
order by
    day_bucket
    , candidate
