import { spawn } from 'child_process';

console.log('Starting Python Flask server directly...');

const pythonProcess = spawn('python', ['start_python_server.py'], {
  stdio: 'inherit',
  cwd: process.cwd()
});

pythonProcess.on('close', (code) => {
  console.log(`Python process exited with code ${code}`);
  process.exit(code || 0);
});

pythonProcess.on('error', (err) => {
  console.error('Failed to start Python process:', err);
  process.exit(1);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  pythonProcess.kill();
});

process.on('SIGINT', () => {
  pythonProcess.kill();
});