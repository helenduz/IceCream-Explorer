DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS reviews;
CREATE TABLE products (
  brand text,
  image_key text,
  product_name text,
  subhead text,
  product_description text,
  rating real,
  rating_count int,
  ingredients text
);
CREATE TABLE reviews (
  brand text,
  image_key text,
  author text,
  review_date date,
  stars real,
  title text,
  helpful_yes real,
  helpful_no real,
  review_text text,
  taste real,
  ingredients real,
  texture real,
  likes text
);