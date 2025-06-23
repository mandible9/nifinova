import express from 'express';
import { spawn } from 'child_process';
import type { ChildProcess } from 'child_process';

const app = express();

// Middleware
app.use(express.json());
app.use(express.static('static'));

// Start Python Flask server as a subprocess
let pythonProcess: ChildProcess | null = null;

function startPythonServer() {
  console.log('Starting Python Flask server...');
  pythonProcess = spawn('python', ['start_python_server.py'], {
    stdio: 'inherit',
    cwd: process.cwd()
  });

  pythonProcess.on('close', (code: number | null) => {
    console.log(`Python process exited with code ${code}`);
  });

  pythonProcess.on('error', (err: Error) => {
    console.error('Failed to start Python process:', err);
  });
}

// Proxy all requests to Python Flask server
app.use('/', async (req, res) => {
  try {
    const url = `http://localhost:5001${req.path}`;
    const response = await fetch(url, {
      method: req.method,
      headers: {
        'Content-Type': 'application/json',
        ...req.headers
      },
      body: req.method !== 'GET' && req.method !== 'HEAD' ? JSON.stringify(req.body) : undefined
    });

    const contentType = response.headers.get('content-type');
    
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      res.status(response.status).json(data);
    } else {
      const text = await response.text();
      res.status(response.status).send(text);
    }
  } catch (error) {
    console.error('Proxy error:', error);
    res.status(503).json({ 
      error: 'Service temporarily unavailable',
      message: 'Python Flask server is starting up...'
    });
  }
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('Shutting down...');
  if (pythonProcess) {
    pythonProcess.kill();
  }
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('Shutting down...');
  if (pythonProcess) {
    pythonProcess.kill();
  }
  process.exit(0);
});

// Start Python server
startPythonServer();

const PORT = 5000;
app.listen(PORT, '0.0.0.0', () => {
  console.log(`Node.js proxy server running on port ${PORT}`);
  console.log('Python Flask server starting as subprocess...');
});