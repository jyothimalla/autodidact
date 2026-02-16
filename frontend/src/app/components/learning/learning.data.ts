import { LearningModule } from './learning.models';

export const LEARNING_MODULES: LearningModule[] = [
  {
    id: 'four-operations',
    name: 'Four Operations',
    description: 'Master core arithmetic with method choice and accuracy.',
    icon: '🧮',
    progress: 60,
    atoms: [
      {
        id: 'addition-subtraction-core',
        moduleId: 'four-operations',
        name: 'Addition and Subtraction Core',
        level: 1,
        status: 'developing',
        summary: 'Build confidence with single-step calculations.',
        videoUrl: 'https://www.youtube.com/embed/NybHckSEQBI',
        teachingNotes: 'Start with concrete manipulatives (counters, base-ten blocks) before moving to written methods. Ensure students can explain what "carrying" and "borrowing" mean in plain language before drilling the written method.',
        commonMistakes: [
          'Not aligning digits by place value',
          'Forgetting to carry the 1 after addition',
          'Borrowing incorrectly — reducing the wrong column',
          'Treating subtraction as commutative (e.g., 3 − 7 = 4)'
        ],
        prerequisites: ['Place value to 4 digits', 'Number bonds to 20'],
        teachingStrategies: [
          'Column method with clear place-value headings',
          'Number line jumps for mental checking',
          'Inverse check: use addition to verify subtraction answers'
        ],
        assessmentCriteria: 'Student can reliably add and subtract any two 3-digit numbers using the column method with no more than 1 error in 10 questions.',
        estimatedMinutes: 30
      },
      {
        id: 'multiplication-division-core',
        moduleId: 'four-operations',
        name: 'Multiplication and Division Core',
        level: 2,
        status: 'weak',
        summary: 'From tables recall to short method fluency.',
        videoUrl: 'https://www.youtube.com/embed/EI2qZC1vUGk',
        teachingNotes: 'Check times-table fluency first (2–12×). Students who cannot recall tables under 5 seconds will struggle with short multiplication. Teach division as the inverse of multiplication explicitly.',
        commonMistakes: [
          'Confusing the multiplier and multiplicand positions',
          'Omitting the placeholder zero in long multiplication',
          'Dividing left to right but forgetting to carry remainders',
          'Stating remainders as decimals when integers are expected'
        ],
        prerequisites: ['Times tables 2–12', 'Addition and Subtraction Core'],
        teachingStrategies: [
          'Short multiplication: multiply each digit separately, carry above',
          'Chunking division for weaker students before introducing short division',
          'Arrays and area models to build conceptual understanding'
        ],
        assessmentCriteria: 'Student completes 10 short multiplication and 10 short division questions with at least 80% accuracy within 5 minutes.',
        estimatedMinutes: 40
      },
      {
        id: 'mixed-operation-word-problems',
        moduleId: 'four-operations',
        name: 'Mixed Operation Word Problems',
        level: 3,
        status: 'weak',
        summary: 'Choose the correct operation in context.',
        videoUrl: 'https://www.youtube.com/embed/Y6M89-6106I',
        teachingNotes: 'Emphasise the reading phase: underline the key numbers and the question. Many errors come from rushing to calculate before identifying what is being asked. Teach students to write the bare calculation before doing it.',
        commonMistakes: [
          'Choosing the wrong operation because of "trigger words" (e.g., assuming "more" always means addition)',
          'Using all numbers in the problem whether needed or not',
          'Rounding intermediate answers, causing errors in multi-step problems'
        ],
        prerequisites: ['Addition and Subtraction Core', 'Multiplication and Division Core'],
        teachingStrategies: [
          'RUCSAC strategy: Read, Underline, Choose, Solve, Answer, Check',
          'Think-aloud modelling with worked examples',
          'Paired problem solving with verbal justification'
        ],
        assessmentCriteria: 'Student can correctly identify the required operation and produce a correct answer for 4 out of 5 one-step word problems across all four operations.',
        estimatedMinutes: 35
      }
    ]
  },
  {
    id: 'fractions-decimals',
    name: 'Fractions and Decimals',
    description: 'Understand equivalent values, comparisons, and conversions.',
    icon: '🍕',
    progress: 40,
    atoms: [
      {
        id: 'equivalent-fractions',
        moduleId: 'fractions-decimals',
        name: 'Equivalent Fractions',
        level: 1,
        status: 'developing',
        summary: 'Spot different forms of the same value.',
        videoUrl: 'https://www.youtube.com/embed/tDQipFjAoT8',
        teachingNotes: 'Use fraction walls and pizza diagrams before moving to symbolic methods. Students must understand that multiplying numerator and denominator by the same number does not change value — connect to the identity property (multiplying by 1).',
        commonMistakes: [
          'Adding instead of multiplying numerator and denominator',
          'Multiplying numerator but forgetting the denominator',
          'Confusing simplification with finding equivalents'
        ],
        prerequisites: ['Multiplication tables', 'Understanding of numerator and denominator'],
        teachingStrategies: [
          'Fraction wall visual — shade and compare',
          'Multiply/divide both parts by the same number',
          'Spot-the-pattern exercises using factor families'
        ],
        assessmentCriteria: 'Student can generate two equivalent fractions for any given fraction and simplify a fraction to its lowest terms.',
        estimatedMinutes: 25
      },
      {
        id: 'comparing-fractions',
        moduleId: 'fractions-decimals',
        name: 'Comparing Fractions',
        level: 2,
        status: 'weak',
        summary: 'Order and compare using common denominators.',
        videoUrl: 'https://www.youtube.com/embed/48Z8iGPKQqk',
        teachingNotes: 'Students often incorrectly think a larger denominator means a larger fraction. Begin with unit fractions (1/n) to build intuition, then extend to non-unit fractions. Finding the LCM is the core skill here.',
        commonMistakes: [
          'Comparing denominators directly without finding common denominator',
          'Thinking 1/8 > 1/3 because 8 > 3',
          'Errors in finding LCM, especially for larger denominators'
        ],
        prerequisites: ['Equivalent Fractions', 'Multiples and LCM'],
        teachingStrategies: [
          'Number line placement of fractions',
          'Convert to common denominator then compare numerators',
          'Cross-multiplication method for quick comparison of two fractions'
        ],
        assessmentCriteria: 'Student can order four fractions with different denominators from smallest to largest with full working shown.',
        estimatedMinutes: 30
      },
      {
        id: 'fraction-decimal-conversion',
        moduleId: 'fractions-decimals',
        name: 'Fraction to Decimal Conversion',
        level: 3,
        status: 'weak',
        summary: 'Convert quickly and apply in word problems.',
        videoUrl: 'https://www.youtube.com/embed/A6zP8dlrA2Y',
        teachingNotes: 'Teach common equivalences (1/4=0.25, 1/3=0.333…, 1/2=0.5) by heart first. Then show the division method (numerator ÷ denominator) for others. Recurring decimals need careful handling — acknowledge them but do not expect full mastery at this level.',
        commonMistakes: [
          'Writing 1/4 as 0.4 instead of 0.25',
          'Confusing the direction of conversion',
          'Not recognising that 0.3 ≠ 1/3'
        ],
        prerequisites: ['Equivalent Fractions', 'Short division'],
        teachingStrategies: [
          'Memorise key benchmarks: halves, quarters, tenths, fifths',
          'Division method: divide numerator by denominator',
          'Place-value chart to show tenths/hundredths columns'
        ],
        assessmentCriteria: 'Student can convert any fraction with denominator 2, 4, 5, 8, 10, 25, or 100 to a decimal without a calculator.',
        estimatedMinutes: 25
      }
    ]
  },
  {
    id: 'ratios',
    name: 'Ratios',
    description: 'Solve ratio sharing and missing-value reasoning questions.',
    icon: '⚖️',
    progress: 35,
    atoms: [
      {
        id: 'ratio-interpretation',
        moduleId: 'ratios',
        name: 'Ratio Interpretation',
        level: 1,
        status: 'developing',
        summary: 'Read and simplify basic ratios.',
        videoUrl: 'https://www.youtube.com/embed/8q5l2V8xQ8I',
        teachingNotes: 'Begin with concrete contexts (mixing paint, recipe scaling). Students must understand that a ratio compares parts, not part to whole. Distinguish clearly between ratio and fraction notation early.',
        commonMistakes: [
          'Confusing ratio with fraction (e.g., treating 2:3 as 2/3)',
          'Simplifying only one side of the ratio',
          'Reversing the order of the ratio from the question'
        ],
        prerequisites: ['Factors and HCF', 'Multiplication tables'],
        teachingStrategies: [
          'Bar model to represent ratio parts visually',
          'Divide both parts by the HCF to simplify',
          'Contextual problems first, abstract after'
        ],
        assessmentCriteria: 'Student can write, read, and simplify ratios given in words or notation.',
        estimatedMinutes: 25
      },
      {
        id: 'ratio-sharing',
        moduleId: 'ratios',
        name: 'Sharing in a Ratio',
        level: 2,
        status: 'weak',
        summary: 'Split totals correctly using ratio parts.',
        videoUrl: 'https://www.youtube.com/embed/gM3Q8f4fYUw',
        teachingNotes: 'The key step students miss is finding the value of one part. Always write: total parts = sum of ratio → value of 1 part = total ÷ total parts → each share = part × value of 1 part. Repeat this structure explicitly.',
        commonMistakes: [
          'Dividing the total by the number of terms rather than the sum of the ratio',
          'Forgetting to multiply back to find each share',
          'Using the wrong total when a partial amount is given'
        ],
        prerequisites: ['Ratio Interpretation', 'Division'],
        teachingStrategies: [
          'Step-by-step scaffold: (1) add parts, (2) divide total, (3) multiply each share',
          'Bar model — equal-width boxes for each part',
          'Reverse sharing: given one share, find the total'
        ],
        assessmentCriteria: 'Student correctly shares an amount in a given ratio, showing all three working steps.',
        estimatedMinutes: 30
      }
    ]
  },
  {
    id: 'percentages',
    name: 'Percentages',
    description: 'Work with percentages, changes, and reverse calculations.',
    icon: '💯',
    progress: 30,
    atoms: [
      {
        id: 'percentage-of-quantity',
        moduleId: 'percentages',
        name: 'Percentage of Quantity',
        level: 1,
        status: 'developing',
        summary: 'Calculate common percentages confidently.',
        videoUrl: 'https://www.youtube.com/embed/_M7M6dQ5x5M',
        teachingNotes: 'Build from 50% (÷2), 25% (÷4), 10% (÷10), 1% (÷100) as benchmark methods. Students who understand these can combine them for 15%, 35%, etc. Avoid the formula method until benchmarks are secure.',
        commonMistakes: [
          'Dividing by the percentage instead of 100',
          'Finding 10% then forgetting to scale (e.g., for 30%)',
          'Confusing % of quantity with % change'
        ],
        prerequisites: ['Division by 2, 4, 10, 100', 'Fractions and Decimals basics'],
        teachingStrategies: [
          'Benchmark method: 10% first, then scale',
          'Multiplier method: convert % to decimal, then multiply',
          'Percentage spider diagrams for quick reference'
        ],
        assessmentCriteria: 'Student finds any multiple of 5% of a whole number quantity without a calculator, showing their method.',
        estimatedMinutes: 25
      },
      {
        id: 'increase-decrease',
        moduleId: 'percentages',
        name: 'Percentage Increase and Decrease',
        level: 2,
        status: 'weak',
        summary: 'Apply changes to round and non-round numbers.',
        videoUrl: 'https://www.youtube.com/embed/lfJwNwM9jL8',
        teachingNotes: 'Two methods: (1) find the % and add/subtract; (2) multiplier method (e.g., 20% increase → × 1.2). Method 2 is faster and essential for compound changes later. Ensure students understand that a 20% increase followed by a 20% decrease does not return to the original.',
        commonMistakes: [
          'Adding the percentage number directly instead of the calculated amount',
          'Using the wrong multiplier (e.g., × 0.8 for a 20% increase)',
          'Assuming percentage changes are reversible'
        ],
        prerequisites: ['Percentage of Quantity', 'Decimal multiplication'],
        teachingStrategies: [
          'Multiplier table: increase by n% → ×(1 + n/100), decrease → ×(1 − n/100)',
          'Bar model for visualising the original and new amounts',
          'Worked examples with money contexts (sales, tax)'
        ],
        assessmentCriteria: 'Student correctly applies percentage increase and decrease using the multiplier method for at least 4 of 5 problems.',
        estimatedMinutes: 30
      }
    ]
  },
  {
    id: 'multi-step-word-problems',
    name: 'Multi-step Word Problems',
    description: 'Extract data, plan steps, and avoid trap-style mistakes.',
    icon: '🧩',
    progress: 25,
    atoms: [
      {
        id: 'two-step-problems',
        moduleId: 'multi-step-word-problems',
        name: 'Two-step Problems',
        level: 1,
        status: 'developing',
        summary: 'Break questions into clear, logical steps.',
        videoUrl: 'https://www.youtube.com/embed/2WlC8r6Zdrs',
        teachingNotes: 'Explicitly model how to identify intermediate questions within the problem. Use a "what do I need to find first?" prompt before starting. Students should write their plan in words before calculating.',
        commonMistakes: [
          'Answering the intermediate step, not the final question',
          'Using the wrong intermediate result in the second step',
          'Not labelling units in the answer'
        ],
        prerequisites: ['All Four Operations', 'Single-step word problems'],
        teachingStrategies: [
          'Annotate the problem: circle numbers, box the question',
          'Write a plan: "First I will… then I will…"',
          'Table format: Step | Calculation | Result'
        ],
        assessmentCriteria: 'Student correctly solves two-step problems showing a clear plan and both working steps.',
        estimatedMinutes: 30
      },
      {
        id: 'mixed-topic-reasoning',
        moduleId: 'multi-step-word-problems',
        name: 'Mixed-topic Reasoning',
        level: 3,
        status: 'weak',
        summary: 'Handle hidden information in longer prompts.',
        videoUrl: 'https://www.youtube.com/embed/5juto2ze8Lg',
        teachingNotes: 'These questions combine multiple topic areas. Students must slow down and extract only the relevant data. Common traps include irrelevant numbers and embedded unit conversions. Teach systematic elimination of irrelevant information.',
        commonMistakes: [
          'Using all numbers present rather than selecting the relevant ones',
          'Missing an embedded unit conversion',
          'Stopping after answering an intermediate question'
        ],
        prerequisites: ['Two-step Problems', 'Percentages', 'Ratios', 'Fractions'],
        teachingStrategies: [
          'Colour-coding: highlight used numbers, cross out unused',
          'Work backwards from the question to identify needed information',
          'Peer discussion: "what information is not needed?"'
        ],
        assessmentCriteria: 'Student extracts the correct data and solves a multi-topic reasoning question with full, labelled working.',
        estimatedMinutes: 40
      }
    ]
  },
  {
    id: 'mental-arithmetic',
    name: 'Mental Arithmetic',
    description: 'Build speed and working-memory fluency under short timers.',
    icon: '⚡',
    progress: 55,
    atoms: [
      {
        id: 'quick-add-subtract',
        moduleId: 'mental-arithmetic',
        name: 'Quick Add and Subtract',
        level: 1,
        status: 'strong',
        summary: 'Use number bonds and compensation strategies.',
        videoUrl: 'https://www.youtube.com/embed/_NN8g2jWIAs',
        teachingNotes: 'Focus on number bonds to 10, 20, and 100. Compensation (e.g., +19 = +20 − 1) is the highest-value mental strategy. Near-double strategies (8+7 = double 7 + 1) should also be automatic. Time pressure is helpful once the strategies are known.',
        commonMistakes: [
          'Reverting to written methods under time pressure',
          'Applying compensation in the wrong direction (adding instead of subtracting the extra)',
          'Slow recall of number bonds to 10 causing cascade errors'
        ],
        prerequisites: ['Number bonds to 20', 'Place value to 1000'],
        teachingStrategies: [
          'Daily 60-second drill: random addition and subtraction within 100',
          'Compensation strategy cards with examples',
          'Partner quizzing with instant feedback'
        ],
        assessmentCriteria: 'Student answers 20 mental addition/subtraction questions within 60 seconds with 90%+ accuracy.',
        estimatedMinutes: 20
      },
      {
        id: 'estimation-approximation',
        moduleId: 'mental-arithmetic',
        name: 'Estimation and Approximation',
        level: 2,
        status: 'developing',
        summary: 'Estimate quickly, then refine to exact answers.',
        videoUrl: 'https://www.youtube.com/embed/BZ4FjSXjzgg',
        teachingNotes: 'Rounding to the nearest 10 or 100 before calculating is the foundation. Stress that estimates are used to check reasonableness, not to replace the exact answer. "Is my answer sensible?" should become a reflex.',
        commonMistakes: [
          'Rounding both numbers up, causing over-estimation',
          'Presenting the estimate as the final answer',
          'Not using estimation to check — spot large discrepancies'
        ],
        prerequisites: ['Rounding to 10, 100, 1000', 'Quick Add and Subtract'],
        teachingStrategies: [
          'Round-then-calculate workflow for every word problem',
          'Sanity check: is the answer in the right ballpark?',
          'Error estimation: how far off can rounding make us?'
        ],
        assessmentCriteria: 'Student estimates the answer to a calculation before solving, and flags if their exact answer differs from the estimate by more than 20%.',
        estimatedMinutes: 20
      }
    ]
  },
  {
    id: 'speed-based-calculation',
    name: 'Speed-Based Calculation',
    description: 'Simulate exam pressure with timed mixed arithmetic.',
    icon: '🚀',
    progress: 45,
    atoms: [
      {
        id: 'rapid-mixed-arithmetic',
        moduleId: 'speed-based-calculation',
        name: 'Rapid Mixed Arithmetic',
        level: 1,
        status: 'developing',
        summary: 'Increase pace while protecting accuracy.',
        videoUrl: 'https://www.youtube.com/embed/mAvuom42NyY',
        teachingNotes: 'Speed should only be pushed once accuracy is above 85%. Use the "floor" principle: set a minimum accuracy before reducing time. Students who rush and make errors should slow down first, then speed up progressively.',
        commonMistakes: [
          'Sacrificing accuracy for speed',
          'Getting stuck on a hard question instead of moving on',
          'Inconsistent operation choice when questions are mixed'
        ],
        prerequisites: ['All Four Operations at 80%+ accuracy'],
        teachingStrategies: [
          'Timed grids: start at 2 min, reduce by 10 sec each session',
          'Skip-and-return: mark a question and come back to it',
          'Operation signposting: underline +/−/×/÷ symbol before answering'
        ],
        assessmentCriteria: 'Student completes 20 mixed arithmetic questions in under 3 minutes with at least 85% accuracy.',
        estimatedMinutes: 20
      },
      {
        id: 'adaptive-timing',
        moduleId: 'speed-based-calculation',
        name: 'Adaptive Timing Drills',
        level: 2,
        status: 'weak',
        summary: 'Answer harder questions with less time.',
        videoUrl: 'https://www.youtube.com/embed/qmfXyR7Z6Lk',
        teachingNotes: 'Adaptive timing means the student has fewer seconds per question as difficulty increases. This mirrors real exam pressure. Introduce this only after rapid-mixed arithmetic is secure. Build in reflection time after each drill.',
        commonMistakes: [
          'Freezing when the timer is short — emphasise moving on',
          'Reverting to long methods under time pressure',
          'Not reviewing wrong answers after the drill'
        ],
        prerequisites: ['Rapid Mixed Arithmetic', 'All standard written methods'],
        teachingStrategies: [
          'Per-question timer visible on screen',
          'Post-drill analysis: categorise errors by type',
          'Difficulty ladder: increase question complexity each week'
        ],
        assessmentCriteria: 'Student maintains 80%+ accuracy when allowed only 8 seconds per question on mixed difficulty arithmetic.',
        estimatedMinutes: 25
      }
    ]
  },
  {
    id: 'logical-number-puzzles',
    name: 'Logical Number Puzzles',
    description: 'Solve pattern and deduction puzzles with structured logic.',
    icon: '🧠',
    progress: 50,
    atoms: [
      {
        id: 'number-sequences',
        moduleId: 'logical-number-puzzles',
        name: 'Number Sequences',
        level: 1,
        status: 'strong',
        summary: 'Find rules behind sequence changes.',
        videoUrl: 'https://www.youtube.com/embed/r3qKojj4g4g',
        teachingNotes: 'Sequences should be explored by finding the difference between consecutive terms first. Arithmetic sequences (constant difference) come before geometric (constant ratio). Encourage students to describe the rule in words before writing it algebraically.',
        commonMistakes: [
          'Assuming all sequences are arithmetic (constant difference)',
          'Calculating the wrong term position (off-by-one errors)',
          'Not checking the rule against multiple terms, only the first two'
        ],
        prerequisites: ['All Four Operations', 'Negative numbers (for decreasing sequences)'],
        teachingStrategies: [
          'Difference table: list the gaps between consecutive terms',
          'Rule in words: "Start at ___, add ___ each time"',
          'Predict then verify: student predicts next term, checks with calculation'
        ],
        assessmentCriteria: 'Student identifies the rule and correctly extends an arithmetic or geometric sequence by at least 3 terms.',
        estimatedMinutes: 20
      },
      {
        id: 'deduction-puzzles',
        moduleId: 'logical-number-puzzles',
        name: 'Deduction Puzzles',
        level: 3,
        status: 'developing',
        summary: 'Use constraints and elimination techniques.',
        videoUrl: 'https://www.youtube.com/embed/HdU_rf7eMTI',
        teachingNotes: 'Deduction puzzles (cryptarithmetic, logic grids, missing-digit problems) build systematic thinking. The key skill is "if this, then not that" reasoning. Model how to record eliminations so students do not re-test ruled-out options.',
        commonMistakes: [
          'Guessing randomly instead of eliminating systematically',
          'Not recording eliminated options, leading to repeated guesses',
          'Ignoring a constraint after partially applying it'
        ],
        prerequisites: ['Number Sequences', 'Addition and Subtraction', 'Multiplication tables'],
        teachingStrategies: [
          'Grid elimination: cross out impossible options in a table',
          'Think-aloud walkthroughs of worked examples',
          'Work from the most constrained position first'
        ],
        assessmentCriteria: 'Student solves a deduction puzzle by recording every elimination step and arriving at the unique correct answer.',
        estimatedMinutes: 35
      }
    ]
  }
];
