# E-Commerce Web Application

A modern React-based web application for managing purchase orders, order tracking, and e-commerce operations with separate interfaces for administrators and regular users.

## 📸 Screenshots

### Login Page
![image](https://github.com/user-attachments/assets/e544118b-42b8-4d09-94a5-259e4e9139c6)


### Admin Dashboard
![image](https://github.com/user-attachments/assets/628d83f4-15a9-4372-a52a-860f3442ef90)


### Admin Purchase Order Upload
![image](https://github.com/user-attachments/assets/ceb87eec-96b5-47da-9d22-27a56d14514e)


###  Admin Purchase Order Upload Process
![image](https://github.com/user-attachments/assets/d942b41a-ff8d-43bf-ad7c-f8b0dfc7f89d)

###  Non-Admin Order Upload
![image](https://github.com/user-attachments/assets/632afb73-7f80-485e-bf38-7e4c95b48010)


## 🚀 Features

### User Authentication
- Secure login system with role-based access control
- Separate interfaces for administrators and regular users
- Session management for persistent login

### Admin Features
- **Dashboard**: Overview of system activity and key metrics
- **Purchase Order Processing**: Upload, view, and process purchase orders
  - PDF file upload with multi-file support
  - Automatic extraction of order details
  - Manual editing capabilities for extracted data
  - Customer-specific processing rules
- **Order Entry**: Create and manage orders directly in the system
- **Order Tracking**: Monitor status of all orders in the system

### User Features
- **Purchase Order Upload**: Submit purchase orders for processing
- **Order History**: View past and current orders
- **Order Status Tracking**: Monitor the progress of submitted orders

### PDF Processing Integration
- Seamless integration with backend PDF processing API
- Support for various purchase order formats
- Real-time feedback on processing status

## 🛠️ Technology Stack

### Frontend
- **React 19**: Latest version of the React library for building user interfaces
- **React Router 7**: For application routing and navigation
- **React Bootstrap**: UI component library based on Bootstrap
- **Axios**: HTTP client for API requests
- **XLSX**: For Excel file processing
- **React DnD**: For drag-and-drop functionality
- **Framer Motion**: For smooth animations and transitions

### Backend Integration
- RESTful API integration with Flask backend
- PDF processing capabilities
- Customer data management

## 🏗️ Project Structure

```
ecom_web/
├── public/             # Static files
├── src/                # Source code
│   ├── apipost/        # API integration utilities
│   ├── components/     # Reusable UI components
│   │   ├── AlertMessage.js
│   │   ├── Footer.js
│   │   ├── Header.js
│   │   └── Product.js
│   ├── data/           # Static data and mock data
│   ├── pages/          # Application pages
│   │   ├── LoginPage.js
│   │   ├── MainExternal.js
│   │   ├── MainInternal.js
│   │   ├── adminview/  # Admin-specific pages
│   │   │   ├── AdminDashboard.js
│   │   │   ├── OrderEntryAdmin.js
│   │   │   ├── OrderRecords.js
│   │   │   └── POuploadAdmin.js
│   │   └── userview/   # User-specific pages
│   │       ├── HomePage.js
│   │       ├── OrderRecords.js
│   │       └── POupload.js
│   ├── App.js          # Main application component
│   ├── index.js        # Application entry point
│   └── users.js        # User management utilities
└── package.json        # Project dependencies and scripts
```

## 📋 Application Flow

1. **Authentication**: Users log in through the LoginPage component
2. **Role-Based Routing**: 
   - Administrators are directed to the admin interface
   - Regular users are directed to the user interface
3. **Purchase Order Processing**:
   - User uploads PDF purchase orders
   - System processes the PDFs and extracts relevant information
   - User reviews and can edit the extracted information
   - User submits the processed information to the system
4. **Order Tracking**:
   - Users can view the status of their orders
   - Administrators can view and manage all orders in the system

## 🔄 Purchase Order Processing Workflow

### Admin Workflow
1. Select customer from dropdown
2. View customer-specific shipping information
3. Upload one or more PDF purchase orders
4. System processes the PDFs and extracts order details
5. Review extracted information in a tabular format
6. Edit information if necessary
7. View original PDF for verification
8. Submit processed orders to the system

### User Workflow
1. Upload purchase order PDF(s)
2. System processes the PDFs
3. Review extracted information
4. Submit order for processing

## 📸 Key UI Components

### Header Component
[Add screenshot of header component here]

The Header component provides navigation and user information across the application.

### Purchase Order Upload
[Add screenshot of PO upload component here]

The PO upload component allows users to upload and process purchase order PDFs.

### Order Records Table
[Add screenshot of order records table here]

The Order Records component displays order information in a sortable, filterable table.

## 🚀 Getting Started

### Prerequisites
- Node.js 16.x or higher
- npm 8.x or higher

### Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd ecom_web
   ```

2. Install dependencies:
   ```
   npm install
   ```

3. Start the development server:
   ```
   npm start
   ```

4. Open your browser and navigate to:
   ```
   http://localhost:3000
   ```

### Building for Production

```
npm run build
```

This creates an optimized production build in the `build` folder.

## 🔌 Backend Integration

This frontend application integrates with a Flask backend API for PDF processing and data management. The backend provides the following endpoints:

- `/api/process-purchase-order`: Processes uploaded PDF purchase orders
- `/api/customers`: Retrieves the list of available customers
- `/api/customer-ship-to/:customer`: Retrieves shipping information for a specific customer

## 🧩 Extending the Application

### Adding New Features
1. Create new components in the appropriate directories
2. Update routing in App.js
3. Integrate with backend API as needed

### Adding New Customer Types
The system supports customer-specific processing rules. To add a new customer:

1. Update the backend API to support the new customer
2. The frontend will automatically include the new customer in the dropdown

## 📝 Development Notes

### State Management
- Component-level state using React hooks
- Props for component communication
- Context API for global state (authentication, etc.)

### API Integration
- Axios for HTTP requests
- Error handling with try/catch blocks
- Loading states for better user experience

### Responsive Design
- Bootstrap Grid System
- Media queries for custom responsive behavior
- Mobile-first approach

## 🔒 Security Considerations

- Authentication token management
- Role-based access control
- Input validation
- Secure API communication

## 🔮 Future Enhancements

- Enhanced data visualization
- Batch processing improvements
- Integration with additional backend services
- Advanced search and filtering capabilities
- Export functionality for reports
