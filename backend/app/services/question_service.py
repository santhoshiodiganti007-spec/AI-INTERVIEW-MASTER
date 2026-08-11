from sqlalchemy.orm import Session
from app.models.all_models import Question, CodingProblem

INITIAL_QUESTIONS = [
    # --- PYTHON TRACK ---
    {
        "question": "Explain Python's GIL (Global Interpreter Lock). How does it affect multithreading vs multiprocessing?",
        "category": "Python",
        "topic": "Concurrency & Memory Management",
        "difficulty": "ADVANCED",
        "role": "Software / Python Developer",
        "expected_answer": "The Global Interpreter Lock (GIL) is a mutex that prevents multiple native threads from executing Python bytecodes at once in CPython. It simplifies CPython's memory management because reference counting is non-atomic. Consequently, multithreading in CPython does not run CPU-bound tasks in parallel across CPU cores. For CPU-bound workloads, multiprocessing should be used as it spawns separate Python processes, each with its own interpreter and memory space. For I/O-bound tasks, multithreading or asyncio remains effective.",
        "key_points": [
            "CPython single-thread bytecode lock",
            "Reference counting thread safety",
            "CPU-bound vs I/O-bound performance",
            "Multiprocessing spawns separate processes with independent GILs",
            "Asyncio/Multithreading suitable for I/O bound concurrency"
        ],
        "common_mistakes": [
            "Confusing multithreading impossibility with inability to run I/O concurrently",
            "Thinking GIL exists in all Python implementations (it is specific to CPython, Jython/IronPython do not have GIL)"
        ],
        "follow_up_questions": [
            "How does Python 3.12+ subinterpreters (PEP 684) mitigate GIL restrictions?",
            "When would you choose `asyncio` over `concurrent.futures.ThreadPoolExecutor`?"
        ],
        "estimated_time_minutes": 10,
        "tags": ["GIL", "Multithreading", "Multiprocessing", "Concurrency", "CPython"]
    },
    {
        "question": "Compare Iterators and Generators in Python. What is the memory benefit of `yield`?",
        "category": "Python",
        "topic": "Iterators & Generators",
        "difficulty": "INTERMEDIATE",
        "role": "Software / Python Developer",
        "expected_answer": "An Iterator is an object that implements the iterator protocol with `__iter__()` and `__next__()` methods. A Generator is a simpler way of creating iterators using functions with the `yield` keyword. Generators compute values lazily on-the-fly (lazy evaluation) rather than storing the entire dataset in memory, achieving O(1) space complexity compared to O(N) space for lists.",
        "key_points": [
            "Iterator protocol (__iter__ & __next__)",
            "Generator functions yield values on demand",
            "Lazy evaluation saves RAM",
            "Generators maintain execution state automatically between yield statements"
        ],
        "common_mistakes": [
            "Trying to index or reuse a generator once exhausted",
            "Believing generator expressions create tuples when enclosed in parentheses"
        ],
        "follow_up_questions": [
            "How does `yield from` simplify nested generator delegation?",
            "What exception is raised when an iterator runs out of elements?"
        ],
        "estimated_time_minutes": 8,
        "tags": ["Iterators", "Generators", "Memory Management", "Python Basics"]
    },
    {
        "question": "What are Decorators in Python, and how do you write a parameterized decorator that preserves function metadata?",
        "category": "Python",
        "topic": "Decorators",
        "difficulty": "INTERMEDIATE",
        "role": "Software / Python Developer",
        "expected_answer": "Decorators are callable objects used to modify or extend the behavior of functions or classes without altering their source code. They take a function as an argument and return a wrapper function. To write a parameterized decorator, you nest three functions: outer function for arguments, middle for the target function, and inner wrapper. Always use `@functools.wraps(fn)` on the inner wrapper to preserve original metadata like `__name__` and `__doc__`.",
        "key_points": [
            "Higher-order functions in Python",
            "Closure pattern",
            "functools.wraps preservation",
            "Triple function nesting for arguments"
        ],
        "common_mistakes": [
            "Forgetting to return the wrapper function from the decorator",
            "Omitting @wraps, leading to loss of __name__ and docstrings in debugging"
        ],
        "follow_up_questions": [
            "Can class instances act as decorators? How?",
            "How do decorators execute at module import time versus function call time?"
        ],
        "estimated_time_minutes": 10,
        "tags": ["Decorators", "Functional", "Closures", "OOP"]
    },

    # --- OOP TRACK (14 Pillars) ---
    {
        "question": "Explain Method Overriding vs Method Overloading in Python with code examples.",
        "category": "OOP",
        "topic": "Polymorphism",
        "difficulty": "INTERMEDIATE",
        "role": "Software / Python Developer",
        "expected_answer": "Method Overriding allows a subclass to provide a specific implementation of a method defined in its superclass. Method Overloading allows a class to have multiple methods with the same name but different parameters. Python natively supports Method Overriding, but does NOT support classical compile-time Method Overloading by default (the last method definition overrides previous ones). In Python, overloading is typically achieved via default arguments, `*args`, `**kwargs`, or `@functools.singledispatch`.",
        "key_points": [
            "Overriding happens across inheritance hierarchy",
            "Overloading happens within the same class signature scope",
            "Python dynamic typing and optional parameters handle overloading",
            "functools.singledispatch for single-dispatch overload polymorphism"
        ],
        "common_mistakes": [
            "Defining two methods with the same name in a Python class expecting traditional Java-style overloading",
            "Confusing method overriding with operator overloading"
        ],
        "follow_up_questions": [
            "How does `super().method()` work in Python's multiple inheritance and MRO (Method Resolution Order)?",
            "What algorithm does C3 linearization use for MRO?"
        ],
        "estimated_time_minutes": 10,
        "tags": ["OOP", "Polymorphism", "Method Overriding", "Method Overloading", "MRO"]
    },
    {
        "question": "What is Encapsulation and how does Python achieve private/protected members?",
        "category": "OOP",
        "topic": "Encapsulation",
        "difficulty": "BEGINNER",
        "role": "Software / Python Developer",
        "expected_answer": "Encapsulation bundles data (attributes) and methods that operate on that data into a single unit (class), while restricting direct external access to internal state. Python uses naming conventions: single underscore `_var` indicates protected (convention only), while double underscore `__var` triggers name mangling (`_ClassName__var`) to prevent accidental override in subclasses. Controlled access is best provided using `@property` getters and setters.",
        "key_points": [
            "Bundling state & behavior",
            "Single underscore protected convention",
            "Double underscore name mangling",
            "Property decorators (@property, @setter)"
        ],
        "common_mistakes": [
            "Assuming double underscores make attributes strictly private/inaccessible in memory",
            "Writing explicit Java-like get_var() and set_var() methods instead of pythonic @property"
        ],
        "follow_up_questions": [
            "How do `@classmethod` and `@staticmethod` differ in binding scope?",
            "What are `__slots__` and how do they impact encapsulation and RAM usage?"
        ],
        "estimated_time_minutes": 8,
        "tags": ["OOP", "Encapsulation", "Properties", "Name Mangling"]
    },

    # --- AIML TRACK ---
    {
        "question": "Explain Bias-Variance Tradeoff, Overfitting, Underfitting, and how to detect/mitigate them in XGBoost.",
        "category": "Machine Learning",
        "topic": "ML Fundamentals & Boosting",
        "difficulty": "ADVANCED",
        "role": "AIML / Data Science",
        "expected_answer": "Bias error stems from oversimplifying assumptions (Underfitting: high training error, high validation error). Variance error stems from high sensitivity to small fluctuations in training data (Overfitting: low training error, high validation error). XGBoost mitigates high variance (overfitting) using L1 (reg_alpha) & L2 (reg_lambda) regularization, subsampling rows (`subsample`), feature sampling (`colsample_bytree`), max_depth caps, learning rate scaling (`eta`), and early stopping rounds.",
        "key_points": [
            "Bias = Error from erroneous model assumptions",
            "Variance = Error from sensitivity to training noise",
            "Underfitting vs Overfitting learning curves",
            "XGBoost hyperparameters: max_depth, subsample, colsample_bytree, reg_alpha, reg_lambda, learning_rate",
            "Cross-validation monitoring"
        ],
        "common_mistakes": [
            "Increasing max_depth in XGBoost when attempting to solve overfitting",
            "Evaluating model generalization performance solely on training accuracy"
        ],
        "follow_up_questions": [
            "How does Gradient Boosting differ from Random Forest in bagging vs boosting philosophy?",
            "Explain how SHAP (Shapley Additive exPlanations) explains XGBoost predictions."
        ],
        "estimated_time_minutes": 12,
        "tags": ["ML", "XGBoost", "Bias-Variance", "Regularization", "Overfitting"]
    },
    {
        "question": "What is vanishing/exploding gradient in deep neural networks, and how do Residual Connections (ResNet) and Batch Normalization resolve it?",
        "category": "Deep Learning",
        "topic": "Neural Networks Architecture",
        "difficulty": "ADVANCED",
        "role": "AIML / Data Science",
        "expected_answer": "In deep networks, backpropagating gradients through many layers using the chain rule causes repeated matrix multiplications. If weights/derivatives are <1, gradients exponentially vanish to 0; if >1, they explode to infinity. Batch Normalization stabilizes layer inputs by normalizing mean to 0 and variance to 1 per batch, preventing internal covariate shift. Residual Connections (ResNet) add skip connections $y = f(x) + x$, allowing gradients to flow directly back through the identity mapping $\\frac{\\partial y}{\\partial x} = \\frac{\\partial f(x)}{\\partial x} + 1$, guaranteeing non-zero gradient flow.",
        "key_points": [
            "Chain rule multiplication through deep layers",
            "Batch Normalization stabilizes internal covariate shift & scales gradients",
            "Residual skip connections y = f(x) + x",
            "Identity mapping guarantees minimum gradient magnitude of 1 during backprop"
        ],
        "common_mistakes": [
            "Believing Batch Normalization works identically during training and inference (during inference, running mean/std are used)",
            "Using sigmoid activations in ultra-deep networks without residual links"
        ],
        "follow_up_questions": [
            "Why is Layer Normalization preferred over Batch Normalization in Transformers?",
            "How does Gradient Clipping explicitly address exploding gradients in RNNs?"
        ],
        "estimated_time_minutes": 12,
        "tags": ["Deep Learning", "ResNet", "BatchNorm", "Gradients", "Backpropagation"]
    },

    # --- GENERATIVE AI / LLM TRACK ---
    {
        "question": "Explain Self-Attention and Multi-Head Attention in the Transformer Architecture with Query, Key, and Value matrices.",
        "category": "Generative AI",
        "topic": "Transformers & Attention",
        "difficulty": "ADVANCED",
        "role": "Generative AI / LLM",
        "expected_answer": "Self-attention enables a sequence token to dynamically attend to all other tokens in the context. Given input embeddings X, linear projections produce Query ($Q=XW_Q$), Key ($K=XW_K$), and Value ($V=XW_V$). The attention score matrix is calculated as $\\text{Softmax}\\left(\\frac{QK^T}{\\sqrt{d_k}}\\right)V$. Scaling by $\\sqrt{d_k}$ prevents dot products from growing excessively large, avoiding vanishing gradients in softmax. Multi-Head Attention computes multiple parallel attention heads using independent linear projections, allowing the model to jointly attend to information from different representation subspaces at different positions.",
        "key_points": [
            "Q, K, V linear projections",
            "Scaled Dot-Product formula: Softmax(Q K^T / sqrt(d_k)) V",
            "Scaling factor sqrt(d_k) stabilizes softmax gradients",
            "Multi-head splits embedding dimension into h subspaces to capture diverse semantic relationships"
        ],
        "common_mistakes": [
            "Forgetting why the scaling factor sqrt(d_k) is mathematically essential",
            "Confusing causal (masked) self-attention in decoders with bi-directional self-attention in encoders"
        ],
        "follow_up_questions": [
            "What is Rotary Position Embedding (RoPE) and why is it superior to learned absolute positional encodings for context extension?",
            "Explain FlashAttention and how it speeds up attention calculation without changing output math."
        ],
        "estimated_time_minutes": 15,
        "tags": ["GenAI", "Transformers", "Self-Attention", "Multi-Head Attention", "LLMs"]
    },
    {
        "question": "Design a Production RAG System for Millions of Enterprise Documents. Detail Chunking, Hybrid Search, Reranking, and Evaluation.",
        "category": "RAG",
        "topic": "System Architecture",
        "difficulty": "ADVANCED",
        "role": "Generative AI / LLM",
        "expected_answer": "A production RAG pipeline consists of: 1) Ingestion: OCR/PDF text extraction, semantic chunking (256-512 tokens with 10-20% overlap) with metadata tagging. 2) Embeddings & Vector DB: Dense embeddings (e.g. OpenAI text-embedding-3 or BGE-M3) indexed in Qdrant/Pinecone/PGVector with HNSW indexing. 3) Hybrid Search: Reciprocal Rank Fusion (RRF) combining dense vector search (semantic) and BM25 sparse keyword search. 4) Reranking: Cross-Encoder reranker (Cohere/BGE-Reranker) to select top-k (e.g., top 5 out of 50 retrieved). 5) Prompting & LLM: System prompt with groundness instructions, temperature=0.0. 6) Evaluation: RAGAS metrics (Faithfulness, Answer Relevance, Context Recall, Context Precision).",
        "key_points": [
            "Semantic chunking with overlap",
            "Hybrid Search (Dense vector + Sparse BM25 via RRF)",
            "Cross-Encoder Reranking to eliminate noise",
            "Context window optimization & citation enforcement",
            "RAGAS evaluation framework"
        ],
        "common_mistakes": [
            "Relying solely on dense vector search for domain-specific acronyms/IDs where sparse keyword matching is crucial",
            "Not handling chunk boundary truncation"
        ],
        "follow_up_questions": [
            "How would you implement Parent-Document Retrieval vs Sentence-Window Retrieval?",
            "How do you handle real-time document updates and deletion in HNSW vector indices?"
        ],
        "estimated_time_minutes": 15,
        "tags": ["RAG", "System Design", "Vector DB", "Hybrid Search", "Reranking", "LLM"]
    },
    {
        "question": "What is the difference between Fine-Tuning with LoRA / QLoRA versus RAG? When should you use which?",
        "category": "Generative AI",
        "topic": "LLM Customization",
        "difficulty": "ADVANCED",
        "role": "Generative AI / LLM",
        "expected_answer": "RAG provides external static/dynamic knowledge to the LLM at inference time via prompt injection without modifying model parameters. It is ideal for rapidly changing data, strict factual accuracy, and explicit citation. Fine-Tuning (LoRA/QLoRA) updates small low-rank adapter matrices ($W = W_0 + B A$) attached to base model weights, teaching the model new styles, output formats, domain tone, or specialized reasoning tasks. Use RAG to add knowledge; use LoRA to change behavior or style. Use both (RA-FT) for enterprise specialized AI assistants.",
        "key_points": [
            "RAG = In-context dynamic knowledge injection",
            "LoRA/QLoRA = Weight modification via Low-Rank Adaptation matrices",
            "RAG for facts/freshness; Fine-tuning for format/style/tone/reasoning",
            "QLoRA uses 4-bit NormalFloat (NF4) quantization + double quantization to reduce VRAM requirements"
        ],
        "common_mistakes": [
            "Fine-tuning an LLM to memorize enterprise dynamic knowledge bases (leads to hallucination and static knowledge staleness)",
            "Using high rank r in LoRA when low rank (r=8 or 16) achieves identical task alignment"
        ],
        "follow_up_questions": [
            "Explain how RLHF (Direct Preference Optimization - DPO) aligns LLM responses compared to SFT.",
            "What is Tool/Function Calling and how does MCP (Model Context Protocol) standardize LLM agent connections?"
        ],
        "estimated_time_minutes": 12,
        "tags": ["GenAI", "LoRA", "QLoRA", "Fine-Tuning", "RAG", "LLMs"]
    },

    # --- BEHAVIORAL TRACK (STAR Framework) ---
    {
        "question": "Tell me about a time when you faced a severe technical disagreement or conflict within your team. How did you resolve it?",
        "category": "Behavioral",
        "topic": "Conflict Resolution & Teamwork",
        "difficulty": "INTERMEDIATE",
        "role": "ALL",
        "expected_answer": "Use the STAR framework: Situation: Brief context on the project and the technical disagreement (e.g. monolithic refactoring vs microservice adoption under deadline). Task: Your responsibility to deliver on-time without compromising team cohesion. Action: Objective benchmarks, prototyping both approaches, gathering data, initiating open design review, active listening, finding compromise. Result: Concrete positive metric (e.g. delivered 2 weeks early, 99.9% uptime, unified team buy-in).",
        "key_points": [
            "Situation (S): Context & problem statement",
            "Task (T): Specific role and goals",
            "Action (A): Objective data-driven actions & communication",
            "Result (R): Quantifiable metric & positive takeaway"
        ],
        "common_mistakes": [
            "Focusing 80% of the time on complaining about the situation or team member instead of personal actions taken",
            "Failing to provide measurable results or engineering lessons learned"
        ],
        "follow_up_questions": [
            "What would you do differently if faced with the exact same situation today?",
            "How do you ensure quiet team members' opinions are heard during architecture discussions?"
        ],
        "estimated_time_minutes": 10,
        "tags": ["Behavioral", "STAR", "Leadership", "Google Leadership Principles"]
    }
]

INITIAL_CODING_PROBLEMS = [
    {
        "title": "Two Sum (Hash Table Pattern)",
        "topic": "Arrays & Hashing",
        "difficulty": "BEGINNER",
        "problem_statement": "Given an array of integers `nums` and an integer `target`, return indices of the two numbers such that they add up to `target`. You may assume that each input would have exactly one solution, and you may not use the same element twice.",
        "examples": [
            {"input": "nums = [2, 7, 11, 15], target = 9", "output": "[0, 1]", "explanation": "nums[0] + nums[1] == 9, so return [0, 1]."}
        ],
        "constraints": ["2 <= nums.length <= 10^4", "-10^9 <= nums[i] <= 10^9", "Exactly one valid answer exists."],
        "hint": "Use a hash map to store previously seen numbers and their indices while iterating.",
        "brute_force_approach": "Use nested loops to check all pairs of elements. Time Complexity: O(N^2), Space Complexity: O(1).",
        "optimized_approach": "Iterate through the array once. For each number x, calculate complement = target - x. Check if complement exists in hash map. If yes, return current index and complement index. If no, insert x and its index into hash map.",
        "python_solution": """def twoSum(nums: list[int], target: int) -> list[int]:
    seen = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in seen:
            return [seen[complement], i]
        seen[num] = i
    return []""",
        "time_complexity": "O(N)",
        "space_complexity": "O(N)",
        "explanation": "Single-pass hash table lookup takes O(1) time per element. Total time O(N), total space O(N).",
        "follow_up_questions": ["What if the array is already sorted? How would Two Pointers achieve O(1) space complexity?"]
    },
    {
        "title": "Longest Substring Without Repeating Characters (Sliding Window)",
        "topic": "Sliding Window",
        "difficulty": "INTERMEDIATE",
        "problem_statement": "Given a string `s`, find the length of the longest substring without repeating characters.",
        "examples": [
            {"input": "s = 'abcabcbb'", "output": "3", "explanation": "The answer is 'abc', with length 3."}
        ],
        "constraints": ["0 <= s.length <= 5 * 10^4", "s consists of English letters, digits, symbols and spaces."],
        "hint": "Maintain a dynamic sliding window `[left, right]` and record character last seen indices in a dictionary.",
        "brute_force_approach": "Generate all possible substrings and check for duplicate characters using a set. Time Complexity: O(N^3).",
        "optimized_approach": "Use a sliding window with two pointers left and right. Store the most recent index of each character in a map. When a repeating character is encountered at right, move left to max(left, char_map[char] + 1).",
        "python_solution": """def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len""",
        "time_complexity": "O(N)",
        "space_complexity": "O(min(N, M)) where M is alphabet size",
        "explanation": "Both right and left pointers advance at most N times across the string.",
        "follow_up_questions": ["How would you adapt this for at most K distinct characters?"]
    },
    {
        "title": "Invert Binary Tree (Tree Recursion)",
        "topic": "Binary Tree",
        "difficulty": "BEGINNER",
        "problem_statement": "Given the root of a binary tree, invert the tree, and return its root.",
        "examples": [
            {"input": "root = [4,2,7,1,3,6,9]", "output": "[4,7,2,9,6,3,1]", "explanation": "Left and right subtrees of every node are swapped."}
        ],
        "constraints": ["The number of nodes in the tree is in range [0, 100].", "-100 <= Node.val <= 100"],
        "hint": "Recursively swap the left and right children for every node.",
        "brute_force_approach": "N/A - Tree recursion or BFS queue iteration is canonical.",
        "optimized_approach": "Base case: if root is None return None. Swap root.left and root.right. Recursively call invertTree on root.left and root.right.",
        "python_solution": """class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

def invertTree(root: TreeNode) -> TreeNode:
    if not root:
        return None
    root.left, root.right = invertTree(root.right), invertTree(root.left)
    return root""",
        "time_complexity": "O(N)",
        "space_complexity": "O(H) where H is tree height for call stack",
        "explanation": "Every node is visited exactly once.",
        "follow_up_questions": ["Write the iterative BFS solution using collections.deque."]
    }
]

def seed_database_if_empty(db: Session):
    if db.query(Question).count() == 0:
        for q in INITIAL_QUESTIONS:
            db_q = Question(**q)
            db.add(db_q)
    
    if db.query(CodingProblem).count() == 0:
        for p in INITIAL_CODING_PROBLEMS:
            db_p = CodingProblem(**p)
            db.add(db_p)
            
    db.commit()
