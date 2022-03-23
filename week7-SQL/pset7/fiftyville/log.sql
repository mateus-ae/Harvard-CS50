-- Keep a log of any SQL queries you execute as you solve the mystery.
-- All you know is that the theft took place on July 28, 2020 and that it took place on Chamberlin Street.
SELECT * FROM crime_scene_reports
WHERE street = "Chamberlin Street" AND month = 7 AND day = 28;
-- Theft of the CS50 duck took place at 10:15am at the Chamberlin Street courthouse. Interviews were conducted today with three witnesses who were present at the time — each of their interview transcripts mentions the courthouse.
SELECT * FROM interviews
WHERE month = 7 AND day = 28 AND transcript LIKE "%courthouse%";
-- Ruth: Sometime within ten minutes of the theft, I saw the thief get into a car in the courthouse parking lot and drive away. If you have security footage from the courthouse parking lot, you might want to look for cars that left the parking lot in that time frame.
-- Eugene: I don't know the thief's name, but it was someone I recognized. Earlier this morning, before I arrived at the courthouse, I was walking by the ATM on Fifer Street and saw the thief there withdrawing some money.
-- Raymond: As the thief was leaving the courthouse, they called someone who talked to them for less than a minute. In the call, I heard the thief say that they were planning to take the earliest flight out of Fiftyville tomorrow. The thief then asked the person on the other end of the phone to purchase the flight ticket.
SELECT hour, minute FROM courthouse_security_logs
WHERE activity = "entrance" AND year = 2020 AND month = 7 AND day = 28 AND license_plate = (
SELECT license_plate FROM people
WHERE name = "Eugene");
-- Nothing found
SELECT name FROM people
WHERE id IN(
SELECT person_id FROM bank_accounts
WHERE account_number IN(
SELECT account_number FROM atm_transactions
WHERE month = 7 AND year = 2020 AND day = 28 AND atm_location =  "Fifer Street" AND transaction_type = "withdraw"));
-- Bobby Elizabeth Victoria Madison Roy Danielle Russell Ernest
SELECT id, hour, minute FROM flights
WHERE day = 29 AND month = 7 AND year = 2020 AND origin_airport_id = (
SELECT id FROM airports
WHERE city = "Fiftyville")
ORDER BY hour, minute
LIMIT 1;
-- id 36 | hour 8 | minute 20
SELECT name FROM people 
WHERE passport_number IN (
SELECT passport_number FROM passengers
WHERE flight_id = 36)
AND name IN ('Bobby', 'Elizabeth', 'Victoria', 'Madison', 'Roy', 'Danielle', 'Russell', 'Ernest');
-- Bobby Madison Danielle Ernest
SELECT name from people
WHERE license_plate IN 
(SELECT license_plate FROM courthouse_security_logs
WHERE activity = "exit" AND year = 2020 AND month = 7 AND day = 28 AND hour = 10 AND minute >= 15 AND minute <= 25)
AND name IN ('Bobby', 'Madison', 'Danielle', 'Ernest');
-- Danielle left at 10h19, Ernest left at 10h18
SELECT name, phone_number FROM people
WHERE phone_number IN(
SELECT caller
FROM phone_calls
WHERE year = 2020 AND month = 7 AND day = 28 AND duration < 60)
AND name IN ('Danielle', 'Ernest');
-- Ernest (Thief), (367) 555-5533
SELECT name, phone_number FROM people
WHERE phone_number = (
SELECT receiver FROM phone_calls
WHERE caller = '(367) 555-5533' AND year = 2020 AND month = 7 AND day = 28 AND duration < 60);
-- Berthold(Helper/Receiver of the phone call)
SELECT city FROM airports
WHERE id = (
SELECT destination_airport_id FROM flights
WHERE id = 36);
-- London (Where the thief escaped to)
