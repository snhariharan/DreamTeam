"""
Frontend Framework Skill Packs
-------------------------------
Gives an agent deep expertise in React and Angular ecosystems.

REACT   — React 19, Next.js App Router, React Query, Zustand, Vitest
ANGULAR — Angular 18+, RxJS, NgRx, Angular Material, Jest

Best for: Senior Developer, QA Automation Engineer, Solution Architect
"""
from crewai_tools import ScrapeWebsiteTool

from skills.packs import SkillPack


# ── React ─────────────────────────────────────────────────────────────────

def _react_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://react.dev/learn"),
        ScrapeWebsiteTool(website_url="https://react.dev/reference/react"),
        ScrapeWebsiteTool(website_url="https://nextjs.org/docs"),
        ScrapeWebsiteTool(website_url="https://tanstack.com/query/latest/docs/framework/react/overview"),
        ScrapeWebsiteTool(website_url="https://zustand-demo.pmnd.rs/"),
        ScrapeWebsiteTool(website_url="https://vitest.dev/guide/"),
        ScrapeWebsiteTool(website_url="https://testing-library.com/docs/react-testing-library/intro/"),
        ScrapeWebsiteTool(website_url="https://storybook.js.org/docs"),
    ]


REACT = SkillPack(
    name="react",
    description=(
        "React 19, Next.js App Router, React Query (TanStack), Zustand, "
        "Vitest, React Testing Library, Storybook."
    ),
    tools_factory=_react_tools,
    backstory_addendum=(
        "You are a React expert working with React 19's new features: the "
        "compiler, server components, server actions, use() hook, and "
        "concurrent rendering primitives (Suspense, useTransition). You build "
        "production Next.js applications using the App Router with server-side "
        "rendering, static generation, streaming, and route handlers. You manage "
        "server state with TanStack Query (caching, optimistic updates, "
        "prefetching) and client state with Zustand (no unnecessary Redux). "
        "You write components with TypeScript strict mode, co-locate tests with "
        "Vitest and React Testing Library (test behaviour, not implementation), "
        "and document components in Storybook. You enforce accessibility (ARIA "
        "roles, keyboard navigation, colour contrast), optimise Core Web Vitals "
        "(LCP, INP, CLS), and use code splitting with React.lazy / dynamic imports. "
        "You always sanitise user input to prevent XSS, avoid dangerouslySetInnerHTML, "
        "and use Content Security Policy headers."
    ),
    goal_addendum=(
        "Build React 19 / Next.js App Router UIs with TypeScript, TanStack Query, "
        "Zustand, accessible components, and Vitest tests."
    ),
)


# ── Angular ───────────────────────────────────────────────────────────────

def _angular_tools() -> list:
    return [
        ScrapeWebsiteTool(website_url="https://angular.dev/overview"),
        ScrapeWebsiteTool(website_url="https://angular.dev/guide/components"),
        ScrapeWebsiteTool(website_url="https://rxjs.dev/guide/overview"),
        ScrapeWebsiteTool(website_url="https://ngrx.io/docs"),
        ScrapeWebsiteTool(website_url="https://material.angular.io/components/categories"),
        ScrapeWebsiteTool(website_url="https://angular.dev/guide/testing"),
        ScrapeWebsiteTool(website_url="https://nx.dev/getting-started/intro"),
    ]


ANGULAR = SkillPack(
    name="angular",
    description=(
        "Angular 18+, standalone components, signals, RxJS, NgRx, "
        "Angular Material, Jest, Nx monorepo."
    ),
    tools_factory=_angular_tools,
    backstory_addendum=(
        "You are an Angular architect with deep expertise in Angular 18+ features: "
        "standalone components (no NgModules), signals and signal-based inputs "
        "as the modern reactivity primitive, control flow syntax (@if, @for, "
        "@switch), and deferrable views (@defer) for lazy loading. You compose "
        "complex async workflows with RxJS operators (switchMap, mergeMap, "
        "shareReplay, combineLatest) and manage global state with NgRx "
        "(actions, reducers, effects, selectors, component store). You build "
        "enterprise UI with Angular Material / CDK following ARIA standards. "
        "You structure large applications as Nx monorepos with proper lib "
        "boundaries enforced by module federation. You write Karma-free unit "
        "tests with Jest and component tests with Angular Testing Library. "
        "You apply strict TypeScript, enforce lint rules with ESLint + "
        "angular-eslint, and use the Angular CLI for builds, AOT compilation, "
        "and differential loading."
    ),
    goal_addendum=(
        "Build Angular 18+ apps with standalone components, signals, RxJS, "
        "NgRx state management, Angular Material UI, and Jest tests."
    ),
)
