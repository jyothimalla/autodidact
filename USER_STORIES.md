# User Stories - Autodidact Learning Platform

## Epic 1: Learning Module

### US-1.1: View Main Subject Modules
**As a** student
**I want to** see all available main subject modules (Maths, English, Science, Computers)
**So that** I can choose which subject area to study

**Acceptance Criteria:**
- Main Learning page displays 4 main subject cards: Maths, English, Science, Computers
- Each card shows an icon, subject name, and brief description
- Cards are clickable and navigate to the subject's sub-modules
- UI is responsive and works on mobile devices

**Priority:** P0 (Critical)

---

### US-1.2: Browse Maths Sub-Modules
**As a** student
**I want to** see all maths sub-modules when I select Maths
**So that** I can choose a specific topic to study

**Acceptance Criteria:**
- Clicking Maths shows 12 sub-modules:
  1. Four Operations
  2. Percentages
  3. Ratios
  4. Coordinate Geometry
  5. Mental Arithmetic
  6. Fractions and Decimals
  7. Multi-Step Word Problems
  8. Speed-Based Calculation
  9. Algebra
  10. Angles
  11. Shapes
  12. Measurements
- Each sub-module displays name and level indicator
- Sub-modules are visually distinct and clickable

**Priority:** P0 (Critical)

---

### US-1.3: Browse Computer Science Sub-Modules
**As a** student
**I want to** see all computer science topics when I select Computers
**So that** I can learn programming and computing concepts

**Acceptance Criteria:**
- Clicking Computers shows 11 sub-modules:
  1. Introduction to Computing
  2. Introduction to Programming
  3. Binary Number System
  4. Boolean Logic
  5. Python Programming
  6. Hardware, Software and Data Representation
  7. Databases
  8. System Architecture
  9. Internet and WWW
  10. Data Structures
  11. Algorithms
- Topics are organized logically (basic → advanced)
- Each shows difficulty level and estimated duration

**Priority:** P0 (Critical)

---

### US-1.4: View Lesson Content with Video
**As a** student
**I want to** watch an instructional video for each topic
**So that** I can learn the concept visually

**Acceptance Criteria:**
- Each lesson page displays an embedded YouTube/Vimeo video
- Video is responsive and works on all devices
- Video controls (play, pause, volume, fullscreen) are available
- Video URL is securely sanitized to prevent XSS

**Priority:** P0 (Critical)

---

### US-1.5: Read Study Notes and Teaching Materials
**As a** student
**I want to** read detailed teaching notes alongside the video
**So that** I can understand key concepts, common mistakes, and learning strategies

**Acceptance Criteria:**
- Lesson page displays:
  - **Key Points**: Main concepts summary
  - **Common Mistakes**: List of mistakes to avoid
  - **Learning Strategies**: Tips for better understanding
  - **Prerequisites**: Required prior knowledge
- Notes are formatted with clear headings and bullet points
- Content is readable and well-organized

**Priority:** P0 (Critical)

---

### US-1.6: See Worked Examples
**As a** student
**I want to** see worked examples after concept explanation
**So that** I can understand how to apply the concept step-by-step

**Acceptance Criteria:**
- Each lesson includes at least one worked example
- Example shows:
  - Problem statement
  - Step-by-step solution
  - Final answer
  - Explanation of each step
- Examples are clearly separated from theory

**Priority:** P1 (High)

---

## Epic 2: Practice Mode (Within Lessons)

### US-2.1: Choose Practice or Challenge
**As a** student
**I want to** choose between Practice (5 questions) or Challenge (10 questions) after studying
**So that** I can test my understanding at different levels

**Acceptance Criteria:**
- After viewing lesson content, two buttons are displayed:
  - "Practice Test (5 Questions)"
  - "Challenge (10 Questions)"
- Buttons are clearly labeled with question count
- Clicking either button initiates the test flow

**Priority:** P0 (Critical)

---

### US-2.2: Select Attempt Mode - Online or Download
**As a** student
**I want to** choose between attempting online or downloading the paper
**So that** I can practice in my preferred format

**Acceptance Criteria:**
- After selecting Practice/Challenge, mode selection screen appears with 2 options:
  - **Attempt Online**: Answer questions directly on screen
  - **Download to Attempt on Paper**: Print questions and answer sheet
- Each option has clear icon and description
- "Attempt Online" starts the quiz immediately
- "Download" generates and downloads 2 PDFs (questions + answer sheet)

**Priority:** P0 (Critical)

---

### US-2.3: Attempt Practice Quiz Online
**As a** student
**I want to** answer practice questions online with a clean interface
**So that** I can complete the test quickly and get instant feedback

**Acceptance Criteria:**
- Online quiz displays:
  - Progress indicator (Question X of Y)
  - Progress bar
  - Current question text
  - 4 MCQ options (A, B, C, D)
  - Navigation buttons (Previous, Next, Submit)
- User can change answers before submitting
- "Submit" button only appears on last question
- No time limit for practice mode

**Priority:** P0 (Critical)

---

### US-2.4: Download Practice Papers with QR Code
**As a** student
**I want to** download question paper and answer sheet PDFs
**So that** I can attempt the practice on paper and submit later

**Acceptance Criteria:**
- Clicking "Download" generates:
  1. **Questions PDF**: All questions with options A/B/C/D
  2. **Answer Sheet PDF**: Bubble sheet format with:
     - Attempt ID clearly displayed
     - QR code that links to submission page
     - Checkboxes for A/B/C/D for each question
     - Instructions for submission
- Both PDFs open in new tabs automatically
- PDFs are properly formatted for A4 printing
- Attempt is saved in database with "pending" status

**Priority:** P0 (Critical)

---

### US-2.5: Submit Answers by Scanning QR Code
**As a** student
**I want to** scan the QR code on my answer sheet to open the submission page
**So that** I can easily upload my completed answers

**Acceptance Criteria:**
- QR code on answer sheet encodes URL: `{FRONTEND_URL}/practice-submit/{attemptId}`
- Scanning QR opens submission page in browser/app
- Page displays:
  - Attempt ID
  - Two submission options: Upload or Manual Entry
- Works with any QR scanner app (Camera, QR reader apps)

**Priority:** P0 (Critical)

---

### US-2.6: Upload Completed Answer Sheet
**As a** student
**I want to** upload a photo/scan of my completed answer sheet
**So that** my answers can be automatically graded via OCR

**Acceptance Criteria:**
- Submission page has "Upload Answer Sheet" option
- File input accepts: JPG, PNG, PDF formats
- User can preview selected file before uploading
- System processes upload using OCR (pytesseract)
- Success/failure message is shown
- OCR extracts answers and calculates score
- Results are displayed immediately after processing

**Priority:** P1 (High)
**Note:** OCR implementation is advanced - may use manual entry as fallback

---

### US-2.7: Enter Answers Manually
**As a** student/parent
**I want to** manually type in the answers from the paper
**So that** I can submit answers even if upload/OCR fails

**Acceptance Criteria:**
- Submission page has "Enter Manually" option
- Grid layout shows all question numbers (Q1-Q5 or Q1-Q10)
- Each question has 4 buttons/dropdown for A/B/C/D
- User can select one option per question
- Selected answers are highlighted
- "Submit Answers" button validates and submits
- At least 1 answer must be provided before submission

**Priority:** P0 (Critical)

---

### US-2.8: View Practice Results with Detailed Feedback
**As a** student
**I want to** see my score and review each question with explanations
**So that** I can learn from my mistakes

**Acceptance Criteria:**
- After submission, results page displays:
  - **Score Banner**: Score/Total, Percentage, Pass/Fail status
  - **Review Section**: All questions with expandable details
- Each question review shows:
  - Question number and text
  - Your selected answer (highlighted in red if wrong)
  - Correct answer (highlighted in green)
  - Explanation (expandable/collapsible)
  - ✓ or ✗ icon indicating correctness
- Questions can be clicked to expand/collapse explanations
- "Back to Lesson" button returns to lesson page
- "Continue to Next Level" button (if next level exists)

**Priority:** P0 (Critical)

---

### US-2.9: View Practice Attempt History
**As a** student
**I want to** see all my previous practice and challenge attempts for a topic
**So that** I can track my progress over time

**Acceptance Criteria:**
- Lesson page shows "View History (X attempts)" button
- Clicking shows list of all attempts for this topic/level
- Each attempt displays:
  - Date and time
  - Attempt type (Practice or Challenge)
  - Mode (Online or Download)
  - Score and percentage (if submitted)
  - "Pending submission" status (if not submitted)
- Recent 3 attempts shown as preview on main lesson page
- Full history accessible via dedicated button

**Priority:** P1 (High)

---

## Epic 3: Practice Module (From Header)

### US-3.1: Access Practice Page from Header
**As a** student
**I want to** click "Practice" in the main header/navigation
**So that** I can access standalone practice paper generation

**Acceptance Criteria:**
- Header has "Practice" link visible on all pages
- Clicking navigates to `/practice` route
- Page loads Practice component with subject selection

**Priority:** P0 (Critical)

---

### US-3.2: Select Subject and Topic for Practice
**As a** student
**I want to** select a main subject, then a sub-topic, then question count and difficulty
**So that** I can generate a customized practice paper

**Acceptance Criteria:**
- Practice page displays:
  1. **Subject dropdown**: Maths, English, Science, Computers
  2. **Topic dropdown**: Populated based on selected subject
     - For Maths: Four Operations, Percentages, Ratios, etc.
     - For Computers: Python, Algorithms, Data Structures, etc.
  3. **Number of Questions**: 5, 10, 15, 20 (radio buttons or dropdown)
  4. **Difficulty**: Easy, Medium, Hard, Mixed (radio buttons)
  5. **Time Limit**: 5, 10, 15, 20, 30 minutes (based on question count)
- "Generate Paper" button enabled only when all fields selected
- Form validates selections before generation

**Priority:** P0 (Critical)

---

### US-3.3: Generate Custom Practice Paper
**As a** student
**I want to** generate a practice paper based on my selections
**So that** I can attempt targeted practice

**Acceptance Criteria:**
- Clicking "Generate Paper" calls API to create custom paper
- Questions are randomly selected from the chosen topic
- Difficulty distribution follows selected difficulty:
  - Easy: 80% easy, 20% medium
  - Medium: 20% easy, 60% medium, 20% hard
  - Hard: 20% medium, 80% hard
  - Mixed: 30% easy, 40% medium, 30% hard
- Paper is saved under "My Generated Papers"
- User can immediately attempt or download

**Priority:** P0 (Critical)

---

### US-3.4: View Previously Generated Papers
**As a** student
**I want to** see all practice papers I've previously generated
**So that** I can re-attempt or review them

**Acceptance Criteria:**
- Practice page shows "My Generated Papers" section
- List displays:
  - Paper ID
  - Topic
  - Number of questions
  - Difficulty
  - Date created
  - Status (Attempted/Not Attempted)
- User can click to attempt or download any paper
- Papers persist across sessions

**Priority:** P1 (High)

---

## Epic 4: Test/Mock Exam Module

### US-4.1: Access 20 Seeded Practice Papers
**As a** student
**I want to** see 20 pre-generated practice papers when I open the Test module
**So that** I can practice full-length exams without generating new ones

**Acceptance Criteria:**
- Test page displays grid of 20 practice papers
- Each paper shows:
  - Paper number (1-20)
  - Title (e.g., "Practice Paper 1")
  - 50 Questions
  - Mixed Difficulty
  - 60 minutes duration
- Papers are pre-seeded in database on first load
- Clicking a paper allows immediate attempt

**Priority:** P0 (Critical)

---

### US-4.2: Generate New Mock Test
**As a** student
**I want to** generate a new 50-question mock test
**So that** I can practice with fresh questions

**Acceptance Criteria:**
- "Generate New Mock Test" button at top of Test page
- Clicking generates:
  - 50 MCQ questions (A/B/C/D/E options)
  - Mixed difficulty from all modules
  - Unique test ID
  - 60-minute time limit
- Test is saved under "My Generated Tests"
- User chooses: Attempt Online or Download

**Priority:** P0 (Critical)

---

### US-4.3: Attempt Mock Test Online with Timer
**As a** student
**I want to** attempt a 50-question mock test online with a countdown timer
**So that** I can simulate real exam conditions

**Acceptance Criteria:**
- Test starts with 60:00 countdown timer
- Timer is always visible (sticky header or corner)
- Timer shows minutes:seconds format
- Warning at 10 minutes remaining (yellow)
- Warning at 5 minutes remaining (red + sound/vibration)
- Test auto-submits when timer reaches 00:00
- User can manually submit before time runs out
- Navigation between questions is allowed during the test

**Priority:** P0 (Critical)

---

### US-4.4: Download Mock Test with Answer Sheet
**As a** student
**I want to** download the mock test question paper and answer sheet
**So that** I can attempt it offline on paper

**Acceptance Criteria:**
- "Download" option generates 2 PDFs:
  1. **Question Paper**: All 50 questions with A/B/C/D/E options
  2. **Answer Sheet**: OCR-compatible bubble sheet with:
     - Test ID
     - QR code for submission
     - 50 question rows with 5 bubbles each (A/B/C/D/E)
     - Instructions for marking and scanning
- Both PDFs formatted for A4 printing
- Answer sheet uses OCR-friendly font and spacing
- Test saved as "pending" in database

**Priority:** P0 (Critical)

---

### US-4.5: Submit Mock Test via QR Code
**As a** student
**I want to** scan the QR code on my answer sheet to submit my test
**So that** I can easily access the submission page

**Acceptance Criteria:**
- QR code encodes: `{FRONTEND_URL}/test/{testId}/submit`
- Scanning opens submission page
- Page recognizes test ID from URL
- Shows 2 submission options: Upload or Manual Entry
- Same functionality as practice submission

**Priority:** P0 (Critical)

---

### US-4.6: View Mock Test Results with Module Breakdown
**As a** student
**I want to** see my test results with breakdown by topic
**So that** I can identify my strong and weak areas

**Acceptance Criteria:**
- Results page displays:
  - **Total Score Banner**: XX/50, Percentage, Pass/Fail (60% threshold)
  - **Module Breakdown Table**:
    - Topic Name
    - Score for that topic
    - Total questions for that topic
    - Percentage for that topic
  - **Question Review**: All 50 questions with expandable details
- Color coding:
  - Green: ≥60% (good)
  - Yellow: 40-59% (needs improvement)
  - Red: <40% (weak area)
- Breakdown helps identify specific topics needing more practice

**Priority:** P0 (Critical)

---

### US-4.7: Review Mock Test Answers with Explanations
**As a** student
**I want to** review every question with correct answers and explanations
**So that** I can learn from my mistakes

**Acceptance Criteria:**
- Review section shows all 50 questions
- Each question can be expanded to show:
  - Full question text
  - All options (A/B/C/D/E)
  - Your selected answer (red if wrong, green if correct)
  - Correct answer (always green)
  - Detailed explanation
- Questions are collapsed by default (expandable on click)
- Can expand/collapse all with single button
- Can filter: All / Correct / Incorrect questions

**Priority:** P1 (High)

---

### US-4.8: View Test Attempt History
**As a** student
**I want to** see all my previous mock test attempts
**So that** I can track my improvement over time

**Acceptance Criteria:**
- Test page has "My Test History" section
- Shows list of all attempted tests:
  - Test ID
  - Date and time
  - Score/50
  - Percentage
  - Pass/Fail status
  - Time taken (if online)
- Can click any test to view full results again
- Shows trend graph of scores over time (optional enhancement)

**Priority:** P1 (High)

---

## Epic 5: Parent/Teacher Features

### US-5.1: Manual Answer Entry for Parents
**As a** parent
**I want to** manually enter my child's answers from their paper
**So that** I can help them submit even if they can't use the QR/upload

**Acceptance Criteria:**
- Submission page has clear "Enter Manually" tab
- Grid shows all questions with A/B/C/D/(E) buttons
- Parent can easily select answers
- Clear visual feedback when answers are selected
- Can review all answers before final submission
- Submission confirmation dialog

**Priority:** P0 (Critical)

---

### US-5.2: View Child's Progress and Analytics
**As a** parent
**I want to** see my child's overall progress and performance analytics
**So that** I can identify areas where they need help

**Acceptance Criteria:**
- Analytics page shows:
  - Total attempts by subject
  - Average score by subject
  - Average score by topic
  - Recent attempts timeline
  - Weak topics highlighted
  - Improvement trends over time
- Accessible from My Account or separate Analytics menu
- Can filter by date range (last week, month, all time)

**Priority:** P1 (High)

---

## Epic 6: Admin Features

### US-6.1: Manage Lesson Content
**As an** admin
**I want to** add/edit/delete lessons, videos, and study notes
**So that** I can keep the learning content up-to-date

**Acceptance Criteria:**
- Admin dashboard has "Content Management" section
- Can add new:
  - Subjects
  - Modules/Topics
  - Lessons with video URLs
  - Teaching notes, mistakes, strategies
- Can edit existing content via inline editor
- Can preview changes before saving
- Changes are immediately reflected on frontend

**Priority:** P1 (High)

---

### US-6.2: Manage Question Banks
**As an** admin
**I want to** add/edit questions, answers, and explanations
**So that** students have quality practice materials

**Acceptance Criteria:**
- Question management interface shows:
  - List of all questions by module/topic
  - Filter by difficulty, module
  - Add new question form with:
    - Question text
    - 4 or 5 options
    - Correct answer
    - Explanation
    - Difficulty level
    - Tags/topics
- Bulk import via CSV/Excel
- Validation to ensure all fields are filled
- Preview question as students will see it

**Priority:** P1 (High)

---

### US-6.3: View User Activity and Logs
**As an** admin
**I want to** see user activity logs
**So that** I can monitor system usage and identify issues

**Acceptance Criteria:**
- Admin can view:
  - User login/logout events
  - Practice/test attempts
  - Paper generations
  - Failed submissions
- Logs include timestamp, user ID, action type
- Can filter by user, date range, action type
- Export logs to CSV

**Priority:** P2 (Medium)

---

## Non-Functional Requirements

### NFR-1: Performance
- Practice/test generation should complete within 3 seconds
- PDF generation should complete within 5 seconds
- Page load time < 2 seconds on 4G connection
- Support up to 500 concurrent users

### NFR-2: Security
- All user data encrypted in database
- JWT authentication for API access
- Secure password storage (bcrypt)
- XSS protection on all inputs
- CSRF protection on all forms

### NFR-3: Accessibility
- WCAG 2.1 Level AA compliance
- Keyboard navigation support
- Screen reader compatibility
- Color contrast ratios meet standards
- Font sizes adjustable

### NFR-4: Mobile Responsiveness
- Fully functional on mobile devices (iOS/Android)
- Touch-friendly buttons and controls
- Readable text without zooming
- QR scanner integration works on mobile browsers

### NFR-5: Data Persistence
- All attempts saved permanently
- Practice history never expires
- Progress tracking across sessions
- Automatic backup daily

---

## Technical Debt & Future Enhancements

### TD-1: OCR Implementation
- Current: Placeholder for OCR answer extraction
- Required: Implement pytesseract-based OCR for bubble sheet reading
- Complexity: High
- Priority: P1

### TD-2: Real-time Collaboration
- Allow teachers to monitor students attempting tests live
- Show progress indicators for in-progress tests
- Complexity: High
- Priority: P2

### TD-3: Adaptive Learning
- Adjust difficulty based on student performance
- Recommend specific lessons based on weak areas
- Complexity: High
- Priority: P2

### TD-4: Gamification
- Add badges, achievements, streaks
- Leaderboards by school/class
- Points system for completing practices
- Complexity: Medium
- Priority: P2

---

## Definition of Done

For each user story to be considered "Done":
1. ✅ Code implemented and reviewed
2. ✅ Unit tests written and passing (>80% coverage)
3. ✅ Integration tests passing
4. ✅ Manual testing completed
5. ✅ Responsive design verified on mobile/tablet/desktop
6. ✅ Accessibility checklist completed
7. ✅ Documentation updated
8. ✅ Deployed to staging environment
9. ✅ Product owner approval

---

## Release Plan

**Phase 1 (MVP)** - 6 weeks
- All Epic 1 user stories (Learning Module)
- All Epic 2 user stories (Practice within lessons)
- US-3.1, US-3.2, US-3.3 (Basic practice from header)

**Phase 2** - 4 weeks
- All Epic 4 user stories (Mock Tests)
- US-3.4 (Previously generated papers)
- US-5.1 (Manual entry for parents)

**Phase 3** - 4 weeks
- US-5.2 (Analytics)
- Epic 6 (Admin features)
- OCR implementation

**Phase 4** - Ongoing
- Performance optimizations
- Technical debt resolution
- Future enhancements

---

## Appendix: Estimation

| Epic | User Stories | Story Points | Estimated Weeks |
|------|-------------|--------------|----------------|
| Epic 1: Learning Module | 6 | 21 | 3 |
| Epic 2: Practice Mode | 9 | 34 | 4 |
| Epic 3: Practice Header | 4 | 13 | 2 |
| Epic 4: Mock Tests | 8 | 34 | 4 |
| Epic 5: Parent Features | 2 | 13 | 2 |
| Epic 6: Admin Features | 3 | 21 | 3 |
| **Total** | **32** | **136** | **18** |

*Note: 1 Story Point ≈ 1 ideal day of work. Estimates include development, testing, and review.*
