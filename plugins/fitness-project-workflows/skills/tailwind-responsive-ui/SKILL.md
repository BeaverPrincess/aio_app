---
name: tailwind-responsive-ui
description: Build and review responsive, accessible React UI with Tailwind CSS 4 in this frontend. Use for layout, visual components, responsive behavior, design tokens, and interaction states; do not use for non-visual data or route decisions alone.
---

# Tailwind responsive UI workflow

## Responsive composition

- Design the narrow-screen layout first with unprefixed utilities. Add `sm:`, `md:`, `lg:`, and larger variants only to enhance layouts at and above their breakpoints.
- Prefer flexible widths, sensible maximum content widths, and layouts that work at intermediate viewport sizes; do not target only named devices.
- Use container queries when a reusable component responds to its parent width rather than the viewport.
- Verify interactive screens at a narrow mobile width and a desktop width before handoff.

## Tailwind usage

- Keep utility class names complete and statically detectable. Select whole class strings from a mapping when a variant is dynamic; never build class names such as `bg-${color}-500`.
- Use Tailwind utilities for ordinary styling. Add custom CSS only for global base styles, declared design tokens, or a CSS capability that Tailwind cannot express clearly.
- Establish shared theme tokens before repeating arbitrary colors, dimensions, or breakpoints across components.
- Keep long class lists readable by grouping layout, spacing, typography, color, and state variants consistently.

## Accessible interaction

- Prefer semantic HTML and native controls. Every form field needs an associated label; icon-only controls need an accessible name.
- Make keyboard focus visible and preserve focus, hover, disabled, loading, and error states where relevant.
- Do not rely on color alone to communicate state. Ensure touch controls have an appropriately usable target size.

## References

- Responsive design: https://tailwindcss.com/docs/responsive-design
- Utility classes: https://tailwindcss.com/docs/styling-with-utility-classes
- Theme variables: https://tailwindcss.com/docs/theme
