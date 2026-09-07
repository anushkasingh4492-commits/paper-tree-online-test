import { pool } from "@/lib/db";
import bcrypt from "bcryptjs";

export const runtime = "nodejs";

export async function POST() {
  try {
    await pool.query(`
      CREATE TABLE IF NOT EXISTS admins (
        id TEXT PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        is_master BOOLEAN NOT NULL DEFAULT TRUE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      ALTER TABLE admins
      ADD COLUMN IF NOT EXISTS is_master BOOLEAN NOT NULL DEFAULT FALSE;

      ALTER TABLE teachers
      ADD COLUMN IF NOT EXISTS password_hash TEXT;

      CREATE TABLE IF NOT EXISTS notifications (
        id TEXT PRIMARY KEY,
        student_id TEXT NOT NULL,
        scheduled_test_id TEXT NOT NULL,
        title TEXT NOT NULL,
        message TEXT NOT NULL,
        is_read BOOLEAN NOT NULL DEFAULT FALSE,
        created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
      );

      CREATE INDEX IF NOT EXISTS idx_notifications_student
      ON notifications(student_id);

      CREATE INDEX IF NOT EXISTS idx_notifications_scheduled_test
      ON notifications(scheduled_test_id);
    `);

    const adminPassword = await bcrypt.hash("admin123", 10);
    const teacherPassword = await bcrypt.hash("teacher123", 10);

    await pool.query(
      `
      INSERT INTO admins
        (id, name, email, password_hash, is_master)
      VALUES
        ('admin-master', 'Administrator', 'admin@papertree.com', $1, TRUE)
      ON CONFLICT (email)
      DO UPDATE SET
        password_hash = EXCLUDED.password_hash,
        is_master = TRUE
      `,
      [adminPassword]
    );

    await pool.query(
      `
      INSERT INTO teachers
        (id, name, email, institute_name, password_hash)
      VALUES
        ('teacher-master', 'Teacher', 'teacher@papertree.com',
         'Paper Tree', $1)
      ON CONFLICT (email)
      DO UPDATE SET password_hash = EXCLUDED.password_hash
      `,
      [teacherPassword]
    );

    return Response.json({
      success: true,
      message: "Master accounts and notification system created.",
      admin: {
        email: "admin@papertree.com",
        password: "admin123",
      },
      teacher: {
        email: "teacher@papertree.com",
        password: "teacher123",
      },
    });
  } catch (error) {
    console.error(error);

    return Response.json(
      {
        success: false,
        error: error instanceof Error ? error.message : "Setup failed",
      },
      { status: 500 }
    );
  }
}
