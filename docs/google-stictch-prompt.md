Design a dark-theme, component-based web frontend for an AI-Powered Restaurant 
Recommendation System (similar to Zomato). The UI is a single-page application 
with a clean, premium, glassmorphism-inspired dark aesthetic.

---

🎨 DESIGN SYSTEM

Theme: Deep dark mode
- Background: #0A0A0F (near-black with a blue undertone)
- Surface cards: #12121A with 1px border rgba(255,255,255,0.06)
- Glass panels: backdrop-filter: blur(16px), bg rgba(255,255,255,0.04)
- Primary accent: #FF6B35 (warm orange, food-inspired)
- Secondary accent: #A855F7 (violet/purple for AI elements)
- Text primary: #F4F4F5
- Text muted: #71717A
- Success: #22C55E | Warning: #F59E0B | Error: #EF4444
- Border subtle: rgba(255,255,255,0.08)
- Glow effects: box-shadow using accent colors at low opacity

Typography:
- Font: Inter (Google Fonts)
- Headings: font-weight 700, letter-spacing -0.02em
- Body: font-weight 400, line-height 1.6
- Labels/badges: font-weight 600, uppercase, tracking-wide

---

🧩 COMPONENTS TO DESIGN

1. **AppShell / Layout**
   - Top navbar: logo left ("FoodAI"), nav links center, dark badge "Powered by Gemini" right
   - Subtle gradient top border (orange → purple)
   - Left sidebar (collapsible) showing filter history

2. **HeroSearchBar** (main input component)
   - Full-width pill-shaped search input, glowing orange border on focus
   - Placeholder: "Describe what you're craving... e.g. spicy biryani under ₹300 near Koramangala"
   - Inside the bar: cuisine tag chips, a budget slider button, and a location pin icon
   - Below: animated typing suggestion text ("Try: vegetarian pasta, outdoor seating...")
   - "Find Restaurants" CTA button with gradient (orange → amber) and shimmer animation on hover

3. **FilterPanel** (sidebar or modal)
   - Section: Cuisine Type — multi-select pill toggles (Indian, Chinese, Italian, etc.)
   - Section: Budget — dual-handle range slider with ₹ labels
   - Section: Rating — star rating filter (minimum stars)
   - Section: Location — text input with city autocomplete
   - Section: Dining Options — toggle chips (Delivery, Dine-in, Takeaway)
   - "Apply Filters" button | "Reset All" ghost button
   - Glass card container with subtle purple glow

4. **AIPromptDisplay** (shows the constructed LLM prompt)
   - Collapsible card titled "🤖 AI Prompt Preview"
   - Dark code-block style content with syntax highlighting
   - Animated purple left border glow
   - Copy-to-clipboard icon button

5. **RestaurantCard** (result item)
   - Dark glass card (hover: lift + orange glow border)
   - Left: restaurant image (rounded-lg, 120x120)
   - Right: name (bold), cuisine tags (colored pill badges), rating stars (filled/empty)
   - Second row: price range (₹₹ notation), distance, delivery time
   - AI Reason chip at bottom: purple bg, italic text "Why we picked this..."
   - Heart/save icon (top-right, animates on click)
   - "View Details" ghost button

6. **ResultsGrid**
   - 3-column responsive grid of RestaurantCards
   - Top bar: "X restaurants found" | Sort dropdown (relevance, rating, price)
   - Loading skeleton: pulsing dark shimmer cards
   - Empty state: illustration + "No matches — try adjusting your filters"

7. **AIResponsePanel** (LLM narrative output)
   - Full-width card below results
   - Header: sparkle ✨ icon + "AI Recommendation Summary"
   - Streaming text display (typewriter animation, character by character)
   - Purple gradient left border
   - Formatted markdown output (bold, bullets, emojis supported)
   - Feedback row: thumbs up / thumbs down + "Regenerate" button

8. **Toast / Notification System**
   - Bottom-right toast stack
   - Types: success (green glow), error (red glow), info (blue glow)
   - Slide-in + auto-dismiss with progress bar

9. **LoadingState / Skeleton**
   - Global AI loading overlay: centered spinner with "🤖 Consulting AI..." text
   - Pulsing animation with purple/orange gradient ring

10. **ThemeToggle** (optional secondary light mode)
    - Moon/sun icon toggle in navbar
    - Smooth CSS variable transition on toggle

---

📐 LAYOUT & RESPONSIVENESS
- Desktop: 3-column grid, sidebar visible
- Tablet: 2-column grid, sidebar collapses to filter button
- Mobile: 1-column, bottom sheet filter drawer

---

✨ MICRO-INTERACTIONS & ANIMATIONS
- Search bar focus: border glows orange, slight scale(1.01)
- Card hover: translateY(-4px) + glow border
- Filter pill toggle: scale bounce + color fill
- AI panel: typewriter text streaming
- Button hover: shimmer sweep animation
- Page load: staggered fade-up for cards (0, 50ms, 100ms, 150ms delays)
- Heart icon: scale pop + fill animation

---

🖼️ OUTPUT FORMAT
Generate:
1. Full desktop screen (1440px wide) — main search + results view
2. RestaurantCard component — isolated, hover state shown
3. FilterPanel — open state
4. AIResponsePanel — with streaming text shown
5. Mobile view (390px) — search + 1-column results

Use realistic dummy data:
- Restaurant names: "Spice Garden", "The Curry House", "Biryani Bros"
- Cuisines: Indian, South Indian, Biryani
- Location: Koramangala, Bangalore
- Ratings: 4.2 ⭐, 4.5 ⭐, 3.9 ⭐
- Prices: ₹250, ₹400, ₹180
