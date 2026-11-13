"""
Configuration module for the Local AI Mock Interview Assistant.
Defines roles, experience levels, evaluation criteria, and a comprehensive
curated local question bank. Completely offline, zero external API keys required.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "interview_history.db"
REPORTS_DIR = BASE_DIR / "saved_reports"
REPORTS_DIR.mkdir(parents=True, exist_ok=True)

# Application Meta
APP_TITLE = "AI Interviewer"
APP_SUBTITLE = "Modern, Intelligent AI Interview Platform & Performance Analytics"
APP_VERSION = "2.0.0 (Local Engine)"

# Available Job Roles
JOB_ROLES = [
    "Python Developer / Software Engineer",
    "Frontend Developer (React / JavaScript)",
    "Backend Developer (API & Microservices)",
    "Data Scientist / AI Engineer",
    "DevOps & Cloud Infrastructure Engineer",
    "Product Manager & Technical Lead"
]

# Experience Levels
EXPERIENCE_LEVELS = [
    "Entry Level (0 - 2 Years)",
    "Mid Level (3 - 5 Years)",
    "Senior / Staff Level (5+ Years)"
]

# Interview Categories
INTERVIEW_CATEGORIES = [
    "Comprehensive (3 Technical + 2 Behavioral)",
    "Technical Deep-Dive",
    "Behavioral & Situational (STAR)",
    "System Architecture & Best Practices"
]

# Scoring Rubric & Weights (Total Max = 10.0 points)
# 1. Concept Coverage: 3.5 points (Depth & thematic breadth)
# 2. Keyword & Terminology Match: 2.5 points (Precision & domain vocabulary)
# 3. Structure & Elaboration: 2.0 points (Completeness, length, structured flow)
# 4. Relevance & Focus: 2.0 points (On-topic density, avoidance of filler)
RUBRIC_WEIGHTS = {
    "concept_coverage": 3.5,
    "keyword_match": 2.5,
    "structure_completeness": 2.0,
    "relevance_focus": 2.0
}

TOTAL_QUESTIONS_PER_INTERVIEW = 5
TECHNICAL_QUESTIONS_COUNT = 3
BEHAVIORAL_QUESTIONS_COUNT = 2

# Question Bank Organized by Role & Experience Level
# Each entry contains explicit rubric targets for transparent evaluation.
QUESTION_BANK = {
    "Python Developer / Software Engineer": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "py_entry_01",
                "type": "technical",
                "topic": "Memory Management & Data Types",
                "question": "Explain the difference between mutable and immutable data types in Python. Give two examples of each and describe how Python handles memory assignment for them.",
                "key_concepts": [
                    "object identity and memory address",
                    "in-place modification vs creating new object",
                    "lists/dictionaries as mutable",
                    "tuples/strings/integers as immutable",
                    "id() function or references"
                ],
                "keywords": ["mutable", "immutable", "list", "dict", "tuple", "string", "reference", "memory", "id", "hashable"],
                "guidance": "Mention specific types, how modification affects id() or memory references, and implications on dictionary keys.",
                "sample_answer": "In Python, mutable objects can be modified in-place after creation without changing their memory address (identity). Examples include lists, dictionaries, and sets. Immutable objects cannot be altered once created; any modification produces a new object in memory with a distinct id. Examples include tuples, strings, integers, and frozensets. In memory, variable names are references/pointers to objects. Mutating a list (e.g., list.append()) preserves the object identity (id(x)), whereas reassigning a string creates a fresh object. Immutable types are also hashable, making them suitable as dictionary keys."
            },
            {
                "id": "py_entry_02",
                "type": "technical",
                "topic": "Error Handling & Control Flow",
                "question": "How does exception handling work in Python? Explain try, except, else, and finally blocks, and why catching generic 'Exception' is often discouraged.",
                "key_concepts": [
                    "try block contains risky code",
                    "except catches specific exception types",
                    "else executes only when no exception occurs",
                    "finally always runs regardless of outcome",
                    "catching bare Exception masks bugs and KeyboardInterrupt"
                ],
                "keywords": ["try", "except", "else", "finally", "exception", "raise", "traceback", "specific", "cleanup", "resource"],
                "guidance": "Detail each clause's purpose, resource cleanup in finally, and why bare except hinders debugging.",
                "sample_answer": "Python exception handling uses 'try' to encapsulate code that might raise an error. 'except SpecificError' intercepts known failure modes. The 'else' block executes only if the try block completes successfully without raising exceptions, which keeps the try block minimal. The 'finally' block is guaranteed to execute regardless of whether an exception was raised, caught, or unhandled, making it ideal for resource cleanup (e.g., closing file handles). Catching a generic 'Exception' or using bare 'except:' is discouraged because it can silently mask unrelated programming bugs (like NameError or TypeError) and make root-cause debugging very difficult."
            },
            {
                "id": "py_entry_03",
                "type": "technical",
                "topic": "Object Oriented Programming",
                "question": "What is the difference between class methods, static methods, and instance methods in Python? When would you use the @classmethod and @staticmethod decorators?",
                "key_concepts": [
                    "instance methods receive self and access instance state",
                    "class methods receive cls via @classmethod and access class state/factory",
                    "static methods receive neither self nor cls via @staticmethod",
                    "alternative constructors or utility functions",
                    "decorator syntax and purpose"
                ],
                "keywords": ["instance", "classmethod", "staticmethod", "self", "cls", "decorator", "factory", "utility", "state"],
                "guidance": "Highlight the first argument passed (self vs cls vs none) and typical architectural use cases.",
                "sample_answer": "Instance methods are the default in Python classes; they take 'self' as their first argument and can read/modify both instance attributes and class state. Class methods are decorated with @classmethod and take 'cls' as their first argument; they can access and modify class-level state and are widely used to build alternative constructors (factories). Static methods are decorated with @staticmethod and accept neither 'self' nor 'cls'; they behave like plain functions namespaced within the class, used for self-contained utilities that do not require access to object or class attributes."
            },
            {
                "id": "py_entry_04",
                "type": "technical",
                "topic": "Python Iterators & Generators",
                "question": "What are generators in Python, how does the 'yield' keyword operate, and what are their memory benefits compared to regular lists?",
                "key_concepts": [
                    "lazy evaluation and state suspension",
                    "yield returns value and pauses execution frame",
                    "memory efficiency with large datasets / streams",
                    "iteration protocol (__iter__ and __next__)",
                    "generator expressions vs list comprehensions"
                ],
                "keywords": ["generator", "yield", "lazy", "memory", "iteration", "next", "stream", "comprehension", "iterator"],
                "guidance": "Explain execution suspension, the iterator protocol, and why generators avoid loading entire sequences into RAM.",
                "sample_answer": "Generators are specialized iterator functions in Python that use the 'yield' keyword instead of 'return'. When 'yield' is encountered, the function's execution state, local variables, and instruction pointer are suspended, and the yielded value is sent to the caller. On the next call to next() or within a loop, execution resumes immediately after the yield statement. Generators provide significant memory benefits through lazy evaluation: instead of allocating memory for an entire list upfront in RAM (O(N) memory), generators compute elements on demand (O(1) memory), making them crucial for processing massive files or data streams."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "py_mid_01",
                "type": "technical",
                "topic": "Concurrency & Python GIL",
                "question": "Explain the Python Global Interpreter Lock (GIL). How does it impact multi-threading vs multi-processing, and how do you choose between threading, multiprocessing, and asyncio for high-throughput applications?",
                "key_concepts": [
                    "GIL is a mutex protecting CPython memory management",
                    "prevents true CPU parallelism in multi-threading",
                    "multiprocessing circumvents GIL using separate process memory",
                    "threading/asyncio ideal for I/O-bound tasks",
                    "multiprocessing suitable for CPU-bound computations"
                ],
                "keywords": ["gil", "global interpreter lock", "multithreading", "multiprocessing", "asyncio", "cpu-bound", "io-bound", "concurrency", "cpython", "process pool"],
                "guidance": "Distinguish CPU-bound from I/O-bound operations and explain why threading in CPython doesn't speed up pure CPU math.",
                "sample_answer": "The Global Interpreter Lock (GIL) is a mutual exclusion lock used by CPython to synchronize thread access to Python objects, preventing race conditions in memory management (specifically reference counting). Because of the GIL, only one native thread can execute Python bytecode at a time, meaning multi-threading cannot achieve true parallel execution on multi-core CPUs for CPU-bound tasks. For CPU-bound workloads (such as image processing or scientific computing), we use 'multiprocessing' to spawn distinct processes, each with its own Python interpreter and GIL. For I/O-bound tasks (like database queries, network APIs, or disk reads), threads release the GIL while waiting on I/O, or better yet, 'asyncio' provides cooperative single-threaded asynchronous concurrency with minimal memory overhead."
            },
            {
                "id": "py_mid_02",
                "type": "technical",
                "topic": "Decorators & Metaprogramming",
                "question": "How do decorators work under the hood in Python? Write a mental outline of a decorator that measures execution time and preserves function metadata using functools.wraps.",
                "key_concepts": [
                    "higher-order functions taking and returning callable",
                    "closure capturing original function reference",
                    "use of *args and **kwargs for flexibility",
                    "functools.wraps preserves docstrings, __name__, and signatures",
                    "decorator syntax syntactic sugar for func = decorator(func)"
                ],
                "keywords": ["decorator", "closure", "higher-order", "wraps", "functools", "args", "kwargs", "metadata", "timing", "callable"],
                "guidance": "Explain closures, returning a wrapper function, forwarding variable arguments, and why functools.wraps is critical for inspection.",
                "sample_answer": "In Python, decorators are higher-order functions that accept a callable (function or method) as an argument, wrap it with additional behavior, and return a new callable. Syntactically, '@decorator' is syntactic sugar for 'func = decorator(func)'. Under the hood, the decorator defines an inner wrapper function that accepts '*args, **kwargs', executes custom logic before/after the wrapped function call, and returns the result. Using '@functools.wraps(func)' on the wrapper is vital because it copies over the original function's metadata (__name__, __doc__, __annotations__, __module__), ensuring introspection, debugging, and documentation tools continue to work correctly."
            },
            {
                "id": "py_mid_03",
                "type": "technical",
                "topic": "API Design & ORM Optimization",
                "question": "When building database-driven APIs in Python (using SQLAlchemy or Django ORM), what is the 'N+1 query problem', and how do you diagnose and eliminate it?",
                "key_concepts": [
                    "N+1 query issue occurs when fetching parent records executes 1 query and fetching children executes N queries in a loop",
                    "diagnosed via SQL query loggers, debug toolbars, or ORM profilers",
                    "solved using eager loading (joinedload, selectinload, select_related, prefetch_related)",
                    "trade-offs between SQL joins and batch WHERE IN queries",
                    "indexing foreign keys and query optimization"
                ],
                "keywords": ["n+1", "orm", "eager loading", "lazy loading", "select_related", "prefetch_related", "joinedload", "sqlalchemy", "query", "sql"],
                "guidance": "Define how lazy-loading relationships in iterations explodes database round-trips and explain exact eager-loading solutions.",
                "sample_answer": "The N+1 query problem occurs when an application executes one query to fetch N parent records, and then executes an additional query for each parent record inside an iteration loop to retrieve related child records, resulting in 1 + N total database roundtrips. This degrades latency severely. We diagnose it using database query logging, APM tools, or ORM debug toolbars that reveal identical repeated queries. To eliminate it, we use eager loading strategies: in Django, 'select_related' performs an SQL JOIN for single-valued relationships (ForeignKey/OneToOne), while 'prefetch_related' executes a separate batch query with 'WHERE id IN (...)' for many-to-many or reverse foreign keys. In SQLAlchemy, we specify 'joinedload()' or 'selectinload()' on the query."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "py_sr_01",
                "type": "technical",
                "topic": "System Scalability & Microservices Architecture",
                "question": "You are designing a high-throughput transaction processing service in Python expected to handle 20,000 requests per second. How would you architect this service to guarantee resilience, horizontal scaling, data consistency, and low latency?",
                "key_concepts": [
                    "stateless service layer with ASGI/FastAPI behind load balancers",
                    "asynchronous message queues (Kafka, RabbitMQ, Celery/Arq) for decoupling",
                    "caching layers (Redis cluster) and read/write database replicas",
                    "database partitioning, sharding, and idempotency keys",
                    "resilience patterns: circuit breakers, rate limiting, and observability (metrics/distributed tracing)"
                ],
                "keywords": ["stateless", "fastapi", "asgi", "kafka", "redis", "sharding", "idempotency", "circuit breaker", "load balancer", "horizontal", "latency", "resilience"],
                "guidance": "Cover load balancing, ASGI async runtimes, event-driven message queuing, caching, database partitioning, and idempotency.",
                "sample_answer": "To handle 20,000 RPS in Python, the architecture must separate synchronous API ingestion from heavy business processing. First, I would build stateless API microservices using an ASGI framework like FastAPI deployed with Uvicorn/Gunicorn workers across Kubernetes pods behind an L7 load balancer. The API validates the request, verifies an idempotency key in Redis, and promptly emits an event into an event streaming broker like Apache Kafka. Background workers consume partitions from Kafka asynchronously. Read-heavy endpoints leverage a distributed Redis cache with cache-aside patterns. The database layer utilizes primary-replica configurations with connection pooling (e.g. PgBouncer) and table partitioning. Resilience is enforced through circuit breakers, token-bucket rate limiting, structured logging, Prometheus metrics, and OpenTelemetry distributed tracing."
            },
            {
                "id": "py_sr_02",
                "type": "technical",
                "topic": "Clean Code, Architecture & Domain Driven Design",
                "question": "How do you apply Hexagonal Architecture (Ports and Adapters) or Clean Architecture in a complex Python project to decouple business logic from external frameworks, databases, and third-party APIs?",
                "key_concepts": [
                    "dependency inversion principle (high-level modules depend on abstractions)",
                    "core domain entities and use cases isolated from frameworks",
                    "ports as abstract interfaces (Python typing.Protocol or ABC)",
                    "adapters as concrete implementations (SQLAlchemy repo, Stripe client, FastAPI routers)",
                    "unit testability with in-memory test doubles without mocking third-party libraries"
                ],
                "keywords": ["hexagonal", "clean architecture", "ports and adapters", "dependency inversion", "protocol", "abc", "domain", "repository", "abstraction", "decoupling"],
                "guidance": "Explain layers, ports (interfaces), adapters (implementations), and the testing advantages of pure domain code.",
                "sample_answer": "Hexagonal Architecture isolates business logic at the center of the application, insulating it from database schemas, web frameworks, and external third-party SDKs. In Python, the domain layer contains pure entities, value objects, and domain services with zero external dependencies. Application services orchestrate use cases. Communication with the outside world happens through 'Ports' - defined as Python abstract base classes or Protocols (e.g., UserRepository, PaymentGateway). 'Adapters' are concrete implementations that plug into these ports, such as a PostgresUserRepository using SQLAlchemy or a StripePaymentAdapter. By relying on Dependency Inversion, the core domain depends only on abstractions. This enables 100% in-memory unit testing without mocking external networks, allows swapping databases or frameworks seamlessly, and enforces clean boundaries across the codebase."
            },
            {
                "id": "py_sr_03",
                "type": "technical",
                "topic": "Python Internals & Memory Optimization",
                "question": "How does CPython manage memory under the hood? Explain reference counting, cyclic garbage collection, generational GC (Gen 0, 1, 2), and practical techniques like __slots__ to optimize memory in production.",
                "key_concepts": [
                    "primary mechanism is reference counting (ob_refcnt)",
                    "cyclic garbage collector detects self-referencing or circular graphs",
                    "generational hypothesis: young objects die quickly, Gen 0, 1, 2 thresholds",
                    "__slots__ avoids creating dynamic __dict__ per instance saving substantial memory",
                    "memory profiling tools (tracemalloc, sys.getsizeof, objgraph)"
                ],
                "keywords": ["reference counting", "garbage collection", "cyclic", "generational", "gen 0", "gen 1", "gen 2", "__slots__", "tracemalloc", "cpython", "memory"],
                "guidance": "Walk through reference counting increment/decrement, why circular references need generational GC, and how __slots__ eliminates dict overhead.",
                "sample_answer": "CPython's memory management employs a two-tier approach. The primary mechanism is reference counting: every Python object header contains 'ob_refcnt'. When references increase or decrease, the count updates; when it drops to zero, memory is freed immediately. However, reference counting alone fails when objects reference each other cyclically (e.g., A -> B -> A). To solve this, CPython includes a cyclic generational garbage collector that inspects container objects (lists, dicts, custom classes). It organizes objects into three generations (Gen 0, 1, 2) based on survival age, running frequent scans on Gen 0 and infrequent scans on Gen 2. In production, defining '__slots__' in high-frequency classes prevents the automatic allocation of a per-instance '__dict__', reducing memory usage by 40-70% for millions of objects. We monitor allocations using Python's 'tracemalloc' module."
            }
        ]
    },
    "Frontend Developer (React / JavaScript)": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "fe_entry_01",
                "type": "technical",
                "topic": "React Hooks & Component Lifecycle",
                "question": "What is the difference between useState and useEffect in React? Explain the dependency array in useEffect and what happens if you omit it.",
                "key_concepts": [
                    "useState manages local reactive component state",
                    "useEffect handles side effects (API calls, subscriptions, DOM manipulation)",
                    "empty dependency array [] runs once on mount",
                    "array with values [dep] runs when dependencies change",
                    "omitted array runs after every single render causing potential infinite loops"
                ],
                "keywords": ["usestate", "useeffect", "dependency array", "side effects", "render", "mount", "cleanup", "re-render", "infinite loop"],
                "guidance": "Differentiate state updates from side effects and detail all three dependency array behaviors.",
                "sample_answer": "In React, useState is used to declare and update local reactive state that triggers a re-render when modified. useEffect is designed to manage side effects, such as data fetching, browser DOM interactions, timers, or subscriptions. The dependency array controls when useEffect re-executes: if empty ([]), the effect runs once after the initial mount and cleans up on unmount; if populated with variables ([data, id]), it re-runs whenever any specified variable changes between renders. If the dependency array is omitted entirely, the effect executes after every single render, which can lead to severe performance degradation or infinite loops if state is modified within the effect."
            },
            {
                "id": "fe_entry_02",
                "type": "technical",
                "topic": "JavaScript Event Loop & Async",
                "question": "Explain the JavaScript Event Loop, the Call Stack, and the difference between Microtasks (Promises) and Macrotasks (setTimeout).",
                "key_concepts": [
                    "Call Stack executes synchronous code frame by frame",
                    "Event Loop coordinates execution of asynchronous tasks",
                    "Microtask queue has higher priority (Promise callbacks, queueMicrotask)",
                    "Macrotask queue has lower priority (setTimeout, setInterval, I/O)",
                    "Microtasks drain completely before the next macrotask executes"
                ],
                "keywords": ["event loop", "call stack", "microtask", "macrotask", "promise", "settimeout", "async", "non-blocking", "queue"],
                "guidance": "Explain how synchronous code clears the call stack first, followed by exhausting all microtasks before picking a macrotask.",
                "sample_answer": "JavaScript is single-threaded and executes code synchronously on the Call Stack. Asynchronous callbacks are handled by the Web APIs environment and placed into task queues. The Event Loop continuously checks if the Call Stack is empty; when it is, it dispatches queued tasks. Tasks are prioritized into Microtasks and Macrotasks. Microtasks (such as Promise .then/catch handlers and mutation observers) have strict priority: the Event Loop will completely drain the microtask queue before picking the next Macrotask (such as setTimeout, setInterval, or requestAnimationFrame). As a result, resolved Promises execute before setTimeout callbacks even if setTimeout has a 0ms delay."
            },
            {
                "id": "fe_entry_03",
                "type": "technical",
                "topic": "CSS Layouts & Responsive Design",
                "question": "What are the primary differences between CSS Flexbox and CSS Grid, and when should you choose one over the other for responsive design?",
                "key_concepts": [
                    "Flexbox is one-dimensional (row OR column layout)",
                    "Grid is two-dimensional (simultaneous rows AND columns)",
                    "Flexbox excels for component-level alignment and content-driven sizing",
                    "Grid excels for full page layouts and strict grid structures",
                    "media queries and responsive CSS units (rem, clamp, fr)"
                ],
                "keywords": ["flexbox", "grid", "one-dimensional", "two-dimensional", "responsive", "layout", "align-items", "justify-content", "grid-template-columns"],
                "guidance": "Clarify 1D vs 2D layout systems and give concrete scenarios for choosing each.",
                "sample_answer": "The core distinction between CSS Flexbox and CSS Grid lies in their dimensionality. Flexbox is a one-dimensional layout system: it arranges elements along a single axis (either horizontally as a row or vertically as a column). It is ideal for component-level structures like navigation bars, button groups, and aligning items of varying content sizes. CSS Grid is a two-dimensional layout system that defines simultaneous rows and columns. It is best suited for complex page layouts, dashboard cards, photo galleries, and overarching application scaffolding where strict alignment in both dimensions is needed."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "fe_mid_01",
                "type": "technical",
                "topic": "React Performance & Re-renders",
                "question": "What causes unnecessary re-renders in React applications, and how do you use React.memo, useMemo, and useCallback to optimize performance without over-optimizing?",
                "key_concepts": [
                    "re-renders triggered by state changes, parent re-renders, or new prop references",
                    "React.memo prevents re-render if props are shallowly equal",
                    "useMemo caches expensive computational results",
                    "useCallback preserves function reference stability between renders",
                    "cost of memoization overhead vs benefits"
                ],
                "keywords": ["re-render", "react.memo", "usememo", "usecallback", "reference equality", "shallow comparison", "props", "profiler", "optimization"],
                "guidance": "Explain reference equality in JavaScript, how anonymous functions break memoization, and when memoization is actually needed.",
                "sample_answer": "In React, a component re-renders whenever its state changes, its parent re-renders, or a context it subscribes to updates. Re-renders often propagate down child trees because newly instantiated objects or functions in the parent create fresh memory references, failing shallow equality checks. React.memo wraps a functional component to skip re-renders if its props have not changed. useCallback stabilizes function reference equality so passing callbacks to memoized children doesn't invalidate React.memo. useMemo caches expensive computation values across renders. However, premature optimization adds code complexity and memory overhead; we use the React DevTools Profiler first to target genuine performance bottlenecks."
            },
            {
                "id": "fe_mid_02",
                "type": "technical",
                "topic": "State Management Architecture",
                "question": "Compare React Context API with dedicated state management libraries (like Redux Toolkit or Zustand). When does Context API become a performance bottleneck?",
                "key_concepts": [
                    "Context API is built for prop drilling avoidance and low-frequency global data",
                    "updating Context triggers re-renders on ALL consuming components",
                    "Zustand/Redux use selector subscriptions to re-render only affected components",
                    "middleware, devtools, and time-travel debugging",
                    "separating server cache (React Query/TanStack) from client UI state"
                ],
                "keywords": ["context api", "zustand", "redux toolkit", "selectors", "re-render", "prop drilling", "react query", "state management", "subscription"],
                "guidance": "Explain how Context updates re-render all consumers regardless of what piece of data changed, and how selectors prevent this.",
                "sample_answer": "React Context is a dependency injection mechanism designed to avoid prop drilling for low-frequency updates like themes, user authentication status, or locale. Its major performance bottleneck is that whenever the context value changes, every single component consuming that context is forced to re-render, even if it only needs an untouched property of the context object. State management libraries like Zustand or Redux Toolkit solve this by implementing atomic or selector-based subscriptions: components subscribe only to specific slices of state, re-rendering only when their selected slice changes. Modern frontend architecture also separates server state (managed via TanStack Query) from client UI state."
            },
            {
                "id": "fe_mid_03",
                "type": "technical",
                "topic": "Web Vitals & Frontend Performance",
                "question": "What are Core Web Vitals (LCP, INP, CLS), and what actionable engineering steps do you take to improve each metric in a production web application?",
                "key_concepts": [
                    "LCP (Largest Contentful Paint) measures loading speed of main visual content",
                    "INP (Interaction to Next Paint) measures page responsiveness to user actions",
                    "CLS (Cumulative Layout Shift) measures visual stability during loading",
                    "improvements for LCP: CDN, image optimization, critical CSS, SSR/PPR",
                    "improvements for INP: breaking long tasks, web workers, requestIdleCallback",
                    "improvements for CLS: explicit width/height dimensions, font-display, avoiding dynamic content injection"
                ],
                "keywords": ["core web vitals", "lcp", "inp", "cls", "largest contentful paint", "cumulative layout shift", "lazy loading", "code splitting", "cdn", "long tasks"],
                "guidance": "Detail each metric, its target threshold, and concrete developer techniques to optimize it.",
                "sample_answer": "Core Web Vitals are Google's standardized metrics for user experience. LCP (Largest Contentful Paint, target <= 2.5s) measures perceived loading speed; we improve it by using image compression (WebP/AVIF), setting explicit fetchpriority='high' on hero images, preloading fonts, and using CDNs and server-side caching. INP (Interaction to Next Paint, target <= 200ms) replaced FID to measure interactive responsiveness throughout the page lifecycle; we optimize it by breaking long JavaScript tasks with scheduler.yield(), offloading CPU-heavy operations to Web Workers, and debounce/throttling event handlers. CLS (Cumulative Layout Shift, target <= 0.1) measures visual stability; we fix it by specifying explicit width/height or aspect-ratio on images and embeds, and avoiding dynamically inserting banners above existing content."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "fe_sr_01",
                "type": "technical",
                "topic": "Microfrontends & Modern Web Architecture",
                "question": "How would you architect a large-scale enterprise application using Microfrontends or Module Federation? Discuss routing, state isolation, shared dependencies, and failure containment.",
                "key_concepts": [
                    "Module Federation allows runtime sharing of remote and host bundles",
                    "routing coordination (shell container vs child micro-apps)",
                    "shared singleton dependencies (React, UI libraries) to avoid bundle bloat",
                    "independent CI/CD deployment pipelines per team",
                    "failure isolation using React error boundaries and fallbacks"
                ],
                "keywords": ["microfrontends", "module federation", "webpack", "vite", "shell", "shared dependencies", "error boundary", "isolation", "ci/cd", "deployment"],
                "guidance": "Address team autonomy, runtime vs build-time federation, shared dependency version management, and error boundaries.",
                "sample_answer": "In an enterprise environment with multiple cross-functional teams, Microfrontends using Webpack or Vite Module Federation provide autonomous development and independent deployment. The architecture consists of a lightweight Host/Shell application responsible for global authentication, navigation, and top-level routing, alongside independent Remote applications for distinct business domains (e.g., Billing, Dashboard, Settings). The Host loads Remotes dynamically at runtime. Shared dependencies (like React, ReactDOM, and design system tokens) are configured as singletons in Module Federation config to prevent downloading multiple framework copies. For resilience, every remote is wrapped in React Error Boundaries so a failure in one micro-app renders a localized fallback without crashing the entire user experience."
            },
            {
                "id": "fe_sr_02",
                "type": "technical",
                "topic": "Frontend Security & Protection",
                "question": "What are the most dangerous security vulnerabilities in modern single-page applications (XSS, CSRF, Clickjacking), and what multi-layered defense strategies do you implement?",
                "key_concepts": [
                    "XSS (Cross-Site Scripting) risks with dangerouslySetInnerHTML, eval, or unescaped inputs",
                    "Content Security Policy (CSP) headers restricting script execution sources",
                    "storing JWT/session tokens in HttpOnly, Secure, SameSite cookies instead of localStorage",
                    "CSRF defense using SameSite=Lax/Strict cookies and anti-CSRF tokens",
                    "sanitization libraries (DOMPurify) and dependency vulnerability scanning"
                ],
                "keywords": ["xss", "csrf", "csp", "content security policy", "httponly", "samesite", "jwt", "dompurify", "sanitization", "vulnerability"],
                "guidance": "Compare token storage in localStorage vs HttpOnly cookies, explain CSP headers, and DOM sanitization.",
                "sample_answer": "The primary frontend vulnerabilities are XSS and CSRF. Cross-Site Scripting (XSS) occurs when malicious JavaScript executes in the user's browser; if sensitive tokens are stored in localStorage, an XSS attack can steal them instantly. Multi-layered defense includes: storing authentication tokens strictly in HttpOnly, Secure, SameSite cookies inaccessible to client scripts; sanitizing user-generated HTML with DOMPurify; and configuring a strict Content Security Policy (CSP) with script-src nonces to block inline script injection. CSRF is mitigated by SameSite=Lax/Strict cookie attributes combined with custom anti-CSRF request headers (e.g., X-CSRF-Token). Finally, we use X-Frame-Options: DENY or CSP frame-ancestors 'none' to prevent Clickjacking."
            }
        ]
    },
    "Backend Developer (API & Microservices)": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "be_entry_01",
                "type": "technical",
                "topic": "RESTful API Principles & HTTP",
                "question": "What are the core principles of RESTful APIs? Explain the difference between HTTP GET, POST, PUT, PATCH, and DELETE, and which ones are idempotent.",
                "key_concepts": [
                    "stateless client-server architecture with resource-based URLs",
                    "GET retrieves resource (safe and idempotent)",
                    "POST creates new resource (neither safe nor idempotent)",
                    "PUT replaces entire resource (idempotent)",
                    "PATCH modifies partial resource (often non-idempotent)",
                    "DELETE removes resource (idempotent)"
                ],
                "keywords": ["rest", "idempotent", "get", "post", "put", "patch", "delete", "stateless", "http status", "resource"],
                "guidance": "Define idempotency clearly and categorize each standard HTTP method accordingly.",
                "sample_answer": "REST is an architectural style based on stateless client-server communication using standard HTTP methods to act on URI resources. Idempotency means making multiple identical requests has the exact same side-effect on the server as making a single request. GET retrieves data, is safe (does not alter state), and is idempotent. POST creates a new subordinate resource and is not idempotent because repeating it creates duplicate entries. PUT completely replaces a resource at a given URI and is idempotent. PATCH applies partial modifications to a resource. DELETE removes a resource; whether called once or five times, the resource remains deleted, making it idempotent."
            },
            {
                "id": "be_entry_02",
                "type": "technical",
                "topic": "SQL vs NoSQL Databases",
                "question": "Compare relational (SQL) and non-relational (NoSQL) databases. When would you choose PostgreSQL over MongoDB for a backend application?",
                "key_concepts": [
                    "SQL databases offer structured schemas, relational joins, and strict ACID compliance",
                    "NoSQL offers flexible document/key-value schemas and horizontal scaling",
                    "PostgreSQL is chosen when data integrity, complex relational transactions, and financial accuracy are required",
                    "MongoDB is chosen for semi-structured data, rapid prototyping, or dynamic schemas",
                    "modern hybrid capabilities (Postgres JSONB)"
                ],
                "keywords": ["sql", "nosql", "postgresql", "mongodb", "acid", "schema", "joins", "normalization", "transactions", "jsonb"],
                "guidance": "Discuss ACID transactions, schema rigidity vs flexibility, and relationship querying.",
                "sample_answer": "Relational databases (SQL, like PostgreSQL) store data in structured tables with predefined schemas and enforce ACID (Atomicity, Consistency, Isolation, Durability) guarantees, making them ideal for relational data requiring complex multi-table JOINs and strict transactional consistency (such as e-commerce orders, banking, or inventory). NoSQL databases (like MongoDB) store semi-structured documents (JSON/BSON) with dynamic schemas, facilitating horizontal scaling and hierarchical data storage. I would choose PostgreSQL whenever data relationships are tightly coupled, data integrity is paramount, or strict schema validation is required. Furthermore, PostgreSQL's JSONB support provides document-store flexibility while retaining relational power."
            },
            {
                "id": "be_entry_03",
                "type": "technical",
                "topic": "Authentication & Password Security",
                "question": "How do you securely store passwords in a backend database? Why is MD5 or SHA-256 alone insufficient, and what should be used instead?",
                "key_concepts": [
                    "passwords must never be stored in plain text or reversible encryption",
                    "MD5 and SHA-256 are fast general-purpose hashing algorithms vulnerable to brute-force and rainbow tables",
                    "use adaptive, slow cryptographic hash functions: bcrypt, Argon2, or PBKDF2",
                    "unique cryptographic salt per password prevents rainbow table lookup",
                    "configurable work factor / cost parameter resists GPU-based attacks"
                ],
                "keywords": ["password", "hashing", "salt", "bcrypt", "argon2", "rainbow table", "sha-256", "brute-force", "work factor", "slow hash"],
                "guidance": "Explain why fast hashes are bad for passwords, the role of random salt, and adaptive algorithms like bcrypt/Argon2.",
                "sample_answer": "Passwords must never be stored in plaintext. Fast cryptographic hash algorithms like MD5, SHA-1, or plain SHA-256 are dangerous for passwords because modern GPUs can compute billions of hashes per second, making brute-force and rainbow table attacks trivial. Instead, passwords must be hashed using adaptive, intentionally slow password-hashing algorithms such as Argon2id or bcrypt. These algorithms automatically incorporate a unique cryptographically secure random salt for every user (nullifying rainbow tables) and support a configurable work factor (cost) that can be tuned higher over time to maintain computational defense against advancing hardware."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "be_mid_01",
                "type": "technical",
                "topic": "Database Indexing & Performance",
                "question": "How do B-Tree indexes work in relational databases? What are the trade-offs of adding indexes, and why might a query planner ignore an index?",
                "key_concepts": [
                    "B-Trees maintain self-balancing sorted trees offering O(log N) lookups",
                    "trade-offs: faster SELECT queries vs slower INSERT/UPDATE/DELETE and disk storage overhead",
                    "composite index leftmost prefix rule",
                    "query planner ignores index when table is very small or sequential scan is cheaper",
                    "functions or wildcards on indexed columns (e.g. WHERE LOWER(name) or LIKE '%abc') prevent index usage"
                ],
                "keywords": ["b-tree", "index", "query planner", "sequential scan", "composite index", "insert overhead", "selectivity", "explain analyze", "trade-off"],
                "guidance": "Explain logarithmic tree searches, write penalty, composite index prefix ordering, and query planner cost models.",
                "sample_answer": "B-Tree indexes organize column values in a balanced, sorted tree structure where leaf nodes point to table disk rows. This reduces search time from O(N) full table scans to O(log N) tree traversals, vastly speeding up equality and range queries. The trade-offs are increased disk space and a write penalty: every INSERT, UPDATE, or DELETE on an indexed table must also update the index trees. The query planner might ignore an index if the table is small enough that a sequential scan is faster, if the index has low cardinality/selectivity (e.g. a boolean flag), or if the query wraps the column in a function (e.g. UPPER(col)) without a functional index, or uses a leading wildcard (LIKE '%text')."
            },
            {
                "id": "be_mid_02",
                "type": "technical",
                "topic": "Distributed Caching & Invalidation",
                "question": "How do you implement caching with Redis in a backend system? Explain Cache-Aside, Write-Through, and Cache Invalidation strategies, as well as Cache Stampede / Thundering Herd.",
                "key_concepts": [
                    "Cache-Aside: application queries cache; on miss, loads from DB and populates cache",
                    "Write-Through: writes update cache and DB simultaneously",
                    "Cache invalidation challenges and TTL (Time to Live) expiration",
                    "Cache stampede: simultaneous concurrent cache misses overloading database",
                    "mitigation: distributed mutex locks, probabilistic early expiration (XFetch), or background refreshes"
                ],
                "keywords": ["redis", "cache-aside", "write-through", "ttl", "invalidation", "cache stampede", "thundering herd", "mutex", "distributed lock"],
                "guidance": "Describe Cache-Aside flow, explain how key expiration can trigger stampedes, and provide concrete locking or probabilistic solutions.",
                "sample_answer": "Redis is commonly implemented using the Cache-Aside pattern: the application first checks Redis for the requested key. On a cache hit, it returns data immediately; on a cache miss, it reads from the primary database, writes the data to Redis with a TTL, and returns it. Write-Through updates both cache and DB synchronously. The hardest part is cache invalidation when underlying records change. A 'Cache Stampede' or 'Thundering Herd' problem occurs when a heavily requested key expires: hundreds of concurrent requests experience a cache miss simultaneously, overwhelming the database with identical queries. We prevent this using distributed mutex locks (Redis SETNX) so only one worker recalculates the cache, or using probabilistic early expiration algorithms (like XFetch)."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "be_sr_01",
                "type": "technical",
                "topic": "Distributed Transactions & Sagas",
                "question": "In a distributed microservices ecosystem, how do you handle transactions that span multiple services without using blocking two-phase commits (2PC)? Explain the Saga pattern.",
                "key_concepts": [
                    "two-phase commit (2PC) suffers from high latency, single point of failure, and locking bottlenecks",
                    "Saga pattern decomposes distributed transactions into a sequence of local transactions",
                    "each local transaction updates its service DB and publishes an event/message",
                    "compensating transactions undo previous steps if a subsequent step fails",
                    "Choreography (event-driven) vs Orchestration (central coordinator)"
                ],
                "keywords": ["saga", "distributed transaction", "compensating transaction", "choreography", "orchestration", "2pc", "eventual consistency", "outbox pattern", "message broker"],
                "guidance": "Contrast 2PC with Saga, detail compensating rollback transactions, and compare Choreography vs Orchestration.",
                "sample_answer": "In distributed microservices, traditional Two-Phase Commit (2PC) is avoided because it requires synchronous distributed locks across services, creating high latency, tight coupling, and vulnerability to network partitions. Instead, we use the Saga pattern, which represents a business transaction as a series of local transactions across services with eventual consistency. Each service executes its local transaction, commits its database, and emits an event to trigger the next step. If a step fails, compensating transactions are executed in reverse order to semantically undo prior actions (e.g. refunding payment if inventory reservation fails). Sagas are implemented via Choreography (services react to domain events via Kafka/RabbitMQ) or Orchestration (a dedicated orchestrator coordinates steps, which is easier to monitor and debug)."
            }
        ]
    },
    "Data Scientist / AI Engineer": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "ds_entry_01",
                "type": "technical",
                "topic": "Machine Learning Fundamentals",
                "question": "Explain the Bias-Variance tradeoff in supervised machine learning. What are underfitting and overfitting, and how do you detect and prevent them?",
                "key_concepts": [
                    "Bias represents erroneous assumptions (simplification error)",
                    "Variance represents sensitivity to small fluctuations in training set (memorization error)",
                    "Underfitting: high bias, low training/validation accuracy",
                    "Overfitting: high variance, high training accuracy but poor validation generalization",
                    "prevention: regularization (L1/L2), cross-validation, pruning, dropout, more data"
                ],
                "keywords": ["bias", "variance", "tradeoff", "underfitting", "overfitting", "regularization", "cross-validation", "generalization", "hyperparameters"],
                "guidance": "Explain how model complexity shifts error from bias to variance, and list practical regularization techniques.",
                "sample_answer": "The Bias-Variance tradeoff is the fundamental balance in machine learning between model simplicity and flexibility. Bias is the error introduced by approximating a real-world problem with an overly simplistic model, leading to underfitting (poor performance on both training and test sets). Variance is the error from sensitivity to training data noise, causing overfitting (the model memorizes training samples, performing exceptionally on training data but poorly on unseen test data). To detect overfitting, we compare training loss against validation loss curves. We prevent overfitting by adding regularization (L1/L2 penalties, dropout in neural nets), employing k-fold cross-validation, simplifying model architectures, early stopping, and collecting more diverse training data."
            },
            {
                "id": "ds_entry_02",
                "type": "technical",
                "topic": "Evaluation Metrics",
                "question": "When evaluating an imbalanced classification model (e.g. fraud detection where 99% of transactions are legitimate), why is accuracy misleading? What metrics should you use instead?",
                "key_concepts": [
                    "accuracy paradox: predicting the majority class yields 99% accuracy while failing to detect fraud",
                    "Precision measures true positives out of all predicted positives (minimizing false alarms)",
                    "Recall/Sensitivity measures true positives caught out of all actual positives (minimizing missed fraud)",
                    "F1-Score provides harmonic mean of Precision and Recall",
                    "ROC-AUC and Precision-Recall (PR) Curves"
                ],
                "keywords": ["accuracy paradox", "imbalanced", "precision", "recall", "f1-score", "roc-auc", "confusion matrix", "false positive", "false negative", "pr-curve"],
                "guidance": "Explain the accuracy paradox, define precision, recall, and PR-AUC, and relate them to business cost of errors.",
                "sample_answer": "Accuracy is misleading on imbalanced datasets due to the accuracy paradox: if 99% of transactions are legitimate, a naive model that predicts 'not fraud' 100% of the time achieves 99% accuracy while catching zero fraudulent transactions. Instead, we evaluate with metrics suited for class imbalance: Precision (True Positives / (True Positives + False Positives)), which measures reliability when predicting fraud; Recall (True Positives / (True Positives + False Negatives)), which measures the percentage of actual fraudulent transactions detected; and the F1-Score, the harmonic mean balancing precision and recall. For threshold tuning, the Area Under the Precision-Recall Curve (PR-AUC) is much more informative than ROC-AUC when positive instances are extremely rare."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "ds_mid_01",
                "type": "technical",
                "topic": "Feature Engineering & Model Drift",
                "question": "What is data drift versus concept drift in production ML pipelines, and how do you monitor, detect, and remediate drift over time?",
                "key_concepts": [
                    "Data drift (covariate shift): distribution of input features P(X) changes over time",
                    "Concept drift: relationship between features and target P(Y|X) changes",
                    "statistical drift tests: Kolmogorov-Smirnov (KS) test, Population Stability Index (PSI), Wasserstein distance",
                    "monitoring tools (Evidently, Whylogs, Great Expectations)",
                    "remediation: automated retraining pipelines, windowed data sampling, feature importance monitoring"
                ],
                "keywords": ["data drift", "concept drift", "covariate shift", "psi", "ks-test", "monitoring", "retraining", "pipeline", "distribution", "evidently"],
                "guidance": "Distinguish P(X) shift from P(Y|X) shift, provide statistical tests, and explain production monitoring pipelines.",
                "sample_answer": "In production ML, models degrade due to distribution shifts. Data drift (covariate shift) occurs when the statistical distribution of input features P(X) changes over time while the underlying conditional relationship P(Y|X) remains constant (e.g. user demographics shifting). Concept drift occurs when the fundamental relationship between input features and the target variable P(Y|X) changes (e.g. consumer purchasing habits transforming due to economic inflation). We detect data drift by calculating statistical distance metrics such as the Kolmogorov-Smirnov test for continuous features, Chi-Square for categorical, and Population Stability Index (PSI). Remediation includes setting automated alerts, collecting fresh labeled ground truth, and executing automated model retraining with rolling window datasets."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "ds_sr_01",
                "type": "technical",
                "topic": "LLM Architecture & Retrieval Augmented Generation (RAG)",
                "question": "How do you architect an enterprise Retrieval-Augmented Generation (RAG) system with low latency and high factual accuracy? Discuss chunking, vector embeddings, hybrid search, and hallucination reduction.",
                "key_concepts": [
                    "document preprocessing and semantic chunking with overlapping windows",
                    "vector embeddings and vector database indexing (HNSW, IVFFlat)",
                    "hybrid search combining sparse BM25 keyword search with dense vector similarity",
                    "re-ranking models (cross-encoders) to refine retrieved context",
                    "guardrails, self-consistency evaluation, and source grounding to eliminate hallucinations"
                ],
                "keywords": ["rag", "retrieval augmented generation", "embeddings", "vector database", "hnsw", "hybrid search", "bm25", "re-ranking", "hallucination", "chunking"],
                "guidance": "Walk through chunking strategies, vector search algorithms, hybrid retrieval, cross-encoder re-ranking, and output verification.",
                "sample_answer": "An enterprise RAG system requires a disciplined multi-stage retrieval and generation pipeline. First, document ingestion utilizes semantic or recursive character chunking with 15-20% overlap, preserving context and metadata. Chunks are converted into dense vector representations and stored in a vector database utilizing HNSW indexing for sub-millisecond approximate nearest neighbor search. To overcome dense vector limitations on exact domain keywords or acronyms, we implement Hybrid Search, combining dense semantic search with sparse lexical search (BM25) via Reciprocal Rank Fusion (RRF). Top candidates are passed through a Cross-Encoder re-ranker to maximize contextual relevance before prompt construction. Finally, we implement prompt grounding with strict citation requirements and automated verification checks to prevent hallucinations."
            }
        ]
    },
    "DevOps & Cloud Infrastructure Engineer": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "ops_entry_01",
                "type": "technical",
                "topic": "Containers & Docker",
                "question": "What is the difference between a Docker image and a Docker container? What are container layers, and how do you write a Dockerfile to minimize image size?",
                "key_concepts": [
                    "image is a read-only immutable blueprint; container is a running instance with writable layer",
                    "images are built in cached, layered union file systems",
                    "multi-stage builds compile artifacts in builder stage and copy only runtime binaries to final stage",
                    "using minimal base images (Alpine, distroless, slim)",
                    "chaining RUN commands and cleaning up package manager caches"
                ],
                "keywords": ["docker", "image", "container", "layers", "multi-stage", "alpine", "distroless", "cache", "dockerfile", "writable"],
                "guidance": "Explain immutable layers, union filesystems, multi-stage builds, and lean base images.",
                "sample_answer": "A Docker image is a read-only, immutable snapshot containing the application code, runtime libraries, and environment dependencies. A Docker container is a runnable, isolated instance of an image that adds a thin read-write layer on top. Each instruction in a Dockerfile creates an immutable filesystem layer that Docker caches. To minimize image size and attack surface, we utilize multi-stage builds: a heavy 'build' stage compiles code and installs dependencies, and only the resulting binary or runtime artifact is copied into a minimal production base image (like Alpine or Distroless). Additionally, we chain commands with '&&' to minimize layer counts and remove package manager caches in the same RUN layer."
            },
            {
                "id": "ops_entry_02",
                "type": "technical",
                "topic": "CI/CD Pipelines",
                "question": "Explain Continuous Integration and Continuous Deployment (CI/CD). What stages belong in a robust production CI/CD pipeline?",
                "key_concepts": [
                    "CI automates merging code and running automated linting, tests, and security scans",
                    "CD automates packaging and deploying validated artifacts to staging/production",
                    "typical stages: Lint & Static Analysis, Unit Tests, Integration Tests, Build & Containerize, Vulnerability Scan, Staging Deploy, Canary/Production Deploy",
                    "rollback mechanisms and secret management in CI"
                ],
                "keywords": ["ci/cd", "continuous integration", "continuous deployment", "pipeline", "linting", "unit tests", "canary", "staging", "automated", "rollback"],
                "guidance": "Walk through each step from git push to production rollout with automated safety gates.",
                "sample_answer": "CI/CD is a software engineering methodology that automates application lifecycle management. Continuous Integration (CI) automatically builds and verifies changes every time a developer commits code, running linters, static code analysis, security vulnerability scanners (SAST), and unit tests to detect regressions early. Continuous Delivery/Deployment (CD) automatically packages validated code into immutable artifacts (e.g. Docker images) and deploys them across target environments. A robust production pipeline includes: 1) Lint & Typecheck, 2) Fast Unit Tests, 3) Container Build & Image Scanning (Trivy), 4) Automated Staging Deployment with End-to-End Smoke Tests, 5) Progressive Production Rollout (Canary or Blue-Green) with automated health checks and instant rollback triggers."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "ops_mid_01",
                "type": "technical",
                "topic": "Kubernetes Architecture",
                "question": "Describe the architecture of Kubernetes. What are the key components of the Control Plane and Worker Nodes, and how does a Pod get scheduled and run?",
                "key_concepts": [
                    "Control plane components: kube-apiserver, etcd, kube-scheduler, kube-controller-manager",
                    "Worker node components: kubelet, kube-proxy, container runtime (containerd)",
                    "etcd stores cluster state as distributed key-value store",
                    "kube-scheduler assigns unscheduled pods to nodes based on resource constraints/affinity",
                    "kubelet receives pod spec from apiserver and instructs container runtime"
                ],
                "keywords": ["kubernetes", "control plane", "kube-apiserver", "etcd", "kube-scheduler", "kubelet", "kube-proxy", "pod", "container runtime", "worker node"],
                "guidance": "Detail both control plane and worker node responsibilities and trace pod creation from API server to kubelet.",
                "sample_answer": "Kubernetes architecture is split into a Control Plane and Worker Nodes. The Control Plane manages cluster state and includes: 'kube-apiserver' (the REST API entry point), 'etcd' (highly available distributed key-value store holding the complete cluster state), 'kube-scheduler' (matches unscheduled pods to nodes based on resource limits and affinity rules), and 'kube-controller-manager' (reconciliation loops ensuring desired state equals actual state). Worker Nodes run actual container workloads and include: 'kubelet' (node agent communicating with apiserver to manage pod lifecycle), 'kube-proxy' (maintains host network rules for Kubernetes Services), and the 'container runtime' (e.g. containerd). When a deployment is submitted, apiserver writes to etcd, the scheduler selects a node, and that node's kubelet instructs containerd to pull the image and run the containers."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "ops_sr_01",
                "type": "technical",
                "topic": "Infrastructure as Code & GitOps",
                "question": "How do you design a GitOps workflow using Terraform and ArgoCD across multiple cloud environments (Dev, Staging, Prod)? Address state management, drift detection, and secret management.",
                "key_concepts": [
                    "Terraform manages cloud infrastructure state with remote state locking (S3/DynamoDB or GCS)",
                    "ArgoCD continuously reconciles desired Git state with actual Kubernetes cluster state",
                    "environment separation using branching or folder hierarchies (Kustomize overlays / Helm)",
                    "drift detection and auto-sync capabilities",
                    "secret management without committing plain text: Vault, External Secrets Operator, or Sealed Secrets"
                ],
                "keywords": ["gitops", "terraform", "argocd", "remote state", "drift detection", "kustomize", "vault", "external secrets", "reconciliation", "infrastructure as code"],
                "guidance": "Explain Git as single source of truth, remote state locking in Terraform, ArgoCD reconciliation loops, and secure secret injection.",
                "sample_answer": "In an enterprise GitOps architecture, Git serves as the single source of truth for both infrastructure and applications. Cloud foundation resources (VPCs, IAM, EKS clusters) are provisioned via Terraform using remote state stored in object storage with distributed locking (e.g., S3 + DynamoDB) to prevent concurrent state corruption. Workloads inside Kubernetes are managed via ArgoCD utilizing Kustomize overlays for Dev, Staging, and Production. ArgoCD runs continuous reconciliation loops: if manual changes cause cluster drift, ArgoCD detects and alerts or automatically re-aligns the cluster to match Git. Secrets are never stored in plaintext Git; we use External Secrets Operator connected to HashiCorp Vault or AWS Secrets Manager to inject secrets into Kubernetes Pods dynamically at runtime."
            }
        ]
    },
    "Product Manager & Technical Lead": {
        "Entry Level (0 - 2 Years)": [
            {
                "id": "pm_entry_01",
                "type": "technical",
                "topic": "Product Discovery & MVP Definition",
                "question": "How do you define a Minimum Viable Product (MVP)? Walk through how you prioritize features using frameworks like MoSCoW or RICE.",
                "key_concepts": [
                    "MVP is smallest product version that validates core hypotheses and delivers user value",
                    "avoiding building full solutions before validating user demand",
                    "RICE framework: Reach, Impact, Confidence, divided by Effort",
                    "MoSCoW: Must have, Should have, Could have, Won't have",
                    "defining clear success metrics (KPIs) before launching"
                ],
                "keywords": ["mvp", "minimum viable product", "rice", "moscow", "prioritization", "hypothesis", "reach", "impact", "effort", "kpi"],
                "guidance": "Define MVP as a learning vehicle, explain the mathematical RICE formula, and emphasize user feedback loops.",
                "sample_answer": "A Minimum Viable Product (MVP) is the simplest possible version of a product that allows a team to collect the maximum amount of validated learning about customers with the least effort. It is not a broken product, but a focused solution solving one core user pain point. To prioritize features, I utilize the RICE scoring model: (Reach x Impact x Confidence) / Effort. Reach estimates affected users per month, Impact gauges degree of benefit (0.25 to 3), Confidence (percentage) reflects evidence strength, and Effort measures person-weeks required. Features with the highest RICE scores take priority. Alternatively, MoSCoW (Must, Should, Could, Won't) helps align stakeholders on release scope boundaries."
            }
        ],
        "Mid Level (3 - 5 Years)": [
            {
                "id": "pm_mid_01",
                "type": "technical",
                "topic": "Product Analytics & A/B Testing",
                "question": "How do you design, run, and evaluate an A/B test for a major product feature? How do you ensure statistical significance and avoid common pitfalls?",
                "key_concepts": [
                    "formulate clear null hypothesis and alternative hypothesis",
                    "define primary conversion metric and guardrail metrics",
                    "calculate sample size and test duration upfront based on statistical power (80%) and alpha (0.05)",
                    "avoid peeking at results prematurely to avoid false positive inflation",
                    "interpreting p-values and confidence intervals"
                ],
                "keywords": ["a/b test", "hypothesis", "statistical significance", "p-value", "sample size", "guardrail metrics", "conversion", "power", "variant", "control"],
                "guidance": "Walk through hypothesis formulation, pre-experiment sample size calculations, guardrail metrics, and peeking bias.",
                "sample_answer": "Designing an A/B test begins with a testable hypothesis: e.g., 'Simplifying checkout from 3 steps to 1 will increase completed purchases by 5%'. First, I define a primary metric (conversion rate) and guardrail metrics (refund rate, customer support tickets) to ensure we don't harm user trust. Second, I calculate the required sample size and experiment duration in advance based on minimum detectable effect (MDE), 80% statistical power, and 5% alpha. During the test, randomized traffic splits evenly between Control and Variant. A critical pitfall is 'peeking' - checking p-values continuously and stopping early, which spikes false positives. I evaluate results only after the calculated sample size is reached, confirming statistical significance before full rollout."
            }
        ],
        "Senior / Staff Level (5+ Years)": [
            {
                "id": "pm_sr_01",
                "type": "technical",
                "topic": "Technical Debt vs Feature Velocity",
                "question": "As a Technical Lead or Senior Product Manager, how do you balance stakeholder pressure for new business features against mounting technical debt and engineering refactoring?",
                "key_concepts": [
                    "translating technical debt into business impact (risk of downtime, slowed velocity, customer churn)",
                    "allocating dedicated engineering capacity (e.g. 20% rule) per sprint for debt reduction",
                    "debt categorization: deliberate vs accidental, prudent vs reckless (Martin Fowler debt quadrant)",
                    "opportunistic refactoring: improving code as part of feature delivery ('Boy Scout Rule')",
                    "transparent tracking on engineering roadmap alongside feature backlog"
                ],
                "keywords": ["technical debt", "stakeholders", "refactoring", "velocity", "business impact", "allocation", "roadmap", "risk", "boy scout rule", "trade-off"],
                "guidance": "Discuss communication in terms of risk and velocity rather than technical jargon, sprint allocations, and refactoring hygiene.",
                "sample_answer": "Balancing technical debt and feature velocity requires translating engineering health into business outcomes. Executives don't care about clean code for its own sake, but they care deeply about platform stability, security vulnerabilities, and developer velocity slowing down future revenue. I categorize debt using Martin Fowler's Technical Debt Quadrant to isolate high-risk architectural bottlenecks. Operationally, I negotiate a standing 20% engineering capacity allocation per sprint dedicated exclusively to technical maintenance, infrastructure modernization, and refactoring. For larger refactors, we align them directly with strategic feature initiatives using the 'Boy Scout Rule' (leave code cleaner than you found it). By tracking technical debt transparently on our roadmap with measured velocity impacts, debt remediation becomes a recognized business enabler."
            }
        ]
    }
}

# HR & Behavioral Questions (STAR Method: Situation, Task, Action, Result)
# Applicable across all technical roles and levels
BEHAVIORAL_QUESTION_BANK = [
    {
        "id": "hr_behavioral_01",
        "type": "behavioral",
        "topic": "Conflict Resolution & Collaboration",
        "question": "Tell me about a time when you strongly disagreed with a team member or technical lead regarding an architectural decision or project direction. How did you handle the situation and what was the outcome?",
        "key_concepts": [
            "Situation: clear professional disagreement context",
            "Task: goal of delivering the best technical solution for the team",
            "Action: respectful communication, data/benchmarking over emotion, finding common ground",
            "Result: positive technical outcome, consensus, or committing to the decision professionally",
            "use of STAR structured framework"
        ],
        "keywords": ["disagreement", "star", "situation", "task", "action", "result", "data", "compromise", "communication", "collaborate", "consensus", "outcome"],
        "guidance": "Follow the STAR framework. Focus on objective facts, data-driven reasoning, professional diplomacy, and shared team goals.",
        "sample_answer": "Situation: At my previous company, my lead proposed building a custom caching layer in memory, whereas I advocated for using an established Redis cluster due to horizontal scaling requirements.\nTask: My responsibility was to ensure our caching strategy would remain reliable under upcoming black-Friday traffic without creating maintenance overhead.\nAction: Instead of debating opinions, I built a prototype benchmark comparing both approaches under simulated network load and multi-node failover scenarios. I scheduled a 30-minute review and presented the benchmark data objectively, acknowledging the lead's concern regarding external service dependencies while showing that Redis offered built-in replication that our custom solution lacked.\nResult: The lead appreciated the data-driven demonstration and agreed to adopt Redis with managed failover. The deployment processed over 10M requests with zero cache-related incidents, and our working relationship grew significantly stronger."
    },
    {
        "id": "hr_behavioral_02",
        "type": "behavioral",
        "topic": "Failure, Accountability & Growth",
        "question": "Describe a major mistake or production outage you caused or were directly involved in. What happened, how did you respond in the moment, and what systemic safeguards did you implement afterward?",
        "key_concepts": [
            "Situation: candid description of a real production failure or defect",
            "Task: urgent need to mitigate damage and restore user service",
            "Action: transparent ownership, communication to stakeholders, root-cause investigation without blame",
            "Result: post-mortem analysis, automated test/safeguard implementation, zero recurrence",
            "blameless culture and personal accountability"
        ],
        "keywords": ["mistake", "outage", "production", "post-mortem", "blameless", "root cause", "ownership", "monitoring", "rollback", "safeguard", "star"],
        "guidance": "Demonstrate absolute ownership without shifting blame. Highlight fast incident communication, blameless post-mortem, and lasting preventive automation.",
        "sample_answer": "Situation: Early in my career, I deployed a database migration script that accidentally executed a blocking lock on our primary users table, rendering customer authentication unavailable for 18 minutes.\nTask: I immediately recognized the incident and needed to restore user login availability and prevent customer data corruption.\nAction: I took full ownership on our incident channel immediately rather than hiding the cause, rolled back the migration, and coordinated with DevOps to terminate stalled database connections. Once production stabilized, I led a blameless post-mortem analyzing why our CI pipeline allowed an unindexed alter table statement to run during peak hours.\nResult: To ensure this could never happen again, I added automated migration linting to our GitHub Actions pipeline (preventing blocking DDL commands) and instituted a zero-downtime migration policy using blue-green database rollout patterns. The issue never recurred."
    },
    {
        "id": "hr_behavioral_03",
        "type": "behavioral",
        "topic": "Prioritization Under High Pressure & Tight Deadlines",
        "question": "Give an example of a project where project requirements changed drastically close to a critical deadline. How did you prioritize tasks, manage stakeholder expectations, and deliver results?",
        "key_concepts": [
            "Situation: high-stakes project with sudden scope change or tight timeline",
            "Task: balancing scope, quality, and delivery date",
            "Action: ruthless scope prioritization, transparent stakeholder negotiation, team focus",
            "Result: on-time delivery of essential value, phased roadmap for remaining items",
            "calm leadership and proactive communication"
        ],
        "keywords": ["deadline", "priority", "stakeholders", "scope", "trade-off", "communication", "delivery", "phased", "agile", "pressure", "star"],
        "guidance": "Use STAR. Emphasize transparent trade-off discussions (Iron Triangle: scope, time, budget) and proactive stakeholder alignment.",
        "sample_answer": "Situation: Two weeks before a major enterprise client launch, regulatory compliance required us to add multi-factor authentication (MFA) and audit trail logging that were not in the original scope.\nTask: We could not move the launch date due to client contracts, but shoehorning all features risked introducing severe software defects.\nAction: I immediately convened a meeting with the Product Manager and Tech Lead. We mapped out an emergency MoSCoW prioritization: MFA and audit logging were classified as non-negotiable Must-Haves, while optional reporting dashboards and CSV exports were deferred to Phase 2. I communicated this trade-off clearly to the client success team with a transparent revised timeline.\nResult: The team stayed focused on core security requirements, delivered a bug-free launch on the promised date, and shipped the secondary features two sprints later with zero customer dissatisfaction."
    },
    {
        "id": "hr_behavioral_04",
        "type": "behavioral",
        "topic": "Leadership, Mentorship & Knowledge Sharing",
        "question": "Can you share an experience where you mentored a junior engineer or helped a struggling teammate improve their technical performance and engineering confidence?",
        "key_concepts": [
            "Situation: identifying a teammate struggling with onboarding, code quality, or confidence",
            "Task: providing structured support without taking over their work",
            "Action: pair programming, constructive code reviews, psychological safety, growth goals",
            "Result: mentee became autonomous, contributed independently, improved team throughput",
            "empathy and supportive leadership"
        ],
        "keywords": ["mentorship", "junior", "pair programming", "code review", "guidance", "confidence", "growth", "autonomy", "empathy", "feedback", "star"],
        "guidance": "Demonstrate empathy, patience, and structured mentorship methods (e.g. asking guiding questions rather than writing code for them).",
        "sample_answer": "Situation: A junior developer joined our team and struggled during their first month with our distributed architecture and pull request reviews, becoming hesitant to pick up complex tickets.\nTask: I wanted to help them build technical competence and psychological safety so they could contribute autonomously.\nAction: I initiated 30-minute bi-weekly 1-on-1 check-ins and dedicated an hour twice a week for collaborative pair programming. Rather than writing code for them, I used the Socratic method, asking questions that guided them to deduce solutions themselves. In code reviews, I balanced critiques with positive praise and linked to architectural RFCs explaining the 'why' behind design patterns.\nResult: Within three months, the developer's pull request approval speed doubled, their bug rate dropped substantially, and they independently designed and delivered our new notification service ahead of schedule."
    }
]

