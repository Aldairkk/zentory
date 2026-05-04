# SaaS Inventory Dashboard - Specification

## Project Overview
- **Project Name**: Zentory Inventory Dashboard
- **Type**: Single-page SaaS webapp mockup
- **Core Functionality**: Modern inventory management dashboard with clean fintech aesthetic
- **Target Users**: Business managers, warehouse staff, inventory controllers

## UI/UX Specification

### Layout Structure

**Page Sections**:
1. **Sidebar** (fixed left, 240px width)
2. **Main Area** (flex: 1, contains header + content)
   - Header (64px height)
   - Content (flex: 1, padding 24px)

**Grid/Flex Layout**:
- Sidebar: Fixed width 240px, flex-column
- Main: flex: 1, flex-column
- Content area: max-width 1400px, centered

**Responsive Breakpoints**:
- Desktop: 1200px+ (full sidebar)
- Tablet: 768px-1199px (collapsible sidebar)
- Mobile: <768px (hidden sidebar, hamburger menu)

### Visual Design

**Color Palette**:
- Primary Blue: #2563EB
- Primary Blue Hover: #1D4ED8
- Sidebar Background: #1E3A5F
- Sidebar Text: #94A3B8
- Sidebar Active: #FFFFFF
- Main Background: #F8FAFC
- Card Background: #FFFFFF
- Text Primary: #0F172A
- Text Secondary: #64748B
- Text Muted: #94A3B8
- Border: #E2E8F0
- Success: #10B981
- Success BG: #ECFDF5
- Warning: #F59E0B
- Warning BG: #FFFBEB
- Danger: #EF4444
- Danger BG: #FEF2F2
- Gray: #64748B
- Gray BG: #F1F5F9

**Typography**:
- Font Family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif
- Title (H1): 24px, 700 weight
- Heading (H2): 18px, 600 weight
- Body: 14px, 400 weight
- Small: 12px, 400 weight
- Table: 13px, 400 weight

**Spacing System**:
- Base unit: 4px
- XS: 4px
- SM: 8px
- MD: 12px
- LG: 16px
- XL: 24px
- 2XL: 32px
- Card padding: 24px
- Section gap: 24px

**Visual Effects**:
- Card shadow: 0 1px 3px rgba(0,0,0,0.05), 0 1px 2px rgba(0,0,0,0.1)
- Card shadow hover: 0 4px 12px rgba(0,0,0,0.1)
- Sidebar shadow: 0 0 40px rgba(0,0,0,0.2)
- Border radius cards: 12px
- Border radius buttons: 8px
- Border radius pills: 20px (full)
- Border radius inputs: 8px
- Border radius tags: 16px
- Transitions: all 0.2s ease

### Components

**Sidebar**:
- Logo area at top (40px height logo)
- Navigation items with icons
- Active item: white text, left border accent
- Hover: subtle background highlight
- Icons: 20px, stroke style

**Header**:
- Title "Inventario" left aligned
- User profile right (avatar + name)
- Background white, bottom border

**Filter Section**:
- Pill buttons in horizontal row
- Inactive: #F1F5F9 background, #64748B text
- Active: #2563EB background, #FFFFFF text
- Hover: slight background darken

**Search Bar**:
- Rounded input (8px radius)
- Search icon left side
- Placeholder text
- Background #F8FAFC
- Border on focus

**Action Buttons**:
- Primary (Nuevo Ingreso): #2563EB bg, white text, solid
- Secondary (Exportar): transparent bg, #2563EB border/text, outlined
- Danger (Eliminar): #FEF2F2 bg, #EF4444 text, outlined soft

**Data Table**:
- Header: #F8FAFC background, 600 weight
- Rows: alternating white/#F8FAFC (zebra)
- Hover: subtle blue tint
- Status tags: rounded full, colored bg variants
- Numbers: right aligned
- Minimal borders between rows

**Animations**:
- Button hover: translateY(-1px), enhanced shadow
- Card hover: enhanced shadow
- Table row hover: background transition
- Page load: fade in, subtle slide up
- Staggered delays for content

## Functionality Specification

### Core Features
1. Sidebar navigation with Icons (Dashboard, Productos, Ingresos, Proveedores, Reportes, Configuración)
2. Search functionality (UI only)
3. Filter pills (Todos, En Stock, Bajo Stock, Agotado)
4. Action buttons (Nuevo Ingreso, Exportar, Eliminar)
5. Sortable table columns (mock UI)
6. Status badges with color variants
7. User profile dropdown (UI only)

### User Interactions
- Hover states on all interactive elements
- Active states for filters and nav items
- Focus states for inputs
- Visual feedback on buttons

### Data (Mock)
- Table rows: 10 sample products
- Categories: Electrónica, Ropa, Alimentos, Hogar
- Statuses: En Stock (green), Bajo Stock (yellow), Agotado (gray)

## Acceptance Criteria

1. ✓ Sidebar displays correctly at 240px with dark blue (#1E3A5F) background
2. ✓ Active nav item shows white text with accent highlight
3. ✓ Header shows "Inventario" title and user avatar profile
4. ✓ Main content area has white cards on #F8FAFC background
5. ✓ Filter pills demonstrate active/inactive states with blue accent
6. ✓ Search bar has rounded edges and focus states
7. ✓ Primary, Secondary, Danger buttons styled correctly
8. ✓ Table displays zebra rows with hover effects
9. ✓ Status tags show correct color variants
10. ✓ Numbers right-aligned in table
11. ✓ Soft shadows and rounded corners throughout
12. ✓ Inter font family applied
13. ✓ Smooth animations on interactions
14. ✓ Professional fintech SaaS aesthetic achieved