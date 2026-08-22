const fs = require("fs");
const { neon } = require("@neondatabase/serverless");

const sql = neon(process.env.DATABASE_URL);

async function main() {
  const file = fs.readFileSync(
    "drizzle/0000_wild_ted_forrester.sql",
    "utf8"
  );

  const statements = file
    .split("--> statement-breakpoint")
    .map((s) => s.trim())
    .filter(Boolean);

  console.log(`Found ${statements.length} SQL statements.`);

  for (let i = 0; i < statements.length; i++) {
    console.log(`Running ${i + 1}/${statements.length}...`);
    await sql.query(statements[i]);
  }

  console.log("Migration completed successfully.");
}

main().catch((err) => {
  console.error("Migration failed:");
  console.error(err);
  process.exit(1);
});
