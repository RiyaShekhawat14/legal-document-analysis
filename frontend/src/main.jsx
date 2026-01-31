import React from 'react'
import ReactDOM from 'react-dom/client'
import "./styles/index.css"
import LanguageProvider from './context/LanguageContext'
import { UserProvider } from './context/UserContext'
import { DocumentProvider } from './context/DocumentContext'
import AppRoutes from './routes'


ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <LanguageProvider>
      <UserProvider>
        <DocumentProvider>
          <AppRoutes/>
        </DocumentProvider>
      </UserProvider>
    </LanguageProvider>
  </React.StrictMode>
);
