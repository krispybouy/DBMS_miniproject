import streamlit as st
import mysql.connector
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="SIDRAMA - Movie & TV Review Platform",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #e50914;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #564d4d;
        margin-bottom: 1rem;
    }
    .card {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f0f2f6;
        margin-bottom: 1rem;
    }
    .metric-card {
        text-align: center;
        padding: 1rem;
        border-radius: 0.5rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)

# Database connection function
def get_db_connection():
    """Create and return database connection"""
    try:
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            port=st.secrets["mysql"]["port"]
        )
        return connection
    except Exception as e:
        st.error(f"Database connection error: {e}")
        return None

# Initialize session state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'user_id' not in st.session_state:
    st.session_state.user_id = None
if 'username' not in st.session_state:
    st.session_state.username = None
if 'page' not in st.session_state:
    st.session_state.page = "Home"

# Authentication functions
def login_user(username, password):
    """Authenticate user"""
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT user_id, username, name FROM User WHERE username = %s AND password = %s", 
                      (username, password))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        return user
    return None

def register_user(username, password, name, dob, email, ph_no, address):
    """Register new user"""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                """INSERT INTO User (username, password, name, dob, email, ph_no, address) 
                   VALUES (%s, %s, %s, %s, %s, %s, %s)""",
                (username, password, name, dob, email, ph_no, address)
            )
            conn.commit()
            user_id = cursor.lastrowid
            cursor.close()
            conn.close()
            return user_id
        except mysql.connector.Error as e:
            st.error(f"Registration error: {e}")
            return None
    return None

def logout():
    """Logout user"""
    st.session_state.logged_in = False
    st.session_state.user_id = None
    st.session_state.username = None
    st.session_state.page = "Home"

# Main app
def main():
    # Header
    st.markdown('<h1 class="main-header">🎬 SIDRAMA</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">Your Ultimate Movie & TV Show Review Platform</p>', 
                unsafe_allow_html=True)
    
    # Sidebar navigation
    with st.sidebar:
        st.title("Navigation")
        
        if not st.session_state.logged_in:
            # Login/Register section
            st.subheader("Account")
            auth_choice = st.radio("", ["Login", "Register"], label_visibility="collapsed")
            
            if auth_choice == "Login":
                with st.form("login_form"):
                    st.subheader("Login")
                    username = st.text_input("Username")
                    password = st.text_input("Password", type="password")
                    submit = st.form_submit_button("Login")
                    
                    if submit:
                        user = login_user(username, password)
                        if user:
                            st.session_state.logged_in = True
                            st.session_state.user_id = user['user_id']
                            st.session_state.username = user['username']
                            st.success(f"Welcome back, {user['name']}!")
                            st.rerun()
                        else:
                            st.error("Invalid credentials")
            
            else:  # Register
                with st.form("register_form"):
                    st.subheader("Register")
                    new_username = st.text_input("Username")
                    new_password = st.text_input("Password", type="password")
                    name = st.text_input("Full Name")
                    dob = st.date_input("Date of Birth", min_value=datetime(1900, 1, 1))
                    email = st.text_input("Email")
                    ph_no = st.text_input("Phone Number")
                    address = st.text_area("Address")
                    submit = st.form_submit_button("Register")
                    
                    if submit:
                        if new_username and new_password and name and email:
                            user_id = register_user(new_username, new_password, name, dob, email, ph_no, address)
                            if user_id:
                                st.success("Registration successful! Please login.")
                            else:
                                st.error("Registration failed. Username or email may already exist.")
                        else:
                            st.error("Please fill in all required fields")
        
        else:
            # Logged in navigation
            st.success(f"👤 {st.session_state.username}")
            if st.button("Logout", use_container_width=True):
                logout()
                st.rerun()
            
            st.divider()
            
            # Navigation menu
            pages = {
                "🏠 Home": "Home",
                "🎬 Movies": "Movies",
                "📺 TV Shows": "TV Shows",
                "⭐ My Reviews": "My Reviews",
                "🔍 Search": "Search",
                "📊 Statistics": "Statistics",
                "👤 Profile": "Profile"
            }
            
            for label, page in pages.items():
                if st.button(label, use_container_width=True):
                    st.session_state.page = page
                    st.rerun()
    
    # Main content area
    if not st.session_state.logged_in:
        show_home_page()
    else:
        if st.session_state.page == "Home":
            show_home_page()
        elif st.session_state.page == "Movies":
            show_movies_page()
        elif st.session_state.page == "TV Shows":
            show_tvshows_page()
        elif st.session_state.page == "My Reviews":
            show_my_reviews_page()
        elif st.session_state.page == "Search":
            show_search_page()
        elif st.session_state.page == "Statistics":
            show_statistics_page()
        elif st.session_state.page == "Profile":
            show_profile_page()

def show_home_page():
    """Display home page with popular movies and shows"""
    st.header("🎬 Welcome to SIDRAMA")
    
    if st.session_state.logged_in:
        st.write(f"Hello, **{st.session_state.username}**! Explore movies and TV shows below.")
    else:
        st.info("Please login or register to start reviewing movies and TV shows!")
    
    # Display popular movies using view
    st.subheader("🔥 Popular Movies")
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, pm.avg_rating, pm.total_reviews 
            FROM popular_movies pm
            JOIN Movie m ON pm.movie_id = m.movie_id
            LIMIT 6
        """)
        movies = cursor.fetchall()
        
        if movies:
            cols = st.columns(3)
            for idx, movie in enumerate(movies):
                with cols[idx % 3]:
                    # Display poster image
                    if movie.get('poster_url'):
                        try:
                            st.image(movie['poster_url'], use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    
                    st.markdown(f"### {movie['name']}")
                    st.write(f"⭐ Rating: {movie['avg_rating']:.2f}/5.0")
                    st.write(f"📝 {movie['total_reviews']} reviews")
                    st.write(f"🗓️ {movie['release_date']}")
                    st.write(f"🌐 {movie['language']}")
        cursor.close()
        conn.close()
    
    st.divider()
    
    # Display top rated shows
    st.subheader("📺 Top Rated TV Shows")
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM tvshow ORDER BY ratings DESC LIMIT 4")
        shows = cursor.fetchall()
        
        if shows:
            cols = st.columns(2)
            for idx, show in enumerate(shows):
                with cols[idx % 2]:
                    # Display show poster
                    if show.get('poster_url'):
                        try:
                            st.image(show['poster_url'], use_container_width=True)
                        except:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    else:
                        st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    
                    st.markdown(f"### {show['name']}")
                    st.write(f"⭐ Rating: {show['ratings']:.2f}/5.0")
                    st.write(f"📺 {show['num_of_seasons']} seasons, {show['num_of_episodes']} episodes")
        cursor.close()
        conn.close()

def show_movies_page():
    """Display movies page"""
    st.header("🎬 Movies")
    
    # Search and filter
    col1, col2, col3 = st.columns([2, 1, 1])
    with col1:
        search_term = st.text_input("🔍 Search movies", placeholder="Enter movie name...")
    with col2:
        # Get genres
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM Genre ORDER BY name")
            genres = [g[0] for g in cursor.fetchall()]
            cursor.close()
            conn.close()
            genre_filter = st.selectbox("Genre", ["All"] + genres)
    with col3:
        min_rating = st.slider("Min Rating", 0.0, 5.0, 0.0, 0.5)
    
    # Fetch movies using direct query
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Build query dynamically - include all necessary fields and genres
        query = """
            SELECT DISTINCT
                m.movie_id,
                m.name,
                m.release_date,
                m.ratings,
                m.language,
                m.poster_url,
                m.descr,
                m.total_duration,
                m.age_rating,
                m.box_office,
                GROUP_CONCAT(DISTINCT g.name ORDER BY g.name SEPARATOR ', ') as genres
            FROM Movie m
            LEFT JOIN Movie_Genre mg ON m.movie_id = mg.movie_id
            LEFT JOIN Genre g ON mg.genre_id = g.genre_id
            WHERE 1=1
        """
        params = []
        
        if search_term:
            query += " AND m.name LIKE %s"
            params.append(f"%{search_term}%")
        
        if genre_filter and genre_filter != "All":
            query += " AND g.name = %s"
            params.append(genre_filter)
        
        if min_rating > 0:
            query += " AND m.ratings >= %s"
            params.append(min_rating)
        
        query += " GROUP BY m.movie_id, m.name, m.release_date, m.ratings, m.language, m.poster_url, m.descr, m.total_duration, m.age_rating, m.box_office"
        query += " ORDER BY m.ratings DESC, m.release_date DESC LIMIT 50"
        
        cursor.execute(query, params)
        movies = cursor.fetchall()
        
        if movies:
            for movie in movies:
                # Create expander title with genres
                genres_display = f" | {movie['genres']}" if movie.get('genres') else ""
                expander_title = f"**{movie['name']}** ⭐ {movie['ratings']:.2f}{genres_display}"
                
                with st.expander(expander_title, expanded=False):
                    # Create two columns: poster on left, details on right
                    col_poster, col_details = st.columns([1, 2])
                    
                    with col_poster:
                        # Display movie poster
                        if movie.get('poster_url'):
                            try:
                                st.image(movie['poster_url'], use_container_width=True)
                            except:
                                st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    
                    with col_details:
                        # Movie details section
                        st.markdown(f"### {movie['name']}")
                        
                        # Genres with badges (using markdown)
                        if movie.get('genres'):
                            genres_list = movie['genres'].split(', ')
                            genres_badges = ' '.join([f'`{genre}`' for genre in genres_list])
                            st.markdown(f"**Genres:** {genres_badges}")
                        
                        # Description - prominently displayed
                        if movie.get('descr'):
                            st.markdown(f"**Synopsis:**")
                            st.info(movie['descr'])
                        
                        # Other details in columns
                        detail_col1, detail_col2 = st.columns(2)
                        
                        with detail_col1:
                            st.write(f"📅 **Release:** {movie['release_date']}")
                            st.write(f"🌐 **Language:** {movie['language']}")
                            st.write(f"🔞 **Age Rating:** {movie['age_rating']}")
                        
                        with detail_col2:
                            if movie.get('total_duration'):
                                st.write(f"⏱️ **Duration:** {movie['total_duration']} min")
                            if movie.get('box_office'):
                                st.write(f"💰 **Box Office:** ${movie['box_office']:,}")
                            st.write(f"⭐ **Rating:** {movie['ratings']:.2f}/5.0")
                        
                        # Get directors from view
                        cursor.execute("SELECT directors FROM movie_details_view WHERE movie_id = %s", (movie['movie_id'],))
                        details = cursor.fetchone()
                        if details and details.get('directors'):
                            st.write(f"🎬 **Directors:** {details['directors']}")
                        
                        # Review button
                        st.divider()
                        col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
                        with col_btn2:
                            if st.button(f"✍️ Write a Review", key=f"review_movie_{movie['movie_id']}", use_container_width=True):
                                st.session_state.reviewing_movie = movie['movie_id']
                                st.session_state.reviewing_movie_name = movie['name']
                                st.rerun()
                    
                    # Show recent reviews (full width below)
                    cursor.execute("""
                        SELECT * FROM movie_reviews_view 
                        WHERE movie_name = %s 
                        ORDER BY review_date DESC 
                        LIMIT 5
                    """, (movie['name'],))
                    reviews = cursor.fetchall()
                    
                    if reviews:
                        st.divider()
                        st.markdown("### 💬 Recent Reviews")
                        for review in reviews:
                            with st.container():
                                col_review1, col_review2 = st.columns([4, 1])
                                with col_review1:
                                    st.markdown(f"**{review['username']}** - {review['review_date']}")
                                    st.write(review['review_text'])
                                with col_review2:
                                    st.metric("Rating", f"{review['rating']:.1f}/5")
                                st.caption("---")
                    else:
                        st.divider()
                        st.info("No reviews yet. Be the first to review this movie!")
        else:
            st.info("No movies found matching your criteria.")
        
        cursor.close()
        conn.close()
    
    # Review form
    if 'reviewing_movie' in st.session_state and st.session_state.reviewing_movie:
        st.divider()
        st.markdown(f"## ✍️ Write a Review for: {st.session_state.reviewing_movie_name}")
        
        with st.form("movie_review_form"):
            rating = st.slider("Your Rating ⭐", 0.0, 5.0, 3.0, 0.5)
            review_text = st.text_area("Your Review", height=150, 
                                       placeholder="Share your thoughts about this movie... What did you like? What could be better?")
            
            col1, col2, col3 = st.columns([1, 1, 3])
            with col1:
                submit = st.form_submit_button("Submit Review", use_container_width=True)
            with col2:
                cancel = st.form_submit_button("Cancel", use_container_width=True)
            
            if submit:
                if not review_text.strip():
                    st.error("Please write a review before submitting!")
                else:
                    # Direct INSERT instead of stored procedure
                    conn = get_db_connection()
                    if conn:
                        cursor = conn.cursor()
                        try:
                            # Check if user already reviewed this movie
                            cursor.execute("""
                                SELECT review_id FROM Review 
                                WHERE user_id = %s AND movie_id = %s
                            """, (st.session_state.user_id, st.session_state.reviewing_movie))
                            
                            existing_review = cursor.fetchone()
                            
                            if existing_review:
                                st.error("You have already reviewed this movie!")
                            else:
                                # Insert the review (trigger will auto-update movie rating)
                                cursor.execute("""
                                    INSERT INTO Review (user_id, movie_id, date, rating, review_text)
                                    VALUES (%s, %s, CURDATE(), %s, %s)
                                """, (
                                    st.session_state.user_id,
                                    st.session_state.reviewing_movie,
                                    rating,
                                    review_text
                                ))
                                conn.commit()
                                st.success("✅ Review submitted successfully! Movie rating updated automatically.")
                                del st.session_state.reviewing_movie
                                del st.session_state.reviewing_movie_name
                                cursor.close()
                                conn.close()
                                st.rerun()
                        except mysql.connector.Error as e:
                            st.error(f"❌ Error submitting review: {e}")
                            conn.rollback()
                            cursor.close()
                            conn.close()
            
            if cancel:
                del st.session_state.reviewing_movie
                del st.session_state.reviewing_movie_name
                st.rerun()


def show_tvshows_page():
    """Display TV shows page"""
    st.header("📺 TV Shows")
    
    # Fetch TV shows
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT s.*, GROUP_CONCAT(DISTINCT g.name SEPARATOR ', ') as genres
            FROM tvshow s
            LEFT JOIN Show_Genre sg ON s.show_id = sg.show_id
            LEFT JOIN Genre g ON sg.genre_id = g.genre_id
            GROUP BY s.show_id
            ORDER BY s.ratings DESC
        """)
        shows = cursor.fetchall()
        
        if shows:
            for show in shows:
                with st.expander(f"**{show['name']}** ⭐ {show['ratings']:.2f}", expanded=False):
                    # Create two columns: poster on left, details on right
                    col_poster, col_details = st.columns([1, 2])
                    
                    with col_poster:
                        # Display show poster
                        if show.get('poster_url'):
                            try:
                                st.image(show['poster_url'], use_container_width=True)
                            except:
                                st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                    
                    with col_details:
                        col1, col2 = st.columns([3, 1])
                        
                        with col1:
                            st.write(f"**Seasons:** {show['num_of_seasons']} | **Episodes:** {show['num_of_episodes']}")
                            st.write(f"**Release Date:** {show['release_date']}")
                            st.write(f"**Language:** {show['language']}")
                            st.write(f"**Status:** {show['status']}")
                            st.write(f"**Age Rating:** {show['age_rating']}")
                            
                            if show['genres']:
                                st.write(f"**Genres:** {show['genres']}")
                            if show['descr']:
                                st.write(f"**Description:** {show['descr']}")
                        
                        with col2:
                            if st.button("📺 View Episodes", key=f"view_episodes_{show['show_id']}", use_container_width=True):
                                st.session_state.viewing_show = show['show_id']
                                st.session_state.viewing_show_name = show['name']
                                st.rerun()
                    
                    # Show episode reviews (full width below)
                    cursor.execute("""
                        SELECT * FROM episode_reviews_view 
                        WHERE show_name = %s 
                        ORDER BY review_date DESC LIMIT 3
                    """, (show['name'],))
                    reviews = cursor.fetchall()
                    if reviews:
                        st.divider()
                        st.write("**Recent Episode Reviews:**")
                        for review in reviews:
                            st.caption(f"⭐ {review['rating']}/5 - S{review['season_number']}E{review['episode_no']} - **{review['username']}**: {review['review_text'][:100]}...")
        
        cursor.close()
        conn.close()
    
    # Episode list and review
    if 'viewing_show' in st.session_state and st.session_state.viewing_show:
        st.divider()
        st.subheader(f"Episodes: {st.session_state.viewing_show_name}")
        
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
                SELECT * FROM Episode 
                WHERE show_id = %s 
                ORDER BY season_number, episode_no
            """, (st.session_state.viewing_show,))
            episodes = cursor.fetchall()
            
            if episodes:
                for episode in episodes:
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        with col1:
                            st.write(f"**S{episode['season_number']}E{episode['episode_no']}** - {episode['title'] if episode['title'] else 'Episode ' + str(episode['episode_no'])}")
                            if episode['ep_descr']:
                                st.caption(episode['ep_descr'])
                        with col2:
                            st.caption(f"⏱️ {episode['duration']} min")
                            if episode['air_date']:
                                st.caption(f"📅 {episode['air_date']}")
                        with col3:
                            if st.button("✍️ Review", key=f"review_ep_{episode['episode_id']}", use_container_width=True):
                                st.session_state.reviewing_episode = episode['episode_id']
                                st.session_state.reviewing_episode_name = f"S{episode['season_number']}E{episode['episode_no']}"
                                st.rerun()
                        st.divider()
            
            cursor.close()
            conn.close()
        
        if st.button("← Back to Shows", use_container_width=False):
            del st.session_state.viewing_show
            del st.session_state.viewing_show_name
            st.rerun()
    
    # Episode review form (keep the same as before)
    if 'reviewing_episode' in st.session_state and st.session_state.reviewing_episode:
        st.divider()
        st.subheader(f"Review Episode: {st.session_state.viewing_show_name} - {st.session_state.reviewing_episode_name}")
        
        with st.form("episode_review_form"):
            rating = st.slider("Rating", 0.0, 5.0, 3.0, 0.5)
            review_text = st.text_area("Your Review", height=150, placeholder="Share your thoughts about this episode...")
            col1, col2 = st.columns([1, 5])
            with col1:
                submit = st.form_submit_button("Submit Review")
            with col2:
                cancel = st.form_submit_button("Cancel")
            
            if submit:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor()
                    try:
                        cursor.execute("""
                            INSERT INTO Review (user_id, episode_id, date, rating, review_text)
                            VALUES (%s, %s, CURDATE(), %s, %s)
                        """, (st.session_state.user_id, st.session_state.reviewing_episode, rating, review_text))
                        conn.commit()
                        st.success("✅ Review submitted successfully!")
                        del st.session_state.reviewing_episode
                        del st.session_state.reviewing_episode_name
                        cursor.close()
                        conn.close()
                        st.rerun()
                    except mysql.connector.Error as e:
                        st.error(f"❌ Error: {e}")
                        cursor.close()
                        conn.close()
            
            if cancel:
                del st.session_state.reviewing_episode
                del st.session_state.reviewing_episode_name
                st.rerun()

def show_my_reviews_page():
    """Display user's reviews using stored procedure"""
    st.header("⭐ My Reviews")
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # Use stored procedure to get user reviews
        cursor.callproc('get_user_reviews', [st.session_state.user_id])
        
        reviews = []
        for result in cursor.stored_results():
            reviews = result.fetchall()
        
        if reviews:
            st.write(f"**Total Reviews:** {len(reviews)}")
            
            for review in reviews:
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    with col1:
                        st.write(f"**{review['content_name']}** ({review['content_type']})")
                        st.caption(review['review_text'])
                    with col2:
                        st.metric("Rating", f"{review['rating']:.1f}/5")
                    with col3:
                        st.caption(f"📅 {review['date']}")
                    st.divider()
        else:
            st.info("You haven't written any reviews yet. Start exploring movies and TV shows!")
        
        cursor.close()
        conn.close()

def show_search_page():
    """Advanced search page"""
    st.header("🔍 Advanced Search")
    
    tab1, tab2, tab3 = st.tabs(["By Genre", "By Director", "By Actor"])
    
    with tab1:
        st.subheader("Search Movies by Genre")
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            cursor.execute("SELECT name FROM Genre ORDER BY name")
            genres = [g[0] for g in cursor.fetchall()]
            cursor.close()
            conn.close()
            
            selected_genre = st.selectbox("Select Genre", genres)
            
            if st.button("Search by Genre"):
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    cursor.callproc('search_movies_by_genre', [selected_genre])
                    
                    movies = []
                    for result in cursor.stored_results():
                        movies = result.fetchall()
                    
                    if movies:
                        st.write(f"**Found {len(movies)} movies in {selected_genre}:**")
                        for movie in movies:
                            st.write(f"- **{movie['name']}** ({movie['release_date']}) ⭐ {movie['ratings']:.2f}")
                    else:
                        st.info("No movies found.")
                    
                    cursor.close()
                    conn.close()
    
    with tab2:
        st.subheader("Search Movies by Director")
        director_name = st.text_input("Enter Director Name")
        
        if st.button("Search by Director"):
            if director_name:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    cursor.callproc('get_movies_by_director', [director_name])
                    
                    movies = []
                    for result in cursor.stored_results():
                        movies = result.fetchall()
                    
                    if movies:
                        st.write(f"**Found {len(movies)} movies:**")
                        for movie in movies:
                            st.write(f"- **{movie['name']}** ({movie['release_date']}) ⭐ {movie['ratings']:.2f}")
                            st.caption(f"Director: {movie['director_name']}")
                    else:
                        st.info("No movies found for this director.")
                    
                    cursor.close()
                    conn.close()
    
    with tab3:
        st.subheader("Search Movies by Actor")
        actor_name = st.text_input("Enter Actor Name")
        
        if st.button("Search by Actor"):
            if actor_name:
                conn = get_db_connection()
                if conn:
                    cursor = conn.cursor(dictionary=True)
                    cursor.callproc('get_movies_by_actor', [actor_name])
                    
                    movies = []
                    for result in cursor.stored_results():
                        movies = result.fetchall()
                    
                    if movies:
                        st.write(f"**Found {len(movies)} movies:**")
                        for movie in movies:
                            st.write(f"- **{movie['name']}** ({movie['release_date']}) ⭐ {movie['ratings']:.2f}")
                            st.caption(f"Actor: {movie['actor_name']}")
                    else:
                        st.info("No movies found for this actor.")
                    
                    cursor.close()
                    conn.close()
def show_statistics_page():
    """Display statistics using views and functions"""
    st.header("📊 Statistics & Analytics")
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        
        # User statistics from view
        cursor.execute("SELECT * FROM user_stats_view WHERE user_id = %s", (st.session_state.user_id,))
        user_stats = cursor.fetchone()
        
        if user_stats:
            st.subheader("Your Activity")
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Reviews", user_stats['total_reviews'])
            with col2:
                avg_rating = user_stats['avg_rating_given']
                st.metric("Avg Rating Given", f"{avg_rating:.2f}" if avg_rating else "N/A")
            with col3:
                st.metric("Movies Reviewed", user_stats['movies_reviewed'])
            with col4:
                st.metric("Episodes Reviewed", user_stats['episodes_reviewed'])
        else:
            st.info("Start reviewing movies and shows to see your statistics!")
        
        st.divider()
        
        # Detailed stats using functions
        st.subheader("Detailed Stats")
        col1, col2 = st.columns(2)
        
        with col1:
            try:
                cursor.execute("SELECT get_user_avg_rating(%s) as avg_rating", (st.session_state.user_id,))
                result = cursor.fetchone()
                st.info(f"📊 **Average Rating (Function):** {result['avg_rating']:.2f}/5.0")
            except:
                st.info("📊 **Average Rating (Function):** N/A")
            
            try:
                cursor.execute("SELECT count_user_reviews(%s) as review_count", (st.session_state.user_id,))
                result = cursor.fetchone()
                st.info(f"📝 **Total Review Count (Function):** {result['review_count']}")
            except:
                st.info("📝 **Total Review Count (Function):** 0")
        
        with col2:
            try:
                cursor.execute("SELECT count_movies_reviewed(%s) as movie_count", (st.session_state.user_id,))
                result = cursor.fetchone()
                st.info(f"🎬 **Movies Reviewed (Function):** {result['movie_count']}")
            except:
                st.info("🎬 **Movies Reviewed (Function):** 0")
        
        st.divider()
        
        # Platform statistics
        st.subheader("Platform Statistics")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Top Rated Movies**")
            try:
                # Use correct column names from popular_movies view
                cursor.execute("""
                    SELECT name, avg_rating, total_reviews 
                    FROM popular_movies 
                    LIMIT 5
                """)
                top_movies = cursor.fetchall()
                if top_movies:
                    for movie in top_movies:
                        st.write(f"⭐ **{movie['name']}** - {movie['avg_rating']:.2f} ({movie['total_reviews']} reviews)")
                else:
                    st.info("No movies with reviews yet.")
            except Exception as e:
                st.error(f"Error loading movies: {e}")
        
        with col2:
            st.write("**Top Rated Shows**")
            try:
                # Query directly for shows
                cursor.execute("""
                    SELECT s.name, s.ratings, COUNT(DISTINCT r.review_id) as total_reviews
                    FROM tvshow s
                    LEFT JOIN Episode e ON s.show_id = e.show_id
                    LEFT JOIN Review r ON e.episode_id = r.episode_id
                    GROUP BY s.show_id, s.name, s.ratings
                    HAVING total_reviews > 0
                    ORDER BY s.ratings DESC
                    LIMIT 5
                """)
                top_shows = cursor.fetchall()
                if top_shows:
                    for show in top_shows:
                        st.write(f"⭐ **{show['name']}** - {show['ratings']:.2f} ({show['total_reviews']} reviews)")
                else:
                    st.info("No shows with reviews yet.")
            except Exception as e:
                st.error(f"Error loading shows: {e}")
        
        cursor.close()
        conn.close()


def show_profile_page():
    """Display and edit user profile"""
    st.header("👤 My Profile")
    
    conn = get_db_connection()
    if conn:
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM User WHERE user_id = %s", (st.session_state.user_id,))
        user = cursor.fetchone()
        
        if user:
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader("Profile Information")
                st.write(f"**Username:** {user['username']}")
                st.write(f"**Name:** {user['name']}")
                st.write(f"**Email:** {user['email']}")
                st.write(f"**Phone:** {user['ph_no']}")
                st.write(f"**Date of Birth:** {user['dob']}")
                st.write(f"**Address:** {user['address']}")
            
            with col2:
                st.subheader("Account Statistics")
                
                # Use functions to display stats
                cursor.execute("SELECT get_user_avg_rating(%s) as avg_rating", (st.session_state.user_id,))
                avg_rating = cursor.fetchone()['avg_rating']
                
                cursor.execute("SELECT count_user_reviews(%s) as total_reviews", (st.session_state.user_id,))
                total_reviews = cursor.fetchone()['total_reviews']
                
                cursor.execute("SELECT count_movies_reviewed(%s) as movies_reviewed", (st.session_state.user_id,))
                movies_reviewed = cursor.fetchone()['movies_reviewed']
                
                st.metric("Average Rating Given", f"{avg_rating:.2f}/5.0")
                st.metric("Total Reviews", total_reviews)
                st.metric("Movies Reviewed", movies_reviewed)
                st.metric("Episodes Reviewed", total_reviews - movies_reviewed)
        
        cursor.close()
        conn.close()

if __name__ == "__main__":
    main()
