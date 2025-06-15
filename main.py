import React, { useState, useEffect, useRef } from 'react';
import { initializeApp } from 'firebase/app';
import { getAuth, signInAnonymously, onAuthStateChanged, signInWithCustomToken } from 'firebase/auth';
import { getFirestore, doc, getDoc, setDoc, onSnapshot, collection, addDoc, query, getDocs, where, Timestamp, deleteDoc } from 'firebase/firestore';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, BarChart, Bar } from 'recharts';
import { ArrowRight, ChevronLeft, ChevronRight, Dumbbell, Flame, Target, Weight, Pizza, CheckCircle, PlusCircle, Calendar, BarChart2, Home, User, Settings as SettingsIcon, HeartPulse, Moon, X, Bot, Send, BookOpen, Check, Utensils, Drumstick, Trash2, Award, ShieldCheck, Zap, Star, Trophy, ChefHat, Link as LinkIcon } from 'lucide-react';

// --- Firebase Configuration ---
const firebaseConfig = typeof __firebase_config !== 'undefined' ? JSON.parse(__firebase_config) : {};
const appId = typeof __app_id !== 'undefined' ? __app_id : 'default-app-id';

// --- Firebase Initialization ---
const app = initializeApp(firebaseConfig);
const auth = getAuth(app);
const db = getFirestore(app);

// --- FULL DOCUMENT TEXT FOR VIEWER AND CHATBOT ---
const PLAN_DOC_TEXT = `An Adaptive 10-Month Blueprint for Sustainable Physique Transformation...`;
const SCHEDULE_DOC_TEXT = `Your 10-Month Workout Compass: A Weekly Guide to Physique Transformation...`;
const PHOENIX_PROTOCOL_DOC_TEXT = `The Phoenix Protocol: A Comprehensive 10-Month Blueprint for Elite Body Recomposition

Section I: The Blueprint for Your Transformation: An Introduction

A. Foreword from Your Transformation Architect

This document outlines a comprehensive, evidence-based 10-month protocol designed to guide a remarkable physical and metabolic transformation. The primary objectives are ambitious yet physiologically achievable: a 70-pound reduction in fat mass coupled with a 10 to 15-pound gain in lean muscle mass. This is not merely a diet or a workout program; it is an integrated, adaptive blueprint for rebuilding your physique from the ground up.

The protocol is founded on the understanding that success in such an endeavor is not born from short-term, extreme efforts, but from the relentless application of intelligent, sustainable habits. It has been meticulously crafted to synthesize the most effective elements from established fitness strategies while being specifically tailored to the available resources—namely, a set of 10, 20, and 30 lb dumbbells and cardio equipment—and the explicit request for a gradual, manageable start.

This is not a static set of rules. It is a dynamic roadmap, designed to be a collaborative partnership. It will equip you with the "what" to do, but more importantly, the "why" behind every nutritional target, every exercise, and every phase. By understanding the scientific principles that govern fat loss and muscle growth, you will become an educated, empowered participant in your own journey, capable of making informed adjustments and sustaining your results for a lifetime.

B. Core Philosophies of This Plan

Three core philosophies underpin every aspect of this protocol. Internalizing them is as critical as executing the workouts themselves.

• Sustainability Over Initial Intensity: The architecture of this plan is intentionally front-loaded for habit formation. The journey begins with a reduced workout frequency of two full-body sessions per week, as specifically requested. This initial phase is not designed to be maximally taxing; it is designed to be maximally achievable. Its purpose is to build an unbreakable foundation of consistency in training, nutrition tracking, and daily movement. This foundation is the bedrock upon which all future, more intense phases will be built. True transformation is a marathon, and this plan ensures a strong, steady start rather than a premature burnout.

• Consistency is the Super-ingredient: The single most potent determinant of success in any long-term transformation is unwavering consistency. It is the cumulative effect of small, daily actions—meticulously tracking nutritional intake, hitting daily step goals, and faithfully executing every planned workout—that drives profound change. This protocol is designed to make consistency manageable. The most advanced training techniques and perfect nutritional calculations are rendered useless without the discipline to apply them day in and day out. Therefore, adherence is the primary metric of success, especially in the foundational first month.

• Auto-regulation: Becoming an Expert on Your Body: This plan rejects the notion of a rigid, one-size-fits-all prescription. Instead, it incorporates powerful tools for "auto-regulation," which allow for daily flexibility based on your body's feedback. By using the Rate of Perceived Exertion (RPE) for cardiovascular effort and Reps in Reserve (RIR) for strength training intensity, you are empowered to adjust your workouts based on real-time factors like energy levels, sleep quality, and recovery status. On a day you feel strong, you might push for more repetitions to hit the target RIR. On a day you feel fatigued, you might use a lighter weight. This dynamic approach transforms the plan from a static set of commands into an intelligent, responsive system, making you an active partner in your own progress.`;


// --- NEW 10-MONTH PLAN DATA (from PDFs) ---

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

const ACHIEVEMENT_LIST = {
    consistency: [
        { id: 'c1', title: 'First Workout!', description: 'Complete your first activity.', check: (data) => data.completedWorkouts >= 1, icon: Star },
        { id: 'c2', title: 'One Week Strong', description: 'Complete a full week of planned workouts.', check: (data) => data.workoutStreak >= 7, icon: ShieldCheck },
        { id: 'c3', title: '30-Day Hustle', description: 'Complete 30 workouts.', check: (data) => data.completedWorkouts >= 30, icon: Zap },
        { id: 'c4', title: 'Consistency King', description: 'Maintain a 30-day workout streak.', check: (data) => data.workoutStreak >= 30, icon: Trophy },
    ],
    weightLoss: [
        { id: 'w1', title: 'On the Board', description: 'Lose your first 10 lbs.', check: (data) => data.weightLost >= 10, icon: Target },
        { id: 'w2', title: '25 Down', description: 'Lose a total of 25 lbs.', check: (data) => data.weightLost >= 25, icon: Target },
        { id: 'w3', title: 'Halfway There!', description: 'Lose 35 lbs, halfway to your goal.', check: (data) => data.weightLost >= 35, icon: Target },
        { id: 'w4', title: '50 Pound Club', description: 'Lose a total of 50 lbs.', check: (data) => data.weightLost >= 50, icon: Award },
        { id: 'w5', title: 'Goal Crusher', description: 'Reach your 70 lb weight loss goal.', check: (data) => data.weightLost >= 70, icon: Trophy },
    ],
    workoutMilestones: [
        { id: 'm1', title: 'Getting Started', description: 'Complete 10 workouts.', check: (data) => data.completedWorkouts >= 10, icon: Dumbbell },
        { id: 'm2', title: 'Regular', description: 'Complete 50 workouts.', check: (data) => data.completedWorkouts >= 50, icon: Dumbbell },
        { id: 'm3', title: 'Veteran', description: 'Complete 100 workouts.', check: (data) => data.completedWorkouts >= 100, icon: Dumbbell },
    ],
    nutrition: [
        { id: 'n1', title: 'Perfect Protein', description: 'Hit your protein goal for 7 days in a row.', check: (data) => data.proteinStreak >= 7, icon: Drumstick },
        { id: 'n2', title: 'Calorie Control', description: 'Hit your calorie goal for 7 days in a row.', check: (data) => data.calorieStreak >= 7, icon: Utensils },
        { id: 'n3', title: 'Nutritionist', description: 'Hit both calorie and protein goals for a full week.', check: (data) => data.perfectNutritionWeek, icon: ChefHat },
    ],
    planProgression: [
        { id: 'p1', title: 'Phase 1 Complete', description: 'Finish the first phase of your plan.', check: (data) => data.currentWeek > 4, icon: Star },
        { id: 'p2', title: 'Phase 2 Complete', description: 'Finish the second phase of your plan.', check: (data) => data.currentWeek > 8, icon: ShieldCheck },
        { id: 'p3', title: 'Phase 3 Complete', description: 'Finish the third phase of your plan.', check: (data) => data.currentWeek > 16, icon: Zap },
        { id: 'p4', title: 'Phase 4 Complete', description: 'Finish the fourth phase of your plan.', check: (data) => data.currentWeek > 28, icon: Award },
        { id: 'p5', title: 'Plan Mastered!', description: 'Complete all 10 months of the plan.', check: (data) => data.currentWeek >= 40, icon: Trophy },
    ],
};


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
            unlockedAchievements: {}
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


const Dashboard = ({ profile, dailyData, weightHistory, currentPlan, currentWeek, userId, setPage, showAchievementNotification }) => {
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
        if (hour >= 12 && !isActivityCompleted && !todaysWorkoutInfo.type.includes('Rest')) {
            const lastReminder = localStorage.getItem('lastWorkoutReminder');
            if (lastReminder !== today) {
                setShowWorkoutReminder(true);
                localStorage.setItem('lastWorkoutReminder', today);
            }
        }

        const isWeighInDay = dayOfWeek === 1; // Monday
        if (isWeighInDay && hour >= 9) {
            const lastReminderTimestamp = localStorage.getItem('lastWeighInReminder');
            if (lastReminderTimestamp) {
                const lastDate = new Date(parseInt(lastReminderTimestamp));
                const todayDate = new Date();
                if (lastDate.getFullYear() === todayDate.getFullYear() &&
                    lastDate.getMonth() === todayDate.getMonth() &&
                    lastDate.getDate() === todayDate.getDate()) {
                    return; // Already reminded today
                }
            }
            setShowWeighInReminder(true);
            localStorage.setItem('lastWeighInReminder', Date.now().toString());
        }

    }, [isActivityCompleted, today, dayOfWeek, dailyData, todaysWorkoutInfo]);


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

const Nutrition = ({ profile, dailyData, userId }) => {
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
            querySnapshot.forEach((doc) => {
                fetchedMeals.push({ id: doc.id, ...doc.data() });
            });
            setMeals(fetchedMeals);
            
            const totalCalories = fetchedMeals.reduce((sum, meal) => sum + (meal.calories || 0), 0);
            const totalProtein = fetchedMeals.reduce((sum, meal) => sum + (meal.protein || 0), 0);
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

    const handleDeleteMeal = async (mealId) => {
        if (!userId || !date || !mealId) return;
        await deleteDoc(doc(db, `artifacts/${appId}/users/${userId}/meals`, mealId));
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
                            <div>
                                <p className="font-semibold text-white">{meal.name}</p>
                                <div className="flex space-x-4 text-sm text-gray-400">
                                    <span>{meal.calories} kcal</span>
                                    <span>{meal.protein}g protein</span>
                                </div>
                            </div>
                            <button onClick={() => handleDeleteMeal(meal.id)} className="text-gray-500 hover:text-red-500 p-2">
                                <Trash2 size={18}/>
                            </button>
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

        const prompt = `Based on the provided fitness plan documents, answer the following user question. If the user's question cannot be answered by the documents, use your general knowledge to answer.
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

const DocumentViewer = ({ title, content, link }) => {
  return (
    <div className="p-4 md:p-6 h-full flex flex-col">
        <div className="flex justify-between items-center mb-4">
            <h1 className="text-3xl font-bold text-white">{title}</h1>
            {link && (
                <a href={link} target="_blank" rel="noopener noreferrer" className="flex items-center gap-2 bg-emerald-600 hover:bg-emerald-700 text-white font-bold py-2 px-4 rounded-lg">
                    <LinkIcon size={16} />
                    View Original PDF
                </a>
            )}
        </div>
      <div className="flex-1 bg-gray-800 rounded-2xl p-6 overflow-y-auto">
        <p className="text-gray-300 whitespace-pre-wrap font-mono text-sm leading-relaxed">
          {content}
        </p>
      </div>
    </div>
  );
};

const Achievements = ({ unlockedAchievements }) => {
    return (
        <div className="p-4 md:p-6 space-y-8">
            <h1 className="text-3xl font-bold text-white">Achievements</h1>
            {Object.entries(ACHIEVEMENT_LIST).map(([category, achievements]) => (
                <div key={category} className="bg-gray-800 rounded-2xl p-6 shadow-lg">
                    <h2 className="text-xl font-semibold text-emerald-400 capitalize mb-4">{category}</h2>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                        {achievements.map(ach => {
                            const isUnlocked = unlockedAchievements[ach.id];
                            const Icon = ach.icon || Star;
                            return (
                                <div key={ach.id} className={`p-4 rounded-lg flex items-start space-x-4 transition-all ${isUnlocked ? 'bg-yellow-400/20 border-l-4 border-yellow-400' : 'bg-gray-700/50 opacity-60'}`}>
                                    <Icon className={`mt-1 flex-shrink-0 ${isUnlocked ? 'text-yellow-400' : 'text-gray-500'}`} size={24}/>
                                    <div>
                                        <h3 className={`font-bold ${isUnlocked ? 'text-white' : 'text-gray-400'}`}>{ach.title}</h3>
                                        <p className="text-sm text-gray-400">{ach.description}</p>
                                        {isUnlocked && <p className="text-xs text-yellow-500 mt-1">Unlocked: {new Date(unlockedAchievements[ach.id]).toLocaleDateString()}</p>}
                                    </div>
                                </div>
                            )
                        })}
                    </div>
                </div>
            ))}
        </div>
    );
}


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
    const [unlockedAchievements, setUnlockedAchievements] = useState({});
    const [newAchievement, setNewAchievement] = useState(null);

    const checkAchievements = (profileData, dailyData, weightHistory) => {
        if (!profileData || !profileData.startDate || !userId) return;

        const newUnlocked = { ...(profileData.unlockedAchievements || {}) };
        let hasNewAchievement = false;

        const latestWeight = weightHistory.length > 0 ? weightHistory[weightHistory.length - 1].weight : profileData.startWeight;
        const progressData = {
            completedWorkouts: Object.values(dailyData).filter(d => d.activityCompleted).length,
            weightLost: profileData.startWeight - latestWeight,
            currentWeek: getWeekNumber(profileData.startDate),
        };
        
        for (const category in ACHIEVEMENT_LIST) {
            for (const ach of ACHIEVEMENT_LIST[category]) {
                if (!newUnlocked[ach.id] && ach.check(progressData)) {
                    newUnlocked[ach.id] = new Date().toISOString();
                    setNewAchievement(ach);
                    hasNewAchievement = true;
                    setTimeout(() => setNewAchievement(null), 5000);
                }
            }
        }
        if (hasNewAchievement) {
            const profileRef = doc(db, `artifacts/${appId}/users/${userId}/profile/main`);
            setDoc(profileRef, { unlockedAchievements: newUnlocked }, { merge: true });
        }
    };
    
    useEffect(() => {
        if(profile && dailyData && weightHistory.length > 0){
             checkAchievements(profile, dailyData, weightHistory);
        }
    }, [dailyData, weightHistory, profile]);
    
    useEffect(() => {
        const fullPlanContext = `DOCUMENT 1: Phoenix Protocol\n${PHOENIX_PROTOCOL_DOC_TEXT}\n\nDOCUMENT 2: Main Fitness Plan\n${PLAN_DOC_TEXT}\n\nDOCUMENT 3: Workout Schedule\n${SCHEDULE_DOC_TEXT}`;
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
            if (docSnap.exists()) {
                const data = docSnap.data();
                setProfile(data);
                setUnlockedAchievements(data.unlockedAchievements || {});
            } else {
                setProfile(null);
            }
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
            case 'awards': return <Achievements unlockedAchievements={unlockedAchievements} />;
            case 'settings': return <Settings profile={profile} userId={userId} weightHistory={weightHistory}/>;
            case 'chat': return <Chatbot planContext={planContext} />;
            case 'doc_plan': return <DocumentViewer title="Adaptive 10-Month Blueprint" content={PLAN_DOC_TEXT} />;
            case 'doc_schedule': return <DocumentViewer title="10-Month Workout Compass" content={SCHEDULE_DOC_TEXT} />;
            case 'doc_phoenix': return <DocumentViewer title="The Phoenix Protocol" content={PHOENIX_PROTOCOL_DOC_TEXT} link="https://acrobat.adobe.com/id/urn:aaid:sc:VA6C2:8599afd6-1705-46be-9944-7a12b1a671b9" />;
            default: return <Dashboard profile={profile} dailyData={dailyData} weightHistory={weightHistory} currentPlan={currentPlan} currentWeek={currentWeek} userId={userId} />;
        }
    };
    
    const navItems = [
        { id: 'dashboard', label: 'Dashboard', icon: Home },
        { id: 'plan', label: 'Plan', icon: Calendar },
        { id: 'workout', label: 'Workouts', icon: Dumbbell },
        { id: 'nutrition', label: 'Nutrition', icon: Pizza },
        { id: 'progress', label: 'Progress', icon: BarChart2 },
        { id: 'awards', label: 'Awards', icon: Award },
        { id: 'chat', label: 'AI Chat', icon: Bot },
        { id: 'documents', label: 'Docs', icon: BookOpen },
        { id: 'settings', label: 'Settings', icon: SettingsIcon },
    ];

    return (
        <div className="h-screen bg-gray-900 text-white font-sans flex flex-col relative">
            {newAchievement && (
                <div className="absolute top-5 right-5 bg-emerald-500 text-white p-4 rounded-lg shadow-lg z-[101] animate-fade-in-out">
                    <div className="flex items-center">
                        <Award className="mr-3" />
                        <div>
                            <p className="font-bold">Achievement Unlocked!</p>
                            <p className="text-sm">{newAchievement.title}</p>
                        </div>
                        <button onClick={() => setNewAchievement(null)} className="ml-4"><X size={18} /></button>
                    </div>
                </div>
            )}
            <style>{`
                @keyframes fade-in-out {
                    0% { opacity: 0; transform: translateY(-20px); }
                    10% { opacity: 1; transform: translateY(0); }
                    90% { opacity: 1; transform: translateY(0); }
                    100% { opacity: 0; transform: translateY(-20px); }
                }
                .animate-fade-in-out { animation: fade-in-out 5s forwards; }
            `}</style>
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
                                          <li><button onClick={() => setCurrentPage('doc_phoenix')} className={`w-full text-left p-2 rounded-lg text-sm transition-colors ${currentPage === 'doc_phoenix' ? 'text-white bg-emerald-700/50' : 'text-gray-400 hover:text-white hover:bg-gray-700'}`}>Phoenix Protocol</button></li>
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
