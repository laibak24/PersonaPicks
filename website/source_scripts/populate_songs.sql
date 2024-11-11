-- Inserting 10 sample songs into the Song table
INSERT INTO your_app_mbtitype (mbti_type_id, mbti_type) VALUES
    (1, 'INTJ'),
    (2, 'INTP'),
    (3, 'ENTJ'),
    (4, 'ENTP'),
    (5, 'INFJ'),
    (6, 'INFP'),
    (7, 'ENFJ'),
    (8, 'ENFP'),
    (9, 'ISTJ'),
    (10, 'ISFJ'),
    (11, 'ESTJ'),
    (12, 'ESFJ'),
    (13, 'ISTP'),
    (14, 'ISFP'),
    (15, 'ESTP'),
    (16, 'ESFP');


INSERT INTO website_song (title, artist, album, release_date, image, first_preference_id, second_preference_id, third_preference_id)
VALUES 
('Blinding Lights', 'The Weeknd', 'After Hours', '2019-11-29', 'song_images/blinding_lights.jpg', 1, 3, 5),  -- INTJ, ENTP, ISFJ
('Shape of You', 'Ed Sheeran', 'Divide', '2017-01-06', 'song_images/shape_of_you.jpg', 2, 6, 4),  -- INFP, ENFJ, ESTJ
('Levitating', 'Dua Lipa', 'Future Nostalgia', '2020-03-27', 'song_images/levitating.jpg', 6, 5, 3),  -- ENFJ, ISFP, INTP
('Bad Guy', 'Billie Eilish', 'When We All Fall Asleep, Where Do We Go?', '2019-03-29', 'song_images/bad_guy.jpg', 3, 7, 8),  -- INTP, ESTJ, ENTP
('Rolling in the Deep', 'Adele', '21', '2010-11-29', 'song_images/rolling_in_the_deep.jpg', 4, 1, 2),  -- ISFJ, INTJ, ESFJ
('Uptown Funk', 'Mark Ronson ft. Bruno Mars', 'Uptown Special', '2014-11-10', 'song_images/uptown_funk.jpg', 8, 2, 4),  -- ENFP, INFP, ESTJ
('Someone Like You', 'Adele', '21', '2011-01-24', 'song_images/someone_like_you.jpg', 1, 4, 5),  -- INTJ, ISFJ, INFP
('Stay', 'The Kid LAROI, Justin Bieber', 'F*ck Love', '2021-07-09', 'song_images/stay.jpg', 3, 5, 7),  -- INTP, ISFP, ENFP
('All of Me', 'John Legend', 'Love in the Future', '2013-08-12', 'song_images/all_of_me.jpg', 2, 4, 8),  -- INFP, ISFJ, ENFP
('Bohemian Rhapsody', 'Queen', 'A Night at the Opera', '1975-11-21', 'song_images/bohemian_rhapsody.jpg', 6, 1, 3);  -- ENFJ, INTJ, INTP
