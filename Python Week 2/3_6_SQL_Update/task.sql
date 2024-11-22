CREATE TABLE IF NOT EXISTS tasks (
    id SERIAL PRIMARY KEY,
    task_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL DEFAULT 'pending',
    worker_id INTEGER,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE OR REPLACE FUNCTION fetch_task(p_worker_id INTEGER)
RETURNS INTEGER AS $$
DECLARE
    task_id INTEGER;
BEGIN
    SELECT id INTO task_id
    FROM tasks
    WHERE status = 'pending'
    ORDER BY created_at
    FOR UPDATE SKIP LOCKED
    LIMIT 1;

    IF task_id IS NOT NULL THEN
        UPDATE tasks
        SET status = 'processing', worker_id = p_worker_id, updated_at = CURRENT_TIMESTAMP
        WHERE id = task_id;

        RETURN task_id;
    ELSE
        RETURN NULL;
    END IF;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION complete_task(p_task_id INTEGER)
RETURNS BOOLEAN AS $$
DECLARE
    current_status VARCHAR(50);
BEGIN
    SELECT status INTO current_status
    FROM tasks
    WHERE id = p_task_id;

    IF current_status = 'processing' THEN
        UPDATE tasks
        SET status = 'completed', updated_at = CURRENT_TIMESTAMP
        WHERE id = p_task_id;

        RETURN TRUE;
    ELSE
        RETURN FALSE;
    END IF;
END;
$$ LANGUAGE plpgsql;