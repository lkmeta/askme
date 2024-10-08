-- Create the pgvector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the faqs table 
CREATE TABLE IF NOT EXISTS faqs (
    id SERIAL PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    -- assuming we use a pgvector with a dimension of 1536 as maximum
    embedding vector(1536)
);

