const express = require('express');
const path = require('path');

const app = express();

// Middleware
app.use(express.urlencoded({ extended: false }));
app.use(express.json());
app.use(express.static(path.join(__dirname, 'public')));

// Configure View Engine
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// Utility: Sanitize string inputs to prevent XSS
const sanitize = (str) => {
  if (typeof str !== 'string') return '';
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
};

// Git Commit ID Resolution
const getCommitSha = () => {
  const sha = process.env.GIT_SHA || process.env.RENDER_GIT_COMMIT || 'local';
  return sha.slice(0, 7);
};

// In-Memory Data Store for Cosarc Discipline Contracts
let contracts = [
  {
    id: 'c-1',
    title: 'Morning Cyber Workout',
    category: 'Workout',
    target: '45 mins High Intensity Strength',
    status: 'Completed',
    rating: 5,
    createdAt: new Date(Date.now() - 86400000).toISOString()
  },
  {
    id: 'c-2',
    title: 'Hydration Protocol',
    category: 'Hydration',
    target: '3.5 Liters Pure Water',
    status: 'Completed',
    rating: 5,
    createdAt: new Date(Date.now() - 43200000).toISOString()
  },
  {
    id: 'c-3',
    title: 'High-Protein Fuel Plan',
    category: 'Fuel',
    target: '180g Protein / 2400 kcal',
    status: 'In Progress',
    rating: 4,
    createdAt: new Date(Date.now() - 10800000).toISOString()
  },
  {
    id: 'c-4',
    title: 'Mindset & Recovery Session',
    category: 'Mindset',
    target: '15 mins Meditation & Cold Bath',
    status: 'Completed',
    rating: 5,
    createdAt: new Date().toISOString()
  }
];

// Helper: Calculate live statistics
const calculateStats = (data) => {
  const total = data.length;
  const completed = data.filter((item) => item.status === 'Completed').length;
  const completionRate = total > 0 ? Math.round((completed / total) * 100) : 0;
  const totalRating = data.reduce((acc, item) => acc + (Number(item.rating) || 0), 0);
  const avgRating = total > 0 ? (totalRating / total).toFixed(1) : '0.0';

  return { total, completed, completionRate, avgRating };
};

// Route: Home Page (Dynamic Server-Side Rendering)
app.get('/', (req, res) => {
  const commit = getCommitSha();
  const stats = calculateStats(contracts);
  const error = req.query.error ? sanitize(req.query.error) : null;
  const success = req.query.success ? sanitize(req.query.success) : null;

  res.render('index', {
    contracts,
    stats,
    commit,
    error,
    success,
    sanitize
  });
});

// Route: POST /contracts (Add new discipline contract with input validation)
app.post('/contracts', (req, res) => {
  const title = (req.body.title || '').trim();
  const category = (req.body.category || '').trim();
  const target = (req.body.target || '').trim();
  const status = (req.body.status || 'Pending').trim();
  const rating = parseInt(req.body.rating, 10);

  const allowedCategories = ['Workout', 'Fuel', 'Hydration', 'Mindset'];
  const allowedStatuses = ['Pending', 'In Progress', 'Completed'];

  // Input Validation Quality Gate
  if (!title || !category || !target) {
    if (req.headers['accept']?.includes('application/json')) {
      return res.status(400).json({ error: 'Title, category, and target are required fields.' });
    }
    return res.status(400).send('Title, category, and target are required fields.');
  }

  if (!allowedCategories.includes(category)) {
    if (req.headers['accept']?.includes('application/json')) {
      return res.status(400).json({ error: `Invalid category. Must be one of: ${allowedCategories.join(', ')}` });
    }
    return res.status(400).send(`Invalid category. Must be one of: ${allowedCategories.join(', ')}`);
  }

  if (!allowedStatuses.includes(status)) {
    if (req.headers['accept']?.includes('application/json')) {
      return res.status(400).json({ error: `Invalid status. Must be one of: ${allowedStatuses.join(', ')}` });
    }
    return res.status(400).send(`Invalid status. Must be one of: ${allowedStatuses.join(', ')}`);
  }

  if (isNaN(rating) || rating < 1 || rating > 5) {
    if (req.headers['accept']?.includes('application/json')) {
      return res.status(400).json({ error: 'Rating must be an integer between 1 and 5.' });
    }
    return res.status(400).send('Rating must be an integer between 1 and 5.');
  }

  // Create new contract record
  const newContract = {
    id: `c-${Date.now().toString(36)}`,
    title: sanitize(title),
    category: sanitize(category),
    target: sanitize(target),
    status: sanitize(status),
    rating,
    createdAt: new Date().toISOString()
  };

  contracts.unshift(newContract);

  if (req.headers['accept']?.includes('application/json')) {
    return res.status(201).json(newContract);
  }

  res.redirect('/?success=' + encodeURIComponent('Discipline contract successfully added!'));
});

// Route: POST /contracts/:id/delete (Delete contract)
app.post('/contracts/:id/delete', (req, res) => {
  const { id } = req.params;
  const initialLength = contracts.length;
  contracts = contracts.filter((c) => c.id !== id);

  if (contracts.length === initialLength) {
    return res.status(404).send('Contract not found');
  }

  res.redirect('/?success=' + encodeURIComponent('Contract removed.'));
});

// Route: GET /api/contracts (JSON API Route)
app.get('/api/contracts', (req, res) => {
  res.json({
    count: contracts.length,
    stats: calculateStats(contracts),
    contracts
  });
});

// Route: GET /health (Health Check for CI/CD Smoke Testing & Docker)
app.get('/health', (req, res) => {
  const commit = getCommitSha();
  res.json({
    status: 'ok',
    commit,
    uptime: process.uptime(),
    timestamp: new Date().toISOString()
  });
});

// Export functions for testing
app.resetStore = () => {
  contracts = [
    {
      id: 'c-1',
      title: 'Morning Cyber Workout',
      category: 'Workout',
      target: '45 mins High Intensity Strength',
      status: 'Completed',
      rating: 5,
      createdAt: new Date().toISOString()
    }
  ];
};

module.exports = app;
