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
    SELECT
      tc.constraint_name,
      tc.table_name,
      kcu.column_name,
      ccu.table_name AS foreign_table_name,
      ccu.column_name AS foreign_column_name
    FROM information_schema.table_constraints AS tc
    JOIN information_schema.key_column_usage AS kcu
      ON tc.constraint_name = kcu.constraint_name
      AND tc.table_schema = kcu.table_schema
    JOIN information_schema.constraint_column_usage AS ccu
      ON ccu.constraint_name = tc.constraint_name
      AND ccu.table_schema = tc.table_schema
    WHERE tc.constraint_type = 'FOREIGN KEY'
      AND tc.table_name IN ('test_attempts', 'tests', 'scheduled_tests')
    ORDER BY tc.table_name, tc.constraint_name;
  `);

  console.log(JSON.stringify(result.rows, null, 2));
} catch (error) {
  console.error("DATABASE ERROR:", error.message);
} finally {
  await pool.end();
}
