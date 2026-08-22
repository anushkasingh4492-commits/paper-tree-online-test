import type { Question } from "@/types/question";

export const mhtCetQuestions: Question[] = [
  {
    id: "mht-phy-001",
    exam: "MHT-CET",
    subject: "Physics",
    chapter: "Rotational Motion",
    difficulty: "Easy",
    question:
      "The SI unit of angular velocity is:",
    options: [
      "m/s",
      "rad/s",
      "rad/s²",
      "m/s²",
    ],
    answer: 1,
    explanation:
      "Angular velocity is measured in radians per second.",
  },

  {
    id: "mht-phy-002",
    exam: "MHT-CET",
    subject: "Physics",
    chapter: "Rotational Motion",
    difficulty: "Medium",
    question:
      "The moment of inertia of a body depends on:",
    options: [
      "Only its mass",
      "Only its angular velocity",
      "Distribution of mass about the axis",
      "Only its radius",
    ],
    answer: 2,
    explanation:
      "Moment of inertia depends on how mass is distributed relative to the axis of rotation.",
  },

  {
    id: "mht-phy-003",
    exam: "MHT-CET",
    subject: "Physics",
    chapter: "Thermodynamics",
    difficulty: "Easy",
    question:
      "The first law of thermodynamics is based on conservation of:",
    options: [
      "Momentum",
      "Charge",
      "Energy",
      "Mass",
    ],
    answer: 2,
    explanation:
      "The first law expresses conservation of energy.",
  },

  {
    id: "mht-chem-001",
    exam: "MHT-CET",
    subject: "Chemistry",
    chapter: "Electrochemistry",
    difficulty: "Easy",
    question:
      "The SI unit of conductance is:",
    options: [
      "Ohm",
      "Siemens",
      "Volt",
      "Ampere",
    ],
    answer: 1,
    explanation:
      "Conductance is measured in Siemens.",
  },

  {
    id: "mht-chem-002",
    exam: "MHT-CET",
    subject: "Chemistry",
    chapter: "Chemical Kinetics",
    difficulty: "Medium",
    question:
      "The rate of a chemical reaction generally increases with:",
    options: [
      "Decrease in temperature",
      "Increase in temperature",
      "Decrease in concentration",
      "Removal of reactants",
    ],
    answer: 1,
    explanation:
      "Increasing temperature generally increases reaction rate.",
  },

  {
    id: "mht-math-001",
    exam: "MHT-CET",
    subject: "Mathematics",
    chapter: "Probability",
    difficulty: "Easy",
    question:
      "The probability of an event that is certain to occur is:",
    options: [
      "0",
      "1",
      "1/2",
      "-1",
    ],
    answer: 1,
    explanation:
      "A certain event has probability 1.",
  },

  {
    id: "mht-math-002",
    exam: "MHT-CET",
    subject: "Mathematics",
    chapter: "Differentiation",
    difficulty: "Easy",
    question:
      "The derivative of x² with respect to x is:",
    options: [
      "x",
      "2x",
      "x²",
      "2",
    ],
    answer: 1,
    explanation:
      "Using the power rule, d(x²)/dx = 2x.",
  },
];
