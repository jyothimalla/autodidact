import { Subject, LearningTopic } from './learning.models';

// Four Operations Topics with separate Addition, Subtraction, Multiplication, Division
const FOUR_OPERATIONS_TOPICS: LearningTopic[] = [
  {
    id: 'addition',
    name: 'Addition',
    description: 'Master addition from single digits to multi-digit numbers',
    icon: '➕',
    levels: [
      {
        id: 'addition-level-1',
        moduleId: 'four-operations',
        name: 'Addition Level 1',
        level: 1,
        status: 'developing',
        summary: 'Single and double-digit addition with carrying',
        videoUrl: 'https://www.youtube.com/embed/NybHckSEQBI',
        teachingNotes: 'Start with concrete manipulatives (counters, base-ten blocks) before moving to written methods. Ensure students can explain what "carrying" means in plain language.',
        commonMistakes: [
          'Not aligning digits by place value',
          'Forgetting to carry the 1',
          'Adding digits in wrong columns'
        ],
        prerequisites: ['Place value to 4 digits', 'Number bonds to 20'],
        teachingStrategies: [
          'Column method with clear place-value headings',
          'Number line jumps for mental checking',
          'Use addition grids for practice'
        ],
        assessmentCriteria: 'Student can reliably add any two 3-digit numbers using the column method.',
        estimatedMinutes: 30
      },
      {
        id: 'addition-level-2',
        moduleId: 'four-operations',
        name: 'Addition Level 2',
        level: 2,
        status: 'weak',
        summary: 'Three and four-digit addition with multiple carries',
        videoUrl: 'https://www.youtube.com/embed/NybHckSEQBI',
        teachingNotes: 'Focus on systematic carrying across multiple columns. Practice with money and measurement contexts.',
        commonMistakes: [
          'Carrying incorrectly across multiple columns',
          'Mixing up thousands and hundreds columns',
          'Calculation errors in mental arithmetic'
        ],
        prerequisites: ['Addition Level 1', 'Place value to 10,000'],
        teachingStrategies: [
          'Extended column method',
          'Real-world problems with money',
          'Estimate then calculate strategy'
        ],
        assessmentCriteria: 'Student adds four-digit numbers with 90% accuracy.',
        estimatedMinutes: 35
      }
    ]
  },
  {
    id: 'subtraction',
    name: 'Subtraction',
    description: 'Master subtraction including borrowing and regrouping',
    icon: '➖',
    levels: [
      {
        id: 'subtraction-level-1',
        moduleId: 'four-operations',
        name: 'Subtraction Level 1',
        level: 1,
        status: 'developing',
        summary: 'Basic subtraction with borrowing',
        videoUrl: 'https://www.youtube.com/embed/NybHckSEQBI',
        teachingNotes: 'Emphasize understanding of borrowing/regrouping. Use place value blocks to demonstrate.',
        commonMistakes: [
          'Borrowing incorrectly — reducing the wrong column',
          'Treating subtraction as commutative',
          'Subtracting smaller from larger digit regardless of position'
        ],
        prerequisites: ['Place value', 'Addition Level 1'],
        teachingStrategies: [
          'Column method with borrowing visualization',
          'Inverse check: use addition to verify',
          'Number line for mental methods'
        ],
        assessmentCriteria: 'Student subtracts 3-digit numbers with borrowing accurately.',
        estimatedMinutes: 30
      },
      {
        id: 'subtraction-level-2',
        moduleId: 'four-operations',
        name: 'Subtraction Level 2',
        level: 2,
        status: 'weak',
        summary: 'Multi-digit subtraction with multiple borrowing',
        videoUrl: 'https://www.youtube.com/embed/NybHckSEQBI',
        teachingNotes: 'Practice systematic borrowing across zeros. Build confidence with word problems.',
        commonMistakes: [
          'Errors when borrowing across zeros',
          'Confusion with place value in large numbers',
          'Not checking answers with addition'
        ],
        prerequisites: ['Subtraction Level 1'],
        teachingStrategies: [
          'Special focus on borrowing across zeros',
          'Real-world contexts (change, measurements)',
          'Always verify with inverse operation'
        ],
        assessmentCriteria: 'Student subtracts four-digit numbers including zeros with 85% accuracy.',
        estimatedMinutes: 35
      }
    ]
  },
  {
    id: 'multiplication',
    name: 'Multiplication',
    description: 'From times tables to long multiplication',
    icon: '✖️',
    levels: [
      {
        id: 'multiplication-level-1',
        moduleId: 'four-operations',
        name: 'Multiplication Level 1',
        level: 1,
        status: 'developing',
        summary: 'Times tables and short multiplication',
        videoUrl: 'https://www.youtube.com/embed/EI2qZC1vUGk',
        teachingNotes: 'Ensure times tables (2-12) are fluent before moving to written methods. Use arrays to build understanding.',
        commonMistakes: [
          'Confusing multiplier and multiplicand',
          'Errors in times table recall',
          'Forgetting to carry'
        ],
        prerequisites: ['Times tables 2-12', 'Addition with carrying'],
        teachingStrategies: [
          'Short multiplication: grid method first',
          'Arrays and area models',
          'Times table rapid recall practice'
        ],
        assessmentCriteria: 'Student completes short multiplication with 85% accuracy.',
        estimatedMinutes: 30
      },
      {
        id: 'multiplication-level-2',
        moduleId: 'four-operations',
        name: 'Multiplication Level 2',
        level: 2,
        status: 'weak',
        summary: 'Long multiplication and multi-digit problems',
        videoUrl: 'https://www.youtube.com/embed/EI2qZC1vUGk',
        teachingNotes: 'Teach placeholder zeros systematically. Practice with partitioning method first.',
        commonMistakes: [
          'Omitting placeholder zero in long multiplication',
          'Alignment errors in partial products',
          'Addition errors when combining rows'
        ],
        prerequisites: ['Multiplication Level 1', 'Column addition'],
        teachingStrategies: [
          'Grid method for visualization',
          'Standard algorithm with clear spacing',
          'Estimate first, then calculate'
        ],
        assessmentCriteria: 'Student performs long multiplication of 2-digit by 2-digit numbers accurately.',
        estimatedMinutes: 40
      }
    ]
  },
  {
    id: 'division',
    name: 'Division',
    description: 'Division with remainders and long division',
    icon: '➗',
    levels: [
      {
        id: 'division-level-1',
        moduleId: 'four-operations',
        name: 'Division Level 1',
        level: 1,
        status: 'developing',
        summary: 'Short division and remainders',
        videoUrl: 'https://www.youtube.com/embed/EI2qZC1vUGk',
        teachingNotes: 'Teach division as inverse of multiplication. Start with sharing model, then chunking.',
        commonMistakes: [
          'Dividing left to right but forgetting carries',
          'Remainder larger than divisor',
          'Writing remainders as decimals when integers expected'
        ],
        prerequisites: ['Times tables', 'Multiplication Level 1'],
        teachingStrategies: [
          'Short division with bus stop method',
          'Chunking for conceptual understanding',
          'Always check: quotient × divisor + remainder = dividend'
        ],
        assessmentCriteria: 'Student completes short division with remainders accurately.',
        estimatedMinutes: 35
      },
      {
        id: 'division-level-2',
        moduleId: 'four-operations',
        name: 'Division Level 2',
        level: 2,
        status: 'weak',
        summary: 'Long division and division with larger numbers',
        videoUrl: 'https://www.youtube.com/embed/EI2qZC1vUGk',
        teachingNotes: 'Build up from short division. Use estimation to determine quotient digits.',
        commonMistakes: [
          'Incorrect estimation of quotient digits',
          'Multiplication errors within division',
          'Not bringing down digits systematically'
        ],
        prerequisites: ['Division Level 1', 'Multiplication Level 2'],
        teachingStrategies: [
          'Long division algorithm step by step',
          'Estimate, multiply, subtract, bring down pattern',
          'Practice with real-world sharing problems'
        ],
        assessmentCriteria: 'Student performs long division by single-digit divisor with 80% accuracy.',
        estimatedMinutes: 40
      }
    ]
  }
];

export const SUBJECTS: Subject[] = [
  {
    id: 'maths',
    name: 'Maths',
    icon: '🔢',
    description: 'Master arithmetic, algebra, and problem-solving',
    modules: [
      {
        id: 'four-operations',
        name: 'Four Operations',
        description: 'Addition, Subtraction, Multiplication, Division',
        icon: '🧮',
        progress: 60,
        topics: FOUR_OPERATIONS_TOPICS
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
            teachingNotes: 'Use fraction walls and pizza diagrams before moving to symbolic methods.',
            commonMistakes: [
              'Adding instead of multiplying numerator and denominator',
              'Multiplying numerator but forgetting the denominator'
            ],
            prerequisites: ['Multiplication tables', 'Understanding of numerator and denominator'],
            teachingStrategies: [
              'Fraction wall visual — shade and compare',
              'Multiply/divide both parts by the same number'
            ],
            assessmentCriteria: 'Student can generate two equivalent fractions for any given fraction.',
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
        atoms: []
      },
      {
        id: 'percentages',
        name: 'Percentages',
        description: 'Work with percentages, changes, and reverse calculations.',
        icon: '💯',
        progress: 30,
        atoms: []
      },
      {
        id: 'word-problems',
        name: 'Multi-step Word Problems',
        description: 'Solve complex real-world problems using multiple operations.',
        icon: '🧩',
        progress: 25,
        atoms: []
      },
      {
        id: 'mental-arithmetic',
        name: 'Mental Arithmetic',
        description: 'Quick mental calculation strategies and number sense.',
        icon: '⚡',
        progress: 40,
        atoms: []
      },
      {
        id: 'speed-calculation',
        name: 'Speed-Based Calculation',
        description: 'Build calculation speed and accuracy under time pressure.',
        icon: '🚀',
        progress: 20,
        atoms: []
      },
      {
        id: 'number-puzzles',
        name: 'Logical Number Puzzles',
        description: 'Pattern recognition and logical thinking with numbers.',
        icon: '🧠',
        progress: 15,
        atoms: []
      },
      {
        id: 'probability',
        name: 'Probability',
        description: 'Calculate likelihood and understand chance events.',
        icon: '🎲',
        progress: 10,
        atoms: [
          {
            id: 'probability-level-1',
            moduleId: 'probability',
            name: 'Basic Probability',
            level: 1,
            status: 'weak',
            summary: 'Understand equally likely outcomes and express probability as a fraction',
            videoUrl: 'https://www.youtube.com/embed/KzfWUEJjG18',
            teachingNotes: 'Introduce probability as a fraction: favourable outcomes / total outcomes. Use physical objects (bags of counters, dice, coins) before moving to abstract examples. Ensure students understand that probability sits between 0 and 1.',
            commonMistakes: [
              'Writing probability as a ratio instead of a fraction',
              'Not simplifying the fraction to its lowest terms',
              'Confusing favourable outcomes with total outcomes',
              'Thinking higher numbers of trials always match exact theoretical probability'
            ],
            prerequisites: ['Fractions and Decimals Level 1', 'Understanding of simplifying fractions'],
            teachingStrategies: [
              'Bag of coloured counters — students pick and record outcomes',
              'Probability scale from 0 (impossible) to 1 (certain)',
              'Lots of worked examples: dice, spinners, cards',
              'Venn diagrams to show overlapping events'
            ],
            assessmentCriteria: 'Student can write the probability of a simple event as a fraction in its simplest form.',
            estimatedMinutes: 35
          },
          {
            id: 'probability-level-2',
            moduleId: 'probability',
            name: 'Combined Events & Probability',
            level: 2,
            status: 'weak',
            summary: 'Use probability notation, P(not A), and combined events with two spinners or coins',
            videoUrl: 'https://www.youtube.com/embed/KzfWUEJjG18',
            teachingNotes: 'Extend to P(not A) = 1 − P(A) and combined events using sample space diagrams. Introduce the multiplication rule for independent events. Use two-way tables for systematic listing.',
            commonMistakes: [
              'Not listing all outcomes systematically in sample spaces',
              'Forgetting to use P(not A) = 1 − P(A)',
              'Multiplying probabilities when they are not independent',
              'Errors in two-way table totals'
            ],
            prerequisites: ['Basic Probability'],
            teachingStrategies: [
              'Sample space diagrams for two dice / two spinners',
              'Two-way tables for systematic listing',
              'Complement rule worked examples',
              'Tree diagrams introduction for combined events'
            ],
            assessmentCriteria: 'Student calculates P(not A) and combined event probabilities using sample space diagrams with 80% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'algebra',
        name: 'Algebra',
        description: 'Solve equations, work with expressions and formulae.',
        icon: '📐',
        progress: 20,
        atoms: [
          {
            id: 'algebra-level-1',
            moduleId: 'algebra',
            name: 'Expressions and Substitution',
            level: 1,
            status: 'weak',
            summary: 'Write and evaluate algebraic expressions; substitute values into simple formulae',
            videoUrl: 'https://www.youtube.com/embed/tHYis-DP0oU',
            teachingNotes: 'Start with the idea of a letter representing an unknown number. Teach term, expression, equation, and formula as distinct vocabulary. Emphasise the difference between 3n (3 × n) and n³ (n × n × n).',
            commonMistakes: [
              'Writing 3 + n instead of 3n for 3 multiplied by n',
              'Treating 2a and a2 as the same',
              'Substituting incorrectly when negatives are involved',
              'Confusing expressions with equations'
            ],
            prerequisites: ['Four Operations', 'Order of operations (BIDMAS)'],
            teachingStrategies: [
              'Substitution tables — substitute multiple values to see patterns',
              'Real-world formulae: perimeter, temperature conversions',
              'Matching activity: expression cards to worded descriptions',
              'Use colour-coding for different terms'
            ],
            assessmentCriteria: 'Student evaluates expressions like 3x + 2 and ax² + b for given values of x with 85% accuracy.',
            estimatedMinutes: 35
          },
          {
            id: 'algebra-level-2',
            moduleId: 'algebra',
            name: 'Solving Linear Equations',
            level: 2,
            status: 'weak',
            summary: 'Solve one- and two-step equations using the balance method',
            videoUrl: 'https://www.youtube.com/embed/tHYis-DP0oU',
            teachingNotes: 'Teach the balance method: whatever you do to one side, do to the other. Start with one-step equations before two-step. Use bar models to build understanding before abstract algebra. Verify answers by substitution.',
            commonMistakes: [
              'Applying inverse operations in the wrong order',
              'Losing the negative sign when subtracting from both sides',
              'Not checking answers by substituting back',
              'Dividing only one term instead of the whole side'
            ],
            prerequisites: ['Expressions and Substitution'],
            teachingStrategies: [
              'Balance diagrams to visualise both sides',
              'Bar models before abstract equations',
              'Worked examples with step-by-step inverse operations',
              'Self-checking: always substitute back'
            ],
            assessmentCriteria: 'Student solves equations of the form ax + b = c and verifies solutions by substitution, with 85% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'perimeter-area',
        name: 'Perimeter and Areas',
        description: 'Calculate perimeters and areas of various shapes.',
        icon: '📏',
        progress: 30,
        atoms: [
          {
            id: 'perimeter-area-level-1',
            moduleId: 'perimeter-area',
            name: 'Perimeter and Area of Rectangles and Triangles',
            level: 1,
            status: 'weak',
            summary: 'Calculate area and perimeter of rectangles, squares and triangles',
            videoUrl: 'https://www.youtube.com/embed/AAB0WhMwkAk',
            teachingNotes: 'Establish perimeter as the distance around the outside and area as the space inside. Use squared paper to count squares first, then derive formulae. Emphasise that area uses cm² and perimeter uses cm.',
            commonMistakes: [
              'Confusing perimeter and area',
              'Forgetting to halve when calculating triangle area',
              'Using incorrect units (cm vs cm²)',
              'Adding all sides including the interior height for triangle perimeter'
            ],
            prerequisites: ['Four Operations', 'Multiplication tables'],
            teachingStrategies: [
              'Squared paper: count squares for area, count edges for perimeter',
              'Derive formula through repeated counting patterns',
              'Real-world contexts: fencing (perimeter), carpeting (area)',
              'Distinguish height vs slant side in triangle area'
            ],
            assessmentCriteria: 'Student correctly calculates area and perimeter of rectangles, squares and triangles with correct units in 85% of questions.',
            estimatedMinutes: 35
          },
          {
            id: 'perimeter-area-level-2',
            moduleId: 'perimeter-area',
            name: 'Area of Parallelograms and Trapeziums',
            level: 2,
            status: 'weak',
            summary: 'Extend to parallelograms, trapeziums and composite shapes',
            videoUrl: 'https://www.youtube.com/embed/AAB0WhMwkAk',
            teachingNotes: 'Show how parallelogram formula derives from rectangle by cutting and rearranging. For trapezium, demonstrate the ½(a+b)h formula using two identical trapeziums forming a parallelogram. Introduce composite shapes by splitting into simpler shapes.',
            commonMistakes: [
              'Using the slant height instead of the perpendicular height in parallelogram',
              'Forgetting the ½ in the trapezium formula',
              'Miscounting sides in composite shapes',
              'Adding areas when should subtract (shapes with holes)'
            ],
            prerequisites: ['Perimeter and Area Level 1'],
            teachingStrategies: [
              'Cut-and-rearrange activity for parallelogram',
              'Two-trapezium demonstration for the formula',
              'Splitting composite shapes into rectangles/triangles',
              'Worked examples with annotated diagrams'
            ],
            assessmentCriteria: 'Student calculates area of parallelograms, trapeziums and composite shapes with 80% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'angles',
        name: 'Angles',
        description: 'Understand angle types, properties, and calculations.',
        icon: '📐',
        progress: 25,
        atoms: [
          {
            id: 'angles-level-1',
            moduleId: 'angles',
            name: 'Angle Types and Straight-Line Rules',
            level: 1,
            status: 'weak',
            summary: 'Identify angle types and apply rules for angles on a straight line, in triangles and around a point',
            videoUrl: 'https://www.youtube.com/embed/mMLSMtNaIZQ',
            teachingNotes: 'Classify angles: acute (<90°), right (90°), obtuse (90°–180°), reflex (>180°). Teach the three core rules: straight line = 180°, around a point = 360°, triangle = 180°. Use protractors for measurement practice.',
            commonMistakes: [
              'Confusing obtuse and reflex angles',
              'Subtracting from 360° when should use 180° (and vice versa)',
              'Measuring angle from the wrong baseline on a protractor',
              'Not identifying the correct "missing" angle in a diagram'
            ],
            prerequisites: ['Basic number operations', 'Understanding of degrees'],
            teachingStrategies: [
              'Physical protractor practice before written questions',
              'Angle classification sorting activity',
              'Worked examples with clearly labelled diagrams',
              'Estimate before measuring to build number sense'
            ],
            assessmentCriteria: 'Student identifies angle types and finds missing angles using straight-line, around-a-point and triangle rules with 85% accuracy.',
            estimatedMinutes: 35
          },
          {
            id: 'angles-level-2',
            moduleId: 'angles',
            name: 'Angles in Polygons and Parallel Lines',
            level: 2,
            status: 'weak',
            summary: 'Find angles in quadrilaterals, vertically opposite angles, and corresponding/alternate angles',
            videoUrl: 'https://www.youtube.com/embed/mMLSMtNaIZQ',
            teachingNotes: 'Extend to quadrilaterals (sum = 360°). Introduce vertically opposite angles (equal). For parallel lines, teach corresponding (F-angle), alternate (Z-angle) and co-interior angles. Use diagrams labelled with arrow markers for parallel lines.',
            commonMistakes: [
              'Using 180° for quadrilateral angles instead of 360°',
              'Confusing corresponding and alternate angles',
              'Not recognising parallel line markers',
              'Arithmetic errors in multi-step angle calculations'
            ],
            prerequisites: ['Angles Level 1'],
            teachingStrategies: [
              'Quadrilateral tessellation to show 360° sum',
              'F, Z, C shapes on parallel line diagrams',
              'Multi-step angle problems with clear working',
              'Interactive geometry software for visual exploration'
            ],
            assessmentCriteria: 'Student finds missing angles in quadrilaterals and identifies vertically opposite, corresponding, and alternate angles with 80% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'coordinate-geometry',
        name: 'Coordinate Geometry',
        description: 'Plot points, draw shapes, and work with coordinates.',
        icon: '📊',
        progress: 15,
        atoms: [
          {
            id: 'coordinate-geometry-level-1',
            moduleId: 'coordinate-geometry',
            name: 'Plotting and Reading Coordinates',
            level: 1,
            status: 'weak',
            summary: 'Read and plot coordinates in all four quadrants; identify horizontal and vertical distances',
            videoUrl: 'https://www.youtube.com/embed/9Uc62CuFmvM',
            teachingNotes: 'Reinforce "along the corridor, then up the stairs" (x first, then y). Start in the first quadrant only, then extend to all four. Remind students that negative x goes left and negative y goes down.',
            commonMistakes: [
              'Swapping x and y coordinates',
              'Forgetting that negative values go in the opposite direction',
              'Plotting on grid lines instead of intersections',
              'Errors reading coordinates off a scale that is not 1:1'
            ],
            prerequisites: ['Understanding of negative numbers', 'Basic number line work'],
            teachingStrategies: [
              '"Corridor and stairs" mnemonic for (x, y) order',
              'Physical grid on classroom floor for kinesthetic learning',
              'Coordinate art activities',
              'Battleships game for reading and plotting practice'
            ],
            assessmentCriteria: 'Student plots and reads coordinates correctly in all four quadrants, and calculates horizontal/vertical distances between points with 85% accuracy.',
            estimatedMinutes: 35
          },
          {
            id: 'coordinate-geometry-level-2',
            moduleId: 'coordinate-geometry',
            name: 'Midpoints and Shapes on a Grid',
            level: 2,
            status: 'weak',
            summary: 'Find midpoints of line segments and identify vertices of geometric shapes on a coordinate grid',
            videoUrl: 'https://www.youtube.com/embed/9Uc62CuFmvM',
            teachingNotes: 'Teach the midpoint formula as "average of the x-coordinates, average of the y-coordinates". Extend to identifying which quadrant a point is in and plotting vertices of known shapes given some coordinates.',
            commonMistakes: [
              'Not dividing by 2 when finding the midpoint',
              'Sign errors with negative coordinate midpoints',
              'Confusing which quadrant based on sign combination',
              'Plotting the wrong vertex when completing a shape'
            ],
            prerequisites: ['Plotting and Reading Coordinates'],
            teachingStrategies: [
              'Midpoint as "halfway" on a number line first',
              'Complete-the-shape challenges on grid paper',
              'Quadrant identification card sort',
              'Worked examples with step-by-step midpoint calculations'
            ],
            assessmentCriteria: 'Student correctly calculates midpoints and identifies quadrants for given coordinates with 85% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'volumes',
        name: 'Volumes',
        description: 'Calculate volumes of 3D shapes and objects.',
        icon: '📦',
        progress: 10,
        atoms: [
          {
            id: 'volumes-level-1',
            moduleId: 'volumes',
            name: 'Volume of Cuboids and Cubes',
            level: 1,
            status: 'weak',
            summary: 'Calculate volume of cubes and cuboids using V = l × w × h',
            videoUrl: 'https://www.youtube.com/embed/6mWN6Yb2-N0',
            teachingNotes: 'Build cuboids from unit cubes to make volume concrete. Establish the formula V = length × width × height. Emphasise the unit cm³ means "cubic centimetres". Relate to area: volume = base area × height.',
            commonMistakes: [
              'Confusing surface area with volume',
              'Using cm² instead of cm³ for volume',
              'Multiplying only two dimensions instead of three',
              'Errors when dimensions include decimals'
            ],
            prerequisites: ['Perimeter and Area Level 1', 'Multiplication of two and three numbers'],
            teachingStrategies: [
              'Build cuboids with multilink cubes and count layers',
              'Derive formula from counting: rows × columns × layers',
              'Real-world contexts: boxes, fish tanks, packaging',
              'Compare surface area vs volume with the same object'
            ],
            assessmentCriteria: 'Student calculates volume of cubes and cuboids using the formula with correct cm³ units in 85% of questions.',
            estimatedMinutes: 35
          },
          {
            id: 'volumes-level-2',
            moduleId: 'volumes',
            name: 'Volume of Prisms and Cylinders',
            level: 2,
            status: 'weak',
            summary: 'Extend volume to triangular prisms and cylinders using V = cross-section area × length',
            videoUrl: 'https://www.youtube.com/embed/6mWN6Yb2-N0',
            teachingNotes: 'Generalise volume as: area of cross-section × length. For triangular prisms, first calculate the triangular cross-section (½ × b × h). For cylinders, use V = πr²h and allow use of calculator. Ensure students understand that the cross-section must be the uniform face.',
            commonMistakes: [
              'Using the wrong face as the cross-section',
              'Forgetting to halve when calculating the triangular cross-section',
              'Confusing radius and diameter in the cylinder formula',
              'Rounding π too early in the calculation'
            ],
            prerequisites: ['Volumes Level 1', 'Area of triangles'],
            teachingStrategies: [
              'Cross-section slicing activity with play-dough prisms',
              'Compare: cuboid formula as special case of prism formula',
              'Step-by-step cylinder examples with π on calculator',
              'Problem-solving with real-world prisms (ramps, tins)'
            ],
            assessmentCriteria: 'Student calculates volume of triangular prisms and cylinders correctly, showing the cross-section area step, with 80% accuracy.',
            estimatedMinutes: 45
          }
        ]
      }
    ]
  },
  {
    id: 'english',
    name: 'English',
    icon: '📚',
    description: '11+ English preparation: grammar, vocabulary, comprehension, and writing',
    modules: [
      {
        id: 'grammar',
        name: 'Grammar',
        description: 'Parts of speech, sentence structure, and grammar control',
        icon: '✍️',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-grammar-core',
            moduleId: 'grammar',
            name: 'Year 4 Grammar Foundations',
            level: 1,
            status: 'developing',
            summary: 'Build sentence accuracy using tense, agreement, and grammar signals.',
            videoUrl: 'https://www.youtube.com/embed/N5fyb6n3AAE',
            teachingNotes: 'Teach pupils to read the whole sentence first, then test each option for tense, subject-verb agreement, and meaning. Emphasise grammar signals such as time words (yesterday/tomorrow), pronouns, and conjunction clues.',
            commonMistakes: [
              'Picking an option before reading the full sentence',
              'Incorrect tense choice in cloze questions',
              'Subject-verb agreement errors',
              'Selecting grammatically correct but contextually wrong words'
            ],
            prerequisites: ['Confident reading fluency'],
            teachingStrategies: [
              'Practice: cloze drills using short passages with one missing word each',
              'Practice: grammar signal highlighting (underline clue words first)',
              'Challenge: dual-check routine (grammar check then meaning check)',
              'Challenge: timed mixed cloze sets with error analysis after completion',
              'Exam technique: complete grammar rounds in short timed blocks, then review only flagged questions'
            ],
            assessmentCriteria: 'Student completes cloze and grammar multiple-choice questions with at least 75% timed accuracy and clear correction of errors.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'punctuation',
        name: 'Punctuation',
        description: 'Capital letters, full stops, commas, apostrophes, and sentence punctuation',
        icon: '🖊️',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-spag',
            moduleId: 'punctuation',
            name: 'Year 4 Spelling and Punctuation Accuracy',
            level: 1,
            status: 'weak',
            summary: 'Secure punctuation, common spelling patterns, and sentence correctness under exam timing.',
            videoUrl: 'https://www.youtube.com/embed/XnN6x6Q7fS8',
            teachingNotes: 'Cover commas in lists, apostrophes for contraction/possession, capital letters, and full stops first. For spelling, prioritise frequent exam patterns (prefixes/suffixes, silent letters, homophones). Keep correction routines short and consistent.',
            commonMistakes: [
              'Missing apostrophes or placing them incorrectly',
              'Inconsistent capital letters and end punctuation',
              'Confusing common homophones (their/there, your/you\'re)',
              'Ignoring spelling patterns and relying only on sound'
            ],
            prerequisites: ['Year 4 Grammar Foundations'],
            teachingStrategies: [
              'Practice: edit-the-sentence drills for punctuation errors',
              'Practice: weekly high-frequency spelling pattern lists',
              'Challenge: mixed SPaG mini-tests with strict timing',
              'Challenge: explain-why corrections to build rule awareness',
              'Exam technique: keep punctuation checks as a final 60-second pass before submission'
            ],
            assessmentCriteria: 'Student identifies and corrects punctuation/spelling errors in mixed MCQ sets with 80% accuracy.',
            estimatedMinutes: 35
          }
        ]
      },
      {
        id: 'synonyms',
        name: 'Synonyms',
        description: 'Choose words with closest meaning in context',
        icon: '🧠',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-synonyms',
            moduleId: 'synonyms',
            name: 'Year 4 Synonyms Practice',
            level: 1,
            status: 'developing',
            summary: 'Build synonym accuracy for grammar-school style English questions.',
            videoUrl: 'https://www.youtube.com/embed/6nqH6iM14sM',
            teachingNotes: 'Focus on meaning in context, not memorising isolated words. Teach students to swap a candidate synonym into the sentence and check if tone and meaning still fit.',
            commonMistakes: [
              'Choosing a word that is related but not closest in meaning',
              'Ignoring sentence context when selecting synonyms',
              'Not checking the tone of the replacement word',
              'Rushing through options without elimination'
            ],
            prerequisites: ['Confident reading fluency', 'Basic dictionary skills'],
            teachingStrategies: [
              'Practice: 10 quick synonym questions daily with timed recall',
              'Practice: context swap method (replace and reread the sentence)',
              'Challenge: mixed synonym sets with near-meaning distractors',
              'Challenge: one-minute rounds where students justify each choice',
              'Exam technique: use elimination-first strategy like verbal-skills papers'
            ],
            assessmentCriteria: 'Student answers Year 4 synonym questions with at least 80% accuracy across timed sets.',
            estimatedMinutes: 30
          }
        ]
      },
      {
        id: 'antonyms',
        name: 'Antonyms',
        description: 'Identify opposite meanings accurately and quickly',
        icon: '↔️',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-antonyms',
            moduleId: 'antonyms',
            name: 'Year 4 Antonyms Practice',
            level: 1,
            status: 'developing',
            summary: 'Strengthen opposite-meaning recognition for entrance-style MCQs.',
            videoUrl: 'https://www.youtube.com/embed/6nqH6iM14sM',
            teachingNotes: 'Teach antonyms by meaning pairs and context use. Encourage checking whether the selected opposite still fits sentence grammar when inserted.',
            commonMistakes: [
              'Choosing unrelated words instead of true opposites',
              'Confusing formal/informal variants as antonyms',
              'Ignoring sentence clues',
              'Selecting a partial opposite that changes only one aspect'
            ],
            prerequisites: ['Year 4 Synonyms Practice'],
            teachingStrategies: [
              'Practice: opposite-pair drills grouped by theme',
              'Practice: sentence-based antonym replacement tasks',
              'Challenge: timed antonym ladders with increasing difficulty',
              'Challenge: error review by distractor type',
              'Exam technique: mark uncertain items and return after completing easier verbal questions'
            ],
            assessmentCriteria: 'Student selects correct antonyms in mixed MCQ sets with at least 80% accuracy.',
            estimatedMinutes: 30
          }
        ]
      },
      {
        id: 'comprehension',
        name: 'Comprehension',
        description: 'Reading understanding and inference',
        icon: '📖',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-language-analysis',
            moduleId: 'comprehension',
            name: 'Year 4 Language Analysis and Inference',
            level: 1,
            status: 'developing',
            summary: 'Answer meaning, tone, and inference questions using evidence from short passages.',
            videoUrl: 'https://www.youtube.com/embed/V8f1UBCDgJ0',
            teachingNotes: 'Train students to locate evidence lines before choosing an option. For inference, use the structure: quote evidence, infer meaning, match option. Build stamina with short but regular passage work rather than occasional long sessions.',
            commonMistakes: [
              'Answering from memory instead of checking the text',
              'Choosing an option that sounds nice but lacks evidence',
              'Missing tone clues in descriptive vocabulary',
              'Spending too long on one difficult inference item'
            ],
            prerequisites: ['Year 4 Synonyms Practice'],
            teachingStrategies: [
              'Practice: 1 short passage + 5 questions every study session',
              'Practice: underline-evidence-before-answer routine',
              'Challenge: mixed language-analysis sets under section timing',
              'Challenge: review wrong answers by question type (literal, inference, vocabulary-in-context)',
              'Exam technique: reading-comprehension approach (skim questions, read passage, then answer with line evidence)'
            ],
            assessmentCriteria: 'Student answers language-analysis and inference questions with evidence-based reasoning and at least 75% accuracy.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'creative-writing',
        name: 'Creative Writing',
        description: 'Imaginative writing with strong vocabulary and structure',
        icon: '📝',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-creative-writing',
            moduleId: 'creative-writing',
            name: 'Year 4 Creative Writing Essentials',
            level: 1,
            status: 'developing',
            summary: 'Plan and write imaginative responses with clear openings, detail, and endings.',
            videoUrl: 'https://www.youtube.com/embed/9RkM4DToJz4',
            teachingNotes: 'Use a simple plan: setting, character, problem, resolution. Prioritise sentence quality over length. Teach pupils to include sensory detail and varied sentence starters.',
            commonMistakes: [
              'Starting writing without a plan',
              'No clear problem or ending',
              'Repeated simple sentence starters',
              'Weak paragraph structure'
            ],
            prerequisites: ['Year 4 Grammar Foundations'],
            teachingStrategies: [
              'Practice: 5-minute planning grid before each writing task',
              'Practice: sentence expansion with adjectives and adverbs',
              'Challenge: timed creative prompt writing (15-20 mins)',
              'Challenge: edit and improve one paragraph for impact',
              'Exam technique: spend first 3-4 minutes planning ideas before writing full response'
            ],
            assessmentCriteria: 'Student writes a structured creative response with clear beginning, middle, and end using accurate punctuation.',
            estimatedMinutes: 45
          }
        ]
      },
      {
        id: 'narrative-writing',
        name: 'Narrative Writing',
        description: 'Story writing with plot, character, and sequence control',
        icon: '📘',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-narrative-writing',
            moduleId: 'narrative-writing',
            name: 'Year 4 Narrative Writing Structure',
            level: 1,
            status: 'developing',
            summary: 'Write coherent narratives with paragraph flow and timeline control.',
            videoUrl: 'https://www.youtube.com/embed/2x5vKfW6QVk',
            teachingNotes: 'Teach the narrative arc clearly: opening, build-up, problem, resolution. Encourage pupils to sequence events logically and keep point of view consistent.',
            commonMistakes: [
              'Jumping between events without transitions',
              'Inconsistent tense',
              'No clear climax or resolution',
              'Overuse of dialogue without action'
            ],
            prerequisites: ['Year 4 Creative Writing Essentials'],
            teachingStrategies: [
              'Practice: storyboard planning before writing',
              'Practice: paragraph linking words (later, meanwhile, finally)',
              'Challenge: rewrite a flat paragraph with stronger action verbs',
              'Challenge: timed narrative tasks with peer feedback checklist',
              'Exam technique: keep one clear narrative arc and avoid adding extra plot branches'
            ],
            assessmentCriteria: 'Student produces a sequenced narrative with clear plot progression and controlled tense.',
            estimatedMinutes: 45
          }
        ]
      },
      {
        id: 'non-chronological-report',
        name: 'Non-Chronological Report',
        description: 'Fact-based report writing using headings and formal structure',
        icon: '📄',
        progress: 0,
        atoms: [
          {
            id: 'english-y4-non-chronological-report',
            moduleId: 'non-chronological-report',
            name: 'Year 4 Non-Chronological Report Writing',
            level: 1,
            status: 'developing',
            summary: 'Organise facts into clear report sections with headings and topic sentences.',
            videoUrl: 'https://www.youtube.com/embed/3tQjzSgL3cQ',
            teachingNotes: 'Teach report features: title, introduction, subheadings, grouped facts, and conclusion. Emphasise formal tone and precise vocabulary. Use model texts and annotation before writing.',
            commonMistakes: [
              'Writing in story style instead of report style',
              'Missing subheadings and paragraph grouping',
              'Including opinions instead of facts',
              'Poor sentence linking between sections'
            ],
            prerequisites: ['Year 4 Grammar Foundations', 'Year 4 Comprehension fluency'],
            teachingStrategies: [
              'Practice: identify report features from sample texts',
              'Practice: sort facts into matching subheadings',
              'Challenge: write a full mini-report from a fact bank',
              'Challenge: edit for formal tone and punctuation accuracy',
              'Exam technique: structure report answers with title, intro, subheadings, and grouped facts'
            ],
            assessmentCriteria: 'Student writes a structured non-chronological report with accurate factual grouping and clear headings.',
            estimatedMinutes: 45
          }
        ]
      }
    ]
  },
  {
    id: 'verbal-reasoning',
    name: 'Verbal Reasoning',
    icon: '🗣️',
    description: 'Language-based logic, word patterns, and reasoning skills',
    modules: [
      {
        id: 'verbal-reasoning',
        name: 'Verbal Reasoning',
        description: 'Build logic with words, patterns, and language clues.',
        icon: '🗣️',
        progress: 0,
        atoms: [
          {
            id: 'verbal-reasoning-level-1',
            moduleId: 'verbal-reasoning',
            name: 'Verbal Reasoning Foundations',
            level: 1,
            status: 'developing',
            summary: 'Alphabet positions, letter shifts, and simple word logic patterns.',
            videoUrl: 'https://www.youtube.com/embed/KD38vC6-dCM',
            teachingNotes: 'Teach A=1 to Z=26 fluency first. Then build letter-shift confidence (for example, 2 letters after C is E). Keep a clear method: identify the rule, test it on earlier items, then apply once to the missing term.',
            commonMistakes: [
              'Losing track of alphabet positions in the middle of a sequence',
              'Applying a different rule at each step instead of one consistent rule',
              'Forgetting to wrap around from Z back to A',
              'Rushing and choosing an answer before checking the full pattern'
            ],
            prerequisites: ['Confident alphabet order (A-Z)', 'Basic pattern recognition'],
            teachingStrategies: [
              'Use an alphabet strip for early drills, then remove support gradually',
              'Highlight step size in patterns (+1, +2, -1, alternating)',
              'Model think-aloud reasoning before independent questions',
              'Use timed mini-sets to build speed and accuracy'
            ],
            assessmentCriteria: 'Student solves letter-position and simple letter-sequence questions with at least 80% accuracy.',
            estimatedMinutes: 35
          },
          {
            id: 'verbal-reasoning-level-2',
            moduleId: 'verbal-reasoning',
            name: 'Advanced Verbal Reasoning',
            level: 2,
            status: 'weak',
            summary: 'Mixed verbal codes, analogies, and multi-step reasoning under time pressure.',
            videoUrl: 'https://www.youtube.com/embed/3G3N3xw1vW0',
            teachingNotes: 'Move from single-step rules to mixed-step items. Encourage students to annotate quickly: mark known rule parts, eliminate impossible options, then confirm with reverse-checking. Emphasise time management and accuracy balance.',
            commonMistakes: [
              'Missing one step in multi-step code questions',
              'Choosing a plausible option without verifying all parts of the rule',
              'Confusing analogy direction (A:B is like C:?)',
              'Spending too long on one difficult question and losing time overall'
            ],
            prerequisites: ['Verbal Reasoning Foundations'],
            teachingStrategies: [
              'Use elimination first: remove clearly invalid options quickly',
              'Split complex questions into mini-steps and solve systematically',
              'Practice with mixed question sets and timed checkpoints',
              'Review errors by category (sequence, code, analogy) to target weaknesses'
            ],
            assessmentCriteria: 'Student answers mixed verbal reasoning questions with clear working and at least 75% accuracy in timed practice.',
            estimatedMinutes: 40
          },
          {
            id: 'verbal-reasoning-cem-vocab-codes',
            moduleId: 'verbal-reasoning',
            name: 'CEM Verbal: Vocabulary and Codes',
            level: 3,
            status: 'weak',
            summary: 'CEM-style synonym/antonym speed, letter-number codes, and hidden rules.',
            videoUrl: 'https://www.youtube.com/embed/6nqH6iM14sM',
            teachingNotes: 'Train students to switch quickly between vocabulary meaning and code rules. Use short bursts with strict timing to build CEM-style pace. Prioritise elimination and rule-checking before committing an answer.',
            commonMistakes: [
              'Using first-impression answers without checking all code steps',
              'Confusing similar-meaning words in synonym/antonym sets',
              'Spending too long decoding one difficult item',
              'Not spotting repeated rule structures across questions'
            ],
            prerequisites: ['Advanced Verbal Reasoning'],
            teachingStrategies: [
              'Practice: 12-question mini sets split by vocabulary and code items',
              'Practice: elimination-first method for close options',
              'Challenge: timed mixed verbal rounds with 30-45 seconds per question',
              'Challenge: error log by type (vocabulary, code, analogy)'
            ],
            assessmentCriteria: 'Student completes CEM-style mixed verbal sets with 75%+ accuracy while maintaining exam pace.',
            estimatedMinutes: 40
          },
          {
            id: 'verbal-reasoning-cem-sequences-analogies',
            moduleId: 'verbal-reasoning',
            name: 'CEM Verbal: Sequences and Analogies',
            level: 4,
            status: 'weak',
            summary: 'Solve multi-step sequences and analogy links under strict time pressure.',
            videoUrl: 'https://www.youtube.com/embed/3G3N3xw1vW0',
            teachingNotes: 'Teach a fixed routine: identify relationship type, test with first pair, apply to second pair, and verify. Emphasise speed with accuracy by skipping and returning to heavy items.',
            commonMistakes: [
              'Mixing up analogy direction (A:B :: C:?)',
              'Assuming one-step patterns in multi-step sequences',
              'Ignoring positional clues in letter/number patterns',
              'Not returning to flagged questions'
            ],
            prerequisites: ['CEM Verbal: Vocabulary and Codes'],
            teachingStrategies: [
              'Practice: analogy banks grouped by relationship type',
              'Practice: sequence drills with alternating and mirrored patterns',
              'Challenge: 15-minute CEM verbal sprint papers',
              'Challenge: post-test review focused on process errors'
            ],
            assessmentCriteria: 'Student solves CEM sequence and analogy items with method clarity and 75%+ timed accuracy.',
            estimatedMinutes: 45
          }
        ]
      }
    ]
  },
  {
    id: 'non-verbal-reasoning',
    name: 'Non Verbal Reasoning',
    icon: '🧩',
    description: 'Visual pattern, spatial logic, and abstract reasoning skills',
    modules: [
      {
        id: 'non-verbal-reasoning',
        name: 'Non Verbal Reasoning',
        description: 'Develop visual pattern and spatial reasoning skills.',
        icon: '🧩',
        progress: 0,
        atoms: [
          {
            id: 'nvr-cem-pattern-matrices',
            moduleId: 'non-verbal-reasoning',
            name: 'CEM NVR: Pattern Matrices',
            level: 1,
            status: 'developing',
            summary: 'Identify shape, number, and position rules in matrix-style questions.',
            videoUrl: 'https://www.youtube.com/embed/qn2F6z4Lw7Q',
            teachingNotes: 'Start with single-rule matrices, then move to dual-rule and three-rule grids. Teach students to scan across rows and down columns before checking options.',
            commonMistakes: [
              'Checking only one direction (row or column) in a matrix',
              'Missing multiple simultaneous rules',
              'Choosing visually similar options without rule confirmation',
              'Rushing and ignoring transformation consistency'
            ],
            prerequisites: ['Basic shape vocabulary', 'Pattern recognition'],
            teachingStrategies: [
              'Practice: one-rule then two-rule matrix progression',
              'Practice: verbalise rule before selecting option',
              'Challenge: mixed CEM matrix sets with strict timing',
              'Challenge: identify whether change is shape, count, rotation, or shading'
            ],
            assessmentCriteria: 'Student solves NVR matrix questions with at least 80% accuracy in untimed sets and 70% in timed sets.',
            estimatedMinutes: 40
          },
          {
            id: 'nvr-cem-rotations-reflections',
            moduleId: 'non-verbal-reasoning',
            name: 'CEM NVR: Rotations and Reflections',
            level: 2,
            status: 'weak',
            summary: 'Track movement, rotation, and mirror transformations accurately.',
            videoUrl: 'https://www.youtube.com/embed/u4X2s3nYg4A',
            teachingNotes: 'Use tracing and arrow markers initially, then remove scaffolds. Reinforce clockwise vs anti-clockwise changes and vertical vs horizontal reflection.',
            commonMistakes: [
              'Confusing rotation with reflection',
              'Applying the wrong rotation direction',
              'Ignoring internal marks inside shapes',
              'Losing orientation in multi-step transformations'
            ],
            prerequisites: ['CEM NVR: Pattern Matrices'],
            teachingStrategies: [
              'Practice: card rotation drills at 90/180/270 degrees',
              'Practice: mirror-line exercises using folded paper',
              'Challenge: two-step transformation questions under time pressure',
              'Challenge: option elimination using impossible orientation checks'
            ],
            assessmentCriteria: 'Student distinguishes and applies rotation/reflection rules with at least 75% timed accuracy.',
            estimatedMinutes: 40
          },
          {
            id: 'nvr-cem-odd-one-out',
            moduleId: 'non-verbal-reasoning',
            name: 'CEM NVR: Odd One Out and Classification',
            level: 3,
            status: 'weak',
            summary: 'Classify shapes by shared properties and detect the non-matching figure quickly.',
            videoUrl: 'https://www.youtube.com/embed/qn2F6z4Lw7Q',
            teachingNotes: 'Teach quick property scanning: number of sides, symmetry, orientation, shading, and internal symbols. Encourage students to group first, then isolate the outlier.',
            commonMistakes: [
              'Focusing on one feature and missing stronger rules',
              'Choosing the most complex shape as odd one out by default',
              'Ignoring symmetry cues',
              'Not checking all options against the same rule'
            ],
            prerequisites: ['CEM NVR: Pattern Matrices'],
            teachingStrategies: [
              'Practice: classify by one feature, then mixed features',
              'Practice: timed odd-one-out drills with reasoning explanation',
              'Challenge: dual-criteria classification sets',
              'Challenge: speed rounds (20 questions, 10 minutes)'
            ],
            assessmentCriteria: 'Student identifies odd-one-out/classification rules consistently with 75%+ timed accuracy.',
            estimatedMinutes: 35
          },
          {
            id: 'nvr-cem-3d-nets',
            moduleId: 'non-verbal-reasoning',
            name: 'CEM NVR: 3D Nets and Spatial Reasoning',
            level: 4,
            status: 'weak',
            summary: 'Visualise 2D nets, cube movement, and 3D matching patterns.',
            videoUrl: 'https://www.youtube.com/embed/4A8h5x6s4nY',
            teachingNotes: 'Use physical cube nets first to build mental rotation skill. Train students to track adjacent faces and opposite faces systematically before checking choices.',
            commonMistakes: [
              'Misidentifying opposite faces in cube questions',
              'Over-relying on one visible face',
              'Failing to track edge adjacency in nets',
              'Guessing without fold-logic checks'
            ],
            prerequisites: ['CEM NVR: Rotations and Reflections'],
            teachingStrategies: [
              'Practice: paper-net folding activities',
              'Practice: opposite-face memory patterns for cubes',
              'Challenge: mixed 3D spatial sets under CEM-like timing',
              'Challenge: explain fold path before selecting answer'
            ],
            assessmentCriteria: 'Student answers net and spatial NVR questions with clear method and at least 70-75% timed accuracy.',
            estimatedMinutes: 45
          }
        ]
      }
    ]
  },
  {
    id: 'science',
    name: 'Science',
    icon: '🔬',
    description: 'Biology, chemistry, physics, and scientific method',
    modules: [
      {
        id: 'biology',
        name: 'Biology',
        description: 'Living organisms and life processes',
        icon: '🌱',
        progress: 0,
        atoms: []
      },
      {
        id: 'physics',
        name: 'Physics',
        description: 'Forces, energy, and matter',
        icon: '⚡',
        progress: 0,
        atoms: []
      }
    ]
  },
  {
    id: 'computers',
    name: 'Computers',
    icon: '💻',
    description: 'Programming, digital literacy, and computational thinking',
    modules: [
      {
        id: 'intro-computing',
        name: 'Introduction to Computing',
        description: 'Computer basics, file management, online safety, and spreadsheets',
        icon: '🖥️',
        progress: 0,
        atoms: [
          {
            id: 'intro-it-safety',
            moduleId: 'intro-computing',
            name: 'Computer Basics & Online Safety',
            level: 1,
            status: 'weak',
            summary: 'Learn file management, internet safety, and digital citizenship',
            videoUrl: 'https://www.youtube.com/embed/gcbMKt079l0',
            teachingNotes: 'Teach students how to navigate file systems, create organized folder structures, and save work appropriately. Focus on practical demonstrations of productivity tools. Emphasize real-world examples of online threats and digital footprint.',
            commonMistakes: [
              'Saving files in wrong locations',
              'Not organizing files with clear naming conventions',
              'Falling for phishing attempts',
              'Sharing personal information online',
              'Not understanding privacy settings'
            ],
            prerequisites: ['Basic computer literacy', 'Ability to use mouse and keyboard'],
            teachingStrategies: [
              'Hands-on practice with file management',
              'Show real examples of phishing emails and fake news',
              'Interactive discussions about online safety scenarios',
              'Teach SMART rules for internet safety',
              'Demonstrate password security best practices',
              'Reference: CGP KS2 Computing Study Book (Online Safety and Digital Literacy units)',
              'Online: UK Safer Internet Centre advice hub (saferinternet.org.uk/advice-centre/young-people)',
              'Quick note: Stop-Think-Check before clicking links or sharing any personal information'
            ],
            assessmentCriteria: 'Student can create organized folder structures, identify phishing attempts, distinguish between real and fake news, and demonstrate safe online behavior.',
            estimatedMinutes: 45
          },
          {
            id: 'spreadsheets-basics',
            moduleId: 'intro-computing',
            name: 'Spreadsheet Modeling',
            level: 2,
            status: 'weak',
            summary: 'Master formulas, functions, and data presentation',
            videoUrl: 'https://www.youtube.com/embed/upcIRjyGzWQ',
            teachingNotes: 'Start with basic cell referencing before moving to formulas. Build up from simple calculations (SUM) to complex functions (MAX, MIN, AVERAGE, COUNT, IF). Use real-world examples like grade calculators or budget planners.',
            commonMistakes: [
              'Confusing cell references (A1 vs $A$1)',
              'Incorrect formula syntax',
              'Forgetting to format cells appropriately',
              'Not using cell ranges efficiently',
              'Circular reference errors'
            ],
            prerequisites: ['Computer Basics & Online Safety'],
            teachingStrategies: [
              'Visual cell referencing demonstrations',
              'Practice with grade calculators and budgets',
              'Step-by-step formula building',
              'Visual formatting for data presentation',
              'Chart creation for data visualization',
              'Reference: Brilliant Activities for Computing by Miles Berry (spreadsheet classroom tasks)',
              'Online: Microsoft Excel and Google Sheets beginner guides (support.microsoft.com / support.google.com/docs)',
              'Quick note: Teach formula flow as Input -> Process -> Output and always test with sample values'
            ],
            assessmentCriteria: 'Student can create formulas, use functions (SUM, MAX, MIN, AVERAGE, COUNT, IF), format spreadsheets professionally, and create basic charts.',
            estimatedMinutes: 50
          }
        ]
      },
      {
        id: 'intro-programming',
        name: 'Introduction to Programming',
        description: 'Programming fundamentals using visual programming languages',
        icon: '🎮',
        progress: 0,
        atoms: [
          {
            id: 'scratch-programming',
            moduleId: 'intro-programming',
            name: 'Scratch Programming Fundamentals',
            level: 1,
            status: 'weak',
            summary: 'Learn sequence, selection, iteration, and variables using Scratch',
            videoUrl: 'https://www.youtube.com/embed/jXUZaf5D12A',
            teachingNotes: 'Introduce programming concepts through game creation. Start with simple sprite movements, then add conditionals, loops, and finally variables for scoring. Let students be creative with their projects. Emphasize decomposition and abstraction.',
            commonMistakes: [
              'Not understanding the difference between sequence and selection',
              'Infinite loops without stop conditions',
              'Incorrect variable scoping',
              'Forgetting to reset variables at game start',
              'Not using broadcast messages effectively'
            ],
            prerequisites: ['Spreadsheet Modeling'],
            teachingStrategies: [
              'Start with simple sprite animations',
              'Build up to interactive games with keyboard controls',
              'Use variables to track score and lives',
              'Peer code review and sharing projects',
              'Decompose complex problems into smaller tasks',
              'Reference: Hello Ruby: Adventures in Coding by Linda Liukas (parent-supported reading)',
              'Online: Scratch Ideas + Tutorials (scratch.mit.edu/ideas and scratch.mit.edu/projects/editor/?tutorial=getStarted)',
              'Quick note: Sequence -> Selection -> Iteration -> Variables is the best Year 4/5 progression order'
            ],
            assessmentCriteria: 'Student creates a working game using sequence, selection, iteration, and variables with at least 90% functionality and demonstrates understanding of programming concepts.',
            estimatedMinutes: 60
          },
          {
            id: 'block-programming',
            moduleId: 'intro-programming',
            name: 'Block-Based Programming Projects',
            level: 2,
            status: 'weak',
            summary: 'Create complex projects with custom blocks and advanced features',
            videoUrl: 'https://www.youtube.com/embed/jXUZaf5D12A',
            teachingNotes: 'Build on Scratch fundamentals by creating custom blocks (functions). Teach students to break down complex problems using decomposition. Focus on creating reusable code and debugging strategies.',
            commonMistakes: [
              'Not creating reusable custom blocks',
              'Overly complex sprite interactions',
              'Poor project organization',
              'Not testing incrementally'
            ],
            prerequisites: ['Scratch Programming Fundamentals'],
            teachingStrategies: [
              'Create custom blocks for repeated code',
              'Build multi-level games with state management',
              'Use lists for data management',
              'Systematic debugging approach',
              'Reference: DK Help Your Kids with Computer Coding (visual, beginner-friendly projects)',
              'Online: Raspberry Pi Projects - Scratch and beginner game projects (projects.raspberrypi.org/en/pathways/scratch-intro)',
              'Quick note: Encourage plan-build-test-refactor cycle every 10-15 minutes during project work'
            ],
            assessmentCriteria: 'Student creates a complex project using custom blocks, lists, and demonstrates proper decomposition and debugging skills.',
            estimatedMinutes: 60
          }
        ]
      },
      {
        id: 'binary-number-system',
        name: 'Binary Number System',
        description: 'Understanding binary, hexadecimal, and number conversions',
        icon: '🔢',
        progress: 0,
        atoms: [
          {
            id: 'binary-systems',
            moduleId: 'binary-number-system',
            name: 'Binary Number Systems',
            level: 1,
            status: 'weak',
            summary: 'Convert between denary, binary, and hexadecimal',
            videoUrl: 'https://www.youtube.com/embed/1-YMkNd3Fx0',
            teachingNotes: 'Year 7 Explanation:\n\nComputers store data using switches: ON (1) and OFF (0). This is binary.\n\nImportant words:\n- bit = one 0/1\n- nibble = 4 bits\n- byte = 8 bits\n- denary = normal base-10 numbers\n- hexadecimal = base-16 numbers (0-9, A-F)\n\nBinary place values (8-bit):\n128  64  32  16  8  4  2  1\n\nTo convert binary -> denary:\nAdd the place values where the bit is 1.\nExample: 01001101 = 64 + 8 + 4 + 1 = 77\n\nTo convert denary -> binary:\nCheck each place value from left to right and put 1 if it fits, else 0.\nExample: 56 = 00111000\n\nTo convert binary -> hex:\nSplit into nibbles (groups of 4 bits), then convert each nibble.\nExample: 01001101 -> 0100 1101 -> 4D\n\nTip: Learn A=10 to F=15 by heart. It makes hex conversion much faster.',
            commonMistakes: [
              'Confusing place values in binary',
              'Arithmetic errors when adding binary numbers',
              'Not understanding why hex is used',
              'Overflow errors when adding 8-bit numbers',
              'Incorrectly converting negative numbers'
            ],
            prerequisites: ['Introduction to Programming'],
            teachingStrategies: [
              'Place value charts for conversions',
              'Binary addition practice with visual aids',
              'Real-world examples (IP addresses, colors in hex)',
              'Interactive binary games and puzzles',
              'Use binary cards for hands-on learning',
              'Reference: BBC Bitesize Computing - Binary and data topics',
              'Online: CS Unplugged binary activities (csunplugged.org)',
              'Quick note: Binary confidence grows fastest with daily 5-minute conversion drills'
            ],
            assessmentCriteria: 'Student converts numbers between bases accurately and adds three 8-bit binary numbers with understanding of overflow.',
            estimatedMinutes: 45
          },
          {
            id: 'binary-hex-conversions-addition',
            moduleId: 'binary-number-system',
            name: 'Binary and Hexadecimal Conversions + Binary Addition',
            level: 2,
            status: 'weak',
            summary: 'Master denary-binary-hex conversions, nibbles, place value, and binary carry addition.',
            videoUrl: 'https://www.youtube.com/embed/1-YMkNd3Fx0',
            teachingNotes: 'Year 7 Explanation:\n\nComputers only understand ON and OFF. We write ON as 1 and OFF as 0. That is binary.\n\nKey words:\n- bit = one binary digit (0 or 1)\n- nibble = 4 bits\n- byte = 8 bits\n- denary = normal base-10 numbers\n- hexadecimal (hex) = base-16 using 0-9 and A-F\n\nHex values to remember:\nA=10, B=11, C=12, D=13, E=14, F=15\n\nBinary place value (8-bit):\n128  64  32  16  8  4  2  1\n\nExample 1: Binary to denary\n01001101\n= 64 + 8 + 4 + 1\n= 77\n\nExample 2: Denary to binary (56)\nCheck each place value from left to right:\n128 64 32 16 8 4 2 1\n 0  0  1  1 1 0 0 0\nSo 56 in binary is 00111000.\n\nExample 3: Binary to hex\nSplit into nibbles (groups of 4):\n01001101 -> 0100 1101\n0100 = 4\n1101 = 13 = D\nSo binary 01001101 = hex 4D.\n\nExample 4: Hex to binary\nF5 -> F and 5\nF = 1111\n5 = 0101\nSo F5 = 11110101.\n\nBinary addition rules:\n0 + 0 = 0\n0 + 1 = 1\n1 + 1 = 10 (write 0, carry 1)\n1 + 1 + 1 = 11 (write 1, carry 1)\n\nExample 5: Binary addition\n  0100\n+ 0101\n------\n  1001\nSo answer is 1001 (which is denary 9).\n\nAlways work right to left in binary addition and do not forget carries.',
            commonMistakes: [
              'Reading place values left-to-right instead of right-to-left in binary columns',
              'Forgetting to carry in binary addition (especially 1 + 1 and 1 + 1 + 1)',
              'Treating each hex digit as base-10 instead of base-16',
              'Not splitting binary into nibbles (4 bits) when converting to hex',
              'Writing denary-to-hex remainders in the wrong order'
            ],
            prerequisites: ['Binary Number Systems'],
            teachingStrategies: [
              'Use fixed conversion grids for every question (binary PV and hex PV headings)',
              'Practice denary->binary, binary->denary, binary->hex, and hex->binary in mixed sets',
              'Run short binary addition drills with explicit carry rows',
              'Teach alternative conversion methods (nibble grouping and repeated ÷16) and compare',
              'Reference: BBC Bitesize + CGP Computer Science conversion practice pages',
              'Online: CS Unplugged binary cards and conversion worksheets',
              'Quick note: For hex, remember A=10, B=11, C=12, D=13, E=14, F=15'
            ],
            assessmentCriteria: 'Student converts accurately between denary, binary, and hexadecimal and completes binary addition with correct carry handling in at least 80% of questions.',
            estimatedMinutes: 50
          },
          {
            id: 'binary-shifts',
            moduleId: 'binary-number-system',
            name: 'Binary Shifts and Two\'s Complement',
            level: 3,
            status: 'weak',
            summary: 'Binary shifts, multiplication/division, and negative numbers',
            videoUrl: 'https://www.youtube.com/embed/1-YMkNd3Fx0',
            teachingNotes: 'Explain how left and right shifts multiply/divide by powers of 2. Teach two\'s complement for representing negative numbers. Show practical applications in computer operations.',
            commonMistakes: [
              'Not understanding overflow in shifts',
              'Errors in two\'s complement conversion',
              'Confusing arithmetic and logical shifts',
              'Sign bit errors'
            ],
            prerequisites: ['Binary and Hexadecimal Conversions + Binary Addition'],
            teachingStrategies: [
              'Visual demonstrations of bit shifting',
              'Practice two\'s complement systematically',
              'Real-world applications in computer graphics',
              'Compare with calculator results',
              'Reference: OCR/GCSE style Binary and Logic revision workbooks (age-appropriate sections)',
              'Online: Khan Academy and YouTube binary shift walkthroughs',
              'Quick note: Left shift x2 and right shift ÷2 only works reliably within bit-length limits'
            ],
            assessmentCriteria: 'Student performs binary shifts correctly and represents negative numbers using two\'s complement accurately.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'boolean-logic',
        name: 'Boolean Logic',
        description: 'Logic gates, truth tables, and digital circuits',
        icon: '⚡',
        progress: 0,
        atoms: [
          {
            id: 'logic-gates',
            moduleId: 'boolean-logic',
            name: 'Logic Gates & Truth Tables',
            level: 1,
            status: 'weak',
            summary: 'AND, OR, NOT, XOR gates and truth table construction',
            videoUrl: 'https://www.youtube.com/embed/gI-qXk7XojA',
            teachingNotes: 'Start with simple AND/OR/NOT gates. Build truth tables systematically. Show real circuit applications (burglar alarms, automatic lights). Explain XOR behavior with practical examples.',
            commonMistakes: [
              'Confusing AND with OR logic',
              'Incorrectly filling truth tables',
              'Not understanding XOR gate behavior',
              'Missing rows in truth tables'
            ],
            prerequisites: ['Binary Number System'],
            teachingStrategies: [
              'Truth table practice with real scenarios',
              'Logic gate symbols memorization',
              'Physical switches demonstration',
              'Interactive logic simulators',
              'Reference: Hello World: Computer Science for Kids (logic chapter)',
              'Online: Logicly / CircuitVerse simulators (interactive gate experiments)',
              'Quick note: Build confidence by writing truth tables before drawing full circuits'
            ],
            assessmentCriteria: 'Student completes truth tables accurately for all basic gates and identifies gates from truth tables.',
            estimatedMinutes: 45
          },
          {
            id: 'circuit-design',
            moduleId: 'boolean-logic',
            name: 'Logic Circuit Design',
            level: 2,
            status: 'weak',
            summary: 'Design and simplify logic circuits for real-world problems',
            videoUrl: 'https://www.youtube.com/embed/gI-qXk7XojA',
            teachingNotes: 'Let students design their own logic circuits for specific requirements. Teach Boolean algebra basics for circuit simplification. Use online simulators for testing.',
            commonMistakes: [
              'Overly complex circuit designs for simple problems',
              'Incorrect gate combinations',
              'Not simplifying circuits',
              'Wiring errors in simulators'
            ],
            prerequisites: ['Logic Gates & Truth Tables'],
            teachingStrategies: [
              'Design challenges with specific requirements',
              'Logic circuit simulators online',
              'Boolean algebra simplification',
              'Peer review of circuit designs',
              'Reference: CGP GCSE Computer Science revision guide (logic circuit design sections)',
              'Online: CircuitVerse challenge library (circuitverse.org/explore)',
              'Quick note: Start with required output condition, then work backward to choose gates'
            ],
            assessmentCriteria: 'Student designs logic circuits for real-world problems with 85% correctness and demonstrates basic simplification.',
            estimatedMinutes: 50
          }
        ]
      },
      {
        id: 'python-programming',
        name: 'Python Programming',
        description: 'Text-based programming with Python',
        icon: '🐍',
        progress: 0,
        atoms: [
          {
            id: 'python-with-karel',
            moduleId: 'python-programming',
            name: 'Introduction to Python with Karel',
            level: 0,
            status: 'weak',
            summary: 'Meet Karel the robot and learn your very first Python commands — move, turn, and place balls!',
            videoUrl: 'https://www.youtube.com/embed/rfscVS0vtbw',
            notesTopicId: 'python-with-karel',
            teachingNotes: 'Karel is a visual, robot-based environment that removes syntax anxiety. Students command a robot on a grid before writing real Python. Great for absolute beginners aged 8–12.',
            commonMistakes: [
              'Forgetting brackets on commands: move() not move',
              'Confusing turn_left() with turn_right() (Karel only has turn_left built in)',
              'Not thinking about which direction Karel is facing before moving'
            ],
            prerequisites: [],
            teachingStrategies: [
              'Act out Karel moves physically in the classroom first',
              'Draw the grid on paper and trace the path before coding',
              'Reference: Stanford CS106A – Karel the Robot Learns Java (adapted concepts)',
              'Online: code.org Karel lessons and CS Education for Kids',
              'Quick note: Ask "which way is Karel facing?" before every command'
            ],
            assessmentCriteria: 'Student can write a simple Karel program that moves, turns, and places a ball using basic commands.',
            estimatedMinutes: 30
          },
          {
            id: 'python-basics',
            moduleId: 'python-programming',
            name: 'Python Fundamentals',
            level: 1,
            status: 'weak',
            summary: 'Variables, data types, input/output, and basic operations',
            videoUrl: 'https://www.youtube.com/embed/rfscVS0vtbw',
            teachingNotes: 'Start with simple print statements and progress to variables and input. Emphasize proper naming conventions and code readability. Use IDLE or simple Python editors.',
            commonMistakes: [
              'Indentation errors',
              'Syntax errors (missing colons, quotes)',
              'Type conversion errors',
              'Variable naming issues'
            ],
            prerequisites: ['Boolean Logic'],
            teachingStrategies: [
              'Live coding demonstrations',
              'Simple calculator programs',
              'Input validation exercises',
              'Error message interpretation practice',
              'Reference: Python for Kids by Jason R. Briggs (beginner-friendly fundamentals)',
              'Online: Replit Python basics and Python docs tutorial (docs.python.org/3/tutorial)',
              'Quick note: Read error line numbers first, then fix one issue at a time'
            ],
            assessmentCriteria: 'Student writes simple Python programs with correct syntax, proper variable usage, and handles input/output.',
            estimatedMinutes: 50
          },
          {
            id: 'python-control',
            moduleId: 'python-programming',
            name: 'Control Structures in Python',
            level: 2,
            status: 'weak',
            summary: 'If statements, loops (for, while), and logical operators',
            videoUrl: 'https://www.youtube.com/embed/rfscVS0vtbw',
            teachingNotes: 'Teach if-elif-else systematically. Practice for loops with range. Introduce while loops with clear exit conditions. Use flowcharts to visualize logic.',
            commonMistakes: [
              'Incorrect indentation in nested structures',
              'Infinite loops without break conditions',
              'Off-by-one errors in ranges',
              'Logical operator confusion (and vs or)'
            ],
            prerequisites: ['Python Fundamentals'],
            teachingStrategies: [
              'Flowchart-to-code translation',
              'Number guessing games',
              'Pattern printing with loops',
              'Debugging practice with intentional errors',
              'Reference: Invent Your Own Computer Games with Python by Al Sweigart (control flow chapters)',
              'Online: W3Schools Python conditions and loops',
              'Quick note: If logic is wrong, trace with sample inputs before rewriting entire code'
            ],
            assessmentCriteria: 'Student writes programs using if-elif-else, for loops, and while loops with proper logic and indentation.',
            estimatedMinutes: 60
          },
          {
            id: 'python-functions',
            moduleId: 'python-programming',
            name: 'Functions and Modular Programming',
            level: 3,
            status: 'weak',
            summary: 'Define functions, parameters, return values, and code organization',
            videoUrl: 'https://www.youtube.com/embed/rfscVS0vtbw',
            teachingNotes: 'Emphasize code reuse and modular design. Teach function definition, parameters, and return values. Use RUCSAC for problem-solving. Practice debugging systematically.',
            commonMistakes: [
              'Not understanding function parameters',
              'Confusion between print and return',
              'Variable scope issues',
              'Not breaking down problems into functions'
            ],
            prerequisites: ['Control Structures in Python'],
            teachingStrategies: [
              'RUCSAC problem-solving framework',
              'Modular design with functions',
              'Code review and refactoring exercises',
              'Unit testing basics',
              'Reference: Python Crash Course (functions chapter, simplified tasks for Year 5 transition)',
              'Online: Real Python function basics and beginner examples',
              'Quick note: Use small single-purpose functions and clear names to reduce bugs'
            ],
            assessmentCriteria: 'Student writes Python programs using functions with parameters and return values, demonstrating proper debugging practices.',
            estimatedMinutes: 60
          },
          {
            id: 'python-data-structures',
            moduleId: 'python-programming',
            name: 'Lists and Data Structures',
            level: 4,
            status: 'weak',
            summary: 'Lists, tuples, dictionaries, and data manipulation',
            videoUrl: 'https://www.youtube.com/embed/rfscVS0vtbw',
            teachingNotes: 'Introduce lists for storing multiple values. Teach list methods (append, remove, sort). Progress to dictionaries for key-value storage. Use real-world data examples.',
            commonMistakes: [
              'Index out of range errors',
              'Modifying lists during iteration',
              'Confusing list methods',
              'Dictionary key errors'
            ],
            prerequisites: ['Functions and Modular Programming'],
            teachingStrategies: [
              'Shopping list programs',
              'Student database projects',
              'List comprehensions for advanced students',
              'File reading into lists',
              'Reference: Coding Projects in Python by DK (lists/dictionaries project sections)',
              'Online: Programiz Python lists and dictionaries tutorials',
              'Quick note: Prefer stepwise list operations first; introduce comprehensions only after mastery'
            ],
            assessmentCriteria: 'Student manipulates lists and dictionaries effectively and creates programs that store and process data.',
            estimatedMinutes: 60
          }
        ]
      },
      {
        id: 'hardware-software-data',
        name: 'Hardware, Software and Data Representation',
        description: 'Computer architecture, storage, and how data is represented',
        icon: '🔧',
        progress: 0,
        atoms: [
          {
            id: 'computer-architecture',
            moduleId: 'hardware-software-data',
            name: 'Computer Architecture & CPU',
            level: 1,
            status: 'weak',
            summary: 'CPU components, Fetch-Decode-Execute cycle, and Von Neumann architecture',
            videoUrl: 'https://www.youtube.com/embed/Z5JC9Ve1sfI',
            teachingNotes: 'Explain the FDE cycle with visual diagrams. Identify CPU components (ALU, CU, registers, cache). Show how CPU, RAM, and storage work together. Use animations to demonstrate the cycle.',
            commonMistakes: [
              'Confusing RAM and storage',
              'Not understanding CPU components (ALU, CU, registers)',
              'FDE cycle order errors',
              'Cache vs RAM confusion'
            ],
            prerequisites: ['Python Programming'],
            teachingStrategies: [
              'FDE cycle animations and diagrams',
              'Component identification quizzes',
              'CPU simulation activities',
              'Compare different processor specifications',
              'Reference: BBC Bitesize Computer Systems (CPU and architecture units)',
              'Online: CrashCourse Computer Science episodes on CPU basics',
              'Quick note: Anchor every lesson to Fetch -> Decode -> Execute sequence for retention'
            ],
            assessmentCriteria: 'Student explains FDE cycle accurately, identifies CPU components, and understands Von Neumann architecture.',
            estimatedMinutes: 45
          },
          {
            id: 'memory-storage',
            moduleId: 'hardware-software-data',
            name: 'Memory and Storage',
            level: 2,
            status: 'weak',
            summary: 'RAM, ROM, storage types, and capacity calculations',
            videoUrl: 'https://www.youtube.com/embed/Z5JC9Ve1sfI',
            teachingNotes: 'Distinguish between primary (RAM, ROM, cache) and secondary storage (HDD, SSD, optical, cloud). Teach capacity units (KB, MB, GB, TB). Calculate file sizes and storage requirements.',
            commonMistakes: [
              'Confusing volatile and non-volatile memory',
              'Unit conversion errors',
              'Not understanding storage hierarchy',
              'SSD vs HDD confusion'
            ],
            prerequisites: ['Computer Architecture & CPU'],
            teachingStrategies: [
              'Storage comparison tables',
              'Hands-on with different storage devices',
              'Capacity calculation practice',
              'Real-world storage scenarios',
              'Reference: CGP Computer Science revision sections on memory and storage',
              'Online: Techquickie style explainers on HDD vs SSD and memory hierarchy',
              'Quick note: Keep unit ladders visible (KB, MB, GB, TB) during every calculation task'
            ],
            assessmentCriteria: 'Student distinguishes memory types, converts capacity units correctly, and selects appropriate storage for scenarios.',
            estimatedMinutes: 40
          },
          {
            id: 'data-representation',
            moduleId: 'hardware-software-data',
            name: 'Data Representation',
            level: 3,
            status: 'weak',
            summary: 'How images, sound, and text are stored as binary',
            videoUrl: 'https://www.youtube.com/embed/Z5JC9Ve1sfI',
            teachingNotes: 'Demonstrate how images are represented using pixels and color depth. Explain sound sampling and bit depth. Show ASCII and Unicode for text. Calculate file sizes for different media.',
            commonMistakes: [
              'Unclear about how images are represented in binary',
              'File size calculation errors',
              'Not understanding sampling rate impact',
              'ASCII vs Unicode confusion'
            ],
            prerequisites: ['Memory and Storage'],
            teachingStrategies: [
              'Calculate file sizes for images and sound',
              'Pixel grid demonstrations',
              'Sampling rate comparisons (audio quality)',
              'Character encoding examples',
              'Reference: OCR/GCSE data representation workbook exercises',
              'Online: BBC Bitesize pages for image/audio/text representation',
              'Quick note: File size questions are easiest when students write formula before substituting values'
            ],
            assessmentCriteria: 'Student calculates file sizes for images and sound, explains sampling and color depth, and understands text encoding.',
            estimatedMinutes: 50
          },
          {
            id: 'input-output',
            moduleId: 'hardware-software-data',
            name: 'Input and Output Devices',
            level: 4,
            status: 'weak',
            summary: 'Input/output devices and their applications',
            videoUrl: 'https://www.youtube.com/embed/Z5JC9Ve1sfI',
            teachingNotes: 'Classify devices as input, output, or storage. Discuss appropriate devices for different scenarios (accessibility, gaming, design). Understand sensors and actuators.',
            commonMistakes: [
              'Confusion between input and output devices',
              'Not considering accessibility needs',
              'Touchscreen classification confusion'
            ],
            prerequisites: ['Data Representation'],
            teachingStrategies: [
              'Device classification activities',
              'Scenario-based device selection',
              'Hands-on with various input/output devices',
              'Accessibility technology exploration',
              'Reference: KS2/KS3 Computing curriculum resource packs on hardware devices',
              'Online: AbilityNet accessibility and assistive technology guides',
              'Quick note: Always classify by function in context (input, output, storage, control)'
            ],
            assessmentCriteria: 'Student classifies devices correctly and selects appropriate devices for specific scenarios including accessibility.',
            estimatedMinutes: 40
          }
        ]
      },
      {
        id: 'databases',
        name: 'Databases',
        description: 'Database design, SQL queries, and data management',
        icon: '🗄️',
        progress: 0,
        atoms: [
          {
            id: 'db-basics',
            moduleId: 'databases',
            name: 'Database Fundamentals',
            level: 1,
            status: 'weak',
            summary: 'Tables, records, fields, primary keys, and simple query ideas',
            videoUrl: 'https://www.youtube.com/embed/HXV3zeQKqGY',
            teachingNotes: 'Introduce database language through everyday examples (library books, student lists). Clarify the difference between field names and field values. Use simple table diagrams before SQL syntax.',
            commonMistakes: [
              'Confusing a field with a record',
              'Not understanding why primary keys must be unique',
              'Mixing data types in one column',
              'Assuming spreadsheets and databases are identical'
            ],
            prerequisites: ['Spreadsheet Modeling'],
            teachingStrategies: [
              'Build toy databases with paper cards first',
              'Identify keys and duplicate values in examples',
              'Practice basic filtering and sorting tasks',
              'Reference: CGP GCSE Computer Science - Databases chapter',
              'Online: W3Schools SQL introduction',
              'Quick note: Table = entity, row = record, column = field'
            ],
            assessmentCriteria: 'Student identifies fields, records, and keys correctly and explains why primary keys are required.',
            estimatedMinutes: 45
          },
          {
            id: 'db-sql-queries',
            moduleId: 'databases',
            name: 'SQL Query Basics',
            level: 2,
            status: 'weak',
            summary: 'Use SELECT, WHERE, ORDER BY, and simple conditions to retrieve data',
            videoUrl: 'https://www.youtube.com/embed/HXV3zeQKqGY',
            teachingNotes: 'Teach query writing in small steps: choose columns, choose table, then filter conditions. Focus on reading query output and checking correctness.',
            commonMistakes: [
              'Missing WHERE conditions',
              'Using text values without quotes',
              'Confusing ascending and descending sort',
              'Selecting wrong columns'
            ],
            prerequisites: ['Database Fundamentals'],
            teachingStrategies: [
              'Use one-query-one-goal exercises',
              'Compare expected output with actual output',
              'Introduce AND/OR only after single-condition confidence',
              'Reference: SQL QuickStart style beginner guides',
              'Online: SQLBolt interactive lessons',
              'Quick note: Query plan = SELECT -> FROM -> WHERE -> ORDER BY'
            ],
            assessmentCriteria: 'Student writes simple SQL queries that return correct filtered and sorted outputs.',
            estimatedMinutes: 50
          }
        ]
      },
      {
        id: 'system-architecture',
        name: 'System Architecture',
        description: 'Operating systems, networks, and system design',
        icon: '🏗️',
        progress: 0,
        atoms: [
          {
            id: 'os-basics',
            moduleId: 'system-architecture',
            name: 'Operating System Basics',
            level: 1,
            status: 'weak',
            summary: 'Understand operating system roles: memory, files, process and user management',
            videoUrl: 'https://www.youtube.com/embed/26QPDBe-NB8',
            teachingNotes: 'Explain OS as the manager between user and hardware. Use concrete examples: app opening, file saving, switching tasks.',
            commonMistakes: [
              'Confusing OS with applications',
              'Not understanding multitasking',
              'Mixing up RAM and storage responsibilities',
              'Assuming files are managed by apps only'
            ],
            prerequisites: ['Computer Architecture & CPU'],
            teachingStrategies: [
              'Map user action to OS responsibility',
              'Demonstrate process/task switching live',
              'Use file-permission examples in school context',
              'Reference: BBC Bitesize - Operating systems',
              'Online: Khan Academy computer systems intro',
              'Quick note: OS handles resources, apps handle specific tasks'
            ],
            assessmentCriteria: 'Student explains core OS functions and distinguishes OS tasks from application tasks.',
            estimatedMinutes: 40
          },
          {
            id: 'network-basics',
            moduleId: 'system-architecture',
            name: 'Network Fundamentals',
            level: 2,
            status: 'weak',
            summary: 'LAN/WAN, routers, packets, and basic network performance factors',
            videoUrl: 'https://www.youtube.com/embed/26QPDBe-NB8',
            teachingNotes: 'Teach networks as connected devices exchanging packets. Introduce latency, bandwidth, and reliability using relatable examples (video call, gaming, downloads).',
            commonMistakes: [
              'Confusing internet with Wi-Fi',
              'Mixing up router and server roles',
              'Assuming faster bandwidth always means lower latency',
              'Not understanding packet transfer'
            ],
            prerequisites: ['Operating System Basics'],
            teachingStrategies: [
              'Draw packet journey diagrams',
              'Compare LAN and WAN scenarios',
              'Use simple performance troubleshooting cases',
              'Reference: CGP Computer Science networking sections',
              'Online: Cisco Networking Academy beginner resources',
              'Quick note: Bandwidth = amount, latency = delay'
            ],
            assessmentCriteria: 'Student describes network components and explains bandwidth/latency in practical situations.',
            estimatedMinutes: 45
          }
        ]
      },
      {
        id: 'internet-www',
        name: 'Internet and WWW',
        description: 'How the internet works, protocols, and web technologies',
        icon: '🌐',
        progress: 0,
        atoms: [
          {
            id: 'internet-protocols',
            moduleId: 'internet-www',
            name: 'Internet, IP and DNS',
            level: 1,
            status: 'weak',
            summary: 'Understand IP addresses, DNS lookup, and basic internet routing',
            videoUrl: 'https://www.youtube.com/embed/7_LPdttKXPc',
            teachingNotes: 'Use a postal-address analogy: domain names map to IP addresses through DNS. Keep protocol detail simple but accurate for Year 4/5 progression.',
            commonMistakes: [
              'Confusing URL and IP address',
              'Thinking DNS stores website content',
              'Not understanding why DNS lookup is needed',
              'Mixing browser and internet roles'
            ],
            prerequisites: ['Network Fundamentals'],
            teachingStrategies: [
              'Practice URL-to-IP concept mapping',
              'Walk through a simple DNS request flow',
              'Use role cards: browser, DNS server, web server',
              'Reference: BBC Bitesize internet basics',
              'Online: Cloudflare Learning Center - What is DNS',
              'Quick note: DNS translates names; IP identifies destination'
            ],
            assessmentCriteria: 'Student explains how a web request uses DNS and IP to reach a website.',
            estimatedMinutes: 40
          },
          {
            id: 'web-basics',
            moduleId: 'internet-www',
            name: 'Web Pages and HTTP Basics',
            level: 2,
            status: 'weak',
            summary: 'Difference between internet and WWW, and how browsers request pages',
            videoUrl: 'https://www.youtube.com/embed/7_LPdttKXPc',
            teachingNotes: 'Clarify that the web is one service running on the internet. Introduce request/response model with simple browser examples.',
            commonMistakes: [
              'Using internet and web as exact synonyms',
              'Not understanding browser-server interaction',
              'Assuming websites are stored in browser',
              'Ignoring HTTPS security purpose'
            ],
            prerequisites: ['Internet, IP and DNS'],
            teachingStrategies: [
              'Simulate HTTP request/response with classroom role play',
              'Identify browser, server, and protocol in examples',
              'Explain HTTPS lock icon and secure transfer',
              'Reference: CS Field Guide web chapter',
              'Online: Mozilla Learning - HTTP overview',
              'Quick note: Internet is infrastructure; WWW is a service on top'
            ],
            assessmentCriteria: 'Student distinguishes internet vs WWW and describes basic HTTP/HTTPS request flow.',
            estimatedMinutes: 45
          }
        ]
      },
      {
        id: 'data-structures',
        name: 'Data Structures',
        description: 'Arrays, stacks, queues, trees, and graphs',
        icon: '📊',
        progress: 0,
        atoms: [
          {
            id: 'ds-arrays-lists',
            moduleId: 'data-structures',
            name: 'Arrays and Lists Basics',
            level: 1,
            status: 'weak',
            summary: 'Store, access, and update collections of values effectively',
            videoUrl: 'https://www.youtube.com/embed/bum_19loj9A',
            teachingNotes: 'Start with everyday list examples before code. Emphasize index positions and bounds checking.',
            commonMistakes: [
              'Off-by-one index errors',
              'Confusing value and index',
              'Not checking list length before access',
              'Modifying list while iterating incorrectly'
            ],
            prerequisites: ['Python Fundamentals'],
            teachingStrategies: [
              'Use index cards to model list operations',
              'Practice insert/delete/search operations',
              'Pair tracing activities with small datasets',
              'Reference: DK Coding Projects - Lists sections',
              'Online: Programiz arrays/lists tutorials',
              'Quick note: Index starts at 0 in most programming languages'
            ],
            assessmentCriteria: 'Student performs basic list operations correctly and explains index-based access.',
            estimatedMinutes: 40
          },
          {
            id: 'ds-stack-queue',
            moduleId: 'data-structures',
            name: 'Stacks and Queues',
            level: 2,
            status: 'weak',
            summary: 'Understand LIFO and FIFO behavior with practical computing examples',
            videoUrl: 'https://www.youtube.com/embed/bum_19loj9A',
            teachingNotes: 'Use physical analogies: plates for stack, line of students for queue. Then map to programming operations push/pop/enqueue/dequeue.',
            commonMistakes: [
              'Mixing LIFO and FIFO rules',
              'Applying wrong operation names',
              'Not handling empty structure cases',
              'Confusing queue front and rear'
            ],
            prerequisites: ['Arrays and Lists Basics'],
            teachingStrategies: [
              'Role-play stack and queue operations',
              'Trace operation sequences step by step',
              'Use browser history and printer queue examples',
              'Reference: CS Unplugged data structures activities',
              'Online: GeeksforGeeks beginner stack/queue explainers',
              'Quick note: Stack = last in first out, Queue = first in first out'
            ],
            assessmentCriteria: 'Student identifies and simulates stack/queue operations with correct order and outputs.',
            estimatedMinutes: 45
          }
        ]
      },
      {
        id: 'algorithms',
        name: 'Algorithms',
        description: 'Sorting, searching, and algorithmic thinking',
        icon: '🧮',
        progress: 0,
        atoms: [
          {
            id: 'algo-searching',
            moduleId: 'algorithms',
            name: 'Linear and Binary Search',
            level: 1,
            status: 'weak',
            summary: 'Find items efficiently using step-by-step search strategies',
            videoUrl: 'https://www.youtube.com/embed/P3YID7liBug',
            teachingNotes: 'Teach linear search first, then binary search on sorted lists only. Make students justify why binary search is faster.',
            commonMistakes: [
              'Using binary search on unsorted data',
              'Incorrect midpoint calculation',
              'Not updating search bounds correctly',
              'Stopping too early'
            ],
            prerequisites: ['Arrays and Lists Basics'],
            teachingStrategies: [
              'Compare steps taken by linear vs binary search',
              'Use number cards to simulate midpoint checks',
              'Practice search trace tables',
              'Reference: KS3 Computing search algorithm worksheets',
              'Online: Khan Academy binary search lesson',
              'Quick note: Binary search only works when data is sorted'
            ],
            assessmentCriteria: 'Student traces linear and binary search correctly and selects the appropriate search method.',
            estimatedMinutes: 45
          },
          {
            id: 'algo-sorting',
            moduleId: 'algorithms',
            name: 'Sorting Algorithms Basics',
            level: 2,
            status: 'weak',
            summary: 'Understand and trace simple sorting methods like bubble sort',
            videoUrl: 'https://www.youtube.com/embed/P3YID7liBug',
            teachingNotes: 'Focus on process understanding over speed. Use visual swaps and passes for bubble sort and compare with selection-style approaches.',
            commonMistakes: [
              'Skipping full passes in bubble sort',
              'Not tracking swap count',
              'Assuming one pass always sorts the list',
              'Confusing ascending and descending order rules'
            ],
            prerequisites: ['Linear and Binary Search'],
            teachingStrategies: [
              'Run sort demonstrations with cards',
              'Count comparisons and swaps in each pass',
              'Use pseudocode-to-trace exercises',
              'Reference: CS Field Guide sorting activities',
              'Online: Visualgo sorting visualizer',
              'Quick note: Sorting accuracy first, then optimisation later'
            ],
            assessmentCriteria: 'Student traces a simple sorting algorithm accurately and explains each pass.',
            estimatedMinutes: 45
          }
        ]
      }
    ]
  }
];
