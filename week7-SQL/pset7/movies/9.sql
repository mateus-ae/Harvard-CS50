SELECT p.name FROM movies m
INNER JOIN stars s
ON m.id = s.movie_id
INNER JOIN people p
ON s.person_id = p.id
WHERE m.year = 2004
ORDER BY p.birth;