import { useState, useEffect } from 'react';
import { appWindow } from '@tauri-apps/api/window';

function App() {
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Setup for window controls
    const handleWindowControls = async () => {
      document.getElementById('titlebar-minimize')?.addEventListener('click', () => appWindow.minimize());
      document.getElementById('titlebar-maximize')?.addEventListener('click', () => appWindow.toggleMaximize());
      document.getElementById('titlebar-close')?.addEventListener('click', () => appWindow.close());
    };
    
    handleWindowControls();
    
    // The frontend is loaded in an iframe to reuse your existing React application
    const iframe = document.getElementById('frontend-iframe') as HTMLIFrameElement;
    
    iframe.onload = () => {
      setIsLoading(false);
    };
    
    // Load frontend URL
    iframe.src = 'http://frontend:80';
  }, []);

  return (
    <div className="container">
      <div className="titlebar">
        <div className="titlebar-drag-region">Poly Micro Manager</div>
        <div className="titlebar-controls">
          <button id="titlebar-minimize">—</button>
          <button id="titlebar-maximize">□</button>
          <button id="titlebar-close">×</button>
        </div>
      </div>
      
      <div className="content">
        {isLoading && (
          <div className="loading">
            <p>Loading application...</p>
          </div>
        )}
        <iframe 
          id="frontend-iframe" 
          className={isLoading ? 'hidden' : ''}
          title="Poly Micro Manager"
          allow="fullscreen"
        />
      </div>
    </div>
  );
}

export default App;
