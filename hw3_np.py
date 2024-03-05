from enum import Enum
import sqlite3

class Director:
    def __init__(self, first_name: str, birth_year: int, last_name: str, birth_place: str):
        self.first_name = first_name
        self.birth_year = birth_year
        self.last_name = last_name
        self.birth_place = birth_place

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.birth_year})"

class Genre(Enum):
    ACTION = "Action"
    SCI_FI = "Sci-Fi"
    DRAMA = "Drama"
    THRILLER = "Thriller"
    ADVENTURE = "Adventure"

class Movie:
    def __init__(self, name: str, year: int, director: Director, rating: float):
        self.name = name
        self.year = year
        self.director = director
        self.rating = rating
        self.genre = set()

    def add_genre(self, *genres: Genre):
        """
        Add one or more genres to the movie.
        """
        self.genre.update(genres)
    
    def print_info(self):
        """
        Pretty-print movie information.
        """
        print("Movie Name:", self.name)
        print("Release Year:", self.year)
        print("Director:", self.director)
        print("Rating:", self.rating)
        print("Genres:", ", ".join(genre.value for genre in self.genre))

# Connect to SQLite database
conn = sqlite3.connect('movies.db')
c = conn.cursor()

# Create a table for movies
c.execute('''CREATE TABLE IF NOT EXISTS movies
             (name TEXT, year INTEGER, director TEXT, rating REAL)''')

# Function to insert a movie into the database
def insert_movie(movie: Movie):
    genres = ', '.join([genre.value for genre in movie.genre])
    c.execute("INSERT INTO movies VALUES (?, ?, ?, ?)",
              (movie.name, movie.year, movie.director.first_name + ' ' + movie.director.last_name, movie.rating))
    conn.commit()

def execute(sqlstr: str = "INSERT INTO movies VALUES (?, ?, ?, ?)", values: tuple = ()):
    c.execute(sqlstr, values)
    conn.commit()

# Example usage
if __name__ == "__main__":
    # Create a director instance
    director = Director("Joel", 1976, "Silver", "South Orange")

    # Create a movie instance
    movie = Movie("The Matrix", 1999, director, 8.7)
    
    # Add genres to the movie
    movie.add_genre(Genre.ACTION, Genre.SCI_FI)
    
    # Insert movie into the database
    insert_movie(movie)

    # Print movie information using the print_info method
    movie.print_info()

# Close the database connection
conn.close()
