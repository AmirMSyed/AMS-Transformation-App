import React, { useState, useEffect, useRef } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, onSnapshot, collection, addDoc, query, getDocs, where, Timestamp } from 'firebase/firestore';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ArrowRight, ChevronLeft, ChevronRight, Dumbbell, Flame, Target, Weight, Pizza, CheckCircle, PlusCircle, Calendar, BarChart2, Home, User, Settings as SettingsIcon, HeartPulse, Moon, X, Bot, Send, BookOpen, Check, Utensils, Drumstick } from 'lucide-react';

// --- Firebase Configuration ---
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

// --- Firebase Initialization ---
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// --- FULL DOCUMENT TEXT FOR VIEWER AND CHATBOT ---
const PLAN_DOC_TEXT = `
An Adaptive 10-Month Blueprint for Sustainable Physique Transformation

I. Executive Summary: An Enhanced 10-Month Adaptive Transformation Blueprint

A. Purpose of This Revised Document
This document presents a meticulously revised 10-month fitness and nutrition plan, building upon the robust foundation of the "Revised 10-Month Blueprint for Sustainable Physique Transformation". It has been specifically tailored to incorporate valuable feedback, aiming for a more granular, adaptive, and personalized pathway toward the established transformation goals. The primary objectives remain the achievement of a 70-pound fat loss and a 10-pound gain in lean muscle mass, culminating in a projected body weight of approximately 245 lbs and a body fat percentage of around 19-20%. This endeavor represents a significant commitment to health and well-being, and this plan is designed to provide a structured, evidence-based pathway.

B. Key Enhancements Based on Feedback
To optimize the journey and align more closely with individual preferences and needs, several key enhancements have been integrated:
- Ten Distinct Monthly Phases: The comprehensive 10-month plan is now segmented into ten individual monthly phases. Each phase will feature specific, progressive targets for nutrition, strength training, and cardiovascular exercise. This structure facilitates continuous adaptation, allows for regular progress reviews, and is intended to maximize adherence and long-term results.
- Adjusted Initial Workout Frequency: Recognizing the importance of a sustainable start, Month 1 will commence with two full-body dumbbell workouts per week. These sessions will be separated by three to four days to ensure adequate recovery and foster the development of consistent exercise habits.
- Refined Cardio Protocol: The cardiovascular exercise plan has been updated to include preferences for slow, steady walks, variable-intensity elliptical training (25-45 minutes per session), and the strategic introduction of moderate jogging once a significant weight loss milestone (approximately 40-50 pounds) is achieved. Intensity for cardiovascular exercise will be guided using the Rate of Perceived Exertion (RPE) scale.
- Explicit Intensity Guidance for Strength Training: To ensure clarity and appropriate stimulus, strength training intensity will be prescribed using Reps in Reserve (RIR) and the RPE scale. The plan will begin with a conservative intensity, systematically increasing as strength and work capacity improve.
- Monthly Recalibrations: All components of the plan, including caloric intake, macronutrient distribution, and training variables, will be reviewed and adjusted on a monthly basis. More frequent micro-adjustments may be considered if progress tracking indicates a need, ensuring the plan remains responsive to physiological changes.

C. Commitment to Scientific Rigor
Every recommendation within this enhanced plan is underpinned by established scientific principles of exercise physiology, nutrition science, and behavioral science. The objective extends beyond simply providing a regimen; it aims to empower the individual with an understanding of the physiological and metabolic rationale behind each component, fostering a deeper engagement with the transformation process and equipping them with knowledge for sustained health.

II. Reaffirming Transformation Goals & Our Scientific Approach

A. The Starting Point
An accurate understanding of the initial baseline is crucial for effective planning and realistic goal setting. The following metrics serve as this foundation:
- Age: 30 years
- Height: 6'2" (188 cm)
- Starting Weight: 305 lbs (138.3 kg)
- Starting Body Fat Percentage (Estimated): 38.5%
- Derived Starting Lean Body Mass (LBM): 187.575 lbs (85.08 kg)
- Derived Starting Fat Mass (FM): 117.425 lbs (53.26 kg)
- Calculated Basal Metabolic Rate (BMR) (Katch-McArdle Formula): BMR=370+(21.6×LBM in kg)): Approximately 2208 kcal/day
- Initial Total Daily Energy Expenditure (TDEE) (Lightly Active multiplier of 1.375): Approximately 3036 kcal/day

B. The Ambitious Yet Achievable 10-Month Targets
The overarching goals for this 10-month period remain consistent:
- Target Fat Loss: 70 pounds (averaging 1.75 lbs per week)
- Target Muscle Gain: 10 pounds (averaging 1 lb per month)
- Projected End Weight: Approximately 245 pounds
- Projected End Body Fat Percentage: Approximately 19.4%

These targets are substantial and require consistent dedication. However, they are physiologically plausible within the 10-month timeframe, particularly considering the starting point.

C. The "Novice Effect" & Body Recomposition
A key factor supporting the feasibility of simultaneous fat loss and muscle gain (body recomposition) is the "novice effect". Individuals who are relatively new to consistent, structured resistance training, especially those starting with a higher body fat percentage, often experience more rapid initial gains in muscle mass, even while in a caloric deficit. This plan is strategically designed to leverage this period of enhanced responsiveness to training.

D. Core Scientific Principles Guiding This Plan
The design of this transformation plan rests upon several fundamental scientific principles:
- Energy Balance for Fat Loss: The cornerstone of fat loss is the creation of a sustained negative energy balance, meaning more calories are expended than consumed. One pound of body fat is approximately equivalent to 3500 kcal; thus, a consistent daily caloric deficit is required to achieve the 70-pound fat loss goal.
- Protein for Muscle Preservation & Growth: During a caloric deficit, adequate protein intake is paramount. A higher protein intake, targeted here at approximately 2.4 g/kg of LBM, supports muscle protein synthesis, helps preserve existing lean mass, and contributes to satiety, which is beneficial for dietary adherence.
- Progressive Overload for Strength & Hypertrophy: For muscles to adapt and grow stronger and larger, they must be subjected to progressively increasing demands. Given the limitation of dumbbell weights (10 lb, 20 lb, 30 lb), progressive overload will be achieved through a variety of methods. These include increasing repetitions, adding sets, enhancing time under tension (TUT) by controlling movement tempo, reducing rest periods between sets, employing unilateral (single-limb) exercises, and progressing to more challenging exercise variations.
- Metabolic Adaptation: The human body is highly adaptive. Prolonged caloric deficits and consistent training stimuli can lead to metabolic adaptations, where the body becomes more efficient and TDEE may decrease more than predicted by weight loss alone. The requested monthly adjustments are a proactive strategy to address these adaptations. By regularly recalibrating caloric targets based on changes in body weight and composition, and by introducing variations in training stimuli, the plan aims to mitigate the extent of these adaptations and prevent progress from stalling. This dynamic approach transforms the plan from a static prescription into a responsive guide, better aligning with the body's ongoing changes.
- Specificity of Training: Exercises have been selected to effectively target all major muscle groups using the available dumbbell equipment, ensuring a balanced development of strength and muscle.
- Individual Response & Auto-regulation: It is recognized that individuals respond differently to exercise and nutrition plans. The incorporation of tools like Rate of Perceived Exertion (RPE) and Reps in Reserve (RIR) allows for a degree of auto-regulation, enabling adjustments based on daily readiness levels and subjective experience.

E. Introducing Workout Intensity Gauges: RPE & RIR
To effectively manage and progress workout intensity, particularly with fixed dumbbell increments, two subjective scales will be utilized:
- Rate of Perceived Exertion (RPE): RPE is a subjective assessment of how hard an individual feels their body is working during physical activity. For cardiovascular exercise, the Modified Borg CR10 RPE scale (ranging from 0 to 10) will be employed:
    - 0: No exertion (at rest)
    - 1: Very light activity
    - 2-3: Light activity (comfortable, easy breathing, can sing or whistle)
    - 4-5: Moderate activity (breathing noticeably, can hold a conversation with some effort)
    - 6-7: Vigorous activity (breathing deeply, can only speak in short sentences)
    - 8-9: Very hard activity (breathing very heavily, can barely speak a few words)
    - 10: Maximum effort (cannot sustain for more than a few seconds) This scale helps in tuning into the body's signals—such as breathing rate, heart rate, muscle fatigue, and perspiration—to guide cardiovascular intensity to the intended level for optimal benefits without overexertion, especially crucial in the initial phases of the plan.
- Reps in Reserve (RIR): RIR is a method for gauging intensity in strength training by estimating how many more repetitions could have been performed with good form at the end of a set before reaching technical (form) failure.
    - 0 RIR (corresponds to RPE 10): True muscular failure; no additional repetitions possible with proper technique.
    - 1 RIR (RPE 9): One more repetition could have been completed.
    - 2 RIR (RPE 8): Two more repetitions could have been completed.
    - 3 RIR (RPE 7): Three more repetitions could have been completed.
    - 4+ RIR (RPE <7): More than three repetitions remaining; the set felt relatively easy. The use of RIR allows for auto-regulation of training loads. On days when feeling strong and well-rested, the prescribed RIR might be achieved with a slightly heavier dumbbell or more repetitions. Conversely, on days with higher fatigue, a lighter dumbbell or fewer repetitions might be necessary to match the target RIR. This adaptability is particularly valuable when dumbbell increments are fixed, as it allows for consistent effort and stimulus even if the absolute load cannot be finely tuned. For muscle hypertrophy, an RIR of 0-2 is often considered optimal, while for strength development, an RIR of 2-4 can be effective. This plan will generally start with higher RIR values (less strenuous) and progressively decrease them (more strenuous) as fitness improves. This approach empowers the individual with tools for self-monitoring and intensity management, fostering a greater understanding of their body's response to training and enhancing the effectiveness of the program with limited equipment.
`;

const SCHEDULE_DOC_TEXT = `Your 10-Month Workout Compass: A Weekly Guide to Physique Transformation

1. Introduction: Your 10-Month Workout Compass

Purpose of this Document
This document serves as the practical, actionable workout schedule companion to the "Adaptive 10-Month Blueprint for Sustainable Physique Transformation". Its core function is to translate the comprehensive monthly strategies outlined in that blueprint into a detailed, week-by-week exercise plan for the entire 10-month duration. The aim is to provide absolute clarity on daily exercise requirements, intensity parameters such as Rate of Perceived Exertion (RPE) and Reps in Reserve (RIR), and specific progression methods. This ensures that the individual undertaking this transformation journey knows precisely what to do each day to effectively work towards the established goals.

How to Use This Schedule
It is paramount to understand that this schedule is not a standalone document. Its effective use is contingent upon its integration with the main "Adaptive 10-Month Blueprint for Sustainable Physique Transformation". The main blueprint provides the crucial "why" behind the program: the physiological rationale, detailed nutritional guidance (including monthly recalibrations of caloric and macronutrient targets), and strategies for adapting the plan as progress is made. These elements are critical for overall success, as consistent adherence to the nutritional protocols detailed in the main blueprint is equally vital for achieving the desired physique transformation. This document, in contrast, focuses exclusively on the "what" and "how" of the exercise component of the plan.

To maximize effectiveness, it is recommended to first read the overview section provided at the beginning of each month within this document. This overview will reiterate the specific focus, training variables, and progression strategies for that particular phase, all derived from the main blueprint.

The successful execution of this workout schedule is deeply intertwined with adherence to the nutritional and recalibration protocols detailed in the foundational blueprint. The ambitious goals of a 70-pound fat loss and a 10-pound muscle gain are predicated on a synergistic approach where exercise and nutrition work in concert. The workout schedule provides the stimulus for muscle growth and caloric expenditure, but the nutritional strategy creates the necessary caloric deficit for fat loss and provides the building blocks (especially protein) for muscle repair and synthesis. Without the supporting nutritional framework, the efforts in the gym, however diligent, will not yield the transformative results outlined. The "plan" is a comprehensive strategy, and this workout schedule is one of its two core pillars; its success hinges on the strength and consistency of both.

A Note on Your Starting Point
The initial physiological statistics provided (Weight: 304.0 lbs, BMI: 39.0, Body Fat: 39.5%) have been noted and align remarkably well with the baseline metrics used in the foundational "Adaptive 10-Month Blueprint" (Starting Weight: 305 lbs, Starting Body Fat % (Est.): 38.5%). This close correspondence is highly advantageous. The plan's initial calculations for energy expenditure, caloric targets, macronutrient distribution, and initial workout programming are, therefore, already well-suited to the user's current state. This congruence minimizes the need for immediate, significant deviations from the prescribed protocols, fostering a smoother initiation phase and supporting a confident commencement of the transformation journey.

2. Core Training Principles: A Quick Recap

Before embarking on the weekly schedules, it is essential to briefly revisit the core training principles that underpin this 10-month program. These principles, drawn directly from the foundational blueprint, are designed to ensure safe, effective, and sustainable progress.

Understanding Key Training Principles
- Progressive Overload with Limited Equipment: The principle of progressive overload dictates that for muscles to grow stronger and larger, they must be subjected to gradually increasing demands over time. The available equipment consists of 10 lb, 20 lb, and 30 lb dumbbells. While this presents limitations in making small, incremental increases in weight, progressive overload will be strategically achieved through a variety of other methods. These include:
  - Increasing the number of repetitions (reps) performed with a given weight.
  - Increasing the number of sets performed for an exercise.
  - Enhancing Time Under Tension (TUT) by slowing down the movement, particularly the eccentric (lowering) phase.
  - Reducing rest periods between sets to increase workout density.
  - Employing unilateral (single-limb) exercises, which effectively double the load on the working limb compared to bilateral versions with the same dumbbell.
  - Progressing to more challenging exercise variations. This multifaceted approach to progressive overload is crucial given the fixed nature of the available dumbbells, ensuring that muscular adaptation can continue even when simply adding more weight is not an option.

- Rate of Perceived Exertion (RPE) for Cardio: Rate of Perceived Exertion (RPE) is a subjective assessment of how hard the body feels it is working during physical activity. This plan utilizes the Modified Borg CR10 RPE scale, ranging from 0 (no exertion) to 10 (maximum effort). For cardiovascular exercise, RPE helps to guide intensity to the intended level (e.g., light, moderate, vigorous) for optimal benefits without overexertion. This is particularly crucial in the initial phases and allows for intensity adjustments based on how the body feels on any given day.

- Reps in Reserve (RIR) for Strength Training: Reps in Reserve (RIR) is a method for gauging intensity in strength training by estimating how many more repetitions could have been performed with good form at the end of a set before reaching technical (form) failure. For example, an RIR of 2 means two more repetitions could have been completed. This plan will typically start with higher RIR values (e.g., RIR 3, meaning the set is moderately challenging) and progressively decrease them (e.g., to RIR 1-2, meaning the set is taken closer to failure) as fitness improves.

The combined use of RPE for cardiovascular training and RIR for strength training is a cornerstone of this plan's adaptability. This is especially pertinent given the fixed increments of the available dumbbells. Since micro-progressions in load are limited, RIR becomes an indispensable tool for modulating strength training intensity. By adjusting how close to failure each set is taken, the perceived effort and training stimulus can be progressed even when using the same dumbbell. For instance, performing dumbbell presses with a 20 lb dumbbell to an RIR of 3 is less intense and provides a different stimulus than performing the same exercise with the same weight to an RIR of 1. Similarly, RPE allows for consistent cardiovascular stimulus regardless of external factors; an RPE of 4 should feel like an RPE of 4 whether walking outdoors on a cool day or using an elliptical on a warmer day. These subjective intensity measures empower the individual to become an active participant in their training, making the plan responsive to daily fluctuations in energy and recovery. This auto-regulation helps to ensure that the training stimulus is appropriate—neither too little to effect change nor too much to impede recovery or risk injury—thereby fostering adherence and optimizing long-term progress. It shifts the focus from purely external metrics (like weight lifted) to the internal physiological response, which is paramount for sustained adaptation. This active role in managing daily training intensity is a key factor in navigating the long-term demands of the program and developing a deeper understanding of one's own physical responses.

Importance of Warm-ups & Cool-downs
As detailed in the foundational plan, every strength training session must begin with a 5-10 minute warm-up. This should include light cardiovascular activity (like marching in place or arm circles) to increase blood flow, followed by dynamic stretches (such as leg swings and torso twists) targeting the muscles to be worked. Similarly, each strength session should conclude with a 5-10 minute cool-down involving static stretches for the major muscle groups engaged during the workout. Each stretch should be held for 20-30 seconds. These routines are not optional; they are integral for injury prevention, preparing the body for the demands of the workout, improving performance, and aiding in the post-exercise recovery process.

The Non-Negotiable: Consistency and Adherence
The foundational blueprint emphasizes that "Consistency and Adherence: The Non-Negotiables" are paramount for success. The ultimate achievement of the ambitious transformation goals—70-pound fat loss and 10-pound muscle gain—hinges on unwavering consistency in following the nutritional plan (detailed in the main blueprint) and diligently executing the workouts as prescribed in this weekly schedule. Each component of the plan is designed to build upon the previous, and therefore, faithful adherence to the daily and weekly tasks is key to unlocking the full potential of this 10-month program and realizing the projected results.

3. Detailed 10-Month Weekly Workout Schedules
This section provides the week-by-week workout schedules for the entire 10-month duration. Each month begins with an overview of its specific focus and key training variables, followed by guidance on how to progress within that month. The weekly tables then lay out the daily plan.
`;


const MONTHLY_PLAN_DATA = [
  { month: 1, calories: 2230, protein: 205, phase: 1, neat: '7,000-8,000 steps' },
  { month: 2, calories: 2180, protein: 200, phase: 2, neat: '8,000-9,000 steps' },
  { month: 3, calories: 2130, protein: 195, phase: 3, neat: '8,000-10,000 steps' },
  { month: 4, calories: 2080, protein: 190, phase: 3, neat: '8,000-10,000 steps' },
  { month: 5, calories: 2030, protein: 185, phase: 4, neat: '10,000+ steps' },
  { month: 6, calories: 1980, protein: 180, phase: 4, neat: '10,000+ steps' },
  { month: 7, calories: 1930, protein: 175, phase: 4, neat: '10,000+ steps' },
  { month: 8, calories: 1880, protein: 170, phase: 5, neat: '10,000+ steps' },
  { month: 9, calories: 1850, protein: 168, phase: 5, neat: '10,000+ steps' },
  { month: 10, calories: 1820, protein: 165, phase: 5, neat: '10,000+ steps' },
];

const WORKOUTS_DATA = {
    'Full Body A': { type: 'Strength', rir: 3, exercises: [ { name: 'Dumbbell Goblet Squats', sets: '3', reps: '10-15' }, { name: 'Push-ups', sets: '3', reps: 'AMRAP' }, { name: 'Single-Arm DB Rows', sets: '3', reps: '10-12/arm' }, { name: 'Dumbbell RDLs', sets: '3', reps: '12-15' }, { name: 'Dumbbell OHP', sets: '3', reps: '10-15' }, { name: 'Plank', sets: '3', reps: '30-60s' }, ]},
    'Full Body B': { type: 'Strength', rir: 3, exercises: [ { name: 'Dumbbell Lunges', sets: '3', reps: '8-12/leg' }, { name: 'Dumbbell Floor Press', sets: '3', reps: '10-15' }, { name: 'Bent-Over Two-DB Row', sets: '3', reps: '10-15' }, { name: 'Dumbbell Hammer Curls', sets: '2', reps: '12-15' }, { name: 'Dumbbell Triceps Kickbacks', sets: '2', reps: '12-15' }, { name: 'Bird-Dog', sets: '3', reps: '10-12/side' }, ]},
    'Full Body C': { type: 'Strength', rir: '2-3', exercises: [ { name: 'Dumbbell Front Squats', sets: '3', reps: '10-15' }, { name: 'Push-up Variation', sets: '3', reps: 'AMRAP' }, { name: 'Dumbbell Renegade Rows', sets: '3', reps: '8-10/arm' }, { name: 'Dumbbell Glute Bridges', sets: '3', reps: '12-15' }, { name: 'Arnold Press', sets: '3', reps: '10-12' }, { name: 'DB Concentration Curls', sets: '2', reps: '10-15/arm'}, { name: 'DB Lying Triceps Ext', sets: '2', reps: '10-15' }, { name: 'Russian Twists', sets: '3', reps: '15-20' }, ]},
    'Upper Body A': { type: 'Strength', rir: '1-2', progression: 'Focus on unilaterals and shorter rests (60-75s)', exercises: [ { name: 'DB Bench Press', sets: '3-4', reps: '8-12'}, { name: 'Bent-Over Rows', sets: '3-4', reps: '8-10/arm'}, { name: 'DB OHP', sets: '3-4', reps: '8-12'}, { name: 'Lateral Raises', sets: '3', reps: '12-15'}, { name: 'Bicep Curls', sets: '3', reps: '10-15'}, ]},
    'Upper Body B': { type: 'Strength', rir: '1-2', progression: 'Focus on unilaterals and shorter rests (60-75s)', exercises: [ { name: 'Incline DB Press', sets: '3-4', reps: '8-12'}, { name: 'Single-Arm Rows', sets: '3-4', reps: '8-10/arm'}, { name: 'Arnold Press', sets: '3', reps: '10-15'}, { name: 'Hammer Curls', sets: '3', reps: '10-15'}, { name: 'Triceps Extensions', sets: '3', reps: '10-15'}, ]},
    'Lower Body A': { type: 'Strength', rir: '1-2', progression: 'Focus on unilaterals and shorter rests (60-75s)', exercises: [ { name: 'DB Goblet Squats', sets: '3-4', reps: '8-12'}, { name: 'DB RDLs', sets: '3-4', reps: '10-12'}, { name: 'DB Lunges', sets: '3', reps: '8-12/leg'}, { name: 'Calf Raises', sets: '4', reps: '15-20'}, ]},
    'Lower Body B': { type: 'Strength', rir: '1-2', progression: 'Focus on unilaterals and shorter rests (60-75s)', exercises: [ { name: 'Bulgarian Split Squat', sets: '3', reps: '8-12/leg'}, { name: 'DB Glute Bridges', sets: '3-4', reps: '10-15'}, { name: 'Single-Leg RDLs', sets: '3', reps: '8-12/leg'}, { name: 'Hamstring Curls (Bodyweight)', sets: '3', reps: 'AMRAP'}, ]},
    'Upper Body (Advanced)': { type: 'Strength', rir: '0-2', progression: 'Introduce Drop Sets & High Reps', exercises: [ { name: 'DB Bench Press', sets: '3-4', reps: '8-12'}, { name: 'Bent-Over Rows', sets: '3-4', reps: '8-10/arm'}, { name: 'DB OHP', sets: '3-4', reps: '8-12'}, { name: 'Lateral Raises', sets: '3', reps: '15-25'}, { name: 'Bicep Curls', sets: '3', reps: '15-25'}, ]},
    'Lower Body (Advanced)': { type: 'Strength', rir: '0-2', progression: 'Introduce Drop Sets & High Reps', exercises: [ { name: 'DB Goblet Squats', sets: '3-4', reps: '8-12'}, { name: 'DB RDLs', sets: '3-4', reps: '10-12'}, { name: 'DB Lunges', sets: '3', reps: '15-20/leg'}, { name: 'Calf Raises', sets: '4', reps: '20-25'}, ]},
    'Cardio': { type: 'Cardio' },
    'Rest': { type: 'Rest' }
};

const CARDIO_DETAILS_DATA = {
  1: { title: 'LISS Cardio', details: '2-3 sessions per week of 25-35 minutes on a Brisk Walk or Elliptical.', RPE: '3-4 (Light to Moderate)', tip: 'Maintain a conversational pace.' },
  2: { title: 'LISS Progression', details: '2-3 sessions per week, increasing to 30-40 minutes.', RPE: '3-5 (Light to Moderate)', tip: 'Focus on sustainable effort.' },
  3: { title: 'Cardio Intensification', details: '3 sessions per week. Two are LISS at RPE 4-5 for 35-45 mins. One is a Vigorous session at RPE 6-7 for 25-30 mins.', RPE: 'Varies', tip: 'Push yourself on the vigorous day, but ensure good recovery.' },
  4: { title: 'Advanced Cardio & Jogging', details: 'Conditional jogging intro (walk/jog intervals). 1-2 other Elliptical/LISS sessions.', RPE: '5-6 (Jogging)', tip: 'Listen to your joints and progress slowly.' },
  5: { title: 'Peak Cardio', details: '2-3 jogging sessions per week, aiming for 20-30 mins continuous. 1-2 other cardio sessions.', RPE: '5-7 (Jogging)', tip: 'Focus on consistency and performance.' }
};


const generateFullPlan = () => {
    let fullPlan = [];
    for (let week = 1; week <= 40; week++) {
        const monthIndex = Math.floor((week - 1) / 4);
        const monthData = MONTHLY_PLAN_DATA[monthIndex] || MONTHLY_PLAN_DATA[MONTHLY_PLAN_DATA.length - 1];
        
        let weeklySchedule = [];
        
        if (monthData.phase === 1) { 
            weeklySchedule = [
                { day: 'Monday', type: 'Full Body A', details: WORKOUTS_DATA['Full Body A'] },
                { day: 'Tuesday', type: 'Cardio', details: CARDIO_DETAILS_DATA[1] },
                { day: 'Wednesday', type: 'Rest', details: WORKOUTS_DATA['Rest'] },
                { day: 'Thursday', type: 'Cardio', details: CARDIO_DETAILS_DATA[1] },
                { day: 'Friday', type: 'Full Body B', details: WORKOUTS_DATA['Full Body B'] },
                { day: 'Saturday', type: 'Cardio', details: CARDIO_DETAILS_DATA[1] },
                { day: 'Sunday', type: 'Rest', details: WORKOUTS_DATA['Rest'] },
            ];
        } else if (monthData.phase === 2 || monthData.phase === 3) { 
             weeklySchedule = [
                { day: 'Monday', type: 'Full Body A', details: {...WORKOUTS_DATA['Full Body A'], rir: monthData.phase === 2 ? '2-3' : '1-2'} },
                { day: 'Tuesday', type: 'Cardio', details: CARDIO_DETAILS_DATA[monthData.phase] },
                { day: 'Wednesday', type: 'Full Body C', details: {...WORKOUTS_DATA['Full Body C'], rir: monthData.phase === 2 ? '2-3' : '1-2'} },
                { day: 'Thursday', type: 'Cardio', details: CARDIO_DETAILS_DATA[monthData.phase] },
                { day: 'Friday', type: 'Full Body B', details: {...WORKOUTS_DATA['Full Body B'], rir: monthData.phase === 2 ? '2-3' : '1-2'} },
                { day: 'Saturday', type: 'Cardio', details: CARDIO_DETAILS_DATA[monthData.phase] },
                { day: 'Sunday', type: 'Rest', details: WORKOUTS_DATA['Rest'] },
            ];
        } else if (monthData.phase === 4) { 
            weeklySchedule = [
                { day: 'Monday', type: 'Upper Body A', details: WORKOUTS_DATA['Upper Body A'] },
                { day: 'Tuesday', type: 'Lower Body A', details: WORKOUTS_DATA['Lower Body A'] },
                { day: 'Wednesday', type: 'Cardio', details: CARDIO_DETAILS_DATA[4] },
                { day: 'Thursday', type: 'Upper Body B', details: WORKOUTS_DATA['Upper Body B'] },
                { day: 'Friday', type: 'Lower Body B', details: WORKOUTS_DATA['Lower Body B'] },
                { day: 'Saturday', type: 'Cardio', details: CARDIO_DETAILS_DATA[4] },
                { day: 'Sunday', type: 'Rest', details: WORKOUTS_DATA['Rest'] },
            ];
        } else { // Phase 5: Final Push
             weeklySchedule = [
                { day: 'Monday', type: 'Upper Body (Advanced)', details: WORKOUTS_DATA['Upper Body (Advanced)'] },
                { day: 'Tuesday', type: 'Lower Body (Advanced)', details: WORKOUTS_DATA['Lower Body (Advanced)'] },
                { day: 'Wednesday', type: 'Cardio', details: CARDIO_DETAILS_DATA[5] },
                { day: 'Thursday', type: 'Upper Body (Advanced)', details: WORKOUTS_DATA['Upper Body (Advanced)'] },
                { day: 'Friday', type: 'Lower Body (Advanced)', details: WORKOUTS_DATA['Lower Body (Advanced)'] },
                { day: 'Saturday', type: 'Cardio', details: CARDIO_DETAILS_DATA[5] },
                { day: 'Sunday', type: 'Rest', details: WORKOUTS_DATA['Rest'] },
            ];
        }
        
        fullPlan.push({ ...monthData, week, schedule: weeklySchedule });
    }
    return fullPlan;
};

const FULL_PLAN = generateFullPlan();
const getTodayString = () => new Date().toISOString().split('T')[0];
const getWeekNumber = (startDate, currentDate = new Date()) => {
    if (!startDate || !startDate.toDate) return 1;
    const start = startDate.toDate();
    const diff = currentDate.getTime() - start.getTime();
    if (diff < 0) return 1;
    const week = Math.floor(diff / (1000 * 60 * 60 * 24 * 7)) + 1;
    return week > 40 ? 40 : week;
};
const getDayName = (dayIndex) => ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayIndex];


// --- Components ---

const Onboarding = ({ onComplete }) => { /* ... No changes ... */ 
    const [startDate, setStartDate] = useState(getTodayString());
    const [startWeight, setStartWeight] = useState('304');
    const [goalWeight] = useState('245');

    const handleSubmit = (e) => {
        e.preventDefault();
        onComplete({
            startDate: Timestamp.fromDate(new Date(startDate)),
            startWeight: parseFloat(startWeight),
            goalWeight: parseFloat(goalWeight),
        });
    };
    return (
        <div className="min-h-screen bg-gray-900 text-white flex flex-col justify-center items-center p-4">
            <div className="w-full max-w-md bg-gray-800 rounded-2xl shadow-lg p-8 space-y-6">
                <div className="text-center">
                    <Target className="mx-auto h-12 w-12 text-emerald-400" />
                    <h1 className="text-3xl font-bold mt-4">Welcome!</h1>
                    <p className="text-gray-400 mt-2">Let's set up your 10-Month Transformation.</p>
                </div>
                <form onSubmit={handleSubmit} className="space-y-6">
                    <div>
                        <label htmlFor="start-date" className="block text-sm font-medium text-gray-300">Start Date</label>
                        <input type="date" id="start-date" value={startDate} onChange={(e) => setStartDate(e.target.value)}
                            className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 text-white focus:outline-none focus:ring-emerald-500"/>
                    </div>
                    <div>
                        <label htmlFor="start-weight" className="block text-sm font-medium text-gray-300">Starting Weight (lbs)</label>
                        <input type="number" id="start-weight" value={startWeight} onChange={(e) => setStartWeight(e.target.value)}
                            className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 text-white focus:outline-none focus:ring-emerald-500"/>
                    </div>
                     <div>
                        <label htmlFor="goal-weight" className="block text-sm font-medium text-gray-300">Goal Weight (lbs)</label>
                        <input type="number" id="goal-weight" value={goalWeight} readOnly
                            className="mt-1 block w-full bg-gray-700 border-gray-600 rounded-md shadow-sm py-2 px-3 text-gray-400 cursor-not-allowed"/>
                    </div>
                    <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-4 rounded-lg flex items-center justify-center space-x-2">
                        <span>Start My Journey</span>
                        <ArrowRight className="h-5 w-5" />
                    </button>
                </form>
            </div>
        </div>
    );
};

const WeightLogModal = ({ onClose, onLogWeight, latestWeight }) => {
    const [newWeight, setNewWeight] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (!newWeight) return;
        onLogWeight(parseFloat(newWeight));
        onClose();
    };

    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="bg-gray-800 rounded-2xl shadow-lg w-full max-w-sm">
                <div className="p-6">
                    <div className="flex justify-between items-center mb-4">
                        <h2 className="text-xl font-bold text-white">Log Today's Weight</h2>
                        <button onClick={onClose} className="text-gray-400 hover:text-white p-1 rounded-full hover:bg-gray-700">
                            <X size={24} />
                        </button>
                    </div>
                    <form onSubmit={handleSubmit} className="space-y-4">
                        <input
                            type="number"
                            step="0.1"
                            value={newWeight}
                            onChange={(e) => setNewWeight(e.target.value)}
                            placeholder={`Last: ${latestWeight.toFixed(1)} lbs`}
                            className="w-full bg-gray-700 border-gray-600 rounded-lg shadow-sm py-3 px-4 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                            autoFocus
                        />
                        <button type="submit" className="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-3 px-4 rounded-lg transition-transform transform hover:scale-105">
                            Save Weight
                        </button>
                    </form>
                </div>
            </div>
        </div>
    );
};


const WorkoutModal = ({ workoutInfo, onClose }) => {
    if (!workoutInfo) return null;

    const { type, details } = workoutInfo;
    const Icon = type.includes('Rest') ? Moon : (details && details.type === 'Cardio') ? HeartPulse : Dumbbell;
    const color = type.includes('Rest') ? 'text-gray-500' : (details && details.type === 'Cardio') ? 'text-red-500' : 'text-emerald-500';

    return (
        <div className="fixed inset-0 bg-black bg-opacity-75 flex items-center justify-center p-4 z-50">
            <div className="bg-gray-800 rounded-2xl shadow-lg w-full max-w-md max-h-full overflow-y-auto">
                <div className="p-6">
                    <div className="flex justify-between items-start mb-4">
                        <div className="flex items-center">
                            <Icon className={`${color} mr-4 flex-shrink-0`} size={32}/>
                            <div>
                                <h2 className="text-2xl font-bold text-white">{type}</h2>
                                {details && details.type === 'Cardio' && <p className="text-lg text-red-400">{details.title}</p>}
                            </div>
                        </div>
                        <button onClick={onClose} className="text-gray-400 hover:text-white p-1 rounded-full hover:bg-gray-700">
                            <X size={24}/>
                        </button>
                    </div>
                    <div className="space-y-4 text-gray-300">
                        {details && details.type === 'Strength' && (
                            <>
                                {details.progression && <p className="text-sm text-yellow-400 mb-3 p-2 bg-yellow-400/10 rounded-md">Focus: {details.progression}</p>}
                                <ul className="space-y-3">
                                    {details.exercises.map(ex => (
                                        <li key={ex.name} className="flex justify-between p-3 bg-gray-700/50 rounded-lg">
                                            <span className="font-semibold">{ex.name}</span> 
                                            <span className="text-gray-400">{ex.sets}x{ex.reps} @ RIR {details.rir || ex.rir}</span>
                                        </li>
                                    ))}
                                </ul>
                            </>
                        )}
                        {details && details.type === 'Cardio' && (
                          <div className="space-y-3">
                            <p>{details.details}</p>
                            <p className="text-sm text-sky-300 p-2 bg-sky-500/10 rounded-md"><strong>Target RPE:</strong> {details.RPE}</p>
                            <p className="text-sm text-sky-300 mt-2 p-2 bg-sky-500/10 rounded-md"><strong>Pro Tip:</strong> {details.tip}</p>
                          </div>
                        )}
                        {type.includes('Rest') && ( <p>Take a full day to rest and recover. Focus on sleep, hydration, and light stretching if you feel stiff.</p> )}
                    </div>
                     <button onClick={onClose} className="mt-6 w-full bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-lg"> Close </button>
                </div>
            </div>
        </div>
    );
};

const Celebration = () => {
  return (
    <div className="fixed inset-0 pointer-events-none z-[100] overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 text-center">
        <h2 className="text-5xl font-bold text-white drop-shadow-lg animate-celebrate-text">Great Job!</h2>
      </div>
      {[...Array(100)].map((_, i) => {
        const size = Math.random() * 12 + 5;
        return (
            <div
              key={i}
              className="absolute"
              style={{
                left: `${Math.random() * 100}%`,
                top: `${-20 + Math.random() * -100}px`,
                width: `${size}px`,
                height: `${size}px`,
                backgroundColor: ['#34D399', '#FBBF24', '#60A5FA', '#EC4899', '#fff'][Math.floor(Math.random() * 5)],
                borderRadius: Math.random() > 0.5 ? '50%' : '0%',
                animation: `fall-elaborate 4s ${i * 0.03}s linear forwards`,
              }}
            />
        );
      })}
      <style>{`
        @keyframes fall-elaborate {
          0% {
            transform: translateY(-20vh) translateX(0) scale(0) rotate(0deg);
            opacity: 1;
          }
          10% {
             transform: scale(1.2);
          }
          100% {
            transform: translateY(110vh) translateX(${Math.random() * 100 - 50}px) scale(0.5) rotate(${Math.random() * 720}deg);
            opacity: 0;
          }
        }
        @keyframes celebrate-text {
          0%, 100% { transform: scale(1); opacity: 0; }
          10%, 80% { transform: scale(1.1); opacity: 1; }
        }
      `}</style>
    </div>
  );
};


const Dashboard = ({ profile, dailyData, weightHistory, currentPlan, currentWeek, userId }) => {
    const [isWorkoutModalOpen, setIsWorkoutModalOpen] = useState(false);
    const [showCelebration, setShowCelebration] = useState(false);
    const [isWeightModalOpen, setIsWeightModalOpen] = useState(false);
    const [showWorkoutReminder, setShowWorkoutReminder] = useState(false);
    const [showWeighInReminder, setShowWeighInReminder] = useState(false);

    const today = getTodayString();
    const todaysEntry = dailyData[today] || { calories: 0, protein: 0 };
    const latestWeight = (weightHistory && weightHistory.length > 0) ? weightHistory[weightHistory.length - 1].weight : (profile ? profile.startWeight : 0);
    const dayOfWeek = new Date().getUTCDay(); // Sunday = 0
    const dayName = getDayName(dayOfWeek);
    const todaysWorkoutInfo = currentPlan.schedule.find(d => d.day === dayName);

    const isActivityCompleted = !!(dailyData[today] && dailyData[today].activityCompleted);

    useEffect(() => {
        const hour = new Date().getHours();
        if (hour >= 12 && !isActivityCompleted) {
            setShowWorkoutReminder(true);
        }

        const isWeighInDay = [1, 3, 5].includes(dayOfWeek); // Mon, Wed, Fri
        if (isWeighInDay && !(dailyData[today] && dailyData[today].weight)) {
            const lastReminderDate = localStorage.getItem('lastWeighInReminder');
            if (lastReminderDate !== today) {
                setShowWeighInReminder(true);
                localStorage.setItem('lastWeighInReminder', today);
            }
        }

    }, []);


    const handleCheckOff = async () => {
        if (isActivityCompleted) return;
        
        await setDoc(doc(db, `artifacts/${appId}/users/${userId}/dailyData/${today}`), { activityCompleted: true }, { merge: true });
        setShowCelebration(true);
        setTimeout(() => setShowCelebration(false), 4000);
    };
    
    const handleLogWeight = async (weightValue) => {
        const today = getTodayString();
        const dailyRef = doc(db, `artifacts/${appId}/users/${userId}/dailyData/${today}`);
        await setDoc(dailyRef, { weight: weightValue }, { merge: true });
        setIsWeightModalOpen(false);
    };

    const calorieProgress = currentPlan.calories > 0 ? Math.min(100, (todaysEntry.calories / currentPlan.calories) * 100) : 0;
    const proteinProgress = currentPlan.protein > 0 ? Math.min(100, (todaysEntry.protein / currentPlan.protein) * 100) : 0;

    return (
        <>
            {showCelebration && <Celebration />}
            <div className="p-4 md:p-6 space-y-6">
                {showWorkoutReminder && (
                    <div className="bg-yellow-500/20 border-l-4 border-yellow-400 text-yellow-300 p-4 rounded-lg flex justify-between items-center">
                        <div className="flex items-center">
                            <Dumbbell className="mr-3" />
                            <p className="font-semibold">Don't forget your workout today!</p>
                        </div>
                        <button onClick={() => setShowWorkoutReminder(false)}><X size={20} /></button>
                    </div>
                )}

                <h1 className="text-3xl font-bold text-white">Dashboard</h1>
                <p className="text-gray-400">Week {currentWeek} of your 10-Month Plan.</p>

                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
                     <div className="bg-gray-800 rounded-2xl p-6 shadow-lg col-span-1 md:col-span-2 lg:col-span-1">
                        <div className="flex justify-between items-center">
                            <h2 className="text-lg font-semibold text-white">Weight Progress</h2>
                            <button onClick={() => setIsWeightModalOpen(true)} className="text-emerald-400 hover:text-emerald-300 text-sm font-semibold flex items-center gap-1">
                                <PlusCircle size={16}/> Log Weight
                            </button>
                        </div>
                        <p className="text-4xl font-bold text-white mt-2">{latestWeight.toFixed(1)} lbs</p>
                        <p className="text-gray-400">Goal: {profile.goalWeight} lbs</p>
                    </div>
                    <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                        <h2 className="text-lg font-semibold text-white mb-2">Calories</h2>
                        <p className="text-2xl font-bold text-orange-400">{todaysEntry.calories || 0} / {currentPlan.calories} kcal</p>
                        <div className="w-full bg-gray-700 rounded-full h-2.5 mt-3">
                            <div className="bg-orange-500 h-2.5 rounded-full" style={{ width: `${calorieProgress}%` }}></div>
                        </div>
                    </div>
                    <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                        <h2 className="text-lg font-semibold text-white mb-2">Protein</h2>
                        <p className="text-2xl font-bold text-sky-400">{todaysEntry.protein || 0} / {currentPlan.protein} g</p>
                        <div className="w-full bg-gray-700 rounded-full h-2.5 mt-3">
                            <div className="bg-sky-500 h-2.5 rounded-full" style={{ width: `${proteinProgress}%` }}></div>
                        </div>
                    </div>
                    <div className={`bg-gray-800 rounded-2xl p-6 shadow-lg flex flex-col justify-between text-center border-2 transition-colors ${
                        todaysWorkoutInfo.type.includes('Rest') ? 'border-gray-600' : (todaysWorkoutInfo.details && todaysWorkoutInfo.details.type === 'Cardio') ? 'border-red-500' : 'border-emerald-500'
                    }`}>
                        <div>
                            <h2 className="text-lg font-semibold text-white mb-2">Today's Activity</h2>
                            <button onClick={() => setIsWorkoutModalOpen(true)} className="w-full">
                                {todaysWorkoutInfo.type.includes('Rest') ? <Moon className="h-8 w-8 text-gray-500 mx-auto" /> : 
                                (todaysWorkoutInfo.details && todaysWorkoutInfo.details.type === 'Cardio') ? <HeartPulse className="h-8 w-8 text-red-500 mx-auto" /> : 
                                <Dumbbell className="h-8 w-8 text-emerald-500 mx-auto" />}
                                <p className="text-xl font-bold mt-2">{todaysWorkoutInfo.type}</p>
                            </button>
                        </div>
                        <button onClick={handleCheckOff} disabled={isActivityCompleted} className={`w-full mt-4 py-2 rounded-lg font-semibold text-white transition-colors disabled:cursor-not-allowed ${isActivityCompleted ? 'bg-green-500' : 'bg-emerald-600 hover:bg-emerald-700'}`}>
                           {isActivityCompleted ? <CheckCircle className="inline-block mr-2"/> : ''} {isActivityCompleted ? 'Completed!' : 'Mark as Done'}
                        </button>
                    </div>
                </div>

                <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                    <h2 className="text-lg font-semibold text-white mb-4">Weight Trend</h2>
                    <ResponsiveContainer width="100%" height={300}>
                        <LineChart data={weightHistory || []} margin={{ top: 5, right: 20, left: -10, bottom: 5 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#4A5568" />
                            <XAxis dataKey="date" stroke="#A0AEC0" />
                            <YAxis domain={['dataMin - 5', 'dataMax + 5']} stroke="#A0AEC0" />
                            <Tooltip contentStyle={{ backgroundColor: '#1A202C', border: '1px solid #2D3748' }} />
                            <Line type="monotone" dataKey="weight" stroke="#34D399" strokeWidth={2} dot={{ r: 4 }} activeDot={{ r: 8 }} />
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
            {isWorkoutModalOpen && <WorkoutModal workoutInfo={todaysWorkoutInfo} onClose={() => setIsWorkoutModalOpen(false)} />}
            {isWeightModalOpen && <WeightLogModal onClose={() => setIsWeightModalOpen(false)} onLogWeight={handleLogWeight} latestWeight={latestWeight} />}
            {showWeighInReminder && <WeightLogModal onClose={() => setShowWeighInReminder(false)} onLogWeight={handleLogWeight} latestWeight={latestWeight} />}
        </>
    );
};

const Nutrition = ({ profile, dailyData, userId }) => { /* ... No changes ... */ 
    const [date, setDate] = useState(getTodayString());
    const [meals, setMeals] = useState([]);
    const [mealName, setMealName] = useState('');
    const [calories, setCalories] = useState('');
    const [protein, setProtein] = useState('');
    const [isAdding, setIsAdding] = useState(false);
    
    const weekForDate = getWeekNumber(profile.startDate, new Date(date));
    const datePlan = FULL_PLAN[weekForDate -1];
    const dateEntry = dailyData[date] || { calories: 0, protein: 0 };

    useEffect(() => {
        if (!userId || !date) return;
        const mealsRef = collection(db, `artifacts/${appId}/users/${userId}/meals`);
        const q = query(mealsRef, where("date", "==", date));
        
        const unsubscribe = onSnapshot(q, (querySnapshot) => {
            const fetchedMeals = [];
            let totalCalories = 0;
            let totalProtein = 0;
            querySnapshot.forEach((doc) => {
                const mealData = doc.data();
                fetchedMeals.push({ id: doc.id, ...mealData });
                totalCalories += mealData.calories || 0;
                totalProtein += mealData.protein || 0;
            });
            setMeals(fetchedMeals);
            
            const dailyRef = doc(db, `artifacts/${appId}/users/${userId}/dailyData/${date}`);
            setDoc(dailyRef, { calories: totalCalories, protein: totalProtein }, { merge: true });
        });

        return () => unsubscribe();
    }, [date, userId]);
    
    const handleAddMeal = async (e) => {
        e.preventDefault();
        if (!mealName || !calories || !protein || !userId) return;
        const newMeal = { date, name: mealName, calories: parseInt(calories), protein: parseInt(protein) };
        await addDoc(collection(db, `artifacts/${appId}/users/${userId}/meals`), newMeal);
        setMealName(''); setCalories(''); setProtein(''); setIsAdding(false);
    };

    const changeDate = (offset) => {
        const currentDate = new Date(date);
        currentDate.setUTCDate(currentDate.getUTCDate() + offset);
        setDate(currentDate.toISOString().split('T')[0]);
    };

    const calorieProgress = datePlan.calories > 0 ? (dateEntry.calories / datePlan.calories) * 100 : 0;
    const proteinProgress = datePlan.protein > 0 ? (dateEntry.protein / datePlan.protein) * 100 : 0;
    
    return (
        <div className="p-4 md:p-6 space-y-6">
            <div className="flex justify-between items-center">
                <h1 className="text-3xl font-bold text-white">Nutrition</h1>
                <div className="flex items-center bg-gray-800 rounded-lg">
                    <button onClick={() => changeDate(-1)} className="p-2 text-gray-400 hover:text-white"><ChevronLeft/></button>
                    <input type="date" value={date} onChange={(e) => setDate(e.target.value)} className="bg-transparent text-white text-center outline-none p-2"/>
                    <button onClick={() => changeDate(1)} className="p-2 text-gray-400 hover:text-white"><ChevronRight/></button>
                </div>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                    <h2 className="text-lg font-semibold text-white mb-2">Calories</h2>
                    <p className="text-3xl font-bold text-orange-400">{dateEntry.calories} / {datePlan.calories} <span className="text-xl">kcal</span></p>
                    <div className="w-full bg-gray-700 rounded-full h-2.5 mt-3"><div className="bg-orange-500 h-2.5 rounded-full" style={{ width: `${calorieProgress}%` }}></div></div>
                </div>
                <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                    <h2 className="text-lg font-semibold text-white mb-2">Protein</h2>
                    <p className="text-3xl font-bold text-sky-400">{dateEntry.protein} / {datePlan.protein} <span className="text-xl">g</span></p>
                    <div className="w-full bg-gray-700 rounded-full h-2.5 mt-3"><div className="bg-sky-500 h-2.5 rounded-full" style={{ width: `${proteinProgress}%` }}></div></div>
                </div>
            </div>
            <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                <div className="flex justify-between items-center mb-4">
                     <h2 className="text-xl font-semibold text-white">Meals for {new Date(date).toLocaleDateString('en-US', {timeZone: 'UTC', month: 'long', day: 'numeric'})}</h2>
                     <button onClick={() => setIsAdding(!isAdding)} className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-lg flex items-center space-x-2">
                         <PlusCircle size={20}/><span>{isAdding ? 'Cancel' : 'Add Meal'}</span></button>
                </div>
                {isAdding && (
                    <form onSubmit={handleAddMeal} className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-6 p-4 bg-gray-700/50 rounded-lg">
                        <input type="text" placeholder="Meal Name" value={mealName} onChange={e => setMealName(e.target.value)} className="col-span-1 md:col-span-2 bg-gray-700 border-gray-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-emerald-500"/>
                        <input type="number" placeholder="Calories" value={calories} onChange={e => setCalories(e.target.value)} className="bg-gray-700 border-gray-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-emerald-500"/>
                        <input type="number" placeholder="Protein (g)" value={protein} onChange={e => setProtein(e.target.value)} className="bg-gray-700 border-gray-600 rounded-md py-2 px-3 text-white focus:outline-none focus:ring-emerald-500"/>
                        <button type="submit" className="md:col-start-4 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-lg">Log Meal</button>
                    </form>
                )}
                <div className="space-y-4">
                    {meals.length > 0 ? meals.map(meal => (
                        <div key={meal.id} className="flex justify-between items-center bg-gray-700 p-4 rounded-lg">
                            <p className="font-semibold text-white">{meal.name}</p>
                            <div className="flex space-x-4 text-sm">
                                <span className="text-orange-400">{meal.calories} kcal</span>
                                <span className="text-sky-400">{meal.protein}g protein</span>
                            </div>
                        </div>
                    )) : (<div className="text-center py-8 text-gray-400"><Pizza size={48} className="mx-auto text-gray-500"/><p className="mt-2">No meals logged yet.</p></div>)}
                </div>
            </div>
        </div>
    );
};
const Workout = ({ profile }) => {
    const [currentWeek, setCurrentWeek] = useState(getWeekNumber(profile.startDate));
    const [expandedDay, setExpandedDay] = useState(getDayName(new Date().getUTCDay()));
    const weekData = FULL_PLAN[currentWeek - 1];

    return (
      <div className="p-4 md:p-6 space-y-6">
        <div className="flex justify-between items-center">
            <h1 className="text-3xl font-bold text-white">Weekly Workout Plan</h1>
            <div className="flex items-center bg-gray-800 rounded-lg">
                <button onClick={() => setCurrentWeek(w => Math.max(1, w - 1))} className="p-3 text-gray-400 hover:text-white"><ChevronLeft/></button>
                <span className="font-bold text-white text-center w-24">Week {currentWeek}</span>
                <button onClick={() => setCurrentWeek(w => Math.min(40, w + 1))} className="p-3 text-gray-400 hover:text-white"><ChevronRight/></button>
            </div>
        </div>
        
        <div className="space-y-2">
            {weekData.schedule.map((day, index) => {
                const isExpanded = expandedDay === day.day;
                const Icon = day.type.includes('Rest') ? Moon : (day.details && day.details.type === 'Cardio') ? HeartPulse : Dumbbell;
                const color = day.type.includes('Rest') ? 'text-gray-500' : (day.details && day.details.type === 'Cardio') ? 'text-red-500' : 'text-emerald-500';

                return (
                    <div key={index} className="bg-gray-800 rounded-lg overflow-hidden">
                        <button onClick={() => setExpandedDay(isExpanded ? null : day.day)} className="w-full flex items-center p-4 text-left">
                            <Icon className={`${color} mr-4 flex-shrink-0`} size={24}/>
                            <div className="flex-1">
                                <p className="text-sm text-gray-400">{day.day}</p>
                                <p className="text-lg font-bold text-white">{day.type}</p>
                            </div>
                            <ChevronRight className={`transform transition-transform ${isExpanded ? 'rotate-90' : ''}`} />
                        </button>
                        {isExpanded && (
                            <div className="p-4 border-t border-gray-700 bg-gray-800/50">
                                {day.details && day.details.type === 'Strength' && (
                                    <>
                                        {day.details.progression && <p className="text-sm text-yellow-400 mb-3 p-2 bg-yellow-400/10 rounded-md">Focus: {day.details.progression}</p>}
                                        <ul className="space-y-3 text-gray-300">
                                            {day.details.exercises.map(ex => <li key={ex.name} className="flex justify-between"><span>{ex.name}</span> <span className="text-gray-400">{ex.sets}x{ex.reps} @RIR {day.details.rir || ex.rir}</span></li>)}
                                        </ul>
                                    </>
                                )}
                                {day.details && day.details.type === 'Cardio' && (
                                    <div className="space-y-3">
                                        <h3 className="font-bold text-lg text-red-400">{day.details.title}</h3>
                                        <p className="text-gray-300">{day.details.details}</p>
                                        <div className="text-sm text-sky-300 p-3 bg-sky-500/10 rounded-md">
                                          <p><strong>Target RPE:</strong> {day.details.RPE}</p>
                                          <p className="mt-1"><strong>Pro Tip:</strong> {day.details.tip}</p>
                                        </div>
                                    </div>
                                )}
                                {day.type.includes('Rest') && (
                                    <p className="text-gray-300">Take a full day to rest and recover.</p>
                                )}
                            </div>
                        )}
                    </div>
                )
            })}
        </div>
      </div>
    );
};
const Plan = ({ profile }) => { /* ... No changes ... */ 
    return (
        <div className="p-4 md:p-6 space-y-6">
            <h1 className="text-3xl font-bold text-white">Your 10-Month Transformation Plan</h1>
            <div className="space-y-4">
                {FULL_PLAN.slice(0, 40).map(week => (
                    <div key={week.week} className="bg-gray-800 p-5 rounded-xl shadow-lg">
                        <h2 className="text-xl font-bold text-emerald-400">Week {week.week} (Month {week.month})</h2>
                        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mt-3 text-center">
                            <div className="bg-gray-700/50 p-3 rounded-lg">
                                <p className="text-sm text-gray-400">Phase</p>
                                <p className="font-bold text-lg">{week.phase}</p>
                            </div>
                            <div className="bg-gray-700/50 p-3 rounded-lg">
                                <p className="text-sm text-gray-400">Calories</p>
                                <p className="font-bold text-lg">{week.calories} kcal</p>
                            </div>
                             <div className="bg-gray-700/50 p-3 rounded-lg">
                                <p className="text-sm text-gray-400">Protein</p>
                                <p className="font-bold text-lg">{week.protein} g</p>
                            </div>
                             <div className="bg-gray-700/50 p-3 rounded-lg">
                                <p className="text-sm text-gray-400">NEAT Target</p>
                                <p className="font-bold text-xs md:text-sm">{week.neat}</p>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    )
};
const Progress = ({ profile, dailyData }) => {
    const startDate = profile.startDate.toDate();
    const totalDays = 10 * 4 * 7; 
    const allDates = [...Array(totalDays)].map((_, i) => {
        const date = new Date(startDate);
        date.setDate(startDate.getDate() + i);
        return date.toISOString().split('T')[0];
    });

    return (
        <div className="p-4 md:p-6 space-y-8">
            <h1 className="text-3xl font-bold text-white">Progress Overview</h1>

            <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                <h2 className="text-xl font-semibold text-white mb-4">Daily Scorecard</h2>
                <div className="flex overflow-x-auto space-x-2 pb-4">
                    {allDates.map(dateStr => {
                         const week = getWeekNumber(profile.startDate, new Date(dateStr));
                         const planForDay = FULL_PLAN[week - 1];
                         const dayData = dailyData[dateStr];

                         const caloriesMet = dayData && planForDay ? (dayData.calories || 0) > 0 && (dayData.calories || 0) <= planForDay.calories : false;
                         const proteinMet = dayData && planForDay ? (dayData.protein || 0) >= planForDay.protein : false;
                         const workoutMet = dayData && dayData.activityCompleted;

                        return (
                            <div key={dateStr} className="flex-shrink-0 w-36 bg-gray-700 p-3 rounded-lg flex flex-col items-center justify-between">
                                <p className="font-bold text-sm text-white">{new Date(dateStr).toLocaleDateString('en-US', {timeZone: 'UTC', month: 'short', day: 'numeric' })}</p>
                                <div className="space-y-2 mt-2 w-full">
                                    <div title={`Calories: ${dayData ? dayData.calories || 0 : 0} / ${planForDay.calories}`} className={`flex items-center justify-between text-xs p-1 rounded ${caloriesMet ? 'bg-green-500/20 text-green-400' : dayData && dayData.calories > 0 ? 'bg-red-500/20 text-red-400' : 'bg-gray-600 text-gray-400'}`}>
                                        <Utensils size={14}/>
                                        <span>{caloriesMet ? 'Met' : 'Miss'}</span>
                                    </div>
                                     <div title={`Protein: ${dayData ? dayData.protein || 0 : 0} / ${planForDay.protein}`} className={`flex items-center justify-between text-xs p-1 rounded ${proteinMet ? 'bg-green-500/20 text-green-400' : dayData && dayData.protein > 0 ? 'bg-red-500/20 text-red-400' : 'bg-gray-600 text-gray-400'}`}>
                                        <Drumstick size={14}/>
                                        <span>{proteinMet ? 'Met' : 'Miss'}</span>
                                    </div>
                                    <div className={`flex items-center justify-between text-xs p-1 rounded ${workoutMet ? 'bg-green-500/20 text-green-400' : 'bg-gray-600 text-gray-400'}`}>
                                       <Dumbbell size={14}/>
                                        <span>{workoutMet ? 'Done' : 'Pending'}</span>
                                    </div>
                                </div>
                            </div>
                        )
                    })}
                </div>
            </div>
        </div>
    );
};
const Settings = ({ profile, userId, weightHistory }) => {
    return (
        <div className="p-4 md:p-6 space-y-6">
            <h1 className="text-3xl font-bold text-white">Settings</h1>
             <div className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                <h2 className="text-xl font-semibold text-white mb-4">User Info</h2>
                <p className="text-gray-400">User ID: <span className="text-xs text-gray-500">{userId}</span></p>
                <p className="text-gray-400">Plan Start Date: <span className="text-white">{profile && profile.startDate ? profile.startDate.toDate().toLocaleDateString() : 'N/A'}</span></p>
                <p className="text-gray-400">Starting Weight: <span className="text-white">{profile ? profile.startWeight : 'N/A'} lbs</span></p>
                 <p className="text-gray-400">Goal Weight: <span className="text-white">{profile ? profile.goalWeight : 'N/A'} lbs</span></p>
            </div>
        </div>
    );
};

const Chatbot = ({ planContext }) => { /* ... No changes ... */ 
    const [messages, setMessages] = useState([
        { role: 'bot', text: "Hello! I'm your AI fitness assistant. Ask me anything about your 10-month plan." }
    ]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages]);

    const handleSend = async () => {
        if (!input.trim()) return;

        const userMessage = { role: 'user', text: input };
        setMessages(prev => [...prev, userMessage]);
        setInput('');
        setIsLoading(true);

        const prompt = `Based *only* on the provided fitness plan documents, answer the following user question.
        User Question: "${input}"
        
        Fitness Plan Context:
        ${planContext}`;

        try {
            let chatHistory = [];
            chatHistory.push({ role: "user", parts: [{ text: prompt }] });
            const payload = { contents: chatHistory };
            const apiKey = "";
            const apiUrl = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key=${apiKey}`;
            
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(payload)
            });

            if (!response.ok) {
                throw new Error(`API request failed with status ${response.status}`);
            }

            const result = await response.json();
            
            let botResponse = "Sorry, I couldn't find an answer in your plan. Please try rephrasing.";
            if (result.candidates && result.candidates.length > 0 &&
                result.candidates[0].content && result.candidates[0].content.parts &&
                result.candidates[0].content.parts.length > 0) {
                botResponse = result.candidates[0].content.parts[0].text;
            }
             setMessages(prev => [...prev, { role: 'bot', text: botResponse }]);

        } catch (error) {
            console.error("Chatbot API error:", error);
            setMessages(prev => [...prev, { role: 'bot', text: "There was an error connecting to the chat service. Please try again later." }]);
        } finally {
            setIsLoading(false);
        }
    };

    return (
        <div className="p-4 md:p-6 h-full flex flex-col">
            <h1 className="text-3xl font-bold text-white mb-4">AI Fitness Chat</h1>
            <div className="flex-1 bg-gray-800 rounded-2xl p-4 overflow-y-auto space-y-4">
                {messages.map((msg, index) => (
                    <div key={index} className={`flex items-end gap-2 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                        {msg.role === 'bot' && <div className="w-8 h-8 rounded-full bg-emerald-500 flex items-center justify-center flex-shrink-0"><Bot size={20}/></div>}
                        <div className={`max-w-xs md:max-w-md lg:max-w-lg p-3 rounded-2xl ${msg.role === 'user' ? 'bg-emerald-600' : 'bg-gray-700'}`}>
                            <p className="text-white whitespace-pre-wrap">{msg.text}</p>
                        </div>
                         {msg.role === 'user' && <div className="w-8 h-8 rounded-full bg-gray-600 flex items-center justify-center flex-shrink-0"><User size={20}/></div>}
                    </div>
                ))}
                {isLoading && <div className="flex justify-start"><div className="p-3 rounded-2xl bg-gray-700 text-white">Typing...</div></div>}
                <div ref={messagesEndRef} />
            </div>
            <div className="mt-4 flex gap-4">
                <input
                    type="text"
                    value={input}
                    onChange={(e) => setInput(e.target.value)}
                    onKeyPress={(e) => e.key === 'Enter' && !isLoading && handleSend()}
                    placeholder="Ask about your plan..."
                    className="flex-1 bg-gray-700 border-gray-600 rounded-lg shadow-sm py-3 px-4 text-white focus:outline-none focus:ring-2 focus:ring-emerald-500"
                    disabled={isLoading}
                />
                <button onClick={handleSend} disabled={isLoading} className="bg-emerald-600 hover:bg-emerald-700 text-white font-bold p-3 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed">
                    <Send size={24}/>
                </button>
            </div>
        </div>
    );
};

const DocumentViewer = ({ title, content }) => {
  return (
    <div className="p-4 md:p-6 h-full flex flex-col">
      <h1 className="text-3xl font-bold text-white mb-4">{title}</h1>
      <div className="flex-1 bg-gray-800 rounded-2xl p-6 overflow-y-auto">
        <p className="text-gray-300 whitespace-pre-wrap font-mono text-sm leading-relaxed">
          {content}
        </p>
      </div>
    </div>
  );
};


// --- Main App Component ---
export default function App() {
    const [userId, setUserId] = useState(null);
    const [isLoading, setIsLoading] = useState(true);
    const [profile, setProfile] = useState(null);
    const [dailyData, setDailyData] = useState({});
    const [weightHistory, setWeightHistory] = useState([]);
    const [currentPage, setCurrentPage] = useState('dashboard');
    const [planContext, setPlanContext] = useState('');
    const [docsSubMenuOpen, setDocsSubMenuOpen] = useState(false);
    
    useEffect(() => {
        const fullPlanContext = `DOCUMENT 1: Main Fitness Plan\n${PLAN_DOC_TEXT}\n\nDOCUMENT 2: Workout Schedule\n${SCHEDULE_DOC_TEXT}`;
        setPlanContext(fullPlanContext);
    }, []);

    useEffect(() => {
        const unsubscribe = onAuthStateChanged(auth, async (user) => {
            if (user) setUserId(user.uid);
            else {
                try {
                    const token = typeof __initial_auth_token !== 'undefined' ? __initial_auth_token : null;
                    if(token) await signInWithCustomToken(auth, token);
                    else await signInAnonymously(auth);
                } catch (error) { console.error("Auth Error:", error); }
            }
        });
        return () => unsubscribe();
    }, []);

    useEffect(() => {
        if (!userId) return;
        const unsubProfile = onSnapshot(doc(db, `artifacts/${appId}/users/${userId}/profile/main`), (docSnap) => {
            setProfile(docSnap.exists() ? docSnap.data() : null);
            setIsLoading(false);
        });
        const unsubDaily = onSnapshot(collection(db, `artifacts/${appId}/users/${userId}/dailyData`), (snap) => {
            const allDailyData = {};
            const allWeightHistory = [];
            snap.forEach(docSnap => {
                const data = docSnap.data();
                allDailyData[docSnap.id] = data;
                if(data.weight > 0) allWeightHistory.push({date: docSnap.id, weight: data.weight});
            });
            allWeightHistory.sort((a, b) => new Date(a.date) - new Date(b.date));
            setDailyData(allDailyData);
            setWeightHistory(allWeightHistory);
        });
        return () => { unsubProfile(); unsubDaily(); };
    }, [userId]);
    
    const handleOnboardingComplete = async (profileData) => {
        if (!userId) return;
        setIsLoading(true);
        await setDoc(doc(db, `artifacts/${appId}/users/${userId}/profile/main`), profileData);
        const today = profileData.startDate.toDate().toISOString().split('T')[0];
        await setDoc(doc(db, `artifacts/${appId}/users/${userId}/dailyData/${today}`), { weight: profileData.startWeight, calories: 0, protein: 0 }, { merge: true });
        setIsLoading(false);
    };

    if (isLoading) return <div className="min-h-screen bg-gray-900 flex items-center justify-center text-white text-xl">Loading Your Plan...</div>;
    if (!profile) return <Onboarding onComplete={handleOnboardingComplete} />;

    const currentWeek = getWeekNumber(profile.startDate);
    const currentPlan = FULL_PLAN[currentWeek - 1];

    const renderPage = () => {
        switch (currentPage) {
            case 'dashboard': return <Dashboard profile={profile} dailyData={dailyData} weightHistory={weightHistory} currentPlan={currentPlan} currentWeek={currentWeek} userId={userId} />;
            case 'plan': return <Plan profile={profile} />;
            case 'workout': return <Workout profile={profile} />;
            case 'nutrition': return <Nutrition profile={profile} dailyData={dailyData} userId={userId} />;
            case 'progress': return <Progress profile={profile} dailyData={dailyData} />;
            case 'settings': return <Settings profile={profile} userId={userId} weightHistory={weightHistory}/>;
            case 'chat': return <Chatbot planContext={planContext} />;
            case 'doc_plan': return <DocumentViewer title="Adaptive 10-Month Blueprint" content={PLAN_DOC_TEXT} />;
            case 'doc_schedule': return <DocumentViewer title="10-Month Workout Compass" content={SCHEDULE_DOC_TEXT} />;
            default: return <Dashboard profile={profile} dailyData={dailyData} weightHistory={weightHistory} currentPlan={currentPlan} currentWeek={currentWeek} userId={userId} />;
        }
    };
    
    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: Home },
        { id: 'plan', label: 'Plan', icon: Calendar },
        { id: 'workout', label: 'Workouts', icon: Dumbbell },
        { id: 'nutrition', label: 'Nutrition', icon: Pizza },
        { id: 'progress', label: 'Progress', icon: BarChart2 },
        { id: 'chat', label: 'AI Chat', icon: Bot },
        { id: 'documents', label: 'Docs', icon: BookOpen },
        { id: 'settings', label: 'Settings', icon: SettingsIcon },
    ];

    return (
        <div className="h-screen bg-gray-900 text-white font-sans flex flex-col">
            <div className="flex flex-1 overflow-hidden">
                <nav className="bg-gray-800 p-2 md:p-4 flex flex-col justify-between">
                    <div>
                       <div className="p-2 mb-6 hidden md:block"><Target size={32} className="text-emerald-400"/></div>
                        <ul>
                            {navItems.map(item => {
                                const isDocs = item.id === 'documents';
                                const effectiveCurrentPage = currentPage.startsWith('doc_') ? 'documents' : currentPage;
                                return (
                                <li key={item.id}>
                                    <button 
                                        onClick={() => {
                                            if (isDocs) {
                                                setDocsSubMenuOpen(!docsSubMenuOpen);
                                            } else {
                                                setCurrentPage(item.id);
                                                setDocsSubMenuOpen(false);
                                            }
                                        }} 
                                        className={`flex items-center justify-center md:justify-start space-x-0 md:space-x-3 w-full p-3 my-2 rounded-lg transition-colors ${effectiveCurrentPage === item.id ? 'bg-emerald-600 text-white' : 'text-gray-400 hover:bg-gray-700 hover:text-white'}`}
                                    >
                                       <item.icon size={24} /><span className="hidden md:inline">{item.label}</span>
                                    </button>
                                    {isDocs && docsSubMenuOpen && (
                                      <div className="pl-4 md:pl-6 pt-2">
                                        <ul className="space-y-1">
                                          <li><button onClick={() => setCurrentPage('doc_plan')} className={`w-full text-left p-2 rounded-lg text-sm transition-colors ${currentPage === 'doc_plan' ? 'text-white bg-emerald-700/50' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}>Fitness Plan</button></li>
                                          <li><button onClick={() => setCurrentPage('doc_schedule')} className={`w-full text-left p-2 rounded-lg text-sm transition-colors ${currentPage === 'doc_schedule' ? 'text-white bg-emerald-700/50' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}>Workout Schedule</button></li>
                                        </ul>
                                      </div>
                                    )}
                                </li>
                            )})}
                        </ul>
                    </div>
                     <div className="hidden md:block p-2 text-center text-xs text-gray-500">
                        <p>User ID:</p><p className="break-all">{userId || 'loading...'}</p>
                    </div>
                </nav>
                <main className="flex-1 overflow-y-auto">
                    {renderPage()}
                </main>
            </div>
        </div>
    );
}
