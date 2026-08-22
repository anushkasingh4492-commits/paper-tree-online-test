CREATE TABLE "answers" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"test_id" uuid NOT NULL,
	"test_question_id" uuid NOT NULL,
	"selected_option" varchar(5),
	"is_correct" boolean,
	"time_spent_seconds" integer DEFAULT 0 NOT NULL,
	"answered_at" timestamp with time zone,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "questions" (
	"id" varchar(100) PRIMARY KEY NOT NULL,
	"exam" varchar(50) DEFAULT 'MHT-CET' NOT NULL,
	"subject" varchar(50) NOT NULL,
	"standard" integer NOT NULL,
	"chapter_number" integer NOT NULL,
	"chapter_name" varchar(255) NOT NULL,
	"major_topic" varchar(255),
	"subtopic" varchar(255),
	"concept_tested" text,
	"stem" text NOT NULL,
	"options" jsonb NOT NULL,
	"correct_option" varchar(5) NOT NULL,
	"correct_answer_text" text,
	"distractor_rationale" jsonb,
	"solution" text,
	"formula_principle" text,
	"common_misconception" text,
	"difficulty" varchar(20) NOT NULL,
	"estimated_time" varchar(100),
	"question_type" varchar(100),
	"figure_asset" text,
	"concept_family_id" varchar(100),
	"family_size" integer,
	"generator_eligible_strict_cet" boolean DEFAULT false NOT NULL,
	"generator_eligible_extended_revision" boolean DEFAULT false,
	"syllabus_scope_status" varchar(50),
	"syllabus_version" varchar(100),
	"release_version" varchar(50),
	"raw_data" jsonb,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "test_questions" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"test_id" uuid NOT NULL,
	"question_id" varchar(100) NOT NULL,
	"question_number" integer NOT NULL,
	"marked_for_review" boolean DEFAULT false NOT NULL,
	"visited" boolean DEFAULT false NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "test_results" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"test_id" uuid NOT NULL,
	"total_questions" integer NOT NULL,
	"attempted" integer NOT NULL,
	"correct" integer NOT NULL,
	"wrong" integer NOT NULL,
	"unattempted" integer NOT NULL,
	"score" real NOT NULL,
	"accuracy" real NOT NULL,
	"total_time_seconds" integer NOT NULL,
	"subject_analysis" jsonb,
	"chapter_analysis" jsonb,
	"difficulty_analysis" jsonb,
	"weak_areas" jsonb,
	"completed_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "test_violations" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"test_id" uuid NOT NULL,
	"type" varchar(50) NOT NULL,
	"description" text,
	"occurred_at" timestamp with time zone DEFAULT now() NOT NULL,
	"metadata" jsonb
);
--> statement-breakpoint
CREATE TABLE "tests" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"user_id" uuid NOT NULL,
	"exam" varchar(50) DEFAULT 'MHT-CET' NOT NULL,
	"title" varchar(255) NOT NULL,
	"subjects" jsonb NOT NULL,
	"chapters" jsonb,
	"difficulty" varchar(20) NOT NULL,
	"question_count" integer NOT NULL,
	"duration_minutes" integer NOT NULL,
	"status" varchar(30) DEFAULT 'in_progress' NOT NULL,
	"started_at" timestamp with time zone,
	"submitted_at" timestamp with time zone,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
CREATE TABLE "users" (
	"id" uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
	"name" varchar(150) NOT NULL,
	"email" varchar(255) NOT NULL,
	"password_hash" text NOT NULL,
	"created_at" timestamp with time zone DEFAULT now() NOT NULL,
	"updated_at" timestamp with time zone DEFAULT now() NOT NULL
);
--> statement-breakpoint
ALTER TABLE "answers" ADD CONSTRAINT "answers_test_id_tests_id_fk" FOREIGN KEY ("test_id") REFERENCES "public"."tests"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "answers" ADD CONSTRAINT "answers_test_question_id_test_questions_id_fk" FOREIGN KEY ("test_question_id") REFERENCES "public"."test_questions"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "test_questions" ADD CONSTRAINT "test_questions_test_id_tests_id_fk" FOREIGN KEY ("test_id") REFERENCES "public"."tests"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "test_questions" ADD CONSTRAINT "test_questions_question_id_questions_id_fk" FOREIGN KEY ("question_id") REFERENCES "public"."questions"("id") ON DELETE restrict ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "test_results" ADD CONSTRAINT "test_results_test_id_tests_id_fk" FOREIGN KEY ("test_id") REFERENCES "public"."tests"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "test_violations" ADD CONSTRAINT "test_violations_test_id_tests_id_fk" FOREIGN KEY ("test_id") REFERENCES "public"."tests"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
ALTER TABLE "tests" ADD CONSTRAINT "tests_user_id_users_id_fk" FOREIGN KEY ("user_id") REFERENCES "public"."users"("id") ON DELETE cascade ON UPDATE no action;--> statement-breakpoint
CREATE UNIQUE INDEX "answers_test_question_unique" ON "answers" USING btree ("test_question_id");--> statement-breakpoint
CREATE INDEX "answers_test_idx" ON "answers" USING btree ("test_id");--> statement-breakpoint
CREATE INDEX "questions_exam_subject_idx" ON "questions" USING btree ("exam","subject");--> statement-breakpoint
CREATE INDEX "questions_chapter_idx" ON "questions" USING btree ("subject","chapter_number");--> statement-breakpoint
CREATE INDEX "questions_difficulty_idx" ON "questions" USING btree ("subject","difficulty");--> statement-breakpoint
CREATE INDEX "questions_generator_eligible_idx" ON "questions" USING btree ("generator_eligible_strict_cet");--> statement-breakpoint
CREATE UNIQUE INDEX "test_questions_unique" ON "test_questions" USING btree ("test_id","question_id");--> statement-breakpoint
CREATE UNIQUE INDEX "test_questions_number_unique" ON "test_questions" USING btree ("test_id","question_number");--> statement-breakpoint
CREATE INDEX "test_questions_test_idx" ON "test_questions" USING btree ("test_id");--> statement-breakpoint
CREATE UNIQUE INDEX "test_results_test_unique" ON "test_results" USING btree ("test_id");--> statement-breakpoint
CREATE INDEX "violations_test_idx" ON "test_violations" USING btree ("test_id");--> statement-breakpoint
CREATE INDEX "tests_user_idx" ON "tests" USING btree ("user_id");--> statement-breakpoint
CREATE INDEX "tests_status_idx" ON "tests" USING btree ("user_id","status");--> statement-breakpoint
CREATE UNIQUE INDEX "users_email_unique" ON "users" USING btree ("email");