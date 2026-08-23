import pg from "pg";
import fs from "fs";

const env = fs.readFileSync(".env.local", "utf8");
const line = env.split("\n").find(x => x.startsWith("DATABASE_URL="));

const DATABASE_URL = line
  .split("=")
  .slice(1)
  .join("=")
  .trim()
  .replace(/^"|"$/g, "");

const pool = new pg.Pool({
  connectionString: DATABASE_URL,
  ssl: { rejectUnauthorized: false },
  connectionTimeoutMillis: 10000,
});

try {
  const result = await pool.query(`
    SELECT pg_get_constraintdef(oid) AS definition
    FROM pg_constraint
    WHERE conname = 'test_attempts_status_check'
  `);

  console.log(JSON.stringify(result.rows, null, 2));
} catch (error) {
  console.error("DATABASE ERROR:", error.message);
} finally {
  await pool.end();
}
