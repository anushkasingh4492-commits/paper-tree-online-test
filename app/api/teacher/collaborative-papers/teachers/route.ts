import { NextResponse } from "next/server";
import { pool } from "@/lib/db";
import { apiError, getCollaborativeTeacher } from "@/lib/collaborative-papers";
export const runtime="nodejs";
export async function GET(){try{const t=await getCollaborativeTeacher();if(!t)return apiError("Teacher login required.",401);const r=await pool.query(`SELECT id::text,name,email FROM teachers WHERE academy_id::text=$1::text AND id::text<>$2::text ORDER BY name`,[t.academy_id,t.id]);return NextResponse.json({success:true,teachers:r.rows})}catch(e){console.error(e);return apiError("Could not load academy professors.",500)}}
