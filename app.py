# Core Pkgs
import streamlit as st 
import streamlit.components.v1 as components
import pandas as pd

# DB Mgmt
import mysql.connector

questions = {
    "q1": "Q1) Which categories of movies released in 2018? Fetch with the number of movies.",
    "q2": "Q2) Update the address of actor id 36 to “677 Jazz Street”.",
    "q3": "Q3) Add the new actors (id : 105 , 95) in film  ARSENIC INDEPENDENCE (id:41).",
    "q4": "Q4) Get the name of films of the actors who belong to India.",
    "q5": "Q5) How many actors are from the United States?",
	"q6": "Q6) Get all languages in which films are released in the year between 2001 and 2010.",
	"q7": "Q7) The film ALONE TRIP (id:17) was actually released in Mandarin, update the info.",
	"q8": "Q8) Fetch cast details of films released during 2005 and 2015 with PG rating.",
	"q9": "Q9) In which year most films were released?",
	"q10": "Q10) In which year least number of films were released?",
	"q11": "Q11) Get the details of the film with maximum length released in 2014 .",
	"q12": "Q12) Get all Sci- Fi movies with NC-17 ratings and language they are screened in.",
	"q13": "Q13) The actor FRED COSTNER (id:16) shifted to a new address:\n055,  Piazzale Michelangelo, Postal Code - 50125 , District - Rifredi at Florence, Italy. \nInsert the new city and update the address of the actor.",
	"q14": "Q 14) A new film “No Time to Die” is releasing in 2020 whose details are : Title :- No Time to Die | Description: Recruited to rescue a kidnapped scientist, globe-trotting spy James Bond finds himself hot on the trail of a mysterious villain, who's armed with a dangerous new technology. | \nLanguage: English | \nOrg. Language : English | \nLength : 100 | \nRental duration : 6 | \nRental rate : 3.99 | \nRating : PG-13 | \nReplacement cost : 20.99 | \nSpecial Features = Trailers,Deleted Scenes | \nInsert the above data.",
	"q15": "Q15) Assign the category Action, Classics, Drama  to the movie “No Time to Die” .",
	"q16": "Q16) Assign the cast: PENELOPE GUINESS, NICK WAHLBERG, JOE SWANK to the movie “No Time to Die” .",
	"q17": "Q17) Assign a new category Thriller  to the movie ANGELS LIFE.",
	"q18": "Q18) Which actor acted in most movies?",
	"q19": "Q19) The actor JOHNNY LOLLOBRIGIDA was removed from the movie GRAIL FRANKENSTEIN. How would you update that record?",
	"q20": "Q20) The HARPER DYING movie is an animated movie with Drama and Comedy. Assign these categories to the movie",
	"q21": "Q21) The entire cast of the movie WEST LION has changed. The new actors are DAN TORN, MAE HOFFMAN, SCARLETT DAMON. How would you update the record in the safest way?",
	"q22": "Q22) The entire category of the movie WEST LION was wrongly inserted. The correct categories are Classics, Family, Children. How would you update the record ensuring no wrong data is left?",
	"q23": " Q23) How many actors acted in films released in 2017?",
	"q24": "Q24) How many Sci-Fi films released between the year 2007 to 2017?",
	"q25": "Q25) Fetch the actors of the movie WESTWARD SEABISCUIT with the city they live in.",
	"q26": "Q26) What is the total length of all movies played in 2008?",
	"q27": "Q27) Which film has the shortest length? In which language and year was it released?",
	"q28": "Q28) How many movies were released each year?",
	"q29": "Q29)  How many languages of movies were released each year?.",
	"q30": "Q30) Which actor did least movies?"

}

@st.experimental_singleton
def init_connection():
    return mysql.connector.connect(**st.secrets["mysql"])

conn = init_connection()

# Fxn Make Execution
@st.experimental_memo(ttl=600)
def sql_executor(query):
    with conn.cursor() as cur:
        cur.execute(query)
        return cur.fetchall()







def main():
	st.title("SQL query executor")

	# menu = ["Home"]
	# choice = st.sidebar.selectbox("Menu", menu)
	tab1, tab2, tab3, tab4 = st.tabs(['About', 'Database Schema', 'SQL Query Execution', 'Insights'])
	# if choice == "Home":
		# st.subheader("HomePage")
	with tab1:
		
		st.subheader("About the database")
		st.markdown(
			'This database is a collection of films, its actors, their address, film description, etc up till the year 2020\n. Our goal here is to perform various operations on the given database with execution of MySQL queries\n. Tables present in this database are \n - actor \n - address \n - category \n - city \n - country \n - film \n - film_actor \n - film_category \n - language'
		)

	with tab2:
		components.iframe(src='https://dbdiagram.io/embed/62d984380d66c746552514e4', height=500, scrolling=False)
	with tab3:
		# Columns/Layout
		col1,col2 = st.columns(2)

		with col1:
			with st.form(key='query_form'):
				raw_code = st.text_area("SQL Code Here")
				submit_code = st.form_submit_button("Execute")
			
		
			
		# Results Layouts
		with col2:
			if submit_code:
				st.info("Query Submitted")
				st.code(raw_code)

				# Results 
				query_results = sql_executor(raw_code)
				with st.expander("Result json"):
					st.write(query_results)

				with st.expander("Result dataframe"):
					query_df = pd.DataFrame(query_results)
					st.dataframe(query_df)

	with tab4:
		st.subheader('Insights')
		with st.expander(questions['q1']):
			st.code(
				'SELECT DISTINCT category.name AS category, COUNT(category.category_id) AS number_of_films \nFROM film_category \nLEFT JOIN film ON film_category.film_id = film.film_id \nINNER JOIN category ON film_category.category_id = category.category_id \nWHERE release_year = 2018 \nGROUP BY category.category_id;' 
			)

		with st.expander(questions['q2']):
			st.code(
				'UPDATE address SET address = "677 Jazz Street" \nWHERE address_id = (SELECT address_id FROM actor WHERE actor_id = 36);'
			)

			st.write('to view changes : ')
			st.code('SELECT actor.first_name, actor.last_name, address.address\nFROM actor\nLEFT JOIN address ON actor.address_id = address.address_id\nWHERE actor.actor_id = 36;')
		
		with st.expander(questions['q3']):
			st.code('INSERT INTO film_actor(actor_id, film_id) VALUES(105, 41), (95, 41);')

		with st.expander(questions['q4']):
			st.code(
				"SELECT DISTINCT film.title\nFROM film\nINNER JOIN film_actor ON film_actor.film_id = film.film_id\nINNER JOIN actor ON actor.actor_id = film_actor.actor_id\nINNER JOIN address ON address.address_id = actor.address_id\nINNER JOIN city ON city.city_id = address.city_id\nINNER JOIN country ON country.country_id = city.country_id\nWHERE country.country = 'India';"
			)

		with st.expander(questions['q5']):
			st.code(
				"SELECT COUNT(actor.actor_id)\nFROM actor\nINNER JOIN address ON address.address_id = actor.address_id\nINNER JOIN city ON city.city_id = address.city_id\nINNER JOIN country on country.country_id = city.country_id\nWHERE country.country = 'United States';"
			)


		with st.expander(questions['q6']):
			st.code(
				'SELECT language.name AS language, film.release_year, COUNT(language.language_id) AS no_of_films\nFROM language\nINNER JOIN film ON film.language_id = language.language_id\nWHERE film.release_year BETWEEN 2001 AND 2010\nGROUP BY language.language_id\nORDER BY film.release_year;'
			)

		with st.expander(questions['q7']):
			st.code(
				"UPDATE film\nSET language_id = (SELECT language_id FROM language WHERE name = 'Mandarin')\nWHERE film_id = 17;"
			)


		with st.expander(questions['q8']):
			st.code(
				"SELECT actor.actor_id, CONCAT(actor.first_name, ' ', actor.last_name), film.title\nFROM film \nINNER JOIN film_actor ON film_actor.film_id = film.film_id\nINNER JOIN actor ON actor.actor_id = film_actor.actor_id\nWHERE film.rating = 'PG';"
			)

		with st.expander(questions['q9']):
			st.code(
				"SELECT release_year as year_with_most_films, COUNT(release_year) AS no_of_films \nFROM film \nGROUP BY release_year\nORDER BY COUNT(release_year) DESC \nLIMIT 1;"
			)

		with st.expander(questions['q10']):
			st.code(
				"SELECT release_year AS year_with_least_films , COUNT(release_year) AS no_of_films\nFROM film\nGROUP BY release_year\nORDER BY COUNT(release_year) \nLIMIT 1;"
			)

		with st.expander(questions['q11']):
			st.code(
				"SELECT * FROM film\nWHERE release_year = 2014\nORDER BY length DESC\nLIMIT 1;"
			)

		with st.expander(questions['q12']):
			st.code(
				"SELECT film.title, language.name\nFROM film\nINNER JOIN language ON language.language_id = film.language_id\nINNER JOIN film_category ON film_category.film_id = film.film_id\nINNER JOIN category ON category.category_id = film_category.category_id \nWHERE category.name = 'Sci-Fi' AND film.rating = 'NC-17'\n"
			)

		with st.expander(questions['q13']):
			st.write('Insert new city : ')
			st.code(
				'INSERT INTO city(city, country_id) VALUES("Florence", (SELECT country_id FROM country WHERE country = "Italy"))'
			)
			st.write('update address :')
			st.code(
				'UPDATE address \nSET address.address = "055,  Piazzale Michelangelo", \naddress.postal_code = "50125" , \naddress.district =  "Rifredi",\naddress.city_id = (SELECT city_id FROM city WHERE city = "FLorence")\nWHERE address_id = (SELECT address_id FROM actor WHERE actor_id = 16);'
			)

		with st.expander(questions['q14']):
			st.code(
				'INSERT INTO film(\ntitle, \ndescription, \nlanguage_id, \noriginal_language_id, \nlength, \nrental_duration,\nrental_rate,\nrating,\nreplacement_cost,\nspecial_features,\nrelease_yea\n) VALUES(\n"No Time to Die",\n"Recruited to rescue a kidnapped scientist, globe-trotting spy James Bond finds himself hot on the trail of a mysterious villain, who\'s armed with a dangerous new technology",\n(SELECT language_id FROM language WHERE name = "English"),\n(SELECT language_id FROM language WHERE name = "English"),\n100,\n6,\n3.99,\n"PG-13",\n20.99,\n"Trailers,Deleted Scenes",\n2020);'
			)

		with st.expander(questions['q15']):
			st.code(
				'INSERT INTO film_category(film_id, category_id) VALUES\n((SELECT film_id FROM film WHERE title = "No Time to Die"),(SELECT category_id FROM category WHERE name = "Action")),\n((SELECT film_id FROM film WHERE title = "No Time to Die"),(SELECT category_id FROM category WHERE name = "Classics")),\n((SELECT film_id FROM film WHERE title = "No Time to Die"),(SELECT category_id FROM category WHERE name = "Drama"))'
			)

		with st.expander(questions['q16']):
			st.code(
				'INSERT INTO film_actor(actor_id, film_id) \nVALUES ((SELECT actor_id FROM actor WHERE first_name = "PENELOPE" AND last_name = \n"GUINESS"), (SELECT film_id FROM film WHERE title = "No Time to Die")), \n((SELECT actor_id FROM actor WHERE first_name = "NICK" AND last_name = "WAHLBERG"), \n(SELECT film_id FROM film WHERE title = "No Time to Die")), \n((SELECT actor_id FROM actor WHERE first_name = "JOE" AND last_name = "SWANK"), (SELECT \nfilm_id FROM film WHERE title = "No Time to Die"));'
			)

		with st.expander(questions['q17']):
			st.code(
				'INSERT INTO category(name) VALUES ("Thriller");\nINSERT INTO film_category(film_id, category_id)\nVALUES ((SELECT film_id FROM film WHERE title = "ANGELS LIFE" ), (SELECT category_id\nFROM category WHERE name = "THriller"));'
			)
			st.write('Check result : ')
			st.code(
				'SELECT film.title, category.name as Category \nFROM film \nINNER JOIN film_category ON film.film_id = film_category.film_id \nINNER JOIN category ON category.category_id = film_category.category_id \nWHERE film.title = "ANGELS LIFE";'
			)

		with st.expander(questions['q18']):
			st.code(
				'SELECT actor.actor_id, CONCAT(actor.first_name, ' ', actor.last_name) AS Actor, COUNT(film_actor.actor_id) AS no_of_films\nFROM actor\nINNER JOIN film_actor ON actor.actor_id = film_actor.actor_id\nGROUP BY film_actor.actor_id\nORDER BY COUNT(film_actor.actor_id) DESC\nLIMIT 1;'
			)

		with st.expander(questions['q19']):
			st.code(
				'DELETE FROM film_actorTE FROM film_actor\n\
WHERE actor_id = (\n\
	SELECT actor_id\n\
	FROM actor\n\
	WHERE actor.first_name = "JOHNNY" AND actor.last_name = "LOLLOBRIGIDA"\n\
) AND film_id = (\n\
	SELECT film_id FROM film\n\
	WHERE title = "GRAIL FRANKENSTEIN"\n\
)\n\
WHERE actor_id = (\n\
	SELECT actor_id\n\
	FROM actor\n\
	WHERE actor.first_name = "JOHNNY" AND actor.last_name = "LOLLOBRIGIDA"\n\
) AND film_id = (\n\
	SELECT film_id FROM film\n\
	WHERE title = "GRAIL FRANKENSTEIN"\n\
);'
			)

		with st.expander(questions['q20']):
			st.code(
				'INSERT INTO film_category(film_id, category_id)\n\
VALUES ((SELECT film_id FROM film WHERE title = "HARPER DYING"),(SELECT category_id FROM \ncategory WHERE name = "comedy")),\n\
((SELECT film_id FROM film WHERE title = "HARPER DYING"),(SELECT category_id FROM \ncategory WHERE name = "drama"));'
			)

		with st.expander(questions['q21']):
			st.write('Step 1 : ')
			st.code(
				'DELETE FROM film_actor\n\
WHERE film_id = (SELECT film_id FROM film WHERE title = "WEST LION")'
			)
			st.write('Step 2 : ')
			st.code(
				'INSERT INTO film_actor(actor_id, film_id)\n\
VALUES ((SELECT actor_id FROM actor WHERE actor.first_name = "DAN" AND actor.last_name = "TORN"),(SELECT film_id FROM film WHERE title = "WEST LION")),\n\
((SELECT actor_id FROM actor WHERE actor.first_name = "MAE" AND actor.last_name = "HOFFMAN"),(SELECT film_id FROM film WHERE title = "WEST LION")),\n\
((SELECT actor_id FROM actor WHERE actor.first_name = "SCARLETT" AND actor.last_name = "DAMON"),(SELECT film_id FROM film WHERE title = "WEST LION"));'
			)

		with st.expander(questions['q22']):
			st.write('Step 1 : ')
			st.code('DELETE FROM film_category\n\
WHERE film_id = (SELECT film_id FROM film WHERE title = "WEST LION");')
			st.write('Step 2 : ')
			st.code(
				'INSERT INTO film_category(film_id, category_id)\n\
VALUES ((SELECT film_id FROM film WHERE title = "WEST LION"),(SELECT category_id FROM\n category WHERE name = "Classics")),\n\
((SELECT film_id FROM film WHERE title = "WEST LION"),(SELECT category_id FROM category WHERE name = "Family")),\n\
((SELECT film_id FROM film WHERE title = "WEST LION"),(SELECT category_id FROM category\n WHERE name = "Children"));'
			)


		with st.expander(questions['q23']):
			st.code(
				'SELECT COUNT(film_actor.actor_id) AS no_of_actors_2017\n\
FROM film_actor\n\
INNER JOIN film ON film_actor.film_id = film.film_id\n\
WHERE film.release_year = 2017'
			)

		with st.expander(questions['q24']):
			st.code(
				'SELECT COUNT(film.film_id) AS SCIFI_betw_2007__2017\n\
FROM category\n\
INNER JOIN film_category ON category.category_id = film_category.category_id\n\
INNER JOIN film ON film_category.film_id = film.film_id\n\
WHERE category.name = "Sci-Fi"  AND film.release_year BETWEEN 2007 AND 2017;'
			)

		with st.expander(questions['q25']):
			st.code(
				'SELECT CONCAT(actor.first_name, " ", actor.last_name) AS actors, city.city \n\
FROM actor\n\
LEFT JOIN address ON actor.address_id = address.address_id\n\
INNER JOIN city ON address.city_id = city.city_id\n\
INNER JOIN film_actor ON actor.actor_id = film_actor.actor_id\n\
WHERE film_actor.film_id = (SELECT film_id FROM film WHERE title = "WESTWARD SEABISCUIT" );'
			)

		with st.expander(questions['q26']):
			st.code(
				'SELECT SUM(length) AS total_length\n\
FROM film\n\
WHERE release_year = 2008'
			)

		with st.expander(questions['q27']):
			st.code(
				'SELECT film.title, film.length, film.release_year, language.name\n\
FROM film\n\
INNER JOIN language ON film.language_id = language.language_id\n\
WHERE film.length = (SELECT MIN(film.length) FROM film );'
			)


		with st.expander(questions['q28']):
			st.code(
				'SELECT release_year, COUNT(*) AS no_of_movies\n\
FROM film\n\
GROUP BY release_year\n\
ORDER BY release_year;'
			)

		with st.expander(questions['q29']):
			st.code(
				'SELECT language.name ,COUNT(film.language_id) AS no_of_films\n\
FROM film\n\
INNER JOIN language ON language.language_id = film.language_id\n\
GROUP BY language.name;'
			)


		with st.expander(questions['q30']):
			st.code(
				'SELECT CONCAT(actor.first_name, " ", actor.last_name) as actor, COUNT(film_actor.actor_id) AS no_of_movies\n\
FROM film_actor\n\
INNER JOIN actor ON film_actor.actor_id = actor.actor_id\n\
GROUP BY film_actor.actor_id\n\
ORDER BY COUNT(film_actor.actor_id)\n\
LIMIT 1;'
			)



if __name__ == '__main__':
	main()
