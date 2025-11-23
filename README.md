
***

# Movie & TV Show Review Database

## Overview

**SIDRAMA** is a comprehensive MySQL-based system to catalog movies and TV shows, users, reviews, detailed metadata, and advanced analytics. The schema supports core entertainment features similar to IMDb and Letterboxd, enabling users to review movies and episodes, maintain watchlists, follow other users, and perform advanced searches. Multiple real-world enhancements, like genre tagging, watchlists, review likes, and user stats, are included for robust entertainment data management.[1][2][3]

***

## Features

- Rich, normalized entertainment database (Movies, Shows, Episodes, Users, Reviews, Actors, Directors, Genres)[3][1]
- Supports reviews for both movies and TV episodes, with rating aggregation and review text
- Many-to-many relationships for actors, directors, genres with movies and shows
- Watchlists, custom user lists, review likes, and user following
- Automated triggers to update ratings/statistics on insert, update, or delete[2][3]
- Stored procedures for frequent operations: advanced search, insert reviews, fetch statistics, etc.[2][3]
- Sample data covering popular movies, shows, episodes, users, and reviews

***

## Schema Overview

| Table         | Description                                            |
|---------------|-------------------------------------------------------|
| User          | User accounts, profile, login, and metadata[1]      |
| Movie         | Movie details, rating, box office, metadata[1]      |
| TV Show       | Series details, seasons, status, genres[1]          |
| Episode       | Per-episode info for shows[1]                  |
| Review        | User-generated reviews for movies or episodes[1]   |
| Genre         | Movie/show genres[1]                            |
| Actor/Director| Talent with biography and relationships[1]         |
| Link Tables*  | MovieActor, MovieDirector, MovieGenre, ShowGenre      |
| Watchlist     | User watchlists[1]                              |
| UserList      | Custom user lists (e.g., “Favorite Thrillers”)[1]    |
| ListItems     | Contents of user-defined lists[1]               |
| ReviewLikes   | Users “like” reviews[1]                         |
| UserFollowers | Social connections[1]                           |

*All link tables enable many-to-many relationships.

***

## Views, Triggers, and Procedures

- **Views:** Aggregated review details, popular movies, user stats, complete movie/show metadata, recent activity, etc.[3][2]
- **Triggers:** Keep all aggregate ratings, review counts, and constraint checks consistent automatically (e.g., after new reviews)[2][3]
- **Stored Procedures:** For adding reviews, advanced search, filtering by talent or genre, fetching stats, and more[3][2]
- **Functions:** Custom business logic, such as popularity scores and user statistics[2][3]

***

## Setup Instructions

1. **Create Database and Tables:**
   - Run `PES1UG23CS577_table_creation.sql` to create all tables and basic schema.[1]
   - Ensure you use a database named `sidrama`, or edit scripts as needed.

2. **Insert Sample Data:**
   - Execute `PES1UG23CS577_values.sql` to populate with sample genres, movies, shows, users, reviews, and relationships.[3]

3. **Add Advanced Logic:**
   - Apply triggers, views, stored procedures, and functions using `PES1UG23CS577_view_trigger_procedure_functions.sql`.[2]

4. **Order:**
   - Table creation → Data population → Views/Triggers/Procedures/Functions.

***

## Usage Examples

- **Insert a new movie review:**
  ```
  CALL addmoviereview(1, 6, 5.0, 'The Matrix revolutionized action cinema!');
  ```

- **Get reviews by a user:**
  ```
  CALL getuserreviews(1);
  ```

- **Search movies by genre:**
  ```
  CALL searchmoviesbygenre('Action');
  ```

- **Test available views, triggers, and retrieve stats as demonstrated in the sample script comments.**[3]

***

## Notes & Customization

- Passwords used in sample data are placeholder hashes; replace with a secure hash function for real deployments.[3]
- Triggers enforce review constraints and aggregate updates; review all constraints if customizing.[2][3]
- Includes robust test and example queries for validation and demonstration.[3]

***
