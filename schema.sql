
 
DROP TABLE IF EXISTS users;
CREATE TABLE users (id SERIAL PRIMARY KEY, username TEXT, password TEXT,access_level TEXT);
 
DROP TABLE IF EXISTS visitors;
CREATE TABLE visitors (id SERIAL PRIMARY KEY, moment TIMESTAMP);

DROP TABLE IF EXISTS topicareas;
CREATE TABLE topicareas (id SERIAL PRIMARY KEY, name TEXT, visible BOOLEAN);

DROP TABLE IF EXISTS topics;
CREATE TABLE topics (id SERIAL PRIMARY KEY, topicarea_id INTEGER REFERENCES topicareas, name TEXT, user_id INTEGER REFERENCES users, visible BOOLEAN);

DROP TABLE IF EXISTS messages;
CREATE TABLE messages (id SERIAL PRIMARY KEY, topics_id INTEGER REFERENCES topics, content TEXT, created_at TIMESTAMP, user_id INTEGER REFERENCES users, visible BOOLEAN);

