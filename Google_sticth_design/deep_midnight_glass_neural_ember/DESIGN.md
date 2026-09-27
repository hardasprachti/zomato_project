---
name: Deep Midnight Glass & Neural Ember
colors:
  surface: '#131318'
  surface-dim: '#131318'
  surface-bright: '#39383e'
  surface-container-lowest: '#0e0e13'
  surface-container-low: '#1b1b20'
  surface-container: '#1f1f25'
  surface-container-high: '#2a292f'
  surface-container-highest: '#35343a'
  on-surface: '#e4e1e9'
  on-surface-variant: '#e1bfb5'
  inverse-surface: '#e4e1e9'
  inverse-on-surface: '#303036'
  outline: '#a98a80'
  outline-variant: '#594139'
  surface-tint: '#ffb59d'
  primary: '#ffb59d'
  on-primary: '#5d1900'
  primary-container: '#ff6b35'
  on-primary-container: '#5f1900'
  inverse-primary: '#ab3500'
  secondary: '#ddb7ff'
  on-secondary: '#490080'
  secondary-container: '#6f00be'
  on-secondary-container: '#d6a9ff'
  tertiary: '#4ae176'
  on-tertiary: '#003915'
  tertiary-container: '#00b150'
  on-tertiary-container: '#003a16'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#ffdbd0'
  primary-fixed-dim: '#ffb59d'
  on-primary-fixed: '#390c00'
  on-primary-fixed-variant: '#832600'
  secondary-fixed: '#f0dbff'
  secondary-fixed-dim: '#ddb7ff'
  on-secondary-fixed: '#2c0051'
  on-secondary-fixed-variant: '#6900b3'
  tertiary-fixed: '#6bff8f'
  tertiary-fixed-dim: '#4ae176'
  on-tertiary-fixed: '#002109'
  on-tertiary-fixed-variant: '#005321'
  background: '#131318'
  on-background: '#e4e1e9'
  surface-variant: '#35343a'
typography:
  display-hero:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '800'
    lineHeight: 56px
    letterSpacing: -0.03em
  display-hero-mobile:
    fontFamily: Inter
    fontSize: 34px
    fontWeight: '800'
    lineHeight: 42px
    letterSpacing: -0.025em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 26px
    fontWeight: '700'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-caps:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '700'
    lineHeight: 16px
    letterSpacing: 0.08em
  label-bold:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '600'
    lineHeight: 18px
    letterSpacing: 0.02em
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-mobile: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system blends deep-space midnight dark mode with futuristic glassmorphism and radiant neural glow accents. Crafted for an intelligent culinary discovery platform, the interface merges the warmth and craving of gastronomy with the precision of generative artificial intelligence.

The experience evokes culinary anticipation, algorithmic intelligence, and effortless luxury:
- **Atmospheric & Immersive:** The interface recedes into an obsidian field, allowing rich food photography and AI highlights to stand out without cognitive fatigue.
- **Glassmorphic Precision:** Layered frosted surfaces, subtle edge-refractions, and high-diffusion backdrops create a layered spatial depth reminiscent of modern heads-up displays.
- **Electric Culinary Energy:** Searing culinary amber-orange represents flavor, appetite, and human warmth, countered by vibrant synaptic violet to denote deep intelligence, reasoning, and real-time generation.
- **Target Audience:** Modern food enthusiasts, tech-forward diners, urban culinary explorers, and users seeking taste matchmaking powered by natural language prompts.

## Colors

The palette is engineered specifically for OLED depth, edge contrast, and low light readability:

### Base Surfaces
- **Canvas Base (`#0A0A0F`):** Deep near-black with a subtle indigo undertone, grounding the entire viewport.
- **Surface Elevation (`#12121A`):** Opaque raised container tone, used for primary feed cards, drawers, and modal backdrops.
- **Glass Panel Surface (`rgba(255, 255, 255, 0.04)`):** Translucent frosted layer with `backdrop-filter: blur(16px)` and delicate edge reflections.
- **Subtle Surface Border (`rgba(255, 255, 255, 0.06)`):** Structural hairline divider preserving form boundaries across zero-light backgrounds.
- **Glass Edge Highlight (`rgba(255, 255, 255, 0.12)`):** High-tier refraction border applied to active interactive elements and floating search surfaces.

### Core Accents
- **Culinary Flame (`#FF6B35`):** Primary action color. Ignites appetite, used for booking conversions, primary CTAs, active ratings, and food emphasis.
- **Synaptic Violet (`#A855F7`):** Secondary AI accent. Signifies generative synthesis, semantic matchmaking, model reasoning, and prompt triggers.
- **Neural Gradient:** `linear-gradient(135deg, #FF6B35 0%, #A855F7 100%)` used strictly for the highest-value AI discovery highlights, match score rings, and active query glows.

### Text & Feedback
- **Text Primary (`#F4F4F5`):** Near-white neutral with zinc undertones, anti-aliased for extreme readability.
- **Text Secondary (`#A1A1AA`):** Medium neutral for card descriptions, metadata, and conversational responses.
- **Text Muted (`#71717A`):** Low-contrast zinc for timestamps, disabled states, unselected tabs, and placeholder strings.
- **Success (`#22C55E`):** Dietary match confirmations, open now statuses, high compatibility scores.
- **Warning (`#F59E0B`):** Surge demand, waitlist warnings, limited seating notices.
- **Error (`#EF4444`):** Allergen conflict alerts, closed venues, connectivity errors.

## Typography

The typographic hierarchy prioritizes rapid optical scanning, modern technical confidence, and crisp contrast across obsidian backgrounds.

- **Weight Variance:** Heavy weights (`700` and `800`) are used for headlines and numbers (ratings, distances, match percentages) to establish immediate hierarchy against translucent backdrops.
- **Negative Tracking:** Headings use tight letter-spacing (`-0.01em` to `-0.03em`) to impart an editorial, tech-forward tone.
- **Uppercase Tracking:** Micro-labels, metadata categories, and pill badges leverage `label-caps` with wide letter-spacing (`+0.08em`) to remain sharp and legible at minute scales.
- **Code & Reasoning Spec:** AI prompt execution traces and raw system parameter tags use a secondary monospace (`JetBrains Mono`) to separate user input context from algorithmic inference output.

## Layout & Spacing

The layout is built on a responsive 12-column grid for desktop views, converting down to an 8-column layout on tablets and a 4-column layout on mobile viewports.

### Breakpoints & Fluid Adaptation
- **Mobile (< 768px):** 4 columns, outer canvas margins at `1rem` (`16px`), gutter spacing at `1rem` (`16px`). Bottom-docked translucent navigation and full-width floating search bars.
- **Tablet (768px - 1024px):** 8 columns, margins at `1.5rem` (`24px`), gutter spacing at `1.25rem` (`20px`). Side-by-side feed and contextual preview panels.
- **Desktop (> 1024px):** 12 columns, max-width constrained to `1440px` centered with auto-margins, gutter spacing at `1.5rem` (`24px`). Triple-pane architecture: contextual filters & prompt rail (3 cols), dynamic card stream (6 cols), and persistent interactive AI drawer (3 cols).

### Vertical Rhythm
Structural sections maintain an open, uncluttered breathing room with `space-xl` gaps, while inner component clusters (chips, metric badges, title-to-description offsets) adhere to strict `space-xs` (4px) and `space-sm` (8px) relationships.

## Elevation & Depth

Spatial layering relies on a combination of optical glassmorphism, multi-stop diffusion shadows, and neural radial glows.

### Spatial Elevation Tiers
1. **Level 0 (Canvas):** Pure `#0A0A0F` base with ambient radial gradient spotlights (`radial-gradient(circle at top right, rgba(168, 85, 247, 0.08), transparent 45%)`).
2. **Level 1 (Structural Cards & Surfaces):** `#12121A` with a 1px uniform perimeter border of `rgba(255, 255, 255, 0.06)`. Flat depth, zero cast shadow.
3. **Level 2 (Glass Overlays & Interactive Surfaces):** `background: rgba(255, 255, 255, 0.04)`, `backdrop-filter: blur(16px) saturate(180%)`, encased with a 1px border of `rgba(255, 255, 255, 0.08)`. Shadows: `0 8px 32px -4px rgba(0, 0, 0, 0.5)`.
4. **Level 3 (Floating Navbars, Modal Drawers, Active Prompts):** Enhanced frosted glass with top-edge highlight (`border-top: 1px solid rgba(255, 255, 255, 0.15)`), inner glow shadow (`inset 0 1px 0 rgba(255, 255, 255, 0.1)`), and external shadow `0 20px 48px -8px rgba(0, 0, 0, 0.75)`.

### Chromatic Light Emissions
- **Primary Pulse Glow:** Actionable hot-states emit an orange drop glow: `box-shadow: 0 0 24px 0 rgba(255, 107, 53, 0.35)`.
- **Neural Reasoning Glow:** AI-recommended entities emit an ambient violet contour: `box-shadow: 0 0 32px -6px rgba(168, 85, 247, 0.28)`.

## Shapes

The geometric architecture balances modern ergonomics with high-tech software precision:

- **Base Radius (`0.5rem` / `8px`):** Applied to internal controls, micro-cards, form inputs, and syntax code blocks.
- **Card & Surface Radius (`1rem` / `16px`):** Standard outer geometry for restaurant cards, glass response containers, and floating filter bar wrappers.
- **Panel & Modal Radius (`1.5rem` / `24px`):** Top corners for mobile bottom drawers, desktop AI panels, and image spotlight frames.
- **Full Pill (`9999px`):** Reserved for interactive filter tags, AI confidence indicators, status badges, and primary action buttons.

## Components

### Buttons
- **Primary AI Action:** Filled with `#FF6B35` or neural gradient (`#FF6B35` to `#A855F7`), text `#F4F4F5`, `font-weight: 600`, pill-shaped (`rounded-full`). On hover, scales by `1.02` with an ambient glow of `0 0 24px rgba(255, 107, 53, 0.4)`.
- **Secondary Glass Action:** Translucent background (`rgba(255, 255, 255, 0.06)`), 1px border (`rgba(255, 255, 255, 0.1)`), pill-shaped. On hover, background shifts to `rgba(255, 255, 255, 0.1)` with pure white text.
- **Ghost Action:** No border, text `#A1A1AA`, hover text `#F4F4F5` with subtle violet text-shadow.

### Glassmorphic Search Bar
- **Construction:** Full-width floating pill with `rgba(255, 255, 255, 0.05)` backdrop blur (16px), 1px perimeter border of `rgba(255, 255, 255, 0.1)`.
- **Leading Indicator:** Pulsing sparkle glyph in `#A855F7`.
- **Input Styling:** Seamless zero-background text input, placeholder `#71717A`, cursor `#FF6B35`.
- **Trailing Shortcuts:** Monospace keyboard shortcut pill (`⌘K`) in `rgba(255, 255, 255, 0.08)` and audio/voice prompt trigger button.

### Filter & Category Pill Tags
- **Default State:** Pill shape (`9999px`), padding `6px 14px`, surface `rgba(255, 255, 255, 0.04)`, border `rgba(255, 255, 255, 0.08)`, text `#A1A1AA`, `label-bold`.
- **Active / Selected State:** Surface `rgba(255, 107, 53, 0.12)`, border `#FF6B35`, text `#FF6B35`, soft orange drop glow.
- **AI Suggested State:** Border `rgba(168, 85, 247, 0.4)` with an animated shifting border gradient and micro-sparkle prefix icon.

### Restaurant Cards
- **Base:** `#12121A` solid structure with `1rem` radius, 1px border `rgba(255, 255, 255, 0.06)`, overflow hidden.
- **Media Header:** 16:9 ratio photo overlayed with a bottom gradient (`linear-gradient(to top, #12121A, transparent)`).
- **Match Quotient Pill:** Floating glass pill at the top right: `rgba(10, 10, 15, 0.7)` with `backdrop-filter: blur(8px)`, displaying a dynamic AI match score (e.g., `98% Match`) styled with `#22C55E` or `#A855F7`.
- **Content:** Headline-sm venue title, zinc cuisine tags, price tier (`$$$$`), real-time walking distance, and a glass divider leading into the AI takeaway.
- **AI Synthesis Snippet:** A frosted micro-panel at the card's base featuring a violet quote marker and a 1-sentence personalized synthesis (e.g., *"Matches your craving for spicy noodles with quiet patio seating."*).

### AI Markdown Response Panel
- **Container:** Frosted glass panel with `backdrop-filter: blur(20px)`, top-edge refraction highlight, padding `1.5rem`.
- **Typography:** `body-md` in `#F4F4F5` with generous 1.7 line height. Unordered lists render with `#FF6B35` glowing bullet points. Emphasized phrases receive subtle `#A855F7` highlighting.
- **Interactive Mentions:** Inline restaurant or dish references render as interactive pill chips that expand micro-cards on hover.

### Syntax-Highlighted Prompt Preview Drawer
- **Drawer Exterior:** Docked or sliding lateral sheet, `#12121A` background, left border `1px solid rgba(255, 255, 255, 0.08)`.
- **Code Container:** `#0A0A0F` inset well with `0.5rem` radius, 1px border `rgba(255, 255, 255, 0.05)`, padding `1rem`.
- **Syntax Tokens:** Monospaced (`JetBrains Mono`). System parameters in `#71717A`, user context variables in `#FF6B35`, model instructions and weights in `#A855F7`, status returns in `#22C55E`.

### Form Controls (Checkboxes, Switches, Radios)
- **Checkbox/Radio:** Base `rgba(255, 255, 255, 0.06)`, border `1px solid rgba(255, 255, 255, 0.2)`. Checked state fills `#FF6B35` with white checkmark.
- **AI Smart Switch:** Track toggles between `rgba(255, 255, 255, 0.08)` and active violet glow (`#A855F7`), with a glowing white pill thumb.