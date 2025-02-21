# E-Commerce Web Application

This is a React-based e-commerce web application that provides both internal and external user interfaces along with administrative functionalities.

## Features

- User Authentication (Login System)
- Internal User Interface
- External User Interface
- Administrative Dashboard with:
  - Order Tracking
  - Order Entry System
  - Purchase Order Upload

## Project Structure

The application is organized with the following main components:

- `src/App.js` - Main application router
- `src/components/Header` - Navigation header component
- `src/pages/`
  - `LoginPage` - User authentication
  - `MainExternal` - External user interface
  - `MainInternal` - Internal user interface
  - `adminview/`
    - `OrderEntryAdmin` - Admin order entry interface
    - `OrderRecords` - Order tracking system
    - `POuploadAdmin` - Purchase order upload system

## Dependencies

Major dependencies include:

- React v19.0.0
- React Router DOM v7.1.5
- React Bootstrap v2.10.9
- Bootstrap v5.3.3
- Axios v1.7.9
- Framer Motion v12.4.0
- React DnD v16.0.1
- XLSX v0.18.5

## Getting Started

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm start
```

The application will be available at `http://localhost:3000`

## Available Scripts

- `npm start` - Runs the app in development mode
- `npm test` - Launches the test runner
- `npm run build` - Builds the app for production
- `npm run eject` - Ejects from create-react-app

## Browser Support

### Production
- Browser market share > 0.2%
- Not dead
- Not Opera Mini

### Development
- Latest versions of:
  - Chrome
  - Firefox
  - Safari
