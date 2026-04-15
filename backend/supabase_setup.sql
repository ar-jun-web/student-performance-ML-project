-- ══════════════════════════════════════════════════════════════
-- AcademyFlow Database Setup
-- Run this in Supabase SQL Editor
-- ══════════════════════════════════════════════════════════════

-- 1. Student profiles (extends Supabase auth.users)
CREATE TABLE public.students (
    id UUID PRIMARY KEY REFERENCES auth.users(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    department TEXT,
    year INTEGER CHECK (year BETWEEN 1 AND 4),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 2. Prediction history
CREATE TABLE public.predictions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    hours_studied INTEGER NOT NULL,
    previous_scores INTEGER NOT NULL,
    extracurricular BOOLEAN NOT NULL,
    sleep_hours INTEGER NOT NULL,
    sample_papers INTEGER NOT NULL,
    predicted_score FLOAT NOT NULL,
    grade TEXT NOT NULL,
    target_score INTEGER,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- 3. Goals
CREATE TABLE public.goals (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID NOT NULL REFERENCES public.students(id) ON DELETE CASCADE,
    target_score INTEGER NOT NULL CHECK (target_score BETWEEN 0 AND 100),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ══════════════════════════════════════════════════════════════
-- Row Level Security (students can only access their own data)
-- ══════════════════════════════════════════════════════════════

ALTER TABLE public.students ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.predictions ENABLE ROW LEVEL SECURITY;
ALTER TABLE public.goals ENABLE ROW LEVEL SECURITY;

-- Students: can read/update their own profile
CREATE POLICY "Users can view own profile" ON public.students
    FOR SELECT USING (auth.uid() = id);
CREATE POLICY "Users can update own profile" ON public.students
    FOR UPDATE USING (auth.uid() = id);
CREATE POLICY "Users can insert own profile" ON public.students
    FOR INSERT WITH CHECK (auth.uid() = id);

-- Predictions: can read/insert their own
CREATE POLICY "Users can view own predictions" ON public.predictions
    FOR SELECT USING (auth.uid() = student_id);
CREATE POLICY "Users can insert own predictions" ON public.predictions
    FOR INSERT WITH CHECK (auth.uid() = student_id);

-- Goals: can read/insert/update their own
CREATE POLICY "Users can view own goals" ON public.goals
    FOR SELECT USING (auth.uid() = student_id);
CREATE POLICY "Users can insert own goals" ON public.goals
    FOR INSERT WITH CHECK (auth.uid() = student_id);
CREATE POLICY "Users can update own goals" ON public.goals
    FOR UPDATE USING (auth.uid() = student_id);
