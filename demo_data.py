"""
Benchmark curated demo lecture content and questions for offline demonstration.
This guarantees that during a hackathon or viva, the student can test and demonstrate
the full interactive workflow without an active internet connection or AI API credits.
"""

from typing import List, Dict, Any

DEMO_LECTURE = {
    "title": "Process Synchronization, Critical Section & Semaphores",
    "subject": "Operating Systems (B.Tech CSE)",
    "content": """
Lecture Notes: Operating Systems - Unit III: Process Synchronization

1. Introduction to Race Conditions
When multiple concurrent processes execute and access shared data, the final result depends on the order of execution. This non-deterministic behavior is called a Race Condition. To avoid race conditions, concurrent processes must be synchronized.

2. The Critical Section Problem
A critical section is a piece of code where a process accesses shared resources (like shared memory, global variables, or files).
Any valid solution to the critical section problem must satisfy three essential criteria:
- Mutual Exclusion: If process P is executing in its critical section, no other processes can execute in their critical sections simultaneously.
- Progress: If no process is executing in its critical section and some processes wish to enter, only those processes not executing in their remainder sections can participate in deciding which will enter next, and this selection cannot be postponed indefinitely.
- Bounded Waiting: There must be a bound or limit on the number of times other processes are allowed to enter their critical sections after a process has made a request to enter and before that request is granted, avoiding starvation.

3. Synchronization Mechanisms: Mutex Locks and Semaphores
- Mutex Lock: A boolean lock (available or busy). A process acquires the lock before entering the critical section and releases it upon exiting. Only the process that acquired the lock can release it.
- Semaphores: An integer variable accessed only through two standard atomic operations: wait() (also known as P) and signal() (also known as V).
  - wait(S): while (S <= 0); S--; (decrements the semaphore value; blocks if S <= 0).
  - signal(S): S++; (increments the semaphore value; wakes up a blocked process).
- Counting Semaphore: Value can range over an unrestricted integer domain, useful for controlling access to a given resource consisting of a finite number of instances.
- Binary Semaphore: Integer value ranges between 0 and 1, functionally equivalent to a mutex lock.

4. The Bounded-Buffer (Producer-Consumer) Problem
A pool of n buffers, each capable of holding one item.
Uses three semaphores:
- mutex: binary semaphore initialized to 1 (protects access to buffer pool).
- empty: counting semaphore initialized to n (tracks empty slots).
- full: counting semaphore initialized to 0 (tracks filled slots).
Producer decrements empty and mutex, inserts item, increments mutex and full.
Consumer decrements full and mutex, removes item, increments mutex and empty.

5. Deadlocks and Priority Inversion
Improper synchronization can lead to deadlocks where two or more processes are waiting indefinitely for an event that can be caused only by one of the waiting processes.
Priority inversion occurs when a higher-priority process is blocked waiting for a resource held by a lower-priority process, while a medium-priority process preempts the lower-priority process. Priority Inheritance Protocol solves this by temporarily elevating the priority of the lower-priority process.
"""
}

DEMO_QUESTIONS_EN: List[Dict[str, Any]] = [
    {
        "question": "What is the primary condition where the outcome of concurrent execution depends on the exact order of access to shared memory?",
        "question_type": "mcq",
        "options": ["Deadlock", "Race Condition", "Starvation", "Priority Inversion"],
        "correct_answer": "Race Condition",
        "explanation": "A Race Condition occurs when multiple processes access and manipulate the same shared data concurrently and the outcome depends on the execution sequence.",
        "topic": "Race Conditions",
        "difficulty": "Easy",
        "evaluation_rubric": ""
    },
    {
        "question": "Which of the following is NOT one of the three fundamental requirements for solving the Critical Section Problem?",
        "question_type": "mcq",
        "options": ["Mutual Exclusion", "Progress", "Bounded Waiting", "Priority Scheduling"],
        "correct_answer": "Priority Scheduling",
        "explanation": "The three requirements defined by Dijkstra are Mutual Exclusion, Progress, and Bounded Waiting. Priority Scheduling is a CPU scheduling policy, not a requirement for critical section.",
        "topic": "Critical Section",
        "difficulty": "Easy",
        "evaluation_rubric": ""
    },
    {
        "question": "In the standard definition of a Semaphore, what occurs during the atomic wait() / P() operation when the semaphore value S is greater than 0?",
        "question_type": "mcq",
        "options": [
            "The process is added to a waiting queue and blocked",
            "The semaphore value S is decremented by 1 and the process continues",
            "The semaphore value S is incremented by 1",
            "An interrupt is triggered to reschedule all processes"
        ],
        "correct_answer": "The semaphore value S is decremented by 1 and the process continues",
        "explanation": "The wait() operation tests if S > 0; if true, it decrements S by 1 (S--) and allows the calling process to enter the critical section.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Medium",
        "evaluation_rubric": ""
    },
    {
        "question": "Explain what 'Bounded Waiting' means in the context of critical section synchronization and why it is critical for preventing starvation.",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Bounded waiting means there is a limit on the number of times other processes can enter their critical sections after a process has requested entry, ensuring no process is starved indefinitely.",
        "explanation": "Bounded waiting ensures fairness and prevents indefinite postponement (starvation). Even if other processes want the critical section, a requesting process will eventually get its turn within a finite bound.",
        "topic": "Critical Section",
        "difficulty": "Medium",
        "evaluation_rubric": "Full credit if student mentions: 1) A limit/bound on times other processes enter, and 2) Prevents starvation or ensures entry within finite time."
    },
    {
        "question": "In the classic Bounded-Buffer (Producer-Consumer) problem with buffer size N, what are the initial values of the 'empty' and 'full' semaphores?",
        "question_type": "mcq",
        "options": [
            "empty = 0, full = N",
            "empty = N, full = 0",
            "empty = 1, full = 1",
            "empty = N, full = N"
        ],
        "correct_answer": "empty = N, full = 0",
        "explanation": "Initially, all N slots are empty (so empty = N) and zero slots are occupied with items (so full = 0).",
        "topic": "Producer-Consumer Problem",
        "difficulty": "Medium",
        "evaluation_rubric": ""
    },
    {
        "question": "How does a Counting Semaphore differ from a Binary Semaphore (Mutex)?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "A counting semaphore can take any non-negative integer value to manage multiple instances of a resource, whereas a binary semaphore only takes values 0 or 1 and acts as a mutual exclusion lock.",
        "explanation": "Counting semaphores manage finite pools of multiple resource instances (e.g., N printers or N buffer slots), while binary semaphores provide mutual exclusion for a single resource.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Medium",
        "evaluation_rubric": "Full credit if the student notes that counting semaphores have unrestricted integer domains for multiple resources, while binary semaphores are restricted to 0 and 1 (or single resource mutual exclusion)."
    },
    {
        "question": "Consider a system where a high-priority process H needs a lock held by low-priority process L, but medium-priority process M preempts L. What is this phenomenon called and how is it solved?",
        "question_type": "mcq",
        "options": [
            "Convoy Effect, solved by Round Robin scheduling",
            "Priority Inversion, solved by Priority Inheritance Protocol",
            "Deadlock, solved by Banker's Algorithm",
            "Thrashing, solved by Working Set Model"
        ],
        "correct_answer": "Priority Inversion, solved by Priority Inheritance Protocol",
        "explanation": "Priority inversion happens when a medium process delays a low process holding a lock needed by a high process. Priority Inheritance temporarily elevates the low process to high priority until it releases the lock.",
        "topic": "Deadlocks & Priority Inversion",
        "difficulty": "Hard",
        "evaluation_rubric": ""
    },
    {
        "question": "Why does the Producer in the Bounded-Buffer problem call wait(empty) BEFORE calling wait(mutex)? What disaster would happen if the order were reversed when the buffer is full?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "If the producer called wait(mutex) first when the buffer was full, it would acquire the mutex lock and then block on wait(empty). The consumer could never acquire the mutex to consume an item and free up a slot, causing a deadlock.",
        "explanation": "Acquiring mutex first creates a circular wait deadlock: Producer holds mutex and waits for empty slot; Consumer needs mutex to produce empty slot but is blocked.",
        "topic": "Producer-Consumer Problem",
        "difficulty": "Hard",
        "evaluation_rubric": "Full credit if answer explains that acquiring mutex first when buffer is full causes a deadlock because the producer holds the mutex while blocking, preventing the consumer from emptying a slot."
    },
    {
        "question": "If two concurrent threads increment a shared counter variable 'count++' without synchronization, why can the final value be incorrect even on a single-core CPU?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Because count++ is not atomic at the machine level; it consists of three separate instructions (read memory to register, increment register, write back). Preemption between these instructions causes lost updates.",
        "explanation": "At the assembly level, count++ is: 1) MOV R1, [count], 2) ADD R1, 1, 3) MOV [count], R1. A context switch between these instructions results in one thread overwriting the other's update.",
        "topic": "Race Conditions",
        "difficulty": "Hard",
        "evaluation_rubric": "Full credit if the student mentions that count++ consists of multiple assembly instructions (load, increment, store) and is non-atomic, so context switches cause lost updates."
    },
    {
        "question": "Can a Binary Semaphore be signaled (V operation) by a thread that did NOT originally acquire it (P operation)?",
        "question_type": "mcq",
        "options": [
            "Yes, semaphores have no concept of ownership, unlike strict mutexes",
            "No, the operating system throws an illegal access exception",
            "No, only the thread with the lowest PID can signal",
            "Yes, but only if the process runs in kernel mode"
        ],
        "correct_answer": "Yes, semaphores have no concept of ownership, unlike strict mutexes",
        "explanation": "Unlike Mutex locks (which typically enforce ownership where only the acquiring thread can release it), a semaphore is purely a signaling integer variable and can be signaled by any thread.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Hard",
        "evaluation_rubric": ""
    }
]

DEMO_QUESTIONS_HI: List[Dict[str, Any]] = [
    {
        "question": "Jab multiple concurrent processes ek hi shared memory ko access karte hain aur output unke execution sequence par depend karta hai, toh ise kya kehte hain?",
        "question_type": "mcq",
        "options": ["Deadlock", "Race Condition", "Starvation", "Priority Inversion"],
        "correct_answer": "Race Condition",
        "explanation": "Race Condition tab hoti hai jab concurrent processes shared data ko manipulate karte hain aur final result execution order par depend karta hai.",
        "topic": "Race Conditions",
        "difficulty": "Easy",
        "evaluation_rubric": ""
    },
    {
        "question": "Critical Section Problem ke valid solution ke liye inme se kaunsi requirement zaroori NAHI hai?",
        "question_type": "mcq",
        "options": ["Mutual Exclusion", "Progress", "Bounded Waiting", "Priority Scheduling"],
        "correct_answer": "Priority Scheduling",
        "explanation": "Dijkstra ke anusaar teen zaroori conditions hain: Mutual Exclusion, Progress, aur Bounded Waiting. Priority Scheduling iska hissa nahi hai.",
        "topic": "Critical Section",
        "difficulty": "Easy",
        "evaluation_rubric": ""
    },
    {
        "question": "Standard Semaphore me wait() ya P() operation tab kya karta hai jab semaphore variable S ki value 0 se badi hoti hai?",
        "question_type": "mcq",
        "options": [
            "Process ko queue me block kar deta hai",
            "S ki value ko 1 se decrement karta hai aur process continue karta hai",
            "S ki value ko 1 se increment karta hai",
            "Ek system interrupt trigger karta hai"
        ],
        "correct_answer": "S ki value ko 1 se decrement karta hai aur process continue karta hai",
        "explanation": "Agar S > 0 hai, toh wait() operation S ko decrement (S--) karta hai aur process critical section me enter kar sakta hai.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Medium",
        "evaluation_rubric": ""
    },
    {
        "question": "Critical section synchronization me 'Bounded Waiting' ka kya matlab hai aur ye starvation rokne ke liye kyu zaroori hai?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Bounded waiting ka matlab hai ki ek process ke entry request karne ke baad baaki processes ke entry karne par ek fixed limit ya bound hota hai, jisse koi bhi process indefinitely wait na kare aur starvation na ho.",
        "explanation": "Bounded waiting guarantee karti hai ki har requesting process ko finite time ke andar critical section ka access milega.",
        "topic": "Critical Section",
        "difficulty": "Medium",
        "evaluation_rubric": "Full credit agar student mention kare: 1) Dusre processes par limit/bound, aur 2) Starvation ya infinite wait rokna."
    },
    {
        "question": "Bounded-Buffer (Producer-Consumer) problem me buffer capacity N hone par, 'empty' aur 'full' semaphores ki starting values kya hoti hain?",
        "question_type": "mcq",
        "options": [
            "empty = 0, full = N",
            "empty = N, full = 0",
            "empty = 1, full = 1",
            "empty = N, full = N"
        ],
        "correct_answer": "empty = N, full = 0",
        "explanation": "Shuruat me saare N slots empty hote hain (empty = N) aur 0 slots full hote hain (full = 0).",
        "topic": "Producer-Consumer Problem",
        "difficulty": "Medium",
        "evaluation_rubric": ""
    },
    {
        "question": "Counting Semaphore aur Binary Semaphore (Mutex) ke beech me kya main farak hai?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Counting semaphore ki value kisi bhi non-negative integer tak ho sakti hai multiple resources manage karne ke liye, jabki binary semaphore sirf 0 ya 1 value leta hai aur mutual exclusion ke liye use hota hai.",
        "explanation": "Counting semaphore multiple resource units ke liye hota hai, jabki binary semaphore single resource lock ki tarah kaam karta hai.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Medium",
        "evaluation_rubric": "Full credit agar answer me unrestricted integer vs 0/1 binary domain ka zikr ho."
    },
    {
        "question": "Jab High-priority process H ek lock ke liye wait karta hai jo Low-priority process L ke paas hai, aur Medium-priority process M beech me L ko preempt kar deta hai, toh is problem ko kya kehte hain aur iska solution kya hai?",
        "question_type": "mcq",
        "options": [
            "Convoy Effect, solved by Round Robin",
            "Priority Inversion, solved by Priority Inheritance Protocol",
            "Deadlock, solved by Banker's Algorithm",
            "Thrashing, solved by Working Set Model"
        ],
        "correct_answer": "Priority Inversion, solved by Priority Inheritance Protocol",
        "explanation": "Ise Priority Inversion kehte hain. Priority Inheritance protocol se Low process ki priority temporarily badha di jaati hai jab tak wo lock release na kare.",
        "topic": "Deadlocks & Priority Inversion",
        "difficulty": "Hard",
        "evaluation_rubric": ""
    },
    {
        "question": "Bounded-Buffer problem me Producer ko wait(mutex) se pehle wait(empty) kyu call karna padta hai? Agar buffer full ho aur ulta call kiya toh kya hoga?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Agar buffer full hone par producer pehle wait(mutex) lega toh wo mutex hold karke wait(empty) par block ho jayega. Consumer mutex na milne ki wajah se koi item consume nahi kar payega, jisse Deadlock ho jayega.",
        "explanation": "Pehle mutex lene se deadlock ban jata hai kyunki producer lock pakad kar so jata hai aur consumer lock na milne se jagah khali nahi kar pata.",
        "topic": "Producer-Consumer Problem",
        "difficulty": "Hard",
        "evaluation_rubric": "Full credit agar answer me Deadlock hone aur producer dwara mutex hold karke block hone ka zikr ho."
    },
    {
        "question": "Agar do concurrent threads shared variable 'count++' ko bina synchronization ke execute karte hain, toh single core processor par bhi answer galat kyu ho sakta hai?",
        "question_type": "short_answer",
        "options": [],
        "correct_answer": "Kyunki count++ machine level par atomic nahi hota; ye teen instructions me banta hai (load from memory, increment in register, store back to memory). Inke beech context switch hone par updates overwrite ho jaate hain.",
        "explanation": "Assembly me load, add, aur store 3 alag steps hote hain. Context switch se lost update problem hoti hai.",
        "topic": "Race Conditions",
        "difficulty": "Hard",
        "evaluation_rubric": "Full credit agar answer me load/increment/store instructions aur non-atomic execution ka zikr ho."
    },
    {
        "question": "Kya Binary Semaphore ko wo thread signal (V) kar sakta hai jisne use acquire (P) nahi kiya tha?",
        "question_type": "mcq",
        "options": [
            "Haan, semaphore me ownership ka concept nahi hota, unlike strict mutex",
            "Nahi, OS illegal memory exception de deta hai",
            "Nahi, sirf lowest PID wala process signal kar sakta hai",
            "Haan, lekin sirf kernel mode me"
        ],
        "correct_answer": "Haan, semaphore me ownership ka concept nahi hota, unlike strict mutex",
        "explanation": "Mutex me ownership hoti hai (jisne lock liya wahi unlock karega), lekin semaphore ek signaling variable hai jise koi bhi thread signal kar sakta hai.",
        "topic": "Semaphores & Mutex",
        "difficulty": "Hard",
        "evaluation_rubric": ""
    }
]

def get_demo_questions(language: str = "en", limit: int = 10) -> List[Dict[str, Any]]:
    """Returns curated demo questions tailored to language and target limit."""
    questions = DEMO_QUESTIONS_HI if language in ["hi", "hinglish"] else DEMO_QUESTIONS_EN
    return questions[:limit]
