-- Users Table
CREATE TABLE users (
    user_id UUID NOT NULL,
    username VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT timezone('UTC'::text, now()),
    PRIMARY KEY (user_id)
);

-- Movies Table
CREATE TABLE movies (
    movie_id SERIAL PRIMARY KEY,
    movie_title VARCHAR(255),
    movie_path VARCHAR(255) NOT NULL,
    movie_thumbnail VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC')
);

-- Access Codes Table
CREATE TABLE access_codes (
    code_id VARCHAR(50) PRIMARY KEY,
    movie_id INTEGER REFERENCES movies(movie_id),
    user_id UUID REFERENCES users(user_id),
    created_at TIMESTAMP WITHOUT TIME ZONE DEFAULT (NOW() AT TIME ZONE 'UTC'),
    expires_at TIMESTAMP WITH TIME ZONE
);