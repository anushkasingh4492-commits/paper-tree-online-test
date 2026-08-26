export type StudentGroup = "PCM" | "PCB";

export type PresetSubject =
  | "physics"
  | "chemistry"
  | "maths"
  | "biology";

export type Preset = {
  id: string;
  name: string;
  subjects: Partial<Record<PresetSubject, number>>;
  examAccurate?: boolean;
};

/*
 * ---------------------------------------------------------
 * MARKS
 * ---------------------------------------------------------
 */

export const MARKS_PER_QUESTION: Record<
  PresetSubject,
  number
> = {
  physics: 1,
  chemistry: 1,
  maths: 2,
  biology: 1,
};

/*
 * ---------------------------------------------------------
 * TEST LIMITS
 * ---------------------------------------------------------
 */

export const MINUTES_PER_MARK = 0.9;
export const ROUND_MINUTES = 5;

export const MAX_MARKS = 200;
export const MAX_DURATION = 180;

/*
 * ---------------------------------------------------------
 * SUBJECTS AVAILABLE FOR EACH GROUP
 * ---------------------------------------------------------
 */

export const GROUP_SUBJECTS: Record<
  StudentGroup,
  PresetSubject[]
> = {
  PCM: [
    "physics",
    "chemistry",
    "maths",
  ],

  PCB: [
    "physics",
    "chemistry",
    "biology",
  ],
};

/*
 * ---------------------------------------------------------
 * PRESETS
 * ---------------------------------------------------------
 */

export const PRESETS: Preset[] = [
  /*
   * -------------------------------------------------------
   * PHYSICS
   * -------------------------------------------------------
   */

  {
    id: "P-15",
    name: "Quick drill",
    subjects: {
      physics: 15,
    },
  },

  {
    id: "P-30",
    name: "Standard",
    subjects: {
      physics: 30,
    },
  },

  {
    id: "P-50",
    name: "Full section",
    subjects: {
      physics: 50,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * CHEMISTRY
   * -------------------------------------------------------
   */

  {
    id: "C-15",
    name: "Quick drill",
    subjects: {
      chemistry: 15,
    },
  },

  {
    id: "C-30",
    name: "Standard",
    subjects: {
      chemistry: 30,
    },
  },

  {
    id: "C-50",
    name: "Full section",
    subjects: {
      chemistry: 50,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * MATHEMATICS
   * -------------------------------------------------------
   */

  {
    id: "M-15",
    name: "Quick drill",
    subjects: {
      maths: 15,
    },
  },

  {
    id: "M-30",
    name: "Standard",
    subjects: {
      maths: 30,
    },
  },

  {
    id: "M-50",
    name: "Full section",
    subjects: {
      maths: 50,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * BIOLOGY
   * -------------------------------------------------------
   */

  {
    id: "B-15",
    name: "Quick drill",
    subjects: {
      biology: 15,
    },
  },

  {
    id: "B-30",
    name: "Standard",
    subjects: {
      biology: 30,
    },
  },

  {
    id: "B-100",
    name: "Full section",
    subjects: {
      biology: 100,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * PHYSICS + CHEMISTRY
   * -------------------------------------------------------
   */

  {
    id: "PC-30",
    name: "Short",
    subjects: {
      physics: 15,
      chemistry: 15,
    },
  },

  {
    id: "PC-50",
    name: "Standard",
    subjects: {
      physics: 25,
      chemistry: 25,
    },
  },

  {
    id: "PC-100",
    name: "Full section",
    subjects: {
      physics: 50,
      chemistry: 50,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * PHYSICS + BIOLOGY
   * -------------------------------------------------------
   */

  {
    id: "PB-30",
    name: "Short",
    subjects: {
      physics: 15,
      biology: 15,
    },
  },

  {
    id: "PB-50",
    name: "Standard",
    subjects: {
      physics: 25,
      biology: 25,
    },
  },

  {
    id: "PB-100",
    name: "Extended",
    subjects: {
      physics: 50,
      biology: 50,
    },
  },

  /*
   * -------------------------------------------------------
   * CHEMISTRY + BIOLOGY
   * -------------------------------------------------------
   */

  {
    id: "CB-30",
    name: "Short",
    subjects: {
      chemistry: 15,
      biology: 15,
    },
  },

  {
    id: "CB-50",
    name: "Standard",
    subjects: {
      chemistry: 25,
      biology: 25,
    },
  },

  {
    id: "CB-100",
    name: "Extended",
    subjects: {
      chemistry: 50,
      biology: 50,
    },
  },

  /*
   * -------------------------------------------------------
   * PHYSICS + MATHEMATICS
   * -------------------------------------------------------
   */

  {
    id: "PM-30",
    name: "Short",
    subjects: {
      physics: 15,
      maths: 15,
    },
  },

  {
    id: "PM-50",
    name: "Standard",
    subjects: {
      physics: 25,
      maths: 25,
    },
  },

  {
    id: "PM-100",
    name: "Extended",
    subjects: {
      physics: 50,
      maths: 50,
    },
  },

  /*
   * -------------------------------------------------------
   * CHEMISTRY + MATHEMATICS
   * -------------------------------------------------------
   */

  {
    id: "CM-30",
    name: "Short",
    subjects: {
      chemistry: 15,
      maths: 15,
    },
  },

  {
    id: "CM-50",
    name: "Standard",
    subjects: {
      chemistry: 25,
      maths: 25,
    },
  },

  {
    id: "CM-100",
    name: "Extended",
    subjects: {
      chemistry: 50,
      maths: 50,
    },
  },

  /*
   * -------------------------------------------------------
   * PCM
   * -------------------------------------------------------
   */

  {
    id: "PCM-75",
    name: "Half paper",
    subjects: {
      physics: 25,
      chemistry: 25,
      maths: 25,
    },
  },

  {
    id: "PCM-90",
    name: "Custom length",
    subjects: {
      physics: 30,
      chemistry: 30,
      maths: 30,
    },
  },

  {
    id: "PCM-150",
    name: "Full paper",
    subjects: {
      physics: 50,
      chemistry: 50,
      maths: 50,
    },
    examAccurate: true,
  },

  /*
   * -------------------------------------------------------
   * PCB
   * -------------------------------------------------------
   */

  {
    id: "PCB-100",
    name: "Half paper",
    subjects: {
      physics: 25,
      chemistry: 25,
      biology: 50,
    },
  },

  {
    id: "PCB-90",
    name: "Custom length",
    subjects: {
      physics: 25,
      chemistry: 25,
      biology: 40,
    },
  },

  {
    id: "PCB-200",
    name: "Full paper",
    subjects: {
      physics: 50,
      chemistry: 50,
      biology: 100,
    },
    examAccurate: true,
  },
];

/*
 * ---------------------------------------------------------
 * CALCULATE PRESET
 * ---------------------------------------------------------
 */

export function calculatePreset(
  preset: Preset
) {
  const totalQuestions =
    Object.values(preset.subjects).reduce(
      (sum, count) =>
        sum + (count || 0),
      0
    );

  const totalMarks =
    Object.entries(
      preset.subjects
    ).reduce(
      (sum, [subject, count]) => {
        const marksPerQuestion =
          MARKS_PER_QUESTION[
            subject as PresetSubject
          ];

        return (
          sum +
          (count || 0) *
            marksPerQuestion
        );
      },
      0
    );

  const rawMinutes =
    totalMarks *
    MINUTES_PER_MARK;

  const durationMinutes =
    Math.ceil(
      rawMinutes /
        ROUND_MINUTES
    ) *
    ROUND_MINUTES;

  return {
    totalQuestions,
    totalMarks,
    durationMinutes,

    /*
     * Useful validation values.
     */

    withinMarkLimit:
      totalMarks <= MAX_MARKS,

    withinDurationLimit:
      durationMinutes <=
      MAX_DURATION,

    valid:
      totalMarks <= MAX_MARKS &&
      durationMinutes <=
        MAX_DURATION,
  };
}

/*
 * ---------------------------------------------------------
 * GET PRESETS FOR GROUP
 * ---------------------------------------------------------
 */

export function getPresetsForGroup(
  group: StudentGroup
): Preset[] {
  const allowedSubjects =
    GROUP_SUBJECTS[group];

  return PRESETS.filter(
    (preset) => {
      const presetSubjects =
        Object.keys(
          preset.subjects
        ) as PresetSubject[];

      /*
       * Every subject used by the preset
       * must be available to the group.
       */

      return presetSubjects.every(
        (subject) =>
          allowedSubjects.includes(
            subject
          )
      );
    }
  );
}

/*
 * ---------------------------------------------------------
 * GET PRESET
 * ---------------------------------------------------------
 */

export function getPreset(
  presetId: string
): Preset | undefined {
  return PRESETS.find(
    (preset) =>
      preset.id === presetId
  );
}

/*
 * ---------------------------------------------------------
 * CHECK PRESET SUBJECT COMBINATION
 * ---------------------------------------------------------
 */

export function presetMatchesSubjects(
  preset: Preset,
  subjects: PresetSubject[]
): boolean {
  const presetSubjects =
    Object.keys(
      preset.subjects
    ) as PresetSubject[];

  if (
    presetSubjects.length !==
    subjects.length
  ) {
    return false;
  }

  return (
    presetSubjects.every(
      (subject) =>
        subjects.includes(
          subject
        )
    ) &&
    subjects.every(
      (subject) =>
        presetSubjects.includes(
          subject
        )
    )
  );
}