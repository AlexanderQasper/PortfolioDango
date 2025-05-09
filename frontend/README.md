# Portfolio Frontend

A modern React frontend for the Portfolio Django application. Built with Vite, React, TypeScript, TailwindCSS, and React Router.

## Features

- JWT Authentication with automatic token refresh
- Protected routes
- File upload and management
- Dark mode support
- Responsive design

## Prerequisites

- Node.js 16.x or later
- npm 7.x or later
- Running Django backend on `http://localhost:8000`

## Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

The application will be available at `http://localhost:5173`.

## Development

- The frontend is built with Vite for fast development and optimized builds
- TailwindCSS is used for styling with dark mode support
- React Router handles client-side routing
- Axios is configured for API requests with JWT authentication
- TypeScript ensures type safety

## Project Structure

```
frontend/
├── src/
│   ├── components/     # Reusable components
│   ├── contexts/       # React contexts (auth, etc.)
│   ├── lib/           # Utility functions and configurations
│   ├── pages/         # Page components
│   └── App.tsx        # Main application component
├── public/            # Static assets
└── index.html         # Entry HTML file
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking
