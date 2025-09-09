-- add_image_columns.sql
-- Добавляет колонку original_image_url в таблицы, если она еще не существует

-- Добавляем колонку в таблицу generated_content
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'generated_content' AND column_name = 'original_image_url'
    ) THEN
        ALTER TABLE generated_content ADD COLUMN original_image_url VARCHAR(500);
    END IF;
END $$;

-- Добавляем колонку в таблицу blog_posts
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1
        FROM information_schema.columns
        WHERE table_name = 'blog_posts' AND column_name = 'original_image_url'
    ) THEN
        ALTER TABLE blog_posts ADD COLUMN original_image_url VARCHAR(500);
    END IF;
END $$;
