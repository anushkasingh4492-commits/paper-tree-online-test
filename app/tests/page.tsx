"use client";

import { useEffect, useMemo, useState } from "react";
import { useRouter } from "next/navigation";

import {
  getPresetsForGroup,
  calculatePreset,
  type StudentGroup,
  type Preset,
} from "@/lib/test-presets";

type Course = "MHT-CET" | "JEE" | "NEET";

type Subject =
  | "Physics"
  | "Chemistry"
  | "Mathematics"
  | "Biology";

type DatabaseChapter = {
  subject: string;
  chapter: string;
};

const COURSE_CONFIG: Record<
  Course,
  {
    description: string;
    subjects: Subject[];
    available: boolean;
  }
> = {
  "MHT-CET": {
    description: "Maharashtra Common Entrance Test",
    subjects: [
      "Physics",
      "Chemistry",
      "Mathematics",
      "Biology",
    ],
    available: true,
  },

  JEE: {
    description: "Joint Entrance Examination",
    subjects: [
      "Physics",
      "Chemistry",
      "Mathematics",
    ],
    available: false,
  },

  NEET: {
    description:
      "National Eligibility cum Entrance Test",
    subjects: [
      "Physics",
      "Chemistry",
      "Biology",
    ],
    available: false,
  },
};

const SAMPLE_CHAPTERS: Record<
  Subject,
  string[]
> = {
  Physics: [
    "Rotational Motion",
    "Thermodynamics",
    "Current Electricity",
    "Electrostatics",
    "Semiconductors",
  ],

  Chemistry: [
    "Some Basic Concepts of Chemistry",
    "Chemical Bonding",
    "Electrochemistry",
    "Chemical Kinetics",
    "Biomolecules",
  ],

  Mathematics: [
    "Trigonometry",
    "Straight Line",
    "Circle",
    "Probability",
    "Differentiation",
  ],

  Biology: [
    "Biomolecules",
    "Respiration and Energy Transfer",
    "Human Nutrition",
    "Inheritance and Variation",
    "Molecular Basis of Inheritance",
  ],
};

const DIFFICULTIES = [
  "Easy",
  "Challenging",
  "Balanced",
  "Difficult",
];

const PRESET_SUBJECT_NAMES: Record<
  string,
  string
> = {
  physics: "Physics",
  chemistry: "Chemistry",
  maths: "Mathematics",
  biology: "Biology",
};

function subjectToPresetSubject(
  subject: Subject
):
  | "physics"
  | "chemistry"
  | "maths"
  | "biology" {
  switch (subject) {
    case "Physics":
      return "physics";

    case "Chemistry":
      return "chemistry";

    case "Mathematics":
      return "maths";

    case "Biology":
      return "biology";
  }
}

function presetSubjectToSubject(
  subject:
    | "physics"
    | "chemistry"
    | "maths"
    | "biology"
): Subject {
  switch (subject) {
    case "physics":
      return "Physics";

    case "chemistry":
      return "Chemistry";

    case "maths":
      return "Mathematics";

    case "biology":
      return "Biology";
  }
}

export default function TestsPage() {
  const router = useRouter();

  const [course, setCourse] =
    useState<Course>("MHT-CET");

  const [subjects, setSubjects] =
    useState<Subject[]>(["Physics"]);

  const [activeChapterSubject, setActiveChapterSubject] =
    useState<Subject>("Physics");

  const [chaptersBySubject, setChaptersBySubject] =
    useState<Record<Subject, string[]>>({
      Physics: [],
      Chemistry: [],
      Mathematics: [],
      Biology: [],
    });

  const [availableChapters, setAvailableChapters] =
    useState<DatabaseChapter[]>([]);

  const [databaseSubjects, setDatabaseSubjects] =
    useState<string[]>([]);

  const [loadingDatabase, setLoadingDatabase] =
    useState(true);

  const [difficulty, setDifficulty] =
    useState("Balanced");

  /*
   * ---------------------------------------------------------
   * MHT CET GROUP
   * ---------------------------------------------------------
   */

  const [studentGroup, setStudentGroup] =
    useState<StudentGroup | null>(null);

  /*
   * ---------------------------------------------------------
   * PRESET
   * ---------------------------------------------------------
   */

  const [selectedPreset, setSelectedPreset] =
    useState<Preset | null>(null);

  const [generating, setGenerating] =
    useState(false);

  const courseConfig =
    COURSE_CONFIG[course];

  /*
   * ---------------------------------------------------------
   * SELECTED CHAPTERS
   * ---------------------------------------------------------
   */

  const selectedChapters = useMemo(() => {
    return subjects.flatMap(
      (subject) =>
        chaptersBySubject[subject] || []
    );
  }, [
    subjects,
    chaptersBySubject,
  ]);

  /*
   * ---------------------------------------------------------
   * AVAILABLE PRESETS
   * ---------------------------------------------------------
   */

  const availablePresets = useMemo(() => {
    if (!studentGroup) {
      return [];
    }

    return getPresetsForGroup(
      studentGroup
    );
  }, [studentGroup]);

  /*
   * ---------------------------------------------------------
   * SELECTED PRESET DETAILS
   * ---------------------------------------------------------
   */

  const presetDetails = useMemo(() => {
    if (!selectedPreset) {
      return null;
    }

    return calculatePreset(
      selectedPreset
    );
  }, [selectedPreset]);

  /*
   * ---------------------------------------------------------
   * LOAD SAVED GROUP
   * ---------------------------------------------------------
   */

  useEffect(() => {
    const savedGroup =
      localStorage.getItem(
        "mhtCETGroup"
      );

    if (
      savedGroup === "PCM" ||
      savedGroup === "PCB"
    ) {
      setStudentGroup(
        savedGroup
      );
    }
  }, []);

  /*
   * ---------------------------------------------------------
   * LOAD DATABASE DATA
   * ---------------------------------------------------------
   */

  useEffect(() => {
    async function loadDatabaseData() {
      try {
        setLoadingDatabase(true);

        const response =
          await fetch(
            "/api/db-schema",
            {
              method: "GET",
              cache: "no-store",
            }
          );

        const data =
          await response.json();

        if (
          !response.ok ||
          !data.success
        ) {
          throw new Error(
            data.error ||
              "Failed to load subjects and chapters."
          );
        }

        setAvailableChapters(
          Array.isArray(
            data.chapters
          )
            ? data.chapters
            : []
        );

        setDatabaseSubjects(
          Array.isArray(
            data.subjects
          )
            ? data.subjects
            : []
        );
      } catch (error) {
        console.error(
          "Failed to load database data:",
          error
        );
      } finally {
        setLoadingDatabase(false);
      }
    }

    loadDatabaseData();
  }, []);

  /*
   * ---------------------------------------------------------
   * GROUP CHANGE
   * ---------------------------------------------------------
   */

  function changeStudentGroup(
    nextGroup: StudentGroup
  ) {
    setStudentGroup(nextGroup);

    localStorage.setItem(
      "mhtCETGroup",
      nextGroup
    );

    /*
     * PCM:
     * Physics + Chemistry + Mathematics
     *
     * PCB:
     * Physics + Chemistry + Biology
     */

    if (nextGroup === "PCM") {
      setSubjects([
        "Physics",
      ]);

      setActiveChapterSubject(
        "Physics"
      );

      setChaptersBySubject(
        (previous) => ({
          ...previous,
          Biology: [],
        })
      );
    } else {
      setSubjects([
        "Physics",
      ]);

      setActiveChapterSubject(
        "Physics"
      );

      setChaptersBySubject(
        (previous) => ({
          ...previous,
          Mathematics: [],
        })
      );
    }

    /*
     * Group change means an old preset
     * may no longer be valid.
     */

    setSelectedPreset(null);
  }

  /*
   * ---------------------------------------------------------
   * KEEP SUBJECTS COMPATIBLE WITH GROUP
   * ---------------------------------------------------------
   */

  useEffect(() => {
    if (!studentGroup) {
      return;
    }

    const allowedSubjects =
      studentGroup === "PCM"
        ? ([
            "Physics",
            "Chemistry",
            "Mathematics",
          ] as Subject[])
        : ([
            "Physics",
            "Chemistry",
            "Biology",
          ] as Subject[]);

    setSubjects(
      (previous) => {
        const validSubjects =
          previous.filter(
            (subject) =>
              allowedSubjects.includes(
                subject
              )
          );

        if (
          validSubjects.length > 0
        ) {
          return validSubjects;
        }

        return ["Physics"];
      }
    );

    setActiveChapterSubject(
      (previous) =>
        allowedSubjects.includes(
          previous
        )
          ? previous
          : "Physics"
    );

    setChaptersBySubject(
      (previous) => ({
        ...previous,

        Mathematics:
          studentGroup === "PCM"
            ? previous.Mathematics
            : [],

        Biology:
          studentGroup === "PCB"
            ? previous.Biology
            : [],
      })
    );

    /*
     * Remove preset if it no longer
     * belongs to the selected group.
     */

    setSelectedPreset(
      (previous) => {
        if (!previous) {
          return null;
        }

        const allowedPresetIds =
          getPresetsForGroup(
            studentGroup
          ).map(
            (preset) =>
              preset.id
          );

        return allowedPresetIds.includes(
          previous.id
        )
          ? previous
          : null;
      }
    );
  }, [studentGroup]);

  /*
   * ---------------------------------------------------------
   * CHAPTERS FOR ACTIVE SUBJECT
   * ---------------------------------------------------------
   */

  const currentSubjectChapters =
    useMemo(() => {
      const databaseChapterNames =
        availableChapters
          .filter(
            (item) =>
              item.subject
                .trim()
                .toLowerCase() ===
              activeChapterSubject
                .trim()
                .toLowerCase()
          )
          .map(
            (item) =>
              item.chapter
          );

      const uniqueDatabaseChapters =
        Array.from(
          new Set(
            databaseChapterNames
          )
        );

      if (
        uniqueDatabaseChapters.length >
        0
      ) {
        return uniqueDatabaseChapters;
      }

      return (
        SAMPLE_CHAPTERS[
          activeChapterSubject
        ] || []
      );
    }, [
      availableChapters,
      activeChapterSubject,
    ]);

  /*
   * ---------------------------------------------------------
   * CHANGE COURSE
   * ---------------------------------------------------------
   */

  function changeCourse(
    nextCourse: Course
  ) {
    setCourse(nextCourse);

    const config =
      COURSE_CONFIG[
        nextCourse
      ];

    if (
      config.subjects.length >
      0
    ) {
      const firstSubject =
        config.subjects[0];

      setSubjects([
        firstSubject,
      ]);

      setActiveChapterSubject(
        firstSubject
      );
    }

    setChaptersBySubject({
      Physics: [],
      Chemistry: [],
      Mathematics: [],
      Biology: [],
    });

    setSelectedPreset(null);
  }

  /*
   * ---------------------------------------------------------
   * TOGGLE SUBJECT
   * ---------------------------------------------------------
   */

  function toggleSubject(
    nextSubject: Subject
  ) {
    if (studentGroup) {
      const allowedSubjects =
        studentGroup === "PCM"
          ? ([
              "Physics",
              "Chemistry",
              "Mathematics",
            ] as Subject[])
          : ([
              "Physics",
              "Chemistry",
              "Biology",
            ] as Subject[]);

      if (
        !allowedSubjects.includes(
          nextSubject
        )
      ) {
        return;
      }
    }

    setSubjects(
      (previous) => {
        /*
         * Mathematics and Biology
         * cannot be combined.
         */

        if (
          nextSubject ===
            "Mathematics" &&
          previous.includes(
            "Biology"
          )
        ) {
          return previous;
        }

        if (
          nextSubject ===
            "Biology" &&
          previous.includes(
            "Mathematics"
          )
        ) {
          return previous;
        }

        /*
         * REMOVE SUBJECT
         */

        if (
          previous.includes(
            nextSubject
          )
        ) {
          if (
            previous.length ===
            1
          ) {
            return previous;
          }

          const updated =
            previous.filter(
              (item) =>
                item !==
                nextSubject
            );

          if (
            activeChapterSubject ===
            nextSubject
          ) {
            setActiveChapterSubject(
              updated[0]
            );
          }

          /*
           * Check whether the
           * existing preset still matches.
           */

          if (selectedPreset) {
            const presetSubjects =
              Object.keys(
                selectedPreset.subjects
              ).map(
                (subject) =>
                  subject as
                    | "physics"
                    | "chemistry"
                    | "maths"
                    | "biology"
              );

            const updatedPresetStillValid =
              presetSubjects.every(
                (
                  presetSubject
                ) =>
                  updated.includes(
                    presetSubjectToSubject(
                      presetSubject
                    )
                  )
              ) &&
              presetSubjects.length ===
                updated.length;

            if (
              !updatedPresetStillValid
            ) {
              setSelectedPreset(
                null
              );
            }
          }

          return updated;
        }

        /*
         * ADD SUBJECT
         */

        const updated = [
          ...previous,
          nextSubject,
        ];

        setActiveChapterSubject(
          nextSubject
        );

        setSelectedPreset(
          null
        );

        return updated;
      }
    );
  }

  /*
   * ---------------------------------------------------------
   * TOGGLE CHAPTER
   * ---------------------------------------------------------
   */

  function toggleChapter(
    subject: Subject,
    chapter: string
  ) {
    setChaptersBySubject(
      (previous) => {
        const current =
          previous[subject] ||
          [];

        if (
          current.includes(
            chapter
          )
        ) {
          return {
            ...previous,

            [subject]:
              current.filter(
                (item) =>
                  item !==
                  chapter
              ),
          };
        }

        return {
          ...previous,

          [subject]: [
            ...current,
            chapter,
          ],
        };
      }
    );

    /*
     * Selecting/clearing chapters
     * means a preset can still remain
     * selected because presets determine
     * question count, not chapters.
     */
  }

  /*
   * ---------------------------------------------------------
   * SELECT ALL CHAPTERS
   * ---------------------------------------------------------
   */

  function selectAllChapters(
    subject: Subject,
    chapterList: string[]
  ) {
    setChaptersBySubject(
      (previous) => ({
        ...previous,

        [subject]: [
          ...chapterList,
        ],
      })
    );
  }

  /*
   * ---------------------------------------------------------
   * CLEAR CHAPTERS
   * ---------------------------------------------------------
   */

  function clearChapters(
    subject: Subject
  ) {
    setChaptersBySubject(
      (previous) => ({
        ...previous,

        [subject]: [],
      })
    );
  }

  /*
   * ---------------------------------------------------------
   * CHECK PRESET SUBJECT MATCH
   * ---------------------------------------------------------
   */

  function presetMatchesSelectedSubjects(
    preset: Preset
  ) {
    const selectedPresetSubjects =
      Object.keys(
        preset.subjects
      ).map(
        (subject) =>
          subject as
            | "physics"
            | "chemistry"
            | "maths"
            | "biology"
      );

    const selectedSubjectKeys =
      subjects.map(
        (subject) =>
          subjectToPresetSubject(
            subject
          )
      );

    /*
     * Exact subject combination
     * is required.
     */

    if (
      selectedPresetSubjects.length !==
      selectedSubjectKeys.length
    ) {
      return false;
    }

    return (
      selectedPresetSubjects.every(
        (subject) =>
          selectedSubjectKeys.includes(
            subject
          )
      ) &&
      selectedSubjectKeys.every(
        (subject) =>
          selectedPresetSubjects.includes(
            subject
          )
      )
    );
  }

  /*
   * ---------------------------------------------------------
   * GENERATE TEST
   * ---------------------------------------------------------
   */

  async function generateTest() {
    if (
      !courseConfig.available
    ) {
      return;
    }

    if (!studentGroup) {
      alert(
        "Please select your MHT CET group: PCM or PCB."
      );

      return;
    }

    if (
      !selectedPreset ||
      !presetDetails
    ) {
      alert(
        "Please select a test preset."
      );

      return;
    }

    if (
      !presetMatchesSelectedSubjects(
        selectedPreset
      )
    ) {
      alert(
        "Please select subjects that match the chosen preset."
      );

      return;
    }

    if (
      presetDetails.totalMarks >
        200 ||
      presetDetails.durationMinutes >
        180
    ) {
      alert(
        "This preset exceeds the maximum allowed test size."
      );

      return;
    }

    if (
      subjects.length === 0
    ) {
      alert(
        "Please select at least one subject."
      );

      return;
    }

    setGenerating(true);

    try {
      const response =
        await fetch(
          "/api/tests/generate",
          {
            method: "POST",

            headers: {
              "Content-Type":
                "application/json",
            },

            body: JSON.stringify({
              exam: course,

              course,

              studentGroup,

              subjects,

              subject:
                subjects[0],

              chapters:
                selectedChapters,

              chaptersBySubject,

              difficulty:
                difficulty.toLowerCase(),

              questionCount:
                presetDetails.totalQuestions,

              duration:
                presetDetails.durationMinutes,

              presetId:
                selectedPreset.id,

              presetName:
                selectedPreset.name,

              totalMarks:
                presetDetails.totalMarks,
            }),
          }
        );

      const data =
        await response.json();

      if (
        !response.ok ||
        !data.success
      ) {
        throw new Error(
          data.error ||
            "Unable to generate test."
        );
      }

      const testId =
        data.testId;

      /*
       * -----------------------------------------------------
       * TEST CONFIGURATION
       * -----------------------------------------------------
       */

      const testConfiguration = {
        testId,

        course,

        studentGroup,

        subjects,

        subject:
          subjects[0],

        chapters:
          selectedChapters,

        chaptersBySubject,

        difficulty,

        questionCount:
          presetDetails.totalQuestions,

        duration:
          presetDetails.durationMinutes,

        totalMarks:
          presetDetails.totalMarks,

        presetId:
          selectedPreset.id,

        presetName:
          selectedPreset.name,

        createdAt:
          new Date().toISOString(),
      };

      /*
       * -----------------------------------------------------
       * SAVE COMPLETE TEST
       * -----------------------------------------------------
       */

      localStorage.setItem(
        `test-${testId}`,
        JSON.stringify({
          ...testConfiguration,

          questions:
            data.questions,

          startedAt:
            new Date().toISOString(),
        })
      );

      /*
       * -----------------------------------------------------
       * SAVE CONFIG
       * -----------------------------------------------------
       */

      localStorage.setItem(
        `test-config-${testId}`,
        JSON.stringify(
          testConfiguration
        )
      );

      /*
       * -----------------------------------------------------
       * OPEN TEST
       * -----------------------------------------------------
       */

      router.push(
        `/test/${testId}`
      );
    } catch (error) {
      console.error(
        "GENERATE TEST ERROR:",
        error
      );

      alert(
        error instanceof Error
          ? error.message
          : "Unable to generate test."
      );
    } finally {
      setGenerating(false);
    }
  }

  /*
   * ---------------------------------------------------------
   * RENDER
   * ---------------------------------------------------------
   */

  return (
    <main className="min-h-screen bg-[#f5f7fb] text-[#111827]">

      {/* HEADER */}

      <header className="h-16 bg-white border-b border-[#e5e7eb] flex items-center justify-between px-6">

        <div className="flex items-center gap-3">

          <button
            onClick={() =>
              router.push(
                "/dashboard"
              )
            }
            className="w-9 h-9 rounded-xl bg-[#1d4ed8] text-white flex items-center justify-center font-bold"
          >
            P
          </button>

          <div>
            <div className="font-semibold">
              Paper Tree
            </div>

            <div className="text-xs text-[#6b7280]">
              Create Test
            </div>
          </div>

        </div>

        <button
          onClick={() =>
            router.push(
              "/dashboard"
            )
          }
          className="text-sm text-[#6b7280] hover:text-[#111827]"
        >
          Dashboard
        </button>

      </header>

      <div className="max-w-6xl mx-auto px-6 py-8">

        {/* PAGE TITLE */}

        <div className="mb-8">

          <div className="text-sm font-medium text-[#2563eb] mb-2">
            TEST GENERATOR
          </div>

          <h1 className="text-3xl font-bold tracking-tight">
            Create a New Test
          </h1>

          <p className="mt-2 text-sm text-[#6b7280]">
            Configure your test and start
            practising with questions from
            the Paper Tree question bank.
          </p>

        </div>

        <div className="grid grid-cols-1 lg:grid-cols-[1fr_330px] gap-6">

          {/* MAIN CONFIGURATION */}

          <div className="space-y-6">

            {/* COURSE */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  1. Choose Exam
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Select the entrance examination
                  you are preparing for.
                </p>

              </div>

              <div className="grid grid-cols-1 md:grid-cols-3 gap-3">

                {(
                  Object.keys(
                    COURSE_CONFIG
                  ) as Course[]
                ).map((item) => {

                  const config =
                    COURSE_CONFIG[
                      item
                    ];

                  const selected =
                    course === item;

                  return (
                    <button
                      key={item}
                      disabled={
                        !config.available
                      }
                      onClick={() =>
                        changeCourse(
                          item
                        )
                      }
                      className={`relative text-left rounded-xl border-2 p-5 transition ${
                        selected
                          ? "border-[#2563eb] bg-[#eff6ff]"
                          : config.available
                          ? "border-[#e5e7eb] hover:border-[#bfdbfe]"
                          : "border-[#e5e7eb] bg-[#fafafa] opacity-60 cursor-not-allowed"
                      }`}
                    >

                      {selected && (
                        <div className="absolute top-4 right-4 w-5 h-5 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs">
                          ✓
                        </div>
                      )}

                      {!config.available && (
                        <span className="absolute top-3 right-3 text-[10px] font-semibold uppercase tracking-wide bg-[#f3f4f6] text-[#6b7280] px-2 py-1 rounded-md">
                          Coming Soon
                        </span>
                      )}

                      <div className="text-lg font-bold">
                        {item}
                      </div>

                      <div className="text-xs text-[#6b7280] mt-2 pr-4">
                        {
                          config.description
                        }
                      </div>

                    </button>
                  );
                })}

              </div>

            </section>

            {/* GROUP */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  2. Choose MHT CET Group
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Choose the subject combination
                  you want to practise.
                </p>

              </div>

              <div className="grid grid-cols-1 md:grid-cols-2 gap-3">

                <button
                  type="button"
                  onClick={() =>
                    changeStudentGroup(
                      "PCM"
                    )
                  }
                  className={`relative text-left rounded-xl border-2 p-5 transition ${
                    studentGroup ===
                    "PCM"
                      ? "border-[#2563eb] bg-[#eff6ff]"
                      : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                  }`}
                >

                  {studentGroup ===
                    "PCM" && (
                    <div className="absolute top-4 right-4 w-5 h-5 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs">
                      ✓
                    </div>
                  )}

                  <div className="text-lg font-bold">
                    PCM
                  </div>

                  <div className="text-sm text-[#6b7280] mt-2">
                    Physics + Chemistry +
                    Mathematics
                  </div>

                </button>

                <button
                  type="button"
                  onClick={() =>
                    changeStudentGroup(
                      "PCB"
                    )
                  }
                  className={`relative text-left rounded-xl border-2 p-5 transition ${
                    studentGroup ===
                    "PCB"
                      ? "border-[#2563eb] bg-[#eff6ff]"
                      : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                  }`}
                >

                  {studentGroup ===
                    "PCB" && (
                    <div className="absolute top-4 right-4 w-5 h-5 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs">
                      ✓
                    </div>
                  )}

                  <div className="text-lg font-bold">
                    PCB
                  </div>

                  <div className="text-sm text-[#6b7280] mt-2">
                    Physics + Chemistry +
                    Biology
                  </div>

                </button>

              </div>

              {!studentGroup && (
                <div className="mt-4 rounded-xl bg-[#fff7ed] border border-[#fed7aa] p-4 text-sm text-[#9a3412]">
                  Select PCM or PCB to
                  continue.
                </div>
              )}

              {studentGroup && (
                <div className="mt-4 rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3">

                  <div className="text-xs text-[#6b7280]">
                    Selected group
                  </div>

                  <div className="text-sm font-semibold mt-1">
                    {studentGroup}
                  </div>

                </div>
              )}

            </section>

            {/* SUBJECT */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  3. Choose Subject
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Select one or more subjects.
                  Mathematics and Biology cannot
                  be selected together.
                </p>

              </div>

              <div className="grid grid-cols-2 md:grid-cols-3 gap-3">

                {courseConfig.subjects
                  .filter(
                    (item) => {
                      if (
                        !studentGroup
                      ) {
                        return false;
                      }

                      if (
                        studentGroup ===
                        "PCM"
                      ) {
                        return [
                          "Physics",
                          "Chemistry",
                          "Mathematics",
                        ].includes(
                          item
                        );
                      }

                      return [
                        "Physics",
                        "Chemistry",
                        "Biology",
                      ].includes(
                        item
                      );
                    }
                  )
                  .map((item) => {

                    const selected =
                      subjects.includes(
                        item
                      );

                    const blocked =
                      (item ===
                        "Mathematics" &&
                        subjects.includes(
                          "Biology"
                        )) ||
                      (item ===
                        "Biology" &&
                        subjects.includes(
                          "Mathematics"
                        ));

                    const hasDatabaseData =
                      databaseSubjects.some(
                        (
                          dbSubject
                        ) =>
                          dbSubject
                            .trim()
                            .toLowerCase() ===
                          item
                            .trim()
                            .toLowerCase()
                      );

                    return (
                      <button
                        key={item}
                        onClick={() =>
                          !blocked &&
                          toggleSubject(
                            item
                          )
                        }
                        disabled={
                          blocked ||
                          !studentGroup
                        }
                        className={`p-4 rounded-xl border-2 text-sm font-semibold transition ${
                          selected
                            ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                            : blocked
                            ? "border-[#e5e7eb] bg-[#f9fafb] opacity-50 cursor-not-allowed"
                            : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                        }`}
                      >

                        <div>
                          {item}
                        </div>

                        {loadingDatabase ? (
                          <div className="text-[10px] text-[#9ca3af] mt-1">
                            Loading...
                          </div>
                        ) : (
                          <div
                            className={`text-[10px] mt-1 ${
                              hasDatabaseData
                                ? "text-green-600"
                                : "text-[#9ca3af]"
                            }`}
                          >
                            {hasDatabaseData
                              ? "Database available"
                              : "No database data"}
                          </div>
                        )}

                        {blocked && (
                          <div className="text-[9px] text-[#9ca3af] mt-1">
                            Cannot combine with{" "}
                            {item ===
                            "Mathematics"
                              ? "Biology"
                              : "Mathematics"}
                          </div>
                        )}

                      </button>
                    );
                  })}

              </div>

              {studentGroup && (
                <div className="mt-4 rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3">

                  <div className="text-xs text-[#6b7280] mb-2">
                    Selected subjects
                  </div>

                  <div className="flex flex-wrap gap-2">

                    {subjects.map(
                      (item) => (
                        <span
                          key={item}
                          className="px-3 py-1.5 rounded-lg bg-[#eff6ff] text-[#1d4ed8] text-xs font-semibold"
                        >
                          {item}
                        </span>
                      )
                    )}

                  </div>

                </div>
              )}

            </section>

            {/* CHAPTERS */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  4. Choose Chapters
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Select chapters separately for
                  each selected subject.
                </p>

              </div>

              {!studentGroup ? (
                <div className="rounded-xl bg-[#fff7ed] border border-[#fed7aa] p-4 text-sm text-[#9a3412]">
                  Select PCM or PCB first.
                </div>
              ) : (
                <>
                  <div className="flex flex-wrap gap-2 mb-5">

                    {subjects.map(
                      (item) => {

                        const selectedCount =
                          (
                            chaptersBySubject[
                              item
                            ] || []
                          ).length;

                        const active =
                          activeChapterSubject ===
                          item;

                        return (
                          <button
                            key={item}
                            onClick={() =>
                              setActiveChapterSubject(
                                item
                              )
                            }
                            className={`px-4 py-2.5 rounded-xl border-2 text-sm font-semibold transition ${
                              active
                                ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                                : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                            }`}
                          >
                            {item}

                            {selectedCount >
                              0 && (
                              <span className="ml-2 text-xs">
                                (
                                {
                                  selectedCount
                                }
                                )
                              </span>
                            )}

                          </button>
                        );
                      }
                    )}

                  </div>

                  {loadingDatabase && (
                    <div className="rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-4 text-sm text-[#6b7280]">
                      Loading chapters from
                      the question bank...
                    </div>
                  )}

                  {!loadingDatabase && (
                    <div className="flex items-center justify-between gap-3 mb-4">

                      <div>

                        <div className="text-sm font-semibold">
                          {
                            activeChapterSubject
                          }
                        </div>

                        <div className="text-xs text-[#6b7280] mt-1">
                          Select chapters for{" "}
                          {
                            activeChapterSubject
                          }.
                        </div>

                      </div>

                      <div className="flex gap-2">

                        <button
                          onClick={() =>
                            selectAllChapters(
                              activeChapterSubject,
                              currentSubjectChapters
                            )
                          }
                          disabled={
                            currentSubjectChapters.length ===
                            0
                          }
                          className="text-xs font-semibold text-[#2563eb] hover:underline disabled:text-[#9ca3af] disabled:no-underline"
                        >
                          Select All
                        </button>

                        <span className="text-[#d1d5db]">
                          |
                        </span>

                        <button
                          onClick={() =>
                            clearChapters(
                              activeChapterSubject
                            )
                          }
                          className="text-xs font-semibold text-[#6b7280] hover:underline"
                        >
                          Clear
                        </button>

                      </div>

                    </div>
                  )}

                  {!loadingDatabase &&
                    currentSubjectChapters.length >
                      0 && (
                      <div className="space-y-2">

                        {currentSubjectChapters.map(
                          (
                            chapter
                          ) => {

                            const selected =
                              (
                                chaptersBySubject[
                                  activeChapterSubject
                                ] || []
                              ).includes(
                                chapter
                              );

                            return (
                              <button
                                key={
                                  chapter
                                }
                                onClick={() =>
                                  toggleChapter(
                                    activeChapterSubject,
                                    chapter
                                  )
                                }
                                className={`w-full flex items-center justify-between p-3.5 rounded-xl border transition text-left ${
                                  selected
                                    ? "border-[#93c5fd] bg-[#eff6ff]"
                                    : "border-[#e5e7eb] hover:bg-[#f9fafb]"
                                }`}
                              >

                                <span className="text-sm font-medium">
                                  {
                                    chapter
                                  }
                                </span>

                                <span
                                  className={`w-5 h-5 rounded-md border flex items-center justify-center text-xs ${
                                    selected
                                      ? "bg-[#2563eb] border-[#2563eb] text-white"
                                      : "border-[#d1d5db]"
                                  }`}
                                >
                                  {selected
                                    ? "✓"
                                    : ""}
                                </span>

                              </button>
                            );
                          }
                        )}

                      </div>
                    )}

                  {!loadingDatabase &&
                    currentSubjectChapters.length ===
                      0 && (
                      <div className="rounded-xl bg-[#fff7ed] border border-[#fed7aa] p-4 text-sm text-[#9a3412]">
                        No chapters found in
                        the database for{" "}
                        <strong>
                          {
                            activeChapterSubject
                          }
                        </strong>
                        .
                      </div>
                    )}

                  <div className="mt-5 space-y-2">

                    {subjects.map(
                      (item) => {

                        const selected =
                          chaptersBySubject[
                            item
                          ] || [];

                        return (
                          <div
                            key={item}
                            className="rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3"
                          >

                            <div className="flex items-center justify-between">

                              <span className="text-xs font-semibold">
                                {item}
                              </span>

                              <span className="text-[11px] text-[#6b7280]">
                                {
                                  selected.length
                                }{" "}
                                selected
                              </span>

                            </div>

                            {selected.length >
                              0 && (
                              <div className="text-[11px] text-[#6b7280] mt-2">
                                {selected.join(
                                  ", "
                                )}
                              </div>
                            )}

                          </div>
                        );
                      }
                    )}

                  </div>

                  {selectedChapters.length ===
                    0 && (
                    <div className="mt-4 rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3 text-xs text-[#6b7280]">
                      No chapter selected —
                      questions can be taken
                      from the selected subjects.
                    </div>
                  )}
                </>
              )}

            </section>

            {/* DIFFICULTY */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  5. Difficulty
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Choose the difficulty level.
                </p>

              </div>

              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">

                {DIFFICULTIES.map(
                  (item) => {

                    const selected =
                      difficulty ===
                      item;

                    return (
                      <button
                        key={item}
                        onClick={() =>
                          setDifficulty(
                            item
                          )
                        }
                        className={`p-3.5 rounded-xl border-2 text-sm font-semibold transition ${
                          selected
                            ? "border-[#2563eb] bg-[#eff6ff] text-[#1d4ed8]"
                            : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                        }`}
                      >
                        {item}
                      </button>
                    );
                  }
                )}

              </div>

            </section>

            {/* PRESETS */}

            <section className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm p-6">

              <div className="mb-5">

                <h2 className="text-lg font-semibold">
                  6. Choose Test Preset
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  Choose a fixed test length.
                  Questions, marks and duration
                  are automatically determined.
                </p>

              </div>

              {!studentGroup && (
                <div className="rounded-xl bg-[#fff7ed] border border-[#fed7aa] p-4 text-sm text-[#9a3412]">
                  Select PCM or PCB above to
                  view the available presets.
                </div>
              )}

              {studentGroup && (
                <div className="space-y-3">

                  {availablePresets
                    .filter(
                      (preset) =>
                        presetMatchesSelectedSubjects(
                          preset
                        )
                    )
                    .map(
                      (preset) => {

                        const details =
                          calculatePreset(
                            preset
                          );

                        const selected =
                          selectedPreset?.id ===
                          preset.id;

                        const subjectSplit =
                          Object.entries(
                            preset.subjects
                          )
                            .map(
                              (
                                [
                                  subject,
                                  count,
                                ]
                              ) =>
                                `${
                                  PRESET_SUBJECT_NAMES[
                                    subject
                                  ]
                                } ${count}`
                            )
                            .join(
                              " + "
                            );

                        return (
                          <button
                            key={
                              preset.id
                            }
                            type="button"
                            onClick={() =>
                              setSelectedPreset(
                                preset
                              )
                            }
                            className={`relative w-full text-left rounded-xl border-2 p-4 transition ${
                              selected
                                ? "border-[#2563eb] bg-[#eff6ff]"
                                : "border-[#e5e7eb] hover:border-[#bfdbfe]"
                            }`}
                          >

                            {selected && (
                              <div className="absolute top-4 right-4 w-5 h-5 rounded-full bg-[#2563eb] text-white flex items-center justify-center text-xs">
                                ✓
                              </div>
                            )}

                            <div className="flex items-start justify-between gap-4 pr-8">

                              <div>

                                <div className="font-semibold">
                                  {
                                    preset.name
                                  }
                                </div>

                                <div className="text-xs text-[#6b7280] mt-1">
                                  {
                                    subjectSplit
                                  }
                                  {" questions per subject"}
                                </div>

                              </div>

                              {preset.examAccurate && (
                                <span className="shrink-0 text-[10px] font-semibold uppercase tracking-wide bg-green-100 text-green-700 px-2 py-1 rounded-md">
                                  Actual MHT CET pattern
                                </span>
                              )}

                            </div>

                            <div className="flex flex-wrap gap-2 mt-4">

                              <span className="px-3 py-1.5 rounded-lg bg-white border border-[#e5e7eb] text-xs font-semibold">
                                {
                                  details.totalQuestions
                                }{" "}
                                questions
                              </span>

                              <span className="px-3 py-1.5 rounded-lg bg-white border border-[#e5e7eb] text-xs font-semibold">
                                {
                                  details.totalMarks
                                }{" "}
                                marks
                              </span>

                              <span className="px-3 py-1.5 rounded-lg bg-white border border-[#e5e7eb] text-xs font-semibold">
                                {
                                  details.durationMinutes
                                }{" "}
                                minutes
                              </span>

                            </div>

                          </button>
                        );
                      }
                    )}

                  {availablePresets.filter(
                    (preset) =>
                      presetMatchesSelectedSubjects(
                        preset
                      )
                  ).length ===
                    0 && (
                    <div className="rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-4 text-sm text-[#6b7280]">
                      No presets are available
                      for the selected subject
                      combination.
                    </div>
                  )}

                </div>
              )}

            </section>

          </div>

          {/* SUMMARY */}

          <aside className="lg:sticky lg:top-6 h-fit">

            <div className="bg-white border border-[#e5e7eb] rounded-2xl shadow-sm overflow-hidden">

              <div className="p-6 border-b border-[#e5e7eb]">

                <div className="text-xs font-semibold uppercase tracking-wider text-[#6b7280]">
                  Test Summary
                </div>

                <h2 className="text-2xl font-bold mt-2">
                  {course}
                </h2>

                <p className="text-sm text-[#6b7280] mt-1">
                  {subjects.join(
                    " + "
                  )}
                </p>

              </div>

              <div className="p-6 space-y-5">

                <SummaryRow
                  label="Exam"
                  value={course}
                />

                <SummaryRow
                  label="Group"
                  value={
                    studentGroup ||
                    "Not selected"
                  }
                />

                <SummaryRow
                  label="Subjects"
                  value={
                    subjects.join(
                      ", "
                    )
                  }
                />

                <SummaryRow
                  label="Chapters"
                  value={
                    selectedChapters.length ===
                    0
                      ? "Entire selected subjects"
                      : `${selectedChapters.length} selected`
                  }
                />

                <SummaryRow
                  label="Difficulty"
                  value={
                    difficulty
                  }
                />

                <SummaryRow
                  label="Preset"
                  value={
                    selectedPreset
                      ? selectedPreset.name
                      : "Not selected"
                  }
                />

                <SummaryRow
                  label="Questions"
                  value={
                    presetDetails
                      ? `${presetDetails.totalQuestions}`
                      : "—"
                  }
                />

                <SummaryRow
                  label="Marks"
                  value={
                    presetDetails
                      ? `${presetDetails.totalMarks}`
                      : "—"
                  }
                />

                <SummaryRow
                  label="Duration"
                  value={
                    presetDetails
                      ? `${presetDetails.durationMinutes} min`
                      : "—"
                  }
                />

                <div className="pt-2">

                  <button
                    onClick={
                      generateTest
                    }
                    disabled={
                      generating ||
                      !studentGroup ||
                      !selectedPreset ||
                      !presetDetails
                    }
                    className="w-full h-12 rounded-xl bg-[#1d4ed8] text-white text-sm font-semibold hover:bg-[#1e40af] disabled:opacity-60 disabled:cursor-not-allowed transition"
                  >
                    {generating
                      ? "Generating Test..."
                      : "Generate Test →"}
                  </button>

                </div>

                <p className="text-[11px] leading-relaxed text-[#9ca3af] text-center">
                  Questions will be selected from
                  the Paper Tree question bank
                  according to your configuration.
                </p>

                <div className="rounded-xl bg-[#f9fafb] border border-[#e5e7eb] p-3 text-[11px] text-[#6b7280] text-center">
                  No negative marking. Wrong and
                  unattempted questions score zero.
                </div>

              </div>

            </div>

          </aside>

        </div>

      </div>

    </main>
  );
}

/*
 * ---------------------------------------------------------
 * SUMMARY ROW
 * ---------------------------------------------------------
 */

function SummaryRow({
  label,
  value,
}: {
  label: string;
  value: string;
}) {
  return (
    <div className="flex items-center justify-between gap-4">

      <span className="text-sm text-[#6b7280]">
        {label}
      </span>

      <span className="text-sm font-semibold text-right">
        {value}
      </span>

    </div>
  );
}