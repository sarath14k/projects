-- In this SQL file, write (and comment!) the typical SQL queries users will run on your database

-- TABLE INSERTS --

-- Images table--
INSERT INTO Images (file_path, date_taken, location, camera_model, resolution, format) VALUES
('images/sunset.jpg', '2023-10-10', 'Goa', 'Nikon D750', '1920x1080', 'JPEG'),
('images/urban.jpg', '2023-09-20', 'Mumbai', 'Canon EOS R', '1920x1080', 'JPEG'),
('images/mountain.jpg', '2023-08-15', 'Himachal Pradesh', 'Sony A7 III', '3840x2160', 'PNG'),
('images/portrait.jpg', '2023-07-05', 'Delhi', 'Fujifilm X-T4', '1920x1080', 'JPEG'),
('images/beach.jpg', '2023-09-25', 'Kochi', 'Olympus OM-D E-M1', '1920x1080', 'JPEG'),
('images/forest.jpg', '2023-06-30', 'Karnataka', 'Canon EOS 90D', '1920x1080', 'JPEG'),
('images/cityscape.jpg', '2023-09-15', 'Bangalore', 'Nikon Z6', '1920x1080', 'JPEG'),
('images/temple.jpg', '2023-08-20', 'Varanasi', 'Sony A6400', '1920x1080', 'JPEG'),
('images/festival.jpg', '2023-10-02', 'Jaipur', 'Canon EOS R5', '1920x1080', 'JPEG'),
('images/rural.jpg', '2023-07-12', 'Punjab', 'Nikon D850', '1920x1080', 'JPEG');

-- Tags table --
INSERT INTO Tags (tag_name) VALUES
('sunset'),
('urban'),
('mountain'),
('portrait'),
('beach'),
('forest'),
('cityscape'),
('temple'),
('festival'),
('rural');

-- Image_Tags Table --
INSERT INTO Image_Tags (image_id, tag_id) VALUES
(1, 1),  -- sunset.jpg tagged as sunset
(2, 2),  -- urban.jpg tagged as urban
(3, 3),  -- mountain.jpg tagged as mountain
(4, 4),  -- portrait.jpg tagged as portrait
(5, 5),  -- beach.jpg tagged as beach
(6, 6),  -- forest.jpg tagged as forest
(7, 2),  -- cityscape.jpg tagged as urban
(8, 8),  -- temple.jpg tagged as temple
(9, 9),  -- festival.jpg tagged as festival
(10, 10); -- rural.jpg tagged as rural

-- Faces Table --
INSERT INTO Faces (image_id, person_name, confidence_score, age_estimate) VALUES
(1, 'Sarath Kumar', 0.95, 28),
(2, 'Anita Sharma', 0.90, 35),
(3, 'Rahul Singh', 0.88, 30),
(4, 'Sneha Patel', 0.85, 25),
(5, 'Ajay Verma', 0.92, 40),
(6, 'Pooja Joshi', 0.89, 32),
(7, 'Vikram Mehta', 0.93, 27),
(8, 'Neha Gupta', 0.91, 29),
(9, 'Sunil Desai', 0.86, 33),
(10, 'Geeta Rani', 0.87, 36);

-- SELECT --

-- Select all tags
SELECT * FROM Tags;

-- Select a specific tag by name
SELECT * FROM Tags
WHERE tag_name = 'portrait';

-- Select tags starting with a specific letter
SELECT * FROM Tags
WHERE tag_name LIKE 's%';

-- Select all images
SELECT * FROM Images;

-- Select images taken in a specific location
SELECT * FROM Images
WHERE location = 'Goa';

-- Select images with a specific camera model
SELECT * FROM Images
WHERE camera_model = 'Canon EOS R';

-- Select all image-tag associations
SELECT * FROM Image_Tags;

-- Select tags for a specific image
SELECT t.tag_name FROM Tags t
JOIN Image_Tags it ON t.id = it.tag_id
WHERE it.image_id = (SELECT id FROM Images WHERE location = 'Goa');

-- Select all faces detected in images
SELECT * FROM Faces;

-- Select faces with a specific confidence score
SELECT * FROM Faces
WHERE confidence_score > 0.90;

-- Select faces associated with a specific image
SELECT * FROM Faces
WHERE image_id = (SELECT id FROM Images WHERE location = 'Delhi');


-- UPDATE --
-- Update the camera model of the image taken in Goa
UPDATE Images
SET camera_model = 'Nikon D850'
WHERE location = 'Goa';

-- Update the resolution of the image taken in Mumbai
UPDATE Images
SET resolution = '2560x1440'
WHERE location = 'Mumbai';

-- Update the date_taken of the image taken in Himachal Pradesh
UPDATE Images
SET date_taken = '2023-08-10'
WHERE location = 'Himachal Pradesh';


-- Change the tag name from 'urban' to 'city'
UPDATE Tags
SET tag_name = 'city'
WHERE tag_name = 'urban';

-- Add a new tag for 'nature'
INSERT INTO Tags (tag_name) VALUES ('nature');

-- Update the tag name for 'festival'
UPDATE Tags
SET tag_name = 'celebration'
WHERE tag_name = 'festival';


-- Change the tag for the image taken in Goa
UPDATE Image_Tags
SET tag_id = (SELECT id FROM Tags WHERE tag_name = 'nature')
WHERE image_id = 1 AND tag_id = (SELECT id FROM Tags WHERE tag_name = 'sunset');


-- Update confidence score for a specific person in an image
UPDATE Faces
SET confidence_score = 0.96
WHERE person_name = 'Ravi Kumar';

-- Update age estimate for a specific individual
UPDATE Faces
SET age_estimate = 30
WHERE person_name = 'Sneha Patel';

-- DELETE --

-- Delete the image taken in Kochi
DELETE FROM Images
WHERE location = 'Kochi';

-- Delete images with a specific format
DELETE FROM Images
WHERE format = 'PNG';


-- Delete the 'nature' tag
DELETE FROM Tags
WHERE tag_name = 'nature';

-- Delete the 'city' tag
DELETE FROM Tags
WHERE tag_name = 'city';


-- Remove the tag association for a specific image
DELETE FROM Image_Tags
WHERE image_id = 1 AND tag_id = (SELECT id FROM Tags WHERE tag_name = 'sunset');


-- Delete a face record by person name
DELETE FROM Faces
WHERE person_name = 'Ajay Verma';

-- Delete face records associated with a specific image
DELETE FROM Faces
WHERE image_id = (SELECT id FROM Images WHERE location = 'Delhi');
