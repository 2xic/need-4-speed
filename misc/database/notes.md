Why is there such a huge difference between the left joins ?
- Postgres seems to be linear
- Firebird seems to be close to exponential.

One thing to note is that Postgres automatically adds a unique index when a primary key is added on a table [1]. But this also seems to be the case with firebird [2] [3].
Have also tried to add it as a foreign key, but the firebird curve still looks almost exponential. 

[1] https://www.postgresql.org/docs/current/indexes-unique.html
[2] https://www.ibexpert.net/ibe/pmwiki.php?n=Doc.Keys
[3] https://www.firebirdfaq.org/faq183/
