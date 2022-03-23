SELECT p.name FROM movies m
INNER JOIN stars s
ON m.id = s.movie_id
INNER JOIN people p
ON p.id = s.person_id
WHERE m.id in(
SELECT m.id FROM movies m
INNER JOIN stars s
ON m.id = s.movie_id
INNER JOIN people p
ON p.id = s.person_id
WHERE p.name = "Kevin Bacon" AND p.birth = 1958)
AND p.name IS NOT "Kevin Bacon";