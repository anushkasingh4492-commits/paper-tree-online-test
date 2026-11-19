import { pool } from "@/lib/db";

export async function ensureAcademyUsernameSchema() {
  await pool.query(`
    ALTER TABLE admins
    ADD COLUMN IF NOT EXISTS username VARCHAR(80)
  `);
  await pool.query(`
    CREATE UNIQUE INDEX IF NOT EXISTS admins_username_unique
    ON admins (LOWER(username))
    WHERE username IS NOT NULL AND username <> ''
  `);
}
