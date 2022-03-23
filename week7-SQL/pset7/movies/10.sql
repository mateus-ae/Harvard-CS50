SELECT DISTINCT p.name FROM movies m
INNER JOIN ratings r
ON m.id = r.movie_id
INNER JOIN directors d
ON m.id = d.movie_id
INNER JOIN people p
ON d.person_id = p.id
WHERE r.rating >= 9.0;