-- In this SQL file, write (and comment!) the schema of your database, including the CREATE TABLE, CREATE INDEX, CREATE VIEW, etc. statements that compose it
CREATE TABLE Images (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_path VARCHAR(255) NOT NULL,
    date_taken DATE NOT NULL,
    location VARCHAR(100),
    camera_model VARCHAR(100),
    resolution VARCHAR(20),
    format VARCHAR(50)
);

CREATE TABLE Tags (
    id INT PRIMARY KEY AUTO_INCREMENT,
    tag_name VARCHAR(50) NOT NULL UNIQUE
);

CREATE TABLE Image_Tags (
    image_id INT,
    tag_id INT,
    PRIMARY KEY (image_id, tag_id),
    FOREIGN KEY (image_id) REFERENCES Images(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES Tags(id) ON DELETE CASCADE
);

CREATE TABLE Faces (
    id INT PRIMARY KEY AUTO_INCREMENT,
    image_id INT,
    person_name VARCHAR(100),
    confidence_score FLOAT CHECK (confidence_score >= 0 AND confidence_score <= 1),
    age_estimate INT,
    FOREIGN KEY (image_id) REFERENCES Images(id)
);


-- Index on Images table for quick searches by date_taken
CREATE INDEX idx_date_taken ON Images(date_taken);

-- Index on Images table for quick searches by camera_model
CREATE INDEX idx_camera_model ON Images(camera_model);

-- Index on Tags table for quick searches by tag_name
CREATE INDEX idx_tag_name ON Images(date_taken);

-- Combined index on Image_Tags for lookups by image_id and tag_id
CREATE INDEX idx_image_tags ON Image_Tags(image_id, tag_id);

-- Index on Faces table for quick searches by image_id
CREATE INDEX idx_faces_image_id ON Faces(image_id);

-- Index on Faces table for quick searches by person name
CREATE INDEX idx_person_name ON Faces(person_name);

-- VIEWS --

-- View for all images with Tags
CREATE VIEW images_with_tags AS
SELECT
    i.id AS image_id,
    i.file_path,
    i.date_taken,
    i.location,
    i.camera_model,
    i.resolution,
    i.format,
    GROUP_CONCAT(t.tag_name) AS tags -- Combine multiple tags into a single field
FROM
    Images i
LEFT JOIN
    Image_Tags it ON i.id = it.image_id
LEFT JOIN
    Tags t ON it.tag_id = t.id
GROUP BY
    i.id; -- Group by image ID to avoid duplicates

-- View for Images with Faces Detected --
CREATE VIEW images_with_faces AS
SELECT
    i.id AS image_id,
    i.file_path,
    i.date_taken,
    f.person_name,
    f.confidence_score,
    f.age_estimate
FROM
    Images i
JOIN
    Faces f ON i.id = f.image_id;

-- View for image statistics --
CREATE VIEW image_statistics AS
SELECT
    i.id AS image_id,
    COUNT(f.id) AS face_count,
    AVG(f.confidence_score) AS avg_confidence_score,
    COUNT(it.tag_id) AS tag_count
FROM
    Images i
LEFT JOIN
    Faces f ON i.id = f.image_id
LEFT JOIN
    Image_Tags it ON i.id = it.image_id
GROUP BY
    i.id;
