import { NextResponse } from "next/server";
import { cookies } from "next/headers";
import { pool } from "@/lib/db";

async function isMasterAdmin(){const v=(await cookies()).get("master_session")?.value;if(!v)return false;try{const s=JSON.parse(v);return s.role==="ADMIN"||s.role==="MASTER_ADMIN";}catch{return false;}}

export async function PATCH(req:Request,{params}:{params:Promise<{academyId:string;id:string}>}){
  if(!(await isMasterAdmin()))return NextResponse.json({success:false,error:"Unauthorized"},{status:401});
  const {academyId,id: batchId}=await params;
  try{const b=await req.json();const name=String(b.name||"").trim();const className=String(b.className||"").trim();if(!name||!["Class 11","Class 12","Class 11 + 12"].includes(className))return NextResponse.json({success:false,error:"Name and a valid class are required."},{status:400});const r=await pool.query(`UPDATE batches SET name=$1,class_name=$2 WHERE id=$3 AND academy_id=$4 RETURNING id,name,class_name,created_at`,[name,className,batchId,academyId]);if(!r.rows.length)return NextResponse.json({success:false,error:"Batch not found."},{status:404});return NextResponse.json({success:true,batch:r.rows[0]});}catch(e){console.error("MASTER BATCH PATCH ERROR:",e);return NextResponse.json({success:false,error:"Failed to update batch."},{status:500});}
}

export async function DELETE(_req:Request,{params}:{params:Promise<{academyId:string;id:string}>}){
  if(!(await isMasterAdmin()))return NextResponse.json({success:false,error:"Unauthorized"},{status:401});
  const {academyId,id: batchId}=await params; const client=await pool.connect();
  try{await client.query("BEGIN");const b=await client.query(`SELECT id FROM batches WHERE id=$1 AND academy_id=$2 LIMIT 1`,[batchId,academyId]);if(!b.rows.length){await client.query("ROLLBACK");return NextResponse.json({success:false,error:"Batch not found."},{status:404});}const tests=await client.query(`SELECT COUNT(*)::int AS count FROM scheduled_tests WHERE batch_id=$1`,[batchId]);if(Number(tests.rows[0]?.count||0)>0){await client.query("ROLLBACK");return NextResponse.json({success:false,error:"This batch has scheduled tests. Remove or finish those tests before deleting the batch."},{status:409});}await client.query(`DELETE FROM batch_students WHERE batch_id=$1`,[batchId]);await client.query(`DELETE FROM batches WHERE id=$1 AND academy_id=$2`,[batchId,academyId]);await client.query("COMMIT");return NextResponse.json({success:true});}catch(e){await client.query("ROLLBACK");console.error("MASTER BATCH DELETE ERROR:",e);return NextResponse.json({success:false,error:"Batch could not be deleted."},{status:409});}finally{client.release();}
}
