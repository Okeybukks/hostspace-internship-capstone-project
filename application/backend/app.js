const express = require('express');
const path = require('path');
const cookieParser = require('cookie-parser');
const logger = require('morgan');
const cors = require('cors')

const app = express();

// Middleware for setting custom headers globally
app.use((req, res, next) => {
    // Set ngrok-skip-browser-warning header
    res.setHeader('ngrok-skip-browser-warning', 'true');
  
    // Set custom User-Agent header
    res.setHeader('User-Agent', 'Custom-User-Agent/1.0');
  
    // Allow all origins for CORS (replace '*' with your specific origins if needed)
    res.setHeader('Access-Control-Allow-Origin', '*');
  
    // Continue with the request handling
    next();
  });
  
app.use(cors())
app.use(logger('dev'));
app.use(express.json());
app.use(express.urlencoded({ extended: false }));
app.use(cookieParser());
app.use(express.static(path.join(__dirname, 'public')));
app.use('/api/v1', require('./src/v1/routes'));

module.exports = app;
